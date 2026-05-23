import api from './api';

export interface Batch {
  id: number;
  batch_id: string;
  estado: string;
}

export interface BatchStatusResponse {
  batch_id: string;
  estado: 'preparando' | 'en_proceso' | 'completado' | 'error';
  documentos_preparados: number;
  total_documentos: number;
  ruta_temporal: string | null;
  archivos_omitidos: string[];
}

export interface DocumentoIngestado {
  nombre_archivo: string;
  extension: string;
  ruta_original: string;
  total_paginas?: number;
}

export interface BatchPrepareRequest {
  documentos: DocumentoIngestado[];
}

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export const batchService = {
  createBatch: async (mode: 'scanner' | 'carpeta'): Promise<APIResponse<Batch>> => {
    try {
      const response = await api.post<APIResponse<Batch>>('/api/v1/batches', { mode });
      return response.data;
    } catch (error) {
      // Mock fallback as approved by the architect
      console.warn('Backend unavailable, using mock batch_id');
      return {
        success: true,
        data: {
          id: Date.now(),
          batch_id: `GRM-${new Date().toISOString().slice(0,10).replace(/-/g,'')}-001`,
          estado: 'created'
        }
      };
    }
  },
  
  prepareBatch: async (batchId: string, data: BatchPrepareRequest): Promise<APIResponse<BatchStatusResponse>> => {
    try {
      const response = await api.post<APIResponse<BatchStatusResponse>>(`/api/v1/batches/${batchId}/prepare`, data);
      return response.data;
    } catch (error: any) {
      console.error('Error in prepareBatch', error);
      return { success: false, error: error.message };
    }
  },

  getBatchStatus: async (batchId: string): Promise<APIResponse<BatchStatusResponse>> => {
    try {
      const response = await api.get<APIResponse<BatchStatusResponse>>(`/api/v1/batches/${batchId}/status`);
      return response.data;
    } catch (error: any) {
      console.error('Error in getBatchStatus', error);
      return { success: false, error: error.message };
    }
  }
};
