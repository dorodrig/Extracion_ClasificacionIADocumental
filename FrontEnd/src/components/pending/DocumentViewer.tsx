import React, { useState } from 'react';
import { usePendientesStore } from '../../store/pendientesStore';
import { PDFViewer } from '../pdf-viewer/PDFViewer';
import { ExtractedDataPanel } from './ExtractedDataPanel';
import { DocumentTimeline } from '../auditoria/DocumentTimeline';

export const DocumentViewer: React.FC = () => {
  const { documentoSeleccionado, documentos, cerrarVisor, navegarVisor } = usePendientesStore();
  const [showTimeline, setShowTimeline] = useState(false);

  if (!documentoSeleccionado) return null;

  const docsArray = Array.isArray(documentos) ? documentos : (documentos as any)?.data || [];

  const currentIndex = docsArray.findIndex((d: any) => d?.id === documentoSeleccionado?.id);
  const total = docsArray.length;
  
  // Encontrar el nombre del archivo original
  const docOriginal = docsArray.find((d: any) => d?.id === documentoSeleccionado?.id);
  const fileName = docOriginal ? docOriginal.filename : 'Documento';

  return (
    <div className="visor-layout">
      <div className="visor-header">
        <a 
          href="#" 
          className="volver-link" 
          onClick={(e) => { e.preventDefault(); cerrarVisor(); }}
        >
          ← Volver a Pendientes
        </a>
        
        <div className="doc-title">
          📄 {fileName} {docOriginal && `| Cliente: ${docOriginal.cliente} | Lote: `}
          {docOriginal && (
            <a href={`/lotes/${docOriginal.lote}`} style={{ color: '#2f81f7', textDecoration: 'none' }}>
              {docOriginal.lote}
            </a>
          )}
        </div>
        
        <div className="nav-buttons">
          <button 
            className="history-btn"
            onClick={() => setShowTimeline(true)}
            style={{ marginRight: '16px', padding: '4px 8px', cursor: 'pointer' }}
          >
            🕒 Historial
          </button>
          <button 
            onClick={() => navegarVisor('anterior')}
            disabled={currentIndex <= 0}
          >
            ◄ Anterior
          </button>
          <span>Pendiente {currentIndex + 1} de {total}</span>
          <button 
            onClick={() => navegarVisor('siguiente')}
            disabled={currentIndex === -1 || currentIndex >= total - 1}
          >
            Siguiente ►
          </button>
        </div>
      </div>

      <div className="visor-content">
        <PDFViewer url={(documentoSeleccionado as any).data?.pdfUrl || documentoSeleccionado.pdfUrl || ''} />
        <ExtractedDataPanel />
      </div>

      {showTimeline && (
        <DocumentTimeline 
          documentId={documentoSeleccionado.id} 
          onClose={() => setShowTimeline(false)} 
        />
      )}
    </div>
  );
};
