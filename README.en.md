# Industry 4.0 Project: Smart Water Dispenser Digital Twin

**Introduction:**
This repository contains an implementation of a Digital Twin for a hot/cold water dispenser, including simulated IoT sensors, local data storage, anomaly detection, and real-time performance metrics evaluation. It demonstrates the feasibility of key Industry 4.0 technologies (simulated IoT, digital twins, analytics, and interactive dashboards) in resource-constrained environments like SMEs or educational institutions.

---

## Prerequisites

- **Git**
- **Python 3.10+** and **pip**
- **Node.js 16+** and **npm**

---

## Backend (Python)

### ⚙️ Installation
```bash
cd backend
python3 -m venv venv
source venv/bin/activate    # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### ⚙️ Execution
```bash
uvicorn api:app --reload
```
- Swagger Documentation: http://localhost:8000/docs


---

## 📦 Project Structure

- **`api.py`**: main FastAPI application that integrates all routers.
- **`anomalies_endpoints.py`**: endpoints for anomaly detection (fixed, adaptive, and classification).
- **`metrics_endpoints.py`**: endpoints for adapted OEE metrics calculation.
- **`readings_endpoints.py`**: CRUD endpoints for sensor readings.
- **`simulate_endpoints.py`**: endpoints for individual data simulation and scenarios.
- **`simulator.py`**: sensor simulation engine with adjustable parameters and state memory.
- **`storage.py`**: SQLite data persistence using pandas.
- **`settings.py`**: global configuration of thresholds and constants.
- **`frontend/`**: React interface to interact with the backend.


### Endpoints
## 🚀 API Endpoints

### Sensor Readings (`readings_endpoints.py`)
- `GET /readings`
  - Returns all stored readings.
- `GET /readings/latest`
  - Returns the most recent reading from each sensor.
- `DELETE /readings`
  - Deletes all readings.

### Simulation (`simulate_endpoints.py`)
- `POST /simulate?hours={h}&users={u}`
  - Generates continuous simulation data for `h` hours with `u` users.
- `POST /simulate_scenarios?duration_hours={d}`
  - Receives an array of configurations (`users`, `flow_rate`, `temp_setpoint`, `heater_regime`).
  - Returns aggregated metrics (total energy, average temperature) for each scenario.

### Anomaly Detection (`anomalies_endpoints.py`)
- `GET /anomalies/static`
  - Fixed thresholds: overtemperature, inactivity, low level, high consumption.
- `GET /anomalies/adaptive?window={n}&sensor={s}`
  - Adaptive thresholds: detects values with z-score > 2 in rolling window of `n` readings.
- `GET /anomalies/classify?window={n}&sensor={s}`
  - Classifies anomalies into `leakage`, `sensor_error`, `overuse`, `other`.

### Performance Metrics (`metrics_endpoints.py`)
- `GET /metrics/availability?start={t0}&end={t1}`
  - Availability: % of time with flow > 0.
- `GET /metrics/performance?users={u}&hours={h}`
  - Performance: actual vs expected liters.
- `GET /metrics/quality?start={t0}&end={t1}`
  - Quality: % temperature within ±1°C of setpoint.
- `GET /metrics/energy_efficiency?start={t0}&end={t1}`
  - Energy Efficiency: kWh/L.
- `GET /metrics/thermal_variation?start={t0}&end={t1}`
  - Thermal Variation: standard deviation.
- `GET /metrics/nonproductive_consumption?start={t0}&end={t1}`
  - Nonproductive Consumption: kWh during inactivity.
- `GET /metrics/peak_flow_ratio?users={u}`
  - Peak Flow: max flow / nominal.
- `GET /metrics/mtba?window={n}&sensor={s}`
  - MTBA: mean time between adaptive anomalies.
- `GET /metrics/response_index?window={n}&sensor={s}`
  - Response Index: minutes to recovery.

---

## Frontend

### ⚙️ Installation and execution
```bash
cd frontend
npm install
npm install react-router-dom recharts react-bootstrap bootstrap
```
In `src/index.js`, add:
```js
import 'bootstrap/dist/css/bootstrap.min.css';
```

```bash
npm start
```
Open http://localhost:3000.


---


This README provides a comprehensive overview of the project, how to install and run both frontend and backend. It also shows detailed information about the APIs.
Happy monitoring!  🚰📊