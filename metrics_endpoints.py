# -*- coding: utf-8 -*-
"""
Endpoints to calculate metrics from sensor data.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List, Optional
import datetime, statistics
from anomalies_endpoints import adaptive_anomalies, classify_anomalies
from storage import LocalStorage

from settings import *

router = APIRouter(prefix="/metrics", tags=["metrics"])
storage = LocalStorage()

@router.get("/availability", summary="Availability: % time flow > 0")
def get_availability(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> Dict[str, float]:
    """
    Calculates percentage of time with flow > 0 between start and end.
    """
    readings = storage.fetch_all()
    # filter by time window using datetime parsing
    flow_readings = [r for r in readings if r['sensor'] == 'flow']
    if start:
        start_dt = datetime.datetime.fromisoformat(start)
        flow_readings = [r for r in flow_readings if datetime.datetime.fromisoformat(r['timestamp']) >= start_dt]
    if end:
        end_dt = datetime.datetime.fromisoformat(end)
        flow_readings = [r for r in flow_readings if datetime.datetime.fromisoformat(r['timestamp']) <= end_dt]
    total = len(flow_readings)
    if total == 0:
        return {"availability": 0.0}
    non_zero = sum(1 for r in flow_readings if r['value'] > 0)
    return {"availability": round(non_zero / total * 100, 2)}

@router.get("/performance", summary="Performance: actual vs expected liters dispensed")
def get_performance(
    users: int = Query(1, ge=1),
    hours: int = Query(1, ge=1)
) -> Dict[str, float]:
    """
    Compares actual liters dispensed vs expected (avg_rate * users * hours).
    """
    from simulator import AVG_FLOW_RATE_DEFAULT
    readings = storage.fetch_all()
    flow_readings = [r for r in readings if r['sensor']=='flow']
    actual = sum(r['value'] for r in flow_readings)  # L/min readings aggregated
    # convert min readings to liters
    actual_liters = actual * (1/60)
    expected = AVG_FLOW_RATE_DEFAULT * users * hours
    performance = round(actual_liters / expected * 100, 2) if expected>0 else 0.0
    return {"performance_percent": performance}

@router.get("/quality", summary="Quality: % temperature within ±5°C setpoint")
def get_quality(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> Dict[str, float]:
    """
    Percentage of temperature readings within ±5°C of setpoint.
    If start/end not provided, considers all readings.
    """
    from simulator import SETPOINT_TEMP_DEFAULT
    readings = storage.fetch_all()
    temp_readings = [r for r in readings if r['sensor'] == 'temperature']
    # apply time filters with proper datetime comparison
    if start:
        start_dt = datetime.datetime.fromisoformat(start)
        temp_readings = [r for r in temp_readings if datetime.datetime.fromisoformat(r['timestamp']) >= start_dt]
    if end:
        end_dt = datetime.datetime.fromisoformat(end)
        temp_readings = [r for r in temp_readings if datetime.datetime.fromisoformat(r['timestamp']) <= end_dt]
    total = len(temp_readings)
    if total == 0:
        return {"quality_percent": 0.0}
    within = sum(1 for r in temp_readings if abs(r['value'] - SETPOINT_TEMP_DEFAULT) <= 5.0)
    return {"quality_percent": round(within / total * 100, 2)}

@router.get("/energy_efficiency", summary="Energy Efficiency: kWh per liter dispensed")
def get_energy_efficiency(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> Dict[str, float]:
    """
    Calculates kWh consumed per liter dispensed.
    """
    readings = storage.fetch_all()
    power_readings = [r for r in readings if r['sensor'] == 'power']
    flow_readings = [r for r in readings if r['sensor'] == 'flow']
    # filter by time
    if start:
        start_dt = datetime.datetime.fromisoformat(start)
        power_readings = [r for r in power_readings if datetime.datetime.fromisoformat(r['timestamp']) >= start_dt]
        flow_readings = [r for r in flow_readings if datetime.datetime.fromisoformat(r['timestamp']) >= start_dt]
    if end:
        end_dt = datetime.datetime.fromisoformat(end)
        power_readings = [r for r in power_readings if datetime.datetime.fromisoformat(r['timestamp']) <= end_dt]
        flow_readings = [r for r in flow_readings if datetime.datetime.fromisoformat(r['timestamp']) <= end_dt]
    total_kwh = sum(r['value'] * (1/60) for r in power_readings)
    total_l = sum(r['value'] for r in flow_readings) * (1/60)
    efficiency = round(total_kwh / total_l, 3) if total_l > 0 else 0.0
    return {"kwh_per_liter": efficiency}

@router.get("/thermal_variation", summary="Thermal Variation: std dev of temperature readings")
def get_thermal_variation(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> Dict[str, float]:
    """
    Standard deviation of temperature readings between start and end.
    """
    readings = storage.fetch_all()
    temps = [r['value'] for r in readings if r['sensor'] == 'temperature']
    if start:
        start_dt = datetime.datetime.fromisoformat(start)
        temps = [v for i,v in enumerate([r['value'] for r in readings if r['sensor']=='temperature']) 
                 if datetime.datetime.fromisoformat(readings[i]['timestamp']) >= start_dt]
    if end:
        end_dt = datetime.datetime.fromisoformat(end)
        temps = [v for i,v in enumerate([r['value'] for r in readings if r['sensor']=='temperature']) 
                 if datetime.datetime.fromisoformat(readings[i]['timestamp']) <= end_dt]
    if len(temps) < 2:
        return {"thermal_variation": 0.0}
    return {"thermal_variation": round(statistics.stdev(temps), 2)}



@router.get("/peak_flow_ratio", summary="Peak Flow Ratio: max flow / nominal")
def get_peak_flow_ratio(
    users: int = Query(1, ge=1)
) -> Dict[str, float]:
    """
    Ratio of max observed flow to nominal flow (avg_rate*users).
    """
    from simulator import AVG_FLOW_RATE_DEFAULT
    readings = storage.fetch_all()
    flow_readings = [r['value'] for r in readings if r['sensor']=='flow']
    if not flow_readings:
        return {"peak_flow_ratio": 0.0}
    max_flow = max(flow_readings)
    nominal = AVG_FLOW_RATE_DEFAULT*users/60  # L/min nominal
    ratio = round(max_flow/nominal,2) if nominal>0 else 0.0
    return {"peak_flow_ratio": ratio}

@router.get("/mtba", summary="Mean Time Between Adaptive Anomalies")
async def get_mtba(
    window: int = Query(60, ge=1, description="Rolling window for adaptive anomalies"),
    sensor: Optional[str] = Query(None, description="Filter by sensor name")
) -> Dict[str, float]:
    """
    Mean Time Between adaptive anomalies (minutes) using rolling z-score method.
    """
    anomalies = await adaptive_anomalies(sensor=sensor, window=window)
    if not anomalies or len(anomalies) < 2:
        return {"mtba_minutes": 0.0}
    times = sorted(datetime.datetime.fromisoformat(a['timestamp']) for a in anomalies)
    diffs = [(times[i] - times[i-1]).total_seconds() / 60.0 for i in range(1, len(times))]
    return {"mtba_minutes": round(statistics.mean(diffs), 2)}

@router.get("/level_uptime")
def get_level_uptime(
    start: str = Query(None),
    end:   str = Query(None)
) -> Dict[str, float]:
    """
    Level Uptime: % time level between low threshold and full.
    """
    rds = storage.fetch_all()
    levels = [r for r in rds if r['sensor']=='level'
              and (not start or r['timestamp']>=start)
              and (not end  or r['timestamp']<=end)]
    total = len(levels)
    if total==0:
        raise HTTPException(404,"No level readings")
    ok = sum(1 for r in levels if LEVEL_LOW_THRESHOLD<=r['value']<=1)
    return {"level_uptime_percent": round(ok/total*100,2)}

@router.get("/response_index", summary="Response Index to Adaptive Anomalies")
async def get_response_index(
    window: int = Query(60, ge=1, description="Rolling window for adaptive anomalies"),
    sensor: Optional[str] = Query(None, description="Filter by sensor name")
) -> Dict[str, float]:
    """
    Response Index: average minutes from adaptive anomaly to recovery.
    """
    anomalies = await classify_anomalies(sensor=sensor, window=window)
    if not anomalies:
        return {"response_index_minutes": 0.0}
    resp_times = []
    all_readings = storage.fetch_all()
    for a in anomalies:
        sname = a['sensor']
        t0 = datetime.datetime.fromisoformat(a['timestamp'])
        for r in all_readings:
            if r['sensor'] == sname and datetime.datetime.fromisoformat(r['timestamp']) > t0:
                t1 = datetime.datetime.fromisoformat(r['timestamp'])
                resp_times.append((t1 - t0).total_seconds() / 60.0)
                break
    if not resp_times:
        return {"response_index_minutes": 0.0}
    return {"response_index_minutes": round(statistics.mean(resp_times), 2)}

@router.get("/nonproductive_consumption", summary="Nonproductive Consumption: kWh when flow ≤ threshold")
def get_nonproductive_consumption(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> Dict[str, float]:
    """
    Energy consumed during periods of inactivity (flow ≤ threshold).
    """
    from settings import FLOW_INACTIVITY_THRESHOLD
    readings = storage.fetch_all()
    power_readings = [r for r in readings if r['sensor']=='power']
    flow_readings = [r for r in readings if r['sensor']=='flow']
    # align on timestamps
    nonprod_energy = 0.0
    for p,f in zip(power_readings, flow_readings):
        ts = datetime.datetime.fromisoformat(p['timestamp'])
        if start and ts < datetime.datetime.fromisoformat(start): continue
        if end and ts > datetime.datetime.fromisoformat(end): continue
        if f['value'] <= FLOW_INACTIVITY_THRESHOLD:
            nonprod_energy += p['value'] * (1/60)
    return {"nonproductive_kwh": round(nonprod_energy, 3)}

