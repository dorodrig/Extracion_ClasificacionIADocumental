"""
Motor de base de datos y fábrica de sesiones SQLAlchemy.

Gobernanza §2.2 — app/db/database.py
Conexión a SQL Server 2019+ vía pyodbc.

La creación del engine se realiza de forma lazy para permitir que los tests
inyecten una BD SQLite en memoria sin necesidad de pyodbc instalado.
"""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

logger = logging.getLogger("grm.database")


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos SQLAlchemy del proyecto GRM."""
    pass


def get_engine(database_url: str | None = None):
    """
    Crea el engine SQLAlchemy para la BD configurada.

    Args:
        database_url: URL de conexión. Si no se proporciona, usa settings.

    Returns:
        Engine de SQLAlchemy configurado.
    """
    if database_url is None:
        from app.core.config import settings
        database_url = settings.database_url

    return create_engine(
        database_url,
        pool_pre_ping=True,
        echo=False,
    )


def get_session_local(engine=None):
    """
    Crea la fábrica de sesiones para el engine dado.

    Args:
        engine: Engine de SQLAlchemy. Si no se proporciona, crea uno por defecto.

    Returns:
        sessionmaker configurado.
    """
    if engine is None:
        engine = get_engine()
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


# Lazy initialization — solo se crean al importar por primera vez desde código real
# Los tests override con su propia BD (SQLite en memoria).
_engine = None
_SessionLocal = None


def _init_default():
    """Inicializa engine y SessionLocal con la configuración por defecto."""
    global _engine, _SessionLocal
    if _engine is None:
        _engine = get_engine()
        _SessionLocal = get_session_local(_engine)


@property
def engine():
    _init_default()
    return _engine


def SessionLocal():
    """Retorna una nueva sesión de BD usando el engine por defecto."""
    _init_default()
    return _SessionLocal()
