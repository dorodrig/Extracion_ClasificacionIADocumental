"""
Repositorio de acceso a datos para Reglas de Trabajo.

Gobernanza §5.4 — Patrón Repository: un repositorio por entidad de dominio.
Gobernanza §3.4 — Clean Architecture: separación Repository/Service.

R-03 Mitigación: Todas las operaciones de escritura usan transacciones
atómicas con try/commit/except/rollback.
"""
import json
import logging
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.rule_db import ReglasTrabajo
from app.db.models.rule_history_db import ReglasTrabajoHistorial

logger = logging.getLogger("grm.rule_repository")


class RuleRepository:
    """
    Repositorio para operaciones CRUD de reglas de trabajo.

    Encapsula todo el acceso a la tabla reglas_trabajo.
    Los endpoints y servicios NUNCA deben ejecutar SQL directo.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de BD.

        Args:
            db: Sesión activa de SQLAlchemy.
        """
        self.db = db

    def get_by_client(self, client_id: int) -> list[ReglasTrabajo]:
        """
        Obtiene todas las reglas activas de un cliente, ordenadas por
        fecha de creación descendente.

        CA-01: Retorna lista vacía si no hay reglas.
        CA-02: Retorna lista completa con campos base.

        Args:
            client_id: ID del cliente.

        Returns:
            Lista de reglas del cliente (puede ser vacía).
        """
        logger.info("Consultando reglas para cliente_id=%d", client_id)
        return (
            self.db.query(ReglasTrabajo)
            .filter(
                ReglasTrabajo.cliente_id == client_id,
                ReglasTrabajo.activa == True,
            )
            .order_by(ReglasTrabajo.created_at.desc())
            .all()
        )

    def get_by_id(self, rule_id: int) -> ReglasTrabajo | None:
        """
        Obtiene una regla por su ID.

        CA-03: Retorna el detalle completo de la regla.

        Args:
            rule_id: ID de la regla.

        Returns:
            La regla encontrada o None si no existe.
        """
        logger.info("Consultando regla id=%d", rule_id)
        return (
            self.db.query(ReglasTrabajo)
            .filter(
                ReglasTrabajo.id == rule_id,
                ReglasTrabajo.activa == True,
            )
            .first()
        )

    def exists_by_name_and_client(
        self, nombre: str, cliente_id: int, exclude_id: int | None = None
    ) -> bool:
        """
        Verifica si ya existe una regla con el mismo nombre para un cliente.

        Args:
            nombre: Nombre de la regla a verificar.
            cliente_id: ID del cliente.
            exclude_id: ID de regla a excluir de la búsqueda (para updates).

        Returns:
            True si ya existe una regla con ese nombre.
        """
        query = self.db.query(ReglasTrabajo).filter(
            func.lower(ReglasTrabajo.nombre) == nombre.strip().lower(),
            ReglasTrabajo.cliente_id == cliente_id,
            ReglasTrabajo.activa == True,
        )
        if exclude_id is not None:
            query = query.filter(ReglasTrabajo.id != exclude_id)
        return query.first() is not None

    def create(self, rule_data: dict) -> ReglasTrabajo:
        """
        Crea una nueva regla de trabajo en la base de datos.

        CA-04: Genera ID automáticamente (IDENTITY).
        R-03 Mitigación: Transacción atómica con rollback en caso de error.

        Args:
            rule_data: Diccionario con los campos de la regla.
                       campos_extraer debe ser una lista de dicts.

        Returns:
            La regla recién creada con su ID generado.

        Raises:
            Exception: Re-lanza cualquier error tras hacer rollback.
        """
        logger.info(
            "Creando regla '%s' para cliente_id=%d",
            rule_data.get("nombre"),
            rule_data.get("cliente_id"),
        )
        # Serializar campos_extraer a JSON string para almacenar en BD
        data = {**rule_data}
        if isinstance(data.get("campos_extraer"), list):
            data["campos_extraer"] = json.dumps(
                data["campos_extraer"], ensure_ascii=False
            )

        db_rule = ReglasTrabajo(**data)
        try:
            self.db.add(db_rule)
            self.db.commit()
            self.db.refresh(db_rule)
            logger.info("Regla creada exitosamente: id=%d", db_rule.id)
            return db_rule
        except Exception as e:
            self.db.rollback()
            logger.error("Error al crear regla: %s", str(e))
            raise

    def save_history_snapshot(self, db_rule: ReglasTrabajo, modified_by: int | None = None) -> None:
        """
        Guarda un snapshot del estado actual de la regla en el historial.

        CA-10: Mantiene versiones anteriores de las reglas.
        
        Args:
            db_rule: Instancia de la regla a respaldar.
            modified_by: ID del usuario que modifica.
        """
        snapshot = {
            "id": db_rule.id,
            "cliente_id": db_rule.cliente_id,
            "nombre": db_rule.nombre,
            "tipo_documento": db_rule.tipo_documento,
            "campos_extraer": json.loads(db_rule.campos_extraer) if isinstance(db_rule.campos_extraer, str) else db_rule.campos_extraer,
            "patron_carpeta": db_rule.patron_carpeta,
            "modo_entrada": db_rule.modo_entrada,
            "umbral_ocr": db_rule.umbral_ocr,
            "version": db_rule.version,
            "activa": db_rule.activa,
            "created_by": db_rule.created_by,
            "created_at": db_rule.created_at.isoformat() if db_rule.created_at else None,
            "updated_at": db_rule.updated_at.isoformat() if db_rule.updated_at else None,
        }

        historial = ReglasTrabajoHistorial(
            regla_id=db_rule.id,
            version=db_rule.version,
            snapshot_json=json.dumps(snapshot, ensure_ascii=False),
            modificado_por=modified_by,
        )
        self.db.add(historial)
        self.db.flush()

    def update(self, rule_id: int, rule_data: dict) -> ReglasTrabajo | None:
        """
        Actualiza una regla de trabajo existente.

        Incrementa automáticamente el campo version.
        R-03 Mitigación: Transacción atómica con rollback en caso de error.

        Args:
            rule_id: ID de la regla a actualizar.
            rule_data: Diccionario con los campos a actualizar.

        Returns:
            La regla actualizada o None si no se encontró.

        Raises:
            Exception: Re-lanza cualquier error tras hacer rollback.
        """
        logger.info("Actualizando regla id=%d", rule_id)
        db_rule = self.get_by_id(rule_id)
        if db_rule is None:
            return None

        # Serializar campos_extraer a JSON string
        data = {**rule_data}
        if isinstance(data.get("campos_extraer"), list):
            data["campos_extraer"] = json.dumps(
                data["campos_extraer"], ensure_ascii=False
            )

        try:
            # Guardar historial ANTES de aplicar los cambios (CA-10)
            self.save_history_snapshot(db_rule)

            for key, value in data.items():
                setattr(db_rule, key, value)

            # Auto-incrementar version
            db_rule.version = (db_rule.version or 1) + 1
            db_rule.updated_at = datetime.now()

            self.db.commit()
            self.db.refresh(db_rule)
            logger.info(
                "Regla id=%d actualizada a version=%d",
                db_rule.id,
                db_rule.version,
            )
            return db_rule
        except Exception as e:
            self.db.rollback()
            logger.error("Error al actualizar regla id=%d: %s", rule_id, str(e))
            raise

    def duplicate(self, rule_id: int, new_name: str) -> ReglasTrabajo | None:
        """
        Duplica una regla existente con un nuevo nombre.

        CA-11: Clona la regla reiniciando versión y timestamps.

        Args:
            rule_id: ID de la regla a duplicar.
            new_name: Nuevo nombre asignado.

        Returns:
            La nueva regla creada o None si no existe la original.
        """
        db_rule = self.get_by_id(rule_id)
        if db_rule is None:
            return None

        campos_str = db_rule.campos_extraer
        campos = json.loads(campos_str) if isinstance(campos_str, str) else campos_str
        
        # Copia profunda forzada
        campos_clonados = json.loads(json.dumps(campos))

        rule_data = {
            "cliente_id": db_rule.cliente_id,
            "nombre": new_name,
            "tipo_documento": db_rule.tipo_documento,
            "campos_extraer": campos_clonados,
            "patron_carpeta": db_rule.patron_carpeta,
            "modo_entrada": db_rule.modo_entrada,
            "umbral_ocr": db_rule.umbral_ocr,
        }

        # self.create() maneja el commit y transacciones
        return self.create(rule_data)
