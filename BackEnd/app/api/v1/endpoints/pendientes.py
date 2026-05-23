from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.core.dependencies import require_role
from app.schemas.common import APIResponse
from app.schemas.pendientes import (
    ListaPendientesResponse,
    DocumentoPendienteVisorResponse,
    CorreccionDirectaRequest,
    InstruccionClasificacionRequest,
    DescarteRequest
)
from app.services.pendientes_service import PendientesService
from app.core.websockets import manager

router = APIRouter()

@router.get("/", response_model=APIResponse[ListaPendientesResponse])
def listar_pendientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    q: Optional[str] = Query(None, description="Término de búsqueda"),
    cliente_id: Optional[int] = Query(None, description="Filtro por cliente"),
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["operario", "admin"]))
):
    """
    Lista los documentos pendientes con soporte para paginación y filtros.
    """
    service = PendientesService(db)
    result = service.list_pendientes(skip=skip, limit=limit, query=q, cliente_id=cliente_id)
    return APIResponse(success=True, data=result, message="Documentos pendientes obtenidos correctamente.")


@router.get("/{pendiente_id}/visor", response_model=APIResponse[DocumentoPendienteVisorResponse])
def obtener_detalle_visor(
    pendiente_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["operario", "admin"]))
):
    """
    Obtiene los detalles completos de un documento pendiente para el visor.
    """
    service = PendientesService(db)
    result = service.get_visor_data(pendiente_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento pendiente no encontrado.")
    return APIResponse(success=True, data=result)


@router.put("/{pendiente_id}/correccion", response_model=APIResponse[bool])
async def correccion_directa(
    pendiente_id: int,
    request: CorreccionDirectaRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["operario", "admin"]))
):
    """
    Guarda una corrección directa de campos realizada por el operario.
    """
    service = PendientesService(db)
    success = await service.corregir_documento(pendiente_id, current_user.id, request)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento pendiente no encontrado.")
    return APIResponse(success=True, data=True, message="Corrección guardada exitosamente.")


@router.post("/{pendiente_id}/instruccion", response_model=APIResponse[bool])
async def enviar_instruccion(
    pendiente_id: int,
    request: InstruccionClasificacionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["operario", "admin"]))
):
    """
    Envía una instrucción al Agente de Clasificación para reprocesar el documento.
    """
    service = PendientesService(db)
    success = await service.enviar_instruccion(pendiente_id, current_user.id, request)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento pendiente no encontrado.")
    return APIResponse(success=True, data=True, message="Instrucción enviada exitosamente.")


@router.put("/{pendiente_id}/descarte", response_model=APIResponse[bool])
async def descartar_documento(
    pendiente_id: int,
    request: DescarteRequest,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["operario", "admin"]))
):
    """
    Descarta un documento pendiente con un motivo especificado.
    """
    service = PendientesService(db)
    success = await service.descartar_documento(pendiente_id, current_user.id, request)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento pendiente no encontrado.")
    return APIResponse(success=True, data=True, message="Documento descartado exitosamente.")


@router.websocket("/ws")
async def websocket_pendientes(websocket: WebSocket):
    """
    WebSocket para actualizaciones en tiempo real sobre el estado de los pendientes.
    """
    await manager.connect(websocket)
    try:
        while True:
            # We keep the connection open, waiting for client messages if any, 
            # though usually it's one-way server-to-client notifications.
            data = await websocket.receive_text()
            # Handle possible heartbeat or ping from client if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)
