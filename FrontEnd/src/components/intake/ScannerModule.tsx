import React, { useState } from 'react';
import { useBatchStore } from '@/store/batchStore';
import { batchService } from '@/services/batchService';
import { DocumentList } from './DocumentList';
import dashboardStyles from './IntakeDashboard.module.scss';
import styles from './ScannerModule.module.scss';
import { Printer, AlertTriangle, RefreshCcw, Scan } from 'lucide-react';

export const ScannerModule: React.FC = () => {
  const [connectedDevice, setConnectedDevice] = useState<string | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { addDocuments, documentsList, setActiveBatch } = useBatchStore();

  const handleConnect = (deviceName: string) => {
    // Mock connection
    setConnectedDevice(deviceName);
    setError(null);
    
    // Create batch in backend
    batchService.createBatch('scanner').then(res => {
      if (res.data) setActiveBatch(res.data.batch_id);
    });
  };

  const handleScan = () => {
    setIsScanning(true);
    
    // Simulate scan delay
    setTimeout(() => {
      const mockDocs = Array.from({ length: 3 }).map((_, i) => ({
        id: `scan_${Date.now()}_${i}`,
        file: null,
        name: `scan_${String(documentsList.length + i + 1).padStart(3, '0')}.pdf`,
        extension: 'PDF',
        pages: Math.floor(Math.random() * 5) + 1,
        sizeMB: parseFloat((Math.random() * 2 + 0.1).toFixed(1)),
        status: (Math.random() > 0.9 ? 'Ilegible' : 'Listo') as 'Listo' | 'Ilegible',
        selected: true
      }));
      
      addDocuments(mockDocs);
      setIsScanning(false);
    }, 2000);
  };

  return (
    <div className={styles['grm-scanner-module']}>
      {!connectedDevice ? (
        <>
          <div className={styles['grm-scanner-module__header']}>
            <h3>CONECTAR ESCÁNER</h3>
          </div>
          
          <p>Dispositivos detectados:</p>
          <div className={styles['grm-scanner-module__device-list']}>
            <div className={styles['device-item']}>
              <span>🖨 HP ScanJet Pro 3600</span>
              <button 
                className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--outline']}`}
                onClick={() => handleConnect('HP ScanJet Pro 3600')}
              >
                Seleccionar
              </button>
            </div>
            <div className={styles['device-item']}>
              <span>🖨 Canon DR-C230</span>
              <button 
                className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--outline']}`}
                onClick={() => handleConnect('Canon DR-C230')}
              >
                Seleccionar
              </button>
            </div>
          </div>
          
          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <button className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--outline']}`}>
              <RefreshCcw size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }}/> Buscar Escáneres
            </button>
          </div>
          
          <div className={styles['grm-scanner-module__warning']}>
            <AlertTriangle size={16} /> Si no aparece tu escáner, verifica la conexión USB/red y que el driver esté instalado.
          </div>
        </>
      ) : (
        <>
          <div className={styles['grm-scanner-module__header']}>
            <div className={`${styles['status']} ${styles['connected']}`}>
              <Printer size={20} />
              <span>{connectedDevice} ● Conectado</span>
            </div>
            <button 
              className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--outline']}`}
              onClick={() => setConnectedDevice(null)}
            >
              Desconectar
            </button>
          </div>
          
          <div className={styles['grm-scanner-module__capture-area']}>
            <Scan size={64} className={styles['icon']} />
            <p>Coloca los documentos en el escáner y presiona el botón de inicio de escáner</p>
            <button 
              className={`${dashboardStyles['grm-btn']} ${dashboardStyles['grm-btn--primary']}`}
              onClick={handleScan}
              disabled={isScanning}
            >
              {isScanning ? 'Escaneando...' : '▶ Iniciar Escaneo'}
            </button>
          </div>
          
          {documentsList.length > 0 && <DocumentList mode="scanner" />}
        </>
      )}
    </div>
  );
};
