from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class LogProcesoCreate(BaseModel):
    documento_id: int
    estado_anterior: Optional[str] = None
    estado_nuevo: str
    mensaje: Optional[str] = None

class LogAuditoriaUsuarioCreate(BaseModel):
    documento_id: int
    usuario_id: int
    accion: str
    detalles: Optional[Dict[str, Any]] = None

class LogIAInvocacionesCreate(BaseModel):
    documento_id: int
    proveedor: str
    endpoint_invocado: Optional[str] = None
    payload_enviado: Optional[Dict[str, Any]] = None
    respuesta_recibida: Optional[Dict[str, Any]] = None
    tiempo_respuesta_ms: Optional[int] = None
    exitoso: bool = True

class DocumentoHistorialItem(BaseModel):
    id: int
    tipo_log: str # "proceso", "auditoria_usuario", "ia_invocacion"
    documento_id: int
    created_at: datetime
    
    # Specific fields based on type
    estado_anterior: Optional[str] = None
    estado_nuevo: Optional[str] = None
    mensaje: Optional[str] = None
    
    usuario_id: Optional[int] = None
    accion: Optional[str] = None
    detalles: Optional[Dict[str, Any]] = None
    
    proveedor: Optional[str] = None
    endpoint_invocado: Optional[str] = None
    tiempo_respuesta_ms: Optional[int] = None
    exitoso: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class DocumentoHistorialResponse(BaseModel):
    documento_id: int
    historial: List[DocumentoHistorialItem]
