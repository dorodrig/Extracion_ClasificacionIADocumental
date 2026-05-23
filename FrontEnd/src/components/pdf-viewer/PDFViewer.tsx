import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

// Configurar el worker de PDF.js
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

interface PDFViewerProps {
  url: string;
}

export const PDFViewer: React.FC<PDFViewerProps> = ({ url }) => {
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState(1.0);
  const [rotation, setRotation] = useState(0);

  function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
    setNumPages(numPages);
    setPageNumber(1);
  }

  const changePage = (offset: number) => {
    setPageNumber(prevPageNumber => prevPageNumber + offset);
  };

  const previousPage = () => changePage(-1);
  const nextPage = () => changePage(1);
  const zoomIn = () => setScale(prev => Math.min(prev + 0.2, 3.0));
  const zoomOut = () => setScale(prev => Math.max(prev - 0.2, 0.5));
  const resetZoom = () => setScale(1.0);
  const rotate = () => setRotation(prev => (prev + 90) % 360);

  return (
    <div className="pdf-viewer-panel">
      <div className="pdf-toolbar">
        <div className="toolbar-group">
          <button type="button" disabled={pageNumber <= 1} onClick={previousPage}>
            ← Pág anterior
          </button>
          <span>
            Página {pageNumber} de {numPages || '--'}
          </span>
          <button type="button" disabled={pageNumber >= (numPages || 1)} onClick={nextPage}>
            Pág siguiente →
          </button>
        </div>
        
        <div className="toolbar-group">
          <button type="button" onClick={zoomOut}>🔍-</button>
          <button type="button" onClick={resetZoom}>{Math.round(scale * 100)}%</button>
          <button type="button" onClick={zoomIn}>🔍+</button>
          <span style={{ borderLeft: '1px solid #30363d', height: '24px', margin: '0 8px' }}></span>
          <button type="button" onClick={rotate}>↺ Rotar</button>
        </div>
      </div>
      
      <div className="pdf-container">
        <Document
          file={url}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={<div style={{ color: '#8b949e' }}>Cargando documento...</div>}
          error={<div style={{ color: '#f85149' }}>Error al cargar el PDF. Puede que sea una imagen o URL inválida.</div>}
        >
          <Page 
            pageNumber={pageNumber} 
            scale={scale} 
            rotate={rotation}
            renderTextLayer={false}
            renderAnnotationLayer={false}
          />
        </Document>
      </div>
    </div>
  );
};
