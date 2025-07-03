# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime

# Import modules
from simulator import SensorSimulator
from storage import LocalStorage

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
    hours: int = Query(8, ge=1, description="Cantidad de horas a simular"),
    users: int = Query(10, ge=1, description="Número de usuarios activos"),
):
    """
    Simula generación continua de datos durante `hours` horas
    con `users` usuarios simultáneos.
    """
    total_minutes = hours * 60
    now = datetime.datetime.utcnow()
    for minute in range(total_minutes):
        ts = (now + datetime.timedelta(minutes=minute)).isoformat()
        batch = simulator.generate_frame(timestamp=ts, users=users)
        storage.save_batch(batch)
    return {
        "status": "ok",
        "hours": hours,
        "users": users,
        "generated_records": total_minutes * users * simulator.sensors_count
    }

@app.delete('/readings')
def delete_readings():
    """Deletes all stored sensor readings."""
    storage.clear_all()
    return {"status": "deleted"}