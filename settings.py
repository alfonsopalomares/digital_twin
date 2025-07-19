# -*- coding: utf-8 -*-

# Parámetros y umbrales
temperature_setpoint       = 25.0   # °C
TMP_TOLERANCE              = 2.0    # ±2°C
FLOW_INACTIVITY_THRESHOLD  = 0.001  # L/min
FLOW_INACTIVITY_MINUTES    = 5      # minutos
LEVEL_LOW_THRESHOLD        = 0.2    # 20%
POWER_HIGH_THRESHOLD       = 0.04   # kW (80% of max power)

# === Configurable constants from simulator ===
# Configuration constants:
AVG_FLOW_RATE_DEFAULT = 0.008    # L/min per user (drinking water only - realistic office consumption)
TIME_CONVERSION = 60.0         # minutes in an hour (for L/min to L/h conversion)
TEMPERATURE_MEAN = 60.0        # °C (baseline temperature)
TEMPERATURE_VARIATION = 5.0    # °C (± range for temperature simulation)
LEVEL_MIN = 0.0                # lower bound for tank level (proportion)
LEVEL_MAX = 1.0                # upper bound for tank level (proportion)
POWER_MIN = 0.0                # kW (minimum power draw)
POWER_MAX = 0.05               # kW (maximum power draw - more realistic for low flow)

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
HEATER_POWER_MAX = 0.05        # kW (coherente con POWER_MAX)
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

