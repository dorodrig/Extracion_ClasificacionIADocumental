/**
 * App — Punto de entrada de la aplicación GRM Frontend
 * Gobernanza §4.2 — React Router + React Query Provider
 */
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { Layout } from './components/common/Layout';
import { RulesPage } from './pages/RulesPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      refetchOnWindowFocus: false,
      staleTime: 30000,
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<RulesPage />} />
            <Route path="/reglas" element={<RulesPage />} />
          </Routes>
        </Layout>
      </BrowserRouter>

      {/* Toast Notifications — Gobernanza §6.2 */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#161b22',
            color: '#e6edf3',
            border: '1px solid #30363d',
            borderRadius: '8px',
            fontSize: '14px',
          },
          success: {
            iconTheme: {
              primary: '#3fb950',
              secondary: '#0d1117',
            },
          },
          error: {
            iconTheme: {
              primary: '#f85149',
              secondary: '#0d1117',
            },
          },
        }}
      />
    </QueryClientProvider>
  );
};
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { IntakeDashboard } from '@/components/intake/IntakeDashboard';
import { PendientesPage } from '@/pages/PendientesPage';

function App() {
  return (
    <Router>
      <div className="grm-app">
        <header className="grm-app__header">
          <div className="grm-app__logo">GRM</div>
          <div className="grm-app__user-info">
            Operario: Juan Pérez | Cliente: BANCORP | <a href="#">[Cambiar]</a> <a href="#">[Salir]</a>
          </div>
        </header>
        <div className="grm-app__body">
          <aside className="grm-app__sidebar">
            <nav>
              <ul>
                <li>Inicio</li>
                <li>Reglas</li>
                <li className="active">Ingresar◄</li>
                <li>Pendientes</li>
                <li>Historial</li>
              </ul>
            </nav>
          </aside>
          <main className="grm-app__content">
            <Routes>
              <Route path="/" element={<Navigate to="/intake" replace />} />
              <Route path="/intake" element={<IntakeDashboard />} />
              <Route path="/pendientes" element={<PendientesPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
