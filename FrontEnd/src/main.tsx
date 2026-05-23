/**
 * main.tsx — Entry point de la aplicación GRM Frontend
 * Gobernanza §4.7 — Importa estilos globales SCSS
 */
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles/main.scss';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
