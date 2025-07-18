# Proyecto Industria 4.0: Expendedor de Agua Inteligente

**Introducción:**
Este proyecto implementa un sistema de expendedor de agua inteligente inspirado en la Industria 4.0. Permite simular el comportamiento de sensores IoT, almacenar datos históricos, detectar anomalías y evaluar métricas de desempeño en tiempo real. Está diseñado para demostrar la viabilidad de tecnologías clave (IoT simulado, gemelos digitales, analítica y dashboards interactivos) en entornos con recursos limitados como PYMES o instituciones educativas.

---

## 🔄 Cambios Recientes (Última Actualización)

### **Mejoras en Endpoints de Métricas**

#### **1. Endpoint `energy_efficiency` Mejorado**
- **Valor esperado**: 0.051 kWh/L (calculado teóricamente para calentar agua de 25°C a 60°C)
- **Tolerancia**: ±0.025 kWh/L (50% del valor esperado)
- **Metadatos adicionales**:
  - `expected_value`: Valor esperado (eliminado duplicado `expected_efficiency`)
  - `tolerance_band`: Banda de tolerancia total (0.05)
  - `efficiency_ratio`: Ratio actual vs esperado
  - `within_tolerance`: Entero (0 o 1) indicando si está dentro de tolerancia
  - `total_kwh`: Consumo total de energía
  - `total_liters`: Volumen total dispensado
  - `efficiency_status`: Estado cualitativo ('excellent', 'good', 'poor', 'critical')
  - `unit`: Unidad de medida (kWh/L)

**Clasificación de Estados:**
- **`excellent`**: ≤ 1.5x el valor esperado (≤ 0.0765 kWh/L)
- **`good`**: ≤ 3x el valor esperado (≤ 0.153 kWh/L)  
- **`poor`**: ≤ 10x el valor esperado (≤ 0.51 kWh/L)
- **`critical`**: > 10x el valor esperado (> 0.51 kWh/L)

#### **2. Endpoint `quality` Mejorado**
- **Metadatos adicionales**:
  - `setpoint`: Temperatura setpoint (60°C)
  - `tolerance_band`: Banda de tolerancia (±5°C)
  - `within_count`: Lecturas dentro de tolerancia
  - `total_count`: Total de lecturas
  - `unit`: Unidad de medida (percent)

#### **3. Endpoint `thermal_variation` Mejorado**
- **Metadatos adicionales**:
  - `avg_temperature`: Temperatura promedio
  - `min_temperature`: Temperatura mínima
  - `max_temperature`: Temperatura máxima
  - `temperature_range`: Rango de temperaturas
  - `setpoint`: Temperatura setpoint (60°C)
  - `setpoint_deviation`: Desviación del setpoint
  - `variation_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `within_tolerance_count`: Lecturas dentro de tolerancia
  - `within_tolerance_percent`: Porcentaje dentro de tolerancia
  - `excellent_threshold`: Umbral excelente (1.0°C)
  - `good_threshold`: Umbral bueno (2.0°C)
  - `acceptable_threshold`: Umbral aceptable (5.0°C)
  - `unit`: Unidad de medida (°C)

**Clasificación de Estados:**
- **`excellent`**: ≤ 1.0°C (control de temperatura excelente)
- **`good`**: ≤ 2.0°C (control de temperatura bueno)
- **`acceptable`**: ≤ 5.0°C (control de temperatura aceptable)
- **`poor`**: > 5.0°C (control de temperatura deficiente)

#### **4. Endpoint `peak_flow_ratio` Mejorado**
- **Metadatos adicionales**:
  - `max_flow`: Flujo máximo observado (L/min)
  - `min_flow`: Flujo mínimo observado (L/min)
  - `avg_flow`: Flujo promedio (L/min)
  - `nominal_flow`: Flujo nominal de diseño (L/min)
  - `avg_ratio`: Ratio promedio vs nominal
  - `min_ratio`: Ratio mínimo vs nominal
  - `flow_std`: Desviación estándar del flujo
  - `flow_variability`: Variabilidad del flujo (%)
  - `ratio_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'excessive')
  - `above_nominal_count`: Lecturas por encima del nominal
  - `above_nominal_percent`: Porcentaje por encima del nominal
  - `exceeds_pipe_capacity`: Si excede la capacidad del tubo
  - `below_pipe_minimum`: Si está por debajo del mínimo del tubo
  - `pipe_max_capacity`: Capacidad máxima del tubo (L/min)
  - `pipe_min_capacity`: Capacidad mínima del tubo (L/min)
  - `excellent_threshold`: Umbral excelente (1.2)
  - `good_threshold`: Umbral bueno (1.5)
  - `acceptable_threshold`: Umbral aceptable (2.0)
  - `unit`: Unidad de medida (ratio)

