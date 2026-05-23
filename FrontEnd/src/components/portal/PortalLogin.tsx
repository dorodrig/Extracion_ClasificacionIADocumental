/**
 * PortalLogin — Login page for the client portal
 * HU-07 — Portal de Consulta para Clientes
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useClientStore } from '@/store/clientStore';

export const PortalLogin: React.FC = () => {
  const navigate = useNavigate();
  const { portalLogin } = useClientStore();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) return;
    portalLogin(username);
    navigate('/cliente/dashboard');
  };

  return (
    <div className="grm-portal-login">
      <div className="grm-portal-login__card">
        <div className="grm-portal-login__logo">
          <div className="grm-portal-login__logo-icon">GRM</div>
        </div>
        <h1 className="grm-portal-login__title">Portal de Documentos</h1>
        <p className="grm-portal-login__subtitle">
          Ingrese sus credenciales para acceder
        </p>
        <form onSubmit={handleLogin} className="grm-portal-login__form">
          <div className="grm-portal-login__field">
            <label htmlFor="portal-username">Usuario / Empresa</label>
            <input
              id="portal-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Ej: BANCORP"
            />
          </div>
          <div className="grm-portal-login__field">
            <label htmlFor="portal-password">Contraseña</label>
            <input
              id="portal-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          <button
            type="submit"
            className="grm-portal-login__submit"
            disabled={!username || !password}
          >
            Iniciar Sesión
          </button>
        </form>
        <p className="grm-portal-login__footer">
          GRM Document Intelligence © 2025
        </p>
      </div>
    </div>
  );
};
