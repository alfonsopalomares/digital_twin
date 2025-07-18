# -*- coding: utf-8 -*-
"""
Unit tests for storage
"""
import pytest
from storage import LocalStorage
from settings import AVG_FLOW_RATE_DEFAULT, SETPOINT_TEMP_DEFAULT, HEATER_REGIME_DEFAULT

class TestStorage:
    """Test class for storage"""
    
    def test_storage_initialization(self, storage):
        """Test storage initialization"""
        assert storage is not None
        assert hasattr(storage, 'fetch_all')
        assert hasattr(storage, 'save_batch')
        assert hasattr(storage, 'get_config')
        assert hasattr(storage, 'save_config')
        assert hasattr(storage, 'clear_all')
    
    def test_save_and_get_config(self, storage):
        """Test saving and retrieving configuration"""
        config = {
            'user_quantity': 3,
            'hours': 2,
            'avg_flow_rate': 0.012,
            'temp_setpoint': 65.0,
            'heater_regime': 0.15
        }
        
        storage.save_config(**config)
        retrieved_config = storage.get_config()
        
        assert retrieved_config is not None
        assert retrieved_config['user_quantity'] == config['user_quantity']
        assert retrieved_config['hours'] == config['hours']
        assert retrieved_config['avg_flow_rate'] == config['avg_flow_rate']
        assert retrieved_config['temp_setpoint'] == config['temp_setpoint']
        assert retrieved_config['heater_regime'] == config['heater_regime']
    
    def test_get_config_empty(self, storage):
        """Test getting config when none exists"""
        storage.clear_all()
        config = storage.get_config()
        
        assert config is None
    
    def test_save_batch_and_fetch_all(self, storage, sample_readings):
        """Test saving and retrieving readings"""
        # Save readings
        storage.save_batch(sample_readings)
        
        # Fetch all readings
        retrieved_readings = storage.fetch_all()
        
        # Verify results
        assert len(retrieved_readings) == len(sample_readings)
        
        # Check that all readings have required fields
        for reading in retrieved_readings:
            assert 'sensor' in reading
            assert 'timestamp' in reading
            assert 'value' in reading
        
        # Check specific values
        flow_readings = [r for r in retrieved_readings if r['sensor'] == 'flow']
        assert len(flow_readings) == 2
        flow_values = [r['value'] for r in flow_readings]
        assert 0.008 in flow_values
        assert 0.012 in flow_values
    
    def test_fetch_all_empty(self, storage):
        """Test fetching all readings when database is empty"""
        storage.clear_all()
        readings = storage.fetch_all()
        
        assert readings == []
    
    def test_save_batch_multiple_times(self, storage):
        """Test saving multiple batches"""
        batch1 = [
            {'sensor': 'flow', 'timestamp': '2025-01-01T10:00:00', 'value': 0.008},
            {'sensor': 'temperature', 'timestamp': '2025-01-01T10:00:00', 'value': 60.0}
        ]
        
        batch2 = [
            {'sensor': 'flow', 'timestamp': '2025-01-01T10:01:00', 'value': 0.012},
            {'sensor': 'temperature', 'timestamp': '2025-01-01T10:01:00', 'value': 61.0}
        ]
        
        storage.save_batch(batch1)
        storage.save_batch(batch2)
        
        all_readings = storage.fetch_all()
        
        assert len(all_readings) == 4
        
        # Check that all readings are present
        flow_values = [r['value'] for r in all_readings if r['sensor'] == 'flow']
        assert 0.008 in flow_values
        assert 0.012 in flow_values
    
    def test_clear_all(self, storage, sample_readings):
        """Test clearing all data"""
        # Save some data
        storage.save_batch(sample_readings)
        storage.save_config(user_quantity=2, hours=1, avg_flow_rate=0.008, 
                           temp_setpoint=60.0, heater_regime=0.1)
        
        # Verify data exists
        assert len(storage.fetch_all()) > 0
        assert storage.get_config() is not None
        
        # Clear all
        storage.clear_all()
        
        # Verify data is cleared
        assert len(storage.fetch_all()) == 0
        assert storage.get_config() is None
    
    def test_fetch_latest(self, storage, sample_readings):
        """Test fetching latest reading"""
        storage.save_batch(sample_readings)
        
        latest = storage.fetch_latest()
        
        assert latest is not None
        assert 'sensor' in latest
        assert 'timestamp' in latest
        assert 'value' in latest
        
        # Should be one of the readings in the sample data
        assert latest['sensor'] in ['flow', 'temperature', 'level', 'power']
        assert latest['timestamp'] in ['2025-01-01T10:00:00', '2025-01-01T10:01:00']
        assert latest['value'] in [0.008, 0.012, 60.0, 61.0, 0.8, 0.7, 5.0, 6.0]
    
    def test_fetch_latest_empty(self, storage):
        """Test fetching latest reading when database is empty"""
        storage.clear_all()
        latest = storage.fetch_latest()
        
        assert latest is None
    
    def test_config_persistence(self, storage):
        """Test that configuration persists across storage instances"""
        config = {
            'user_quantity': 5,
            'hours': 3,
            'avg_flow_rate': 0.016,
            'temp_setpoint': 70.0,
            'heater_regime': 0.2
        }
        
        storage.save_config(**config)
        
        # Create new storage instance
        new_storage = LocalStorage()
        retrieved_config = new_storage.get_config()
        
        assert retrieved_config is not None
        assert retrieved_config['user_quantity'] == config['user_quantity']
        assert retrieved_config['hours'] == config['hours']
        assert retrieved_config['avg_flow_rate'] == config['avg_flow_rate']
        assert retrieved_config['temp_setpoint'] == config['temp_setpoint']
        assert retrieved_config['heater_regime'] == config['heater_regime']
    
    def test_readings_persistence(self, storage, sample_readings):
        """Test that readings persist across storage instances"""
        storage.save_batch(sample_readings)
        
        # Create new storage instance
        new_storage = LocalStorage()
        retrieved_readings = new_storage.fetch_all()
        
        assert len(retrieved_readings) == len(sample_readings)
        
        # Check that all readings are present (order may vary)
        original_sensors = [r['sensor'] for r in sample_readings]
        retrieved_sensors = [r['sensor'] for r in retrieved_readings]
        assert sorted(original_sensors) == sorted(retrieved_sensors)
        
        original_values = [r['value'] for r in sample_readings]
        retrieved_values = [r['value'] for r in retrieved_readings]
        assert sorted(original_values) == sorted(retrieved_values)
    
    def test_save_config_partial_update(self, storage):
        """Test updating only part of the configuration"""
        # Save initial config
        initial_config = {
            'user_quantity': 1,
            'hours': 1,
            'avg_flow_rate': 0.008,
            'temp_setpoint': 60.0,
            'heater_regime': 0.1
        }
        storage.save_config(**initial_config)
        
        # Update only some fields
        storage.save_config(user_quantity=3, hours=2, avg_flow_rate=initial_config['avg_flow_rate'], 
                           temp_setpoint=initial_config['temp_setpoint'], heater_regime=initial_config['heater_regime'])
        
        # Get updated config
        updated_config = storage.get_config()
        
        # Check that updated fields changed
        assert updated_config['user_quantity'] == 3
        assert updated_config['hours'] == 2
        
        # Check that other fields remained the same
        assert updated_config['avg_flow_rate'] == initial_config['avg_flow_rate']
        assert updated_config['temp_setpoint'] == initial_config['temp_setpoint']
        assert updated_config['heater_regime'] == initial_config['heater_regime'] 