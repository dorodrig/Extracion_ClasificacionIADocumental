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

# Futuro: Agregar más routers según se implementen las HUs
# from app.api.v1.endpoints import auth, batches, documents, pendientes
# api_v1_router.include_router(auth.router)        # HU-08
# api_v1_router.include_router(batches.router)      # HU-02
# api_v1_router.include_router(documents.router)    # HU-03, HU-05
# api_v1_router.include_router(pendientes.router)   # HU-06
