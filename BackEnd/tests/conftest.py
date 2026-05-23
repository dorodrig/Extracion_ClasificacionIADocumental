import pytest
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.core.dependencies import get_db
from app.db.database import Base

# Setup the in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _patch_mssql_types_for_sqlite():
    """
    Reemplaza tipos MSSQL (UNIQUEIDENTIFIER) por tipos compatibles
    con SQLite en todas las tablas registradas en Base.metadata.
    """
    from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
    for table in Base.metadata.tables.values():
        for col in table.columns:
            if isinstance(col.type, UNIQUEIDENTIFIER):
                col.type = String(36)


@pytest.fixture(scope="session")
def setup_db():
    # Importar todos los modelos para que Base.metadata los conozca
    import app.db.models  # noqa: F401
    import app.db.models.documentos_clasificados  # noqa: F401
    import app.db.models.documentos_pendientes  # noqa: F401
    import app.db.models.auth_stubs  # noqa: F401

    _patch_mssql_types_for_sqlite()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(setup_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
