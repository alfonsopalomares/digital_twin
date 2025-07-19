# Changelog

## [1.1.0] - 2024-12-19

### Mejoras en Endpoints de Métricas

#### 1. Endpoint `failures_count` Mejorado
- **Metadatos adicionales**:
  - `failures_per_week`: Fallas por semana
  - `weekly_failure_rate`: Tasa semanal de fallas
  - `reliability_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `failure_rate`: Tasa de fallas por hora
  - `temp_failures`: Fallas de temperatura
  - `flow_failures`: Fallas de flujo
  - `level_failures`: Fallas de nivel
  - `power_failures`: Fallas de potencia
  - `temp_percent`: Porcentaje de fallas de temperatura
  - `flow_percent`: Porcentaje de fallas de flujo
  - `level_percent`: Porcentaje de fallas de nivel
  - `power_percent`: Porcentaje de fallas de potencia
  - `avg_temp_deviation`: Desviación promedio de temperatura (°C)
  - `max_temp_deviation`: Desviación máxima de temperatura (°C)
  - `avg_power_failure`: Potencia promedio en fallas (kW)
  - `max_power_failure`: Potencia máxima en fallas (kW)
  - `avg_flow_failure`: Flujo promedio en fallas (L/min)
  - `min_flow_failure`: Flujo mínimo en fallas (L/min)
  - `avg_level_failure`: Nivel promedio en fallas (L)
  - `min_level_failure`: Nivel mínimo en fallas (L)
  - `weeks_analyzed`: Semanas analizadas
  - `setpoint_temp`: Temperatura objetivo (°C)
  - `temp_tolerance`: Tolerancia de temperatura (°C)
  - `flow_threshold`: Umbral de flujo (L/min)
  - `level_threshold`: Umbral de nivel (L)
  - `power_threshold`: Umbral de potencia (kW)
  - `excellent_threshold`: Umbral excelente (5.0 fallas/semana)
  - `good_threshold`: Umbral bueno (10.0 fallas/semana)
  - `acceptable_threshold`: Umbral aceptable (20.0 fallas/semana)
  - `unit`: Unidad de medida (failures)

**Clasificación de Estados:**
- **`excellent`**: ≤ 5 fallas/semana (confiabilidad excelente)
- **`good`**: ≤ 10 fallas/semana (confiabilidad buena)
- **`acceptable`**: ≤ 20 fallas/semana (confiabilidad aceptable)
- **`poor`**: > 20 fallas/semana (confiabilidad deficiente)

**Funcionalidades:**
- **Parámetro configurable**: `weeks` para ajustar el período de análisis
- **Categorización de fallas**: Análisis por tipo de sensor (temperatura, flujo, nivel, potencia)
- **Análisis de desviaciones**: Estadísticas de desviaciones de temperatura y potencia
- **Alertas automáticas**: Advertencias para alta tasa de fallas y desviaciones excesivas

#### 2. Endpoint `usage_rate` Mejorado
- **Metadatos adicionales**:
  - `utilization_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'low', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `time_span_days`: Tiempo total analizado (días)
  - `total_services`: Total de servicios realizados
  - `services_per_day`: Servicios por día
  - `avg_flow_per_service`: Flujo promedio por servicio (L/min)
  - `min_flow_per_service`: Flujo mínimo por servicio (L/min)
  - `max_flow_per_service`: Flujo máximo por servicio (L/min)
  - `flow_std`: Desviación estándar del flujo
  - `flow_variability`: Variabilidad del flujo (%)
  - `total_volume`: Volumen total dispensado (L)
  - `avg_service_duration`: Duración promedio del servicio (segundos)
  - `peak_hour_services`: Servicios en hora pico
  - `avg_hourly_services`: Servicios promedio por hora
  - `peak_hour_ratio`: Ratio de hora pico vs promedio
  - `busy_hours`: Horas ocupadas
  - `total_hours`: Total de horas analizadas
  - `busy_period_percent`: Porcentaje de períodos ocupados
  - `avg_interval_minutes`: Intervalo promedio entre servicios (minutos)
  - `min_interval_minutes`: Intervalo mínimo entre servicios (minutos)
  - `max_interval_minutes`: Intervalo máximo entre servicios (minutos)
  - `interval_std`: Desviación estándar de intervalos (minutos)
  - `excellent_threshold`: Umbral excelente (15.0 servicios/hora)
  - `good_threshold`: Umbral bueno (10.0 servicios/hora)
  - `acceptable_threshold`: Umbral aceptable (5.0 servicios/hora)
  - `min_threshold`: Umbral mínimo (2.0 servicios/hora)
  - `unit`: Unidad de medida (services/hour)

