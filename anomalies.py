# -*- coding: utf-8 -*-
from typing import List, Dict, Any
from storage import LocalStorage
from settings import *

storage = LocalStorage()


def detect_anomalies():
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
            if abs(val - temperature_setpoint) > TMP_TOLERANCE:
                anomalies.append({
                    "sensor": s, "timestamp": ts, "value": val,
                    "type": "Overtemperature",
                    "detail": f"Temperature {val}°C outside ±{TMP_TOLERANCE}°C of setpoint"
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
