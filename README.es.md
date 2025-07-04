# Proyecto Industria 4.0: Expendedor de Agua Inteligente

**Introducción:**
Este proyecto implementa un sistema de expendedor de agua inteligente inspirado en la Industria 4.0. Permite simular el comportamiento de sensores IoT, almacenar datos históricos, detectar anomalías y evaluar métricas de desempeño en tiempo real. Está diseñado para demostrar la viabilidad de tecnologías clave (IoT simulado, gemelos digitales, analítica y dashboards interactivos) en entornos con recursos limitados como PYMES o instituciones educativas.

---

## Prerrequisitos

- **Git**
- **Python 3.10+** y **pip**
- **Node.js 16+** y **npm**

---

## Backend

### Instalación
```bash
cd backend
python3 -m venv venv
source venv/bin/activate    # Windows: venv\\Scripts\\activate
pip install -i requirements.txt
```

### Ejecución
```bash
uvicorn api:app --reload
```
- Documentación Swagger: http://localhost:8000/docs

### Endpoints

#### Lecturas de sensores
| Método | Ruta                      | Descripción                                |
| ------ | ------------------------- | ------------------------------------------ |
| GET    | `/readings`               | Retorna todas las lecturas.                |
| GET    | `/readings/latest`        | Lectura más reciente.                      |
| DELETE | `/readings`               | Elimina todas las lecturas.                |
| POST   | `/simulate?hours=&users=` | Simula datos para `hours` horas y `users` usuarios. |

#### Detección de anomalías
| Método | Ruta           | Descripción                                                   |
| ------ | -------------- | ------------------------------------------------------------- |
| GET    | `/anomalies`   | Detecta sobretemperaturas, inactividad, nivel bajo y consumo alto. |

#### Métricas (`/metrics/...`)
| Ruta                                  | Parámetros             | Descripción                                                     |
| ------------------------------------- | ---------------------- | --------------------------------------------------------------- |
| `/metrics/availability`               | `start`, `end`         | % tiempo con flujo > 0.                                         |
| `/metrics/performance`                | `users`, `hours`       | Litros reales vs esperados.                                     |
| `/metrics/quality`                    | `start`, `end`         | % temperaturas dentro de ±1°C del setpoint.                     |
| `/metrics/energy_efficiency`          | `start`, `end`         | kWh consumidos por litro dispensado.                            |
| `/metrics/peak_flow_ratio`            | `users`                | Flujo máximo / flujo nominal por usuario.                       |
| `/metrics/mtba`                       | —                      | Tiempo medio entre anomalías (minutos).                         |
| `/metrics/level_uptime`               | `start`, `end`         | % tiempo nivel entre 20% y 100%.                                |
| `/metrics/response_index`             | —                      | Minutos promedio hasta recuperación tras anomalía.              |
| `/metrics/thermal_variation`          | `start`, `end`         | Desviación estándar de temperatura (°C).                        |
| `/metrics/nonproductive_consumption`  | `start`, `end`         | kWh consumidos con flujo ≤ umbral de inactividad.               |

Para incluir rutas de métricas en `api.py`:
```python
from api_metrics_endpoints import router as metrics_router
app.include_router(metrics_router)
```

---

## Frontend

### Instalación y ejecución
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

### Estructura de archivos

- `index.js`: Renderiza `<App />` envuelto en `<BrowserRouter>`.
- `App.jsx`: Menú de navegación y `<Routes>`.
- `MainPage.jsx`: Página principal con enlaces.
- `SimulatePage.jsx`: Simulación de uso, grilla de lecturas y limpieza de datos.
- `AnalyticsPage.jsx`: Dashboard de gráficas con `AnalyticsDashboard.jsx`.
- `AnomaliesPage.jsx`: Tablas agrupadas por sensor con `AnomaliesDashboard.jsx`.
- `MetricsPage.jsx`: Dashboard de métricas con Radar y Gauges (`MetricsDashboard.jsx`).

---

## Configuración del Simulador (`simulator.py`)

Constantes configurables al inicio del archivo:
- `AVG_FLOW_RATE_DEFAULT`: L/h por usuario.
- `TIME_CONVERSION`: Conversión L/h → L/min.
- `TEMPERATURE_MEAN`, `TEMPERATURE_VARIATION`: Parámetros de temperatura.
- `LEVEL_MIN`, `LEVEL_MAX`: Rango de nivel de tanque (0–1).
- `POWER_MIN`, `POWER_MAX`: Rango de potencia (kW).

La función `generate_frame(timestamp, users, sensor, value)` permite:
- `timestamp=None`: Usa hora UTC actual.
- `sensor`: Generar solo ese sensor.
- `value`: Anular valor simulado si no es `None`.


---

Este README provee una revisión comprensible del proyecto, como instalar y correr, tanto el frontend como el backend. Además muestra un detalle de las APIs.
Feliz monitoreo!  🚰📊