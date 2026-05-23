"""
Endpoints REST para Reglas de Trabajo — HU-01 (CA-01 a CA-06).

Gobernanza §2.2 — app/api/v1/endpoints/rules.py
Gobernanza §3.2 — Endpoints REST plurales, versión v1, APIResponse.
Gobernanza §3.4 — Validación de autorización en cada endpoint (mock temporal).

Endpoints:
    GET  /api/v1/rules           — Listar reglas por cliente (CA-01, CA-02)
    GET  /api/v1/rules/{id}      — Detalle de una regla (CA-03)
    POST /api/v1/rules           — Crear nueva regla (CA-04, CA-05, CA-06)
    PUT  /api/v1/rules/{id}      — Actualizar regla (CA-05, CA-06)
"""
import logging

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import MockUser, get_db, require_role
from app.schemas.rule_schema import (
    APIResponse,
    RuleCreate,
    RuleResponse,
    RuleUpdate,
)
from app.services.rule_service import RuleService

logger = logging.getLogger("grm.endpoints.rules")

router = APIRouter(
    prefix="/rules",
    tags=["Reglas de Trabajo"],
)


@router.get(
    "",
    response_model=APIResponse[list[RuleResponse]],
    summary="Listar reglas de trabajo por cliente",
    description=(
        "CA-01: Retorna lista vacía si el cliente no tiene reglas. "
        "CA-02: Retorna lista con campos base ordenados por fecha descendente."
    ),
)
def list_rules(
    cliente_id: int = Query(
        ...,
        gt=0,
        description="ID del cliente para filtrar reglas",
    ),
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(require_role(["admin", "operario"])),
) -> APIResponse[list[RuleResponse]]:
    """
    Lista todas las reglas de trabajo activas de un cliente.

    - **CA-01**: Si el cliente no tiene reglas, retorna data=[] con success=True.
    - **CA-02**: Retorna la lista completa con nombre, tipo_documento,
      created_at, updated_at y version por cada regla.
    """
    logger.info(
        "GET /rules — cliente_id=%d, usuario=%s",
        cliente_id,
        current_user.nombre,
    )
    service = RuleService(db)
    rules = service.list_rules(cliente_id)
    message = (
        "Este cliente no tiene reglas configuradas. Crea la primera regla."
        if len(rules) == 0
        else f"Se encontraron {len(rules)} regla(s) para el cliente."
    )
    return APIResponse(
        success=True,
        data=rules,
        message=message,
    )


@router.get(
    "/{rule_id}",
    response_model=APIResponse[RuleResponse],
    summary="Obtener detalle de una regla",
    description="CA-03: Retorna el detalle completo incluyendo campos_extraer parseado.",
)
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(require_role(["admin", "operario"])),
) -> APIResponse[RuleResponse]:
    """
    Obtiene el detalle completo de una regla de trabajo por su ID.

    - **CA-03**: Retorna todos los campos incluyendo campos_extraer
      como un array de objetos JSON parseados.
    """
    logger.info(
        "GET /rules/%d — usuario=%s",
        rule_id,
        current_user.nombre,
    )
    service = RuleService(db)
    rule = service.get_rule(rule_id)
    return APIResponse(
        success=True,
        data=rule,
        message="Detalle de la regla obtenido exitosamente.",
    )


@router.post(
    "",
    response_model=APIResponse[RuleResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva regla de trabajo",
    description=(
        "CA-04: Genera ID automáticamente. "
        "CA-05: Valida campos obligatorios. "
        "CA-06: Valida campos dinámicos a extraer."
    ),
)
def create_rule(
    rule_data: RuleCreate,
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(require_role(["admin", "operario"])),
) -> APIResponse[RuleResponse]:
    """
    Crea una nueva regla de trabajo para un cliente.

    - **CA-04**: El ID se genera automáticamente. Las reglas existentes
      del cliente no son modificadas.
    - **CA-05**: Valida que todos los campos obligatorios estén presentes
      (cliente_id, nombre, tipo_documento, campos_extraer, patron_carpeta,
      modo_entrada).
    - **CA-06**: Valida que no existan campos con nombre duplicado
      dentro de campos_extraer (case-insensitive).
    """
    logger.info(
        "POST /rules — nombre='%s', cliente_id=%d, usuario=%s",
        rule_data.nombre,
        rule_data.cliente_id,
        current_user.nombre,
    )
    service = RuleService(db)
    rule = service.create_rule(rule_data)
    return APIResponse(
        success=True,
        data=rule,
        message="Regla creada exitosamente.",
    )


@router.put(
    "/{rule_id}",
    response_model=APIResponse[RuleResponse],
    summary="Actualizar regla de trabajo",
    description=(
        "CA-05: Valida campos obligatorios. "
        "CA-06: Valida campos dinámicos. "
        "Incrementa version automáticamente."
    ),
)
def update_rule(
    rule_id: int,
    rule_data: RuleUpdate,
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(require_role(["admin", "operario"])),
) -> APIResponse[RuleResponse]:
    """
    Actualiza una regla de trabajo existente.

    - **CA-05**: Valida que todos los campos obligatorios estén presentes.
    - **CA-06**: Valida que no existan campos con nombre duplicado
      dentro de campos_extraer (case-insensitive).
    - La versión se incrementa automáticamente en cada actualización.
    """
    logger.info(
        "PUT /rules/%d — usuario=%s",
        rule_id,
        current_user.nombre,
    )
    service = RuleService(db)
    rule = service.update_rule(rule_id, rule_data)
    return APIResponse(
        success=True,
        data=rule,
        message="Regla actualizada exitosamente.",
    )
