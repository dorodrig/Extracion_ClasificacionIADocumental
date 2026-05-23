"""
Motor de base de datos y fábrica de sesiones SQLAlchemy.

Gobernanza §2.2 — app/db/database.py
Conexión a SQL Server 2019+ vía pyodbc.
"""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("grm.database")

Base = declarative_base()

def _get_database_url() -> str:
    try:
        from app.core.config import settings
        return settings.database_url
    except Exception:
        logger.warning("No se pudo cargar settings.database_url — usando SQLite en memoria para tests.")
        return "sqlite://"

engine = create_engine(
    _get_database_url(),
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
