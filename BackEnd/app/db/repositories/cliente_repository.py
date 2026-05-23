"""
Repositorio de datos del Cliente (HU-07).

Gobernanza §2.2 — app/db/repositories/cliente_repository.py
Capa de persistencia que consulta documentos clasificados,
pendientes y estructura de carpetas filtrados por cliente_id.
"""
import logging
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc

from app.db.models.documentos_clasificados import DocumentoClasificado
from app.db.models.documentos_pendientes import DocumentoPendiente
from app.db.models.batches import DocumentoLote

logger = logging.getLogger("grm.db.repositories.cliente")


class ClienteRepository:
    """Repositorio de solo-lectura para consultas del portal de cliente."""

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------
    # Dashboard  (CA-02, CA-09)
    # ------------------------------------------------------------------

    def count_documentos_by_cliente(self, cliente_id: int) -> int:
        """Total de documentos clasificados del cliente."""
        return (
            self.db.query(func.count(DocumentoClasificado.id))
            .filter(DocumentoClasificado.cliente_id == cliente_id)
            .scalar()
        ) or 0

    def count_pendientes_revision(self, cliente_id: int) -> int:
        """Documentos con estado 'pendiente' en revisión humana (CA-09)."""
        return (
            self.db.query(func.count(DocumentoPendiente.id))
            .filter(
                DocumentoPendiente.cliente_id == cliente_id,
                DocumentoPendiente.estado == "pendiente",
            )
            .scalar()
        ) or 0

    def count_documentos_nuevos(self, cliente_id: int, desde: datetime) -> int:
        """Documentos clasificados después de la fecha dada."""
        return (
            self.db.query(func.count(DocumentoClasificado.id))
            .filter(
                DocumentoClasificado.cliente_id == cliente_id,
                DocumentoClasificado.created_at >= desde,
            )
            .scalar()
        ) or 0

    def get_ultimo_procesado(self, cliente_id: int) -> Optional[datetime]:
        """Fecha del último documento clasificado."""
        result = (
            self.db.query(func.max(DocumentoClasificado.timestamp_clasificacion))
            .filter(DocumentoClasificado.cliente_id == cliente_id)
            .scalar()
        )
        return result

    def get_tipos_conteo(self, cliente_id: int) -> dict[str, int]:
        """Conteo agrupado por tipo_documento."""
        rows = (
            self.db.query(
                DocumentoClasificado.tipo_documento,
                func.count(DocumentoClasificado.id),
            )
            .filter(DocumentoClasificado.cliente_id == cliente_id)
            .group_by(DocumentoClasificado.tipo_documento)
            .all()
        )
        return {tipo: count for tipo, count in rows}

    # ------------------------------------------------------------------
    # Documentos paginados  (CA-04)
    # ------------------------------------------------------------------

    def get_documentos_paginados(
        self,
        cliente_id: int,
        page: int,
        size: int,
        tipo_documento: Optional[str] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        busqueda: Optional[str] = None,
    ) -> tuple[list[DocumentoClasificado], int]:
        """Retorna documentos clasificados con filtros y paginación."""
        query = self.db.query(DocumentoClasificado).filter(
            DocumentoClasificado.cliente_id == cliente_id
        )

        if tipo_documento:
            query = query.filter(DocumentoClasificado.tipo_documento == tipo_documento)
        if fecha_inicio:
            query = query.filter(DocumentoClasificado.created_at >= fecha_inicio)
        if fecha_fin:
            query = query.filter(DocumentoClasificado.created_at <= fecha_fin)
        if busqueda:
            query = query.filter(
                or_(
                    DocumentoClasificado.tipo_documento.ilike(f"%{busqueda}%"),
                    DocumentoClasificado.ruta_destino_final.ilike(f"%{busqueda}%"),
                )
            )

        total = query.count()
        offset = (page - 1) * size
        items = (
            query.order_by(desc(DocumentoClasificado.created_at))
            .offset(offset)
            .limit(size)
            .all()
        )
        return items, total

    # ------------------------------------------------------------------
    # Detalle de un documento  (CA-05)
    # ------------------------------------------------------------------

    def get_documento_by_id(
        self, documento_id: int
    ) -> Optional[DocumentoClasificado]:
        """Obtiene un documento clasificado por su ID."""
        return (
            self.db.query(DocumentoClasificado)
            .filter(DocumentoClasificado.id == documento_id)
            .first()
        )

    def get_nombre_archivo(self, documento_id: int) -> Optional[str]:
        """Obtiene el nombre del archivo original desde documentos_lote."""
        doc_lote = (
            self.db.query(DocumentoLote)
            .filter(DocumentoLote.id == documento_id)
            .first()
        )
        return doc_lote.nombre_archivo if doc_lote else None

    # ------------------------------------------------------------------
    # Carpetas  (CA-03, CA-12)
    # ------------------------------------------------------------------

    def get_rutas_destino(self, cliente_id: int) -> list[str]:
        """Obtiene todas las rutas destino únicas del cliente para construir el árbol."""
        rows = (
            self.db.query(DocumentoClasificado.ruta_destino_final)
            .filter(DocumentoClasificado.cliente_id == cliente_id)
            .distinct()
            .all()
        )
        return [r[0] for r in rows if r[0]]
