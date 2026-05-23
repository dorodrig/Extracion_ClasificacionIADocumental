import React, { useState } from 'react';
import { usePendientesStore } from '../../store/pendientesStore';
import { pendientesService, ExtractedField } from '../../services/pendientesService';

export const ExtractedDataPanel: React.FC = () => {
  const { documentoSeleccionado, cerrarVisor, setDocumentoEnReprocesamiento } = usePendientesStore();
  const [camposEditables, setCamposEditables] = useState<Record<string, string>>({});
  const [instruccionIA, setInstruccionIA] = useState('');
  const [campoActivoId, setCampoActivoId] = useState<string | null>(null);

  if (!documentoSeleccionado) return null;

  // Lógica para determinar el campo problemático principal
  const camposConError = documentoSeleccionado.campos.filter(c => c.estado !== 'Validado');
  const multipleErrores = camposConError.length > 1;

  // Setear el campo activo inicialmente si hay un error
  React.useEffect(() => {
    if (camposConError.length === 1 && !campoActivoId) {
      setCampoActivoId(camposConError[0].id);
    }
  }, [camposConError, campoActivoId]);

  const handleFieldChange = (id: string, value: string) => {
    setCamposEditables(prev => ({ ...prev, [id]: value }));
  };

  const handleFieldClick = (field: ExtractedField) => {
    if (field.estado === 'Validado') {
      const confirmEdit = window.confirm('Este campo fue validado correctamente. ¿Deseas editarlo igualmente?');
      if (confirmEdit) {
        setCampoActivoId(field.id);
        if (field.valor) {
          handleFieldChange(field.id, field.valor);
        }
      }
    } else {
      setCampoActivoId(field.id);
      if (field.valor && !camposEditables[field.id]) {
        handleFieldChange(field.id, field.valor);
      }
    }
  };

  const handleGuardarCorreccion = async () => {
    try {
      await pendientesService.corregirDocumento(documentoSeleccionado.id, camposEditables);
      setDocumentoEnReprocesamiento(documentoSeleccionado.id);
      cerrarVisor();
    } catch (err) {
      console.error('Error al guardar corrección', err);
      alert('Error al guardar la corrección');
    }
  };

  const handleEnviarInstruccion = async () => {
    if (instruccionIA.length < 20) return;
    try {
      await pendientesService.enviarInstruccion(documentoSeleccionado.id, instruccionIA);
      setDocumentoEnReprocesamiento(documentoSeleccionado.id);
      cerrarVisor();
    } catch (err) {
      console.error('Error al enviar instrucción', err);
      alert('Error al enviar instrucción');
    }
  };

  const handleDescartar = async () => {
    const motivo = window.prompt('Motivo de descarte (obligatorio):');
    if (motivo) {
      try {
        await pendientesService.descartarDocumento(documentoSeleccionado.id, motivo);
        cerrarVisor();
      } catch (err) {
        console.error('Error al descartar', err);
        alert('Error al descartar el documento');
      }
    }
  };

  const renderField = (field: ExtractedField) => {
    const isEditing = campoActivoId === field.id;
    const value = isEditing ? (camposEditables[field.id] ?? field.valor ?? '') : (field.valor ?? `[${field.nombre} vacío]`);
    const hasError = field.estado === 'No encontrado';
    const isWarning = field.estado === 'Baja confianza';

    let statusTextClass = 'validado';
    let statusIcon = '✓';
    
    if (hasError) {
      statusTextClass = 'error';
      statusIcon = '✗';
    } else if (isWarning) {
      statusTextClass = 'advertencia';
      statusIcon = '⚠';
    }

    return (
      <div key={field.id} className="field-item">
        <div className="field-label">
          {field.nombre}
          {field.obligatorio && <span className="required">* (Obligatorio)</span>}
        </div>
        <input 
          type="text" 
          value={value}
          readOnly={!isEditing}
          className={`${isEditing ? 'editable' : ''} ${hasError && !isEditing ? 'error-border' : ''}`}
          onChange={(e) => handleFieldChange(field.id, e.target.value)}
          onClick={() => !isEditing && handleFieldClick(field)}
        />
        <div className="field-status">
          <span className={`status-text ${statusTextClass}`}>
            {statusIcon} {field.estado}
          </span>
          <span className="ocr-score">
            OCR: {field.ocrScore ? `${field.ocrScore}%` : '—'}
          </span>
        </div>
      </div>
    );
  };

  const isCorreccionValid = Object.keys(camposEditables).length > 0;
  const isInstruccionValid = instruccionIA.length >= 20;

  return (
    <div className="extracted-data-panel">
      <div className="panel-header">
        <div className="title">⚠ PENDIENTE DE REVISIÓN</div>
        <div className="subtitle">
          Revisa y corrige los campos extraídos o envía instrucciones al agente.
        </div>
      </div>

      <div className="fields-container">
        {documentoSeleccionado.campos.map(renderField)}
      </div>

      <div className="actions-container">
        <div className={`action-card ${!multipleErrores ? 'active' : ''}`}>
          <div className="card-title">✎ Corrección directa</div>
          <div style={{ fontSize: '12px', color: '#8b949e', marginBottom: '8px' }}>
            ({camposConError.length} campo(s) con problema)
          </div>
          <button 
            className="btn-success" 
            disabled={!isCorreccionValid}
            onClick={handleGuardarCorreccion}
          >
            Guardar corrección ▶
          </button>
        </div>

        <div className="divider">O</div>

        <div className={`action-card ${multipleErrores ? 'active' : ''}`}>
          <div className="card-title">🤖 Enviar al Agente</div>
          <textarea 
            placeholder="Ej: El CC del titular es 987654321. El nombre correcto es MARIA GARCIA. El tipo de documento es Pagaré."
            value={instruccionIA}
            onChange={(e) => setInstruccionIA(e.target.value)}
          />
          <div className="char-counter">{instruccionIA.length} / 500</div>
          <button 
            className="btn-primary" 
            disabled={!isInstruccionValid}
            onClick={handleEnviarInstruccion}
          >
            Enviar al Agente ▶
          </button>
        </div>

        <button className="btn-descartar" onClick={handleDescartar}>
          🗑 Descartar documento
        </button>
      </div>
    </div>
  );
};
