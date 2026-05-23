"""
app/api/v1/endpoints/batches.py
Endpoint REST para la gestión de lotes de procesamiento documental.

HU-02 — CA-01 a CA-04: Ingesta Dual de Documentos (Escáner / Carpeta Local)
Gobernanza §3.1, §3.2, §3.3, §3.4
"""
import logging
from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.schemas.batches import BatchCreate, BatchResponse
from app.schemas.common import APIResponse
from app.services.batch_service import BatchService
from app.db.repositories.batch_repository import BatchRepository
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
        repo = BatchRepository(db)
        service = BatchService(repo)
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

from app.schemas.batches import BatchPrepareRequest, BatchStatusResponse
from app.services.ingestion_service import IngestionService
from app.services.storage.local_storage import LocalStorageAdapter
from app.services.storage.pdf_splitter import PyPDFSplitterAdapter

@router.post(
    "/{batch_id}/prepare",
    response_model=APIResponse[BatchStatusResponse],
    status_code=status.HTTP_200_OK,
    summary="Preparar lote para ingesta",
)
async def prepare_batch(
    batch_id: str,
    request: BatchPrepareRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "operario"])),
) -> JSONResponse:
    from app.services.pipeline_orchestrator_service import PipelineOrchestratorService
    
    repo = BatchRepository(db)
    storage = LocalStorageAdapter()
    pdf_splitter = PyPDFSplitterAdapter()
    service = IngestionService(repo, storage, pdf_splitter)
    
    try:
        response_data = service.prepare_batch(batch_id, request)
        
        # Encolar la orquestación del flujo OCR + IA en segundo plano
        orchestrator = PipelineOrchestratorService(db)
        # Recuperar la regla de trabajo del lote
        batch = repo.get_by_batch_id(batch_id)
        if batch and batch.regla_id:
            background_tasks.add_task(
                orchestrator.process_batch_pipeline,
                batch_id=batch_id,
                regla_id=batch.regla_id
            )
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=APIResponse(
                success=True,
                data=response_data.model_dump(mode="json"),
                message="Preparación completada. Flujo OCR e IA iniciado en segundo plano."
            ).model_dump()
        )
    except Exception as exc:
        logger.error("Error al preparar lote: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=APIResponse(
                success=False,
                error=str(exc),
                message="Error en preparación"
            ).model_dump()
        )

@router.get(
    "/{batch_id}/status",
    response_model=APIResponse[BatchStatusResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar estado del lote",
)
async def get_batch_status(
    batch_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin", "operario"])),
) -> JSONResponse:
    repo = BatchRepository(db)
    storage = LocalStorageAdapter()
    pdf_splitter = PyPDFSplitterAdapter()
    service = IngestionService(repo, storage, pdf_splitter)
    
    try:
        response_data = service.get_batch_status(batch_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=APIResponse(
                success=True,
                data=response_data.model_dump(mode="json"),
                message="Estado obtenido"
            ).model_dump()
        )
    except Exception as exc:
        logger.error("Error al obtener estado: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=APIResponse(
                success=False,
                error=str(exc),
                message="Error al consultar estado"
            ).model_dump()
        )
