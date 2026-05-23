"""
Entry point de la aplicación FastAPI — Sistema GRM.

Gobernanza §2.2 — app/main.py
Gobernanza §3.3 — Exception handler global para GRMException.

Responsabilidades:
    - Crear la instancia de FastAPI con metadatos OpenAPI.
    - Registrar el exception handler global para GRMException.
    - Registrar CORS middleware.
    - Incluir el router principal (api/v1).
    - Proveer health check endpoint.
"""
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.domain.exceptions import GRMException, RuleNotFoundException, RuleNameAlreadyExistsException
from app.schemas.rule_schema import APIResponse

# Configurar logging del proyecto GRM
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("grm.main")

# ---------------------------------------------------------------------------
# Instancia FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(
    title="GRM — Gestión y Clasificación Documental con IA",
    description=(
        "API REST del sistema GRM para gestión de reglas de trabajo, "
        "ingesta de documentos, procesamiento OCR, extracción IA y "
        "clasificación documental automática."
    ),
    version="1.0.0",
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

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Exception Handlers — Gobernanza §3.3
# ---------------------------------------------------------------------------


@app.exception_handler(RuleNotFoundException)
async def rule_not_found_handler(
    request: Request, exc: RuleNotFoundException
) -> JSONResponse:
    """Handler específico para reglas no encontradas → 404."""
    logger.warning("Regla no encontrada: %s", str(exc))
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=APIResponse(
            success=False,
            error=str(exc),
            message="Recurso no encontrado",
        ).model_dump(),
    )


@app.exception_handler(RuleNameAlreadyExistsException)
async def rule_name_already_exists_handler(
    request: Request, exc: RuleNameAlreadyExistsException
) -> JSONResponse:
    """Handler específico para nombre de regla duplicado → 409 (CA-12)."""
    logger.warning("Nombre de regla duplicado: %s", str(exc))
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=APIResponse(
            success=False,
            error=str(exc),
            message="Conflicto en nombre de regla",
        ).model_dump(),
    )


@app.exception_handler(GRMException)
async def grm_exception_handler(
    request: Request, exc: GRMException
) -> JSONResponse:
    """
    Handler global para todas las excepciones de dominio GRM.

    Gobernanza §3.3: Las excepciones de dominio tipadas se traducen
    a respuestas APIResponse con success=False y código 400.
    """
    logger.warning("Excepción de dominio GRM: %s", str(exc))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=APIResponse(
            success=False,
            error=str(exc),
            message="Error de validación de negocio",
        ).model_dump(),
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
async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Handler de último recurso para errores no capturados.

    Registra el error completo en logs pero NO expone detalles
    internos al cliente (seguridad).
    """
    logger.error("Error interno no capturado: %s", str(exc), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            success=False,
            error="Error interno del servidor",
            message="Ha ocurrido un error inesperado. Contacte al administrador.",
async def generic_exception_handler(request: Request, exc: Exception):
    logger.critical("Excepción no controlada: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            error="Error interno del servidor.",
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(api_v1_router)

# ---------------------------------------------------------------------------
# Health Check — Preparación Cloud-Ready (Gobernanza §9.4)
# ---------------------------------------------------------------------------


@app.get(
    "/health",
    tags=["Sistema"],
    summary="Health check del sistema GRM",
)
def health_check() -> dict:
    """Endpoint de health check para monitoreo y balanceadores de carga."""
    return {"status": "healthy", "service": "grm-backend", "version": "1.0.0"}


logger.info("GRM Backend inicializado correctamente.")
# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "sistema": "GRM"}
