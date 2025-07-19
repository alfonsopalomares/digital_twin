# Industry 4.0 Project: Smart Water Dispenser

**Introduction:**
This project implements a smart water dispenser system inspired by Industry 4.0. It allows simulating IoT sensor behavior, storing historical data, detecting anomalies, and evaluating real-time performance metrics. It is designed to demonstrate the feasibility of key technologies (simulated IoT, digital twins, analytics, and interactive dashboards) in resource-limited environments such as SMEs or educational institutions.

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
  - Adaptive thresholds: detects values with z-score > 2 in sliding window of `n` readings.
- `GET /anomalies/classify?window={n}&sensor={s}`
  - Classifies anomalies into `leakage`, `sensor_error`, `overuse`, `other`.

### Performance Metrics (`metrics_endpoints.py`)
- `GET /metrics/availability?start={t0}&end={t1}`
  - Availability: % of time with flow > 0.
- `GET /metrics/performance?users={u}&hours={h}`
  - Performance: actual vs expected liters.
- `GET /metrics/quality?start={t0}&end={t1}`
  - Quality: % temperature within ±5°C of setpoint.
- `GET /metrics/energy_efficiency?start={t0}&end={t1}`
  - Energy Efficiency: kWh/L.
- `GET /metrics/thermal_variation?start={t0}&end={t1}`
  - Thermal Variation: temperature standard deviation.
- `GET /metrics/peak_flow_ratio?users={u}`
  - Peak Flow: max flow / nominal.
- `GET /metrics/mtba?window={n}&sensor={s}`
  - MTBA: mean time between adaptive anomalies.
- `GET /metrics/level_uptime?start={t0}&end={t1}`
  - Level Uptime: % of time with level between low threshold and full.
- `GET /metrics/response_index?window={n}&sensor={s}`
  - Response Index: mean response time to adaptive anomalies.
- `GET /metrics/nonproductive_consumption?start={t0}&end={t1}`
  - Nonproductive Consumption: kWh consumed when flow ≤ threshold.
- `GET /metrics/mtbf?start={t0}&end={t1}`
  - MTBF: mean time between failures (hours).
- `GET /metrics/quality_full?start={t0}&end={t1}`
  - Full Quality: % services with correct temperature and volume.
- `GET /metrics/response_time?start={t0}&end={t1}`
  - Response Time: mean time selection→dispense (seconds).
- `GET /metrics/failures_count?weeks={n}`
  - Failures Count: number of failures in the last `n` weeks.
- `GET /metrics/usage_rate?start={t0}&end={t1}`
  - Usage Rate: average services per hour.

---

## 📊 KPI Details

| Category              | Suggested KPI                                      | Unit / Measurement Method                      | Endpoint                          |
| --------------------- | -------------------------------------------------- | --------------------------------------------- | --------------------------------- |
| **Availability**      | % of operational time                              | (Operational time / Total available) × 100    | `/metrics/availability`           |
| **Performance**       | Dispensed volume efficiency                        | (Actual volume / Expected volume) × 100       | `/metrics/performance`            |
| **Quality**           | % of services with correct temperature             | (Correct services / Total services) × 100     | `/metrics/quality`                |
| **Full Quality**      | % of services with correct temperature and volume  | (Correct services / Total services) × 100     | `/metrics/quality_full`           |
| **Energy**            | Consumption per dispensed liter                    | kWh / L                                       | `/metrics/energy_efficiency`      |
| **Nonproductive Consumption** | Energy consumption during inactivity           | kWh when flow ≤ threshold                     | `/metrics/nonproductive_consumption` |
| **Thermal Variation** | Temperature stability                              | Temperature standard deviation (°C)           | `/metrics/thermal_variation`      |
| **Peak Flow**         | Maximum vs nominal flow ratio                      | (Maximum flow / Nominal flow)                 | `/metrics/peak_flow_ratio`        |
| **Level Uptime**      | % of time with adequate level                      | (Correct level time / Total time) × 100       | `/metrics/level_uptime`           |
| **MTBA**              | Mean time between adaptive anomalies               | Average minutes between anomalies             | `/metrics/mtba`                   |
| **Response Index**    | Anomaly response time                              | Average response minutes                      | `/metrics/response_index`         |
| **MTBF**              | Mean time between failures                         | Average hours between failures                | `/metrics/mtbf`                   |
| **Response Time**     | Average selection→dispense wait time              | Seconds                                       | `/metrics/response_time`          |
| **Failures Count**    | Number of failures per week                        | Automatic error counting                      | `/metrics/failures_count`         |
| **Usage Rate**        | Average services per hour                          | Services/hour                                 | `/metrics/usage_rate`             |

---

## 🔧 Recent Improvements (v1.1.0)

