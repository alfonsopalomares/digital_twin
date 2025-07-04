import React, { useState, useEffect } from 'react';
import { Table } from 'react-bootstrap';

/**
 * AnomaliesDashboard muestra anomalías agrupadas por sensor.
 */
export default function AnomaliesDashboard() {
  const [anomalies, setAnomalies] = useState([]);
  const API_BASE = 'http://localhost:8000';

  useEffect(() => {
    async function fetchAnomalies() {
      try {
        const res = await fetch(`${API_BASE}/anomalies`);
        const data = await res.json();
        setAnomalies(data);
      } catch (err) {
        console.error('Error fetching anomalies:', err);
      }
    }
    fetchAnomalies();
  }, []);

  // Agrupar anomalías por sensor
  const grouped = anomalies.reduce((acc, curr) => {
    acc[curr.sensor] = acc[curr.sensor] || [];
    acc[curr.sensor].push(curr);
    return acc;
  }, {});

  // Mapeo de colores por tipo de anomalía
  const colorMap = {
    Overtemperature: '#ff4d4f',
    Inactivity:      '#faad14',
    LowLevel:        '#1890ff',
    HighPower:       '#722ed1',
  };
  return (
    <div>
      <div style={{ padding: 16 }}>
        <h2>Anomalías Detectadas</h2>

        {Object.keys(grouped).length === 0 && (
          <p>No se detectaron anomalías.</p>
        )}

        {/* Grid de sensores: 3 columnas */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 16 }}>
          {Object.entries(grouped).map(([sensor, list]) => (
            <div key={sensor} style={{ border: '1px solid #ccc', borderRadius: 4, padding: 8, height: 400, overflowY: 'auto' }}>
              <h4 style={{ textTransform: 'capitalize', marginTop: 0 }}>{sensor}</h4>
              {list.length > 0 ? (
                <Table striped bordered hover size="sm" responsive>
                  <thead>
                    <tr>
                      <th style={{ minWidth: 80 }}>Timestamp</th>
                      <th>Tipo</th>
                      <th>Detalle</th>
                    </tr>
                  </thead>
                  <tbody>
                    {list.map((a, idx) => (
                      <tr key={idx} style={{ backgroundColor: (colorMap[a.type] || '#ddd') + '20' }}>
                        <td>{new Date(a.timestamp).toLocaleString()}</td>
                        <td style={{ color: colorMap[a.type], fontWeight: 'bold' }}>{a.type}</td>
                        <td>{a.detail}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              ) : (
                <p>No hay anomalías para este sensor.</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
