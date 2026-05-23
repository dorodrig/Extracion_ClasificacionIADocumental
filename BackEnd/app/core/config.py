"""
app/core/config.py
Configuración centralizada usando pydantic-settings.
Todas las credenciales se leen desde variables de entorno o archivo .env.
CERO credenciales hardcodeadas (Gobernanza §3.4).
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base de datos
    database_url: str

    # Seguridad JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Servicios externos
    gemini_api_key: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_default_region: str = "us-east-1"

    # App
    app_name: str = "GRM — Gestión y Clasificación Documental con IA"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
