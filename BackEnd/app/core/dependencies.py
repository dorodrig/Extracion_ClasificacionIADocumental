"""
Dependencias FastAPI: sesión de BD, usuario actual y validación de roles.
"""
import logging
from typing import Annotated
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.db.database import SessionLocal

logger = logging.getLogger("grm.dependencies")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_db():
    """Inyecta una sesión de base de datos por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Mock temporal de autenticación — TODO(HU-08): Reemplazar por JWT real
# ---------------------------------------------------------------------------

@dataclass
class MockUser:
    """Representación temporal de un usuario autenticado."""
    id: int = 1
    cedula: str = "0000000000"
    nombre: str = "Usuario Mock"
    rol: str = "admin"
    cliente_id: int | None = None

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)] = None):
    """
    Decodifica el JWT y retorna el usuario actual.
    Implementación completa en HU-08 (Auth).
    Stub temporal para compilar la capa de dependencias.
    """
    from types import SimpleNamespace
    user = SimpleNamespace(id=1, rol="admin", cliente_id=1)
    return user

def require_role(roles: list[str]):
    """
    Decorator-factory de RBAC.
    Retorna una dependencia que verifica que el usuario tenga uno de los roles dados.
    """
    def _check_role(current_user=Depends(get_current_user)):
        if current_user.rol not in roles:
            logger.warning(
                "Acceso denegado — usuario rol=%s no está en roles permitidos=%s",
                current_user.rol,
                roles,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción.",
            )
        return current_user
    return _check_role

def get_current_cliente() -> MockUser:
    """
    Mock de dependencia para obtener el cliente actual (HU-07 / HU-08).
    """
    return MockUser(id=2, cedula="1111111111", nombre="Cliente Mock", rol="cliente", cliente_id=1)
