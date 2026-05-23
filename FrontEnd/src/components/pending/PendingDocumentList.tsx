import React from 'react';
import { usePendientesStore } from '../../store/pendientesStore';

export const PendingDocumentList: React.FC = () => {
  const { documentos, abrirVisor, isLoadingLista } = usePendientesStore();

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

  if (isLoadingLista) {
    return (
      <div className="empty-state">
        <h3>Cargando documentos...</h3>
      </div>
    );
  }

  // Protección contra nulidad o formato incorrecto (ej: objeto APIResponse)
  const docsArray = Array.isArray(documentos) ? documentos : (documentos as any)?.data || [];

  if (!docsArray || docsArray.length === 0) {
    return (
      <div className="empty-state">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <h3>No hay documentos pendientes de revisión.</h3>
        <p>Todo el lote fue procesado exitosamente o no hay datos disponibles.</p>
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
          <th>Lote de Origen</th>
          <th>Motivo de Rechazo</th>
          <th>En cola</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        {docsArray?.map((doc: any, idx: number) => (
          <tr key={doc?.id || idx}>
            <td>{idx + 1}</td>
            <td>📄 {doc?.filename}</td>
            <td>{doc?.cliente}</td>
            <td>
              <a href={`/lotes/${doc?.lote}`} style={{ color: '#2f81f7', textDecoration: 'none' }}>
                {doc?.lote}
              </a>
            </td>
            <td>
              {doc?.motivoRechazo === '⟳ En reprocesamiento...' ? (
                <span style={{ color: '#2f81f7' }}>{doc?.motivoRechazo}</span>
              ) : (
                doc?.motivoRechazo
              )}
            </td>
            <td>{doc?.motivoRechazo === '⟳ En reprocesamiento...' ? '—' : (doc?.enColaDesde ? getTiempoCola(doc.enColaDesde) : '—')}</td>
            <td>
              {doc?.motivoRechazo === '⟳ En reprocesamiento...' ? (
                <button className="btn-estado" disabled>Ver estado</button>
              ) : (
                <button className="btn-revisar" onClick={() => doc?.id && abrirVisor(doc.id)}>Revisar</button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
