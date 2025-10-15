# tests/services/simple_test.py
import sys
sys.path.append('.')
import asyncio
from application.services.weather_service import WeatherService
from domain.utils.result import Result

async def test_weather_service():
    """Simple test for Weather Service"""
    weather_service = WeatherService()
    
    # Test successful weather retrieval
    result = await weather_service.get_weather("New York")
    
    assert result.is_success
    assert "sunny" in result.value.lower()
    assert "25°C" in result.value
    
    print("✅ Weather Service test passed!")
    
    # Test invalid city
    result = await weather_service.get_weather("InvalidCity")
    assert result.is_error
    assert "not available" in result.error
    
    print("✅ Weather Service error handling test passed!")
    
    # Test supported cities
    result = await weather_service.get_supported_cities()
    assert result.is_success
    cities = result.value
    assert "new york" in cities
    assert "london" in cities
    
    print("✅ Weather Service supported cities test passed!")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_weather_service())
