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

