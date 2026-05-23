import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const SeleccionClientePage = () => {
  const [cliente, setCliente] = useState('');
  const setClient = useAuthStore((state) => state.setClient);
  const user = useAuthStore((state) => state.user);
  const navigate = useNavigate();

  const handleSelect = (e: React.FormEvent) => {
    e.preventDefault();
    if (cliente) {
      setClient(cliente);
      navigate('/intake'); 
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginTop: '4rem' }}>
      <h2>Bienvenido, {user?.nombre || 'Operario'}</h2>
      <p>Por favor seleccione el cliente con el que va a trabajar en esta sesión:</p>
      
      <form onSubmit={handleSelect}>
        <select 
          value={cliente} 
          onChange={(e) => setCliente(e.target.value)}
          style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', fontSize: '1rem', borderRadius: '4px', border: '1px solid #ccc' }}
          required
        >
          <option value="" disabled>-- Seleccione un Cliente --</option>
          <option value="BANCORP">BANCORP</option>
          <option value="FINANCIERA_XYZ">FINANCIERA_XYZ</option>
          <option value="SEGUROS_ABC">SEGUROS_ABC</option>
        </select>
        
        <button 
          type="submit" 
          disabled={!cliente}
          style={{ padding: '0.75rem 1.5rem', background: cliente ? '#0056b3' : '#cccccc', color: 'white', border: 'none', borderRadius: '4px', cursor: cliente ? 'pointer' : 'not-allowed', width: '100%', fontSize: '1rem' }}
        >
          Continuar
        </button>
      </form>
    </div>
  );
};
