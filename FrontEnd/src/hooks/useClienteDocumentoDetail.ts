import { useQuery } from '@tanstack/react-query';
import { clienteService } from '@/services/clienteService';
import type { DocumentoDetail } from '@/types/cliente';

export const useClienteDocumentoDetail = (id: number | null) => {
  return useQuery<DocumentoDetail>({
    queryKey: ['cliente-documento', id],
    queryFn: () => clienteService.getDocumentoDetail(id!),
    enabled: id !== null,
  });
};
