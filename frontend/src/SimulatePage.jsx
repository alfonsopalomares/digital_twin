
import React, { useState, useEffect, useMemo } from 'react';

// Gauge SVG for water level
function DispenserGauge({ levelPercent }) {
  const width = 100;
  const height = 200;
  const waterHeight = (levelPercent / 100) * (height - 20);
  const waterY = height - 10 - waterHeight;

  return (
    <svg width={width} height={height} style={{ border: '2px solid #333', borderRadius: 4 }}>
      <rect x={10} y={10} width={width - 20} height={height - 20} fill="none" stroke="#333" strokeWidth={2} rx={4} />
      <rect x={10} y={waterY} width={width - 20} height={waterHeight} fill="#4aadff" rx={4} />
      <text x={width / 2} y={height / 2} textAnchor="middle" fill="#333" fontSize={16} fontFamily="Arial">
        {Math.round(levelPercent)}%
      </text>
    </svg>
  );
}

// Simple switch component
function Switch({ checked, onChange }) {
  const containerStyle = {
    width: 40,
    height: 20,
    borderRadius: 10,
    backgroundColor: checked ? '#4caf50' : '#ccc',
    position: 'relative',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  };
  const knobStyle = {
    width: 18,
    height: 18,
    borderRadius: '50%',
    background: '#fff',
    position: 'absolute',
    top: 1,
    left: checked ? 21 : 1,
    transition: 'left 0.3s',
  };
  return (
    <div style={containerStyle} onClick={() => onChange(!checked)} role="switch" aria-checked={checked}>
      <div style={knobStyle} />
    </div>
  );
}

