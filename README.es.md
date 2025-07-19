# Proyecto Industria 4.0: Expendedor de Agua Inteligente

**Introducción:**
Este proyecto implementa un sistema de expendedor de agua inteligente inspirado en la Industria 4.0. Permite simular el comportamiento de sensores IoT, almacenar datos históricos, detectar anomalías y evaluar métricas de desempeño en tiempo real. Está diseñado para demostrar la viabilidad de tecnologías clave (IoT simulado, gemelos digitales, analítica y dashboards interactivos) en entornos con recursos limitados como PYMES o instituciones educativas.

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
  - Rendimiento: litros reales vs. esperados.
- `GET /metrics/quality?start={t0}&end={t1}`
  - Calidad: % temperatura dentro de ±5°C del setpoint.
- `GET /metrics/energy_efficiency?start={t0}&end={t1}`
  - Eficiencia Energética: kWh/L.
- `GET /metrics/thermal_variation?start={t0}&end={t1}`
  - Variación Térmica: desviación estándar de temperatura.
- `GET /metrics/peak_flow_ratio?users={u}`
  - Flujo Pico: max flujo / nominal.
- `GET /metrics/mtba?window={n}&sensor={s}`
  - MTBA: tiempo medio entre anomalías adaptativas.
- `GET /metrics/level_uptime?start={t0}&end={t1}`
  - Tiempo de Nivel: % de tiempo con nivel entre umbral bajo y lleno.
- `GET /metrics/response_index?window={n}&sensor={s}`
  - Índice de Respuesta: tiempo medio de respuesta a anomalías adaptativas.
- `GET /metrics/nonproductive_consumption?start={t0}&end={t1}`
  - Consumo No Productivo: kWh consumidos cuando flujo ≤ umbral.
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
| **Rendimiento**      | Eficiencia de volumen dispensado                   | (Volumen real / Volumen esperado) × 100       | `/metrics/performance`            |
| **Calidad**          | % de servicios con temperatura correcta            | (Servicios correctos / Total servicios) × 100 | `/metrics/quality`                |
| **Calidad Completa** | % de servicios con temperatura y volumen correctos | (Servicios correctos / Total servicios) × 100 | `/metrics/quality_full`           |
| **Energía**          | Consumo por litro dispensado                       | kWh / L                                       | `/metrics/energy_efficiency`      |
| **Consumo No Productivo** | Consumo energético en inactividad                 | kWh cuando flujo ≤ umbral                     | `/metrics/nonproductive_consumption` |
| **Variación Térmica** | Estabilidad de temperatura                         | Desviación estándar de temperatura (°C)       | `/metrics/thermal_variation`      |
| **Flujo Pico**       | Relación flujo máximo vs nominal                   | (Flujo máximo / Flujo nominal)                | `/metrics/peak_flow_ratio`        |
| **Tiempo de Nivel**  | % de tiempo con nivel adecuado                     | (Tiempo nivel correcto / Total tiempo) × 100  | `/metrics/level_uptime`           |
| **MTBA**             | Tiempo medio entre anomalías adaptativas           | Promedio de minutos entre anomalías           | `/metrics/mtba`                   |
| **Índice de Respuesta** | Tiempo de respuesta a anomalías                   | Promedio de minutos de respuesta              | `/metrics/response_index`         |
| **MTBF**             | Tiempo medio entre fallas                          | Promedio de horas entre fallas                | `/metrics/mtbf`                   |
| **Tiempo de Respuesta** | Promedio de espera selección→dispensado           | Segundos                                      | `/metrics/response_time`          |
| **Conteo de Fallas** | Número de fallas por semana                        | Conteo automático de errores                  | `/metrics/failures_count`         |
| **Tasa de Uso**      | Promedio de servicios por hora                     | Servicios/hora                               | `/metrics/usage_rate`             |

---

## 🔧 Mejoras Recientes (v1.1.0)

### Metadatos Enriquecidos
Todos los endpoints de métricas ahora incluyen metadatos detallados para análisis avanzado:

#### Estados Cualitativos
- **`excellent`**: Rendimiento excepcional (verde)
- **`good`**: Rendimiento bueno (azul)
- **`acceptable`**: Rendimiento aceptable (amarillo)
- **`poor`**: Rendimiento deficiente (rojo)
- **`low`**: Rendimiento bajo (naranja, solo para `usage_rate`)

#### Metadatos Comunes
- **Status**: Estado cualitativo del sistema
- **Time Span**: Período de tiempo analizado
- **Samples**: Número de muestras procesadas
- **Expected Value**: Valor esperado para comparación
- **Thresholds**: Umbrales de clasificación

