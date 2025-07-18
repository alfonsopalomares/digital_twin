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
  - Performance: ratio of actual vs expected liters (based on 0.008 L/min per user, drinking water only). 1.0 = exact, >1.0 = more than expected, <1.0 = less than expected.
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
- `GET /metrics/mtbf?start={t0}&end={t1}`
  - MTBF: mean time between failures (hours).
- `GET /metrics/quality_full?start={t0}&end={t1}`
  - Full Quality: % services with correct temperature and volume.
- `GET /metrics/response_time?start={t0}&end={t1}`
  - Response Time: average time selection→dispense (seconds).
- `GET /metrics/failures_count?weeks={n}`
  - Failures Count: number of failures in the last `n` weeks.
- `GET /metrics/usage_rate?start={t0}&end={t1}`
  - Usage Rate: average services per hour.

---

## 📊 KPI Details

| Category           | Suggested KPI                                      | Unit / Measurement Method                       | Endpoint                          |
| ------------------ | -------------------------------------------------- | ----------------------------------------------- | --------------------------------- |
| **Availability**   | % of operational time                              | (Operational time / Total available) × 100     | `/metrics/availability`           |
| **Energy**         | Consumption per dispensed liter                    | kWh / L                                        | `/metrics/energy_efficiency`      |
| **Maintenance**    | Mean time between failures (MTBF)                 | Average hours between interruptions             | `/metrics/mtbf` (new)             |
| **Quality**        | % of services with correct temperature and volume | (Correct services / Total services) × 100      | `/metrics/quality_full` (new)     |
| **Response Time**  | Average wait time between selection and dispense  | Seconds                                        | `/metrics/response_time` (new)    |
| **Failures**       | Number of failures per week                       | Automatic error counting                        | `/metrics/failures_count` (new)   |
| **Usage**          | Average services per time slot                    | Services/hour (segmented by shift)             | `/metrics/usage_rate` (new)       |

---

## ⚙️ Adapted OEE Components

| Component      | Description                                                                | Formula                                            | Endpoint                |
| -------------- | -------------------------------------------------------------------------- | -------------------------------------------------- | ----------------------- |
| **Availability** | Time the equipment was operational relative to total available time       | (Operational time / Total available time) × 100   | `/metrics/availability` |
| **Performance**  | Relationship between actual dispensed volume and expected volume          | (Actual dispensed volume / Expected volume) × 100 | `/metrics/performance`  |
| **Quality**      | Percentage of correctly executed services (temp. and flow adequate)       | (Correct services / Total services) × 100         | `/metrics/quality_full` |

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