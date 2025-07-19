import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8000';

export default function AnomaliesDashboard() {
  const [mode, setMode] = useState('static'); // 'static' | 'adaptive' | 'classify'
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedSensor, setSelectedSensor] = useState('all'); // Filter by sensor

  const endpoints = {
    static: '/anomalies/static',
    adaptive: '/anomalies/adaptive',
    classify: '/anomalies/classify',
  };

  // Get unique sensors from data for filter dropdown
  const uniqueSensors = ['all', ...Array.from(new Set(data.map(item => item.sensor)))];
  
  // Filter data based on selected sensor
  const filteredData = selectedSensor === 'all' 
    ? data 
    : data.filter(item => item.sensor === selectedSensor);

  // Explanatory texts for each mode
  const explanations = {
    static: {
      title: "Anomalías Estáticas (Umbrales Fijos)",
      description: "Detecta anomalías basadas en umbrales predefinidos que no cambian. Es útil para detectar violaciones de límites operativos específicos como temperaturas fuera de rango, niveles bajos del tanque, o consumo de energía excesivo.",
      howItWorks: "Compara cada lectura con valores fijos: temperatura fuera de ±2°C del setpoint (60°C), nivel por debajo del 20%, potencia por encima de 6.5 kW, o inactividad de flujo por más de 5 minutos."
    },
    adaptive: {
      title: "Anomalías Adaptativas (Umbrales Dinámicos)",
      description: "Detecta anomalías basándose en el comportamiento local de cada sensor. Se adapta automáticamente a los patrones normales de cada sensor, siendo más sensible a cambios súbitos.",
      howItWorks: "Calcula la media y desviación estándar móvil de cada sensor en una ventana de tiempo. Marca como anomalía cualquier valor que se desvíe más de 1.5 desviaciones estándar del comportamiento local."
    },
    classify: {
      title: "Clasificación de Anomalías",
      description: "Categoriza las anomalías adaptativas en tipos específicos para facilitar el diagnóstico y la toma de decisiones. Ayuda a identificar la causa raíz de los problemas.",
      howItWorks: "Aplica reglas de clasificación: 'leakage' para flujo anormalmente alto, 'sensor_error' para errores de temperatura, 'overuse' para consumo de energía excesivo, y 'other' para otros casos."
    }
  };

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE}${endpoints[mode]}`);
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
        const json = await res.json();
        setData(json);
      } catch (e) {
        setError(e.message);
        setData([]);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [mode]);

  return (
    <div style={{ padding: 16 }}>
      <h2>Panel de Anomalías</h2>
      
      {/* Mode Selection */}
      <div style={{ marginBottom: 16 }}>
        <button 
          onClick={() => setMode('static')} 
          disabled={mode==='static'}
          style={{ 
            padding: '8px 16px', 
            marginRight: '8px',
            backgroundColor: mode === 'static' ? '#007bff' : '#f8f9fa',
            color: mode === 'static' ? 'white' : 'black',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            cursor: mode === 'static' ? 'default' : 'pointer'
          }}
        >
          Estáticas
        </button>
        <button 
          onClick={() => setMode('adaptive')} 
          disabled={mode==='adaptive'}
          style={{ 
            padding: '8px 16px', 
            marginRight: '8px',
            backgroundColor: mode === 'adaptive' ? '#007bff' : '#f8f9fa',
            color: mode === 'adaptive' ? 'white' : 'black',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            cursor: mode === 'adaptive' ? 'default' : 'pointer'
          }}
        >
          Adaptativas
        </button>
        <button 
          onClick={() => setMode('classify')} 
          disabled={mode==='classify'}
          style={{ 
            padding: '8px 16px',
            backgroundColor: mode === 'classify' ? '#007bff' : '#f8f9fa',
            color: mode === 'classify' ? 'white' : 'black',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            cursor: mode === 'classify' ? 'default' : 'pointer'
          }}
        >
          Clasificadas
        </button>
      </div>

      {/* Explanatory Section */}
      <div style={{ 
        marginBottom: 20, 
        padding: 16, 
        backgroundColor: '#f8f9fa', 
        borderRadius: 8, 
        border: '1px solid #dee2e6' 
      }}>
        <h3 style={{ marginTop: 0, color: '#495057' }}>{explanations[mode].title}</h3>
        <p style={{ marginBottom: 12, lineHeight: 1.5 }}>
          <strong>Descripción:</strong> {explanations[mode].description}
        </p>
        <p style={{ marginBottom: 0, lineHeight: 1.5 }}>
          <strong>Cómo funciona:</strong> {explanations[mode].howItWorks}
        </p>
      </div>

      {/* Sensor Filter */}
      <div style={{ marginBottom: 16 }}>
        <label style={{ marginRight: 8, fontWeight: 'bold' }}>Filtrar por sensor:</label>
        <select 
          value={selectedSensor} 
          onChange={(e) => setSelectedSensor(e.target.value)}
          style={{ 
            padding: '4px 8px', 
            border: '1px solid #ced4da', 
            borderRadius: 4,
            backgroundColor: 'white'
          }}
        >
          {uniqueSensors.map(sensor => (
            <option key={sensor} value={sensor}>
              {sensor === 'all' ? 'Todos los sensores' : sensor}
            </option>
          ))}
        </select>
        <span style={{ marginLeft: 8, color: '#6c757d', fontSize: '14px' }}>
          ({filteredData.length} anomalías mostradas)
        </span>
      </div>
      {loading && <p>Cargando...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {!loading && !error && (
        <div style={{ maxHeight: 400, overflowY: 'auto', border: '1px solid #dee2e6', borderRadius: 4 }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f8f9fa' }}>
                <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Sensor</th>
                <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Fecha/Hora</th>
                <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Valor</th>
                {mode === 'adaptive' && (
                  <>
                    <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Media</th>
                    <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Desv. Est.</th>
                    <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Z-Score</th>
                  </>
                )}
                {mode === 'classify' && (
                  <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Tipo</th>
                )}
                <th style={{ border: '1px solid #dee2e6', padding: 12, textAlign: 'left' }}>Detalle</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.length === 0 && (
                <tr>
                  <td
                    colSpan={
                      mode === 'adaptive' ? 6 : mode === 'classify' ? 5 : 4
                    }
                    style={{ textAlign: 'center', padding: 16, color: '#6c757d' }}
                  >
                    {selectedSensor === 'all' ? 'No se detectaron anomalías.' : `No hay anomalías para el sensor "${selectedSensor}".`}
                  </td>
                </tr>
              )}
              {filteredData.map((r, idx) => (
                <tr key={idx} style={{ backgroundColor: idx % 2 === 0 ? '#ffffff' : '#f8f9fa' }}>
                  <td style={{ border: '1px solid #dee2e6', padding: 12 }}>
                    <span style={{ 
                      fontWeight: 'bold', 
                      color: r.sensor === 'temperature' ? '#dc3545' : 
                             r.sensor === 'power' ? '#fd7e14' : 
                             r.sensor === 'flow' ? '#20c997' : '#6f42c1'
                    }}>
                      {r.sensor}
                    </span>
                  </td>
                  <td style={{ border: '1px solid #dee2e6', padding: 12 }}>
                    {new Date(r.timestamp).toLocaleString('es-ES')}
                  </td>
                  <td style={{ border: '1px solid #dee2e6', padding: 12, fontWeight: 'bold' }}>
                    {typeof r.value === 'number' ? r.value.toFixed(3) : r.value}
                  </td>
                  {mode === 'adaptive' && (
                    <>
                      <td style={{ border: '1px solid #dee2e6', padding: 12 }}>
                        {r.mean != null ? r.mean.toFixed(3) : '-'}
                      </td>
                      <td style={{ border: '1px solid #dee2e6', padding: 12 }}>
                        {r.std != null ? r.std.toFixed(3) : '-'}
                      </td>
                      <td style={{ border: '1px solid #dee2e6', padding: 12 }}>
                        <span style={{ 
                          fontWeight: 'bold',
                          color: Math.abs(r.z) > 2 ? '#dc3545' : Math.abs(r.z) > 1.5 ? '#fd7e14' : '#28a745'
                        }}>
                          {r.z != null ? r.z.toFixed(2) : '-'}
                        </span>
                      </td>
                    </>
                  )}
                  {mode === 'classify' && (
                    <td style={{ border: '1px solid #dee2e6', padding: 12 }}>
                      <span style={{ 
                        padding: '2px 8px',
                        borderRadius: 4,
                        fontSize: '12px',
                        fontWeight: 'bold',
                        backgroundColor: r.type === 'leakage' ? '#d4edda' :
                                        r.type === 'sensor_error' ? '#f8d7da' :
                                        r.type === 'overuse' ? '#fff3cd' : '#e2e3e5',
                        color: r.type === 'leakage' ? '#155724' :
                               r.type === 'sensor_error' ? '#721c24' :
                               r.type === 'overuse' ? '#856404' : '#6c757d'
                      }}>
                        {r.type || '-'}
                      </span>
                    </td>
                  )}
                  <td style={{ border: '1px solid #dee2e6', padding: 12, fontSize: '14px' }}>
                    {r.detail || r.type || '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