**Clasificación de Estados:**
- **`excellent`**: ≥ 15 servicios/hora (utilización excelente)
- **`good`**: ≥ 10 servicios/hora (utilización buena)
- **`acceptable`**: ≥ 5 servicios/hora (utilización aceptable)
- **`low`**: ≥ 2 servicios/hora (utilización baja)
- **`poor`**: < 2 servicios/hora (utilización deficiente)

**Funcionalidades:**
- **Filtrado por tiempo**: Parámetros `start` y `end` para análisis temporal
- **Análisis de patrones**: Distribución horaria y análisis de horas pico
- **Métricas de eficiencia**: Duración de servicios e intervalos entre usos
- **Alertas automáticas**: Advertencias para utilización baja y patrones anómalos

### Mejoras en Frontend

#### 1. Dashboard de Métricas Simplificado
- **Reducción significativa de metadatos**: Simplificación de información mostrada en cada métrica
- **Estructura consistente**: Formato uniforme para todas las métricas
- **Status prominente**: Estado de salud del sistema destacado en cada métrica
- **Alertas simplificadas**: Mensajes de advertencia más concisos y relevantes

**Métricas optimizadas:**
- **Quality**: De 12 líneas a 4 líneas (66% reducción)
- **Energy Efficiency**: De 8 líneas a 5 líneas (37% reducción)
- **Thermal Variation**: De 7 líneas a 3 líneas (57% reducción)
- **Peak Flow Ratio**: De 10 líneas a 4 líneas (60% reducción)
- **MTBA**: De 15 líneas a 4 líneas (73% reducción)
- **Level Uptime**: De 12 líneas a 4 líneas (66% reducción)
- **Availability**: De 11 líneas a 5 líneas (54% reducción)
- **Performance**: De 15 líneas a 5 líneas (66% reducción)
- **Response Index**: De 18 líneas a 5 líneas (72% reducción)
- **Nonproductive Consumption**: De 15 líneas a 5 líneas (66% reducción)
- **MTBF**: De 20 líneas a 4 líneas (80% reducción)
- **Quality Full**: De 20 líneas a 4 líneas (80% reducción)
- **Response Time**: De 25 líneas a 5 líneas (80% reducción)
- **Failures Count**: De 25 líneas a 4 líneas (84% reducción)
- **Usage Rate**: De 20 líneas a 4 líneas (80% reducción)

**Estructura de información por métrica:**
1. **Status** (en negrita y color)
2. **2-3 métricas clave** (las más importantes)
3. **1 alerta** (solo si hay problemas)