**Clasificación de Estados:**
- **`excellent`**: ≤ 1.2 (control de flujo excelente)
- **`good`**: ≤ 1.5 (control de flujo bueno)
- **`acceptable`**: ≤ 2.0 (control de flujo aceptable)
- **`excessive`**: > 2.0 (flujo excesivo)

#### **5. Endpoint `mtba` (Mean Time Between Adaptive Anomalies) Mejorado**
- **Metadatos adicionales**:
  - `min_interval`: Intervalo mínimo entre anomalías (minutos)
  - `max_interval`: Intervalo máximo entre anomalías (minutos)
  - `interval_std`: Desviación estándar de intervalos (minutos)
  - `anomaly_rate`: Tasa de anomalías por hora
  - `mtba_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `window_size`: Tamaño de ventana para detección adaptativa
  - `sensor_count_*`: Conteo de anomalías por tipo de sensor (power, flow, level, temperature)
  - `sensor_distribution_*`: Distribución porcentual de anomalías por sensor
  - `filtered_sensor`: Sensor filtrado ('all' o nombre específico)
  - `excellent_threshold`: Umbral excelente (60.0 minutos)
  - `good_threshold`: Umbral bueno (30.0 minutos)
  - `acceptable_threshold`: Umbral aceptable (15.0 minutos)
  - `unit`: Unidad de medida (minutos)

**Clasificación de Estados:**
- **`excellent`**: ≥ 60 minutos (estabilidad del sistema excelente)
- **`good`**: ≥ 30 minutos (estabilidad del sistema buena)
- **`acceptable`**: ≥ 15 minutos (estabilidad del sistema aceptable)
- **`poor`**: < 15 minutos (estabilidad del sistema deficiente)

**Funcionalidades:**
- **Filtrado por sensor**: Parámetro `sensor` para analizar anomalías específicas
- **Ventana configurable**: Parámetro `window` para ajustar sensibilidad (default: 60 muestras)
- **Análisis temporal**: Cálculo de intervalos entre anomalías consecutivas
- **Distribución por sensor**: Análisis de qué tipos de sensores generan más anomalías

#### **6. Endpoint `level_uptime` Mejorado**
- **Metadatos adicionales**:
  - `avg_level`: Nivel promedio de agua (proporción 0-1)
  - `min_level`: Nivel mínimo observado (proporción 0-1)
  - `max_level`: Nivel máximo observado (proporción 0-1)
  - `level_std`: Desviación estándar del nivel
  - `level_variability`: Variabilidad del nivel (%)
  - `uptime_status`: Estado cualitativo ('excellent', 'good', 'acceptable', 'poor')
  - `time_span_hours`: Tiempo total analizado (horas)
  - `low_threshold`: Umbral de nivel bajo (0.2 = 20%)
  - `low_count`: Lecturas por debajo del umbral bajo
  - `normal_count`: Lecturas en rango normal
  - `high_count`: Lecturas por encima del máximo (overflow)
  - `low_percent`: Porcentaje de tiempo en nivel bajo
  - `normal_percent`: Porcentaje de tiempo en nivel normal
  - `high_percent`: Porcentaje de tiempo en overflow
  - `excellent_threshold`: Umbral excelente (98.0%)
  - `good_threshold`: Umbral bueno (95.0%)
  - `acceptable_threshold`: Umbral aceptable (90.0%)
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

#### **7. Endpoint `availability` Mejorado**
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

#### **8. Endpoint `performance` Mejorado**
- **Metadatos adicionales**:
  - `actual_liters`: Litros reales dispensados
  - `expected_liters`: Litros esperados según configuración
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
- **`excellent`**: ≥ 1.05 (utilización de capacidad excelente, ≥105%)
- **`good`**: ≥ 0.95 (utilización de capacidad buena, ≥95%)
- **`acceptable`**: ≥ 0.85 (utilización de capacidad aceptable, ≥85%)
- **`poor`**: ≥ 0.70 (utilización de capacidad deficiente, ≥70%)
- **`critical`**: < 0.70 (utilización de capacidad crítica, <70%)

**Funcionalidades:**
- **Parámetros configurables**: `users` y `hours` para personalizar expectativas
- **Análisis de eficiencia**: Comparación real vs esperado con métricas detalladas
- **Alertas automáticas**: Advertencias para déficit, excedente y rendimiento crítico
- **Análisis de flujo**: Estadísticas detalladas del flujo observado vs configurado

#### **9. Endpoint `quality` Mejorado**
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

#### **3. Corrección de Endpoint `response_index`**
- **Problema**: Error 404 debido a importación incorrecta de `classify_anomalies`
- **Solución**: Creación de función auxiliar local para clasificación de anomalías
- **Resultado**: Endpoint funcional que devuelve tiempo medio de respuesta a anomalías

### **Correcciones en Detección de Anomalías**

#### **1. Coherencia de Setpoints de Temperatura**
- **Problema**: Inconsistencia entre `temperature_setpoint = 25°C` y `SETPOINT_TEMP_DEFAULT = 60°C`
- **Solución**: Unificación del uso de `SETPOINT_TEMP_DEFAULT = 60°C` en todas las anomalías
- **Resultado**: Reducción de falsos positivos en detección de anomalías de temperatura

#### **2. Ajuste de Umbrales de Potencia**
- **Problema**: Umbral de potencia demasiado alto (`POWER_HIGH_THRESHOLD = 8.0 kW`)
- **Solución**: Reducción a `POWER_HIGH_THRESHOLD = 6.5 kW`
- **Ajustes adicionales**:
  - `POWER_MAX`: 10.0 kW → 8.0 kW
  - `HEATER_POWER_MAX`: 10.0 kW → 8.0 kW
- **Resultado**: Detección más realista de anomalías de consumo energético

### **Mejoras en Frontend**

#### **1. Dashboard de Métricas Mejorado**
- **Tooltip corregido**: Muestra valores correctos en lugar de "0"
- **Prevención de llamadas múltiples**: Implementación de `useRef` para evitar re-renders
- **Metadatos adicionales**: Visualización de información extra en gauges
- **Imports optimizados**: Eliminación de imports no utilizados

#### **2. Visualización de Información Adicional**
- **Gauge de Calidad**: Muestra setpoint, tolerancia y conteo de lecturas
- **Gauge de Eficiencia Energética**: Muestra valor esperado, tolerancia, ratio y consumos totales
- **Gauge de Variación Térmica**: Muestra temperatura promedio, rango, setpoint y estado de control
- **Gauge de Peak Flow Ratio**: Muestra flujos máximo, promedio, nominal y estado de control
- **Gauge de MTBA**: Muestra intervalos mínimo/máximo, tasa de anomalías, estado de estabilidad y distribución por sensor
- **Gauge de Level Uptime**: Muestra nivel promedio, rango, variabilidad, distribución de niveles y estado de disponibilidad
- **Gauge de Availability**: Muestra flujo promedio, rango, volumen total, distribución de flujo y estado de utilización
- **Gauge de Performance**: Muestra litros reales vs esperados, eficiencia, estado de rendimiento y análisis de flujo
- **Gauge de Quality**: Muestra temperatura promedio, rango, variabilidad, distribución térmica y estado de control
- **Colores Dinámicos**: Los gauges cambian de color según el estado:
  - 🟢 Verde: Estado 'excellent'
  - 🔵 Azul: Estado 'good' 
  - 🟡 Amarillo: Estado 'acceptable'
  - 🟠 Naranja: Estado 'poor'
  - 🔴 Rojo: Estado 'critical'/'excessive'
- **Alertas Visuales**: Muestra advertencias cuando:
  - ⚠️ Outside tolerance (fuera de tolerancia)
  - ⚠️ Exceeds pipe capacity (excede capacidad del tubo)
  - ⚠️ Below pipe minimum (por debajo del mínimo del tubo)

### **Correcciones Técnicas**

#### **1. Deprecation Warnings**
- **Problema**: Uso de `datetime.utcnow()` (deprecado)
- **Solución**: Reemplazo por `datetime.now(datetime.UTC)`
- **Archivos afectados**: `simulate_endpoints.py`, `simulator.py`

#### **2. Corrección de Endpoint de Simulación**
- **Problema**: Endpoint `/simulate` devolvía 404
- **Solución**: Corrección de ruta de `@router.post('/simulate')` a `@router.post('/')`
- **Resultado**: Simulación funcional con parámetros `hours` y `users`

### **Estadísticas de Mejora**
- **Anomalías de temperatura**: Reducción de 100+ falsos positivos a 38 anomalías reales
- **Anomalías de potencia**: Ajuste de 11 a 12 anomalías reales (umbral más apropiado)
- **Eficiencia energética**: Valores teóricamente calculados y coherentes
- **Frontend**: Eliminación de warnings de ESLint y mejor rendimiento

---

---

## Prerrequisitos

- **Git**
- **Python 3.10+** y **pip**
- **Node.js 16+** y **npm**

---

## Backend (Python)

### ⚙️ Instalación
```bash
cd backend
python3 -m venv venv
source venv/bin/activate    # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### ⚙️ Ejecución
```bash
uvicorn api:app --reload
```
- Documentación Swagger: http://localhost:8000/docs


