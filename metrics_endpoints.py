# -*- coding: utf-8 -*-
"""
Endpoints to calculate metrics from sensor data.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Dict, List, Optional, Union
import datetime, statistics
from anomalies_endpoints import adaptive_anomalies, get_anomalies
from storage import LocalStorage
from settings import *
from settings import AVG_FLOW_RATE_DEFAULT, SETPOINT_TEMP_DEFAULT, HEATER_REGIME_DEFAULT

router = APIRouter(prefix="/metrics", tags=["metrics"])
storage = LocalStorage()

# Helper function to classify anomalies
async def classify_anomalies(sensor: Optional[str] = None, window: int = 60) -> List[dict]:
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
    Availability: % time flow > 0 between start and end.
    
    Measures the percentage of time the system is actively dispensing water
    (flow > 0). Higher values indicate more active usage and better system
    utilization.
    
    Expected availability: > 50% for active systems
    Tolerance: > 30% for acceptable systems
    """
    # Constants for availability assessment
    EXCELLENT_AVAILABILITY = 80.0    # % - excellent system utilization
    GOOD_AVAILABILITY = 60.0         # % - good system utilization
    ACCEPTABLE_AVAILABILITY = 30.0   # % - acceptable system utilization
    
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
        return format_metric_response('availability', 0.0, expected_value=GOOD_AVAILABILITY, samples=0)
    
    # Calculate availability
    non_zero = sum(1 for r in flow_readings if r['value'] > 0)
    availability = round(non_zero / total * 100, 2)
    
    # Calculate flow statistics
    flow_values = [r['value'] for r in flow_readings]
    avg_flow = round(statistics.mean(flow_values), 3)
    min_flow = round(min(flow_values), 3)
    max_flow = round(max(flow_values), 3)
    flow_std = round(statistics.stdev(flow_values), 3) if len(flow_values) > 1 else 0.0
    
    # Determine availability status
    if availability >= EXCELLENT_AVAILABILITY:
        availability_status = 'excellent'
    elif availability >= GOOD_AVAILABILITY:
        availability_status = 'good'
    elif availability >= ACCEPTABLE_AVAILABILITY:
        availability_status = 'acceptable'
    else:
        availability_status = 'poor'
    
    # Calculate flow distribution
    zero_count = sum(1 for v in flow_values if v == 0)
    low_count = sum(1 for v in flow_values if 0 < v <= 0.01)  # Very low flow
    normal_count = sum(1 for v in flow_values if v > 0.01)    # Normal flow
    
    zero_percent = round((zero_count / total) * 100, 1)
    low_percent = round((low_count / total) * 100, 1)
    normal_percent = round((normal_count / total) * 100, 1)
    
    # Calculate time span
    if flow_readings:
        timestamps = [datetime.datetime.fromisoformat(r['timestamp']) for r in flow_readings]
        time_span_hours = round((max(timestamps) - min(timestamps)).total_seconds() / 3600.0, 2)
    else:
        time_span_hours = 0.0
    
    # Calculate flow variability
    flow_variability = round((flow_std / avg_flow) * 100, 1) if avg_flow > 0 else 0.0
    
    # Calculate total volume dispensed (approximate)
    total_volume = 0.0
    for i in range(len(flow_readings) - 1):
        current = flow_readings[i]
        next_reading = flow_readings[i + 1]
        t1 = datetime.datetime.fromisoformat(current['timestamp'])
        t2 = datetime.datetime.fromisoformat(next_reading['timestamp'])
        dt_min = abs((t2 - t1).total_seconds() / 60.0)  # Use absolute value to avoid negative
        total_volume += current['value'] * dt_min
    
    # Prepare response with additional metadata
    response = format_metric_response('availability', availability, expected_value=GOOD_AVAILABILITY, samples=total)
    
    # Add metadata useful for frontend visualization
    response.update({
        'avg_flow': avg_flow,
        'min_flow': min_flow,
        'max_flow': max_flow,
        'flow_std': flow_std,
        'flow_variability': flow_variability,
        'availability_status': availability_status,
        'time_span_hours': time_span_hours,
        'total_volume': round(total_volume, 2),
        'zero_count': zero_count,
        'low_count': low_count,
        'normal_count': normal_count,
        'zero_percent': zero_percent,
        'low_percent': low_percent,
        'normal_percent': normal_percent,
        'excellent_threshold': EXCELLENT_AVAILABILITY,
        'good_threshold': GOOD_AVAILABILITY,
        'acceptable_threshold': ACCEPTABLE_AVAILABILITY
    })
    
    return response

