"""
app/db/database.py
Engine SQLAlchemy, SessionLocal y Base declarativa.
Configuración externalizada via pydantic-settings (.env).
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("grm.database")

# Importación diferida de settings para evitar arrancar pydantic-settings
# antes de que .env esté presente en todos los entornos.
def _get_database_url() -> str:
    try:
        from app.core.config import settings
        return settings.database_url
    except Exception:
        # Fallback para entornos de test sin .env configurado
        logger.warning("No se pudo cargar settings.database_url — usando SQLite en memoria para tests.")
        return "sqlite://"


engine = create_engine(
    _get_database_url(),
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
