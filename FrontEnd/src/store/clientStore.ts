/**
 * Estado global del cliente activo — GRM Frontend
 * Gobernanza §4.2 — Zustand para estado global
 *
 * Nota del Arquitecto: Dado que HU-08 (Autenticación) no está completada,
 * se mockea cliente_id = 1 y "Cliente Activo: BANCORP".
 *
 * HU-07: Se agrega estado de sesión para el Portal Cliente
 * (isPortalAuthenticated, lastActivity, portalLogin, portalLogout, resetActivity).
 */
import { create } from 'zustand';

interface ClientState {
  clienteId: number;
  clienteNombre: string;
  operarioNombre: string;
  operarioRol: string;
  isPortalAuthenticated: boolean;
  lastActivity: number;
}

interface ClientStore extends ClientState {
  setCliente: (clienteId: number, clienteNombre: string) => void;
  portalLogin: (nombre: string) => void;
  portalLogout: () => void;
  resetActivity: () => void;
}

export const useClientStore = create<ClientStore>((set) => ({
  // Mock inicial — se reemplazará con datos reales de HU-08
  clienteId: 1,
  clienteNombre: 'BANCORP',
  operarioNombre: 'Juan Pérez',
  operarioRol: 'Operario Senior',

  // Portal Cliente session state (HU-07)
  isPortalAuthenticated: false,
  lastActivity: Date.now(),

  setCliente: (clienteId, clienteNombre) =>
    set({ clienteId, clienteNombre }),

  portalLogin: (nombre) =>
    set({ isPortalAuthenticated: true, clienteNombre: nombre, lastActivity: Date.now() }),

  portalLogout: () =>
    set({ isPortalAuthenticated: false }),

  resetActivity: () =>
    set({ lastActivity: Date.now() }),
}));