@router.get("/performance", summary="Performance: actual vs expected liters dispensed")
def get_performance(
    users: Optional[int] = Query(None, ge=1),
    hours: Optional[int] = Query(None, ge=1)
) -> MetricResponse:
    """
    Performance: actual vs expected liters dispensed.
    
    Compares actual liters dispensed vs expected based on configured flow rate,
    user quantity, and time period. Performance ratio indicates system efficiency
    and capacity utilization.
    
    Expected performance: 0.95-1.05 ratio for optimal operation
    Tolerance: 0.85-1.15 ratio for acceptable operation
    """
    # Constants for performance assessment
    # Adjusted for more realistic water dispenser performance expectations
    EXCELLENT_PERFORMANCE = 1.05   # ratio - excellent capacity utilization (≥105%)
    GOOD_PERFORMANCE = 0.95        # ratio - good capacity utilization (≥95%)
    ACCEPTABLE_PERFORMANCE = 0.85  # ratio - acceptable capacity utilization (≥85%)
    MIN_ACCEPTABLE = 0.70          # ratio - minimum acceptable performance (≥70%)
    
    # 1) Load and update config
    config = storage.get_config()
    if config is None:
        config = {'user_quantity': 1, 'hours': 1}
        # ensure defaults with simulator parameters
        storage.save_config(
            user_quantity=config['user_quantity'], 
            hours=config['hours'],
            avg_flow_rate=AVG_FLOW_RATE_DEFAULT,
            temp_setpoint=SETPOINT_TEMP_DEFAULT,
            heater_regime=HEATER_REGIME_DEFAULT
        )

    # Handle optional parameters - use provided values or defaults from config
    # Check if parameters are actual values or Query objects
    users_final = users if users is not None and not hasattr(users, 'default') else config['user_quantity']
    hours_final = hours if hours is not None and not hasattr(hours, 'default') else config['hours']

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
    # Note: flow_logs already contain the total flow for all users
    for prev, curr in zip(flow_logs, flow_logs[1:]):
        t0 = datetime.datetime.fromisoformat(prev['timestamp'])
        t1 = datetime.datetime.fromisoformat(curr['timestamp'])
        dt_min = abs((t1 - t0).total_seconds() / 60.0)  # Use absolute value to avoid negative
        actual_liters += prev['value'] * dt_min

    # If there was only one sample or none, actual_liters will remain 0.0

    # 4) Calculate expected using configured flow rate (L/min, convert to L/h for hourly calculation)
    expected_liters = (config['avg_flow_rate'] * 60) * users_final * hours_final

    # 5) Performance as ratio (actual vs expected)
    performance_ratio = (
        round(actual_liters / expected_liters, 3)
        if expected_liters > 0 else 0.0
    )

    # Determine performance status
    if performance_ratio >= EXCELLENT_PERFORMANCE:
        performance_status = 'excellent'
    elif performance_ratio >= GOOD_PERFORMANCE:
        performance_status = 'good'
    elif performance_ratio >= ACCEPTABLE_PERFORMANCE:
        performance_status = 'acceptable'
    elif performance_ratio >= MIN_ACCEPTABLE:
        performance_status = 'poor'
    else:
        performance_status = 'critical'

    # Calculate flow statistics
    flow_values = [r['value'] for r in flow_logs]
    avg_flow = round(statistics.mean(flow_values), 3) if flow_values else 0.0
    min_flow = round(min(flow_values), 3) if flow_values else 0.0
    max_flow = round(max(flow_values), 3) if flow_values else 0.0
    flow_std = round(statistics.stdev(flow_values), 3) if len(flow_values) > 1 else 0.0

    # Calculate time span
    if flow_logs:
        timestamps = [datetime.datetime.fromisoformat(r['timestamp']) for r in flow_logs]
        time_span_hours = round((max(timestamps) - min(timestamps)).total_seconds() / 3600.0, 2)
    else:
        time_span_hours = 0.0

    # Calculate flow variability
    flow_variability = round((flow_std / avg_flow) * 100, 1) if avg_flow > 0 else 0.0

    # Calculate efficiency metrics
    efficiency_percent = round(performance_ratio * 100, 1)
    deficit_liters = round(expected_liters - actual_liters, 2) if actual_liters < expected_liters else 0.0
    surplus_liters = round(actual_liters - expected_liters, 2) if actual_liters > expected_liters else 0.0

    # Calculate average flow rate achieved
    achieved_flow_rate = round(actual_liters / (time_span_hours * 60), 3) if time_span_hours > 0 else 0.0

    # Prepare response with additional metadata
    response = format_metric_response('performance', performance_ratio, expected_value=round(expected_liters, 2), samples=len(flow_logs), users=users_final, hours=hours_final)

    # Add metadata useful for frontend visualization
    response.update({
        'actual_liters': round(actual_liters, 2),
        'performance_status': performance_status,
        'efficiency_percent': efficiency_percent,
        'deficit_liters': deficit_liters,
        'surplus_liters': surplus_liters,
        'avg_flow': avg_flow,
        'min_flow': min_flow,
        'max_flow': max_flow,
        'flow_std': flow_std,
        'flow_variability': flow_variability,
        'achieved_flow_rate': achieved_flow_rate,
        'configured_flow_rate': config['avg_flow_rate'],
        'time_span_hours': time_span_hours,
        'excellent_threshold': EXCELLENT_PERFORMANCE,
        'good_threshold': GOOD_PERFORMANCE,
        'acceptable_threshold': ACCEPTABLE_PERFORMANCE,
        'min_acceptable': MIN_ACCEPTABLE
    })

    return response

