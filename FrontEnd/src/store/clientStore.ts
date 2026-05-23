/**
 * Estado global del cliente activo — GRM Frontend
 * Gobernanza §4.2 — Zustand para estado global
 *
 * Nota del Arquitecto: Dado que HU-08 (Autenticación) no está completada,
 * se mockea cliente_id = 1 y "Cliente Activo: BANCORP".
 */
import { create } from 'zustand';

interface ClientState {
  clienteId: number;
  clienteNombre: string;
  operarioNombre: string;
  operarioRol: string;
}

interface ClientStore extends ClientState {
  setCliente: (clienteId: number, clienteNombre: string) => void;
}

export const useClientStore = create<ClientStore>((set) => ({
  // Mock inicial — se reemplazará con datos reales de HU-08
  clienteId: 1,
  clienteNombre: 'BANCORP',
  operarioNombre: 'Juan Pérez',
  operarioRol: 'Operario Senior',

  setCliente: (clienteId, clienteNombre) =>
    set({ clienteId, clienteNombre }),
}));
