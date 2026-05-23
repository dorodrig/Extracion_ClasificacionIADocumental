import React, { useEffect, useState } from 'react';
import { AuditoriaEvento, getHistorialDocumento } from '../../services/auditoriaService';
import './DocumentTimeline.scss';

interface DocumentTimelineProps {
  documentId: string;
  onClose: () => void;
}

export const DocumentTimeline: React.FC<DocumentTimelineProps> = ({ documentId, onClose }) => {
  const [eventos, setEventos] = useState<AuditoriaEvento[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchHistorial = async () => {
      setLoading(true);
      try {
        const data = await getHistorialDocumento(documentId);
        setEventos(data);
      } catch (error) {
        console.error('Failed to load document history', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchHistorial();
  }, [documentId]);

  return (
    <div className="document-timeline-modal" onClick={onClose}>
      <div className="timeline-content" onClick={(e) => e.stopPropagation()}>
        <div className="timeline-header">
          <h3>Historial y Trazabilidad</h3>
          <button className="close-btn" onClick={onClose} title="Cerrar">
            &times;
          </button>
        </div>
        
        <div className="timeline-body">
          {loading ? (
            <div className="timeline-loading">Cargando historial...</div>
          ) : eventos.length === 0 ? (
            <div className="timeline-empty">No hay eventos registrados para este documento.</div>
          ) : (
            <div className="timeline-container">
              {eventos.map((evento) => (
                <div key={evento.id} className="timeline-item">
                  <div className={`timeline-marker ${evento.estado || 'info'}`}></div>
                  <div className="timeline-card">
                    <div className="timeline-event-title">{evento.evento}</div>
                    <div className="timeline-meta">
                      <span>🕒 {new Date(evento.fecha).toLocaleString()}</span>
                      <span>👤 {evento.usuario}</span>
                    </div>
                    {evento.detalles && (
                      <div className="timeline-details">
                        {evento.detalles}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
