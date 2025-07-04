import React, { useState, useEffect } from 'react';
import {
  RadialBarChart,
  RadialBar,
  ResponsiveContainer,
  Legend,
  Tooltip,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';

const API_BASE = 'http://localhost:8000';

const METRICS = [
  { key: 'availability',       label: 'Availability',       unit: '%',    gaugeMax: 100 },
  { key: 'performance',        label: 'Performance',        unit: '%',    gaugeMax: 100 },
  { key: 'quality',            label: 'Quality',            unit: '%',    gaugeMax: 100 },
  { key: 'energy_efficiency',  label: 'Energy Efficiency',  unit: 'kWh/L', gaugeMax: 0.1 },
  { key: 'peak_flow_ratio',    label: 'Peak Flow Ratio',    unit: '',     gaugeMax: 2 },
  { key: 'mtba',               label: 'MTBA',               unit: 'min',  gaugeMax: 60 },
  { key: 'level_uptime',       label: 'Level Uptime',       unit: '%',    gaugeMax: 100 },
  { key: 'response_index',     label: 'Response Index',     unit: 'min',  gaugeMax: 60 },
  { key: 'thermal_variation',  label: 'Thermal Variation',  unit: '°C',  gaugeMax: 10 },
  { key: 'nonproductive_consumption', label: 'Non-prod Consumption', unit: 'kWh', gaugeMax: 1 }
];

export function MetricsDashboard() {
  const [data, setData] = useState({});

  useEffect(() => {
    METRICS.forEach(metric => {
      fetch(`${API_BASE}/metrics/${metric.key}`)
        .then(res => res.json())
        .then(json => setData(prev => ({ ...prev, [metric.key]: json })))
        .catch(err => console.error(`Error loading ${metric.key}:`, err));
    });
  }, []);

  // Prepare radar data for percent metrics
  const radarData = METRICS.filter(m => ['availability','performance','quality','level_uptime'].includes(m.key))
    .map(m => ({
      metric: m.label,
      value: data[m.key] ? data[m.key][Object.keys(data[m.key]).find(k=>k.includes('percent'))] : 0
    }));

  return (
    <div style={{ padding: 16 }}>
      {/* Radar chart for main percent metrics */}
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <RadarChart data={radarData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
            <PolarGrid />
            <PolarAngleAxis dataKey="metric" />
            <PolarRadiusAxis angle={30} domain={[0,100]} />
            <Radar name="Percent" dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Gauges grid */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(200px,1fr))', gap:16, marginTop:32 }}>
        {METRICS.map(metric => {
          const metricData = data[metric.key];
          const raw = metricData ? metricData[Object.keys(metricData)[0]] : 0;
          const percent = metric.gaugeMax > 0 ? (raw / metric.gaugeMax) * 100 : 0;
          const gaugeValue = percent > 100 ? 100 : percent;
          const gaugeData = [{ name: metric.label, value: gaugeValue }];

          return (
            <div key={metric.key} style={{ border:'1px solid #ccc', borderRadius:8, padding:12, background:'#f9f9f9' }}>
              <h4 style={{ margin:0, textAlign:'center' }}>{metric.label}</h4>
              <ResponsiveContainer width="100%" height={150}>
                <RadialBarChart innerRadius="80%" outerRadius="100%" data={gaugeData} startAngle={180} endAngle={0}>
                  <RadialBar background clockWise dataKey="value" fill="#82ca9d" />
                  <Tooltip formatter={value => `${(value/100*metric.gaugeMax).toFixed(2)} ${metric.unit}`} />
                </RadialBarChart>
              </ResponsiveContainer>
              <p style={{ textAlign:'center', marginTop:8 }}>
                {raw.toFixed(2)} {metric.unit}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}