from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class DashboardMetrics(BaseModel):
    total_documentos: int = Field(..., description="Total de documentos del cliente")
    documentos_nuevos: int = Field(..., description="Documentos nuevos hoy o en periodo")
    pendientes_revision: int = Field(..., description="Documentos Pendiente Revisión Humana")
    ultimo_procesado: Optional[datetime] = Field(None, description="Fecha de último documento procesado")
    tipos_conteo: Dict[str, int] = Field(..., description="Conteo por tipo de documento")

class FolderNode(BaseModel):
    id: str = Field(..., description="Identificador único de la carpeta")
    nombre: str = Field(..., description="Nombre de la carpeta")
    hijos: List['FolderNode'] = Field(default_factory=list, description="Subcarpetas")

FolderNode.model_rebuild()

class DocumentoItem(BaseModel):
    id: int = Field(..., description="ID del documento")
    nombre_archivo: str = Field(..., description="Nombre del archivo original")
    tipo_documento: str = Field(..., description="Tipo de documento clasificado")
    fecha_carga: datetime = Field(..., description="Fecha en que se cargó")
    estado: str = Field(..., description="Estado del procesamiento")

class PaginatedDocumentos(BaseModel):
    total: int = Field(..., description="Total de resultados que coinciden")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de la página")
    items: List[DocumentoItem] = Field(..., description="Documentos en la página actual")

class DocumentoDetail(DocumentoItem):
    campos_extraidos: Dict[str, Any] = Field(default_factory=dict, description="Campos clave-valor extraídos")
    confianza_promedio: Optional[float] = Field(None, description="Porcentaje de confianza promedio de extracción")
