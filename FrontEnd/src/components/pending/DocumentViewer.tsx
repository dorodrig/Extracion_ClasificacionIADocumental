import React from 'react';
import { usePendientesStore } from '../../store/pendientesStore';
import { PDFViewer } from '../pdf-viewer/PDFViewer';
import { ExtractedDataPanel } from './ExtractedDataPanel';

export const DocumentViewer: React.FC = () => {
  const { documentoSeleccionado, documentos, cerrarVisor, navegarVisor } = usePendientesStore();

  if (!documentoSeleccionado) return null;

  const currentIndex = documentos.findIndex(d => d.id === documentoSeleccionado.id);
  const total = documentos.length;
  
  // Encontrar el nombre del archivo original
  const docOriginal = documentos.find(d => d.id === documentoSeleccionado.id);
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
          📄 {fileName} {docOriginal && `| Cliente: ${docOriginal.cliente}`}
        </div>
        
        <div className="nav-buttons">
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
        <PDFViewer url={documentoSeleccionado.pdfUrl} />
        <ExtractedDataPanel />
      </div>
    </div>
  );
};
