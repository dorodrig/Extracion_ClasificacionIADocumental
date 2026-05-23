import React from 'react';
import { usePendientesStore } from '../../store/pendientesStore';

export const PendingDocumentList: React.FC = () => {
  const { documentos, abrirVisor } = usePendientesStore();

  const getTiempoCola = (fechaIngreso: string) => {
    const minDiff = Math.floor((new Date().getTime() - new Date(fechaIngreso).getTime()) / 60000);
    
    let clase = 'ok';
    let icono = '🟢';
    
    if (minDiff > 60) {
      clase = 'urgente';
      icono = '🔴';
    } else if (minDiff >= 15) {
      clase = 'advertencia';
      icono = '🟡';
    }

    const formato = minDiff >= 60 ? `${Math.floor(minDiff/60)}h ${minDiff%60}m` : `${minDiff}m`;

    return (
      <div className={`tiempo-cola ${clase}`} title={`Ingresó a cola: ${new Date(fechaIngreso).toLocaleString()}`}>
        <span>{icono}</span>
        <span>{formato}</span>
      </div>
    );
  };

  if (documentos.length === 0) {
    return (
      <div className="empty-state">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <h3>No hay documentos pendientes de revisión.</h3>
        <p>Todo el lote fue procesado exitosamente.</p>
        <button style={{ marginTop: '1rem', padding: '0.5rem 1rem', background: 'transparent', color: '#8b949e', border: '1px solid #30363d', borderRadius: '4px' }}>
          Ver Historial de Lotes
        </button>
      </div>
    );
  }

  return (
    <table className="pendientes-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Archivo</th>
          <th>Cliente</th>
          <th>Motivo de Rechazo</th>
          <th>En cola</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {documentos.map((doc, idx) => (
          <tr key={doc.id}>
            <td>{idx + 1}</td>
            <td>📄 {doc.filename}</td>
            <td>{doc.cliente}</td>
            <td>
              {doc.motivoRechazo === '⟳ En reprocesamiento...' ? (
                <span style={{ color: '#2f81f7' }}>{doc.motivoRechazo}</span>
              ) : (
                doc.motivoRechazo
              )}
            </td>
            <td>{doc.motivoRechazo === '⟳ En reprocesamiento...' ? '—' : getTiempoCola(doc.enColaDesde)}</td>
            <td>
              {doc.motivoRechazo === '⟳ En reprocesamiento...' ? (
                <button className="btn-estado" disabled>Ver estado</button>
              ) : (
                <button className="btn-revisar" onClick={() => abrirVisor(doc.id)}>Revisar</button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
