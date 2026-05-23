"""
Servicio de aplicación para Reglas de Trabajo.

Gobernanza §2.2 — app/services/rules_service.py
Gobernanza §3.4 — Clean Architecture: capa de aplicación (Use Cases).

Orquesta validaciones de dominio y operaciones de repositorio.
"""
import json
import logging

from sqlalchemy.orm import Session

from app.db.models.rule_db import ReglasTrabajo
from app.db.repositories.rule_repository import RuleRepository
from app.domain.exceptions import (
    RuleNameAlreadyExistsException,
    RuleNotFoundException,
)
from app.domain.rules.rule_validation import validate_rule_data
from app.schemas.rule_schema import (
    CampoExtraerSchema,
    RuleCreate,
    RuleResponse,
    RuleUpdate,
)

logger = logging.getLogger("grm.rule_service")


class RuleService:
    """
    Servicio de aplicación (Use Case) para la gestión de Reglas de Trabajo.

    Responsabilidades:
        - Orquestar validaciones de dominio antes de persistir.
        - Transformar entre schemas Pydantic y datos de repositorio.
        - Serializar/deserializar campos_extraer (JSON ↔ lista).

    Esta clase NO accede directamente a la BD; delega al RuleRepository.
    """

    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de BD.

        Args:
            db: Sesión activa de SQLAlchemy.
        """
        self.repository = RuleRepository(db)

    def _parse_campos_extraer(self, db_rule: ReglasTrabajo) -> list[dict]:
        """
        Deserializa el campo campos_extraer de JSON string a lista de dicts.

        Args:
            db_rule: Instancia del modelo ORM con campos_extraer como string.

        Returns:
            Lista de diccionarios representando los campos a extraer.

        Raises:
            ValueError: Si el JSON almacenado es inválido.
        """
        if isinstance(db_rule.campos_extraer, str):
            try:
                return json.loads(db_rule.campos_extraer)
            except json.JSONDecodeError as e:
                logger.error(
                    "JSON inválido en campos_extraer de regla id=%d: %s",
                    db_rule.id,
                    str(e),
                )
                return []
        return db_rule.campos_extraer if db_rule.campos_extraer else []

    def _to_response(self, db_rule: ReglasTrabajo) -> RuleResponse:
        """
        Convierte un modelo ORM a schema de respuesta Pydantic.

        Deserializa campos_extraer de JSON string a lista de CampoExtraerSchema.

        Args:
            db_rule: Instancia del modelo ORM.

        Returns:
            RuleResponse con todos los campos serializados correctamente.
        """
        campos = self._parse_campos_extraer(db_rule)
        return RuleResponse(
            id=db_rule.id,
            cliente_id=db_rule.cliente_id,
            nombre=db_rule.nombre,
            tipo_documento=db_rule.tipo_documento,
            campos_extraer=[CampoExtraerSchema(**c) for c in campos],
            patron_carpeta=db_rule.patron_carpeta,
            modo_entrada=db_rule.modo_entrada,
            umbral_ocr=db_rule.umbral_ocr,
            version=db_rule.version,
            activa=db_rule.activa,
            created_by=db_rule.created_by,
            created_at=db_rule.created_at,
            updated_at=db_rule.updated_at,
        )

    def list_rules(self, client_id: int) -> list[RuleResponse]:
        """
        Lista todas las reglas activas de un cliente.

        CA-01: Retorna lista vacía si no hay reglas configuradas.
        CA-02: Retorna lista ordenada por fecha de creación descendente.

        Args:
            client_id: ID del cliente.

        Returns:
            Lista de RuleResponse (puede ser vacía).
        """
        logger.info("Listando reglas para cliente_id=%d", client_id)
        db_rules = self.repository.get_by_client(client_id)
        return [self._to_response(r) for r in db_rules]

    def get_rule(self, rule_id: int) -> RuleResponse:
        """
        Obtiene el detalle completo de una regla.

        CA-03: Retorna la regla con campos_extraer parseado como JSON.

        Args:
            rule_id: ID de la regla.

        Returns:
            RuleResponse con el detalle completo.

        Raises:
            RuleNotFoundException: Si la regla no existe o no está activa.
        """
        logger.info("Obteniendo detalle de regla id=%d", rule_id)
        db_rule = self.repository.get_by_id(rule_id)
        if db_rule is None:
            raise RuleNotFoundException(rule_id)
        return self._to_response(db_rule)

    def create_rule(self, data: RuleCreate) -> RuleResponse:
        """
        Crea una nueva regla de trabajo.

        CA-04: Genera ID automáticamente. No modifica reglas existentes.
        CA-05: Los campos obligatorios ya están validados por Pydantic.
        CA-06: Valida nombres duplicados en campos_extraer.

        Flujo:
            1. Ejecutar validaciones de dominio (modo_entrada, duplicados).
            2. Verificar unicidad de nombre por cliente.
            3. Persistir en BD.

        Args:
            data: Schema RuleCreate con los datos de la nueva regla.

        Returns:
            RuleResponse de la regla recién creada.

        Raises:
            InvalidModoEntradaException: Si modo_entrada no es válido.
            DuplicateFieldNameException: Si hay campos con nombre duplicado.
            RuleNameAlreadyExistsException: Si ya existe una regla con ese nombre.
        """
        logger.info(
            "Creando regla '%s' para cliente_id=%d",
            data.nombre,
            data.cliente_id,
        )

        # 1. Validaciones de dominio
        campos_dicts = [c.model_dump() for c in data.campos_extraer]
        validate_rule_data(campos_dicts, data.modo_entrada)

        # 2. Verificar unicidad de nombre por cliente
        if self.repository.exists_by_name_and_client(
            data.nombre, data.cliente_id
        ):
            raise RuleNameAlreadyExistsException(data.nombre, data.cliente_id)

        # 3. Persistir
        rule_data = {
            "cliente_id": data.cliente_id,
            "nombre": data.nombre.strip(),
            "tipo_documento": data.tipo_documento.strip(),
            "campos_extraer": campos_dicts,
            "patron_carpeta": data.patron_carpeta.strip(),
            "modo_entrada": data.modo_entrada.strip(),
        }
        db_rule = self.repository.create(rule_data)
        return self._to_response(db_rule)

    def update_rule(self, rule_id: int, data: RuleUpdate) -> RuleResponse:
        """
        Actualiza una regla de trabajo existente.

        CA-05: Los campos obligatorios ya están validados por Pydantic.
        CA-06: Valida nombres duplicados en campos_extraer.
        Version se incrementa automáticamente en el repositorio.

        Flujo:
            1. Verificar que la regla existe.
            2. Ejecutar validaciones de dominio.
            3. Verificar unicidad de nombre (excluyendo la regla actual).
            4. Actualizar en BD.

        Args:
            rule_id: ID de la regla a actualizar.
            data: Schema RuleUpdate con los nuevos datos.

        Returns:
            RuleResponse de la regla actualizada.

        Raises:
            RuleNotFoundException: Si la regla no existe.
            InvalidModoEntradaException: Si modo_entrada no es válido.
            DuplicateFieldNameException: Si hay campos con nombre duplicado.
            RuleNameAlreadyExistsException: Si el nuevo nombre ya está en uso.
        """
        logger.info("Actualizando regla id=%d", rule_id)

        # 1. Verificar existencia
        db_rule = self.repository.get_by_id(rule_id)
        if db_rule is None:
            raise RuleNotFoundException(rule_id)

        # 2. Validaciones de dominio
        campos_dicts = [c.model_dump() for c in data.campos_extraer]
        validate_rule_data(campos_dicts, data.modo_entrada)

        # 3. Verificar unicidad de nombre (excluyendo la regla actual)
        if self.repository.exists_by_name_and_client(
            data.nombre, db_rule.cliente_id, exclude_id=rule_id
        ):
            raise RuleNameAlreadyExistsException(data.nombre, db_rule.cliente_id)

        # 4. Actualizar
        update_data = {
            "nombre": data.nombre.strip(),
            "tipo_documento": data.tipo_documento.strip(),
            "campos_extraer": campos_dicts,
            "patron_carpeta": data.patron_carpeta.strip(),
            "modo_entrada": data.modo_entrada.strip(),
        }
        updated_rule = self.repository.update(rule_id, update_data)
        return self._to_response(updated_rule)
