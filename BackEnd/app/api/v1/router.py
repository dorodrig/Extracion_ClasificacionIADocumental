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
