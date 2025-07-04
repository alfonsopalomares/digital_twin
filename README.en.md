# Industry 4.0 Project: Smart Water Dispenser

**Introduction:**
This project implements a smart water dispenser system inspired by Industry 4.0 principles. It simulates IoT sensor behaviors, stores historical data, detects anomalies, and evaluates performance metrics in real time. The goal is to demonstrate key technologies (simulated IoT, digital twins, analytics, and interactive dashboards) in resource-constrained environments like small businesses or educational institutions.

---

## Prerequisites

- **Git**
- **Python 3.10+** and **pip**
- **Node.js 16+** and **npm**

---

## Backend

### Installation
```bash
cd backend
git clone <REPO_URL> .
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install fastapi uvicorn pydantic sqlite3
```

### Running the API
```bash
uvicorn api:app --reload
```
- Swagger UI: `http://localhost:8000/docs`

### Endpoints

#### Sensor Readings
| Method | Path                          | Description                                           |
| ------ | ----------------------------- | ----------------------------------------------------- |
| GET    | `/readings`                   | Returns all stored readings.                         |
| GET    | `/readings/latest`            | Returns the most recent reading.                     |
| DELETE | `/readings`                   | Deletes all stored readings.                         |
| POST   | `/simulate?hours={h}&users={u}` | Simulates `h` hours for `u` users and stores data.  |

#### Anomaly Detection
| Method | Path             | Description                                                          |
| ------ | ---------------- | -------------------------------------------------------------------- |
| GET    | `/anomalies`     | Detects overtemperature, inactivity, low level, and high power usage. |

#### Metrics (`/metrics/...`)
| Path                                | Parameters         | Description                                                      |
| ----------------------------------- | ------------------ | ---------------------------------------------------------------- |
| `/metrics/availability`             | `start`, `end`     | % of time flow > 0.                                              |
| `/metrics/performance`              | `users`, `hours`   | Actual liters dispensed vs expected liters.                      |
| `/metrics/quality`                  | `start`, `end`     | % of temperature readings within ±1°C setpoint.                  |
| `/metrics/energy_efficiency`        | `start`, `end`     | kWh consumed per liter dispensed.                                |
| `/metrics/peak_flow_ratio`          | `users`            | Max flow / nominal flow per user.                                |
| `/metrics/mtba`                     | —                  | Mean time between anomalies (minutes).                           |
| `/metrics/level_uptime`             | `start`, `end`     | % of time level between 20% and 100%.                            |
| `/metrics/response_index`           | —                  | Average minutes to recovery after anomaly.                       |
| `/metrics/thermal_variation`        | `start`, `end`     | Standard deviation of temperature (°C).                          |
| `/metrics/nonproductive_consumption`| `start`, `end`     | kWh consumed with flow ≤ inactivity threshold.                   |

To mount metrics routes in `api.py`:
```python
from api_metrics_endpoints import router as metrics_router
app.include_router(metrics_router)
```

---

## Frontend

### Installation & Running
```bash
cd frontend
git clone <REPO_URL> .
npm install
npm install react-router-dom recharts react-bootstrap bootstrap
```
In `src/index.js`, add:
```js
import 'bootstrap/dist/css/bootstrap.min.css';
```
Then:
```bash
npm start
```
Open `http://localhost:3000`.

### File Structure

- `index.js`: Renders `<App />` inside `<BrowserRouter>`.
- `App.jsx`: Navigation menu and `<Routes>` definitions.
- `MainPage.jsx`: Landing page with links.
- `SimulatePage.jsx`: Simulation UI, readings grid, and clear data button.
- `AnalyticsPage.jsx`: Graph dashboard (`AnalyticsDashboard.jsx`).
- `AnomaliesPage.jsx`: Grouped anomaly tables (`AnomaliesDashboard.jsx`).
- `MetricsPage.jsx`: Metrics dashboard with RadarChart and Gauges (`MetricsDashboard.jsx`).

---

## Simulator Configuration (`simulator.py`)
Configurable constants at the top:
- `AVG_FLOW_RATE_DEFAULT`: L/h per user.
- `TIME_CONVERSION`: Convert L/h → L/min.
- `TEMPERATURE_MEAN`, `TEMPERATURE_VARIATION`: Temperature base and variation.
- `LEVEL_MIN`, `LEVEL_MAX`: Tank level range (0–1).
- `POWER_MIN`, `POWER_MAX`: Power draw range (kW).

The `generate_frame(timestamp, users, sensor, value)` function supports:
- `timestamp=None`: uses current UTC time.
- `sensor`: generate only that sensor reading.
- `value`: override the simulated value if provided.

---

This README provides a comprehensive overview of the project, how to install and run both backend and frontend, and detailed API reference. Happy monitoring! 🚰📊