@router.get("/quality", summary="Quality: % temperature within ±5°C setpoint")
def get_quality(
    start: Optional[str] = Query(
        None, description="ISO start timestamp (inclusive)"
    ),
    end: Optional[str] = Query(
        None, description="ISO end timestamp (inclusive)"
    ),

) -> MetricResponse:
    """
    Quality: % temperature within ±5°C setpoint.
    
    Measures the percentage of temperature readings within the acceptable
    tolerance band around the setpoint. Higher values indicate better
    temperature control and consistency.
    
    Expected quality: > 95% for excellent temperature control
    Tolerance: > 90% for acceptable temperature control
    """
    # Constants for quality assessment
    EXCELLENT_QUALITY = 98.0    # % - excellent temperature control
    GOOD_QUALITY = 95.0         # % - good temperature control
    ACCEPTABLE_QUALITY = 90.0   # % - acceptable temperature control

    from settings import TEMPERATURE_VARIATION, SETPOINT_TEMP_DEFAULT

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
        return format_metric_response('quality', 0.0, expected_value=GOOD_QUALITY, samples=0)

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
        return format_metric_response('quality', 0.0, expected_value=GOOD_QUALITY, samples=0)

    # 4) Count readings within ±5°C of setpoint
    within_count = sum(
        1 for l in window_logs
        if abs(l['value'] - SETPOINT_TEMP_DEFAULT) <= (TEMPERATURE_VARIATION/2)
    )

    # 5) Compute quality percentage
    quality_percent = round((within_count / total) * 100.0, 2)

    # Determine quality status
    if quality_percent >= EXCELLENT_QUALITY:
        quality_status = 'excellent'
    elif quality_percent >= GOOD_QUALITY:
        quality_status = 'good'
    elif quality_percent >= ACCEPTABLE_QUALITY:
        quality_status = 'acceptable'
    else:
        quality_status = 'poor'

    # Calculate temperature statistics
    temp_values = [l['value'] for l in window_logs]
    avg_temp = round(statistics.mean(temp_values), 2)
    min_temp = round(min(temp_values), 2)
    max_temp = round(max(temp_values), 2)
    temp_std = round(statistics.stdev(temp_values), 2) if len(temp_values) > 1 else 0.0

    # Calculate temperature distribution
    tolerance_half = TEMPERATURE_VARIATION / 2
    low_count = sum(1 for v in temp_values if v < SETPOINT_TEMP_DEFAULT - tolerance_half)
    within_count_actual = sum(1 for v in temp_values if abs(v - SETPOINT_TEMP_DEFAULT) <= tolerance_half)
    high_count = sum(1 for v in temp_values if v > SETPOINT_TEMP_DEFAULT + tolerance_half)

    low_percent = round((low_count / total) * 100, 1)
    within_percent = round((within_count_actual / total) * 100, 1)
    high_percent = round((high_count / total) * 100, 1)

    # Calculate time span
    if window_logs:
        timestamps = [l['timestamp'] for l in window_logs]
        time_span_hours = round((max(timestamps) - min(timestamps)).total_seconds() / 3600.0, 2)
    else:
        time_span_hours = 0.0

    # Calculate temperature variability
    temp_variability = round((temp_std / avg_temp) * 100, 1) if avg_temp > 0 else 0.0

    # Calculate deviation from setpoint
    avg_deviation = round(abs(avg_temp - SETPOINT_TEMP_DEFAULT), 2)
    max_deviation = round(max(abs(v - SETPOINT_TEMP_DEFAULT) for v in temp_values), 2)

    # 6) Prepare response with additional metadata for frontend
    response = format_metric_response('quality', quality_percent, expected_value=GOOD_QUALITY, samples=total)
    
    # Add metadata useful for frontend visualization
    response.update({
        'setpoint': SETPOINT_TEMP_DEFAULT,
        'tolerance_band': TEMPERATURE_VARIATION,
        'within_count': within_count,
        'total_count': total,
        'quality_status': quality_status,
        'avg_temp': avg_temp,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'temp_std': temp_std,
        'temp_variability': temp_variability,
        'avg_deviation': avg_deviation,
        'max_deviation': max_deviation,
        'time_span_hours': time_span_hours,
        'low_count': low_count,
        'high_count': high_count,
        'low_percent': low_percent,
        'within_percent': within_percent,
        'high_percent': high_percent,
        'excellent_threshold': EXCELLENT_QUALITY,
        'good_threshold': GOOD_QUALITY,
        'acceptable_threshold': ACCEPTABLE_QUALITY
    })

    return response

