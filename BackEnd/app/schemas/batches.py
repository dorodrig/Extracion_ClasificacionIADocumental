from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class ModoIngesta(str, Enum):
    scanner = "scanner"
    carpeta = "carpeta"

class BatchCreate(BaseModel):
    regla_id: int
    cliente_id: int
    modo_ingesta: str

    @field_validator('modo_ingesta')
    @classmethod
    def check_modo_ingesta(cls, v: str) -> str:
        if v not in [ModoIngesta.scanner, ModoIngesta.carpeta]:
            raise ValueError('modo_ingesta must be scanner or carpeta')
        return v

class BatchResponse(BaseModel):
    id: int
    batch_id: UUID
    estado: str
    created_at: datetime
    
    class Config:
        from_attributes = True
