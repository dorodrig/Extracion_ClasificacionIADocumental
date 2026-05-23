import React from 'react';
import { useBatchStore } from '@/store/batchStore';
import styles from './DocumentList.module.scss';
import dashboardStyles from './IntakeDashboard.module.scss';
import { Trash2, CheckCircle2, AlertTriangle } from 'lucide-react';
import { IngestionProgress } from './IngestionProgress';
import { OmittedFilesAlert } from './OmittedFilesAlert';
import { batchService } from '@/services/batchService';
import toast from 'react-hot-toast';

interface DocumentListProps {
  mode: 'scanner' | 'carpeta';
}

export const DocumentList: React.FC<DocumentListProps> = ({ mode }) => {
  const { 
    documentsList, 
    removeDocument, 
    toggleDocumentSelection, 
    toggleAllSelection,
    activeBatchId,
    batchStatus,
    setBatchStatus,
    omittedFilesBackend,
    setOmittedFilesBackend
  } = useBatchStore();

  const selectedCount = documentsList.filter(d => d.selected).length;
  const totalPages = documentsList.reduce((acc, doc) => acc + (doc.selected ? doc.pages : 0), 0);
  const totalSize = documentsList.reduce((acc, doc) => acc + (doc.selected ? doc.sizeMB : 0), 0);
  const allSelected = documentsList.length > 0 && selectedCount === documentsList.length;

  const [isPreparing, setIsPreparing] = React.useState(false);

  const handleConfirmAndSend = async () => {
    if (!activeBatchId) return;
    
    setIsPreparing(true);
    setOmittedFilesBackend([]);

    const documentosPayload = documentsList
      .filter(d => d.selected)
      .map(d => ({
        nombre_archivo: d.name,
        extension: d.extension,
        ruta_original: d.name, // Mock path
        total_paginas: d.pages
      }));

    try {
      const response = await batchService.prepareBatch(activeBatchId, { documentos: documentosPayload });
      
      setIsPreparing(false);
      
      if (response.success && response.data) {
        setBatchStatus('processing');
        if (response.data.archivos_omitidos && response.data.archivos_omitidos.length > 0) {
          setOmittedFilesBackend(response.data.archivos_omitidos);
        }
      } else {
        setBatchStatus('error');
        toast.error(response.error || 'Error al preparar el lote de procesamiento.');
      }
    } catch (e: any) {
      setIsPreparing(false);
      setBatchStatus('error');
      toast.error('Error al preparar el lote de procesamiento.');
    }
  };

  const handleComplete = () => {
    // Redirigir al panel de monitoreo OCR
    window.location.href = '/monitoreo-ocr';
  };

  if (batchStatus === 'processing') {
    return <IngestionProgress batchId={activeBatchId!} onComplete={handleComplete} />;
  }

  return (
    <div className={styles['grm-document-list']}>
      <OmittedFilesAlert omittedFiles={omittedFilesBackend} count={omittedFilesBackend.length} />
      <div className={styles['grm-document-list__table-container']}>
        <table>
          <thead>
            <tr>
              <th style={{ width: "40px" }}>#</th>
              <th>Nombre {mode === 'carpeta' && 'archivo'}</th>
              {mode === 'carpeta' && <th style={{ width: "80px" }}>Ext.</th>}
              <th style={{ width: "80px" }}>Páginas</th>
              <th style={{ width: "100px" }}>Tamaño</th>
              {mode === 'scanner' && <th style={{ width: "120px" }}>Estado</th>}
              <th style={{ width: "80px" }} className={styles['text-center']}>
                {mode === 'carpeta' ? (
                  <input 
                    type="checkbox" 
                    checked={allSelected}
                    onChange={(e) => toggleAllSelection(e.target.checked)}
                  />
                ) : null}
              </th>
            </tr>
          </thead>
          <tbody>
            {documentsList.map((doc, index) => (
              <tr key={doc.id}>
                <td>{index + 1}</td>
                <td>{doc.name}</td>
                {mode === 'carpeta' && <td>{doc.extension}</td>}
                <td>{doc.pages}</td>
                <td>{doc.sizeMB} MB</td>
                {mode === 'scanner' && (
                  <td>
                    <span className={`${styles['status']} ${styles[doc.status.toLowerCase()] || ''}`}>
                      {doc.status === 'Listo' ? <CheckCircle2 size={16}/> : <AlertTriangle size={16}/>}
                      {doc.status}
                    </span>
                  </td>
                )}
                <td className={styles['text-center']}>
                  {mode === 'carpeta' ? (
                    <input 
                      type="checkbox" 
                      checked={doc.selected}
                      onChange={() => toggleDocumentSelection(doc.id)}
                    />
                  ) : (
                    <button 
                      className={styles['delete-btn']}
                      onClick={() => removeDocument(doc.id)}
                    >
                      <Trash2 size={16} />
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        <div className={styles['grm-document-list__footer']}>
          {mode === 'scanner' ? (
            <span>Total: {documentsList.length} documentos | {totalPages} páginas | {totalSize.toFixed(1)} MB</span>
          ) : (
            <span>Seleccionados: {selectedCount} | Total páginas: {totalPages} | Tamaño: {totalSize.toFixed(1)} MB</span>
          )}
        </div>
      </div>
      
      <div className={styles['grm-document-list__actions']}>
        <button className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--outline']}`}>
          Cancelar
        </button>
        <button 
          className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--primary']} ${styles['btn-confirm']}`}
          disabled={selectedCount === 0 || !activeBatchId || isPreparing}
          onClick={handleConfirmAndSend}
        >
          {isPreparing ? 'Preparando...' : '✓ Confirmar y Enviar'}
        </button>
      </div>
    </div>
  );
};
