/**
 * Instancia Axios centralizada — GRM Frontend
 * Gobernanza §4.3 — Interceptores JWT + manejo de 401
 */
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor: agregar JWT automáticamente (cuando Auth esté implementado - HU-08)
api.interceptors.request.use((config) => {
  // TODO: HU-08 — Obtener token del authStore cuando esté implementado
  // const token = useAuthStore.getState().token;
  // if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Interceptor: manejar 401 globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // TODO: HU-08 — Redirigir a login cuando Auth esté implementado
      // useAuthStore.getState().logout();
      // window.location.href = '/login';
      console.warn('GRM: 401 Unauthorized — Auth no implementada aún (HU-08)');
    }
    return Promise.reject(error);
  }
);

export default api;
