# -*- coding: utf-8 -*-
"""
Endpoints to calculate OEE-like metrics for the water dispenser system.
All endpoint paths are in English and cover 10 key metrics.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
import datetime
import statistics

from storage import LocalStorage
from simulator import SensorSimulator
from anomalies import detect_anomalies as fetch_anomalies

from settings import *

router = APIRouter(prefix="/metrics")
storage = LocalStorage()
simulator = SensorSimulator()

# Nominal expected flow per user in L/min
NOMINAL_FLOW_PER_USER_LPM   = simulator.avg_flow_rate / 60.0

@router.get("/availability")
def get_availability(
    start: str = Query(None, description="ISO 8601 start timestamp"),
    end:   str = Query(None, description="ISO 8601 end timestamp")
) -> Dict[str, float]:
    """
    Availability: percentage of time flow > 0 between start and end.
    """
    readings = storage.fetch_all()
    flows = [r for r in readings if r['sensor']=='flow'
             and (not start or r['timestamp']>=start)
             and (not end  or r['timestamp']<=end)]
    total = len(flows)
    if total==0:
        raise HTTPException(404, "No flow readings in range")
    active = sum(1 for r in flows if r['value']>0)
    return {"availability_percent": round(active/total*100,2)}

@router.get("/performance")
def get_performance(
    users: int = Query(1, ge=1),
    hours: int = Query(1, ge=1)
) -> Dict[str, float]:
    """
    Performance: actual liters dispensed vs expected liters.
    """
    expected = simulator.avg_flow_rate * users * hours
    readings = storage.fetch_all()
    actual = sum(r['value'] for r in readings if r['sensor']=='flow')
    pct = (actual/expected*100) if expected>0 else 0.0
    return {"expected_liters":round(expected,3),"actual_liters":round(actual,3),"performance_percent":round(pct,2)}

@router.get("/quality")
def get_quality(
    start: str = Query(None),
    end:   str = Query(None)
) -> Dict[str, float]:
    """
    Quality: % of temperature readings within tolerance.
    """
    allr = storage.fetch_all()
    temps = [r for r in allr if r['sensor']=='temperature'
             and (not start or r['timestamp']>=start)
             and (not end  or r['timestamp']<=end)]
    total = len(temps)
    if total==0:
        raise HTTPException(404, "No temperature readings in range")
    good = sum(1 for r in temps if abs(r['value']-TEMPERATURE_SETPOINT)<=tmp_tolerance)
    return {"quality_percent": round(good/total*100,2)}

@router.get("/energy_efficiency")
def get_energy_efficiency(
    start: str = Query(None),
    end:   str = Query(None)
) -> Dict[str, float]:
    """
    Energy Efficiency: kWh consumed per liter dispensed.
    """
    rds = storage.fetch_all()
    power = [r for r in rds if r['sensor']=='power'
             and (not start or r['timestamp']>=start)
             and (not end  or r['timestamp']<=end)]
    flow  = [r for r in rds if r['sensor']=='flow'
             and (not start or r['timestamp']>=start)
             and (not end  or r['timestamp']<=end)]
    # Sum kWh: each reading value(kW) for 1 minute -> kWh = kW*(1/60)
    energy = sum(r['value'] for r in power)/60.0
    liters = sum(r['value'] for r in flow)
    if liters==0:
        raise HTTPException(404, "No flow to calculate efficiency")
    return {"kwh_per_liter": round(energy/liters,4)}

@router.get("/peak_flow_ratio")
def get_peak_flow_ratio(
    users: int = Query(1, ge=1)
) -> Dict[str, float]:
    """
    Peak Flow Ratio: max flow / nominal flow per user.
    """
    nominal = NOMINAL_FLOW_PER_USER_LPM * users
    flows = [r['value'] for r in storage.fetch_all() if r['sensor']=='flow']
    if not flows:
        raise HTTPException(404, "No flow readings")
    peak = max(flows)
    return {"peak_ratio": round(peak/nominal,2)}

@router.get("/mtba")
def get_mtba() -> Dict[str, float]:
    """
    Mean Time Between Anomalies (minutes).
    """
    anomalies = fetch_anomalies()
    times = [datetime.datetime.fromisoformat(a.timestamp) for a in anomalies]
    if len(times)<2:
        return {"mtba_minutes": 0.0}
    diffs = [(times[i]-times[i-1]).total_seconds()/60.0 for i in range(1,len(times))]
    return {"mtba_minutes": round(statistics.mean(diffs),2)}

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

@router.get("/response_index")
def get_response_index() -> Dict[str, float]:
    """
    Response Index: avg minutes from anomaly to recovery.
    """
    anomalies = fetch_anomalies()
    rds = storage.fetch_all()
    resp_times = []
    for a in anomalies:
        sensor=a.sensor; t0=datetime.datetime.fromisoformat(a.timestamp)
        # find next normal reading
        for r in rds:
            if r['sensor']==sensor and datetime.datetime.fromisoformat(r['timestamp'])>t0:
                val=r['value']
                if sensor=='temperature' and abs(val-TEMPERATURE_SETPOINT)<=tmp_tolerance:
                    t1=datetime.datetime.fromisoformat(r['timestamp']); resp_times.append((t1-t0).total_seconds()/60); break
                if sensor=='flow' and val>FLOW_INACTIVITY_THRESHOLD:
                    t1=datetime.datetime.fromisoformat(r['timestamp']); resp_times.append((t1-t0).total_seconds()/60); break
                if sensor=='level' and val>=LEVEL_LOW_THRESHOLD:
                    t1=datetime.datetime.fromisoformat(r['timestamp']); resp_times.append((t1-t0).total_seconds()/60); break
                if sensor=='power' and val<=POWER_HIGH_THRESHOLD:
                    t1=datetime.datetime.fromisoformat(r['timestamp']); resp_times.append((t1-t0).total_seconds()/60); break
    if not resp_times:
        return {"response_index_minutes":0.0}
    return {"response_index_minutes": round(statistics.mean(resp_times),2)}

@router.get("/thermal_variation")
def get_thermal_variation(
    start: str = Query(None),
    end:   str = Query(None)
) -> Dict[str, float]:
    """
    Thermal Variation: standard deviation of temperature readings.
    """
    temps=[r['value'] for r in storage.fetch_all() if r['sensor']=='temperature'
            and (not start or r['timestamp']>=start)
            and (not end  or r['timestamp']<=end)]
    if len(temps)<2:
        return {"thermal_variation":0.0}
    return {"thermal_variation": round(statistics.stdev(temps),2)}

@router.get("/nonproductive_consumption")
def get_nonproductive_consumption(
    start: str = Query(None),
    end:   str = Query(None)
) -> Dict[str, float]:
    """
    Nonproductive Consumption: kWh consumed when flow ≤ threshold.
    """
    rds=storage.fetch_all()
    power=[r for r in rds if r['sensor']=='power'
           and (not start or r['timestamp']>=start)
           and (not end  or r['timestamp']<=end)]
    flow=[r for r in rds if r['sensor']=='flow'
           and (not start or r['timestamp']>=start)
           and (not end  or r['timestamp']<=end)]
    # align readings by index
    energy=0.0
    for i,p in enumerate(power):
        f=flow[i] if i<len(flow) else {'value':0}
        if f['value']<=FLOW_INACTIVITY_THRESHOLD:
            energy+=p['value']/60.0
    return {"nonproductive_kwh": round(energy,3)}
