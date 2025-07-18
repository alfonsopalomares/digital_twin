# -*- coding: utf-8 =====
"""
Stateful Sensor Simulator for a water dispenser with real-time adjustable parameters
and batch scenario simulation.
"""
import random
import datetime
import math
from typing import List, Dict, Optional
from storage import LocalStorage

# === Configurable constants ===
# Configuration constants:
AVG_FLOW_RATE_DEFAULT = 0.008    # L/min per user (drinking water only - realistic office consumption)
TIME_CONVERSION = 60.0         # minutes in an hour (for L/min to L/h conversion)
TEMPERATURE_MEAN = 60.0        # °C (baseline temperature)
TEMPERATURE_VARIATION = 5.0    # °C (± range for temperature simulation)
LEVEL_MIN = 0.0                # lower bound for tank level (proportion)
LEVEL_MAX = 1.0                # upper bound for tank level (proportion)
POWER_MIN = 0.0                # kW (minimum power draw)
POWER_MAX = 10.0               # kW (maximum power draw)

# Physical parameters of a common pipe:
PIPE_MIN_LPM = 10    # typical minimum flow rate in L/min
PIPE_MAX_LPM = 30    # typical maximum flow rate in L/min
FLOW_VARIATION_LPM = 5  # random variation ±5 L/min
FLOW_VARIATION_FACTOR = 0.2  # random variation factor
SETPOINT_TEMP_DEFAULT = 60.0   # °C, default temperature setpoint
MIN_FLOW_THRESHOLD = 0.01      # L/min, minimum flow rate for a service
HEATER_REGIME_DEFAULT = 0.1    # kW per °C error
PIPE_LENGTH = 1.0              # m
PIPE_DIAMETER = 0.02           # m
WATER_DENSITY = 997.0          # kg/m³
WATER_VISCOSITY = 0.001        # Pa·s
GRAVITY = 9.81                 # m/s²
PIPE_DELAY_SEC = 5             # s
TANK_CAPACITY_L = 20.0         # liters
TANK_SEGMENTS = 5              # thermal layers
HEATER_POWER_MAX = 10.0        # kW
HEATER_EFFICIENCY = 0.8        # fraction
CP_WATER = 4.186               # kJ/kg·°C
T_AMBIENT = 25.0               # °C
CONVECTION_COEFF = 5.0         # W/m²·°C
SURFACE_AREA = 0.5             # m²
THERMAL_DIFFUSIVITY = 1e-7     # m²/s
SENSOR_NOISE_STD = {
    'flow': 0.005,
    'temperature': 0.1,
    'level': 0.002,
    'power': 0.1
}
DEGRADATION_FACTOR = 0.0001    # per minute

class SensorSimulator:
    _instance = None
    def __new__(cls, *args, **kwargs):
        # Singleton: ensure only one simulator instance persists
        if cls._instance is None:
            cls._instance = super(SensorSimulator, cls).__new__(cls)
        return cls._instance

    """
    Stateful simulator with advanced physics and persistent parameters.
    ...
    Extends previous stateful simulator with:
    - Real-time adjustable avg_flow_rate, temp_setpoint, heater_regime
    - Batch simulation for scenario comparisons
    """

    def __init__(self,
                 avg_flow_rate: float = AVG_FLOW_RATE_DEFAULT,
                 temp_setpoint: float = SETPOINT_TEMP_DEFAULT,
                 heater_regime: float = HEATER_REGIME_DEFAULT):
        # adjustable parameters
        self.avg_flow_rate = avg_flow_rate
        self.temp_setpoint = temp_setpoint
        self.heater_regime = heater_regime  # kW per °C error
        # load state
        self.storage = LocalStorage()
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
        """Adjust average flow rate on the fly"""
        self.avg_flow_rate = new_rate

    def set_temp_setpoint(self, new_setpoint: float):
        """Adjust temperature setpoint on the fly"""
        self.temp_setpoint = new_setpoint

    def set_heater_regime(self, new_regime: float):
        """Adjust heater regime (kW per °C error) on the fly"""
        self.heater_regime = new_regime

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
            # clone simulator for isolation
            sim = SensorSimulator(
                avg_flow_rate=cfg.get('flow_rate', self.avg_flow_rate),
                temp_setpoint=cfg.get('temp_setpoint', self.temp_setpoint),
                heater_regime=cfg.get('heater_regime', self.heater_regime)
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
