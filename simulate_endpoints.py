# -*- coding: utf-8 -*-
"""
Endpoints to simulate water dispenser usage.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import datetime

from storage import LocalStorage
from simulator import SensorSimulator
from anomalies import detect_anomalies as fetch_anomalies
from settings import *

router = APIRouter(prefix="/simulate", tags=["Simulate"])
storage = LocalStorage()
simulator = SensorSimulator()

# --- Pydantic model for scenario configurations ---
class ScenarioConfig(BaseModel):
    users: int
    flow_rate: Optional[float] = None
    temp_setpoint: Optional[float] = None
    heater_regime: Optional[float] = None

class ScenarioResult(BaseModel):
    config: dict
    total_energy_kWh: float
    avg_temperature: Optional[float]


@router.post('/simulate')
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
    storage.clear_all()
    storage.save_config(users, hours)
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


@router.post("/simulate_scenarios", response_model=List[ScenarioResult])
async def simulate_scenarios(
    configs: List[ScenarioConfig],
    duration_hours: int = Query(1, ge=1, description="Duration of each scenario in hours")
):
    """
    Run batch simulations for multiple scenarios.

    - configs: list of ScenarioConfig objects defining parameters per scenario.
    - duration_hours: simulation length for each scenario.

    Returns aggregated metrics for each input configuration.
    """
    try:
        # Convert Pydantic models to dicts
        cfg_dicts = [c.dict() for c in configs]
        results = simulator.simulate_scenarios(cfg_dicts, duration_hours)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