function SimulatePage() {
  const lang = navigator.language.startsWith('es') ? 'es' : 'en';
  const dict = {
    controls: { en: 'Controls', es: 'Controles' },
    simulate_save: { en: 'Simulate & Save', es: 'Simular y Guardar' },
    hours: { en: 'Hours', es: 'Horas' },
    users: { en: 'Users', es: 'Usuarios' },
    all_sensors_data: { en: 'All Sensors Data', es: 'Todos los sensores' },
    sensor_info: { en: 'Sensor information', es: 'Información de los sensores' },
  };
  const sensorLabels = {
    temperature: { en: 'Temperature', es: 'Temperatura' },
    flow: { en: 'Flow', es: 'Flujo' },
    level: { en: 'Level', es: 'Nivel' },
    power: { en: 'Power', es: 'Energía' },
  };
  const sensorUnits = {
    temperature: '°C',
    flow: 'L/min',
    level: '%',
    power: 'kW',
  };
  const t = key => (dict[key] ? dict[key][lang] : key);
  const labelSensor = key => (sensorLabels[key] ? sensorLabels[key][lang] : key);
  const getSensorUnit = key => sensorUnits[key] || '';
  const formatSensorValue = (sensor, value) => {
    if (sensor === 'level') {
      return `${(value * 100).toFixed(1)} ${getSensorUnit(sensor)}`;
    }
    return `${value} ${getSensorUnit(sensor)}`;
  };

  const [readings, setReadings] = useState([]);
  const [hours, setHours] = useState(8);
  const [users, setUsers] = useState(10);
  const [notification, setNotification] = useState('');
  const [bannerVisible, setBannerVisible] = useState(false);
  const [showAllReadings, setShowAllReadings] = useState(true);
  const [showSensorToggles, setShowSensorToggles] = useState({});
  const [menuOpen, setMenuOpen] = useState(false);
  const [sortConfig, setSortConfig] = useState({ key: 'timestamp', direction: 'desc' });
  const apiBase = 'http://localhost:8000';

  // Styles
  const bannerStyle = {
    position: 'fixed', top: 16, left: '50%',
    transform: bannerVisible ? 'translate(-50%, 0)' : 'translate(-50%, -20px)',
    backgroundColor: '#d4edda', color: '#155724', padding: '10px 20px', borderRadius: 4,
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)', zIndex: 1000,
    opacity: bannerVisible ? 1 : 0, transition: 'opacity 0.5s ease, transform 0.5s ease',
  };
  const sidebarStyle = {
    position: 'fixed', top: 0, right: 0,
    width: menuOpen ? 220 : 40, height: '100%',
    backgroundColor: '#f9f9f9', borderLeft: '1px solid #ccc', boxSizing: 'border-box',
    padding: menuOpen ? 16 : 8, transition: 'width 0.3s ease', overflow: 'hidden', zIndex: 999,
  };
  const hamburgerStyle = { fontSize: 24, cursor: 'pointer', background: 'none', border: 'none' };
  const containerStyle = { display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, padding: 16 };
  const panelStyle = { border: '1px solid #ccc', borderRadius: 4, padding: 16 };
  const inputStyle = { width: '100%', padding: 6, marginBottom: 8, boxSizing: 'border-box' };
  const buttonStyle = { width: '100%', padding: 8, margin: '8px 0', border: 'none', borderRadius: 4, cursor: 'pointer', textAlign: 'center' };
  const tableContainerStyle = { height: 200, overflowY: 'auto' };
  const tableStyle = { width: '100%', borderCollapse: 'collapse' };
  const thTdStyle = { border: '1px solid #ddd', padding: 8, textAlign: 'left' };

  // Format timestamp
  const formatTimestamp = ts => new Date(ts).toLocaleString(lang);

  // Current water level percentage
  const currentLevel = useMemo(() => {
    const lvl = readings.find(r => r.sensor === 'level');
    return lvl ? lvl.value * 100 : 0;
  }, [readings]);

  // Fetch readings on mount
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${apiBase}/readings/readings`);
        setReadings(await res.json());
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  // Initialize toggles when readings change
  useEffect(() => {
    const sensors = Array.from(new Set(readings.map(r => r.sensor)));
    setShowSensorToggles(prev => {
      const upd = { ...prev };
      sensors.forEach(s => {
        if (!(s in upd)) upd[s] = true;
      });
      return upd;
    });
  }, [readings]);

  // Simulate usage
  const handleSimulate = async () => {
    const now = new Date();
    try {
      await fetch(`${apiBase}/simulate/simulate?hours=${hours}&users=${users}`, { method: 'POST' });
      const res = await fetch(`${apiBase}/readings/readings`);
      setReadings(await res.json());
      const utc = now.toISOString();
      const local = now.toLocaleString(lang);
      setNotification(`${t('simulate_save')} - UTC: ${utc} | Local: ${local}`);
      setBannerVisible(true);
      setTimeout(() => setBannerVisible(false), 1500);
      setTimeout(() => setNotification(''), 2000);
    } catch (err) {
      console.error(err);
    }
  };

  // Clear all data
  const handleClear = async () => {
    try {
      await fetch(`${apiBase}/readings/readings`, { method: 'DELETE' });
      setReadings([]);
      setNotification(lang === 'es' ? 'Datos eliminados' : 'Data cleared');
      setBannerVisible(true);
      setTimeout(() => setBannerVisible(false), 1500);
      setTimeout(() => setNotification(''), 2000);
    } catch (err) {
      console.error(err);
    }
  };

  // Sort logic
  const handleSort = key => {
    let dir = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') dir = 'desc';
    setSortConfig({ key, direction: dir });
  };
  const sortedReadings = useMemo(
    () =>
      [...readings].sort((a, b) => {
        if (sortConfig.key === 'value') {
          return sortConfig.direction === 'asc' ? a.value - b.value : b.value - a.value;
        }
        const diff = new Date(a.timestamp) - new Date(b.timestamp);
        return sortConfig.direction === 'asc' ? diff : -diff;
      }),
    [readings, sortConfig]
  );

  const sensorNames = Array.from(new Set(readings.map(r => r.sensor)));

  return (
    <div style={{ padding: 16 }}>
    <h1>Simulación</h1>
      <h1 style={{ textAlign: 'center', fontSize: 24, margin: '16px 0' }}>
        {lang === 'es' ? 'Gemelo Digital - Panel de Monitoreo' : 'Digital Twin - Monitoring Dashboard'}
      </h1>
      {notification && <div style={bannerStyle}>{notification}</div>}
      <div style={sidebarStyle}>
        <button style={hamburgerStyle} onClick={() => setMenuOpen(!menuOpen)}>
          ☰
        </button>
        {menuOpen && (
          <div>
            <h3 style={{ marginTop: 0 }}>{t('sensor_info')}</h3>
            <div style={{ display: 'flex', alignItems: 'center', margin: '8px 0' }}>
              <Switch checked={showAllReadings} onChange={setShowAllReadings} />
              <span style={{ marginLeft: 8 }}>{t('all_sensors_data')}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'center', margin: '16px 0' }}>
              <DispenserGauge levelPercent={currentLevel} />
            </div>
            <div style={{ margin: '16px 0' }}>
              <button
                style={{ width: '100%', backgroundColor: 'red', color: '#fff', padding: 8, border: 'none', borderRadius: 4, cursor: 'pointer' }}
                onClick={handleClear}
              >
                {lang === 'es' ? 'Limpiar Datos' : 'Clear Data'}
              </button>
            </div>
            {sensorNames.map(s => (
              <div key={s} style={{ display: 'flex', alignItems: 'center', margin: '8px 0' }}>
                <Switch checked={showSensorToggles[s]} onChange={checked => setShowSensorToggles(prev => ({ ...prev, [s]: checked }))} />
                <span style={{ marginLeft: 8 }}>{labelSensor(s)} ({getSensorUnit(s)})</span>
              </div>
            ))}
          </div>
        )}
      </div>
      <div style={{ marginRight: menuOpen ? 240 : 56 }}>
        <div style={containerStyle}>
          <div style={panelStyle}>
            <h2>{t('controls')}</h2>
            <label>{t('hours')}</label>
            <input type="number" min={1} value={hours} onChange={e => setHours(+e.target.value)} style={inputStyle} />
            <label>{t('users')}</label>
            <input type="number" min={1} value={users} onChange={e => setUsers(+e.target.value)} style={inputStyle} />
            <button style={{ ...buttonStyle, backgroundColor: '#007bff', color: '#fff' }} onClick={handleSimulate}>
              {t('simulate_save')}
            </button>
          </div>
          {showAllReadings && (
            <div style={panelStyle}>
              <h2>{t('all_sensors_data')}</h2>
              <div style={tableContainerStyle}>
                <table style={tableStyle}>
                  <thead>
                    <tr>
                      {['sensor', 'timestamp', 'value'].map(key => (
                        <th key={key} style={{ ...thTdStyle, cursor: 'pointer' }} onClick={() => handleSort(key)}>
                          {t(key)} {sortConfig.key === key ? (sortConfig.direction === 'asc' ? '▲' : '▼') : ''}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {sortedReadings.map((r, i) => (
                      <tr key={i}>
                        <td style={thTdStyle}>{labelSensor(r.sensor)} ({getSensorUnit(r.sensor)})</td>
                        <td style={thTdStyle}>{formatTimestamp(r.timestamp)}</td>
                        <td style={thTdStyle}>{formatSensorValue(r.sensor, r.value)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          {sensorNames.map(s =>
            showSensorToggles[s] ? (
              <div key={s} style={panelStyle}>
                <h2>
                  {t('sensor')}: {labelSensor(s)} ({getSensorUnit(s)})
                </h2>
                <div style={tableContainerStyle}>
                  <table style={tableStyle}>
                    <thead>
                      <tr>
                        <th style={thTdStyle}>{t('timestamp')}</th>
                        <th style={thTdStyle}>{t('value')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sortedReadings
                        .filter(r => r.sensor === s)
                        .map((r, idx) => (
                          <tr key={idx}>
                            <td style={thTdStyle}>{formatTimestamp(r.timestamp)}</td>
                            <td style={thTdStyle}>{formatSensorValue(s, r.value)}</td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : null
          )}
        </div>
      </div>
    </div>
  );
}

export default SimulatePage;

