import React from 'react';
import { useOcrProgress } from '../../hooks/useOcrProgress';
import styles from './OcrProgressIndicator.module.scss';

interface OcrProgressIndicatorProps {
  batchId?: string;
}

export const OcrProgressIndicator: React.FC<OcrProgressIndicatorProps> = ({ batchId }) => {
  const { data, isLoading, isError } = useOcrProgress(batchId);

  if (!batchId) {
    return null;
  }

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <span className={styles.title}>Estado del Procesamiento OCR</span>
          <span className={`${styles.status} ${styles.pendiente}`}>Cargando...</span>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <span className={styles.title}>Estado del Procesamiento OCR</span>
          <span className={`${styles.status} ${styles.error}`}>Error de conexión</span>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const percentage = data.total_pages > 0 ? (data.processed_pages / data.total_pages) * 100 : 0;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <span className={styles.title}>Estado del Procesamiento OCR</span>
        <span className={`${styles.status} ${styles[data.status]}`}>
          {data.status.replace('_', ' ')}
        </span>
      </div>

      <div className={styles.progressContainer}>
        <div 
          className={styles.progressBar} 
          style={{ width: `${Math.min(Math.max(percentage, 0), 100)}%` }} 
        />
      </div>

      <div className={styles.stats}>
        <span>
          Páginas procesadas: {data.processed_pages} / {data.total_pages}
        </span>
        {data.errors > 0 && (
          <span className={styles.errorCount}>
            Documentos con error: {data.errors}
          </span>
        )}
      </div>
    </div>
  );
};
