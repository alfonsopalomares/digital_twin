# -*- coding: utf-8 -*-
"""
Unit tests for simulator
"""
import pytest
from simulator import SensorSimulator
from settings import AVG_FLOW_RATE_DEFAULT, SETPOINT_TEMP_DEFAULT, HEATER_REGIME_DEFAULT

class TestSimulator:
    """Test class for simulator"""
    
    def test_simulator_initialization_defaults(self, storage):
        """Test simulator initialization with defaults"""
        sim = SensorSimulator()
        
        assert sim.avg_flow_rate == AVG_FLOW_RATE_DEFAULT
        assert sim.temp_setpoint == SETPOINT_TEMP_DEFAULT
        assert sim.heater_regime == HEATER_REGIME_DEFAULT
        assert sim.level == 1.0
        assert len(sim.temperatures) == 5  # TANK_SEGMENTS
        assert sim.heater_eff == 0.8  # HEATER_EFFICIENCY
        assert sim.time_elapsed == 0
    
    def test_simulator_initialization_with_config(self, storage, sample_config):
        """Test simulator initialization with config from storage"""
        storage.save_config(**sample_config)
        
        sim = SensorSimulator()
        
        assert sim.avg_flow_rate == sample_config['avg_flow_rate']
        assert sim.temp_setpoint == sample_config['temp_setpoint']
        assert sim.heater_regime == sample_config['heater_regime']
    
    def test_simulator_initialization_with_params(self, storage):
        """Test simulator initialization with explicit parameters"""
        custom_flow_rate = 0.012
        custom_temp = 65.0
        custom_regime = 0.15
        
        sim = SensorSimulator(
            avg_flow_rate=custom_flow_rate,
            temp_setpoint=custom_temp,
            heater_regime=custom_regime
        )
        
        assert sim.avg_flow_rate == custom_flow_rate
        assert sim.temp_setpoint == custom_temp
        assert sim.heater_regime == custom_regime
    
    def test_generate_frame_basic(self, storage):
        """Test basic frame generation"""
        sim = SensorSimulator()
        readings = sim.generate_frame(users=2)
        
        # Should generate 4 readings (flow, temperature, level, power)
        assert len(readings) == 4
        
        # Check all required fields
        for reading in readings:
            assert 'sensor' in reading
            assert 'timestamp' in reading
            assert 'value' in reading
            assert isinstance(reading['value'], (int, float))
        
        # Check sensor types
        sensors = [r['sensor'] for r in readings]
        assert 'flow' in sensors
        assert 'temperature' in sensors
        assert 'level' in sensors
        assert 'power' in sensors
    
    def test_generate_frame_single_sensor(self, storage):
        """Test frame generation for single sensor"""
        sim = SensorSimulator()
        readings = sim.generate_frame(users=1, sensor='flow')
        
        # Should generate only 1 reading
        assert len(readings) == 1
        assert readings[0]['sensor'] == 'flow'
        assert readings[0]['value'] > 0
    
    def test_generate_frame_with_override(self, storage):
        """Test frame generation with value override"""
        sim = SensorSimulator()
        override_value = 0.025
        readings = sim.generate_frame(users=1, sensor='flow', value=override_value)
        
        assert len(readings) == 1
        assert readings[0]['sensor'] == 'flow'
        assert readings[0]['value'] == override_value
    
    def test_generate_frame_flow_scaling(self, storage):
        """Test that flow scales with number of users"""
        sim = SensorSimulator()
        
        # Test with 1 user
        readings_1 = sim.generate_frame(users=1)
        flow_1 = next(r['value'] for r in readings_1 if r['sensor'] == 'flow')
        
        # Test with 3 users
        readings_3 = sim.generate_frame(users=3)
        flow_3 = next(r['value'] for r in readings_3 if r['sensor'] == 'flow')
        
        # Flow should be roughly 3x higher with 3 users
        assert flow_3 > flow_1
    
    def test_generate_frame_temperature_range(self, storage):
        """Test that temperature values are within expected range"""
        sim = SensorSimulator()
        readings = sim.generate_frame(users=1)
        
        temp_reading = next(r for r in readings if r['sensor'] == 'temperature')
        temp_value = temp_reading['value']
        
        # Temperature should be reasonable (between 0 and 100°C)
        assert 0 < temp_value < 100
    
    def test_generate_frame_level_range(self, storage):
        """Test that level values are within expected range"""
        sim = SensorSimulator()
        readings = sim.generate_frame(users=1)
        
        level_reading = next(r for r in readings if r['sensor'] == 'level')
        level_value = level_reading['value']
        
        # Level should be between 0 and 1
        assert 0 <= level_value <= 1
    
    def test_generate_frame_power_range(self, storage):
        """Test that power values are within expected range"""
        sim = SensorSimulator()
        readings = sim.generate_frame(users=1)
        
        power_reading = next(r for r in readings if r['sensor'] == 'power')
        power_value = power_reading['value']
        
        # Power should be positive and reasonable
        assert power_value >= 0
        assert power_value < 100  # Should not be unreasonably high
    
    def test_set_flow_rate(self, storage):
        """Test setting flow rate"""
        sim = SensorSimulator()
        new_rate = 0.015
        
        sim.set_flow_rate(new_rate)
        
        assert sim.avg_flow_rate == new_rate
        
        # Check that config was updated
        config = storage.get_config()
        assert config['avg_flow_rate'] == new_rate
    
    def test_set_temp_setpoint(self, storage):
        """Test setting temperature setpoint"""
        sim = SensorSimulator()
        new_temp = 70.0
        
        sim.set_temp_setpoint(new_temp)
        
        assert sim.temp_setpoint == new_temp
        
        # Check that config was updated
        config = storage.get_config()
        assert config['temp_setpoint'] == new_temp
    
    def test_set_heater_regime(self, storage):
        """Test setting heater regime"""
        sim = SensorSimulator()
        new_regime = 0.2
        
        sim.set_heater_regime(new_regime)
        
        assert sim.heater_regime == new_regime
        
        # Check that config was updated
        config = storage.get_config()
        assert config['heater_regime'] == new_regime
    
    def test_simulate_scenarios(self, storage):
        """Test scenario simulation"""
        sim = SensorSimulator()
        
        configs = [
            {'users': 1, 'flow_rate': 0.008},
            {'users': 2, 'flow_rate': 0.012}
        ]
        
        results = sim.simulate_scenarios(configs, duration_hours=1)
        
        assert len(results) == 2
        
        # Check first scenario
        scenario1 = results[0]
        assert 'config' in scenario1
        assert 'total_energy_kWh' in scenario1
        assert 'avg_temperature' in scenario1
        assert scenario1['config']['users'] == 1
        
        # Check second scenario
        scenario2 = results[1]
        assert scenario2['config']['users'] == 2
    
    def test_sensors_count_property(self, storage):
        """Test sensors_count property"""
        sim = SensorSimulator()
        assert sim.sensors_count == 4 