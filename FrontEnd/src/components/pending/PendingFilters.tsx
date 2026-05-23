import React, { useState } from 'react';

interface PendingFiltersProps {
  onFilterChange: (filters: any) => void;
  onClear: () => void;
}

export const PendingFilters: React.FC<PendingFiltersProps> = ({ onFilterChange, onClear }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [cliente, setCliente] = useState('');
  const [motivo, setMotivo] = useState('');

  const hasActiveFilters = searchTerm !== '' || cliente !== '' || motivo !== '';

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    onFilterChange({ search: e.target.value, cliente, motivo });
  };

  const handleClear = () => {
    setSearchTerm('');
    setCliente('');
    setMotivo('');
    onClear();
  };

  return (
    <div className="pendientes-filters">
      <input 
        type="text" 
        placeholder="🔍 Buscar por nombre de archivo..." 
        value={searchTerm}
        onChange={handleSearchChange}
      />
      
      <select value={cliente} onChange={(e) => { setCliente(e.target.value); onFilterChange({ search: searchTerm, cliente: e.target.value, motivo }); }}>
        <option value="">Cliente ▼</option>
        <option value="BANCORP">BANCORP</option>
        <option value="ACME">ACME</option>
      </select>

      <select value={motivo} onChange={(e) => { setMotivo(e.target.value); onFilterChange({ search: searchTerm, cliente, motivo: e.target.value }); }}>
        <option value="">Motivo ▼</option>
        <option value="Campo nulo">Campo nulo</option>
        <option value="Campo incompleto">Campo incompleto</option>
        <option value="Baja confianza">Baja confianza</option>
        <option value="Tipo incorrecto">Tipo incorrecto</option>
        <option value="Error de IA">Error de IA</option>
      </select>

      <input type="date" title="Desde" />
      <span>—</span>
      <input type="date" title="Hasta" />

      {hasActiveFilters && (
        <button className="btn-limpiar" onClick={handleClear} title="Limpiar filtros">
          ✕
        </button>
      )}
    </div>
  );
};
