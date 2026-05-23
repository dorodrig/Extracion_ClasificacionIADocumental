"""
Registro centralizado de todos los routers API v1.

Gobernanza §2.2 — app/api/v1/router.py
Cada módulo de endpoints (HU) se registra aquí con su prefijo.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    rules,
    batches,
    ocr,
    contexto,
    cliente,
    pendientes,
    auth,
    usuarios,
    auditoria,
    clasificacion,
)

api_v1_router = APIRouter()

# HU-01 — Reglas de Trabajo
api_v1_router.include_router(rules.router)

# HU-02 — Ingesta Dual de Documentos
api_v1_router.include_router(batches.router, prefix="/batches", tags=["batches"])

# HU-03 — OCR
api_v1_router.include_router(ocr.router)

# HU-04 — Agente de Contexto IA
api_v1_router.include_router(contexto.router)

# HU-05 — Agente de Clasificación IA
api_v1_router.include_router(clasificacion.router)

# HU-07 — Portal Web de Consulta para Cliente Final
api_v1_router.include_router(cliente.router, prefix="/cliente", tags=["Cliente"])

# HU-06 — Validación Humana: Pendientes y Visor
api_v1_router.include_router(pendientes.router, prefix="/pendientes", tags=["pendientes"])

# HU-08 — Autenticación y Usuarios
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])

# HU-09 — Trazabilidad, Auditoría y Log de Procesos
api_v1_router.include_router(auditoria.router, prefix="/auditoria", tags=["auditoria"])

