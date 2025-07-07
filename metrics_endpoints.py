# -*- coding: utf-8 -*-
"""
Endpoints to calculate metrics from sensor data.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List, Optional
import datetime, statistics
from anomalies_endpoints import adaptive_anomalies, classify_anomalies, get_anomalies
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


@router.get("/mtbf", summary="Mean Time Between Failures (MTBF)")
def get_mtbf(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end:   Optional[str] = Query(None, description="ISO end timestamp")
) -> Dict[str, float]:
    """
    MTBF: promedio de horas entre fallas.
    Consideramos 'falla' cualquier lectura que cumpla condiciones de anomalía estática.
    """
    reads = storage.fetch_all()
    # Filtrar por ventana de tiempo
    def in_range(ts):
        dt = datetime.datetime.fromisoformat(ts)
        if start and dt < datetime.datetime.fromisoformat(start): return False
        if end   and dt > datetime.datetime.fromisoformat(end):   return False
        return True

    # Detectar timestamps de anomalías estáticas
    fail_ts = []
    for r in reads:
        if not in_range(r["timestamp"]): continue
        if r["sensor"] == "temperature" and abs(r["value"] - temperature_setpoint) > TMP_TOLERANCE:
            fail_ts.append(r["timestamp"])
        elif r["sensor"] == "flow" and r["value"] <= FLOW_INACTIVITY_THRESHOLD:
            fail_ts.append(r["timestamp"])
        elif r["sensor"] == "level" and r["value"] < LEVEL_LOW_THRESHOLD:
            fail_ts.append(r["timestamp"])
        elif r["sensor"] == "power" and r["value"] > POWER_HIGH_THRESHOLD:
            fail_ts.append(r["timestamp"])

    if len(fail_ts) < 2:
        return {"mtbf_hours": 0.0}

    times = sorted(datetime.datetime.fromisoformat(t) for t in fail_ts)
    diffs = [
        (times[i] - times[i-1]).total_seconds() / 3600.0
        for i in range(1, len(times))
    ]
    return {"mtbf_hours": round(statistics.mean(diffs), 2)}


@router.get("/quality_full", summary="Full Quality: % of services with correct temp & volume")
def get_quality_full(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None)
) -> Dict[str, float]:
    """
    % de servicios donde:
      - temperatura dentro de ±1°C del setpoint
      - flujo (volume) ≥ min_flow_threshold
    """
    from simulator import SETPOINT_TEMP_DEFAULT, MIN_FLOW_THRESHOLD
    reads = storage.fetch_all()
    # filtrar lecturas de servicio: consideramos cada instante con flow > 0 como 'servicio'
    services = [
        r for r in reads
        if r["sensor"] == "flow" and r["value"] >= MIN_FLOW_THRESHOLD
           and (not start or r["timestamp"] >= start)
           and (not end  or r["timestamp"] <= end)
    ]
    total = len(services)
    if total == 0:
        return {"quality_full_percent": 0.0}
    # para cada flow reading, buscar la temperatura en el mismo timestamp
    correct = 0
    for s in services:
        ts = s["timestamp"]
        temp = next((r["value"] for r in reads if r["sensor"]=="temperature" and r["timestamp"]==ts), None)
        if temp is not None and abs(temp - SETPOINT_TEMP_DEFAULT) <= 1.0:
            correct += 1
    return {"quality_full_percent": round(correct/total*100, 2)}


@router.get("/response_time", summary="Average Response Time Selection→Dispense")
def get_response_time(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None)
) -> Dict[str, float]:
    """
    Tiempo medio (s) entre el momento de selección (simulado como timestamp de evento 'flow' pasa >0)
    y el primer registro de flujo > 0.
    Aquí modelamos selección como lectura previa a flujo; 
    en un sistema real habría un evento explícito de 'select'.
    """
    # para este ejemplo simplificado, asumimos que cada minuto con flow>0 es un servicio
    # y que la 'selección' ocurrió un registro antes.
    reads = sorted(storage.fetch_all(), key=lambda r: r["timestamp"])
    deltas = []
    for i, r in enumerate(reads[1:], start=1):
        if r["sensor"]=="flow" and r["value"]>0:
            prev = reads[i-1]
            # si el anterior era timestamp de selección (cualquier sensor distinto de flow)
            if prev["sensor"]!="flow":
                t0 = datetime.datetime.fromisoformat(prev["timestamp"])
                t1 = datetime.datetime.fromisoformat(r["timestamp"])
                deltas.append((t1-t0).total_seconds())
    if not deltas:
        return {"avg_response_time_sec": 0.0}
    return {"avg_response_time_sec": round(statistics.mean(deltas), 2)}


@router.get("/failures_count", summary="Failures per Week")
def get_failures_count(
    weeks: int = Query(1, ge=1, description="Number of past weeks to consider")
) -> Dict[str, int]:
    """
    Número de fallas (anomalías estáticas) en las últimas `weeks` semanas.
    """
    now = datetime.datetime.utcnow()
    cutoff = now - datetime.timedelta(weeks=weeks)
    reads = storage.fetch_all()

    count = 0
    for r in reads:
        ts = datetime.datetime.fromisoformat(r["timestamp"])
        if ts < cutoff:
            continue
        if r["sensor"] == "temperature" and abs(r["value"] - temperature_setpoint) > TMP_TOLERANCE:
            count += 1
        elif r["sensor"] == "flow" and r["value"] <= FLOW_INACTIVITY_THRESHOLD:
            count += 1
        elif r["sensor"] == "level" and r["value"] < LEVEL_LOW_THRESHOLD:
            count += 1
        elif r["sensor"] == "power" and r["value"] > POWER_HIGH_THRESHOLD:
            count += 1

    return {"failures_last_weeks": count}

@router.get("/usage_rate", summary="Average Services per Hour")
def get_usage_rate(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None)
) -> Dict[str, float]:
    """
    Calcula el promedio de servicios/hora en el periodo.
    Cada lectura de 'flow'>0 se considera un servicio.
    """
    reads = storage.fetch_all()
    # filtrar por rango
    flow = [
        datetime.datetime.fromisoformat(r["timestamp"])
        for r in reads
        if r["sensor"]=="flow" and r["value"]>0
           and (not start or r["timestamp"]>=start)
           and (not end  or r["timestamp"]<=end)
    ]
    total_services = len(flow)
    if total_services == 0:
        return {"services_per_hour": 0.0}
    # periodo en horas
    t0 = min(flow)
    t1 = max(flow)
    hours = (t1 - t0).total_seconds() / 3600.0
    rate = total_services / hours if hours>0 else 0.0
    return {"services_per_hour": round(rate, 2)}

