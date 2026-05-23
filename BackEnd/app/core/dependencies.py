"""
Dependencias de inyección para FastAPI.

Gobernanza §2.2 — app/core/dependencies.py
Provee get_db() para sesiones de BD y mock temporal de autenticación.
"""
import logging
from collections.abc import Generator
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.db.database import SessionLocal as _get_session

logger = logging.getLogger("grm.dependencies")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency de FastAPI que provee una sesión de base de datos.

    Abre una sesión al inicio de cada request y la cierra al finalizar,
    garantizando que los recursos de conexión se liberan correctamente.

    Yields:
        Session: Sesión activa de SQLAlchemy.
    """
    db = _get_session()
app/core/dependencies.py
Dependencias FastAPI: sesión de BD, usuario actual y validación de roles.
"""
import logging
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
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
    """
    Representación temporal de un usuario autenticado.

    TODO(HU-08): Reemplazar por el modelo User real cuando HU-08 esté
    integrada. Esta clase existe solo para mantener la interfaz de
    Depends() lista para inyección de auth real.
    """
    id: int = 1
    cedula: str = "0000000000"
    nombre: str = "Usuario Mock"
    rol: str = "admin"
    cliente_id: int | None = None


def require_role(allowed_roles: list[str]):
    """
    Mock de verificación de roles.

    TODO(HU-08): Make created_by mandatory once Auth is integrated.
    Reemplazar esta función por la implementación real que:
    1. Extraiga y valide el JWT del header Authorization.
    2. Verifique que el rol del usuario está en allowed_roles.
    3. Retorne el usuario autenticado.

    Args:
        allowed_roles: Lista de roles permitidos para el endpoint.

    Returns:
        Función dependency que retorna un MockUser.
    """
    def _mock_dependency() -> MockUser:
        logger.debug(
            "Mock auth: permitiendo acceso. Roles permitidos: %s",
            allowed_roles,
        )
        return MockUser()

    return _mock_dependency

def get_current_cliente() -> MockUser:
    """
    Mock de dependencia para obtener el cliente actual (HU-07 / HU-08).
    Simula que un cliente_id viene en el token JWT.
    """
    logger.debug("Mock auth: simulando cliente autenticado (cliente_id=1).")
    return MockUser(id=2, cedula="1111111111", nombre="Cliente Mock", rol="cliente", cliente_id=1)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Decodifica el JWT y retorna el usuario actual.
    Implementación completa en HU-08 (Auth).
    Stub temporal para compilar la capa de dependencias.
    """
    # TODO: Implementar decodificación JWT completa en HU-08
    # Por ahora retornamos un stub que permite operar en desarrollo
    from types import SimpleNamespace
    user = SimpleNamespace(id=1, rol="operario", cliente_id=1)
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
