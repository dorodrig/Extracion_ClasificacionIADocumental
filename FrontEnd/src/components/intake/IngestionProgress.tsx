import React, { useEffect, useState } from 'react';
import { useBatchStore } from '@/store/batchStore';
import { batchService } from '@/services/batchService';
import styles from './IngestionProgress.module.scss';
import { Loader2 } from 'lucide-react';

interface IngestionProgressProps {
  batchId: string;
  onComplete: () => void;
}

export const IngestionProgress: React.FC<IngestionProgressProps> = ({ batchId, onComplete }) => {
  const { batchProgress, setBatchProgress, setBatchStatus } = useBatchStore();
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    let timeoutId: NodeJS.Timeout;
    let isPolling = true;

    const checkStatus = async () => {
      if (!isPolling) return;
      try {
        const response = await batchService.getBatchStatus(batchId);
        if (response.success && response.data) {
          const { estado, documentos_preparados, total_documentos } = response.data;
          
          setBatchProgress({
            preparados: documentos_preparados,
            total: total_documentos
          });

          if (estado === 'completado') {
            setBatchStatus('completed');
            isPolling = false;
            onComplete();
          } else if (estado === 'error') {
            setBatchStatus('error');
            setErrorMsg('Ocurrió un error durante la preparación del lote.');
            isPolling = false;
          } else {
            // Sigue en proceso, programar siguiente revisión
            if (isPolling) timeoutId = setTimeout(checkStatus, 1500);
          }
        } else {
          setBatchStatus('error');
          setErrorMsg(response.error || 'Error desconocido al consultar el estado.');
          isPolling = false;
        }
      } catch (err) {
        setBatchStatus('error');
        setErrorMsg('Error de conexión con el servidor.');
        isPolling = false;
      }
    };

    // Iniciar polling
    checkStatus();

    return () => {
      isPolling = false;
      clearTimeout(timeoutId);
    };
  }, [batchId, onComplete, setBatchProgress, setBatchStatus]);

  if (errorMsg) {
    return (
      <div className={styles['grm-ingestion-progress']}>
        <div style={{ color: '#f85149', marginBottom: '16px' }}>{errorMsg}</div>
        <button onClick={() => window.location.reload()} className="grm-btn grm-btn--outline">
          Recargar y reintentar
        </button>
      </div>
    );
  }

  const progressPercentage = batchProgress && batchProgress.total > 0 
    ? (batchProgress.preparados / batchProgress.total) * 100 
    : 0;

  return (
    <div className={styles['grm-ingestion-progress']}>
      <div className={styles['grm-ingestion-progress__spinner-container']}>
        <Loader2 size={48} className={styles['grm-ingestion-progress__spinner']} />
      </div>
      <div className={styles['grm-ingestion-progress__text']}>
        Preparando {batchProgress?.preparados || 0} de {batchProgress?.total || 0} documentos...
      </div>
      <div className={styles['grm-ingestion-progress__bar-container']}>
        <div 
          className={styles['grm-ingestion-progress__bar']} 
          style={{ width: `${progressPercentage}%` }}
        />
      </div>
    </div>
  );
};
