# -*- coding: utf-8 -*-
"""
Endpoints to fetch sensor readings.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from storage import LocalStorage

router = APIRouter(prefix="/readings", tags=["Readings"])
storage = LocalStorage()

# Model for serializing sensor readings
class SensorReading(BaseModel):
    sensor: str
    timestamp: str
    value: float

@router.get('/readings', response_model=List[SensorReading])
def get_readings():
    """Returns all stored sensor readings."""
    return storage.fetch_all() or []

@router.get('/readings/latest', response_model=SensorReading)
def get_latest_reading():
    """Returns the most recent stored reading."""
    result = storage.fetch_latest()
    if not result:
        raise HTTPException(status_code=404, detail="No readings found")
    if not all(k in result for k in ("sensor", "timestamp", "value")):
        raise HTTPException(status_code=500, detail="Malformed reading data")
    return result

@router.delete('/readings')
def delete_readings():
    """Deletes all stored sensor readings."""
    storage.clear_all()
    return {"status": "deleted"}