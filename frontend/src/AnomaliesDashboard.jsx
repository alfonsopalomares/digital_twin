import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8000';

export default function AnomaliesDashboard() {
  const [mode, setMode] = useState('static'); // 'static' | 'adaptive' | 'classify'
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const endpoints = {
    static: '/anomalies/static',
    adaptive: '/anomalies/adaptive',
    classify: '/anomalies/classify',
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
      <h2>Anomalies Dashboard</h2>
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setMode('static')} disabled={mode==='static'}>Static</button>
        <button onClick={() => setMode('adaptive')} disabled={mode==='adaptive'} style={{ margin: '0 8px' }}>Adaptive</button>
        <button onClick={() => setMode('classify')} disabled={mode==='classify'}>Classify</button>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && !error && (
        <div style={{ maxHeight: 300, overflowY: 'auto', border: '1px solid #ccc' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ border: '1px solid #ddd', padding: 8 }}>Sensor</th>
                <th style={{ border: '1px solid #ddd', padding: 8 }}>Timestamp</th>
                <th style={{ border: '1px solid #ddd', padding: 8 }}>Value</th>
                {mode === 'adaptive' && (
                  <>
                    <th style={{ border: '1px solid #ddd', padding: 8 }}>Mean</th>
                    <th style={{ border: '1px solid #ddd', padding: 8 }}>Std</th>
                    <th style={{ border: '1px solid #ddd', padding: 8 }}>Z-Score</th>
                  </>
                )}
                {mode === 'classify' && (
                  <th style={{ border: '1px solid #ddd', padding: 8 }}>Type</th>
                )}
                <th style={{ border: '1px solid #ddd', padding: 8 }}>Detail</th>
              </tr>
            </thead>
            <tbody>
              {data.length === 0 && (
                <tr>
                  <td
                    colSpan={
                      mode === 'adaptive' ? 6 : mode === 'classify' ? 5 : 4
                    }
                    style={{ textAlign: 'center', padding: 8 }}
                  >
                    No anomalies detected.
                  </td>
                </tr>
              )}
              {data.map((r, idx) => (
                <tr key={idx}>
                  <td style={{ border: '1px solid #ddd', padding: 8 }}>{r.sensor}</td>
                  <td style={{ border: '1px solid #ddd', padding: 8 }}>
                    {new Date(r.timestamp).toLocaleString()}
                  </td>
                  <td style={{ border: '1px solid #ddd', padding: 8 }}>{r.value}</td>
                  {mode === 'adaptive' && (
                    <>
                      <td style={{ border: '1px solid #ddd', padding: 8 }}>
                        {r.mean != null ? r.mean.toFixed(2) : '-'}
                      </td>
                      <td style={{ border: '1px solid #ddd', padding: 8 }}>
                        {r.std != null ? r.std.toFixed(2) : '-'}
                      </td>
                      <td style={{ border: '1px solid #ddd', padding: 8 }}>
                        {r.z != null ? r.z.toFixed(2) : '-'}
                      </td>
                    </>
                  )}
                  {mode === 'classify' && (
                    <td style={{ border: '1px solid #ddd', padding: 8 }}>
                      {r.type || '-'}
                    </td>
                  )}
                  <td style={{ border: '1px solid #ddd', padding: 8 }}>
                    {r.detail || ''}
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
