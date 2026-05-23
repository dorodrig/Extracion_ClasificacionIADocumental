"""
app/main.py
Entry point de la aplicación FastAPI — GRM Sistema de Clasificación Documental con IA.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import GRMException
from app.schemas.common import APIResponse
from app.api.v1.router import api_v1_router

# Configuración de logging global
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("grm.main")

app = FastAPI(
    title="GRM — Gestión y Clasificación Documental con IA",
    description=(
        "Backend del sistema GRM. FastAPI + SQLAlchemy + Alembic. "
        "Gobernanza v1.1.0 — Clean Architecture (Ports & Adapters)."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Registro del router principal v1 ──────────────────────────────────────────
app.include_router(api_v1_router, prefix="/api/v1")


# ── Exception handlers globales (Gobernanza §3.3) ─────────────────────────────
@app.exception_handler(GRMException)
async def grm_exception_handler(request: Request, exc: GRMException):
    logger.error("GRMException capturada: %s", exc)
    return JSONResponse(
        status_code=400,
        content=APIResponse(success=False, error=str(exc)).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical("Excepción no controlada: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            error="Error interno del servidor.",
        ).model_dump(),
    )


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "sistema": "GRM"}
