import { useQuery } from '@tanstack/react-query';
import { clienteService } from '@/services/clienteService';
import type { PaginatedDocumentos, DocumentosFilterParams } from '@/types/cliente';

export const useClienteDocumentos = (params: DocumentosFilterParams) => {
  return useQuery<PaginatedDocumentos>({
    queryKey: ['cliente-documentos', params],
    queryFn: () => clienteService.getDocumentos(params),
    enabled: params.page >= 1 && params.size >= 1,
  });
};
