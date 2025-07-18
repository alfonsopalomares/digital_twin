import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  Brush,
  ResponsiveContainer,
} from 'recharts';

// Umbrales ajustables
const TEMP_THRESHOLD       = 85.0;   // °C
const FLOW_IDLE_THRESHOLD  = 0.002;  // L/min
const FLOW_LEAK_THRESHOLD  = 0.05;   // L/min
const LEVEL_LOW_THRESHOLD  = 0.20;   // proporción
const POWER_HIGH_THRESHOLD = 6.5;    // kW

const API_BASE = 'http://localhost:8000';

// Colores por sensor
const COLORS = {
  temperature: '#ff7300',
  flow:        '#387908',
  level:       '#8884d8',
  power:       '#82ca9d',
};

/**
 * AnalyticsDashboard: muestra gráficos de cada sensor con zoom/pan y umbrales
 */
export default function AnalyticsDashboard() {
  const [readings, setReadings] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(`${API_BASE}/readings/readings`);
        const all = await res.json();
        // ordenar por timestamp
        const sorted = all.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        setReadings(sorted);
      } catch (err) {
        console.error('Error fetching readings:', err);
      }
    }
    fetchData();
  }, []);

  // Genera datos filtrados por sensor
  const getSensorData = sensor =>
    readings
      .filter(r => r.sensor === sensor)
      .map(r => ({ timestamp: r.timestamp, value: r.value }));

  // Configuración de umbrales por sensor
  const thresholdConfig = {
    temperature: { value: TEMP_THRESHOLD,  color: 'red',    label: `Umbral ${TEMP_THRESHOLD}°C` },
    flow:        { low: FLOW_IDLE_THRESHOLD, color: 'orange', labelLow: `Inactividad ${FLOW_IDLE_THRESHOLD} L/min`, high: FLOW_LEAK_THRESHOLD, labelHigh: `Fuga ${FLOW_LEAK_THRESHOLD} L/min` },
    level:       { value: LEVEL_LOW_THRESHOLD, color: 'blue',   label: `Nivel mínimo ${LEVEL_LOW_THRESHOLD * 100}%` },
    power:       { value: POWER_HIGH_THRESHOLD, color: 'purple', label: `Consumo alto ${POWER_HIGH_THRESHOLD} kW` },
  };

  // Componente genérico de gráfico
  const SensorChart = ({ sensor }) => {
    const data = getSensorData(sensor);
    const cfg  = thresholdConfig[sensor];
    return (
      <div style={{ width: '100%', height: 300, margin: '24px 0' }}>
        <h3 style={{ textAlign: 'center', textTransform: 'capitalize' }}>{sensor}</h3>
        <ResponsiveContainer>
          <LineChart data={data} margin={{ top: 10, right: 30, left: 20, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" tickFormatter={ts => new Date(ts).toLocaleTimeString()} />
            <YAxis />
            <Tooltip labelFormatter={ts => new Date(ts).toLocaleString()} />
            {/* Umbrales */}
            {sensor === 'flow' ? (
              <>              
                <ReferenceLine y={cfg.low} stroke={cfg.color} strokeDasharray="4 4" label={{ position: 'bottom', value: cfg.labelLow, fill: cfg.color }} />
                <ReferenceLine y={cfg.high} stroke="red"     strokeDasharray="4 4" label={{ position: 'top',    value: cfg.labelHigh, fill: 'red'     }} />
              </>
            ) : (
              <ReferenceLine y={cfg.value} stroke={cfg.color} strokeDasharray="4 4" label={{ position: 'top', value: cfg.label, fill: cfg.color }} />
            )}
            <Line type="monotone" dataKey="value" stroke={COLORS[sensor]} dot={false} />
            <Brush dataKey="timestamp" height={20} stroke={COLORS[sensor]} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  };

  return (
    <div style={{ padding: 16 }}>
      {['temperature', 'flow', 'level', 'power'].map(s => (
        <SensorChart key={s} sensor={s} />
      ))}
    </div>
  );
}
