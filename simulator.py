# -*- coding: utf-8 -*-
"""
Stateful Sensor Simulator for a water dispenser with real-time adjustable parameters
and batch scenario simulation.
"""
import random
import datetime
import math
from typing import List, Dict, Optional
from storage import LocalStorage
from settings import (
    AVG_FLOW_RATE_DEFAULT, TIME_CONVERSION, TEMPERATURE_MEAN, TEMPERATURE_VARIATION,
    LEVEL_MIN, LEVEL_MAX, POWER_MIN, POWER_MAX, PIPE_MIN_LPM, PIPE_MAX_LPM,
    FLOW_VARIATION_LPM, FLOW_VARIATION_FACTOR, SETPOINT_TEMP_DEFAULT, MIN_FLOW_THRESHOLD,
    HEATER_REGIME_DEFAULT, PIPE_LENGTH, PIPE_DIAMETER, WATER_DENSITY, WATER_VISCOSITY,
    GRAVITY, PIPE_DELAY_SEC, TANK_CAPACITY_L, TANK_SEGMENTS, HEATER_POWER_MAX,
    HEATER_EFFICIENCY, CP_WATER, T_AMBIENT, CONVECTION_COEFF, SURFACE_AREA,
    THERMAL_DIFFUSIVITY, SENSOR_NOISE_STD, DEGRADATION_FACTOR
)

class SensorSimulator:
    """
    Stateless simulator that uses storage config for parameters.
    Each instance is independent and uses the latest config from storage.
    """

    def __init__(self,
                 avg_flow_rate: float = None,
                 temp_setpoint: float = None,
                 heater_regime: float = None):
        # Load config from storage or use provided values
        self.storage = LocalStorage()
        config = self.storage.get_config()
        
        # Use provided values, then config values, then defaults
        self.avg_flow_rate = avg_flow_rate if avg_flow_rate is not None else (config.get('avg_flow_rate') if config else AVG_FLOW_RATE_DEFAULT)
        self.temp_setpoint = temp_setpoint if temp_setpoint is not None else (config.get('temp_setpoint') if config else SETPOINT_TEMP_DEFAULT)
        self.heater_regime = heater_regime if heater_regime is not None else (config.get('heater_regime') if config else HEATER_REGIME_DEFAULT)
        
        # Load state from storage
        readings = self.storage.fetch_all()
        # init level
        level_readings = [r for r in readings if r['sensor']=='level']
        self.level = level_readings[-1]['value'] if level_readings else 1.0
        # init temperature profile
        temp_readings = [r for r in readings if r['sensor']=='temperature']
        init_temp = temp_readings[-1]['value'] if temp_readings else T_AMBIENT
        self.temperatures = [init_temp]*TANK_SEGMENTS
        self.heater_eff = HEATER_EFFICIENCY
        self.time_elapsed = 0  # seconds

    # --- Real-time adjusters ---
    def set_flow_rate(self, new_rate: float):
        """Adjust average flow rate and save to config"""
        self.avg_flow_rate = new_rate
        self._update_config()

    def set_temp_setpoint(self, new_setpoint: float):
        """Adjust temperature setpoint and save to config"""
        self.temp_setpoint = new_setpoint
        self._update_config()

    def set_heater_regime(self, new_regime: float):
        """Adjust heater regime and save to config"""
        self.heater_regime = new_regime
        self._update_config()
        
    def _update_config(self):
        """Update storage config with current simulator parameters"""
        config = self.storage.get_config()
        if config:
            self.storage.save_config(
                user_quantity=config['user_quantity'],
                hours=config['hours'],
                avg_flow_rate=self.avg_flow_rate,
                temp_setpoint=self.temp_setpoint,
                heater_regime=self.heater_regime
            )

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
        ts = timestamp if timestamp is not None else datetime.datetime.now(datetime.UTC).isoformat()

        # calculate default values:
        # base_flow_lpm = (self.avg_flow_rate * users) / TIME_CONVERSION
        # 2. Apply random variation and limit to physical pipe range
        #flow_lpm = base_flow_lpm + random.uniform(-FLOW_VARIATION_LPM, FLOW_VARIATION_LPM)
        #flow_lpm = max(PIPE_MIN_LPM, min(PIPE_MAX_LPM, flow_lpm))

        #total_flow_lph = flow_lpm * TIME_CONVERSION

        # total_flow_lph = self.avg_flow_rate * users

        # Nominal flow in L/min (avg_flow_rate is already in L/min per user)
        base_flow_lpm = self.avg_flow_rate * users

        # Apply random variation and limit to physical pipe range
        flow_lpm = base_flow_lpm * random.uniform(
            1 - FLOW_VARIATION_FACTOR,
            1 + FLOW_VARIATION_FACTOR
        )

        # Clamp to physical pipe range
        flow_lpm = min(PIPE_MAX_LPM, flow_lpm)

        # Avoid negative flows
        flow_lpm = max(0.0, flow_lpm)

        # Calculate total flow in L/h if needed
        total_flow_lph = flow_lpm * TIME_CONVERSION

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
                'flow': flow_lpm,  # Store flow in L/min
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

    # --- Batch scenario simulation ---
    def simulate_scenarios(self,
                           configs: List[Dict],
                           duration_hours: int = 1) -> List[Dict]:
        """
        Run batch simulations for each config dict containing:
        {'users': int, 'flow_rate': optional, 'temp_setpoint': optional, 'heater_regime': optional}
        Returns aggregated metrics per scenario: total energy, avg temperature, OEE etc.
        """
        results = []
        for cfg in configs:
            # create new simulator instance for isolation
            sim = SensorSimulator(
                avg_flow_rate=cfg.get('flow_rate'),
                temp_setpoint=cfg.get('temp_setpoint'),
                heater_regime=cfg.get('heater_regime')
            )
            total_energy = 0.0
            temp_sum = 0.0
            count = 0
            for minute in range(duration_hours * 60):
                frame = sim.generate_frame(users=cfg.get('users',1))
                # extract power value and temperature
                for r in frame:
                    if r['sensor']=='power': total_energy += r['value']*(1/60)
                    if r['sensor']=='temperature': temp_sum += r['value']; count+=1
            metrics = {
                'config': cfg,
                'total_energy_kWh': round(total_energy,3),
                'avg_temperature': round(temp_sum/count,2) if count else None
            }
            results.append(metrics)
        return results

    @property
    def sensors_count(self) -> int:
        return 4
