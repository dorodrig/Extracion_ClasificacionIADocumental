import React, { useState } from 'react';
import { useBatchStore } from '@/store/batchStore';
import { ScannerModule } from './ScannerModule';
import { FolderModule } from './FolderModule';
import styles from './IntakeDashboard.module.scss';
import { CheckCircle2, Printer, Folder } from 'lucide-react';

export const IntakeDashboard: React.FC = () => {
  const { ingestMode, setIngestMode } = useBatchStore();
  const [step, setStep] = useState<1 | 2>(1);

  const handleContinue = () => {
    setStep(2);
  };

  return (
    <div className={styles['grm-intake-dashboard']}>
      <div className={styles['grm-intake-dashboard__banner']}>
        <div className={styles['grm-intake-dashboard__banner-info']}>
          <strong>📋 Regla activa: Pagarés 2025 | Tipo: Pagaré</strong>
          <span>Modo preseleccionado: {ingestMode === 'carpeta' ? '📁 Carpeta Local' : '🖨️ Escáner por Lotes'}</span>
        </div>
        <button className={`${styles['grm-btn']} ${styles['grm-btn--outline']}`}>Cambiar Regla</button>
      </div>

      <div className={styles['grm-intake-dashboard__step-indicator']}>
        <span className={step === 1 ? styles['active'] : ''}>[PASO 1: Selección de Modo]</span>
        <span className={step === 2 ? styles['active'] : ''}>[PASO 2: Carga de Documentos]</span>
        <span>[PASO 3: Confirmación y Envío]</span>
      </div>

      {step === 1 && (
        <>
          <h2 className={styles['grm-intake-dashboard__step-title']}>¿Cómo deseas ingresar los documentos?</h2>
          <div className={styles['grm-intake-dashboard__mode-selection']}>
            <div 
              className={`${styles['grm-intake-dashboard__mode-card']} ${ingestMode === 'scanner' ? styles['grm-intake-dashboard__mode-card--selected'] : ''}`}
              onClick={() => setIngestMode('scanner')}
            >
              <Printer className={styles['grm-intake-dashboard__icon']} size={48} />
              <h3>Escáner por Lotes</h3>
              <p>Digitaliza múltiples documentos en una sola sesión de escaneo.</p>
              <div className={styles['grm-intake-dashboard__formats']}>Formatos: PDF</div>
              <CheckCircle2 className={styles['grm-intake-dashboard__check']} size={24} />
            </div>

            <div 
              className={`${styles['grm-intake-dashboard__mode-card']} ${ingestMode === 'carpeta' ? styles['grm-intake-dashboard__mode-card--selected'] : ''}`}
              onClick={() => setIngestMode('carpeta')}
            >
              <Folder className={styles['grm-intake-dashboard__icon']} size={48} />
              <h3>Carpeta Local</h3>
              <p>Selecciona una carpeta local y procesa los archivos uno a uno.</p>
              <div className={styles['grm-intake-dashboard__formats']}>Formatos: PDF, JPG, PNG, TIFF</div>
              <CheckCircle2 className={styles['grm-intake-dashboard__check']} size={24} />
            </div>
          </div>

          <div className={styles['grm-intake-dashboard__actions']}>
            <button className={`${styles['grm-btn']} ${styles['grm-btn--outline']}`}>Cancelar</button>
            <button 
              className={`${styles['grm-btn']} ${styles['grm-btn--primary']}`}
              onClick={handleContinue}
            >
              Continuar ►
            </button>
          </div>
        </>
      )}

      {step === 2 && (
        <>
          {ingestMode === 'scanner' && <ScannerModule />}
          {ingestMode === 'carpeta' && <FolderModule />}
        </>
      )}
    </div>
  );
};
