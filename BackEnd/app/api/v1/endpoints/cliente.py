import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from fastapi.responses import Response

from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_cliente, MockUser
from app.schemas.cliente_schema import (
    DashboardMetrics, FolderNode, PaginatedDocumentos, DocumentoItem, DocumentoDetail
)
# from app.db.models.documento_db import DocumentosLote

logger = logging.getLogger("grm.api.cliente")

router = APIRouter()

@router.get(
    "/dashboard",
    response_model=DashboardMetrics,
    summary="Métricas del dashboard",
    description="Retorna métricas agregadas del cliente actual (conteo, tipos, pendientes, etc). CA-02, CA-09"
)
def get_dashboard(
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    # Mock data as HU-08 is pending
    return DashboardMetrics(
        total_documentos=150,
        documentos_nuevos=12,
        pendientes_revision=5,
        ultimo_procesado=datetime.now() - timedelta(minutes=15),
        tipos_conteo={"Factura": 80, "Contrato": 50, "Recibo": 20}
    )

@router.get(
    "/carpetas",
    response_model=FolderNode,
    summary="Jerarquía de carpetas",
    description="Retorna un árbol JSON con la jerarquía de carpetas del cliente. CA-03, CA-12"
)
def get_carpetas(
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    return FolderNode(
        id="root",
        nombre="Documentos",
        hijos=[
            FolderNode(id="f1", nombre="Facturas", hijos=[]),
            FolderNode(id="c1", nombre="Contratos", hijos=[
                FolderNode(id="c1-2026", nombre="2026", hijos=[])
            ]),
        ]
    )

@router.get(
    "/documentos",
    response_model=PaginatedDocumentos,
    summary="Listado de documentos con filtros",
    description="Filtros por tipo, fechas, búsqueda y paginación. CA-04"
)
def get_documentos(
    tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo"),
    fecha_inicio: Optional[datetime] = Query(None, description="Desde fecha"),
    fecha_fin: Optional[datetime] = Query(None, description="Hasta fecha"),
    busqueda: Optional[str] = Query(None, description="Buscar en texto o nombre"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    # Mock data
    items = []
    for i in range(1, size + 1):
        items.append(
            DocumentoItem(
                id=i + (page - 1) * size,
                nombre_archivo=f"Doc_Test_{i}.pdf",
                tipo_documento=tipo_documento or "Factura",
                fecha_carga=datetime.now() - timedelta(days=i),
                estado="PROCESADO"
            )
        )
    return PaginatedDocumentos(
        total=100,
        page=page,
        size=size,
        items=items
    )

@router.get(
    "/documentos/{id}",
    response_model=DocumentoDetail,
    summary="Detalle y metadatos de un documento",
    description="Retorna campos extraídos y estado. CA-05"
)
def get_documento_detail(
    id: int = Path(..., description="ID del documento"),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    # CA-01 & CA-08: Forbidden check (simulated)
    if id == 999:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El documento no pertenece al cliente actual."
        )
        
    return DocumentoDetail(
        id=id,
        nombre_archivo=f"Doc_Test_{id}.pdf",
        tipo_documento="Factura",
        fecha_carga=datetime.now() - timedelta(days=1),
        estado="PROCESADO",
        campos_extraidos={"monto": "$1,000.00", "fecha": "2026-05-23"},
        confianza_promedio=95.5
    )

@router.get(
    "/documentos/{id}/archivo",
    summary="Visualizar archivo del documento",
    description="Retorna el binario del archivo para visualización."
)
def get_documento_archivo(
    id: int = Path(...),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    # Mock file return
    return Response(content=b"%PDF-1.4\n%Fake PDF content for testing", media_type="application/pdf")

@router.get(
    "/documentos/{id}/descargar",
    summary="Descargar archivo del documento",
    description="Fuerza la descarga del archivo (Content-Disposition). CA-07"
)
def descargar_documento_archivo(
    id: int = Path(...),
    current_user: MockUser = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    headers = {
        "Content-Disposition": f"attachment; filename=Doc_Test_{id}.pdf"
    }
    return Response(
        content=b"%PDF-1.4\n%Fake PDF content for testing", 
        media_type="application/pdf", 
        headers=headers
    )