@router.get("/energy_efficiency", summary="Energy Efficiency: kWh per liter dispensed")
def get_energy_efficiency(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
    """
    Calculates kWh consumed per liter dispensed.
    
    Energy efficiency is measured as kWh per liter of water dispensed.
    Lower values indicate better efficiency (less energy per liter).
    
    Expected efficiency: ~0.05-0.15 kWh/L for typical water heating systems
    Tolerance: ±0.025 kWh/L from expected value
    """
    # Constants for energy efficiency calculation
    # For heating water from 25°C to 60°C with 80% heater efficiency
    # Energy = (0.997 kg × 4.186 kJ/kg·°C × 35°C) / 0.8 = 182.6 kJ = 0.0507 kWh
    EXPECTED_EFFICIENCY = 0.051  # kWh/L - theoretical minimum for 25°C→60°C
    EFFICIENCY_TOLERANCE = 0.025  # kWh/L - acceptable deviation (±50% of expected)
    
    readings = storage.fetch_all()
    power_readings = [r for r in readings if r['sensor'] == 'power']
    flow_readings = [r for r in readings if r['sensor'] == 'flow']
    
    # Filter by time window
    if start:
        start_dt = datetime.datetime.fromisoformat(start)
        power_readings = [r for r in power_readings if datetime.datetime.fromisoformat(r['timestamp']) >= start_dt]
        flow_readings = [r for r in flow_readings if datetime.datetime.fromisoformat(r['timestamp']) >= start_dt]
    if end:
        end_dt = datetime.datetime.fromisoformat(end)
        power_readings = [r for r in power_readings if datetime.datetime.fromisoformat(r['timestamp']) <= end_dt]
        flow_readings = [r for r in flow_readings if datetime.datetime.fromisoformat(r['timestamp']) <= end_dt]
    
    # Calculate total energy and volume
    total_kwh = sum(r['value'] * (1/60) for r in power_readings)  # Convert kW to kWh (1 minute intervals)
    total_liters = sum(r['value'] for r in flow_readings) * (1/60)  # Convert L/min to L (1 minute intervals)
    
    # Calculate efficiency
    efficiency = round(total_kwh / total_liters, 3) if total_liters > 0 else 0.0
    
    # Calculate efficiency ratio (current vs expected)
    efficiency_ratio = round(efficiency / EXPECTED_EFFICIENCY, 2) if EXPECTED_EFFICIENCY > 0 else 0.0
    
    # Determine if efficiency is within tolerance
    within_tolerance = abs(efficiency - EXPECTED_EFFICIENCY) <= EFFICIENCY_TOLERANCE
    
    # Prepare response with additional metadata for frontend
    response = format_metric_response('energy_efficiency', efficiency, expected_value=EXPECTED_EFFICIENCY, samples=len(power_readings))
    
    # Add metadata useful for frontend visualization
    response.update({
        'tolerance_band': EFFICIENCY_TOLERANCE * 2,  # Total band width (±0.025 = 0.05 total)
        'efficiency_ratio': efficiency_ratio,
        'within_tolerance': 1 if within_tolerance else 0,  # Convert to integer for consistency
        'total_kwh': round(total_kwh, 3),
        'total_liters': round(total_liters, 3),
        'efficiency_status': 'excellent' if efficiency <= EXPECTED_EFFICIENCY * 1.5 else 
                           'good' if efficiency <= EXPECTED_EFFICIENCY * 3 else
                           'poor' if efficiency <= EXPECTED_EFFICIENCY * 10 else 'critical'
    })
    
    return response

@router.get("/thermal_variation", summary="Thermal Variation: std dev of temperature readings")
def get_thermal_variation(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
    """
    Standard deviation of temperature readings between start and end.
    
    Thermal variation measures the consistency of temperature control.
    Lower values indicate better temperature stability.
    
    Expected variation: < 2°C for good control
    Tolerance: < 5°C for acceptable control
    """
    from settings import SETPOINT_TEMP_DEFAULT, TMP_TOLERANCE
    
    # Constants for thermal variation assessment
    EXCELLENT_VARIATION = 1.0   # °C - excellent temperature control
    GOOD_VARIATION = 2.0        # °C - good temperature control  
    ACCEPTABLE_VARIATION = 5.0  # °C - acceptable temperature control
    
    readings = storage.fetch_all()
    temp_readings = [r for r in readings if r['sensor'] == 'temperature']
    
    # Filter by time window
    if start:
        start_dt = datetime.datetime.fromisoformat(start)
        temp_readings = [r for r in temp_readings if datetime.datetime.fromisoformat(r['timestamp']) >= start_dt]
    if end:
        end_dt = datetime.datetime.fromisoformat(end)
        temp_readings = [r for r in temp_readings if datetime.datetime.fromisoformat(r['timestamp']) <= end_dt]
    
    temps = [r['value'] for r in temp_readings]
    
    if len(temps) < 2:
        return format_metric_response('thermal_variation', 0.0, samples=len(temps))
    
    # Calculate thermal variation statistics
    variation = round(statistics.stdev(temps), 2)
    avg_temp = round(statistics.mean(temps), 2)
    min_temp = round(min(temps), 2)
    max_temp = round(max(temps), 2)
    temp_range = round(max_temp - min_temp, 2)
    
    # Calculate deviation from setpoint
    setpoint_deviation = round(abs(avg_temp - SETPOINT_TEMP_DEFAULT), 2)
    
    # Determine variation status
    if variation <= EXCELLENT_VARIATION:
        variation_status = 'excellent'
    elif variation <= GOOD_VARIATION:
        variation_status = 'good'
    elif variation <= ACCEPTABLE_VARIATION:
        variation_status = 'acceptable'
    else:
        variation_status = 'poor'
    
    # Calculate percentage of readings within tolerance
    within_tolerance_count = sum(1 for t in temps if abs(t - SETPOINT_TEMP_DEFAULT) <= TMP_TOLERANCE)
    within_tolerance_percent = round((within_tolerance_count / len(temps)) * 100, 1)
    
    # Prepare response with additional metadata
    response = format_metric_response('thermal_variation', variation, expected_value=GOOD_VARIATION, samples=len(temps))
    
    # Add metadata useful for frontend visualization
    response.update({
        'avg_temperature': avg_temp,
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'temperature_range': temp_range,
        'setpoint': SETPOINT_TEMP_DEFAULT,
        'setpoint_deviation': setpoint_deviation,
        'variation_status': variation_status,
        'within_tolerance_count': within_tolerance_count,
        'within_tolerance_percent': within_tolerance_percent,
        'excellent_threshold': EXCELLENT_VARIATION,
        'good_threshold': GOOD_VARIATION,
        'acceptable_threshold': ACCEPTABLE_VARIATION,
        'unit': '°C'
    })
    
    return response



@router.get("/peak_flow_ratio", summary="Peak Flow Ratio: max flow / nominal")
def get_peak_flow_ratio(
    users: int = Query(1, ge=1)
) -> MetricResponse:
    """
    Ratio of max observed flow to nominal flow (avg_rate*users).
    
    Peak flow ratio measures the maximum flow rate compared to the nominal design flow.
    A ratio close to 1.0 indicates the system operates as designed.
    
    Expected ratio: ~1.0-1.5 for normal operation
    Tolerance: < 2.0 for acceptable operation
    """
    from settings import PIPE_MAX_LPM, PIPE_MIN_LPM
    
    # Constants for peak flow ratio assessment
    EXCELLENT_RATIO = 1.2    # Excellent peak flow control
    GOOD_RATIO = 1.5         # Good peak flow control
    ACCEPTABLE_RATIO = 2.0   # Acceptable peak flow control
    
    readings = storage.fetch_all()
    flow_readings = [r for r in readings if r['sensor']=='flow']
    
    if not flow_readings:
        return format_metric_response('peak_flow_ratio', 0.0, expected_value=0.0, samples=0, users=users)
    
    # Calculate flow statistics
    flow_values = [r['value'] for r in flow_readings]
    max_flow = max(flow_values)
    min_flow = min(flow_values)
    avg_flow = round(statistics.mean(flow_values), 3)
    flow_std = round(statistics.stdev(flow_values), 3) if len(flow_values) > 1 else 0.0
    
    # Get configured flow rate from storage
    config = storage.get_config()
    avg_flow_rate = config.get('avg_flow_rate') if config else AVG_FLOW_RATE_DEFAULT
    
    # Calculate nominal system flow (not user consumption)
    # The system should be designed to handle multiple users and peak demands
    nominal_system_flow = avg_flow_rate * users * 5  # Assume 5x peak factor for system design
    user_consumption = avg_flow_rate * users  # Actual user consumption
    
    # Calculate peak flow ratio (system capacity vs actual peak)
    ratio = round(max_flow / nominal_system_flow, 2) if nominal_system_flow > 0 else 0.0
    
    # Calculate additional ratios
    avg_ratio = round(avg_flow / nominal_system_flow, 2) if nominal_system_flow > 0 else 0.0
    min_ratio = round(min_flow / nominal_system_flow, 2) if nominal_system_flow > 0 else 0.0
    
    # Determine ratio status
    if ratio <= EXCELLENT_RATIO:
        ratio_status = 'excellent'
    elif ratio <= GOOD_RATIO:
        ratio_status = 'good'
    elif ratio <= ACCEPTABLE_RATIO:
        ratio_status = 'acceptable'
    else:
        ratio_status = 'excessive'
    
    # Calculate flow variability
    flow_variability = round((flow_std / avg_flow) * 100, 1) if avg_flow > 0 else 0.0
    
    # Check if max flow exceeds pipe capacity
    exceeds_pipe_capacity = max_flow > PIPE_MAX_LPM
    below_pipe_minimum = min_flow < PIPE_MIN_LPM
    
    # Calculate percentage of readings above nominal
    above_nominal_count = sum(1 for f in flow_values if f > nominal_system_flow)
    above_nominal_percent = round((above_nominal_count / len(flow_values)) * 100, 1)
    
    # Prepare response with additional metadata
    response = format_metric_response('peak_flow_ratio', ratio, expected_value=1.0, samples=len(flow_values), users=users)
    
    # Add metadata useful for frontend visualization
    response.update({
        'max_flow': round(max_flow, 3),
        'min_flow': round(min_flow, 3),
        'avg_flow': avg_flow,
        'nominal_system_flow': round(nominal_system_flow, 3),
        'user_consumption': round(user_consumption, 3),
        'avg_ratio': avg_ratio,
        'min_ratio': min_ratio,
        'flow_std': flow_std,
        'flow_variability': flow_variability,
        'ratio_status': ratio_status,
        'above_nominal_count': above_nominal_count,
        'above_nominal_percent': above_nominal_percent,
        'exceeds_pipe_capacity': exceeds_pipe_capacity,
        'below_pipe_minimum': below_pipe_minimum,
        'pipe_max_capacity': PIPE_MAX_LPM,
        'pipe_min_capacity': PIPE_MIN_LPM,
        'excellent_threshold': EXCELLENT_RATIO,
        'good_threshold': GOOD_RATIO,
        'acceptable_threshold': ACCEPTABLE_RATIO,
        'unit': 'ratio'
    })
    
    return response

@router.get("/mtba", summary="Mean Time Between Adaptive Anomalies")
async def get_mtba(
    window: int = Query(60, ge=1, description="Rolling window for adaptive anomalies"),
    sensor: Optional[str] = Query(None, description="Filter by sensor name")
) -> MetricResponse:
    """
    Mean Time Between adaptive anomalies (minutes) using rolling z-score method.
    
    MTBA measures the average time between adaptive anomalies detected using z-score analysis.
    Higher values indicate better system stability and fewer anomalies.
    
    Expected MTBA: > 30 minutes for stable systems
    Tolerance: > 15 minutes for acceptable systems
    """
    # Constants for MTBA assessment
    # Adjusted for water dispenser system in active use
    EXCELLENT_MTBA = 30.0    # minutes - excellent system stability (30+ min between anomalies)
    GOOD_MTBA = 15.0         # minutes - good system stability (15+ min between anomalies)
    ACCEPTABLE_MTBA = 5.0    # minutes - acceptable system stability (5+ min between anomalies)
    
    try:
        anomalies = await adaptive_anomalies(sensor=sensor, window=window)
    except Exception as e:
        print(f"Error in adaptive_anomalies: {e}")
        return format_metric_response('mtba', 0.0, expected_value=GOOD_MTBA, samples=0)
    
    if not anomalies:
        return format_metric_response('mtba', 0.0, expected_value=GOOD_MTBA, samples=0)
    
    if len(anomalies) < 2:
        return format_metric_response('mtba', 0.0, expected_value=GOOD_MTBA, samples=len(anomalies))
    
    # Calculate time differences between anomalies (grouping by timestamp)
    try:
        # Group anomalies by timestamp to avoid 0-minute intervals
        timestamp_groups = {}
        for anomaly in anomalies:
            ts = anomaly['timestamp']
            if ts not in timestamp_groups:
                timestamp_groups[ts] = []
            timestamp_groups[ts].append(anomaly)
        
        # Use unique timestamps for MTBA calculation
        unique_times = sorted(datetime.datetime.fromisoformat(ts) for ts in timestamp_groups.keys())
        
        if len(unique_times) < 2:
            return format_metric_response('mtba', 0.0, expected_value=GOOD_MTBA, samples=len(anomalies))
        
        diffs = [(unique_times[i] - unique_times[i-1]).total_seconds() / 60.0 for i in range(1, len(unique_times))]
    except Exception as e:
        print(f"Error parsing timestamps: {e}")
        return format_metric_response('mtba', 0.0, expected_value=GOOD_MTBA, samples=len(anomalies))
    
    # Calculate MTBA statistics
    mtba = round(statistics.mean(diffs), 2)
    min_interval = round(min(diffs), 2) if diffs else 0.0
    max_interval = round(max(diffs), 2) if diffs else 0.0
    interval_std = round(statistics.stdev(diffs), 2) if len(diffs) > 1 else 0.0
    
    # Calculate anomaly rate (anomalies per hour)
    try:
        total_time_hours = (unique_times[-1] - unique_times[0]).total_seconds() / 3600.0 if len(unique_times) > 1 else 0.0
        # Use unique timestamps for rate calculation
        unique_anomaly_count = len(unique_times)
        anomaly_rate = round(unique_anomaly_count / total_time_hours, 2) if total_time_hours > 0 else 0.0
    except Exception as e:
        print(f"Error calculating time: {e}")
        total_time_hours = 0.0
        anomaly_rate = 0.0
    
    # Determine MTBA status
    if mtba >= EXCELLENT_MTBA:
        mtba_status = 'excellent'
    elif mtba >= GOOD_MTBA:
        mtba_status = 'good'
    elif mtba >= ACCEPTABLE_MTBA:
        mtba_status = 'acceptable'
    else:
        mtba_status = 'poor'
    
    # Analyze anomalies by sensor type
    sensor_counts = {}
    for anomaly in anomalies:
        sensor_type = anomaly['sensor']
        sensor_counts[sensor_type] = sensor_counts.get(sensor_type, 0) + 1
    
    # Calculate anomaly distribution
    total_anomalies = len(anomalies)
    sensor_distribution = {sensor: round((count / total_anomalies) * 100, 1) for sensor, count in sensor_counts.items()} if total_anomalies > 0 else {}
    
    # Calculate time span of analysis
    time_span_hours = round(total_time_hours, 2) if total_time_hours > 0 else 0.0
    
    # Prepare response with additional metadata
    response = format_metric_response('mtba', mtba, expected_value=GOOD_MTBA, samples=len(anomalies))
    
    # Add information about anomaly grouping
    total_anomalies = len(anomalies)
    unique_events = len(unique_times) if 'unique_times' in locals() else 0
    simultaneous_anomalies = total_anomalies - unique_events
    
    # Add metadata useful for frontend visualization
    response.update({
        'min_interval': min_interval,
        'max_interval': max_interval,
        'interval_std': interval_std,
        'anomaly_rate': anomaly_rate,
        'mtba_status': mtba_status,
        'time_span_hours': time_span_hours,
        'window_size': window,
        'excellent_threshold': EXCELLENT_MTBA,
        'good_threshold': GOOD_MTBA,
        'acceptable_threshold': ACCEPTABLE_MTBA,
        'unit': 'minutes',
        'total_anomalies': total_anomalies,
        'unique_events': unique_events,
        'simultaneous_anomalies': simultaneous_anomalies
    })
    
    # Add sensor counts as individual fields
    for sensor_type, count in sensor_counts.items():
        response[f'sensor_count_{sensor_type}'] = count
    
    # Add sensor distribution as individual fields
    for sensor_type, percentage in sensor_distribution.items():
        response[f'sensor_distribution_{sensor_type}'] = percentage
    
    # Add filtered sensor info
    if sensor:
        response['filtered_sensor'] = sensor
    else:
        response['filtered_sensor'] = 'all'
    
    return response

@router.get("/level_uptime", summary="Level Uptime: % time level between low threshold and full")
def get_level_uptime(
    start: Optional[str] = Query(None, description="ISO start timestamp"),
    end: Optional[str] = Query(None, description="ISO end timestamp")
) -> MetricResponse:
    """
    Level Uptime: % time level between low threshold and full.
    
    Measures the percentage of time the water level is within acceptable range
    (between low threshold and full capacity). Higher values indicate better
    water availability and system reliability.
    
    Expected uptime: > 95% for reliable systems
    Tolerance: > 80% for acceptable systems
    """
    # Constants for level uptime assessment
    EXCELLENT_UPTIME = 98.0    # % - excellent water availability
    GOOD_UPTIME = 95.0         # % - good water availability
    ACCEPTABLE_UPTIME = 80.0   # % - acceptable water availability
    
    from settings import LEVEL_LOW_THRESHOLD
    
    rds = storage.fetch_all()
    levels = [r for r in rds if r['sensor']=='level'
              and (not start or r['timestamp']>=start)
              and (not end  or r['timestamp']<=end)]
    
    total = len(levels)
    if total == 0:
        raise HTTPException(404, "No level readings")
    
    # Calculate uptime
    ok = sum(1 for r in levels if LEVEL_LOW_THRESHOLD <= r['value'] <= 1)
    uptime = round(ok/total*100, 2)
    
    # Calculate level statistics
    level_values = [r['value'] for r in levels]
    avg_level = round(statistics.mean(level_values), 3)
    min_level = round(min(level_values), 3)
    max_level = round(max(level_values), 3)
    level_std = round(statistics.stdev(level_values), 3) if len(level_values) > 1 else 0.0
    
    # Determine uptime status
    if uptime >= EXCELLENT_UPTIME:
        uptime_status = 'excellent'
    elif uptime >= GOOD_UPTIME:
        uptime_status = 'good'
    elif uptime >= ACCEPTABLE_UPTIME:
        uptime_status = 'acceptable'
    else:
        uptime_status = 'poor'
    
    # Calculate level distribution
    low_count = sum(1 for v in level_values if v < LEVEL_LOW_THRESHOLD)
    normal_count = sum(1 for v in level_values if LEVEL_LOW_THRESHOLD <= v <= 1)
    high_count = sum(1 for v in level_values if v > 1)  # Overflow condition
    
    low_percent = round((low_count / total) * 100, 1)
    normal_percent = round((normal_count / total) * 100, 1)
    high_percent = round((high_count / total) * 100, 1)
    
    # Calculate time span
    if levels:
        timestamps = [datetime.datetime.fromisoformat(r['timestamp']) for r in levels]
        time_span_hours = round((max(timestamps) - min(timestamps)).total_seconds() / 3600.0, 2)
    else:
        time_span_hours = 0.0
    
    # Calculate level variability
    level_variability = round((level_std / avg_level) * 100, 1) if avg_level > 0 else 0.0
    
    # Prepare response with additional metadata
    response = format_metric_response('level_uptime', uptime, expected_value=GOOD_UPTIME, samples=total)
    
    # Add metadata useful for frontend visualization
    response.update({
        'avg_level': avg_level,
        'min_level': min_level,
        'max_level': max_level,
        'level_std': level_std,
        'level_variability': level_variability,
        'uptime_status': uptime_status,
        'time_span_hours': time_span_hours,
        'low_threshold': LEVEL_LOW_THRESHOLD,
        'low_count': low_count,
        'normal_count': normal_count,
        'high_count': high_count,
        'low_percent': low_percent,
        'normal_percent': normal_percent,
        'high_percent': high_percent,
        'excellent_threshold': EXCELLENT_UPTIME,
        'good_threshold': GOOD_UPTIME,
        'acceptable_threshold': ACCEPTABLE_UPTIME
    })
    
    return response

@router.get("/response_index", summary="Response Index to Adaptive Anomalies")
async def get_response_index(
    window: int = Query(60, ge=1, description="Rolling window for adaptive anomalies"),
    sensor: Optional[str] = Query(None, description="Filter by sensor name")
) -> MetricResponse:
    """
    Response Index: average minutes from adaptive anomaly to recovery.
    
    Measures the average time it takes for the system to recover from
    adaptive anomalies detected using z-score analysis. Lower values
    indicate faster response and better system resilience.
    
    Expected response time: < 5 minutes for good system responsiveness
    Tolerance: < 10 minutes for acceptable system responsiveness
    """
    # Constants for response index assessment
    EXCELLENT_RESPONSE = 2.0     # minutes - excellent response time
    GOOD_RESPONSE = 5.0          # minutes - good response time
    ACCEPTABLE_RESPONSE = 10.0   # minutes - acceptable response time
    
    anomalies = await classify_anomalies(sensor=sensor, window=window)
    if not anomalies:
        return format_metric_response('response_index', 0.0, expected_value=GOOD_RESPONSE, samples=0)
    
    resp_times = []
    all_readings = storage.fetch_all()
    
    # Group anomalies by sensor for better analysis
    sensor_anomalies = {}
    for a in anomalies:
        sname = a['sensor']
        if sname not in sensor_anomalies:
            sensor_anomalies[sname] = []
        sensor_anomalies[sname].append(a)
    
    # Calculate response times for each anomaly
    for a in anomalies:
        sname = a['sensor']
        t0 = datetime.datetime.fromisoformat(a['timestamp'])
        for r in all_readings:
            if r['sensor'] == sname and datetime.datetime.fromisoformat(r['timestamp']) > t0:
                t1 = datetime.datetime.fromisoformat(r['timestamp'])
                resp_times.append((t1 - t0).total_seconds() / 60.0)
                break
    
    if not resp_times:
        return format_metric_response('response_index', 0.0, expected_value=GOOD_RESPONSE, samples=len(anomalies))
    
    # Calculate response index statistics
    avg_response_time = round(statistics.mean(resp_times), 2)
    min_response_time = round(min(resp_times), 2) if resp_times else 0.0
    max_response_time = round(max(resp_times), 2) if resp_times else 0.0
    response_std = round(statistics.stdev(resp_times), 2) if len(resp_times) > 1 else 0.0
    
    # Determine response status
    if avg_response_time <= EXCELLENT_RESPONSE:
        response_status = 'excellent'
    elif avg_response_time <= GOOD_RESPONSE:
        response_status = 'good'
    elif avg_response_time <= ACCEPTABLE_RESPONSE:
        response_status = 'acceptable'
    else:
        response_status = 'poor'
    
    # Calculate response time distribution
    fast_count = sum(1 for t in resp_times if t <= 2.0)  # ≤ 2 minutes
    good_count = sum(1 for t in resp_times if 2.0 < t <= 5.0)  # 2-5 minutes
    slow_count = sum(1 for t in resp_times if 5.0 < t <= 10.0)  # 5-10 minutes
    very_slow_count = sum(1 for t in resp_times if t > 10.0)  # > 10 minutes
    
    total_responses = len(resp_times)
    fast_percent = round((fast_count / total_responses) * 100, 1) if total_responses > 0 else 0.0
    good_percent = round((good_count / total_responses) * 100, 1) if total_responses > 0 else 0.0
    slow_percent = round((slow_count / total_responses) * 100, 1) if total_responses > 0 else 0.0
    very_slow_percent = round((very_slow_count / total_responses) * 100, 1) if total_responses > 0 else 0.0
    
    # Calculate response variability
    response_variability = round((response_std / avg_response_time) * 100, 1) if avg_response_time > 0 else 0.0
    
    # Calculate time span of analysis
    if anomalies:
        anomaly_times = [datetime.datetime.fromisoformat(a['timestamp']) for a in anomalies]
        time_span_hours = round((max(anomaly_times) - min(anomaly_times)).total_seconds() / 3600.0, 2)
    else:
        time_span_hours = 0.0
    
    # Calculate response rate (responses per hour)
    response_rate = round(total_responses / time_span_hours, 2) if time_span_hours > 0 else 0.0
    
    # Analyze response times by sensor
    sensor_response_times = {}
    for sname, sensor_anomaly_list in sensor_anomalies.items():
        sensor_times = []
        for a in sensor_anomaly_list:
            t0 = datetime.datetime.fromisoformat(a['timestamp'])
            for r in all_readings:
                if r['sensor'] == sname and datetime.datetime.fromisoformat(r['timestamp']) > t0:
                    t1 = datetime.datetime.fromisoformat(r['timestamp'])
                    sensor_times.append((t1 - t0).total_seconds() / 60.0)
                    break
        if sensor_times:
            sensor_response_times[sname] = round(statistics.mean(sensor_times), 2)
    
    # Prepare response with additional metadata
    response = format_metric_response('response_index', avg_response_time, expected_value=GOOD_RESPONSE, samples=len(anomalies))
    
    # Add metadata useful for frontend visualization
    response.update({
        'min_response_time': min_response_time,
        'max_response_time': max_response_time,
        'response_std': response_std,
        'response_variability': response_variability,
        'response_status': response_status,
        'time_span_hours': time_span_hours,
        'response_rate': response_rate,
        'fast_count': fast_count,
        'good_count': good_count,
        'slow_count': slow_count,
        'very_slow_count': very_slow_count,
        'fast_percent': fast_percent,
        'good_percent': good_percent,
        'slow_percent': slow_percent,
        'very_slow_percent': very_slow_percent,
        'excellent_threshold': EXCELLENT_RESPONSE,
        'good_threshold': GOOD_RESPONSE,
        'acceptable_threshold': ACCEPTABLE_RESPONSE,
        'window_size': window
    })
    
    # Add sensor-specific response times
    for sensor_name, avg_time in sensor_response_times.items():
        response[f'response_time_{sensor_name}'] = avg_time
    
    # Add filtered sensor info
    if sensor:
        response['filtered_sensor'] = sensor
    else:
        response['filtered_sensor'] = 'all'
    
    return response

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
        if r["sensor"] == "temperature" and abs(r["value"] - SETPOINT_TEMP_DEFAULT) > TMP_TOLERANCE:
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
    from settings import SETPOINT_TEMP_DEFAULT, MIN_FLOW_THRESHOLD
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
        if r["sensor"] == "temperature" and abs(r["value"] - SETPOINT_TEMP_DEFAULT) > TMP_TOLERANCE:
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

