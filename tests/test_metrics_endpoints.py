# -*- coding: utf-8 -*-
"""
Unit tests for metrics endpoints
"""
import pytest
from metrics_endpoints import (
    get_availability, get_performance, get_quality, get_energy_efficiency,
    get_thermal_variation, get_peak_flow_ratio
)
from settings import AVG_FLOW_RATE_DEFAULT, SETPOINT_TEMP_DEFAULT

class TestMetricsEndpoints:
    """Test class for metrics endpoints"""
    
    def test_get_availability_empty(self, storage):
        """Test get_availability with empty database"""
        result = get_availability()
        assert result['title'] == 'Availability'
        assert result['unit'] == '%'
        assert result['value'] == 0.0
        assert result['samples'] == 0
    
    def test_get_availability_with_data(self, storage, sample_readings):
        """Test get_availability with sample data"""
        storage.save_batch(sample_readings)
        
        result = get_availability()
        
        assert result['title'] == 'Availability'
        assert result['unit'] == '%'
        assert result['value'] > 0
        assert result['samples'] == 2  # 2 flow readings in sample data
    
    def test_get_performance_empty(self, storage):
        """Test get_performance with empty database"""
        result = get_performance()
        
        assert result['title'] == 'Performance'
        assert result['unit'] == 'ratio'
        assert result['value'] == 0.0
        assert result['expected_value'] == 0.48  # 0.008 * 60 * 1 * 1
        assert result['samples'] == 0
        assert result['users'] == 1
        assert result['hours'] == 1
    
    def test_get_performance_with_data(self, storage, sample_readings):
        """Test get_performance with sample data"""
        storage.save_batch(sample_readings)
        
        result = get_performance()
        
        assert result['title'] == 'Performance'
        assert result['unit'] == 'ratio'
        assert isinstance(result['value'], float)
        assert result['expected_value'] == 0.48
        assert result['samples'] == 2
        assert result['users'] == 1
        assert result['hours'] == 1
    
    def test_get_performance_with_custom_params(self, storage, sample_readings):
        """Test get_performance with custom users and hours"""
        storage.save_batch(sample_readings)
        
        result = get_performance(users=2, hours=2)
        
        assert result['users'] == 2
        assert result['hours'] == 2
        assert result['expected_value'] == 1.92  # 0.008 * 60 * 2 * 2
    
    def test_get_quality_empty(self, storage):
        """Test get_quality with empty database"""
        result = get_quality()
        
        assert result['title'] == 'Quality'
        assert result['unit'] == '%'
        assert result['value'] == 0.0
        assert result['samples'] == 0
    
    def test_get_quality_with_data(self, storage, sample_readings):
        """Test get_quality with sample data"""
        storage.save_batch(sample_readings)
        
        result = get_quality()
        
        assert result['title'] == 'Quality'
        assert result['unit'] == '%'
        assert isinstance(result['value'], float)
        assert 0 <= result['value'] <= 100
        assert result['samples'] == 2  # 2 temperature readings
    
    def test_get_energy_efficiency_empty(self, storage):
        """Test get_energy_efficiency with empty database"""
        result = get_energy_efficiency()
        
        assert result['title'] == 'Energy Efficiency'
        assert result['unit'] == 'kWh/L'
        assert result['value'] == 0.0
        assert result['samples'] == 0
    
    def test_get_energy_efficiency_with_data(self, storage, sample_readings):
        """Test get_energy_efficiency with sample data"""
        storage.save_batch(sample_readings)
        
        result = get_energy_efficiency()
        
        assert result['title'] == 'Energy Efficiency'
        assert result['unit'] == 'kWh/L'
        assert isinstance(result['value'], float)
        assert result['samples'] == 2  # 2 power readings
    
    def test_get_thermal_variation_empty(self, storage):
        """Test get_thermal_variation with empty database"""
        result = get_thermal_variation()
        
        assert result['title'] == 'Thermal Variation'
        assert result['unit'] == '°C'
        assert result['value'] == 0.0
        assert result['samples'] == 0
    
    def test_get_thermal_variation_with_data(self, storage, sample_readings):
        """Test get_thermal_variation with sample data"""
        storage.save_batch(sample_readings)
        
        result = get_thermal_variation()
        
        assert result['title'] == 'Thermal Variation'
        assert result['unit'] == '°C'
        assert isinstance(result['value'], float)
        assert result['value'] >= 0
        assert result['samples'] == 2  # 2 temperature readings
    
    def test_get_peak_flow_ratio_empty(self, storage):
        """Test get_peak_flow_ratio with empty database"""
        result = get_peak_flow_ratio(users=1)
        
        assert result['title'] == 'Peak Flow Ratio'
        assert result['unit'] == ''
        assert result['value'] == 0.0
        assert result['expected_value'] == 0.0
        assert result['samples'] == 0
        assert result['users'] == 1
    
    def test_get_peak_flow_ratio_with_data(self, storage, sample_readings):
        """Test get_peak_flow_ratio with sample data"""
        storage.save_batch(sample_readings)
        
        result = get_peak_flow_ratio(users=1)
        
        assert result['title'] == 'Peak Flow Ratio'
        assert result['unit'] == ''
        assert isinstance(result['value'], float)
        assert result['value'] > 0
        assert result['expected_value'] == 1.0
        assert result['samples'] == 2
        assert result['users'] == 1
    
    def test_get_peak_flow_ratio_different_users(self, storage, sample_readings):
        """Test get_peak_flow_ratio with different user counts"""
        storage.save_batch(sample_readings)
        
        result_1 = get_peak_flow_ratio(users=1)
        result_2 = get_peak_flow_ratio(users=2)
        
        # With more users, the ratio should be different
        assert result_1['users'] == 1
        assert result_2['users'] == 2
        assert result_1['value'] != result_2['value']
    
    def test_metrics_with_time_filters(self, storage, sample_readings):
        """Test metrics with time filters"""
        storage.save_batch(sample_readings)
        
        # Test with start time filter
        start_time = "2025-01-01T09:59:00"
        result = get_availability(start=start_time)
        
        assert result['samples'] > 0
        
        # Test with end time filter
        end_time = "2025-01-01T10:02:00"
        result = get_availability(end=end_time)
        
        assert result['samples'] > 0 