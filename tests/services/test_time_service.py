# tests/services/test_time_service.py
import sys
sys.path.append('.')
import pytest
import asyncio
from datetime import datetime
from application.services.time_service import TimeService
from domain.utils.result import Result

class TestTimeService:
    """Test suite for Time Service"""
    
    @pytest.fixture
    def time_service(self):
        """Create TimeService instance for testing"""
        return TimeService()
    
    @pytest.mark.asyncio
    async def test_get_current_time_success(self, time_service):
        """Test successful time retrieval"""
        result = await time_service.get_current_time("New York")
        
        assert result.is_success
        assert isinstance(result.value, str)
        assert len(result.value) > 0
    
    @pytest.mark.asyncio
    async def test_get_current_time_invalid_city(self, time_service):
        """Test time retrieval for unsupported city"""
        result = await time_service.get_current_time("InvalidCity")
        
        assert result.is_error
        assert "not available" in result.error
        assert "Supported cities" in result.error
    
    @pytest.mark.asyncio
    async def test_get_current_time_empty_city(self, time_service):
        """Test time retrieval with empty city name"""
        result = await time_service.get_current_time("")
        
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_get_timezone_info(self, time_service):
        """Test timezone information retrieval"""
        result = await time_service.get_timezone_info("London")
        
        assert result.is_success
        tz_info = result.value
        assert "timezone" in tz_info
        assert "utc_offset" in tz_info
        assert "dst" in tz_info
        assert "country" in tz_info
        assert tz_info["timezone"] == "Europe/London"
    
    @pytest.mark.asyncio
    async def test_get_world_clock(self, time_service):
        """Test world clock functionality"""
        result = await time_service.get_world_clock()
        
        assert result.is_success
        world_times = result.value
        assert isinstance(world_times, list)
        assert len(world_times) > 0
        
        # Check structure of each entry
        for city_time in world_times:
            assert "city" in city_time
            assert "time" in city_time
            assert "timezone" in city_time
            assert "utc_offset" in city_time
            assert "country" in city_time
    
    @pytest.mark.asyncio
    async def test_convert_time(self, time_service):
        """Test time conversion between cities"""
        result = await time_service.convert_time("14:30", "New York", "London")
        
        assert result.is_success
        assert isinstance(result.value, str)
        assert ":" in result.value  # Should contain time format
    
    @pytest.mark.asyncio
    async def test_convert_time_invalid_cities(self, time_service):
        """Test time conversion with invalid cities"""
        result = await time_service.convert_time("14:30", "InvalidCity1", "InvalidCity2")
        
        assert result.is_error
        assert "not supported" in result.error
    
    @pytest.mark.asyncio
    async def test_convert_time_invalid_format(self, time_service):
        """Test time conversion with invalid time format"""
        result = await time_service.convert_time("invalid_time", "New York", "London")
        
        assert result.is_error
        assert "Invalid time format" in result.error
    
    @pytest.mark.asyncio
    async def test_get_time_difference(self, time_service):
        """Test time difference calculation"""
        result = await time_service.get_time_difference("New York", "London")
        
        assert result.is_success
        diff_info = result.value
        assert "city1" in diff_info
        assert "city2" in diff_info
        assert "offset1" in diff_info
        assert "offset2" in diff_info
        assert "timezone1" in diff_info
        assert "timezone2" in diff_info
    
    @pytest.mark.asyncio
    async def test_get_time_difference_invalid_cities(self, time_service):
        """Test time difference with invalid cities"""
        result = await time_service.get_time_difference("InvalidCity1", "InvalidCity2")
        
        assert result.is_error
        assert "not supported" in result.error
    
    @pytest.mark.asyncio
    async def test_get_supported_cities(self, time_service):
        """Test getting list of supported cities"""
        result = await time_service.get_supported_cities()
        
        assert result.is_success
        cities = result.value
        assert isinstance(cities, list)
        assert len(cities) > 0
        assert "new york" in cities
        assert "london" in cities
        assert "tokyo" in cities
    
    @pytest.mark.asyncio
    async def test_is_city_supported(self, time_service):
        """Test city support checking"""
        # Test supported city
        result = await time_service.is_city_supported("Paris")
        assert result.is_success
        assert result.value is True
        
        # Test unsupported city
        result = await time_service.is_city_supported("InvalidCity")
        assert result.is_success
        assert result.value is False
    
    @pytest.mark.asyncio
    async def test_timezone_data_consistency(self, time_service):
        """Test that timezone data is consistent across methods"""
        city = "Tokyo"
        
        # Get timezone info
        tz_info_result = await time_service.get_timezone_info(city)
        assert tz_info_result.is_success
        
        # Get time difference (should use same data)
        diff_result = await time_service.get_time_difference(city, "London")
        assert diff_result.is_success
        
        # Check consistency
        tz_info = tz_info_result.value
        diff_info = diff_result.value
        
        assert tz_info["timezone"] == diff_info["timezone1"]
        assert tz_info["utc_offset"] == diff_info["offset1"]
    
    @pytest.mark.asyncio
    async def test_time_service_case_insensitive(self, time_service):
        """Test that time service is case insensitive"""
        cities = ["NEW YORK", "london", "ToKyO", "pArIs"]
        
        for city in cities:
            result = await time_service.get_current_time(city)
            assert result.is_success, f"Failed for city: {city}"
    
    @pytest.mark.asyncio
    async def test_time_service_whitespace_handling(self, time_service):
        """Test that time service handles whitespace correctly"""
        cities = ["  New York  ", "\tLondon\t", "\nTokyo\n"]
        
        for city in cities:
            result = await time_service.get_current_time(city)
            assert result.is_success, f"Failed for city with whitespace: '{city}'"
    
    @pytest.mark.asyncio
    async def test_time_service_error_handling(self, time_service):
        """Test error handling in time service"""
        # Test with None input
        result = await time_service.get_current_time(None)
        assert result.is_error
        
        # Test with very long city name
        long_city = "A" * 200
        result = await time_service.get_current_time(long_city)
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_time_service_performance(self, time_service):
        """Test time service performance with multiple requests"""
        import time
        
        cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Moscow"]
        start_time = time.time()
        
        # Make multiple requests
        tasks = [time_service.get_current_time(city) for city in cities]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # Should complete quickly (less than 1 second for 6 requests)
        assert duration < 1.0, f"Performance test failed: {duration:.2f}s for 6 requests"
    
    @pytest.mark.asyncio
    async def test_time_service_concurrent_access(self, time_service):
        """Test concurrent access to time service"""
        # Test concurrent access to same city
        tasks = [time_service.get_current_time("London") for _ in range(5)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        # Times might be slightly different due to execution time
        assert all(len(result.value) > 0 for result in results)
    
    @pytest.mark.asyncio
    async def test_time_service_data_completeness(self, time_service):
        """Test that all cities have complete timezone data"""
        cities_result = await time_service.get_supported_cities()
        assert cities_result.is_success
        
        cities = cities_result.value
        
        for city in cities:
            # Test current time
            time_result = await time_service.get_current_time(city)
            assert time_result.is_success
            
            # Test timezone info
            tz_info_result = await time_service.get_timezone_info(city)
            assert tz_info_result.is_success
            
            # Test time difference with another city
            other_city = cities[0] if city != cities[0] else cities[1]
            diff_result = await time_service.get_time_difference(city, other_city)
            assert diff_result.is_success
    
    @pytest.mark.asyncio
    async def test_time_service_timezone_accuracy(self, time_service):
        """Test timezone accuracy"""
        # Test that timezone info contains valid data
        result = await time_service.get_timezone_info("New York")
        assert result.is_success
        
        tz_info = result.value
        assert tz_info["timezone"] == "America/New_York"
        assert tz_info["utc_offset"] == "-5:00"
        assert tz_info["dst"] is True
        assert tz_info["country"] == "USA"
    
    @pytest.mark.asyncio
    async def test_time_service_world_clock_completeness(self, time_service):
        """Test that world clock includes all supported cities"""
        cities_result = await time_service.get_supported_cities()
        assert cities_result.is_success
        
        world_clock_result = await time_service.get_world_clock()
        assert world_clock_result.is_success
        
        supported_cities = cities_result.value
        world_clock_cities = [entry["city"].lower() for entry in world_clock_result.value]
        
        # All supported cities should be in world clock
        for city in supported_cities:
            assert city in world_clock_cities, f"City {city} not found in world clock"
