/**
 * Servicio HTTP para HU-07 Portal Cliente
 * Gobernanza §4.3 — Usa instancia Axios centralizada
 */
import api from '@/services/api';
import type {
  DashboardMetrics,
  FolderNode,
  PaginatedDocumentos,
  DocumentoDetail,
  DocumentosFilterParams,
} from '@/types/cliente';

const BASE = '/api/v1/cliente';

export const clienteService = {
  /** GET /api/v1/cliente/dashboard */
  async getDashboard(): Promise<DashboardMetrics> {
    const { data } = await api.get<DashboardMetrics>(`${BASE}/dashboard`);
    return data;
  },

  /** GET /api/v1/cliente/carpetas */
  async getCarpetas(): Promise<FolderNode> {
    const { data } = await api.get<FolderNode>(`${BASE}/carpetas`);
    return data;
  },

  /** GET /api/v1/cliente/documentos?... */
  async getDocumentos(params: DocumentosFilterParams): Promise<PaginatedDocumentos> {
    const query: Record<string, string | number> = {
      page: params.page,
      size: params.size,
    };

    if (params.tipo_documento) query.tipo_documento = params.tipo_documento;
    if (params.fecha_inicio) query.fecha_inicio = params.fecha_inicio;
    if (params.fecha_fin) query.fecha_fin = params.fecha_fin;
    if (params.busqueda) query.busqueda = params.busqueda;

    const { data } = await api.get<PaginatedDocumentos>(`${BASE}/documentos`, {
      params: query,
    });
    return data;
  },

  /** GET /api/v1/cliente/documentos/{id} */
  async getDocumentoDetail(id: number): Promise<DocumentoDetail> {
    const { data } = await api.get<DocumentoDetail>(`${BASE}/documentos/${id}`);
    return data;
  },

  /** Returns the full URL to view the document file in-browser */
  getDocumentoArchivoUrl(id: number): string {
    const baseUrl = (api.defaults.baseURL ?? '').replace(/\/$/, '');
    return `${baseUrl}/api/v1/cliente/documentos/${id}/archivo`;
  },

  /** Downloads the document file triggering a browser save-as dialog */
  async descargarDocumento(id: number): Promise<void> {
    const { data, headers } = await api.get<Blob>(
      `${BASE}/documentos/${id}/descargar`,
      { responseType: 'blob' },
    );

    // Extract filename from Content-Disposition header or fallback
    const disposition = headers['content-disposition'] as string | undefined;
    let filename = `documento_${id}`;
    if (disposition) {
      const match = disposition.match(/filename\*?=(?:UTF-8'')?["']?([^"';\n]+)/i);
      if (match?.[1]) filename = decodeURIComponent(match[1]);
    }

    const url = window.URL.createObjectURL(data);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
    window.URL.revokeObjectURL(url);
  },
};
