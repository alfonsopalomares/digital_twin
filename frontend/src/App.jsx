
import { Routes, Route, Link } from 'react-router-dom';
import MainPage from './MainPage';
import SimulatePage from './SimulatePage';
import AnalyticsPage from './AnalyticsPage';
import AnomaliesPage from './AnomaliesPage';
import MetricsPage from './MetricsPage';

// Justo antes de tu componente App
const menuStyle = {
  display: 'flex',
  alignItems: 'center',
  backgroundColor: '#f0f4f8',   // un gris muy suave
  padding: '12px 24px',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
};
const linkStyle = {
  marginRight: 16,
  textDecoration: 'none',
  color: '#2a4365',              // un azul oscuro
  fontWeight: 500,
  padding: '8px 12px',
  borderRadius: 4,
  transition: 'background-color 0.2s',
};
const linkHover = {
  backgroundColor: '#bee3f8',    // azul muy claro al pasar el ratón
};

// comentario

export default function App() {
  return (
    <>
      <nav style={menuStyle}>
        {['/', '/simulate', '/analytics', '/anomalies', '/metrics'].map((to, idx) => {
          const text = ['Home', 'Simulación', 'Analytics', 'Anomalías', 'Metrics'][idx];
          return (
            <Link
              key={to}
              to={to}
              style={linkStyle}
              onMouseEnter={e => Object.assign(e.currentTarget.style, linkHover)}
              onMouseLeave={e => Object.assign(e.currentTarget.style, { backgroundColor: 'transparent' })}
            >
              {text}
            </Link>
          );
        })}
      </nav>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/simulate" element={<SimulatePage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/anomalies" element={<AnomaliesPage />} />
        <Route path="/metrics" element={<MetricsPage />} />
      </Routes>
    </>
  );
}

