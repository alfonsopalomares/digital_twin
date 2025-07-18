# Changelog

## [1.0.0] - 2024-12-19

### Mejoras en Endpoints de Métricas

#### 1. Endpoint `mtba` (Mean Time Between Adaptive Anomalies) Mejorado
- **Metadatos adicionales**:
  - `min_interval`: Intervalo mínimo entre anomalías (minutos)
  - `max_interval`: Intervalo máximo entre anomalías (minutos)
  - `interval_std`: Desviación estándar de intervalos (minutos)
  - `anomaly_rate`: Tasa de anomalías por hora
  - `mtba_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `window_size`: Tamaño de ventana para detección
  - `total_anomalies`: Total de anomalías detectadas
  - `unique_events`: Eventos únicos (agrupados por timestamp)
  - `simultaneous_anomalies`: Anomalías simultáneas
  - `sensor_count_*`: Conteo de anomalías por sensor
  - `sensor_distribution_*`: Distribución porcentual por sensor
  - `filtered_sensor`: Sensor filtrado o 'all'
  - `excellent_threshold`: Umbral excelente (30.0 minutos)
  - `good_threshold`: Umbral bueno (15.0 minutos)
  - `acceptable_threshold`: Umbral aceptable (5.0 minutos)
  - `unit`: Unidad de medida (minutes)

**Clasificación de Estados:**
- **`excellent`**: ≥ 30 minutos (estabilidad del sistema excelente)
- **`good`**: ≥ 15 minutos (estabilidad del sistema buena)
- **`acceptable`**: ≥ 5 minutos (estabilidad del sistema aceptable)
- **`poor`**: < 5 minutos (estabilidad del sistema deficiente)

**Funcionalidades:**
- **Filtrado por sensor**: Parámetro `sensor` para análisis específico
- **Ventana configurable**: Parámetro `window` para ajustar sensibilidad
- **Agrupación de anomalías**: Tratamiento de anomalías simultáneas como eventos únicos
- **Alertas automáticas**: Advertencias para alta tasa de anomalías y estabilidad deficiente

#### 2. Endpoint `level_uptime` Mejorado
- **Metadatos adicionales**:
  - `avg_level`: Nivel promedio observado
  - `min_level`: Nivel mínimo observado
  - `max_level`: Nivel máximo observado
  - `level_std`: Desviación estándar del nivel
  - `level_variability`: Variabilidad del nivel (%)
  - `uptime_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `low_threshold`: Umbral bajo configurado
  - `low_count`: Lecturas por debajo del umbral
  - `normal_count`: Lecturas dentro del rango normal
  - `high_count`: Lecturas por encima del 100% (overflow)
  - `low_percent`: Porcentaje de tiempo con nivel bajo
  - `normal_percent`: Porcentaje de tiempo con nivel normal
  - `high_percent`: Porcentaje de tiempo con overflow
  - `excellent_threshold`: Umbral excelente (98.0%)
  - `good_threshold`: Umbral bueno (95.0%)
  - `acceptable_threshold`: Umbral aceptable (80.0%)
  - `unit`: Unidad de medida (percent)

**Clasificación de Estados:**
- **`excellent`**: ≥ 98% (disponibilidad de agua excelente)
- **`good`**: ≥ 95% (disponibilidad de agua buena)
- **`acceptable`**: ≥ 80% (disponibilidad de agua aceptable)
- **`poor`**: < 80% (disponibilidad de agua deficiente)

**Funcionalidades:**
- **Filtrado por tiempo**: Parámetros `start` y `end` para análisis temporal
- **Detección de overflow**: Identifica cuando el nivel excede el 100%
- **Análisis de variabilidad**: Mide la estabilidad del nivel de agua
- **Alertas automáticas**: Advertencias para niveles bajos prolongados