#### 2. Soporte para Status de Utilización
- **Colores de status para `usage_rate`**:
  - 🟢 **EXCELLENT** (Verde: #28a745) - ≥15 servicios/hora
  - 🔵 **GOOD** (Azul: #17a2b8) - ≥10 servicios/hora
  - 🟡 **ACCEPTABLE** (Amarillo: #ffc107) - ≥5 servicios/hora
  - 🟠 **LOW** (Naranja: #fd7e14) - ≥2 servicios/hora
  - 🔴 **POOR** (Rojo: #dc3545) - <2 servicios/hora

#### 3. Soporte para Status de Confiabilidad
- **Colores de status para `failures_count`**:
  - 🟢 **EXCELLENT** (Verde: #28a745) - ≤5 fallas/semana
  - 🔵 **GOOD** (Azul: #17a2b8) - ≤10 fallas/semana
  - 🟡 **ACCEPTABLE** (Amarillo: #ffc107) - ≤20 fallas/semana
  - 🔴 **POOR** (Rojo: #dc3545) - >20 fallas/semana

### Correcciones Técnicas

#### 1. Manejo de Fechas en `usage_rate`
- **Problema**: Error de comparación entre fechas con y sin zona horaria
- **Solución**: Implementación de función `in_range()` que maneja correctamente las comparaciones de fechas
- **Impacto**: Endpoint ahora funciona correctamente con parámetros de fecha

#### 2. Optimización de Rendimiento
- **Reducción de complejidad**: Eliminación de cálculos redundantes en frontend
- **Mejor experiencia de usuario**: Dashboard más rápido y fácil de navegar
- **Mantenibilidad**: Código más limpio y fácil de mantener

---

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
- **Gauge de Nonproductive Consumption**: Muestra energía total, productiva, ratio de eficiencia, distribución de períodos y estado de gestión energética
- **Gauge de MTBF**: Muestra rango de MTBF, variabilidad, distribución de fallas por tipo, tasas de fallas y estado de confiabilidad
- **Gauge de Quality Full**: Muestra servicios correctos vs incorrectos, distribución de problemas, estadísticas de flujo/temperatura y estado de calidad integral

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
- ⚠️ Poor energy management - high nonproductive consumption (gestión energética deficiente)
- ⚠️ High percentage of nonproductive periods (alto porcentaje de períodos no productivos)
- ⚠️ High nonproductive energy ratio (alto ratio de energía no productiva)
- ⚠️ Poor system reliability - frequent failures (confiabilidad deficiente del sistema)
- ⚠️ High temperature failure rate (alta tasa de fallas de temperatura)
- ⚠️ High failure rate (alta tasa de fallas)
- ⚠️ High temperature deviation (alta desviación de temperatura)
- ⚠️ Poor service quality - high rate of incorrect services (calidad de servicio deficiente)
- ⚠️ High temperature issue rate (alta tasa de problemas de temperatura)
- ⚠️ High flow issue rate (alta tasa de problemas de flujo)
- ⚠️ High temperature variability in correct services (alta variabilidad de temperatura en servicios correctos)

### Correcciones Técnicas

#### Eliminación de Duplicaciones en JSON de Respuesta
- **Endpoint `performance`**: Eliminado `expected_liters` duplicado (ya está en `expected_value`)
- **Endpoint `availability`**: Eliminado `unit` duplicado
- **Endpoint `level_uptime`**: Eliminado `unit` duplicado
- **Endpoint `quality`**: Eliminado `unit` duplicado
- **Endpoint `energy_efficiency`**: Eliminado `unit` duplicado

### Nuevas Mejoras en Endpoints de Métricas

#### 7. Endpoint `nonproductive_consumption` Mejorado
- **Metadatos adicionales**:
  - `total_energy`: Energía total consumida (kWh)
  - `productive_energy`: Energía consumida durante períodos productivos (kWh)
  - `consumption_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `energy_efficiency_ratio`: Ratio de eficiencia energética (%)
  - `time_span_hours`: Tiempo total analizado (horas)
  - `consumption_rate`: Tasa de consumo no productivo (kWh/hora)
  - `nonprod_periods_count`: Conteo de períodos no productivos
  - `prod_periods_count`: Conteo de períodos productivos
  - `nonprod_percent`: Porcentaje de períodos no productivos
  - `prod_percent`: Porcentaje de períodos productivos
  - `avg_nonprod_power`: Potencia promedio no productiva (kW)
  - `min_nonprod_power`: Potencia mínima no productiva (kW)
  - `max_nonprod_power`: Potencia máxima no productiva (kW)
  - `nonprod_power_std`: Desviación estándar de potencia no productiva
  - `nonprod_power_variability`: Variabilidad de potencia no productiva (%)
  - `avg_prod_power`: Potencia promedio productiva (kW)
  - `min_prod_power`: Potencia mínima productiva (kW)
  - `max_prod_power`: Potencia máxima productiva (kW)
  - `prod_power_std`: Desviación estándar de potencia productiva
  - `prod_power_variability`: Variabilidad de potencia productiva (%)
  - `flow_inactivity_threshold`: Umbral de inactividad de flujo (L/min)
  - `excellent_threshold`: Umbral excelente (0.2 kWh)
  - `good_threshold`: Umbral bueno (0.5 kWh)
  - `acceptable_threshold`: Umbral aceptable (1.0 kWh)
  - `unit`: Unidad de medida (kWh)

**Clasificación de Estados:**
- **`excellent`**: ≤ 0.2 kWh (gestión energética excelente)
- **`good`**: ≤ 0.5 kWh (gestión energética buena)
- **`acceptable`**: ≤ 1.0 kWh (gestión energética aceptable)
- **`poor`**: > 1.0 kWh (gestión energética deficiente)

**Funcionalidades:**
- **Filtrado por tiempo**: Parámetros `start` y `end` para análisis temporal
- **Análisis de períodos**: Distinción entre períodos productivos y no productivos
- **Estadísticas de potencia**: Análisis detallado de consumo energético por tipo de período
- **Alertas automáticas**: Advertencias para gestión energética deficiente y períodos no productivos altos

#### 8. Endpoint `mtbf` (Mean Time Between Failures) Mejorado
- **Metadatos adicionales**:
  - `min_mtbf`: MTBF mínimo (horas)
  - `max_mtbf`: MTBF máximo (horas)
  - `mtbf_std`: Desviación estándar de MTBF (horas)
  - `mtbf_variability`: Variabilidad de MTBF (%)
  - `reliability_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `failure_span_hours`: Tiempo de span de fallas (horas)
  - `failure_rate`: Tasa de fallas por hora
  - `total_failures`: Total de fallas detectadas
  - `temp_failures`: Fallas de temperatura
  - `flow_failures`: Fallas de flujo
  - `level_failures`: Fallas de nivel
  - `power_failures`: Fallas de potencia
  - `temp_percent`: Porcentaje de fallas de temperatura
  - `flow_percent`: Porcentaje de fallas de flujo
  - `level_percent`: Porcentaje de fallas de nivel
  - `power_percent`: Porcentaje de fallas de potencia
  - `avg_temp_deviation`: Desviación promedio de temperatura (°C)
  - `max_temp_deviation`: Desviación máxima de temperatura (°C)
  - `avg_power_failure`: Potencia promedio en fallas (kW)
  - `max_power_failure`: Potencia máxima en fallas (kW)
  - `excellent_threshold`: Umbral excelente (72.0 horas)
  - `good_threshold`: Umbral bueno (24.0 horas)
  - `acceptable_threshold`: Umbral aceptable (12.0 horas)
  - `setpoint_temp`: Temperatura setpoint configurada (°C)
  - `temp_tolerance`: Tolerancia de temperatura configurada (°C)
  - `flow_threshold`: Umbral de flujo configurado (L/min)
  - `level_threshold`: Umbral de nivel configurado (L)
  - `power_threshold`: Umbral de potencia configurado (kW)
  - `unit`: Unidad de medida (hours)

**Clasificación de Estados:**
- **`excellent`**: ≥ 72 horas (confiabilidad del sistema excelente)
- **`good`**: ≥ 24 horas (confiabilidad del sistema buena)
- **`acceptable`**: ≥ 12 horas (confiabilidad del sistema aceptable)
- **`poor`**: < 12 horas (confiabilidad del sistema deficiente)

**Funcionalidades:**
- **Filtrado por tiempo**: Parámetros `start` y `end` para análisis temporal
- **Categorización de fallas**: Distinción por tipo de sensor y condición de falla
- **Análisis de desviaciones**: Estadísticas detalladas de fallas de temperatura
- **Alertas automáticas**: Advertencias para confiabilidad deficiente y tasas altas de fallas

#### 9. Endpoint `quality_full` Mejorado
- **Metadatos adicionales**:
  - `quality_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `service_rate`: Tasa de servicios por hora
  - `correct_services_count`: Conteo de servicios correctos
  - `incorrect_services_count`: Conteo de servicios incorrectos
  - `temp_issue_count`: Conteo de problemas de temperatura
  - `flow_issue_count`: Conteo de problemas de flujo
  - `both_issue_count`: Conteo de problemas combinados
  - `temp_issue_percent`: Porcentaje de problemas de temperatura
  - `flow_issue_percent`: Porcentaje de problemas de flujo
  - `both_issue_percent`: Porcentaje de problemas combinados
  - `avg_correct_flow`: Flujo promedio en servicios correctos (L/min)
  - `min_correct_flow`: Flujo mínimo en servicios correctos (L/min)
  - `max_correct_flow`: Flujo máximo en servicios correctos (L/min)
  - `correct_flow_std`: Desviación estándar de flujo correcto
  - `correct_flow_variability`: Variabilidad de flujo correcto (%)
  - `avg_correct_temp`: Temperatura promedio en servicios correctos (°C)
  - `min_correct_temp`: Temperatura mínima en servicios correctos (°C)
  - `max_correct_temp`: Temperatura máxima en servicios correctos (°C)
  - `correct_temp_std`: Desviación estándar de temperatura correcta
  - `correct_temp_variability`: Variabilidad de temperatura correcta (%)
  - `avg_incorrect_flow`: Flujo promedio en servicios incorrectos (L/min)
  - `min_incorrect_flow`: Flujo mínimo en servicios incorrectos (L/min)
  - `max_incorrect_flow`: Flujo máximo en servicios incorrectos (L/min)
  - `incorrect_flow_std`: Desviación estándar de flujo incorrecto
  - `avg_incorrect_temp`: Temperatura promedio en servicios incorrectos (°C)
  - `min_incorrect_temp`: Temperatura mínima en servicios incorrectos (°C)
  - `max_incorrect_temp`: Temperatura máxima en servicios incorrectos (°C)
  - `incorrect_temp_std`: Desviación estándar de temperatura incorrecta
  - `avg_temp_deviation`: Desviación promedio de temperatura (°C)
  - `max_temp_deviation`: Desviación máxima de temperatura (°C)
  - `excellent_threshold`: Umbral excelente (95.0%)
  - `good_threshold`: Umbral bueno (90.0%)
  - `acceptable_threshold`: Umbral aceptable (80.0%)
  - `setpoint_temp`: Temperatura setpoint configurada (°C)
  - `temp_tolerance`: Tolerancia de temperatura configurada (°C)
  - `min_flow_threshold`: Umbral mínimo de flujo configurado (L/min)
  - `unit`: Unidad de medida (percent)

**Clasificación de Estados:**
- **`excellent`**: ≥ 95% (calidad de servicio excelente)
- **`good`**: ≥ 90% (calidad de servicio buena)
- **`acceptable`**: ≥ 80% (calidad de servicio aceptable)
- **`poor`**: < 80% (calidad de servicio deficiente)

**Funcionalidades:**
- **Filtrado por tiempo**: Parámetros `start` y `end` para análisis temporal
- **Categorización de servicios**: Distinción entre servicios correctos e incorrectos
- **Análisis de problemas**: Clasificación por tipo de problema (temperatura, flujo, ambos)
- **Estadísticas detalladas**: Análisis de flujo y temperatura para cada categoría
- **Alertas automáticas**: Advertencias para calidad deficiente y tasas altas de problemas
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