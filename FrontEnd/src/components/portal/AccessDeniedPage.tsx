/**
 * AccessDeniedPage — Error page for unauthorized access
 * HU-07 — Portal de Consulta para Clientes
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock } from 'lucide-react';

export const AccessDeniedPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="grm-portal-error">
      <Lock size={80} className="grm-portal-error__icon" />
      <h1 className="grm-portal-error__title">Acceso Denegado</h1>
      <p className="grm-portal-error__message">
        No tiene permisos para acceder a este recurso. Contacte al
        administrador si cree que esto es un error.
      </p>
      <button
        className="grm-portal-error__btn"
        onClick={() => navigate('/cliente/dashboard')}
      >
        Volver al Dashboard
      </button>
    </div>
  );
};