#### 3. Endpoint `availability` Mejorado
- **Metadatos adicionales**:
  - `avg_flow`: Flujo promedio (L/min)
  - `min_flow`: Flujo mínimo observado (L/min)
  - `max_flow`: Flujo máximo observado (L/min)
  - `flow_std`: Desviación estándar del flujo
  - `flow_variability`: Variabilidad del flujo (%)
  - `availability_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `total_volume`: Volumen total dispensado (L)
  - `zero_count`: Lecturas con flujo cero
  - `low_count`: Lecturas con flujo bajo (≤ 0.01 L/min)
  - `normal_count`: Lecturas con flujo normal (> 0.01 L/min)
  - `zero_percent`: Porcentaje de tiempo sin flujo
  - `low_percent`: Porcentaje de tiempo con flujo bajo
  - `normal_percent`: Porcentaje de tiempo con flujo normal
  - `excellent_threshold`: Umbral excelente (80.0%)
  - `good_threshold`: Umbral bueno (60.0%)
  - `acceptable_threshold`: Umbral aceptable (30.0%)
  - `unit`: Unidad de medida (percent)

**Clasificación de Estados:**
- **`excellent`**: ≥ 80% (utilización del sistema excelente)
- **`good`**: ≥ 60% (utilización del sistema buena)
- **`acceptable`**: ≥ 30% (utilización del sistema aceptable)
- **`poor`**: < 30% (utilización del sistema deficiente)

**Funcionalidades:**
- **Filtrado por tiempo**: Parámetros `start` y `end` para análisis temporal
- **Cálculo de volumen**: Volumen total dispensado basado en integración de flujo
- **Análisis de distribución**: Clasificación de lecturas por nivel de flujo
- **Alertas automáticas**: Advertencias para tiempo de inactividad alto

#### 4. Endpoint `performance` Mejorado
- **Metadatos adicionales**:
  - `actual_liters`: Litros reales dispensados
  - `performance_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor', 'critical')
  - `efficiency_percent`: Eficiencia como porcentaje
  - `deficit_liters`: Déficit de litros (si actual < esperado)
  - `surplus_liters`: Excedente de litros (si actual > esperado)
  - `avg_flow`: Flujo promedio observado (L/min)
  - `min_flow`: Flujo mínimo observado (L/min)
  - `max_flow`: Flujo máximo observado (L/min)
  - `flow_std`: Desviación estándar del flujo
  - `flow_variability`: Variabilidad del flujo (%)
  - `achieved_flow_rate`: Tasa de flujo lograda (L/min)
  - `configured_flow_rate`: Tasa de flujo configurada (L/min)
  - `time_span_hours`: Tiempo total analizado (horas)
  - `excellent_threshold`: Umbral excelente (1.05 ratio, ≥105%)
  - `good_threshold`: Umbral bueno (0.95 ratio, ≥95%)
  - `acceptable_threshold`: Umbral aceptable (0.85 ratio, ≥85%)
  - `min_acceptable`: Mínimo aceptable (0.70 ratio, ≥70%)
  - `unit`: Unidad de medida (ratio)

**Clasificación de Estados:**
- **`excellent`**: ≥ 1.05 (utilización de capacidad excelente)
- **`good`**: ≥ 0.95 (utilización de capacidad buena)
- **`acceptable`**: ≥ 0.85 (utilización de capacidad aceptable)
- **`poor`**: ≥ 0.70 (utilización de capacidad deficiente)
- **`critical`**: < 0.70 (utilización de capacidad crítica)

**Funcionalidades:**
- **Parámetros configurables**: `users` y `hours` para personalizar expectativas
- **Análisis de eficiencia**: Comparación real vs esperado con métricas detalladas
- **Alertas automáticas**: Advertencias para déficit, excedente y rendimiento crítico
- **Análisis de flujo**: Estadísticas detalladas del flujo observado vs configurado

#### 5. Endpoint `quality` Mejorado
- **Metadatos adicionales**:
  - `setpoint`: Temperatura objetivo configurada (°C)
  - `tolerance_band`: Banda de tolerancia total (°C)
  - `within_count`: Lecturas dentro del rango aceptable
  - `total_count`: Total de lecturas analizadas
  - `quality_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `avg_temp`: Temperatura promedio observada (°C)
  - `min_temp`: Temperatura mínima observada (°C)
  - `max_temp`: Temperatura máxima observada (°C)
  - `temp_std`: Desviación estándar de temperatura (°C)
  - `temp_variability`: Variabilidad de temperatura (%)
  - `avg_deviation`: Desviación promedio del setpoint (°C)
  - `max_deviation`: Desviación máxima del setpoint (°C)
  - `time_span_hours`: Tiempo total analizado (horas)
  - `low_count`: Lecturas por debajo del rango aceptable
  - `high_count`: Lecturas por encima del rango aceptable
  - `low_percent`: Porcentaje de lecturas bajas
  - `within_percent`: Porcentaje de lecturas dentro del rango
  - `high_percent`: Porcentaje de lecturas altas
  - `excellent_threshold`: Umbral excelente (98.0%)
  - `good_threshold`: Umbral bueno (95.0%)
  - `acceptable_threshold`: Umbral aceptable (90.0%)
  - `unit`: Unidad de medida (percent)

**Clasificación de Estados:**
- **`excellent`**: ≥ 98% (control de temperatura excelente)
- **`good`**: ≥ 95% (control de temperatura bueno)
- **`acceptable`**: ≥ 90% (control de temperatura aceptable)
- **`poor`**: < 90% (control de temperatura deficiente)

**Funcionalidades:**
- **Filtrado por tiempo**: Parámetros `start` y `end` para análisis temporal
- **Análisis de distribución**: Clasificación de lecturas por rango de temperatura
- **Alertas automáticas**: Advertencias para control deficiente y desviaciones excesivas
- **Análisis de variabilidad**: Estadísticas detalladas de estabilidad térmica

#### 6. Endpoint `response_index` Mejorado
- **Metadatos adicionales**:
  - `min_response_time`: Tiempo de respuesta mínimo (minutos)
  - `max_response_time`: Tiempo de respuesta máximo (minutos)
  - `response_std`: Desviación estándar de tiempos de respuesta (minutos)
  - `response_variability`: Variabilidad de tiempos de respuesta (%)
  - `response_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `response_rate`: Tasa de respuestas por hora
  - `fast_count`: Respuestas rápidas (≤2 minutos)
  - `good_count`: Respuestas buenas (2-5 minutos)
  - `slow_count`: Respuestas lentas (5-10 minutos)
  - `very_slow_count`: Respuestas muy lentas (>10 minutos)
  - `fast_percent`: Porcentaje de respuestas rápidas
  - `good_percent`: Porcentaje de respuestas buenas
  - `slow_percent`: Porcentaje de respuestas lentas
  - `very_slow_percent`: Porcentaje de respuestas muy lentas
  - `excellent_threshold`: Umbral excelente (2.0 minutos)
  - `good_threshold`: Umbral bueno (5.0 minutos)
  - `acceptable_threshold`: Umbral aceptable (10.0 minutos)
  - `window_size`: Tamaño de ventana para detección de anomalías
  - `response_time_*`: Tiempo promedio de respuesta por sensor
  - `filtered_sensor`: Sensor filtrado o 'all' si no hay filtro
  - `unit`: Unidad de medida (min)

