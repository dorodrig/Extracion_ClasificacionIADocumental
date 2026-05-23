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