---

## 📦 Estructura del Proyecto

- **`api.py`**: aplicación principal FastAPI que integra todos los routers.
- **`anomalies_endpoints.py`**: endpoints para detección de anomalías (fijos, adaptativos y clasificación).
- **`metrics_endpoints.py`**: endpoints para cálculo de métricas OEE adaptadas.
- **`readings_endpoints.py`**: endpoints CRUD de lecturas de sensores.
- **`simulate_endpoints.py`**: endpoints para simulación de datos individuales y por escenarios.
- **`simulator.py`**: motor de simulación de sensores con parámetros ajustables y memoria de estado.
- **`storage.py`**: persistencia de datos en SQLite mediante pandas.
- **`settings.py`**: configuración global de umbrales y constantes.
- **`frontend/`**: interfaz React para interactuar con el backend.

---

## ⚙️ Configuración Actualizada

### **Umbrales de Anomalías (settings.py)**
```python
# Temperatura
SETPOINT_TEMP_DEFAULT = 60.0   # °C (setpoint de temperatura)
TMP_TOLERANCE = 2.0            # ±2°C (tolerancia para anomalías)

# Flujo
FLOW_INACTIVITY_THRESHOLD = 0.001  # L/min (umbral de inactividad)
FLOW_INACTIVITY_MINUTES = 5        # minutos (duración mínima de inactividad)

# Nivel
LEVEL_LOW_THRESHOLD = 0.2      # 20% (umbral de nivel bajo)

# Potencia (ajustado recientemente)
POWER_HIGH_THRESHOLD = 6.5     # kW (umbral de consumo alto)
POWER_MAX = 8.0                # kW (máxima potencia del simulador)
HEATER_POWER_MAX = 8.0         # kW (máxima potencia del calentador)
```

