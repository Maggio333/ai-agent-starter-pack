# tests/services/test_weather_service.py
import sys
sys.path.append('.')
import pytest
import asyncio
from application.services.weather_service import WeatherService
from domain.utils.result import Result

class TestWeatherService:
    """Test suite for Weather Service"""
    
    @pytest.fixture
    def weather_service(self):
        """Create WeatherService instance for testing"""
        return WeatherService()
    
    @pytest.mark.asyncio
    async def test_get_weather_success(self, weather_service):
        """Test successful weather retrieval"""
        result = await weather_service.get_weather("New York")
        
        assert result.is_success
        assert "sunny" in result.value.lower()
        assert "25°C" in result.value
    
    @pytest.mark.asyncio
    async def test_get_weather_invalid_city(self, weather_service):
        """Test weather retrieval for unsupported city"""
        result = await weather_service.get_weather("InvalidCity")
        
        assert result.is_error
        assert "not available" in result.error
        assert "Supported cities" in result.error
    
    @pytest.mark.asyncio
    async def test_get_weather_empty_city(self, weather_service):
        """Test weather retrieval with empty city name"""
        result = await weather_service.get_weather("")
        
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_get_weather_forecast(self, weather_service):
        """Test weather forecast retrieval"""
        result = await weather_service.get_weather_forecast("London", 2)
        
        assert result.is_success
        assert len(result.value) == 2
        assert all("day" in forecast for forecast in result.value)
        assert all("condition" in forecast for forecast in result.value)
    
    @pytest.mark.asyncio
    async def test_get_weather_alerts(self, weather_service):
        """Test weather alerts retrieval"""
        result = await weather_service.get_weather_alerts("London")
        
        assert result.is_success
        assert isinstance(result.value, list)
        # London has fog warning in test data
        assert len(result.value) > 0
    
    @pytest.mark.asyncio
    async def test_get_weather_summary(self, weather_service):
        """Test comprehensive weather summary"""
        result = await weather_service.get_weather_summary("Tokyo")
        
        assert result.is_success
        summary = result.value
        assert "city" in summary
        assert "current_weather" in summary
        assert "forecast" in summary
        assert "alerts" in summary
        assert "has_alerts" in summary
        assert summary["city"] == "Tokyo"
    
    @pytest.mark.asyncio
    async def test_get_supported_cities(self, weather_service):
        """Test getting list of supported cities"""
        result = await weather_service.get_supported_cities()
        
        assert result.is_success
        cities = result.value
        assert isinstance(cities, list)
        assert len(cities) > 0
        assert "new york" in cities
        assert "london" in cities
        assert "tokyo" in cities
    
    @pytest.mark.asyncio
    async def test_is_city_supported(self, weather_service):
        """Test city support checking"""
        # Test supported city
        result = await weather_service.is_city_supported("Paris")
        assert result.is_success
        assert result.value is True
        
        # Test unsupported city
        result = await weather_service.is_city_supported("InvalidCity")
        assert result.is_success
        assert result.value is False
    
    @pytest.mark.asyncio
    async def test_weather_data_consistency(self, weather_service):
        """Test that weather data is consistent across methods"""
        city = "Sydney"
        
        # Get weather
        weather_result = await weather_service.get_weather(city)
        assert weather_result.is_success
        
        # Get summary
        summary_result = await weather_service.get_weather_summary(city)
        assert summary_result.is_success
        
        # Check consistency
        summary = summary_result.value
        assert summary["current_weather"] == weather_result.value
    
    @pytest.mark.asyncio
    async def test_weather_forecast_structure(self, weather_service):
        """Test weather forecast data structure"""
        result = await weather_service.get_weather_forecast("Moscow", 3)
        
        assert result.is_success
        forecast = result.value
        
        for day_forecast in forecast:
            assert "day" in day_forecast
            assert "condition" in day_forecast
            assert "temp" in day_forecast
            assert "humidity" in day_forecast
    
    @pytest.mark.asyncio
    async def test_weather_alerts_structure(self, weather_service):
        """Test weather alerts data structure"""
        # Test city with alerts
        result = await weather_service.get_weather_alerts("Moscow")
        assert result.is_success
        alerts = result.value
        assert isinstance(alerts, list)
        
        # Test city without alerts
        result = await weather_service.get_weather_alerts("Sydney")
        assert result.is_success
        alerts = result.value
        assert isinstance(alerts, list)
    
    @pytest.mark.asyncio
    async def test_weather_service_error_handling(self, weather_service):
        """Test error handling in weather service"""
        # Test with None input
        result = await weather_service.get_weather(None)
        assert result.is_error
        
        # Test with very long city name
        long_city = "A" * 200
        result = await weather_service.get_weather(long_city)
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_weather_service_case_insensitive(self, weather_service):
        """Test that weather service is case insensitive"""
        cities = ["NEW YORK", "london", "ToKyO", "pArIs"]
        
        for city in cities:
            result = await weather_service.get_weather(city)
            assert result.is_success, f"Failed for city: {city}"
    
    @pytest.mark.asyncio
    async def test_weather_service_whitespace_handling(self, weather_service):
        """Test that weather service handles whitespace correctly"""
        cities = ["  New York  ", "\tLondon\t", "\nTokyo\n"]
        
        for city in cities:
            result = await weather_service.get_weather(city)
            assert result.is_success, f"Failed for city with whitespace: '{city}'"
    
    @pytest.mark.asyncio
    async def test_weather_service_performance(self, weather_service):
        """Test weather service performance with multiple requests"""
        import time
        
        cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Moscow"]
        start_time = time.time()
        
        # Make multiple requests
        tasks = [weather_service.get_weather(city) for city in cities]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # Should complete quickly (less than 1 second for 6 requests)
        assert duration < 1.0, f"Performance test failed: {duration:.2f}s for 6 requests"
    
    @pytest.mark.asyncio
    async def test_weather_service_concurrent_access(self, weather_service):
        """Test concurrent access to weather service"""
        # Test concurrent access to same city
        tasks = [weather_service.get_weather("London") for _ in range(5)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed and return same data
        assert all(result.is_success for result in results)
        assert all(result.value == results[0].value for result in results)
    
    @pytest.mark.asyncio
    async def test_weather_service_data_completeness(self, weather_service):
        """Test that all cities have complete weather data"""
        cities_result = await weather_service.get_supported_cities()
        assert cities_result.is_success
        
        cities = cities_result.value
        
        for city in cities:
            # Test weather
            weather_result = await weather_service.get_weather(city)
            assert weather_result.is_success
            
            # Test forecast
            forecast_result = await weather_service.get_weather_forecast(city, 1)
            assert forecast_result.is_success
            
            # Test alerts
            alerts_result = await weather_service.get_weather_alerts(city)
            assert alerts_result.is_success
            
            # Test summary
            summary_result = await weather_service.get_weather_summary(city)
            assert summary_result.is_success
