import { useQuery } from '@tanstack/react-query';
import { clienteService } from '@/services/clienteService';
import type { DashboardMetrics } from '@/types/cliente';

export const useClienteDashboard = () => {
  return useQuery<DashboardMetrics>({
    queryKey: ['cliente-dashboard'],
    queryFn: () => clienteService.getDashboard(),
    staleTime: 60000,
  });
};