### **Métricas Mejoradas**
```python
# Eficiencia Energética
EXPECTED_EFFICIENCY = 0.051    # kWh/L (valor esperado teórico)
EFFICIENCY_TOLERANCE = 0.025   # kWh/L (tolerancia ±50%)

# Calidad
TEMPERATURE_VARIATION = 5.0    # °C (banda de tolerancia para calidad)
```

### Endpoints
## 🚀 Endpoints de la API

### Lecturas de Sensores (`readings_endpoints.py`)
- `GET /readings`
  - Devuelve todas las lecturas almacenadas.
- `GET /readings/latest`
  - Devuelve la lectura más reciente de cada sensor.
- `DELETE /readings`
  - Elimina todas las lecturas.

### Simulación (`simulate_endpoints.py`)
- `POST /simulate?hours={h}&users={u}`
  - Genera datos de simulación continuos durante `h` horas con `u` usuarios.
- `POST /simulate_scenarios?duration_hours={d}`
  - Recibe un array de configuraciones (`users`, `flow_rate`, `temp_setpoint`, `heater_regime`).
  - Devuelve métricas agregadas (energía total, temperatura promedio) para cada escenario.

### Detección de Anomalías (`anomalies_endpoints.py`)
- `GET /anomalies/static`
  - Umbrales fijos: sobretemperatura, inactividad, nivel bajo, consumo alto.
