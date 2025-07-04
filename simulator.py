# -*- coding: utf-8 -*-
import random
import datetime
from typing import List, Dict, Optional

# Configuration constants:
AVG_FLOW_RATE_DEFAULT = 0.5    # L/h per user (average flow rate)
TIME_CONVERSION = 60.0         # minutes in an hour (for L/h to L/min)
TEMPERATURE_MEAN = 25.0        # °C (baseline temperature)
TEMPERATURE_VARIATION = 1.0    # °C (± range for temperature simulation)
LEVEL_MIN = 0.0                # lower bound for tank level (proportion)
LEVEL_MAX = 1.0                # upper bound for tank level (proportion)
POWER_MIN = 0.0                # kW (minimum power draw)
POWER_MAX = 10.0               # kW (maximum power draw)

class SensorSimulator:
    """
    Generates synthetic data for a water dispenser as a cyber-physical system.
    avg_flow_rate: liters per hour per user.
    """
    def __init__(self, avg_flow_rate: float = AVG_FLOW_RATE_DEFAULT):
        # average flow rate in liters per hour per user
        self.avg_flow_rate = avg_flow_rate

    def generate_frame(
        self,
        timestamp: Optional[str] = None,
        users: int = 1,
        sensor: Optional[str] = None,
        value: Optional[float] = None
    ) -> List[Dict]:
        """
        Generate a snapshot of sensor readings.
        If `sensor` is provided, only that sensor is returned,
        with its `value` and `timestamp` overridden if given.

        :param timestamp: ISO string for date/time; if None, uses current UTC.
        :param users: number of active users for flow simulation.
        :param sensor: name of sensor to override (flow, temperature, level, power).
        :param value: override value for the given sensor.
        :return: list of readings (dicts with sensor, timestamp, value).
        """
        # determine timestamp:
        ts = timestamp if timestamp is not None else datetime.datetime.utcnow().isoformat()

        # calculate default values:
        total_flow_lph = self.avg_flow_rate * users
        flow_lpm = total_flow_lph / TIME_CONVERSION
        temp_val = TEMPERATURE_MEAN + random.uniform(-TEMPERATURE_VARIATION, TEMPERATURE_VARIATION)
        level_val = random.uniform(LEVEL_MIN, LEVEL_MAX)
        power_val = random.uniform(POWER_MIN, POWER_MAX)

        # helper to create a reading dict
        def make_reading(name: str, default: float) -> Dict:
            return {
                "sensor": name,
                "timestamp": ts,
                "value": round(value if (sensor == name and value is not None) else default, 3),
            }

        # if a specific sensor override is requested, return only that
        if sensor:
            defaults = {
                'flow': flow_lpm,
                'temperature': temp_val,
                'level': level_val,
                'power': power_val,
            }
            if sensor not in defaults:
                raise ValueError(f"Unknown sensor '{sensor}'")
            return [make_reading(sensor, defaults[sensor])]

        # otherwise return all sensors
        readings = [
            make_reading('flow', flow_lpm),
            make_reading('temperature', temp_val),
            make_reading('level', level_val),
            make_reading('power', power_val),
        ]
        return readings

    @property
    def sensors_count(self) -> int:
        """
        Number of sensor types returned per full frame.
        """
        # generate a sample frame to count sensors
        return len(self.generate_frame(timestamp=datetime.datetime.utcnow().isoformat(), users=1))
    