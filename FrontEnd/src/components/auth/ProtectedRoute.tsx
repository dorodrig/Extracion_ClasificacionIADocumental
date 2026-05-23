import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

interface ProtectedRouteProps {
  allowedRoles?: ('Admin' | 'Operario' | 'Cliente')[];
}

export const ProtectedRoute = ({ allowedRoles }: ProtectedRouteProps) => {
  const { token, user, selectedClient } = useAuthStore();
  const location = useLocation();

  /*
  if (!token || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // Or redirect to some default page, let's just go to their natural root or login for simplicity
    return <Navigate to="/login" replace />;
  }

  if (user.role === 'Operario' && !selectedClient && location.pathname !== '/operario/seleccion-cliente') {
    return <Navigate to="/operario/seleccion-cliente" replace />;
  }
  */

  return <Outlet />;
};
