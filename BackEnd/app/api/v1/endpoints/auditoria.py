from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.dependencies import require_role
from app.schemas.common import APIResponse
from app.schemas.auditoria import DocumentoHistorialResponse
from app.services.auditoria_service import AuditoriaService

router = APIRouter()

@router.get("/documentos/{documento_id}/historial", response_model=APIResponse[DocumentoHistorialResponse])
def obtener_historial_documento(
    documento_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["operario", "admin"]))
):
    """
    Obtiene el historial completo de eventos (procesos, auditoría, IA) de un documento,
    ordenado cronológicamente.
    """
    service = AuditoriaService(db)
    result = service.obtener_historial_documento(documento_id)
    
    if not result or not result.historial:
        # We can either return empty or 404. Let's return empty array if no history
        pass
        
    return APIResponse(success=True, data=result, message="Historial obtenido correctamente.")
