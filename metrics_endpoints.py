# -*- coding: utf-8 -*-
"""
Endpoints to calculate metrics from sensor data.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List, Optional, Union
import datetime, statistics
from anomalies_endpoints import adaptive_anomalies, classify_anomalies, get_anomalies
from storage import LocalStorage
from settings import *

router = APIRouter(prefix="/metrics", tags=["metrics"])
storage = LocalStorage()

# Type for metric response
MetricResponse = Dict[str, Union[str, float, int]]

# Metric metadata for consistent returns
METRIC_METADATA = {
    'availability': {'title': 'Availability', 'unit': '%'},
    'performance': {'title': 'Performance', 'unit': 'ratio'},
    'quality': {'title': 'Quality', 'unit': '%'},
    'energy_efficiency': {'title': 'Energy Efficiency', 'unit': 'kWh/L'},
    'thermal_variation': {'title': 'Thermal Variation', 'unit': '°C'},
    'peak_flow_ratio': {'title': 'Peak Flow Ratio', 'unit': ''},
    'mtba': {'title': 'Mean Time Between Adaptive Anomalies', 'unit': 'min'},
    'level_uptime': {'title': 'Level Uptime', 'unit': '%'},
    'response_index': {'title': 'Response Index', 'unit': 'min'},
    'nonproductive_consumption': {'title': 'Nonproductive Consumption', 'unit': 'kWh'},
    'mtbf': {'title': 'Mean Time Between Failures', 'unit': 'hours'},
    'quality_full': {'title': 'Full Quality', 'unit': '%'},
    'response_time': {'title': 'Average Response Time', 'unit': 'sec'},
    'failures_count': {'title': 'Failures Count', 'unit': 'failures'},
    'usage_rate': {'title': 'Usage Rate', 'unit': 'services/hour'}
}

def format_metric_response(metric_key: str, value: float, expected_value: float = None, samples: int = None, users: int = None, hours: int = None) -> MetricResponse:
    """Generate consistent metric response format with additional metadata"""
    metadata = METRIC_METADATA.get(metric_key, {'title': metric_key.title(), 'unit': ''})
    response = {
        'title': metadata['title'],
        'unit': metadata['unit'],
        'value': value
    }
    
    # Add optional metadata if provided
    if expected_value is not None:
        response['expected_value'] = expected_value
    if samples is not None:
        response['samples'] = samples
    if users is not None:
        response['users'] = users
    if hours is not None:
        response['hours'] = hours
    
    return response

@router.get("/availability", summary="Availability: % time flow > 0")
def get_availability(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
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
        return format_metric_response('availability', 0.0, samples=0)
    non_zero = sum(1 for r in flow_readings if r['value'] > 0)
    return format_metric_response('availability', round(non_zero / total * 100, 2), samples=total)

@router.get("/performance", summary="Performance: actual vs expected liters dispensed")
def get_performance(
    users: Optional[int] = Query(None, ge=1),
    hours: Optional[int] = Query(None, ge=1)
) -> MetricResponse:
    """
    Compara litros reales dispensados vs esperados 
    (avg_rate * users * hours), integrando cada lectura
    de flujo según Δt real entre muestras.
    """
    from simulator import AVG_FLOW_RATE_DEFAULT

    # 1) Load and update config
    config = storage.get_config()
    if config is None:
        config = {'user_quantity': 1, 'hours': 1}
        # ensure defaults
        storage.save_config(config['user_quantity'], config['hours'])

    if users is not None:
        config['user_quantity'] = users
    if hours is not None:
        config['hours'] = hours

    
    users_final = config['user_quantity']
    hours_final = config['hours']

    # 2) Get readings and filter only flow
    readings = storage.fetch_all()
    flow_logs = [
        r for r in readings
        if r['sensor'] == 'flow'
    ]

    # 3) Sort by timestamp and calculate integrated liters
    flow_logs.sort(key=lambda r: r['timestamp'])
    actual_liters = 0.0

    # For each consecutive pair, L/min × minutes elapsed = L
    for prev, curr in zip(flow_logs, flow_logs[1:]):
        t0 = datetime.datetime.fromisoformat(prev['timestamp'])
        t1 = datetime.datetime.fromisoformat(curr['timestamp'])
        dt_min = (t1 - t0).total_seconds() / 60.0
        actual_liters += prev['value'] * dt_min

    # If there was only one sample or none, actual_liters will remain 0.0

    # 4) Calculate expected (AVG_FLOW_RATE_DEFAULT is now in L/min, convert to L/h for hourly calculation)
    expected_liters = (AVG_FLOW_RATE_DEFAULT * 60) * users_final * hours_final

    
    # 5) Performance as ratio (actual vs expected)
    performance_ratio = (
        round(actual_liters / expected_liters, 3)
        if expected_liters > 0 else 0.0
    )

    # No need to clamp ratio - can be > 1.0 (more than expected) or < 1.0 (less than expected)
    return format_metric_response('performance', performance_ratio, expected_value=round(expected_liters, 2), samples=len(flow_logs), users=users_final, hours=hours_final)

@router.get("/quality", summary="Quality: % temperature within ±5°C setpoint")
def get_quality(
    start: Optional[str] = Query(
        None, description="ISO start timestamp (inclusive)"
    ),
    end: Optional[str] = Query(
        None, description="ISO end timestamp (inclusive)"
    )
) -> MetricResponse:
    """
    Percentage of temperature readings within ±5°C of setpoint,
    over the time window [start, end]. If start/end not provided,
    uses full range of available readings.
    Returns:
      - quality_percent: clamped 0–100%
      - raw_quality: actual fraction*100 (may be >100 or <0, though unlikely)
      - within_count: number of readings within band
      - total_samples: number of readings in window
      
    """
    from simulator import SETPOINT_TEMP_DEFAULT, TEMPERATURE_VARIATION

    # 1) Fetch and parse all temperature readings
    readings = storage.fetch_all()
    temp_logs = []
    for r in readings:
        if r.get('sensor') != 'temperature':
            continue
        ts_str = r.get('timestamp')
        try:
            ts = datetime.datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            # skip bad timestamps
            continue
        temp_logs.append({'timestamp': ts, 'value': r.get('value', 0.0)})

    # If no valid temperature logs at all
    if not temp_logs:
        return format_metric_response('quality', 0.0, samples=0)

    # 2) Determine window
    # parse user-supplied start/end or default to min/max from data
    try:
        start_dt = datetime.datetime.fromisoformat(start) if start else min(l['timestamp'] for l in temp_logs)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ISO format for 'start'")
    try:
        end_dt = datetime.datetime.fromisoformat(end) if end else max(l['timestamp'] for l in temp_logs)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ISO format for 'end'")

    if start_dt > end_dt:
        raise HTTPException(status_code=400, detail="'start' must be <= 'end'")

    # 3) Filter logs to window
    window_logs = [
        l for l in temp_logs
        if start_dt <= l['timestamp'] <= end_dt
    ]
    total = len(window_logs)
    if total == 0:
        return format_metric_response('quality', 0.0, samples=0)

    # 4) Count readings within ±5°C of setpoint
    within_count = sum(
        1 for l in window_logs
        if abs(l['value'] - SETPOINT_TEMP_DEFAULT) <= (TEMPERATURE_VARIATION/2)
    )

    # 5) Compute raw and clamped percentages
    raw_quality = (within_count / total) * 100.0
    quality_percent = round(min(max(raw_quality, 0.0), 100.0), 2)

    return format_metric_response('quality', quality_percent, samples=total)

@router.get("/energy_efficiency", summary="Energy Efficiency: kWh per liter dispensed")
def get_energy_efficiency(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
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
    return format_metric_response('energy_efficiency', efficiency, samples=len(power_readings))

@router.get("/thermal_variation", summary="Thermal Variation: std dev of temperature readings")
def get_thermal_variation(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
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
        return format_metric_response('thermal_variation', 0.0, samples=len(temps))
    return format_metric_response('thermal_variation', round(statistics.stdev(temps), 2), samples=len(temps))



@router.get("/peak_flow_ratio", summary="Peak Flow Ratio: max flow / nominal")
def get_peak_flow_ratio(
    users: int = Query(1, ge=1)
) -> MetricResponse:
    """
    Ratio of max observed flow to nominal flow (avg_rate*users).
    """
    from simulator import AVG_FLOW_RATE_DEFAULT
    readings = storage.fetch_all()
    flow_readings = [r['value'] for r in readings if r['sensor']=='flow']
    if not flow_readings:
        return format_metric_response('peak_flow_ratio', 0.0, expected_value=0.0, samples=0, users=users)
    max_flow = max(flow_readings)
    nominal = AVG_FLOW_RATE_DEFAULT * users  # L/min nominal (AVG_FLOW_RATE_DEFAULT is already in L/min)
    ratio = round(max_flow/nominal,2) if nominal>0 else 0.0
    return format_metric_response('peak_flow_ratio', ratio, expected_value=1.0, samples=len(flow_readings), users=users)

@router.get("/mtba", summary="Mean Time Between Adaptive Anomalies")
async def get_mtba(
    window: int = Query(60, ge=1, description="Rolling window for adaptive anomalies"),
    sensor: Optional[str] = Query(None, description="Filter by sensor name")
) -> MetricResponse:
    """
    Mean Time Between adaptive anomalies (minutes) using rolling z-score method.
    """
    anomalies = await adaptive_anomalies(sensor=sensor, window=window)
    if not anomalies or len(anomalies) < 2:
        return format_metric_response('mtba', 0.0, samples=len(anomalies) if anomalies else 0)
    times = sorted(datetime.datetime.fromisoformat(a['timestamp']) for a in anomalies)
    diffs = [(times[i] - times[i-1]).total_seconds() / 60.0 for i in range(1, len(times))]
    return format_metric_response('mtba', round(statistics.mean(diffs), 2), samples=len(anomalies))

@router.get("/level_uptime")
def get_level_uptime(
    start: str = Query(None),
    end:   str = Query(None)
) -> MetricResponse:
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
    return format_metric_response('level_uptime', round(ok/total*100,2), samples=total)

@router.get("/response_index", summary="Response Index to Adaptive Anomalies")
async def get_response_index(
    window: int = Query(60, ge=1, description="Rolling window for adaptive anomalies"),
    sensor: Optional[str] = Query(None, description="Filter by sensor name")
) -> MetricResponse:
    """
    Response Index: average minutes from adaptive anomaly to recovery.
    """
    anomalies = await classify_anomalies(sensor=sensor, window=window)
    if not anomalies:
        return format_metric_response('response_index', 0.0, samples=0)
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
        return format_metric_response('response_index', 0.0, samples=len(anomalies))
    return format_metric_response('response_index', round(statistics.mean(resp_times), 2), samples=len(anomalies))

@router.get("/nonproductive_consumption", summary="Nonproductive Consumption: kWh when flow ≤ threshold")
def get_nonproductive_consumption(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
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
    return format_metric_response('nonproductive_consumption', round(nonprod_energy, 3), samples=len(power_readings))


@router.get("/mtbf", summary="Mean Time Between Failures (MTBF)")
def get_mtbf(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end:   Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
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
        return format_metric_response('mtbf', 0.0, samples=len(fail_ts))

    times = sorted(datetime.datetime.fromisoformat(t) for t in fail_ts)
    diffs = [
        (times[i] - times[i-1]).total_seconds() / 3600.0
        for i in range(1, len(times))
    ]
    return format_metric_response('mtbf', round(statistics.mean(diffs), 2), samples=len(fail_ts))


@router.get("/quality_full", summary="Full Quality: % of services with correct temp & volume")
def get_quality_full(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None)
) -> MetricResponse:
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
        return format_metric_response('quality_full', 0.0, samples=0)
    # para cada flow reading, buscar la temperatura en el mismo timestamp
    correct = 0
    for s in services:
        ts = s["timestamp"]
        temp = next((r["value"] for r in reads if r["sensor"]=="temperature" and r["timestamp"]==ts), None)
        if temp is not None and abs(temp - SETPOINT_TEMP_DEFAULT) <= 1.0:
            correct += 1
    return format_metric_response('quality_full', round(correct/total*100, 2), samples=total)


@router.get("/response_time", summary="Average Response Time Selection→Dispense")
def get_response_time(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None)
) -> MetricResponse:
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
        return format_metric_response('response_time', 0.0, samples=0)
    return format_metric_response('response_time', round(statistics.mean(deltas), 2), samples=len(deltas))


@router.get("/failures_count", summary="Failures per Week")
def get_failures_count(
    weeks: int = Query(1, ge=1, description="Number of past weeks to consider")
) -> MetricResponse:
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

    return format_metric_response('failures_count', count, samples=len(reads))

@router.get("/usage_rate", summary="Average Services per Hour")
def get_usage_rate(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None)
) -> MetricResponse:
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
        return format_metric_response('usage_rate', 0.0, samples=0)
    # periodo en horas
    t0 = min(flow)
    t1 = max(flow)
    hours = (t1 - t0).total_seconds() / 3600.0
    rate = total_services / hours if hours>0 else 0.0
    return format_metric_response('usage_rate', round(rate, 2), samples=total_services, hours=round(hours, 2))

