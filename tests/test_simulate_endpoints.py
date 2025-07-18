# -*- coding: utf-8 -*-
"""
Unit tests for simulate endpoints
"""
import pytest
import asyncio
from simulate_endpoints import simulate_scenarios, ScenarioConfig
from simulator import SensorSimulator
from settings import AVG_FLOW_RATE_DEFAULT, SETPOINT_TEMP_DEFAULT, HEATER_REGIME_DEFAULT

class TestSimulateEndpoints:
    """Test class for simulate endpoints"""
    
    def test_simulate_scenarios_basic(self, storage):
        """Test simulate_scenarios with basic configuration"""
        # Create test scenarios
        configs = [
            ScenarioConfig(users=1, flow_rate=0.008),
            ScenarioConfig(users=2, flow_rate=0.012)
        ]
        
        # Run simulation
        async def run_test():
            return await simulate_scenarios(configs, duration_hours=1)
        
        results = asyncio.run(run_test())
        
        # Verify results
        assert len(results) == 2
        
        # Check first scenario
        scenario1 = results[0]
        assert 'config' in scenario1
        assert 'total_energy_kWh' in scenario1
        assert 'avg_temperature' in scenario1
        assert scenario1['config']['users'] == 1
        assert scenario1['config']['flow_rate'] == 0.008
        assert isinstance(scenario1['total_energy_kWh'], float)
        assert isinstance(scenario1['avg_temperature'], float)
        
        # Check second scenario
        scenario2 = results[1]
        assert scenario2['config']['users'] == 2
        assert scenario2['config']['flow_rate'] == 0.012
    
    def test_simulate_scenarios_with_all_params(self, storage):
        """Test simulate_scenarios with all parameters specified"""
        configs = [
            ScenarioConfig(
                users=1,
                flow_rate=0.008,
                temp_setpoint=65.0,
                heater_regime=0.2
            ),
            ScenarioConfig(
                users=3,
                flow_rate=0.016,
                temp_setpoint=55.0,
                heater_regime=0.05
            )
        ]
        
        async def run_test():
            return await simulate_scenarios(configs, duration_hours=1)
        
        results = asyncio.run(run_test())
        
        # Verify results
        assert len(results) == 2
        
        # Check first scenario
        scenario1 = results[0]
        assert scenario1['config']['temp_setpoint'] == 65.0
        assert scenario1['config']['heater_regime'] == 0.2
        
        # Check second scenario
        scenario2 = results[1]
        assert scenario2['config']['temp_setpoint'] == 55.0
        assert scenario2['config']['heater_regime'] == 0.05
    
    def test_simulate_scenarios_different_durations(self, storage):
        """Test simulate_scenarios with different durations"""
        configs = [ScenarioConfig(users=1, flow_rate=0.008)]
        
        # Test 1 hour
        async def run_1h():
            return await simulate_scenarios(configs, duration_hours=1)
        
        results_1h = asyncio.run(run_1h())
        energy_1h = results_1h[0]['total_energy_kWh']
        
        # Test 2 hours
        async def run_2h():
            return await simulate_scenarios(configs, duration_hours=2)
        
        results_2h = asyncio.run(run_2h())
        energy_2h = results_2h[0]['total_energy_kWh']
        
        # Energy should be roughly double for 2 hours
        assert energy_2h > energy_1h
    
    def test_simulate_scenarios_empty_config(self, storage):
        """Test simulate_scenarios with empty configuration list"""
        configs = []
        
        async def run_test():
            return await simulate_scenarios(configs, duration_hours=1)
        
        results = asyncio.run(run_test())
        assert results == []
    
    def test_simulate_scenarios_single_config(self, storage):
        """Test simulate_scenarios with single configuration"""
        configs = [ScenarioConfig(users=1, flow_rate=0.008)]
        
        async def run_test():
            return await simulate_scenarios(configs, duration_hours=1)
        
        results = asyncio.run(run_test())
        
        assert len(results) == 1
        assert results[0]['config']['users'] == 1
        assert results[0]['config']['flow_rate'] == 0.008
    
    def test_simulate_scenarios_energy_values(self, storage):
        """Test that energy values are reasonable"""
        configs = [ScenarioConfig(users=1, flow_rate=0.008)]
        
        async def run_test():
            return await simulate_scenarios(configs, duration_hours=1)
        
        results = asyncio.run(run_test())
        
        energy = results[0]['total_energy_kWh']
        
        # Energy should be positive and reasonable
        assert energy > 0
        assert energy < 100  # Should not be unreasonably high
    
    def test_simulate_scenarios_temperature_values(self, storage):
        """Test that temperature values are reasonable"""
        configs = [ScenarioConfig(users=1, flow_rate=0.008)]
        
        async def run_test():
            return await simulate_scenarios(configs, duration_hours=1)
        
        results = asyncio.run(run_test())
        
        temp = results[0]['avg_temperature']
        
        # Temperature should be reasonable (between 0 and 100°C)
        assert temp > 0
        assert temp < 100 