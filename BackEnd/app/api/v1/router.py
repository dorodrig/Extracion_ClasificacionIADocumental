"""
Registro centralizado de todos los routers API v1.

Gobernanza §2.2 — app/api/v1/router.py
Cada módulo de endpoints (HU) se registra aquí con su prefijo.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import rules

api_v1_router = APIRouter(prefix="/api/v1")

# HU-01 — Reglas de Trabajo
api_v1_router.include_router(rules.router)

# HU-03 — OCR
from app.api.v1.endpoints import ocr
api_v1_router.include_router(ocr.router)

# HU-04 — Agente de Contexto IA
from app.api.v1.endpoints import contexto
api_v1_router.include_router(contexto.router)

# HU-07 — Portal Web de Consulta para Cliente Final
from app.api.v1.endpoints import cliente
api_v1_router.include_router(cliente.router, prefix="/cliente", tags=["Cliente"])

# Futuro: Agregar más routers según se implementen las HUs
# from app.api.v1.endpoints import auth, batches, documents, pendientes
# api_v1_router.include_router(auth.router)        # HU-08
# api_v1_router.include_router(batches.router)      # HU-02
# api_v1_router.include_router(documents.router)    # HU-03, HU-05
# api_v1_router.include_router(pendientes.router)   # HU-06
app/api/v1/router.py
Registro central de todos los routers de la API v1.
Cada HU agrega su router aquí (Gobernanza §3.2).
"""
from fastapi import APIRouter
from app.api.v1.endpoints import batches
from app.api.v1.endpoints import pendientes
api_v1_router = APIRouter()

# HU-02 — Ingesta Dual de Documentos (Escáner / Carpeta Local)
api_v1_router.include_router(
    batches.router,
    prefix="/batches",
    tags=["batches"],
)

# HU-01 — Reglas de Trabajo (pendiente — se agregará en su iteración)
# api_v1_router.include_router(rules.router, prefix="/rules", tags=["rules"])

# HU-08 — Autenticación (pendiente — se agregará en su iteración)
# api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# HU-06 — Validación Humana: Pendientes y Visor
api_v1_router.include_router(
    pendientes.router,
    prefix="/pendientes",
    tags=["pendientes"],
)
