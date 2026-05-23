import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Hardcoded as requested for iteration 1
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  // Normally here we get the token from useAuthStore
  // For HU-02 we don't have authentication yet
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle global errors like 401
    return Promise.reject(error);
  }
);

export default api;
