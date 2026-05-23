/**
 * PortalLayout — Shell layout for the client portal (light theme)
 * HU-07 — Portal de Consulta para Clientes
 */
import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  FolderOpen,
  Search,
  Download,
  LogOut,
} from 'lucide-react';
import { useClientStore } from '@/store/clientStore';
import { useSessionTimeout } from '@/hooks/useSessionTimeout';

interface PortalLayoutProps {
  children: React.ReactNode;
}

interface NavItem {
  icon: React.FC<{ size?: number }>;
  label: string;
  path: string;
}

const navItems: NavItem[] = [
  { icon: LayoutDashboard, label: 'Inicio', path: '/cliente/dashboard' },
  { icon: FolderOpen, label: 'Mis Documentos', path: '/cliente/documentos' },
  { icon: Search, label: 'Explorador', path: '/cliente/explorador' },
  { icon: Download, label: 'Descargas', path: '/cliente/documentos' },
];

export const PortalLayout: React.FC<PortalLayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const { clienteNombre, portalLogout } = useClientStore();

  useSessionTimeout();

  const handleLogout = () => {
    portalLogout();
    navigate('/cliente/login');
  };

  return (
    <div className="grm-portal">
      <header className="grm-portal-header">
        <div className="grm-portal-header__logo">
          <div className="grm-portal-header__logo-icon">GRM</div>
          <span>Portal de Documentos</span>
        </div>
        <div className="grm-portal-header__user">
          <span>Bienvenido, {clienteNombre}</span>
          <button
            onClick={handleLogout}
            className="grm-portal-header__logout-btn"
          >
            <LogOut size={16} />
            Cerrar Sesión
          </button>
        </div>
      </header>

      <aside className="grm-portal-sidebar">
        <nav className="grm-portal-sidebar__nav">
          {navItems.map((item) => (
            <NavLink
              key={item.label}
              to={item.path}
              className={({ isActive }) =>
                `grm-portal-sidebar__item${isActive ? ' grm-portal-sidebar__item--active' : ''}`
              }
            >
              <item.icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="grm-portal-main">{children}</main>
    </div>
  );
};
