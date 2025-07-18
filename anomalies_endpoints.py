# -*- coding: utf-8 -*-

import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from storage import LocalStorage
from pydantic import BaseModel
from settings import *

router = APIRouter(prefix="/anomalies", tags=["anomalies"])

# Adaptive threshold parameters
Z_THRESHOLD = 1.5  # anomalies beyond ±1.5 standard deviations (more sensitive)

# Modelo de anomalía
class Anomaly(BaseModel):
    sensor: str
    timestamp: str
    value: float
    type: str
    detail: str

storage = LocalStorage()


@router.get("/static", response_model=List[Anomaly])
def get_anomalies():
    """
    Detecta anomalías:
      - Sobretemperatura: fuera de ±TMP_TOLERANCE de setpoint.
      - Inactividad: flujo ≤ FLOW_INACTIVITY_THRESHOLD por ≥ FLOW_INACTIVITY_MINUTES.
      - Nivel bajo: level < LEVEL_LOW_THRESHOLD.
      - Consumo alto: power > POWER_HIGH_THRESHOLD.
    """
    readings = storage.fetch_all()
    anomalies: List[Dict[str, Any]] = []
    flow_zero_count = 0

    for r in readings:
        s, ts, val = r["sensor"], r["timestamp"], r["value"]

        if s == "temperature":
            if abs(val - SETPOINT_TEMP_DEFAULT) > TMP_TOLERANCE:
                anomalies.append({
                    "sensor": s, "timestamp": ts, "value": val,
                    "type": "Overtemperature",
                    "detail": f"Temperature {val}°C outside ±{TMP_TOLERANCE}°C of setpoint {SETPOINT_TEMP_DEFAULT}°C"
                })

        elif s == "flow":
            if val <= FLOW_INACTIVITY_THRESHOLD:
                flow_zero_count += 1
            else:
                flow_zero_count = 0

            if flow_zero_count >= FLOW_INACTIVITY_MINUTES:
                anomalies.append({
                    "sensor": s, "timestamp": ts, "value": val,
                    "type": "Inactivity",
                    "detail": f"Flow ≤{FLOW_INACTIVITY_THRESHOLD} L/min for {FLOW_INACTIVITY_MINUTES} min"
                })

        elif s == "level":
            if val < LEVEL_LOW_THRESHOLD:
                anomalies.append({
                    "sensor": s, "timestamp": ts, "value": val,
                    "type": "LowLevel",
                    "detail": f"Level {val*100:.1f}% below {LEVEL_LOW_THRESHOLD*100:.0f}%"
                })

        elif s == "power":
            if val > POWER_HIGH_THRESHOLD:
                anomalies.append({
                    "sensor": s, "timestamp": ts, "value": val,
                    "type": "HighPower",
                    "detail": f"Power {val} kW above {POWER_HIGH_THRESHOLD} kW"
                })

    return anomalies

@router.get("/adaptive", summary="Adaptive Threshold Anomaly Detection")
async def adaptive_anomalies(
    sensor: Optional[str] = Query(None, description="Filter by sensor name"),
    window: int = Query(20, ge=5, description="Rolling window size (in readings)")
) -> List[dict]:
    """
    Detect anomalies using adaptive thresholds (rolling mean ± Z_THRESHOLD * std).
    Returns entries where |z-score| > Z_THRESHOLD.
    
    Algorithm:
    1. Calculate rolling mean and standard deviation over the specified window
    2. Compute z-score for each reading: (value - mean) / std
    3. Flag as anomaly if |z-score| > Z_THRESHOLD (default: 2.0)
    
    This method adapts to the local behavior of each sensor, making it more
    sensitive to sudden changes than fixed thresholds.
    """
    storage = LocalStorage()
    readings = storage.fetch_all()
    if not readings:
        raise HTTPException(status_code=404, detail="No readings available")
    
    df = pd.DataFrame(readings)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    if sensor:
        df = df[df['sensor'] == sensor]
    
    if df.empty:
        return []
    
    # Group by sensor to calculate statistics per sensor
    anomalies_list = []
    
    for sensor_name in df['sensor'].unique():
        sensor_df = df[df['sensor'] == sensor_name].copy()
        
        # Calculate rolling statistics
        sensor_df['mean'] = sensor_df['value'].rolling(window=window, min_periods=window//2).mean()
        sensor_df['std'] = sensor_df['value'].rolling(window=window, min_periods=window//2).std().fillna(0)
        
        # Handle zero standard deviation (constant values)
        # Use a small fraction of the mean as minimum std to avoid division by zero
        min_std = sensor_df['value'].mean() * 0.01  # 1% of mean as minimum std
        sensor_df['std'] = sensor_df['std'].replace(0, min_std)
        
        # Calculate z-scores
        sensor_df['z'] = (sensor_df['value'] - sensor_df['mean']) / sensor_df['std']
        
        # Detect anomalies
        sensor_df['anomaly'] = sensor_df['z'].abs() > Z_THRESHOLD
        sensor_anomalies = sensor_df[sensor_df['anomaly']]
        
        # Add to results
        for _, row in sensor_anomalies.iterrows():
            anomalies_list.append({
                'sensor': row['sensor'],
                'timestamp': row['timestamp'].isoformat(),
                'value': row['value'],
                'mean': row['mean'],
                'std': row['std'],
                'z': row['z']
            })
    
    return anomalies_list

@router.get("/classify", summary="Classify Detected Anomalies")
async def classify_anomalies(
    sensor: Optional[str] = Query(None, description="Filter by sensor name"),
    window: int = Query(60, ge=1, description="Rolling window size (in readings)")
) -> List[dict]:
    """
    Classify anomalies into types: 'leakage', 'sensor_error', 'overuse', or 'other'.
    Based on rules applied to adaptive anomalies.
    """
    anomalies = await adaptive_anomalies(sensor, window)
    classified = []
    for a in anomalies:
        typ = 'other'
        if a['sensor'] == 'flow' and a['value'] > a['mean']:
            typ = 'leakage'
        elif a['sensor'] == 'temperature' and abs(a['value'] - a['mean']) > 5:
            typ = 'sensor_error'
        elif a['sensor'] == 'power' and a['value'] > a['mean']:
            typ = 'overuse'
        classified.append({**a, 'type': typ})
    return classified
