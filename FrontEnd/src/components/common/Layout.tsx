/**
 * Layout — Shell de la aplicación GRM
 * Gobernanza §4.2 — Componente funcional con React Hooks
 * Incluye Header, Sidebar con navegación, y área de contenido principal.
 */
import React from 'react';
import { useClientStore } from '../../store/clientStore';

interface LayoutProps {
  children: React.ReactNode;
}

const navItems = [
  { id: 'inicio', label: 'Inicio', icon: '🏠', path: '/', active: false },
  { id: 'reglas', label: 'Reglas de Trabajo', icon: '⚙️', path: '/reglas', active: true },
  { id: 'ingresar', label: 'Ingresar', icon: '📤', path: '/ingresar', active: false },
  { id: 'pendientes', label: 'Pendientes', icon: '📋', path: '/pendientes', active: false, badge: 3 },
  { id: 'historial', label: 'Historial', icon: '📜', path: '/historial', active: false },
];

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { clienteNombre, operarioNombre, operarioRol } = useClientStore();

  return (
    <div className="grm-app-layout">
      {/* Sidebar */}
      <aside className="grm-sidebar">
        <div className="grm-sidebar__logo">
          <div className="grm-sidebar__logo-icon">GRM</div>
          <div className="grm-sidebar__logo-text">
            GRM Document Intelligence
            <span>v1.0.0</span>
          </div>
        </div>

        <div className="grm-sidebar__user">
          <div className="grm-sidebar__user-name">{operarioNombre}</div>
          <div className="grm-sidebar__user-role">{operarioRol}</div>
        </div>

        <nav className="grm-sidebar__nav">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`grm-sidebar__nav-item ${
                item.active ? 'grm-sidebar__nav-item--active' : ''
              }`}
              type="button"
            >
              <span className="grm-sidebar__nav-item-icon">{item.icon}</span>
              {item.label}
              {item.badge !== undefined && (
                <span className="grm-sidebar__nav-item-badge">{item.badge}</span>
              )}
            </button>
          ))}
        </nav>
      </aside>

      {/* Header */}
      <header className="grm-header">
        <div className="grm-header__left">
          <div className="grm-header__info">
            Operario: <strong>{operarioNombre}</strong> &nbsp;|&nbsp; Cliente Activo:{' '}
            <strong>{clienteNombre}</strong>
          </div>
        </div>

        <div className="grm-header__right">
          <button className="grm-header__btn" type="button">
            ↻ Cambiar Cliente
          </button>
          <button className="grm-header__btn grm-header__btn--logout" type="button">
            Cerrar Sesión
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="grm-main">
        {/* Breadcrumb */}
        <nav className="grm-breadcrumb">
          <span className="grm-breadcrumb__item">Inicio</span>
          <span className="grm-breadcrumb__separator">›</span>
          <span className="grm-breadcrumb__item grm-breadcrumb__item--active">
            Reglas de Trabajo
          </span>
        </nav>

        {children}
      </main>
    </div>
  );
};
