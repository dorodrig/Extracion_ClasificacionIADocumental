from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ClasificacionPayload(BaseModel):
    documento_id: int
    cliente_id: int
    batch_id: str
    regla_id: int
    datos_extraidos: Dict[str, Any]
    texto_ocr: Optional[str] = None
    archivo_origen: str

class ClasificacionResponse(BaseModel):
    success: bool
    mensaje: str
    documento_clasificado_id: Optional[int] = None
    ruta_destino: Optional[str] = None

class ReprocesarPayload(BaseModel):
    documento_id: int
    instruccion_correctiva: str
