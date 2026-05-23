"""
Endpoints REST del Agente de Contexto IA (HU-04).

Gobernanza §3.2 — Prefijo /api/v1/, sustantivos plurales, kebab-case.
Gobernanza §3.2 — Respuestas envueltas en APIResponse.

Endpoints:
    POST /api/v1/contexto-ia/procesar — Procesa un documento con IA
    GET  /api/v1/contexto-ia/resultado/{documento_id} — Obtiene resultado
"""
import json
import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import MockUser, get_db, require_role
from app.db.repositories.contexto_resultado_repository import ContextoResultadoRepository
from app.domain.exceptions import GRMException
from app.schemas.contexto_schema import (
    CampoExtraidoSchema,
    ContextoProcessRequest,
    ContextoResultadoResponse,
)
from app.schemas.rule_schema import APIResponse
from app.services.contexto_ia_service import ContextoIAService

logger = logging.getLogger("grm.api.contexto")

router = APIRouter(
    prefix="/contexto-ia",
    tags=["HU-04 — Agente Contexto IA"],
)


def _build_response(resultado) -> ContextoResultadoResponse:
    """Convierte un AgenteContextoResultados a ContextoResultadoResponse."""
    # Parsear campos_extraidos_json a lista de CampoExtraidoSchema
    campos_extraidos = []
    if resultado.campos_extraidos_json:
        try:
            paquete = json.loads(resultado.campos_extraidos_json)
            for campo in paquete.get("campos_extraidos", []):
                campos_extraidos.append(
                    CampoExtraidoSchema(
                        nombre=campo.get("nombre", ""),
                        valor=campo.get("valor"),
                        valor_original=campo.get("valor_original"),
                        confianza_ocr=campo.get("confianza_ocr", 0.0),
                        validado_ia=campo.get("validado_ia", False),
                    )
                )
        except (json.JSONDecodeError, TypeError):
            logger.warning(
                "Error parseando campos_extraidos_json para resultado id=%d",
                resultado.id,
            )

    return ContextoResultadoResponse(
        id=resultado.id,
        documento_id=resultado.documento_id,
        regla_id=resultado.regla_id,
        tipo_doc_detectado=resultado.tipo_doc_detectado,
        campos_extraidos=campos_extraidos,
        datos_completos=resultado.datos_completos,
        motivo_rechazo=resultado.motivo_rechazo,
        modelo_ia=resultado.modelo_ia,
        tokens_entrada=resultado.tokens_entrada,
        tokens_salida=resultado.tokens_salida,
        duracion_ms=resultado.duracion_ms,
        estado=resultado.estado,
        processed_at=resultado.processed_at,
    )


@router.post(
    "/procesar",
    response_model=APIResponse[ContextoResultadoResponse],
    status_code=status.HTTP_200_OK,
    summary="Procesar documento con Agente de Contexto IA",
    description=(
        "CA-01 a CA-12: Invoca el Agente de Contexto IA para procesar un documento. "
        "Construye el prompt con las reglas del cliente y datos OCR, invoca Gemini, "
        "valida campos, normaliza valores y persiste el resultado."
    ),
)
async def procesar_documento(
    request: ContextoProcessRequest,
    db: Session = Depends(get_db),
    user: MockUser = Depends(require_role(["admin", "operario"])),
) -> dict:
    """
    Procesa un documento con el Agente de Contexto IA (HU-04).

    Flujo completo:
        1. Construye prompt dinámico (CA-01)
        2. Invoca Google Gemini (CA-02)
        3. Parsea y valida respuesta (CA-03, CA-04)
        4. Normaliza valores (CA-11)
        5. Determina estado (CA-05/CA-06)
        6. Registra invocación (CA-09)
        7. Persiste resultado (CA-12)
    """
    logger.info(
        "POST /contexto-ia/procesar — documento_id=%d, regla_id=%d, user=%s",
        request.documento_id,
        request.regla_id,
        user.nombre,
    )

    service = ContextoIAService(db)
    resultado = await service.procesar_documento(
        documento_id=request.documento_id,
        regla_id=request.regla_id,
    )

    response_data = _build_response(resultado)

    return APIResponse(
        success=True,
        data=response_data,
        message=(
            f"Documento procesado exitosamente. Estado: {resultado.estado}"
        ),
    ).model_dump()


@router.get(
    "/resultado/{documento_id}",
    response_model=APIResponse[ContextoResultadoResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener resultado del Agente de Contexto IA",
    description="Obtiene el paquete de datos limpios generado por el agente para un documento.",
)
async def obtener_resultado(
    documento_id: int,
    db: Session = Depends(get_db),
    user: MockUser = Depends(require_role(["admin", "operario"])),
) -> dict:
    """Obtiene el resultado del agente de contexto para un documento."""
    logger.info(
        "GET /contexto-ia/resultado/%d — user=%s",
        documento_id,
        user.nombre,
    )

    repo = ContextoResultadoRepository(db)
    resultado = repo.obtener_por_documento(documento_id)

    if not resultado:
        raise GRMException(
            f"No se encontró resultado del agente de contexto "
            f"para el documento id={documento_id}."
        )

    response_data = _build_response(resultado)

    return APIResponse(
        success=True,
        data=response_data,
        message="Resultado obtenido exitosamente",
    ).model_dump()