### Enriched Metadata
All metrics endpoints now include detailed metadata for advanced analysis:

#### Qualitative States
- **`excellent`**: Exceptional performance (green)
- **`good`**: Good performance (blue)
- **`acceptable`**: Acceptable performance (yellow)
- **`poor`**: Poor performance (red)
- **`low`**: Low performance (orange, only for `usage_rate`)

#### Common Metadata
- **Status**: Qualitative system state
- **Time Span**: Analyzed time period
- **Samples**: Number of processed samples
- **Expected Value**: Expected value for comparison
- **Thresholds**: Classification thresholds

#### Specific Metadata by Metric
- **`failures_count`**: Analysis by failure type (temperature, flow, level, power)
- **`usage_rate`**: Usage patterns, peak hours, intervals between services
- **`quality`**: Temperature deviations, reading distribution
- **`performance`**: Efficiency, volume deficit/surplus
- **`energy_efficiency`**: Efficiency ratio, total consumption
- **`availability`**: Flow distribution, total volume
- **`mtba`**: Anomaly rate, distribution by sensor
- **`response_index`**: Response times, distribution by speed
- **`mtbf`**: Reliability analysis, failure distribution
- **`response_time`**: Response categorization by speed
- **`quality_full`**: Analysis of correct vs incorrect services
- **`nonproductive_consumption`**: Analysis of productive vs non-productive periods
- **`thermal_variation`**: Thermal stability, setpoint deviations
- **`peak_flow_ratio`**: Capacity vs actual flow analysis
- **`level_uptime`**: Water availability analysis

### Optimized Frontend
- **Simplified dashboard**: 70% reduction in displayed information
- **Prominent status**: Health states visually highlighted
- **Smart alerts**: Contextual warning messages
- **Consistent structure**: Uniform format for all metrics

---

## ⚙️ Adapted OEE Components

| Component      | Description                                                                 | Formula                                               | Endpoint                |
| -------------- | --------------------------------------------------------------------------- | ----------------------------------------------------- | ----------------------- |
| **Availability** | Time the equipment was operational relative to total available time      | (Operational time / Total available time) × 100       | `/metrics/availability` |
| **Performance**   | Relationship between actual dispensed volume and expected volume          | (Actual dispensed volume / Expected volume) × 100     | `/metrics/performance`  |
| **Quality**       | Percentage of correctly executed services (temp. and flow adequate)       | (Correct services / Total services) × 100             | `/metrics/quality_full` |

### Complementary OEE Metrics

| Complementary Metric | Description | Endpoint |
| -------------------- | ----------- | -------- |
| **Energy Efficiency** | Energy consumption per dispensed liter | `/metrics/energy_efficiency` |
| **Reliability** | Mean time between failures and failure count | `/metrics/mtbf`, `/metrics/failures_count` |
| **Utilization** | Usage patterns and service rate | `/metrics/usage_rate` |
| **Thermal Stability** | Temperature control and variations | `/metrics/thermal_variation` |
| **Response Time** | System response speed | `/metrics/response_time` |
| **Anomaly Management** | Anomaly detection and response | `/metrics/mtba`, `/metrics/response_index` |

---

## 📋 Usage Examples

### System Reliability Analysis
```bash
# Get failure analysis for the last 2 weeks
curl "http://localhost:8000/metrics/failures_count?weeks=2"

# Response includes:
# - reliability_status: 'excellent'/'good'/'acceptable'/'poor'
# - total_failures: total number of failures
# - failures_per_week: weekly rate
# - Analysis by type: temp_failures, flow_failures, level_failures, power_failures
```

### Usage Pattern Analysis
```bash
# Get system utilization analysis
curl "http://localhost:8000/metrics/usage_rate?start=2024-12-01T00:00:00&end=2024-12-07T23:59:59"

# Response includes:
# - utilization_status: 'excellent'/'good'/'acceptable'/'low'/'poor'
# - total_services: total services
# - services_per_day: services per day
# - peak_hour_ratio: peak hour vs average ratio
# - busy_period_percent: % of busy periods
```

### Real-time Quality Monitoring
```bash
# Get system quality status
curl "http://localhost:8000/metrics/quality"

# Response includes:
# - quality_status: qualitative state
# - within_percent: % of readings within range
# - avg_temp: average temperature
# - Automatic alerts if quality_status is 'poor'
```

### Energy Efficiency Analysis
```bash
# Get energy efficiency analysis
curl "http://localhost:8000/metrics/energy_efficiency"

# Response includes:
# - efficiency_status: efficiency state
# - efficiency_ratio: ratio vs expected value
# - total_kwh: total consumption
# - total_liters: total volume
```

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


This README provides a comprehensive review of the project, how to install and run both frontend and backend. It also shows details of the APIs.
Happy monitoring!  🚰📊