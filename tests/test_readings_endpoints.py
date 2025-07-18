# -*- coding: utf-8 -*-
"""
Unit tests for readings endpoints
"""
import pytest
from readings_endpoints import get_readings, get_latest_reading, delete_readings
from fastapi import HTTPException

class TestReadingsEndpoints:
    """Test class for readings endpoints"""
    
    def test_get_readings_empty(self, storage):
        """Test get_readings with empty database"""
        result = get_readings()
        assert result == []
    
    def test_get_readings_with_data(self, storage, sample_readings):
        """Test get_readings with sample data"""
        # Save sample readings
        storage.save_batch(sample_readings)
        
        # Get readings
        result = get_readings()
        
        # Verify results
        assert len(result) == len(sample_readings)
        assert all('sensor' in reading for reading in result)
        assert all('timestamp' in reading for reading in result)
        assert all('value' in reading for reading in result)
        
        # Verify specific values
        flow_readings = [r for r in result if r['sensor'] == 'flow']
        assert len(flow_readings) == 2
        flow_values = [r['value'] for r in flow_readings]
        assert 0.008 in flow_values
        assert 0.012 in flow_values
    
    def test_get_latest_reading_empty(self, storage):
        """Test get_latest_reading with empty database"""
        with pytest.raises(HTTPException) as exc_info:
            get_latest_reading()
        assert exc_info.value.status_code == 404
        assert "No readings found" in str(exc_info.value.detail)
    
    def test_get_latest_reading_with_data(self, storage, sample_readings):
        """Test get_latest_reading with sample data"""
        # Save sample readings
        storage.save_batch(sample_readings)
        
        # Get latest reading
        result = get_latest_reading()
        
        # Verify result
        assert 'sensor' in result
        assert 'timestamp' in result
        assert 'value' in result
        
        # Should be one of the readings in the sample data
        assert result['sensor'] in ['flow', 'temperature', 'level', 'power']
        assert result['timestamp'] in ['2025-01-01T10:00:00', '2025-01-01T10:01:00']
        assert result['value'] in [0.008, 0.012, 60.0, 61.0, 0.8, 0.7, 5.0, 6.0]
    
    def test_delete_readings(self, storage, sample_readings):
        """Test delete_readings functionality"""
        # Save sample readings
        storage.save_batch(sample_readings)
        
        # Verify data exists
        assert len(storage.fetch_all()) == len(sample_readings)
        
        # Delete readings
        result = delete_readings()
        
        # Verify response
        assert result == {"status": "deleted"}
        
        # Verify data is deleted
        assert len(storage.fetch_all()) == 0
    
    def test_get_readings_after_delete(self, storage, sample_readings):
        """Test get_readings after deleting data"""
        # Save and delete data
        storage.save_batch(sample_readings)
        delete_readings()
        
        # Get readings should return empty list
        result = get_readings()
        assert result == []
    
    def test_get_latest_reading_after_delete(self, storage, sample_readings):
        """Test get_latest_reading after deleting data"""
        # Save and delete data
        storage.save_batch(sample_readings)
        delete_readings()
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            get_latest_reading()
        assert exc_info.value.status_code == 404 