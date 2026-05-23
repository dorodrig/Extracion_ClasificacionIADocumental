"""
Servicio (Use Case) del Portal de Cliente (HU-07).

Gobernanza §2.2 — app/services/cliente_service.py
Capa de lógica de negocio que orquesta las consultas del repositorio
y transforma los datos a los schemas de respuesta.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.db.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente_schema import (
    DashboardMetrics,
    FolderNode,
    PaginatedDocumentos,
    DocumentoItem,
    DocumentoDetail,
)

logger = logging.getLogger("grm.services.cliente")


class ClienteService:
    """Casos de uso del portal de consulta para el cliente final."""

    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    # ------------------------------------------------------------------
    # Dashboard  (CA-02, CA-09)
    # ------------------------------------------------------------------

    def get_dashboard(self, cliente_id: int) -> DashboardMetrics:
        """
        Retorna métricas agregadas del cliente.

        CA-02: conteo, tipos, último procesado, documentos nuevos.
        CA-09: incluye conteo de pendientes de revisión humana.
        """
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        total = self.repo.count_documentos_by_cliente(cliente_id)
        nuevos = self.repo.count_documentos_nuevos(cliente_id, hoy)
        pendientes = self.repo.count_pendientes_revision(cliente_id)
        ultimo = self.repo.get_ultimo_procesado(cliente_id)
        tipos = self.repo.get_tipos_conteo(cliente_id)

        return DashboardMetrics(
            total_documentos=total,
            documentos_nuevos=nuevos,
            pendientes_revision=pendientes,
            ultimo_procesado=ultimo,
            tipos_conteo=tipos,
        )

    # ------------------------------------------------------------------
    # Carpetas  (CA-03, CA-12)
    # ------------------------------------------------------------------

    def get_carpetas(self, cliente_id: int) -> FolderNode:
        """
        Construye un árbol JSON de carpetas a partir de las rutas
        destino únicas del cliente.

        CA-03: Jerarquía visual de carpetas.
        CA-12: Árbol JSON representando la estructura.
        """
        rutas = self.repo.get_rutas_destino(cliente_id)
        return self._build_folder_tree(rutas)

    @staticmethod
    def _build_folder_tree(rutas: list[str]) -> FolderNode:
        """Construye un FolderNode raíz a partir de una lista de rutas."""
        root = FolderNode(id="root", nombre="Documentos", hijos=[])

        if not rutas:
            return root

        children_map: dict[str, FolderNode] = {}

        for ruta in rutas:
            # Normalizar separadores
            parts = ruta.replace("\\", "/").strip("/").split("/")
            current_children = root.hijos
            current_path = ""

            for part in parts:
                current_path = f"{current_path}/{part}" if current_path else part
                node_id = current_path.replace("/", "_").lower()

                if node_id not in children_map:
                    new_node = FolderNode(id=node_id, nombre=part, hijos=[])
                    children_map[node_id] = new_node
                    current_children.append(new_node)

                current_children = children_map[node_id].hijos

        return root

    # ------------------------------------------------------------------
    # Documentos paginados  (CA-04)
    # ------------------------------------------------------------------

    def get_documentos(
        self,
        cliente_id: int,
        page: int,
        size: int,
        tipo_documento: Optional[str] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        busqueda: Optional[str] = None,
    ) -> PaginatedDocumentos:
        """
        Retorna documentos paginados con filtros.

        CA-04: Paginación, filtro por tipo_documento, rango de fechas y búsqueda.
        """
        items_db, total = self.repo.get_documentos_paginados(
            cliente_id=cliente_id,
            page=page,
            size=size,
            tipo_documento=tipo_documento,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            busqueda=busqueda,
        )

        items = []
        for doc in items_db:
            nombre = self.repo.get_nombre_archivo(doc.documento_id) or f"Doc_{doc.documento_id}"
            items.append(
                DocumentoItem(
                    id=doc.id,
                    nombre_archivo=nombre,
                    tipo_documento=doc.tipo_documento,
                    fecha_carga=doc.created_at,
                    estado="PROCESADO",
                )
            )

        return PaginatedDocumentos(
            total=total,
            page=page,
            size=size,
            items=items,
        )

    # ------------------------------------------------------------------
    # Detalle de documento  (CA-05)
    # ------------------------------------------------------------------

    def get_documento_detail(
        self, documento_id: int, cliente_id: int
    ) -> Optional[DocumentoDetail]:
        """
        Retorna detalle de un documento incluyendo campos extraídos.

        CA-05: Metadatos y campos extraídos.
        CA-01 / CA-08: Retorna None si el documento no pertenece al cliente.
        """
        doc = self.repo.get_documento_by_id(documento_id)
        if doc is None:
            return None

        # Validación de ownership (CA-01 & CA-08)
        if doc.cliente_id != cliente_id:
            return "FORBIDDEN"

        nombre = self.repo.get_nombre_archivo(doc.documento_id) or f"Doc_{doc.documento_id}"
        campos = doc.campos_extraidos_json or {}

        # Calcular confianza promedio si los campos tienen un campo "confianza"
        confianza = None
        if isinstance(campos, dict) and campos:
            confianzas = [
                v.get("confianza", 0)
                for v in campos.values()
                if isinstance(v, dict) and "confianza" in v
            ]
            if confianzas:
                confianza = sum(confianzas) / len(confianzas)

        return DocumentoDetail(
            id=doc.id,
            nombre_archivo=nombre,
            tipo_documento=doc.tipo_documento,
            fecha_carga=doc.created_at,
            estado="PROCESADO",
            campos_extraidos=campos,
            confianza_promedio=confianza,
        )

    # ------------------------------------------------------------------
    # Descarga  (CA-07)
    # ------------------------------------------------------------------

    def get_ruta_archivo(self, documento_id: int, cliente_id: int) -> Optional[str]:
        """
        Retorna la ruta del archivo para descarga.
        Retorna None si el documento no existe o no pertenece al cliente.
        Retorna 'FORBIDDEN' si el documento pertenece a otro cliente.
        """
        doc = self.repo.get_documento_by_id(documento_id)
        if doc is None:
            return None
        if doc.cliente_id != cliente_id:
            return "FORBIDDEN"
        return doc.ruta_destino_final
