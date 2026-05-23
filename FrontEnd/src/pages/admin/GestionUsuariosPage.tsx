import React, { useState, useEffect } from 'react';
import api from '../../services/api';

interface User {
  id: string;
  cedula: string;
  nombre: string;
  role: string;
  activo: boolean;
}

export const GestionUsuariosPage = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    cedula: '',
    nombre: '',
    password: '',
    role: 'Operario'
  });

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const res = await api.get('/api/v1/usuarios/');
      setUsers(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al cargar usuarios');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/api/v1/usuarios/', formData);
      setShowForm(false);
      setFormData({ cedula: '', nombre: '', password: '', role: 'Operario' });
      fetchUsers();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al crear usuario');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Gestión de Usuarios</h2>
        <button 
          onClick={() => setShowForm(!showForm)}
          style={{ padding: '0.5rem 1rem', background: '#0056b3', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          {showForm ? 'Cancelar' : 'Nuevo Usuario'}
        </button>
      </div>

      {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}

      {showForm && (
        <form onSubmit={handleSubmit} style={{ background: '#f5f5f5', padding: '1.5rem', borderRadius: '8px', marginBottom: '2rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Cédula</label>
              <input type="text" value={formData.cedula} onChange={e => setFormData({...formData, cedula: e.target.value})} required style={{ width: '100%', padding: '0.5rem', border: '1px solid #ccc', borderRadius: '4px' }} />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Nombre</label>
              <input type="text" value={formData.nombre} onChange={e => setFormData({...formData, nombre: e.target.value})} required style={{ width: '100%', padding: '0.5rem', border: '1px solid #ccc', borderRadius: '4px' }} />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Contraseña</label>
              <input type="password" value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} required style={{ width: '100%', padding: '0.5rem', border: '1px solid #ccc', borderRadius: '4px' }} />
            </div>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Rol</label>
              <select value={formData.role} onChange={e => setFormData({...formData, role: e.target.value})} style={{ width: '100%', padding: '0.5rem', border: '1px solid #ccc', borderRadius: '4px' }}>
                <option value="Admin">Admin</option>
                <option value="Operario">Operario</option>
                <option value="Cliente">Cliente</option>
              </select>
            </div>
          </div>
          <button type="submit" style={{ padding: '0.5rem 1rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Crear Usuario</button>
        </form>
      )}

      {loading ? (
        <p>Cargando usuarios...</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', background: 'white', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <thead>
            <tr style={{ background: '#f8f9fa', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>
              <th style={{ padding: '1rem' }}>Cédula</th>
              <th style={{ padding: '1rem' }}>Nombre</th>
              <th style={{ padding: '1rem' }}>Rol</th>
              <th style={{ padding: '1rem' }}>Estado</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                <td style={{ padding: '1rem' }}>{u.cedula}</td>
                <td style={{ padding: '1rem' }}>{u.nombre}</td>
                <td style={{ padding: '1rem' }}>{u.role}</td>
                <td style={{ padding: '1rem' }}>
                  <span style={{ 
                    padding: '0.25rem 0.5rem', 
                    borderRadius: '12px', 
                    fontSize: '0.85rem',
                    background: u.activo !== false ? '#d4edda' : '#f8d7da',
                    color: u.activo !== false ? '#155724' : '#721c24'
                  }}>
                    {u.activo !== false ? 'Activo' : 'Bloqueado'}
                  </span>
                </td>
              </tr>
            ))}
            {users.length === 0 && (
              <tr>
                <td colSpan={4} style={{ padding: '2rem', textAlign: 'center', color: '#6c757d' }}>No hay usuarios registrados.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
};
