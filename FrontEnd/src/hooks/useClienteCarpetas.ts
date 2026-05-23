import { useQuery } from '@tanstack/react-query';
import { clienteService } from '@/services/clienteService';
import type { FolderNode } from '@/types/cliente';

export const useClienteCarpetas = () => {
  return useQuery<FolderNode>({
    queryKey: ['cliente-carpetas'],
    queryFn: () => clienteService.getCarpetas(),
  });
};
