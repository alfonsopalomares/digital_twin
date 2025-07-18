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
  { key: 'availability',       gaugeMax: 100, isPercentage: true },
  { key: 'performance',        gaugeMax: 2, isPercentage: false },
  { key: 'quality',            gaugeMax: 100, isPercentage: true },
  { key: 'energy_efficiency',  gaugeMax: 0.1, isPercentage: false },
  { key: 'peak_flow_ratio',    gaugeMax: 2, isPercentage: false },
  { key: 'mtba',               gaugeMax: 60, isPercentage: false },
  { key: 'level_uptime',       gaugeMax: 100, isPercentage: true },
  { key: 'response_index',     gaugeMax: 60, isPercentage: false },
  { key: 'thermal_variation',  gaugeMax: 10, isPercentage: false },
  { key: 'nonproductive_consumption', gaugeMax: 1, isPercentage: false }
];

export function MetricsDashboard() {
  const lang = navigator.language.startsWith('es') ? 'es' : 'en';
  
  // Dictionary for internationalization
  const dict = {
    // Metadata labels
    samples: { en: 'Samples', es: 'Muestras' },
    expected: { en: 'Expected', es: 'Esperado' },
    users: { en: 'Users', es: 'Usuarios' },
    hours: { en: 'Hours', es: 'Horas' },
    percent: { en: 'Percent', es: 'Porcentaje' },
    
    // Page titles
    metrics_dashboard: { en: 'Metrics Dashboard', es: 'Panel de Métricas' },
    main_percent_metrics: { en: 'Main Percent Metrics', es: 'Métricas Principales de Porcentaje' },
    
    // Loading and error messages
    loading: { en: 'Loading metrics...', es: 'Cargando métricas...' },
    error: { en: 'Error loading metric', es: 'Error al cargar métrica' },
    
    // Metric titles
    availability: { en: 'Availability', es: 'Disponibilidad' },
    performance: { en: 'Performance', es: 'Rendimiento' },
    quality: { en: 'Quality', es: 'Calidad' },
    energy_efficiency: { en: 'Energy Efficiency', es: 'Eficiencia Energética' },
    thermal_variation: { en: 'Thermal Variation', es: 'Variación Térmica' },
    peak_flow_ratio: { en: 'Peak Flow Ratio', es: 'Relación de Flujo Máximo' },
    mtba: { en: 'Mean Time Between Adaptive Anomalies', es: 'Tiempo Medio Entre Anomalías Adaptativas' },
    level_uptime: { en: 'Level Uptime', es: 'Tiempo Activo de Nivel' },
    response_index: { en: 'Response Index', es: 'Índice de Respuesta' },
    nonproductive_consumption: { en: 'Nonproductive Consumption', es: 'Consumo No Productivo' },
    mtbf: { en: 'Mean Time Between Failures', es: 'Tiempo Medio Entre Fallas' },
    quality_full: { en: 'Full Quality', es: 'Calidad Completa' },
    response_time: { en: 'Average Response Time', es: 'Tiempo de Respuesta Promedio' },
    failures_count: { en: 'Failures Count', es: 'Conteo de Fallas' },
    usage_rate: { en: 'Usage Rate', es: 'Tasa de Uso' }
  };
  
  const t = key => (dict[key] ? dict[key][lang] : key);
  
  // Function to get translated metric title
  const getTranslatedTitle = (metricKey) => {
    return t(metricKey) || metricKey;
  };
  
  // Function to calculate appropriate gauge range
  const calculateGaugeRange = (metric, value) => {
    if (metric.isPercentage) {
      // For percentage metrics, use 0-100 range
      return { min: 0, max: 100, current: value };
    } else {
      // For non-percentage metrics, use a dynamic range based on the value
      const max = Math.max(metric.gaugeMax, value * 1.2); // Add 20% buffer
      return { min: 0, max: max, current: value };
    }
  };
  
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const promises = METRICS.map(metric => 
      fetch(`${API_BASE}/metrics/${metric.key}`)
        .then(res => res.json())
        .then(json => ({ key: metric.key, data: json }))
        .catch(err => {
          console.error(`Error loading ${metric.key}:`, err);
          return { key: metric.key, data: null };
        })
    );
    
    Promise.all(promises)
      .then(results => {
        const newData = {};
        results.forEach(({ key, data }) => {
          if (data) newData[key] = data;
        });
        setData(newData);
        setLoading(false);
      });
  }, []); // Solo se ejecuta una vez al montar el componente

  // Prepare radar data for percent metrics only
  const radarData = METRICS.filter(m => ['availability','quality','level_uptime'].includes(m.key))
    .map(m => {
      const metricData = data[m.key];
      return {
        metric: getTranslatedTitle(m.key), // Use translated title
        value: metricData?.value || 0
      };
    });

  if (loading) {
    return (
      <div style={{ padding: 16, textAlign: 'center' }}>
        <h1 style={{ fontSize: 24, margin: '16px 0' }}>
          {t('metrics_dashboard')}
        </h1>
        <p>{t('loading')}</p>
      </div>
    );
  }

  return (
    <div style={{ padding: 16 }}>
      <h1 style={{ textAlign: 'center', fontSize: 24, margin: '16px 0' }}>
        {t('metrics_dashboard')}
      </h1>
      {/* Radar chart for main percent metrics */}
      <h3 style={{ textAlign: 'center', margin: '16px 0' }}>
        {t('main_percent_metrics')}
      </h3>
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <RadarChart data={radarData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
            <PolarGrid />
            <PolarAngleAxis dataKey="metric" />
            <PolarRadiusAxis angle={30} domain={[0,100]} />
            <Radar name={t('percent')} dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Gauges grid */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(200px,1fr))', gap:16, marginTop:32 }}>
        {METRICS.map(metric => {
          const metricData = data[metric.key];
          const raw = metricData?.value || 0;
          const title = getTranslatedTitle(metric.key); // Use translated title instead of backend title
          const unit = metricData?.unit || '';
          
          const range = calculateGaugeRange(metric, raw);
          const percent = range.max > 0 ? (raw / range.max) * 100 : 0;
          const gaugeValue = Math.min(percent, 100); // Cap at 100%
          const gaugeData = [{ name: title, value: gaugeValue }];

          return (
            <div key={metric.key} style={{ border:'1px solid #ccc', borderRadius:8, padding:12, background:'#f9f9f9' }}>
              <h4 style={{ margin:0, textAlign:'center' }}>{title}</h4>
              <ResponsiveContainer width="100%" height={150}>
                <RadialBarChart innerRadius="80%" outerRadius="100%" data={gaugeData} startAngle={180} endAngle={0}>
                  <RadialBar background clockWise dataKey="value" fill="#82ca9d" />
                  <Tooltip formatter={value => `${(value/100*range.max).toFixed(2)} ${unit}`} />
                </RadialBarChart>
              </ResponsiveContainer>
              <p style={{ textAlign:'center', marginTop:8 }}>
                {raw.toFixed(2)} {unit}
                {!metric.isPercentage && (
                  <span style={{ fontSize: '12px', color: '#666' }}>
                    {' '}(0 - {range.max.toFixed(2)})
                  </span>
                )}
              </p>
              {/* Additional metadata */}
              {metricData && (
                <div style={{ fontSize: '12px', color: '#666', textAlign: 'center', marginTop: 4 }}>
                  {metricData.samples && <div>{t('samples')}: {metricData.samples}</div>}
                  {metricData.expected_value && <div>{t('expected')}: {metricData.expected_value.toFixed(2)} {unit}</div>}
                  {metricData.users && <div>{t('users')}: {metricData.users}</div>}
                  {metricData.hours && <div>{t('hours')}: {metricData.hours}</div>}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}