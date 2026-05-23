import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { IntakeDashboard } from './components/intake/IntakeDashboard';
import { PendientesPage } from './pages/PendientesPage';
import { LoginPage } from './pages/auth/LoginPage';
import { SeleccionClientePage } from './pages/auth/SeleccionClientePage';
import { GestionUsuariosPage } from './pages/admin/GestionUsuariosPage';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { useAuthStore } from './store/authStore';

const INACTIVITY_TIMEOUT = 15 * 60 * 1000; // 15 minutes

const SessionManager = ({ children }: { children: React.ReactNode }) => {
  const logout = useAuthStore((state) => state.logout);
  const token = useAuthStore((state) => state.token);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) return;

    let timeoutId: NodeJS.Timeout;

    const resetTimer = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        logout();
        navigate('/login');
      }, INACTIVITY_TIMEOUT);
    };

    window.addEventListener('mousemove', resetTimer);
    window.addEventListener('keypress', resetTimer);
    window.addEventListener('click', resetTimer);
    window.addEventListener('scroll', resetTimer);

    resetTimer();

    return () => {
      clearTimeout(timeoutId);
      window.removeEventListener('mousemove', resetTimer);
      window.removeEventListener('keypress', resetTimer);
      window.removeEventListener('click', resetTimer);
      window.removeEventListener('scroll', resetTimer);
    };
  }, [token, logout, navigate]);

  return <>{children}</>;
};

const AppLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, selectedClient, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = (e: React.MouseEvent) => {
    e.preventDefault();
    logout();
    navigate('/login');
  };

  const handleCambiarCliente = (e: React.MouseEvent) => {
    e.preventDefault();
    navigate('/operario/seleccion-cliente');
  };

  return (
    <div className="grm-app">
      <header className="grm-app__header">
        <div className="grm-app__logo">GRM</div>
        <div className="grm-app__user-info">
          {user ? (
            <>
              {user.role}: {user.nombre} 
              {selectedClient && ` | Cliente: ${selectedClient}`}
              {user.role === 'Operario' && <a href="#" onClick={handleCambiarCliente}> [Cambiar]</a>}
              <a href="#" onClick={handleLogout}> [Salir]</a>
            </>
          ) : (
            <a href="/login">Iniciar Sesión</a>
          )}
        </div>
      </header>
      <div className="grm-app__body">
        <aside className="grm-app__sidebar">
          <nav>
            <ul>
              <li>Inicio</li>
              {user?.role === 'Admin' && <li onClick={() => navigate('/admin/gestion-usuarios')} style={{cursor: 'pointer'}}>Usuarios</li>}
              {user?.role !== 'Admin' && (
                <>
                  <li>Reglas</li>
                  <li className="active" onClick={() => navigate('/intake')} style={{cursor: 'pointer'}}>Ingresar◄</li>
                  <li onClick={() => navigate('/pendientes')} style={{cursor: 'pointer'}}>Pendientes</li>
                  <li>Historial</li>
                </>
              )}
            </ul>
          </nav>
        </aside>
        <main className="grm-app__content">
          {children}
        </main>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <SessionManager>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          <Route path="/" element={<Navigate to="/login" replace />} />
          
          <Route element={<ProtectedRoute allowedRoles={['Operario']} />}>
            <Route path="/operario/seleccion-cliente" element={<SeleccionClientePage />} />
          </Route>

          <Route element={<ProtectedRoute allowedRoles={['Admin']} />}>
            <Route path="/admin/gestion-usuarios" element={<AppLayout><GestionUsuariosPage /></AppLayout>} />
          </Route>

          <Route element={<ProtectedRoute allowedRoles={['Operario', 'Cliente']} />}>
            <Route path="/intake" element={<AppLayout><IntakeDashboard /></AppLayout>} />
            <Route path="/pendientes" element={<AppLayout><PendientesPage /></AppLayout>} />
          </Route>
          
        </Routes>
      </SessionManager>
    </Router>
  );
}

export default App;
