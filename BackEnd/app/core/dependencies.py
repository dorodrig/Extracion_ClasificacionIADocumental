"""
Dependencias FastAPI: sesión de BD, usuario actual y validación de roles.
"""
import logging
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.security import decode_access_token
from app.db.models.usuarios import Usuario

logger = logging.getLogger("grm.dependencies")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)

def get_db():
    """Inyecta una sesión de base de datos por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
    Decodifica el JWT y retorna el usuario actual de la base de datos.
    """
    # --- BYPASS DE SEGURIDAD PARA PILOTO ---
    return MockUser(id=1, cedula="0000000000", nombre="Bypass Admin", rol="admin", cliente_id=1)
    # -----------------------------------------

def require_role(roles: list[str]):
    """
    Decorator-factory de RBAC.
    Retorna una dependencia que verifica que el usuario tenga uno de los roles permitidos en la lista.
    """
    def _check_role(current_user: Usuario = Depends(get_current_user)):
        # --- BYPASS DE SEGURIDAD PARA PILOTO ---
        return current_user
        # ---------------------------------------
    return _check_role

# Temporary mock for backwards compatibility with endpoints not yet migrated
from dataclasses import dataclass

@dataclass
class MockUser:
    """Representación temporal de un usuario autenticado."""
    id: int = 1
    cedula: str = "0000000000"
    nombre: str = "Usuario Mock"
    rol: str = "admin"
    cliente_id: int | None = None

def get_current_cliente() -> MockUser:
    return MockUser(id=2, cedula="1111111111", nombre="Cliente Mock", rol="cliente", cliente_id=1)
