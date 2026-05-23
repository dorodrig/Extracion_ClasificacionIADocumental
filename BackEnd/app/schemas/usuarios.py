from pydantic import BaseModel, Field
from typing import List, Optional

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    identificacion: Optional[str] = None

    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    cedula: str
    nombre: str
    rol: str

class UsuarioCreate(UsuarioBase):
    password: str
    cliente_ids: Optional[List[int]] = []

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    clientes: List[ClienteResponse] = []

    class Config:
        from_attributes = True
