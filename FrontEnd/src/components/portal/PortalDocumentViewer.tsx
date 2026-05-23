/**
 * PortalDocumentViewer — Document viewer with metadata panel
 * HU-07 — Portal de Consulta para Clientes (CA-12)
 */
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download, FileText, FolderOpen } from 'lucide-react';
import { useClienteDocumentoDetail } from '@/hooks/useClienteDocumentoDetail';
import { clienteService } from '@/services/clienteService';
import { PDFViewer } from '@/components/pdf-viewer/PDFViewer';

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

const isPdfFile = (name: string | undefined): boolean => {
  if (!name) return false;
  return name.toLowerCase().endsWith('.pdf');
};

const buildMiniTree = (filename: string): string[] => {
  const parts = filename.split(/[/\\]/);
  return parts;
};

const formatFieldLabel = (key: string): string => {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
};

/* ── Component ───────────────────────────────────────────── */

export const PortalDocumentViewer: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data, isLoading, error } = useClienteDocumentoDetail(Number(id));

  // Handle 403 → redirect to access-denied
  useEffect(() => {
    if (error) {
      const status = (error as { response?: { status?: number } })?.response?.status;
      if (status === 403) {
        navigate('/cliente/acceso-denegado', { replace: true });
      }
    }
  }, [error, navigate]);

  const fileUrl = id ? clienteService.getDocumentoArchivoUrl(Number(id)) : '';
  const isPdf = isPdfFile(data?.nombre_archivo);
  const miniTreeParts = data?.nombre_archivo
    ? buildMiniTree(data.nombre_archivo)
    : [];

  const handleDownload = () => {
    if (id) {
      clienteService.descargarDocumento(Number(id));
    }
  };

  if (isLoading) {
    return (
      <div className="grm-portal-viewer">
        <div className="grm-portal-viewer__toolbar">
          <div className="grm-portal-viewer__skeleton-bar" />
        </div>
        <div className="grm-portal-viewer__content">
          <div className="grm-portal-viewer__doc-panel">
            <div className="grm-portal-viewer__skeleton-doc" />
          </div>
          <div className="grm-portal-viewer__info-panel">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="grm-portal-viewer__skeleton-field" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="grm-portal-viewer">
      {/* Toolbar */}
      <div className="grm-portal-viewer__toolbar">
        <button
          className="grm-portal-viewer__back"
          onClick={() => navigate('/cliente/documentos')}
        >
          <ArrowLeft size={16} /> Volver a Mis Documentos
        </button>
        <span className="grm-portal-viewer__filename">
          <FileText size={16} /> {data?.nombre_archivo}
        </span>
        <button
          className="grm-portal-viewer__download"
          onClick={handleDownload}
        >
          <Download size={16} /> Descargar
        </button>
      </div>

      {/* Content */}
      <div className="grm-portal-viewer__content">
        {/* Left: Document */}
        <div className="grm-portal-viewer__doc-panel">
          {isPdf ? (
            <PDFViewer url={fileUrl} />
          ) : (
            <img
              src={fileUrl}
              alt={data?.nombre_archivo}
              className="grm-portal-viewer__image"
            />
          )}
        </div>

        {/* Right: Metadata */}
        <div className="grm-portal-viewer__info-panel">
          <h3 className="grm-portal-viewer__section-title">
            Información del Documento
          </h3>

          <div className="grm-portal-viewer__field">
            <span className="grm-portal-viewer__field-label">Tipo</span>
            <span className="grm-portal-viewer__field-value">
              {data?.tipo_documento}
            </span>
          </div>

          {/* Dynamic fields from campos_extraidos */}
          {data?.campos_extraidos &&
            Object.entries(data.campos_extraidos).map(([key, value]) => (
              <div key={key} className="grm-portal-viewer__field">
                <span className="grm-portal-viewer__field-label">
                  {formatFieldLabel(key)}
                </span>
                <span className="grm-portal-viewer__field-value">
                  {String(value ?? '—')}
                </span>
              </div>
            ))}

          <div className="grm-portal-viewer__field">
            <span className="grm-portal-viewer__field-label">Fecha</span>
            <span className="grm-portal-viewer__field-value">
              {formatDate(data?.fecha_carga)}
            </span>
          </div>

          <div className="grm-portal-viewer__field">
            <span className="grm-portal-viewer__field-label">Estado</span>
            <span className="grm-portal-viewer__field-value">
              {data?.estado}
            </span>
          </div>

          {data?.confianza_promedio != null && (
            <div className="grm-portal-viewer__field">
              <span className="grm-portal-viewer__field-label">
                Confianza Promedio
              </span>
              <span className="grm-portal-viewer__field-value">
                {(data.confianza_promedio * 100).toFixed(1)}%
              </span>
            </div>
          )}

          {/* CA-12: Mini tree / location */}
          <h3 className="grm-portal-viewer__section-title">Ubicación</h3>
          <div className="grm-portal-viewer__mini-tree">
            {miniTreeParts.map((part, idx) => (
              <span key={idx} className="grm-portal-viewer__mini-tree-item">
                {idx < miniTreeParts.length - 1 ? (
                  <>
                    <FolderOpen size={14} className="grm-portal-viewer__mini-tree-icon" />
                    <span>{part}</span>
                    <span className="grm-portal-viewer__mini-tree-arrow">→</span>
                  </>
                ) : (
                  <>
                    <FileText size={14} className="grm-portal-viewer__mini-tree-icon" />
                    <span>{part}</span>
                  </>
                )}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
