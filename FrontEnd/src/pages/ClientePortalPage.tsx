/**
 * ClientePortalPage — Page wrapper with PortalLayout and nested routes
 * HU-07 — Portal de Consulta para Clientes
 */
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { PortalLayout } from '@/components/portal/PortalLayout';
import { PortalDashboard } from '@/components/portal/PortalDashboard';
import { PortalDocumentList } from '@/components/portal/PortalDocumentList';
import { PortalExplorer } from '@/components/portal/PortalExplorer';
import { PortalDocumentViewer } from '@/components/portal/PortalDocumentViewer';

export const ClientePortalPage: React.FC = () => {
  return (
    <PortalLayout>
      <Routes>
        <Route path="dashboard" element={<PortalDashboard />} />
        <Route path="documentos" element={<PortalDocumentList />} />
        <Route path="explorador" element={<PortalExplorer />} />
        <Route path="visor/:id" element={<PortalDocumentViewer />} />
        <Route path="*" element={<Navigate to="dashboard" replace />} />
      </Routes>
    </PortalLayout>
  );
};
