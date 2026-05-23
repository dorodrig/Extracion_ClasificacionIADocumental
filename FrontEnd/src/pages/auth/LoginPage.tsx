import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import api from '../../services/api';

export const LoginPage = () => {
  const [cedula, setCedula] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // BYPASS
    navigate('/admin/dashboard');
    /*
    if (!cedula.trim() || !password.trim()) {
      setError('Cédula y contraseña son requeridas');
      return;
    }
    
    setError(null);
    setLoading(true);
    
    try {
      const response = await api.post('/api/v1/auth/token', {
        cedula,
        password,
      });
      
      // Handle APIResponse wrapper if present
      const responseData = response.data.data ? response.data.data : response.data;
      const { access_token } = responseData;
      const user = responseData.user || {};
      
      if (!access_token) {
        throw new Error('No se recibió un token de acceso válido.');
      }
      
      // Attempt to decode JWT to extract roles if not directly in user object
      let payload: any = {};
      try {
        payload = JSON.parse(atob(access_token.split('.')[1]));
      } catch (e) {
        console.warn('Could not decode JWT payload');
      }
      
      const authUser: any = {
        id: payload.sub || payload.usuario_id || user.id || '1',
        cedula: cedula,
        role: payload.rol || user.role || payload.role || 'Operario',
        nombre: payload.nombre || user.nombre || 'Usuario',
      };
      
      login(access_token, authUser);
      
      if (authUser.role === 'Admin') navigate('/admin/dashboard');
      else if (authUser.role === 'Operario') navigate('/operario/seleccion-cliente');
      else navigate('/cliente/dashboard');
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error de autenticación. Verifique sus credenciales.');
    } finally {
      setLoading(false);
    }
    */
  };

  return (
    <div className="grm-login-page" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f5f5f5' }}>
      <form onSubmit={handleSubmit} style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>Iniciar Sesión</h2>
        {error && <div style={{ color: 'red', marginBottom: '1rem', padding: '0.5rem', background: '#ffebee', borderRadius: '4px' }}>{error}</div>}
        
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Cédula</label>
          <input
            type="text"
            value={cedula}
            onChange={(e) => setCedula(e.target.value)}
            disabled={loading}
            style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc' }}
          />
        </div>
        
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Contraseña</label>
          <div style={{ display: 'flex' }}>
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              style={{ width: '100%', padding: '0.5rem', borderRadius: '4px 0 0 4px', border: '1px solid #ccc', borderRight: 'none' }}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              style={{ padding: '0.5rem 1rem', background: '#e0e0e0', border: '1px solid #ccc', borderRadius: '0 4px 4px 0', cursor: 'pointer' }}
            >
              {showPassword ? 'Ocultar' : 'Mostrar'}
            </button>
          </div>
        </div>
        
        <button 
          type="submit" 
          disabled={loading} 
          style={{ width: '100%', padding: '0.75rem', background: '#0056b3', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1rem' }}
        >
          {loading ? 'Cargando...' : 'Ingresar'}
        </button>
      </form>
    </div>
  );
};
