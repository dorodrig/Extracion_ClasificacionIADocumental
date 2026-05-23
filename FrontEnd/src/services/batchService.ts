import api from './api';

export interface Batch {
  id: number;
  batch_id: string;
  estado: string;
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
  }
};
