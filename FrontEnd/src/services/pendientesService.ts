import axios from 'axios';

export interface PendingDocument {
  id: string;
  filename: string;
  cliente: string;
  motivoRechazo: string;
  enColaDesde: string; // ISO String
  lote: string;
}

export interface ExtractedField {
  id: string;
  nombre: string;
  valor: string | null;
  obligatorio: boolean;
  estado: 'Validado' | 'No encontrado' | 'Baja confianza';
  ocrScore: number | null;
}

export interface DocumentViewerData {
  id: string;
  pdfUrl: string;
  campos: ExtractedField[];
  motivoRechazo: string;
  lote: string;
}

const API_BASE_URL = '/api/v1'; // Configurar según base URL

export const pendientesService = {
  getListaPendientes: async (): Promise<PendingDocument[]> => {
    const response = await axios.get(`${API_BASE_URL}/pendientes`);
    return response.data.data || response.data;
  },

  getVisorDatos: async (id: string): Promise<DocumentViewerData> => {
    const response = await axios.get(`${API_BASE_URL}/pendientes/${id}/visor`);
    return response.data.data || response.data;
  },

  corregirDocumento: async (id: string, camposCorregidos: Record<string, string>) => {
    const response = await axios.put(`${API_BASE_URL}/pendientes/${id}/correccion`, camposCorregidos);
    return response.data;
  },

  enviarInstruccion: async (id: string, instruccion: string) => {
    const response = await axios.post(`${API_BASE_URL}/pendientes/${id}/instruccion`, { instruccion });
    return response.data;
  },

  descartarDocumento: async (id: string, motivo: string) => {
    const response = await axios.put(`${API_BASE_URL}/pendientes/${id}/descarte`, { motivo });
    return response.data;
  }
};
