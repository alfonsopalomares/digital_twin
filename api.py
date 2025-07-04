# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime

# Import modules
from simulator import SensorSimulator
from storage import LocalStorage

# Import API endpoints
from api_metrics_endpoints import router as metrics_router
from anomalies import detect_anomalies as fetch_anomalies
from settings import *

app = FastAPI()
# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar dominios en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for serializing sensor readings
class SensorReading(BaseModel):
    sensor: str
    timestamp: str
    value: float

# Instancias únicas de simulador y almacenamiento
simulator = SensorSimulator(avg_flow_rate=0.5)
storage = LocalStorage()



# Modelo de anomalía
class Anomaly(BaseModel):
    sensor: str
    timestamp: str
    value: float
    type: str
    detail: str


@app.get("/")
def api_root():
    return {
        "readings": "/readings",
        "reading_latest": "/readings/latest",
        "simulate": "/simulate?hours={hours}&users={users}",
        "delete_readings": "/readings (DELETE)",
        "anomalies": "/anomalies",
        "metrics": {
            "availability": "/metrics/availability?start={ISO}&end={ISO}",
            "performance": "/metrics/performance?users={n}&hours={h}",
            "quality": "/metrics/quality?start={ISO}&end={ISO}",
            "energy_efficiency": "/metrics/energy_efficiency?start={ISO}&end={ISO}",
            "peak_flow_ratio": "/metrics/peak_flow_ratio?users={n}",
            "mtba": "/metrics/mtba",
            "level_uptime": "/metrics/level_uptime?start={ISO}&end={ISO}",
            "response_index": "/metrics/response_index",
            "thermal_variation": "/metrics/thermal_variation?start={ISO}&end={ISO}",
            "nonproductive_consumption": "/metrics/nonproductive_consumption?start={ISO}&end={ISO}"
        }
    }

@app.get("/anomalies", response_model=List[Anomaly])
def get_anomalies():
    return fetch_anomalies()


@app.get('/readings', response_model=List[SensorReading])
def get_readings():
    """Returns all stored sensor readings."""
    return storage.fetch_all() or []

@app.get('/readings/latest', response_model=SensorReading)
def get_latest_reading():
    """Returns the most recent stored reading."""
    result = storage.fetch_latest()
    if not result:
        raise HTTPException(status_code=404, detail="No readings found")
    if not all(k in result for k in ("sensor", "timestamp", "value")):
        raise HTTPException(status_code=500, detail="Malformed reading data")
    return result

@app.post('/simulate')
async def simulate_usage(
    hours: int = Query(8, ge=1, description="Simulation duration in hours"),
    users: int = Query(10, ge=1, description="Number of active users"),
    sensor: str = Query(None, description="(Optional) Specific sensor to simulate"),
    value: float = Query(None, description="(Optional) Override value for the sensor"),
    timestamp: str = Query(None, description="(Optional) ISO timestamp to use for simulation")
):
    """
    Simulate continuous data for `hours` hours and `users` users.
    Optional parameters `sensor`, `value`, `timestamp` override generate_frame behavior.

    - If `sensor` is set, only that sensor is generated per timestamp.
    - If `value` is provided, it overrides the simulated value for the given sensor.
    - If `timestamp` is provided, it overrides the generated timestamp; otherwise current UTC is used.
    """
    total_minutes = hours * 60
    now = datetime.datetime.utcnow()
    for minute in range(total_minutes):
        ts = timestamp or (now + datetime.timedelta(minutes=minute)).isoformat()
        # Pass sensor and value overrides into generate_frame
        batch = simulator.generate_frame(
            timestamp=ts,
            users=users,
            sensor=sensor,
            value=value
        )
        # Store batch in DB
        storage.save_batch(batch)
    return {
        "status": "ok",
        "hours": hours,
        "users": users,
        "sensor_override": sensor,
        "value_override": value,
        "timestamp_override": bool(timestamp),
        "generated_records": total_minutes * simulator.sensors_count
    }

@app.delete('/readings')
def delete_readings():
    """Deletes all stored sensor readings."""
    storage.clear_all()
    return {"status": "deleted"}


app.include_router(metrics_router)