- `GET /anomalies/adaptive?window={n}&sensor={s}`
  - Umbrales adaptativos: detecta valores con z-score > 2 en ventana móvil de `n` lecturas.
- `GET /anomalies/classify?window={n}&sensor={s}`
  - Clasifica anomalías en `leakage`, `sensor_error`, `overuse`, `other`.

### Métricas de Desempeño (`metrics_endpoints.py`)
- `GET /metrics/availability?start={t0}&end={t1}`
  - Disponibilidad: % de tiempo con flujo > 0.
- `GET /metrics/performance?users={u}&hours={h}`
  - Rendimiento: ratio de litros reales vs. esperados (basado en 0.008 L/min por usuario, solo agua para beber). 1.0 = exacto, >1.0 = más de lo esperado, <1.0 = menos de lo esperado.
- `GET /metrics/quality?start={t0}&end={t1}`
  - Calidad: % temperatura dentro de ±5°C del setpoint (60°C). Incluye metadatos adicionales.
- `GET /metrics/energy_efficiency?start={t0}&end={t1}`
  - Eficiencia Energética: kWh/L. Valor esperado: 0.051 kWh/L, tolerancia: ±0.025 kWh/L.
- `GET /metrics/thermal_variation?start={t0}&end={t1}`
  - Variación Térmica: desviación estándar.
- `GET /metrics/nonproductive_consumption?start={t0}&end={t1}`
  - Consumo No Productivo: kWh en inactividad.
- `GET /metrics/peak_flow_ratio?users={u}`
  - Flujo Pico: max flujo / nominal.
- `GET /metrics/mtba?window={n}&sensor={s}`
  - MTBA: tiempo medio entre adaptativas.
- `GET /metrics/response_index?window={n}&sensor={s}`
  - Índice de Respuesta: minutos a recuperación.
- `GET /metrics/mtbf?start={t0}&end={t1}`
  - MTBF: tiempo medio entre fallas (horas).
- `GET /metrics/quality_full?start={t0}&end={t1}`
  - Calidad Completa: % servicios con temperatura y volumen correctos.
- `GET /metrics/response_time?start={t0}&end={t1}`
  - Tiempo de Respuesta: tiempo medio selección→dispensado (segundos).
- `GET /metrics/failures_count?weeks={n}`
  - Conteo de Fallas: número de fallas en las últimas `n` semanas.
- `GET /metrics/usage_rate?start={t0}&end={t1}`
  - Tasa de Uso: promedio de servicios por hora.

---

## 📊 Detalle de KPIs

