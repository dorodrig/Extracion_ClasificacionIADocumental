/**
 * PortalDashboard — Client portal dashboard with metrics and recent docs
 * HU-07 — Portal de Consulta para Clientes (CA-02, CA-09)
 */
import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { FileText, Calendar, Eye, CreditCard, Shield } from 'lucide-react';
import { useClienteDashboard } from '@/hooks/useClienteDashboard';
import { useClienteDocumentos } from '@/hooks/useClienteDocumentos';
import type { DashboardMetrics } from '@/types/cliente';

/* ── helpers ─────────────────────────────────────────────── */

const formatDate = (raw: string | null | undefined): string => {
  if (!raw) return '—';
  try {
    return new Intl.DateTimeFormat('es-CO', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(new Date(raw));
  } catch {
    return raw;
  }
};

/* ── MetricCard (local) ──────────────────────────────────── */

interface MetricCardProps {
  icon: React.FC<{ size?: number; className?: string }>;
  value: string | number | undefined;
  label: string;
  color: 'blue' | 'indigo' | 'green' | 'amber';
  isLoading: boolean;
}

const MetricCard: React.FC<MetricCardProps> = ({
  icon: Icon,
  value,
  label,
  color,
  isLoading,
}) => (
  <div className={`grm-portal-metric grm-portal-metric--${color}`}>
    <div className="grm-portal-metric__icon-wrap">
      <Icon size={22} className="grm-portal-metric__icon" />
    </div>
    {isLoading ? (
      <div className="grm-portal-metric__skeleton" />
    ) : (
      <span className="grm-portal-metric__value">{value ?? 0}</span>
    )}
    <span className="grm-portal-metric__label">{label}</span>
  </div>
);

/* ── PortalDashboard ─────────────────────────────────────── */

export const PortalDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useClienteDashboard();
  const { data: recentDocs, isLoading: recentLoading } =
    useClienteDocumentos({ page: 1, size: 5 });

  return (
    <div className="grm-portal-dashboard">
      <h1 className="grm-portal-dashboard__title">Dashboard</h1>

      {/* CA-09: Pending banner */}
      {data && data.pendientes_revision > 0 && (
        <div className="grm-portal-banner-pending">
          <span className="grm-portal-banner-pending__icon">⏳</span>
          <div className="grm-portal-banner-pending__body">
            <strong>En revisión por el equipo de digitalización</strong>
            <p>
              {data.pendientes_revision} documento(s) están siendo revisados
              actualmente.
            </p>
          </div>
        </div>
      )}

      {/* CA-02: Metric cards */}
      <div className="grm-portal-metrics">
        <MetricCard
          icon={FileText}
          value={data?.total_documentos}
          label="Total Documentos"
          color="blue"
          isLoading={isLoading}
        />
        <MetricCard
          icon={CreditCard}
          value={data?.tipos_conteo?.['Pagaré'] ?? 0}
          label="Pagarés"
          color="indigo"
          isLoading={isLoading}
        />
        <MetricCard
          icon={Shield}
          value={data?.tipos_conteo?.['Cédula'] ?? 0}
          label="Cédulas"
          color="green"
          isLoading={isLoading}
        />
        <MetricCard
          icon={Calendar}
          value={formatDate(data?.ultimo_procesado)}
          label="Último Procesamiento"
          color="amber"
          isLoading={isLoading}
        />
      </div>

      {/* Recent docs table */}
      <div className="grm-portal-recent-docs">
        <div className="grm-portal-recent-docs__header">
          <h2>Últimos documentos procesados</h2>
          <NavLink
            to="/cliente/documentos"
            className="grm-portal-recent-docs__link"
          >
            Ver todos →
          </NavLink>
        </div>

        {recentLoading ? (
          <div className="grm-portal-recent-docs__skeleton">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="grm-portal-recent-docs__skeleton-row" />
            ))}
          </div>
        ) : (
          <table className="grm-portal-table">
            <thead>
              <tr>
                <th>Nombre de archivo</th>
                <th>Tipo</th>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Acción</th>
              </tr>
            </thead>
            <tbody>
              {recentDocs?.items.map((doc) => (
                <tr key={doc.id} className="grm-portal-table__row">
                  <td>
                    <span className="grm-portal-table__file-name">
                      <FileText size={14} />
                      {doc.nombre_archivo}
                    </span>
                  </td>
                  <td>
                    <span
                      className={`grm-portal-badge grm-portal-badge--${getBadgeClass(doc.tipo_documento)}`}
                    >
                      {doc.tipo_documento}
                    </span>
                  </td>
                  <td>{formatDate(doc.fecha_carga)}</td>
                  <td>{doc.estado}</td>
                  <td>
                    <button
                      className="grm-portal-table__btn-ver"
                      onClick={() => navigate(`/cliente/visor/${doc.id}`)}
                    >
                      <Eye size={14} /> Ver
                    </button>
                  </td>
                </tr>
              ))}
              {recentDocs?.items.length === 0 && (
                <tr>
                  <td colSpan={5} className="grm-portal-table__empty">
                    No hay documentos procesados aún.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

/* ── badge helper ────────────────────────────────────────── */

function getBadgeClass(tipo: string): string {
  switch (tipo) {
    case 'Pagaré':
      return 'pagare';
    case 'Cédula':
      return 'cedula';
    case 'Endoso':
      return 'endoso';
    default:
      return 'otro';
  }
}
