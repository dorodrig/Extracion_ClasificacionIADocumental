import React, { useEffect, useState } from 'react';
import { usePendientesStore } from '../store/pendientesStore';
import { PendingFilters } from '../components/pending/PendingFilters';
import { PendingDocumentList } from '../components/pending/PendingDocumentList';
import { DocumentViewer } from '../components/pending/DocumentViewer';
import { wsService } from '../services/websocketService';

export const PendientesPage: React.FC = () => {
  const { 
    documentoSeleccionado, 
    fetchPendientes, 
    isLoadingLista, 
    error,
    actualizarDocumentoWS,
    nuevoDocumentoWS
  } = usePendientesStore();

  const [notification, setNotification] = useState<{ id: string, filename: string, motivo: string } | null>(null);

  useEffect(() => {
    fetchPendientes();

    // Inicializar WebSocket
    wsService.connect();

    wsService.onMessage((data) => {
      // Diferenciar el tipo de mensaje que llega por WS
      if (data.type === 'NEW_DOCUMENT') {
        nuevoDocumentoWS(data.document);
        // Mostrar notificación
        setNotification({
          id: data.document.id,
          filename: data.document.filename,
          motivo: data.document.motivoRechazo
        });
        
        // Ocultar notificación después de 8 segundos
        setTimeout(() => {
          setNotification(null);
        }, 8000);
      } else if (data.type === 'UPDATE_DOCUMENT') {
        actualizarDocumentoWS(data.document);
      }
    });

    return () => {
      wsService.disconnect();
    };
  }, [fetchPendientes, nuevoDocumentoWS, actualizarDocumentoWS]);

  // Si hay un documento seleccionado, mostramos solo el visor (Full Page Mode)
  if (documentoSeleccionado) {
    return <DocumentViewer />;
  }

  // Si no, mostramos la lista
  return (
    <div className="pendientes-page">
      <div style={{ marginBottom: '16px' }}>
        {/* Breadcrumb simulado */}
        <span style={{ color: '#8b949e' }}>Inicio {'>'} </span>
        <span style={{ color: '#c9d1d9', fontWeight: 600 }}>Documentos Pendientes</span>
      </div>

      <h1 style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        Documentos Pendientes
        <span style={{ 
          background: '#f85149', 
          color: '#ffffff', 
          fontSize: '14px', 
          padding: '2px 8px', 
          borderRadius: '12px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          {usePendientesStore.getState().documentos.length}
        </span>
      </h1>

      <PendingFilters 
        onFilterChange={(filters) => console.log('Filtros aplicados:', filters)}
        onClear={() => console.log('Limpiar filtros')}
      />

      {isLoadingLista ? (
        <div style={{ padding: '32px', textAlign: 'center', color: '#8b949e' }}>Cargando lista de pendientes...</div>
      ) : error ? (
        <div style={{ padding: '32px', textAlign: 'center', color: '#f85149' }}>Error: {error}</div>
      ) : (
        <PendingDocumentList />
      )}

      {/* Toast Notification para nuevos documentos */}
      {notification && (
        <div style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          backgroundColor: '#161b22',
          border: '1px solid #30363d',
          borderRadius: '8px',
          padding: '16px',
          boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
          zIndex: 1000,
          animation: 'fadeIn 0.3s ease-out'
        }}>
          <div style={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <span>🔔</span> Nuevo documento pendiente
          </div>
          <div style={{ color: '#8b949e', fontSize: '14px', marginBottom: '16px' }}>
            {notification.filename} — Motivo: {notification.motivo}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <button 
              style={{ background: 'transparent', border: 'none', color: '#2f81f7', cursor: 'pointer', padding: 0 }}
              onClick={() => usePendientesStore.getState().abrirVisor(notification.id)}
            >
              Ver ahora
            </button>
            <button 
              style={{ background: 'transparent', border: 'none', color: '#8b949e', cursor: 'pointer', padding: 0 }}
              onClick={() => setNotification(null)}
            >
              Descartar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
