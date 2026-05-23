/**
 * App — Punto de entrada de la aplicación GRM Frontend
 * Gobernanza §4.2 — React Router + React Query Provider
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { Layout } from './components/common/Layout';
import { RulesPage } from './pages/RulesPage';
import { IntakeDashboard } from '@/components/intake/IntakeDashboard';
import { PendientesPage } from '@/pages/PendientesPage';
import { PortalLogin } from '@/components/portal/PortalLogin';
import { ClientePortalPage } from '@/pages/ClientePortalPage';
import { AccessDeniedPage } from '@/components/portal/AccessDeniedPage';

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
        <Routes>
          {/* Portal Cliente routes — outside operario Layout (light theme) */}
          <Route path="/cliente/login" element={<PortalLogin />} />
          <Route path="/cliente/acceso-denegado" element={<AccessDeniedPage />} />
          <Route path="/cliente/*" element={<ClientePortalPage />} />

          {/* Operario routes — inside dark-theme Layout */}
          <Route
            path="/*"
            element={
              <Layout>
                <Routes>
                  <Route path="/" element={<Navigate to="/intake" replace />} />
                  <Route path="/reglas" element={<RulesPage />} />
                  <Route path="/intake" element={<IntakeDashboard />} />
                  <Route path="/pendientes" element={<PendientesPage />} />
                </Routes>
              </Layout>
            }
          />
        </Routes>
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

export default App;
