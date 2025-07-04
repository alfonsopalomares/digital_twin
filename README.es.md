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
  - Calidad: % temperatura dentro de ±1°C del setpoint.
- `GET /metrics/energy_efficiency?start={t0}&end={t1}`
  - Eficiencia Energética: kWh/L.
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