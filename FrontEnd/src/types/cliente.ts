/**
 * TypeScript interfaces for HU-07 Portal Cliente
 * Mirror of backend schemas: BackEnd/app/schemas/cliente_schema.py
 * Gobernanza §4.2 — Tipado obligatorio
 */

export interface DashboardMetrics {
  total_documentos: number;
  documentos_nuevos: number;
  pendientes_revision: number;
  ultimo_procesado: string | null;
  tipos_conteo: Record<string, number>;
}

export interface FolderNode {
  id: string;
  nombre: string;
  hijos: FolderNode[];
}

export interface DocumentoItem {
  id: number;
  nombre_archivo: string;
  tipo_documento: string;
  fecha_carga: string;
  estado: string;
}

export interface PaginatedDocumentos {
  total: number;
  page: number;
  size: number;
  items: DocumentoItem[];
}

export interface DocumentoDetail extends DocumentoItem {
  campos_extraidos: Record<string, unknown>;
  confianza_promedio: number | null;
}

export interface DocumentosFilterParams {
  tipo_documento?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  busqueda?: string;
  page: number;
  size: number;
}
