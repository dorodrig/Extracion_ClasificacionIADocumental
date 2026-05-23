/**
 * PortalDocumentList — Filterable, paginated document list
 * HU-07 — Portal de Consulta para Clientes
 */
import React, { useState, useMemo, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, Eye, FileText } from 'lucide-react';
import { useClienteDocumentos } from '@/hooks/useClienteDocumentos';

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

/* ── Component ───────────────────────────────────────────── */

export const PortalDocumentList: React.FC = () => {
  const navigate = useNavigate();

  // Filter state
  const [page, setPage] = useState(1);
  const [size] = useState(10);
  const [busqueda, setBusqueda] = useState('');
  const [tipoDocumento, setTipoDocumento] = useState('');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');

  const params = useMemo(
    () => ({
      page,
      size,
      busqueda: busqueda || undefined,
      tipo_documento: tipoDocumento || undefined,
      fecha_inicio: fechaInicio || undefined,
      fecha_fin: fechaFin || undefined,
    }),
    [page, size, busqueda, tipoDocumento, fechaInicio, fechaFin],
  );

  const { data, isLoading } = useClienteDocumentos(params);

  const totalPages = data ? Math.ceil(data.total / size) : 1;

  const clearFilters = useCallback(() => {
    setBusqueda('');
    setTipoDocumento('');
    setFechaInicio('');
    setFechaFin('');
    setPage(1);
  }, []);

  const pageNumbers = useMemo(() => {
    const pages: number[] = [];
    for (let i = 1; i <= totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }, [totalPages]);

  return (
    <div className="grm-portal-document-list">
      <h1 className="grm-portal-document-list__title">Mis Documentos</h1>

      {/* Filters */}
      <div className="grm-portal-filters">
        <div className="grm-portal-filters__search">
          <Search size={16} />
          <input
            type="text"
            placeholder="Buscar por CC, nombre, archivo..."
            value={busqueda}
            onChange={(e) => {
              setBusqueda(e.target.value);
              setPage(1);
            }}
          />
        </div>
        <select
          className="grm-portal-filters__select"
          value={tipoDocumento}
          onChange={(e) => {
            setTipoDocumento(e.target.value);
            setPage(1);
          }}
        >
          <option value="">Todos los tipos</option>
          <option value="Pagaré">Pagaré</option>
          <option value="Cédula">Cédula</option>
          <option value="Endoso">Endoso</option>
          <option value="Otro">Otro</option>
        </select>
        <input
          type="date"
          className="grm-portal-filters__date"
          value={fechaInicio}
          onChange={(e) => {
            setFechaInicio(e.target.value);
            setPage(1);
          }}
        />
        <input
          type="date"
          className="grm-portal-filters__date"
          value={fechaFin}
          onChange={(e) => {
            setFechaFin(e.target.value);
            setPage(1);
          }}
        />
        <button className="grm-portal-filters__clear" onClick={clearFilters}>
          <X size={14} /> Limpiar
        </button>
      </div>

      {/* Table */}
      {isLoading ? (
        <div className="grm-portal-table__skeleton">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="grm-portal-table__skeleton-row" />
          ))}
        </div>
      ) : (
        <table className="grm-portal-table">
          <thead>
            <tr>
              <th>Nombre de archivo</th>
              <th>Tipo</th>
              <th>Cédula</th>
              <th>Fecha</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            {data?.items.map((doc) => (
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
                <td>--</td>
                <td>{formatDate(doc.fecha_carga)}</td>
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
            {data?.items.length === 0 && (
              <tr>
                <td colSpan={5} className="grm-portal-table__empty">
                  No se encontraron documentos.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}

      {/* Pagination */}
      {data && data.total > 0 && (
        <div className="grm-portal-pagination">
          <span className="grm-portal-pagination__info">
            Mostrando {data.items.length} de {data.total}
          </span>
          <div className="grm-portal-pagination__buttons">
            <button
              className="grm-portal-pagination__btn"
              disabled={page <= 1}
              onClick={() => setPage((p) => p - 1)}
            >
              ‹
            </button>
            {pageNumbers.map((n) => (
              <button
                key={n}
                className={`grm-portal-pagination__btn${n === page ? ' grm-portal-pagination__btn--active' : ''}`}
                onClick={() => setPage(n)}
              >
                {n}
              </button>
            ))}
            <button
              className="grm-portal-pagination__btn"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => p + 1)}
            >
              ›
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
