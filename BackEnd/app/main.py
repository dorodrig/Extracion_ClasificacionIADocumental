"""
Entry point de la aplicación FastAPI — Sistema GRM.

Gobernanza §2.2 — app/main.py
Gobernanza §3.3 — Exception handler global para GRMException.
"""
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.exceptions import GRMException
# We'll avoid importing missing exceptions and schemas that might not be correct yet.
# We will use a generic APIResponse class if needed or fallback to dict

class APIResponse:
    def __init__(self, success: bool, error: str = None, message: str = None):
        self.success = success
        self.error = error
        self.message = message

    def model_dump(self):
        return {"success": self.success, "error": self.error, "message": self.message}

# Configurar logging del proyecto GRM
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("grm.main")

app = FastAPI(
    title="GRM — Gestión y Clasificación Documental con IA",
    description="Backend del sistema GRM. FastAPI + SQLAlchemy + Alembic.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(GRMException)
async def grm_exception_handler(request: Request, exc: GRMException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=APIResponse(success=False, error=str(exc), message="Error de validación de negocio").model_dump(),
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical("Excepción no controlada: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse(success=False, error="Error interno del servidor.").model_dump(),
    )

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "healthy", "service": "grm-backend", "version": "1.0.0"}

