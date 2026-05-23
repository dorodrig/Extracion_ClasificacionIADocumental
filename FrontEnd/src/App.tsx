import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { IntakeDashboard } from '@/components/intake/IntakeDashboard';
import { PendientesPage } from '@/pages/PendientesPage';

function App() {
  return (
    <Router>
      <div className="grm-app">
        <header className="grm-app__header">
          <div className="grm-app__logo">GRM</div>
          <div className="grm-app__user-info">
            Operario: Juan Pérez | Cliente: BANCORP | <a href="#">[Cambiar]</a> <a href="#">[Salir]</a>
          </div>
        </header>
        <div className="grm-app__body">
          <aside className="grm-app__sidebar">
            <nav>
              <ul>
                <li>Inicio</li>
                <li>Reglas</li>
                <li className="active">Ingresar◄</li>
                <li>Pendientes</li>
                <li>Historial</li>
              </ul>
            </nav>
          </aside>
          <main className="grm-app__content">
            <Routes>
              <Route path="/" element={<Navigate to="/intake" replace />} />
              <Route path="/intake" element={<IntakeDashboard />} />
              <Route path="/pendientes" element={<PendientesPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
