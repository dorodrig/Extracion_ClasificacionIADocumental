import React, { useState, useRef } from 'react';
import { useBatchStore } from '@/store/batchStore';
import { batchService } from '@/services/batchService';
import { DocumentList } from './DocumentList';
import dashboardStyles from './IntakeDashboard.module.scss';
import styles from './FolderModule.module.scss';
import { Folder, AlertTriangle } from 'lucide-react';

export const FolderModule: React.FC = () => {
  const { addDocuments, documentsList, setActiveBatch } = useBatchStore();
  const [folderPath, setFolderPath] = useState<string | null>(null);
  const [omittedFiles, setOmittedFiles] = useState<string[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const SUPPORTED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'];

  const handleDirectorySelection = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    // Get folder path from first file
    const path = (files[0] as any).webkitRelativePath.split('/')[0] || 'Carpeta seleccionada';
    setFolderPath(`C:\\Documentos\\BANCORP\\${path}\\`); // Mocking local C: path for UX
    
    const validDocs = [];
    const invalidDocs = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const ext = file.name.split('.').pop()?.toLowerCase() || '';
      
      if (SUPPORTED_EXTENSIONS.includes(ext)) {
        validDocs.push({
          id: `file_${Date.now()}_${i}`,
          file: file,
          name: file.name,
          extension: ext.toUpperCase(),
          pages: ext === 'pdf' ? Math.floor(Math.random() * 10) + 1 : 1, // PDF pages require parsing, mock for now
          sizeMB: parseFloat((file.size / (1024 * 1024)).toFixed(2)),
          status: 'Listo' as const,
          selected: true
        });
      } else {
        invalidDocs.push(file.name);
      }
    }

    setOmittedFiles(invalidDocs);
    addDocuments(validDocs);

    // Create batch in backend
    try {
      const res = await batchService.createBatch('carpeta');
      if (res.data) setActiveBatch(res.data.batch_id);
    } catch (e) {
      console.error(e);
    }
    
    // Reset input
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className={styles['grm-folder-module']}>
      {!folderPath ? (
        <>
          <h3>SELECCIONAR CARPETA DE DOCUMENTOS</h3>
          <div className={styles['grm-folder-module__selection-area']}>
            <Folder size={64} className={styles['icon']} />
            <p>Haz clic para seleccionar la carpeta que contiene los documentos a procesar.</p>
            <p className={styles['grm-folder-module__supported-formats']}>Formatos soportados: PDF, JPG, PNG, TIFF</p>
            
            <button className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--primary']}`}>
              📁 Seleccionar Carpeta
            </button>
            
            {/* The webkitdirectory attribute allows folder selection */}
            <input 
              type="file" 
              ref={fileInputRef}
              onChange={handleDirectorySelection} 
              // @ts-expect-error webkitdirectory is non-standard but works in most modern browsers
              webkitdirectory="true" 
              directory="true" 
              multiple 
            />
          </div>
        </>
      ) : (
        <>
          <div className={styles['grm-folder-module__header']}>
            <h3><Folder size={20} /> {folderPath}</h3>
            <button 
              className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--outline']}`}
              onClick={() => {
                setFolderPath(null);
                setOmittedFiles([]);
                useBatchStore.getState().resetBatch();
              }}
            >
              Cambiar Carpeta
            </button>
          </div>
          
          <p>Archivos encontrados: {documentsList.length} compatibles | {omittedFiles.length} omitidos</p>
          
          {omittedFiles.length > 0 && (
            <div className={styles['grm-folder-module__warning']}>
              <AlertTriangle size={16} /> 
              Se omitieron {omittedFiles.length} archivos no compatibles: {omittedFiles.slice(0, 3).join(', ')}{omittedFiles.length > 3 ? '...' : ''}
            </div>
          )}
          
          {documentsList.length > 0 && <DocumentList mode="carpeta" />}
        </>
      )}
    </div>
  );
};
