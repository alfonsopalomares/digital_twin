

import React from 'react';
import { Link } from 'react-router-dom';

/**
 * MainPage: Landing page with links to Simulation and Analytics
 */
export default function MainPage() {
  return (
    <div style={{ padding: 16 }}>
      <h1>Bienvenido al Gemelo Digital</h1>
      <ul>
        <li><Link to="/simulate">Ir a Simulación</Link></li>
        <li><Link to="/analytics">Ir a Analytics</Link></li>
        <li><Link to="/anomalies">Ir a Anomalías</Link></li>
        <li><Link to="/metrics">Ir a Métricas OEE Adaptadas</Link></li>
        <li><Link to="/">Ir a Escenarios de Uso y Configuraciones (FALTA DESARROLLAR)</Link></li>
      </ul>
    </div>
  );
}