| Categoría            | KPI Sugerido                                       | Unidad / Método de Medición                   | Endpoint                          |
| -------------------- | -------------------------------------------------- | --------------------------------------------- | --------------------------------- |
| **Disponibilidad**   | % de tiempo operativo                              | (Tiempo operativo / Total disponible) × 100   | `/metrics/availability`           |
| **Energía**          | Consumo por litro dispensado                       | kWh / L                                       | `/metrics/energy_efficiency`      |
| **Mantenimiento**    | Tiempo medio entre fallas (MTBF)                   | Promedio de horas entre interrupciones        | `/metrics/mtbf` (nuevo)           |
| **Calidad**          | % de servicios con temperatura y volumen correctos | (Servicios correctos / Total servicios) × 100 | `/metrics/quality_full` (nuevo)   |
| **Tiempo de Respuesta** | Promedio de espera entre selección y dispensado    | Segundos                                      | `/metrics/response_time` (nuevo)  |
| **Fallos**           | Número de fallos por semana                        | Conteo automático de errores                  | `/metrics/failures_count` (nuevo) |
| **Uso**              | Promedio de servicios por franja horaria           | Servicios/hora (segmentado por turno)         | `/metrics/usage_rate` (nuevo)     |

---

## ⚙️ Componentes del OEE Adaptados

| Componente     | Descripción                                                                | Fórmula                                            | Endpoint                |
| -------------- | -------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------- |
| **Disponibilidad** | Tiempo que el equipo estuvo operativo respecto al tiempo total disponible  | (Tiempo operativo / Tiempo total disponible) × 100 | `/metrics/availability` |
| **Rendimiento**    | Relación entre el volumen real dispensado y el volumen esperado            | (Volumen real dispensado / Volumen esperado) × 100 | `/metrics/performance`  |
| **Calidad**        | Porcentaje de servicios correctamente ejecutados (temp. y flujo adecuados) | (Servicios correctos / Total servicios) × 100      | `/metrics/quality_full` |

---

## Frontend

### ⚙️ Instalación y ejecución
```bash
cd frontend
npm install
npm install react-router-dom recharts react-bootstrap bootstrap
```
En `src/index.js`, agrega:
```js
import 'bootstrap/dist/css/bootstrap.min.css';
```

```bash
npm start
```
Abre http://localhost:3000.


---


Este README provee una revisión comprensible del proyecto, como instalar y correr, tanto el frontend como el backend. Además muestra un detalle de las APIs.

---

## 📈 Estado Actual del Proyecto

### **✅ Funcionalidades Completadas**
- ✅ Simulación de sensores IoT (temperatura, flujo, nivel, potencia)
- ✅ Detección de anomalías estáticas y adaptativas
- ✅ Cálculo de métricas OEE adaptadas
- ✅ Dashboard interactivo con visualizaciones
- ✅ API REST completa con documentación Swagger
- ✅ Corrección de inconsistencias en umbrales y setpoints
- ✅ Mejora de endpoints con metadatos adicionales
- ✅ Optimización del frontend y eliminación de warnings

### **🔧 Mejoras Recientes Implementadas**
- 🔧 Endpoint `energy_efficiency` con valores teóricos realistas
- 🔧 Endpoint `quality` con metadatos adicionales
- 🔧 Corrección de endpoint `response_index` (404 → funcional)
- 🔧 Unificación de setpoints de temperatura (25°C → 60°C)
- 🔧 Ajuste de umbrales de potencia (8.0 kW → 6.5 kW)
- 🔧 Optimización del frontend (tooltips, re-renders, imports)

### **📊 Métricas de Calidad**
- **Anomalías de temperatura**: 38 anomalías reales (vs 100+ falsos positivos)
- **Anomalías de potencia**: 12 anomalías reales (umbral optimizado)
- **Eficiencia energética**: Valores teóricamente calculados
- **Frontend**: Sin warnings de ESLint, mejor rendimiento

Feliz monitoreo!  🚰📊