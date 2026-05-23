from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.clasificacion import ClasificacionPayload, ClasificacionResponse
from app.tasks.clasificacion_tasks import clasificar_documento_task

router = APIRouter(prefix="/clasificacion", tags=["clasificacion"])

@router.post("/async", response_model=ClasificacionResponse)
def trigger_clasificacion_async(payload: ClasificacionPayload, db: Session = Depends(get_db)):
    """
    Inicia la tarea asíncrona de clasificación.
    HU-05 CA-01
    """
    task = clasificar_documento_task.delay(payload.model_dump())
    return ClasificacionResponse(
        success=True,
        mensaje=f"Tarea iniciada con ID: {task.id}"
    )

@router.post("/sync", response_model=ClasificacionResponse)
def trigger_clasificacion_sync(payload: ClasificacionPayload, db: Session = Depends(get_db)):
    """
    Ejecuta la clasificación de forma síncrona (útil para pruebas y debug).
    """
    from app.services.clasificacion_ia_service import ClasificacionIAService
    service = ClasificacionIAService(db)
    result = service.clasificar_documento(payload.model_dump())
    
    if result.get("success"):
        return ClasificacionResponse(
            success=True,
            mensaje="Clasificación exitosa",
            documento_clasificado_id=result.get("documento_clasificado_id"),
            ruta_destino=result.get("ruta")
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Error desconocido")
        )
