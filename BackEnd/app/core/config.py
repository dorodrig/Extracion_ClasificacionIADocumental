"""
Configuración centralizada del proyecto GRM.

Carga todas las variables de entorno desde .env usando pydantic-settings.
Gobernanza §3.4 / §6.1 — CERO credenciales hardcodeadas.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings del backend GRM.

    Todas las variables se cargan desde el archivo .env ubicado en la raíz
    del directorio BackEnd. Ningún valor sensible debe existir en código fuente.
    """

    # Base de Datos
    database_url: str = "mssql+pyodbc://sa:password@localhost\\SQLEXPRESS:1433/GRM_DB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

    # Seguridad JWT
    secret_key: str = "change-me-to-a-random-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    # Futuro: Google Gemini (HU-04, HU-05)
    # gemini_api_key: str = ""
    # gemini_model: str = "gemini-1.5-pro"
    # gemini_timeout_seconds: int = 30

    # Futuro: AWS Textract (HU-03)
    # aws_access_key_id: str = ""
    # aws_secret_access_key: str = ""
    # aws_default_region: str = "us-east-1"

    # Futuro: Celery
    # celery_broker_url: str = "redis://localhost:6379/0"

    # Futuro: Storage
    # storage_base_path: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


settings = Settings()