**Clasificación de Estados:**
- **`excellent`**: ≤ 2 minutos (tiempo de respuesta excelente)
- **`good`**: ≤ 5 minutos (tiempo de respuesta bueno)
- **`acceptable`**: ≤ 10 minutos (tiempo de respuesta aceptable)
- **`poor`**: > 10 minutos (tiempo de respuesta deficiente)

**Funcionalidades:**
- **Filtrado por sensor**: Parámetro `sensor` para análisis específico
- **Análisis de distribución**: Clasificación de respuestas por velocidad
- **Alertas automáticas**: Advertencias para respuestas lentas y porcentajes altos de respuestas muy lentas
- **Análisis por sensor**: Tiempos de respuesta promedio por tipo de sensor

### Mejoras en Frontend

#### Visualizaciones Enriquecidas
- **Gauge de MTBA**: Muestra intervalos mínimo/máximo, tasa de anomalías, estado de estabilidad y distribución por sensor
- **Gauge de Level Uptime**: Muestra nivel promedio, rango, variabilidad, distribución de niveles y estado de disponibilidad
- **Gauge de Availability**: Muestra flujo promedio, rango, volumen total, distribución de flujo y estado de utilización
- **Gauge de Performance**: Muestra litros reales vs esperados, eficiencia, estado de rendimiento y análisis de flujo
- **Gauge de Quality**: Muestra temperatura promedio, rango, variabilidad, distribución térmica y estado de control
- **Gauge de Response Index**: Muestra rango de tiempos, variabilidad, distribución de respuestas y estado de reactividad

#### Colores Dinámicos
Los gauges cambian de color según el estado:
- 🟢 Verde: Estado 'excellent'
- 🔵 Azul: Estado 'good' 
- 🟡 Amarillo: Estado 'acceptable'
- 🟠 Naranja: Estado 'poor'
- 🔴 Rojo: Estado 'critical'/'excessive'

#### Alertas Visuales
Muestra advertencias cuando:
- ⚠️ Outside tolerance (fuera de tolerancia)
- ⚠️ High anomaly rate (alta tasa de anomalías)
- ⚠️ Poor system stability (estabilidad deficiente)
- ⚠️ High low-level time (tiempo alto con nivel bajo)
- ⚠️ Overflow detected (desbordamiento detectado)
- ⚠️ High idle time (tiempo alto de inactividad)
- ⚠️ Low system utilization (utilización baja del sistema)
- ⚠️ Deficit detected (déficit detectado)
- ⚠️ Poor temperature control (control deficiente de temperatura)
- ⚠️ Maximum deviation exceeds tolerance (desviación máxima excede tolerancia)
- ⚠️ Poor response time (tiempo de respuesta deficiente)
- ⚠️ High percentage of very slow responses (alto porcentaje de respuestas muy lentas)

### Correcciones Técnicas

#### Eliminación de Duplicaciones en JSON de Respuesta
- **Endpoint `performance`**: Eliminado `expected_liters` duplicado (ya está en `expected_value`)
- **Endpoint `availability`**: Eliminado `unit` duplicado
- **Endpoint `level_uptime`**: Eliminado `unit` duplicado
- **Endpoint `quality`**: Eliminado `unit` duplicado
- **Endpoint `energy_efficiency`**: Eliminado `unit` duplicado

#### Mejoras en Cálculos
- **MTBA**: Agrupación de anomalías simultáneas para evitar intervalos de 0 minutos
- **Availability**: Cálculo de volumen total con valores absolutos para evitar volúmenes negativos
- **Performance**: Cálculo de tiempo con valores absolutos para evitar intervalos negativos

### Documentación

#### README.es.md
- Reorganización completa para describir funcionalidad del sistema de forma continua
- Eliminación de referencias a "mejoras" y "nuevos cambios"
- Documentación consistente de todos los endpoints y funcionalidades

#### CHANGELOG.md
- Creación de archivo de changelog separado
- Documentación detallada de todas las mejoras implementadas
- Historial de cambios organizado por versiones 