"""
app/api/v1/endpoints/batches.py
Endpoint REST para la gestión de lotes de procesamiento documental.

HU-02 — CA-01 a CA-04: Ingesta Dual de Documentos (Escáner / Carpeta Local)
Gobernanza §3.1, §3.2, §3.3, §3.4
"""
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.schemas.batches import BatchCreate, BatchResponse
from app.schemas.common import APIResponse
from app.services.batch_service import BatchService
from app.core.exceptions import BatchCreationException

logger = logging.getLogger("grm.batches")

router = APIRouter()


@router.post(
    "",
    response_model=APIResponse[BatchResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo lote de procesamiento",
    description=(
        "Crea un nuevo lote de procesamiento documental con UUID único. "
        "Soporta modo de ingesta 'scanner' o 'carpeta'. "
        "HU-02 CA-03/CA-04."
    ),
    tags=["batches"],
)
async def create_batch(
    batch_in: BatchCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "operario"])),
) -> JSONResponse:
    """
    POST /api/v1/batches

    Crea un lote de procesamiento con un UUID (batch_id) único.
    Estado inicial: 'preparando'.
    La ruta temporal se almacena en BD; la carpeta física se crea en CA-07.

    Roles autorizados: admin, operario.
    """
    logger.info(
        "Creando lote — modo=%s, regla_id=%d, cliente_id=%d, operario_id=%d",
        batch_in.modo_ingesta,
        batch_in.regla_id,
        batch_in.cliente_id,
        current_user.id,
    )

    try:
        service = BatchService(db)
        batch_response = service.create_batch(batch_in, operario_id=current_user.id)
        logger.info("Lote creado exitosamente — batch_id=%s", batch_response.batch_id)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=APIResponse(
                success=True,
                data=batch_response.model_dump(mode="json"),
                message="Lote de procesamiento creado exitosamente.",
            ).model_dump(),
        )
    except BatchCreationException as exc:
        logger.error("Error al crear lote: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIResponse(
                success=False,
                error=str(exc),
                message="No se pudo crear el lote de procesamiento.",
            ).model_dump(),
        )
