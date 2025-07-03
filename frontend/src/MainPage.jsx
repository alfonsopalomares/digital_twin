/*
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import MainPage from './MainPage';
import AnalyticsPage from './AnalyticsPage';

function App() {
  return (
    <Router>
      <nav style={{ padding: 16, borderBottom: '1px solid #ccc' }}>
        <Link to="/" style={{ marginRight: 16 }}>Home</Link>
        <Link to="/analytics">Analytics</Link>
      </nav>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
      </Routes>
    </Router>
  );
}

export default App;

*/

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
      </ul>
    </div>
  );
}
