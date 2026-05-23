import { create } from 'zustand';

export interface AuthUser {
  id: string;
  cedula: string;
  role: 'Admin' | 'Operario' | 'Cliente';
  nombre?: string;
}

interface AuthState {
  token: string | null;
  user: AuthUser | null;
  selectedClient: string | null;
  login: (token: string, user: AuthUser) => void;
  logout: () => void;
  setClient: (client: string) => void;
}

const getInitialState = () => {
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');
  const selectedClient = localStorage.getItem('selectedClient');
  
  return {
    token: token || null,
    user: userStr ? JSON.parse(userStr) : null,
    selectedClient: selectedClient || null,
  };
};

export const useAuthStore = create<AuthState>((set) => ({
  ...getInitialState(),
  
  login: (token: string, user: AuthUser) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ token, user, selectedClient: null });
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('selectedClient');
    set({ token: null, user: null, selectedClient: null });
  },
  
  setClient: (client: string) => {
    localStorage.setItem('selectedClient', client);
    set({ selectedClient: client });
  },
}));
