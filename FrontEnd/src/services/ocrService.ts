import api from './api';

export interface OcrProgressResponse {
  batch_id: string;
  status: 'pendiente' | 'en_proceso' | 'completado' | 'error';
  processed_pages: number;
  total_pages: number;
  errors: number;
}

export const ocrService = {
  getProgress: async (batchId: string): Promise<OcrProgressResponse> => {
    const response = await api.get<OcrProgressResponse>(`/api/v1/ocr/progress/${batchId}`);
    return response.data;
  },
};