#### Metadatos Específicos por Métrica
- **`failures_count`**: Análisis por tipo de falla (temperatura, flujo, nivel, potencia)
- **`usage_rate`**: Patrones de uso, horas pico, intervalos entre servicios
- **`quality`**: Desviaciones de temperatura, distribución de lecturas
- **`performance`**: Eficiencia, déficit/excedente de volumen
- **`energy_efficiency`**: Ratio de eficiencia, consumo total
- **`availability`**: Distribución de flujo, volumen total
- **`mtba`**: Tasa de anomalías, distribución por sensor
- **`response_index`**: Tiempos de respuesta, distribución por velocidad
- **`mtbf`**: Análisis de confiabilidad, distribución de fallas
- **`response_time`**: Categorización de respuestas por velocidad
- **`quality_full`**: Análisis de servicios correctos vs incorrectos
- **`nonproductive_consumption`**: Análisis de períodos productivos vs no productivos
- **`thermal_variation`**: Estabilidad térmica, desviaciones del setpoint
- **`peak_flow_ratio`**: Análisis de capacidad vs flujo real
- **`level_uptime`**: Análisis de disponibilidad de agua

### Frontend Optimizado
- **Dashboard simplificado**: Reducción del 70% en información mostrada
- **Status prominente**: Estados de salud destacados visualmente
- **Alertas inteligentes**: Mensajes de advertencia contextuales
- **Estructura consistente**: Formato uniforme para todas las métricas

---

## ⚙️ Componentes del OEE Adaptados

| Componente     | Descripción                                                                | Fórmula                                            | Endpoint                |
| -------------- | -------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------- |
| **Disponibilidad** | Tiempo que el equipo estuvo operativo respecto al tiempo total disponible  | (Tiempo operativo / Tiempo total disponible) × 100 | `/metrics/availability` |
| **Rendimiento**    | Relación entre el volumen real dispensado y el volumen esperado            | (Volumen real dispensado / Volumen esperado) × 100 | `/metrics/performance`  |
| **Calidad**        | Porcentaje de servicios correctamente ejecutados (temp. y flujo adecuados) | (Servicios correctos / Total servicios) × 100      | `/metrics/quality_full` |

### Métricas Complementarias OEE

| Métrica Complementaria | Descripción | Endpoint |
| ---------------------- | ----------- | -------- |
| **Eficiencia Energética** | Consumo energético por litro dispensado | `/metrics/energy_efficiency` |
| **Confiabilidad** | Tiempo medio entre fallas y conteo de fallas | `/metrics/mtbf`, `/metrics/failures_count` |
| **Utilización** | Patrones de uso y tasa de servicios | `/metrics/usage_rate` |
| **Estabilidad Térmica** | Control de temperatura y variaciones | `/metrics/thermal_variation` |
| **Tiempo de Respuesta** | Velocidad de respuesta del sistema | `/metrics/response_time` |
| **Gestión de Anomalías** | Detección y respuesta a anomalías | `/metrics/mtba`, `/metrics/response_index` |

---

## 📋 Ejemplos de Uso

### Análisis de Confiabilidad del Sistema
```bash
# Obtener análisis de fallas de las últimas 2 semanas
curl "http://localhost:8000/metrics/failures_count?weeks=2"

# Respuesta incluye:
# - reliability_status: 'excellent'/'good'/'acceptable'/'poor'
# - total_failures: número total de fallas
# - failures_per_week: tasa semanal
# - Análisis por tipo: temp_failures, flow_failures, level_failures, power_failures
```

### Análisis de Patrones de Uso
```bash
# Obtener análisis de utilización del sistema
curl "http://localhost:8000/metrics/usage_rate?start=2024-12-01T00:00:00&end=2024-12-07T23:59:59"

# Respuesta incluye:
# - utilization_status: 'excellent'/'good'/'acceptable'/'low'/'poor'
# - total_services: servicios totales
# - services_per_day: servicios por día
# - peak_hour_ratio: ratio de hora pico vs promedio
# - busy_period_percent: % de períodos ocupados
```

### Monitoreo de Calidad en Tiempo Real
```bash
# Obtener estado de calidad del sistema
curl "http://localhost:8000/metrics/quality"

# Respuesta incluye:
# - quality_status: estado cualitativo
# - within_percent: % de lecturas dentro del rango
# - avg_temp: temperatura promedio
# - Alertas automáticas si quality_status es 'poor'
```

### Análisis de Eficiencia Energética
```bash
# Obtener análisis de eficiencia energética
curl "http://localhost:8000/metrics/energy_efficiency"

# Respuesta incluye:
# - efficiency_status: estado de eficiencia
# - efficiency_ratio: ratio vs valor esperado
# - total_kwh: consumo total
# - total_liters: volumen total
```

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
Feliz monitoreo!  🚰📊