"""
Registro centralizado de todos los routers API v1.

Gobernanza §2.2 — app/api/v1/router.py
Cada módulo de endpoints (HU) se registra aquí con su prefijo.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import rules, batches, ocr, contexto, cliente, pendientes

api_v1_router = APIRouter()

# HU-01 — Reglas de Trabajo
api_v1_router.include_router(rules.router)

# HU-02 — Ingesta Dual de Documentos
api_v1_router.include_router(batches.router, prefix="/batches", tags=["batches"])

# HU-03 — OCR
api_v1_router.include_router(ocr.router)

# HU-04 — Agente de Contexto IA
api_v1_router.include_router(contexto.router)

# HU-07 — Portal Web de Consulta para Cliente Final
api_v1_router.include_router(cliente.router, prefix="/cliente", tags=["Cliente"])

# HU-06 — Validación Humana: Pendientes y Visor
api_v1_router.include_router(pendientes.router, prefix="/pendientes", tags=["pendientes"])
"""
app/api/v1/router.py
Registro central de todos los routers de la API v1.
Cada HU agrega su router aquí (Gobernanza §3.2).
"""
from fastapi import APIRouter
from app.api.v1.endpoints import batches
from app.api.v1.endpoints import pendientes
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import usuarios
from app.api.v1.endpoints import auditoria
api_v1_router = APIRouter()

# HU-02 — Ingesta Dual de Documentos (Escáner / Carpeta Local)
api_v1_router.include_router(
    batches.router,
    prefix="/batches",
    tags=["batches"],
)

# HU-01 — Reglas de Trabajo (pendiente — se agregará en su iteración)
# api_v1_router.include_router(rules.router, prefix="/rules", tags=["rules"])

# HU-08 — Autenticación
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])

# HU-06 — Validación Humana: Pendientes y Visor
api_v1_router.include_router(
    pendientes.router,
    prefix="/pendientes",
    tags=["pendientes"],
)

# HU-09 — Trazabilidad, Auditoría y Log de Procesos
api_v1_router.include_router(
    auditoria.router,
    prefix="/auditoria",
    tags=["auditoria"],
)
