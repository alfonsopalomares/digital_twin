import React, { useState, useEffect, useRef } from 'react';
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
  const hasLoadedRef = useRef(false);

  useEffect(() => {
    if (hasLoadedRef.current) return; // Prevent multiple calls
    
    console.log('MetricsDashboard useEffect triggered');
    hasLoadedRef.current = true;
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
          // For percentage metrics, use the raw value directly as gauge percentage
          // For non-percentage metrics, calculate the percentage based on range
          const gaugeValue = metric.isPercentage ? Math.min(raw, 100) : Math.min((raw / range.max) * 100, 100);
          const gaugeData = [{ name: title, value: gaugeValue }];
          
          // Debug logging for quality metric
          if (metric.key === 'quality') {
            console.log('Quality Debug:', {
              raw,
              isPercentage: metric.isPercentage,
              gaugeValue,
              range
            });
          }

          return (
            <div key={metric.key} style={{ border:'1px solid #ccc', borderRadius:8, padding:12, background:'#f9f9f9' }}>
              <h4 style={{ margin:0, textAlign:'center' }}>{title}</h4>
              <ResponsiveContainer width="100%" height={150}>
                <RadialBarChart innerRadius="80%" outerRadius="100%" data={gaugeData} startAngle={180} endAngle={0}>
                  <RadialBar 
                    background 
                    clockWise 
                    dataKey="value" 
                    fill={
                      metric.key === 'quality' ? "#ff7300" :
                      metric.key === 'energy_efficiency' && metricData?.efficiency_status === 'critical' ? "#dc3545" :
                      metric.key === 'energy_efficiency' && metricData?.efficiency_status === 'poor' ? "#ffc107" :
                      metric.key === 'energy_efficiency' && metricData?.efficiency_status === 'good' ? "#17a2b8" :
                      metric.key === 'energy_efficiency' && metricData?.efficiency_status === 'excellent' ? "#28a745" :
                      metric.key === 'thermal_variation' && metricData?.variation_status === 'excellent' ? "#28a745" :
                      metric.key === 'thermal_variation' && metricData?.variation_status === 'good' ? "#17a2b8" :
                      metric.key === 'thermal_variation' && metricData?.variation_status === 'acceptable' ? "#ffc107" :
                      metric.key === 'thermal_variation' && metricData?.variation_status === 'poor' ? "#dc3545" :
                      metric.key === 'peak_flow_ratio' && metricData?.ratio_status === 'excellent' ? "#28a745" :
                      metric.key === 'peak_flow_ratio' && metricData?.ratio_status === 'good' ? "#17a2b8" :
                      metric.key === 'peak_flow_ratio' && metricData?.ratio_status === 'acceptable' ? "#ffc107" :
                      metric.key === 'peak_flow_ratio' && metricData?.ratio_status === 'excessive' ? "#dc3545" :
                      metric.key === 'mtba' && metricData?.mtba_status === 'excellent' ? "#28a745" :
                      metric.key === 'mtba' && metricData?.mtba_status === 'good' ? "#17a2b8" :
                      metric.key === 'mtba' && metricData?.mtba_status === 'acceptable' ? "#ffc107" :
                      metric.key === 'mtba' && metricData?.mtba_status === 'poor' ? "#dc3545" :
                      metric.key === 'level_uptime' && metricData?.uptime_status === 'excellent' ? "#28a745" :
                      metric.key === 'level_uptime' && metricData?.uptime_status === 'good' ? "#17a2b8" :
                      metric.key === 'level_uptime' && metricData?.uptime_status === 'acceptable' ? "#ffc107" :
                      metric.key === 'level_uptime' && metricData?.uptime_status === 'poor' ? "#dc3545" :
                      metric.key === 'availability' && metricData?.availability_status === 'excellent' ? "#28a745" :
                      metric.key === 'availability' && metricData?.availability_status === 'good' ? "#17a2b8" :
                      metric.key === 'availability' && metricData?.availability_status === 'acceptable' ? "#ffc107" :
                      metric.key === 'availability' && metricData?.availability_status === 'poor' ? "#dc3545" :
                      metric.key === 'performance' && metricData?.performance_status === 'excellent' ? "#28a745" :
                      metric.key === 'performance' && metricData?.performance_status === 'good' ? "#17a2b8" :
                      metric.key === 'performance' && metricData?.performance_status === 'acceptable' ? "#ffc107" :
                      metric.key === 'performance' && metricData?.performance_status === 'poor' ? "#fd7e14" :
                      metric.key === 'performance' && metricData?.performance_status === 'critical' ? "#dc3545" :
                      metric.key === 'quality' && metricData?.quality_status === 'excellent' ? "#28a745" :
                      metric.key === 'quality' && metricData?.quality_status === 'good' ? "#17a2b8" :
                      metric.key === 'quality' && metricData?.quality_status === 'acceptable' ? "#ffc107" :
                      metric.key === 'quality' && metricData?.quality_status === 'poor' ? "#dc3545" :
                      "#82ca9d"
                    } 
                  />
                  <Tooltip formatter={value => `${raw.toFixed(2)} ${unit}`} />
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
                  {/* Enhanced quality metadata */}
                  {metric.key === 'quality' && metricData.setpoint && (
                    <>
                      <div>Setpoint: {metricData.setpoint}°C</div>
                      <div>Tolerance: ±{metricData.tolerance_band/2}°C</div>
                      <div>Average: {metricData.avg_temp}°C</div>
                      <div>Range: {metricData.min_temp}°C - {metricData.max_temp}°C</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.quality_status === 'excellent' ? '#28a745' :
                               metricData.quality_status === 'good' ? '#17a2b8' :
                               metricData.quality_status === 'acceptable' ? '#ffc107' : '#dc3545'
                      }}>
                        Status: {metricData.quality_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Variability: {metricData.temp_variability}%</div>
                      <div>Avg Deviation: {metricData.avg_deviation}°C</div>
                      <div>Max Deviation: {metricData.max_deviation}°C</div>
                      <div>Low Temp: {metricData.low_percent}% ({metricData.low_count} readings)</div>
                      <div>Within Range: {metricData.within_percent}% ({metricData.within_count} readings)</div>
                      <div>High Temp: {metricData.high_percent}% ({metricData.high_count} readings)</div>
                      {metricData.quality_status === 'poor' && (
                        <div style={{ color: '#dc3545', fontWeight: 'bold' }}>
                          ⚠️ Poor temperature control
                        </div>
                      )}
                      {metricData.max_deviation > metricData.tolerance_band/2 && (
                        <div style={{ color: '#ffc107', fontWeight: 'bold' }}>
                          ⚠️ Maximum deviation exceeds tolerance
                        </div>
                      )}
                    </>
                  )}
                  {/* Enhanced energy efficiency metadata */}
                  {metric.key === 'energy_efficiency' && metricData.expected_value && (
                    <>
                      <div>Expected: {metricData.expected_value} kWh/L</div>
                      <div>Tolerance: ±{metricData.tolerance_band/2} kWh/L</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.efficiency_status === 'excellent' ? '#28a745' :
                               metricData.efficiency_status === 'good' ? '#17a2b8' :
                               metricData.efficiency_status === 'poor' ? '#ffc107' : '#dc3545'
                      }}>
                        Status: {metricData.efficiency_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Ratio: {metricData.efficiency_ratio}x expected</div>
                      <div>Consumption: {metricData.total_kwh} kWh</div>
                      <div>Volume: {metricData.total_liters} L</div>
                      {metricData.within_tolerance === 0 && (
                        <div style={{ color: '#dc3545', fontWeight: 'bold' }}>
                          ⚠️ Outside tolerance
                        </div>
                      )}
                    </>
                  )}
                  {/* Enhanced thermal variation metadata */}
                  {metric.key === 'thermal_variation' && metricData.avg_temperature && (
                    <>
                      <div>Average: {metricData.avg_temperature}°C</div>
                      <div>Range: {metricData.min_temperature}°C - {metricData.max_temperature}°C</div>
                      <div>Setpoint: {metricData.setpoint}°C</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.variation_status === 'excellent' ? '#28a745' :
                               metricData.variation_status === 'good' ? '#17a2b8' :
                               metricData.variation_status === 'acceptable' ? '#ffc107' : '#dc3545'
                      }}>
                        Status: {metricData.variation_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Within tolerance: {metricData.within_tolerance_percent}%</div>
                      <div>Deviation: {metricData.setpoint_deviation}°C</div>
                    </>
                  )}
                  {/* Enhanced peak flow ratio metadata */}
                  {metric.key === 'peak_flow_ratio' && metricData.max_flow && (
                    <>
                      <div>Max Flow: {metricData.max_flow} L/min</div>
                      <div>Avg Flow: {metricData.avg_flow} L/min</div>
                      <div>Nominal: {metricData.nominal_flow} L/min</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.ratio_status === 'excellent' ? '#28a745' :
                               metricData.ratio_status === 'good' ? '#17a2b8' :
                               metricData.ratio_status === 'acceptable' ? '#ffc107' : '#dc3545'
                      }}>
                        Status: {metricData.ratio_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Above nominal: {metricData.above_nominal_percent}%</div>
                      <div>Variability: {metricData.flow_variability}%</div>
                      {metricData.exceeds_pipe_capacity && (
                        <div style={{ color: '#dc3545', fontWeight: 'bold' }}>
                          ⚠️ Exceeds pipe capacity
                        </div>
                      )}
                      {metricData.below_pipe_minimum && (
                        <div style={{ color: '#ffc107', fontWeight: 'bold' }}>
                          ⚠️ Below pipe minimum
                        </div>
                      )}
                    </>
                  )}
                  {/* Enhanced MTBA metadata */}
                  {metric.key === 'mtba' && metricData.min_interval && (
                    <>
                      <div>Min Interval: {metricData.min_interval} min</div>
                      <div>Max Interval: {metricData.max_interval} min</div>
                      <div>Std Dev: {metricData.interval_std} min</div>
                      <div>Anomaly Rate: {metricData.anomaly_rate}/hour</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.mtba_status === 'excellent' ? '#28a745' :
                               metricData.mtba_status === 'good' ? '#17a2b8' :
                               metricData.mtba_status === 'acceptable' ? '#ffc107' : '#dc3545'
                      }}>
                        Status: {metricData.mtba_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Time Span: {metricData.time_span_hours} hours</div>
                      <div>Window: {metricData.window_size} samples</div>
                      {metricData.sensor_count_power && (
                        <div>Power: {metricData.sensor_count_power} anomalies</div>
                      )}
                      {metricData.sensor_count_flow && (
                        <div>Flow: {metricData.sensor_count_flow} anomalies</div>
                      )}
                      {metricData.sensor_count_level && (
                        <div>Level: {metricData.sensor_count_level} anomalies</div>
                      )}
                      {metricData.sensor_count_temperature && (
                        <div>Temperature: {metricData.sensor_count_temperature} anomalies</div>
                      )}
                      {metricData.filtered_sensor && metricData.filtered_sensor !== 'all' && (
                        <div style={{ color: '#17a2b8', fontWeight: 'bold' }}>
                          Filtered: {metricData.filtered_sensor}
                        </div>
                      )}
                    </>
                  )}
                  {/* Enhanced Level Uptime metadata */}
                  {metric.key === 'level_uptime' && metricData.avg_level && (
                    <>
                      <div>Average Level: {metricData.avg_level * 100}%</div>
                      <div>Range: {metricData.min_level * 100}% - {metricData.max_level * 100}%</div>
                      <div>Low Threshold: {metricData.low_threshold * 100}%</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.uptime_status === 'excellent' ? '#28a745' :
                               metricData.uptime_status === 'good' ? '#17a2b8' :
                               metricData.uptime_status === 'acceptable' ? '#ffc107' : '#dc3545'
                      }}>
                        Status: {metricData.uptime_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Variability: {metricData.level_variability}%</div>
                      <div>Low Level: {metricData.low_percent}% ({metricData.low_count} readings)</div>
                      <div>Normal Level: {metricData.normal_percent}% ({metricData.normal_count} readings)</div>
                      {metricData.high_count > 0 && (
                        <div style={{ color: '#dc3545', fontWeight: 'bold' }}>
                          ⚠️ Overflow: {metricData.high_percent}% ({metricData.high_count} readings)
                        </div>
                      )}
                      {metricData.low_percent > 10 && (
                        <div style={{ color: '#ffc107', fontWeight: 'bold' }}>
                          ⚠️ High low-level time: {metricData.low_percent}%
                        </div>
                      )}
                    </>
                  )}
                  {/* Enhanced Availability metadata */}
                  {metric.key === 'availability' && metricData.avg_flow && (
                    <>
                      <div>Average Flow: {metricData.avg_flow} L/min</div>
                      <div>Flow Range: {metricData.min_flow} - {metricData.max_flow} L/min</div>
                      <div>Total Volume: {metricData.total_volume} L</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.availability_status === 'excellent' ? '#28a745' :
                               metricData.availability_status === 'good' ? '#17a2b8' :
                               metricData.availability_status === 'acceptable' ? '#ffc107' : '#dc3545'
                      }}>
                        Status: {metricData.availability_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Flow Variability: {metricData.flow_variability}%</div>
                      <div>Zero Flow: {metricData.zero_percent}% ({metricData.zero_count} readings)</div>
                      <div>Low Flow: {metricData.low_percent}% ({metricData.low_count} readings)</div>
                      <div>Normal Flow: {metricData.normal_percent}% ({metricData.normal_count} readings)</div>
                      {metricData.zero_percent > 50 && (
                        <div style={{ color: '#dc3545', fontWeight: 'bold' }}>
                          ⚠️ High idle time: {metricData.zero_percent}%
                        </div>
                      )}
                      {metricData.availability_status === 'poor' && (
                        <div style={{ color: '#dc3545', fontWeight: 'bold' }}>
                          ⚠️ Low system utilization
                        </div>
                      )}
                    </>
                  )}
                  {/* Enhanced Performance metadata */}
                  {metric.key === 'performance' && metricData.actual_liters && (
                    <>
                      <div>Actual: {metricData.actual_liters} L</div>
                      <div>Expected: {metricData.expected_liters} L</div>
                      <div>Efficiency: {metricData.efficiency_percent}%</div>
                      <div style={{ 
                        fontWeight: 'bold',
                        color: metricData.performance_status === 'excellent' ? '#28a745' :
                               metricData.performance_status === 'good' ? '#17a2b8' :
                               metricData.performance_status === 'acceptable' ? '#ffc107' :
                               metricData.performance_status === 'poor' ? '#fd7e14' : '#dc3545'
                      }}>
                        Status: {metricData.performance_status?.toUpperCase() || 'UNKNOWN'}
                      </div>
                      <div>Flow Rate: {metricData.achieved_flow_rate} L/min (configured: {metricData.configured_flow_rate} L/min)</div>
                      <div>Flow Range: {metricData.min_flow} - {metricData.max_flow} L/min</div>
                      <div>Flow Variability: {metricData.flow_variability}%</div>
                      {metricData.deficit_liters > 0 && (
                        <div style={{ color: '#ffc107', fontWeight: 'bold' }}>
                          ⚠️ Deficit: {metricData.deficit_liters} L below expected
                        </div>
                      )}
                      {metricData.surplus_liters > 0 && (
                        <div style={{ color: '#28a745', fontWeight: 'bold' }}>
                          ✅ Surplus: {metricData.surplus_liters} L above expected
                        </div>
                      )}
                      {metricData.performance_status === 'critical' && (
                        <div style={{ color: '#dc3545', fontWeight: 'bold' }}>
                          ⚠️ Critical performance below minimum acceptable
                        </div>
                      )}
                      {metricData.performance_status === 'poor' && (
                        <div style={{ color: '#fd7e14', fontWeight: 'bold' }}>
                          ⚠️ Poor performance - below acceptable threshold
                        </div>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Quality Timeline Chart - Temporarily disabled */}
      {/* TODO: Re-enable when timeline functionality is fixed */}
    </div>
  );
}