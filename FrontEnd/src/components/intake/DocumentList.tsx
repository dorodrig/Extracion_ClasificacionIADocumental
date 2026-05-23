import React from 'react';
import { useBatchStore } from '@/store/batchStore';
import styles from './DocumentList.module.scss';
import dashboardStyles from './IntakeDashboard.module.scss';
import { Trash2, CheckCircle2, AlertTriangle } from 'lucide-react';

interface DocumentListProps {
  mode: 'scanner' | 'carpeta';
}

export const DocumentList: React.FC<DocumentListProps> = ({ mode }) => {
  const { 
    documentsList, 
    removeDocument, 
    toggleDocumentSelection, 
    toggleAllSelection,
    activeBatchId
  } = useBatchStore();

  const selectedCount = documentsList.filter(d => d.selected).length;
  const totalPages = documentsList.reduce((acc, doc) => acc + (doc.selected ? doc.pages : 0), 0);
  const totalSize = documentsList.reduce((acc, doc) => acc + (doc.selected ? doc.sizeMB : 0), 0);
  const allSelected = documentsList.length > 0 && selectedCount === documentsList.length;

  return (
    <div className={styles['grm-document-list']}>
      <div className={styles['grm-document-list__table-container']}>
        <table>
          <thead>
            <tr>
              <th width="40">#</th>
              <th>Nombre {mode === 'carpeta' && 'archivo'}</th>
              {mode === 'carpeta' && <th width="80">Ext.</th>}
              <th width="80">Páginas</th>
              <th width="100">Tamaño</th>
              {mode === 'scanner' && <th width="120">Estado</th>}
              <th width="80" style={{ textAlign: 'center' }}>
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
                <td style={{ textAlign: 'center' }}>
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
          className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--primary']}`}
          style={{ backgroundColor: '#238636', borderColor: '#238636' }}
          disabled={selectedCount === 0}
          onClick={() => alert(`Enviando batch ${activeBatchId} al pipeline...`)}
        >
          ✓ Confirmar y Enviar
        </button>
      </div>
    </div>
  );
};
