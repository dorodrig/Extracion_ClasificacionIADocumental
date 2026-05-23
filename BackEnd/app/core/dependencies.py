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
"""
app/core/dependencies.py
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


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
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    usuario_id: str = payload.get("usuario_id")
    if usuario_id is None:
        raise credentials_exception
        
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None or not usuario.activo:
        raise credentials_exception
        
    # Añadimos claims adicionales útiles en la solicitud, sin guardarlos en DB si no es necesario
    # Por ejemplo, si el token tiene un cliente_id temporal de sesión
    usuario.current_cliente_id = payload.get("cliente_id")
    
    return usuario


def require_role(roles: list[str]):
    """
    Decorator-factory de RBAC.
    Retorna una dependencia que verifica que el usuario tenga uno de los roles permitidos en la lista.
    """
    def _check_role(current_user: Usuario = Depends(get_current_user)):
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
