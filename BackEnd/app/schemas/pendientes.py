from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from datetime import datetime

class DocumentoPendienteBase(BaseModel):
    cliente_id: int
    batch_id: str
    documento_id: int
    motivo_rechazo: Optional[str] = None
    estado: str

class DocumentoPendienteResponse(DocumentoPendienteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DocumentoPendienteVisorResponse(DocumentoPendienteResponse):
    campos_extraidos_json: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class CorreccionDirectaRequest(BaseModel):
    campos_corregidos: Dict[str, Any]

class InstruccionClasificacionRequest(BaseModel):
    instruccion: str

class DescarteRequest(BaseModel):
    motivo_descarte: str

class ListaPendientesResponse(BaseModel):
    items: List[DocumentoPendienteResponse]
    total: int
