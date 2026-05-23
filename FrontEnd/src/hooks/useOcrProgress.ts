import { useQuery } from '@tanstack/react-query';
import { ocrService } from '../services/ocrService';

export const useOcrProgress = (batchId: string | undefined) => {
  return useQuery({
    queryKey: ['ocrProgress', batchId],
    queryFn: () => ocrService.getProgress(batchId!),
    enabled: !!batchId,
    // Poll every 3 seconds ONLY if status is 'en_proceso' or 'pendiente'
    refetchInterval: (query) => {
      const status = query.state?.data?.status;
      if (status === 'en_proceso' || status === 'pendiente') {
        return 3000;
      }
      return false;
    },
  });
};
