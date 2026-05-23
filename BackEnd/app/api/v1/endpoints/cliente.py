"""
Endpoints del Portal Web de Consulta para Cliente Final (HU-07).

Gobernanza §2.2 — app/api/v1/endpoints/cliente.py
Capa Controller: recibe HTTP, delega al Service, retorna JSON.

CAs cubiertos:
    CA-01: Protección JWT en todas las rutas.
    CA-02: Dashboard con métricas agregadas.
    CA-03: Árbol de carpetas del cliente.
    CA-04: Listado paginado con filtros y búsqueda.
    CA-05: Detalle de documento con campos extraídos.
    CA-07: Descarga de archivo con Content-Disposition.
    CA-08: Validación de ownership por cliente_id (403).
    CA-09: Conteo de pendientes de revisión humana.
    CA-12: Árbol JSON de jerarquía de carpetas.
"""
import logging
import os
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import FileResponse, Response

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_cliente, get_db, MockUser
from app.schemas.cliente_schema import (
    DashboardMetrics,
    DocumentoDetail,
    FolderNode,
    PaginatedDocumentos,
)
from app.services.cliente_service import ClienteService

logger = logging.getLogger("grm.api.cliente")

router = APIRouter()


# ---------------------------------------------------------------------------
# CA-02 & CA-09 — Dashboard
# ---------------------------------------------------------------------------


@router.get(
    "/dashboard",
    response_model=DashboardMetrics,
    summary="Métricas del dashboard del cliente",
    description=(
        "Retorna métricas agregadas: total de documentos, documentos nuevos, "
        "pendientes de revisión humana (CA-09), último procesado y conteo por tipo."
    ),
)
def get_dashboard(
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db),
):
    """CA-02 / CA-09: Métricas agregadas del cliente."""
    service = ClienteService(db)
    return service.get_dashboard(current_user.cliente_id)


# ---------------------------------------------------------------------------
# CA-03 & CA-12 — Carpetas
# ---------------------------------------------------------------------------


@router.get(
    "/carpetas",
    response_model=FolderNode,
    summary="Jerarquía de carpetas del cliente",
    description="Retorna un árbol JSON con la estructura de carpetas del cliente.",
)
def get_carpetas(
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db),
):
    """CA-03 / CA-12: Árbol JSON de carpetas."""
    service = ClienteService(db)
    return service.get_carpetas(current_user.cliente_id)


# ---------------------------------------------------------------------------
# CA-04 — Listado paginado de documentos
# ---------------------------------------------------------------------------


@router.get(
    "/documentos",
    response_model=PaginatedDocumentos,
    summary="Listado de documentos con filtros y paginación",
    description=(
        "Retorna documentos paginados del cliente. "
        "Soporta filtros por tipo_documento, rango de fechas y búsqueda de texto."
    ),
)
def get_documentos(
    tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo de documento"),
    fecha_inicio: Optional[datetime] = Query(None, description="Desde fecha (ISO 8601)"),
    fecha_fin: Optional[datetime] = Query(None, description="Hasta fecha (ISO 8601)"),
    busqueda: Optional[str] = Query(None, description="Buscar en texto o nombre"),
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db),
):
    """CA-04: Documentos paginados con filtros."""
    service = ClienteService(db)
    return service.get_documentos(
        cliente_id=current_user.cliente_id,
        page=page,
        size=size,
        tipo_documento=tipo_documento,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        busqueda=busqueda,
    )


# ---------------------------------------------------------------------------
# CA-05 — Detalle de documento
# ---------------------------------------------------------------------------


@router.get(
    "/documentos/{id}",
    response_model=DocumentoDetail,
    summary="Detalle y metadatos de un documento",
    description="Retorna metadatos completos y campos extraídos por IA.",
)
def get_documento_detail(
    id: int = Path(..., description="ID del documento clasificado"),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db),
):
    """CA-05: Detalle con campos extraídos. CA-01/CA-08: Ownership check."""
    service = ClienteService(db)
    result = service.get_documento_detail(id, current_user.cliente_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado.",
        )
    if result == "FORBIDDEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El documento no pertenece al cliente actual.",
        )
    return result


# ---------------------------------------------------------------------------
# CA-07 — Visualizar archivo
# ---------------------------------------------------------------------------


@router.get(
    "/documentos/{id}/archivo",
    summary="Visualizar archivo del documento",
    description="Retorna el binario del archivo para visualización inline.",
)
def get_documento_archivo(
    id: int = Path(..., description="ID del documento clasificado"),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db),
):
    """Visualización inline del archivo asociado al documento."""
    service = ClienteService(db)
    ruta = service.get_ruta_archivo(id, current_user.cliente_id)

    if ruta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado.",
        )
    if ruta == "FORBIDDEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El documento no pertenece al cliente actual.",
        )

    if os.path.exists(ruta):
        return FileResponse(ruta)

    # Fallback mock si el archivo físico no existe aún
    return Response(
        content=b"%PDF-1.4\n%Placeholder - archivo no disponible en disco",
        media_type="application/pdf",
    )


# ---------------------------------------------------------------------------
# CA-07 — Descargar archivo
# ---------------------------------------------------------------------------


@router.get(
    "/documentos/{id}/descargar",
    summary="Descargar archivo del documento",
    description="Fuerza la descarga del archivo con Content-Disposition: attachment.",
)
def descargar_documento(
    id: int = Path(..., description="ID del documento clasificado"),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db),
):
    """CA-07: Descarga forzada con Content-Disposition: attachment."""
    service = ClienteService(db)
    ruta = service.get_ruta_archivo(id, current_user.cliente_id)

    if ruta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado.",
        )
    if ruta == "FORBIDDEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El documento no pertenece al cliente actual.",
        )

    filename = os.path.basename(ruta) if ruta else f"documento_{id}.pdf"

    if os.path.exists(ruta):
        return FileResponse(
            path=ruta,
            filename=filename,
            media_type="application/octet-stream",
        )

    # Fallback mock
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(
        content=b"%PDF-1.4\n%Placeholder - archivo no disponible en disco",
        media_type="application/pdf",
        headers=headers,
    )
