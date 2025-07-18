# -*- coding: utf-8 -*-
"""
Pytest configuration and fixtures for backend tests
"""
import pytest
import tempfile
import os
from storage import LocalStorage
from settings import AVG_FLOW_RATE_DEFAULT, SETPOINT_TEMP_DEFAULT, HEATER_REGIME_DEFAULT

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    # Create a temporary database file
    temp_db_path = tempfile.mktemp(suffix='.db')
    
    # Store original database path
    original_db_path = getattr(LocalStorage, '_db_path', 'sensor_data.db')
    
    # Set temporary database path
    LocalStorage._db_path = temp_db_path
    
    yield temp_db_path
    
    # Cleanup: remove temporary database
    try:
        os.remove(temp_db_path)
    except FileNotFoundError:
        pass
    
    # Restore original database path
    LocalStorage._db_path = original_db_path

@pytest.fixture
def storage(temp_db):
    """Create a storage instance with temporary database"""
    storage = LocalStorage()
    storage.clear_all()
    return storage

@pytest.fixture
def sample_config():
    """Sample configuration for testing"""
    return {
        'user_quantity': 2,
        'hours': 1,
        'avg_flow_rate': AVG_FLOW_RATE_DEFAULT,
        'temp_setpoint': SETPOINT_TEMP_DEFAULT,
        'heater_regime': HEATER_REGIME_DEFAULT
    }

@pytest.fixture
def sample_readings():
    """Sample sensor readings for testing"""
    return [
        {'sensor': 'flow', 'timestamp': '2025-01-01T10:00:00', 'value': 0.008},
        {'sensor': 'temperature', 'timestamp': '2025-01-01T10:00:00', 'value': 60.0},
        {'sensor': 'level', 'timestamp': '2025-01-01T10:00:00', 'value': 0.8},
        {'sensor': 'power', 'timestamp': '2025-01-01T10:00:00', 'value': 5.0},
        {'sensor': 'flow', 'timestamp': '2025-01-01T10:01:00', 'value': 0.012},
        {'sensor': 'temperature', 'timestamp': '2025-01-01T10:01:00', 'value': 61.0},
        {'sensor': 'level', 'timestamp': '2025-01-01T10:01:00', 'value': 0.7},
        {'sensor': 'power', 'timestamp': '2025-01-01T10:01:00', 'value': 6.0},
    ] 