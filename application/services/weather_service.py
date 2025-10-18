# services/weather_service.py
from typing import Dict, List, Optional, Any
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.services.IWeatherService import IWeatherService

class WeatherService(IWeatherService):
    """Microservice for weather-related operations"""
    
    def __init__(self):
        self.rop_service = ROPService()
        self._weather_data = {
            "new york": {
                "current": "sunny with 25°C (77°F)",
                "forecast": [
                    {"day": "Today", "condition": "sunny", "temp": "25°C", "humidity": "65%"},
                    {"day": "Tomorrow", "condition": "partly cloudy", "temp": "23°C", "humidity": "70%"},
                    {"day": "Day after", "condition": "rainy", "temp": "20°C", "humidity": "85%"}
                ],
                "alerts": []
            },
            "london": {
                "current": "cloudy with 18°C (64°F)",
                "forecast": [
                    {"day": "Today", "condition": "cloudy", "temp": "18°C", "humidity": "80%"},
                    {"day": "Tomorrow", "condition": "rainy", "temp": "16°C", "humidity": "90%"},
                    {"day": "Day after", "condition": "foggy", "temp": "15°C", "humidity": "95%"}
                ],
                "alerts": ["Fog warning in effect"]
            },
            "tokyo": {
                "current": "rainy with 22°C (72°F)",
                "forecast": [
                    {"day": "Today", "condition": "rainy", "temp": "22°C", "humidity": "85%"},
                    {"day": "Tomorrow", "condition": "sunny", "temp": "26°C", "humidity": "60%"},
                    {"day": "Day after", "condition": "partly cloudy", "temp": "24°C", "humidity": "70%"}
                ],
                "alerts": ["Heavy rain warning"]
            },
            "paris": {
                "current": "partly cloudy with 20°C (68°F)",
                "forecast": [
                    {"day": "Today", "condition": "partly cloudy", "temp": "20°C", "humidity": "70%"},
                    {"day": "Tomorrow", "condition": "sunny", "temp": "22°C", "humidity": "65%"},
                    {"day": "Day after", "condition": "cloudy", "temp": "19°C", "humidity": "75%"}
                ],
                "alerts": []
            },
            "sydney": {
                "current": "clear with 24°C (75°F)",
                "forecast": [
                    {"day": "Today", "condition": "clear", "temp": "24°C", "humidity": "55%"},
                    {"day": "Tomorrow", "condition": "sunny", "temp": "26°C", "humidity": "50%"},
                    {"day": "Day after", "condition": "partly cloudy", "temp": "23°C", "humidity": "60%"}
                ],
                "alerts": []
            },
            "moscow": {
                "current": "snowy with -5°C (23°F)",
                "forecast": [
                    {"day": "Today", "condition": "snowy", "temp": "-5°C", "humidity": "90%"},
                    {"day": "Tomorrow", "condition": "cloudy", "temp": "-3°C", "humidity": "85%"},
                    {"day": "Day after", "condition": "sunny", "temp": "0°C", "humidity": "70%"}
                ],
                "alerts": ["Snow storm warning", "Ice on roads"]
            }
        }
    
    async def get_weather(self, city: str) -> Result[str, str]:
        """Get current weather for a city"""
        try:
            city_lower = city.lower().strip()
            
            # Validation using ROP
            city_validator = self.rop_service.validate(
                lambda c: len(c.strip()) > 0 and len(c.strip()) < 100,
                "City name must be between 1 and 100 characters"
            )
            
            city_format_validator = self.rop_service.validate(
                lambda c: c.replace(" ", "").replace("-", "").isalpha(),
                "City name must contain only letters, spaces, and hyphens"
            )
            
            # ROP pipeline for validation
            validation_pipeline = self.rop_service.pipeline(
                city_validator,
                city_format_validator
            )
            
            validation_result = validation_pipeline(city_lower)
            if validation_result.is_error:
                return validation_result
            
            # Get weather data
            if city_lower in self._weather_data:
                weather_info = self._weather_data[city_lower]["current"]
                return Result.success(weather_info)
            else:
                available_cities = list(self._weather_data.keys())
                return Result.error(f"Weather for '{city}' not available. Supported cities: {', '.join(available_cities)}")
                
        except Exception as e:
            return Result.error(f"Failed to get weather: {str(e)}")
    
    async def get_weather_forecast(self, city: str, days: int = 3) -> Result[List[Dict], str]:
        """Get weather forecast for a city"""
        try:
            city_lower = city.lower().strip()
            
            if city_lower not in self._weather_data:
                available_cities = list(self._weather_data.keys())
                return Result.error(f"Weather forecast for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            forecast = self._weather_data[city_lower]["forecast"][:days]
            return Result.success(forecast)
            
        except Exception as e:
            return Result.error(f"Failed to get weather forecast: {str(e)}")
    
    async def get_weather_alerts(self, city: str) -> Result[List[str], str]:
        """Get weather alerts for a city"""
        try:
            city_lower = city.lower().strip()
            
            if city_lower not in self._weather_data:
                available_cities = list(self._weather_data.keys())
                return Result.error(f"Weather alerts for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            alerts = self._weather_data[city_lower]["alerts"]
            return Result.success(alerts)
            
        except Exception as e:
            return Result.error(f"Failed to get weather alerts: {str(e)}")
    
    async def get_weather_summary(self, city: str) -> Result[Dict[str, any], str]:
        """Get comprehensive weather summary for a city"""
        try:
            city_lower = city.lower().strip()
            
            if city_lower not in self._weather_data:
                available_cities = list(self._weather_data.keys())
                return Result.error(f"Weather summary for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            weather_data = self._weather_data[city_lower]
            summary = {
                "city": city.title(),
                "current_weather": weather_data["current"],
                "forecast": weather_data["forecast"],
                "alerts": weather_data["alerts"],
                "has_alerts": len(weather_data["alerts"]) > 0,
                "alert_count": len(weather_data["alerts"])
            }
            
            return Result.success(summary)
            
        except Exception as e:
            return Result.error(f"Failed to get weather summary: {str(e)}")
    
    async def get_supported_cities(self) -> Result[List[str], str]:
        """Get list of supported cities"""
        try:
            cities = list(self._weather_data.keys())
            return Result.success(cities)
        except Exception as e:
            return Result.error(f"Failed to get supported cities: {str(e)}")
    
    async def is_city_supported(self, city: str) -> Result[bool, str]:
        """Check if city is supported"""
        try:
            city_lower = city.lower().strip()
            is_supported = city_lower in self._weather_data
            return Result.success(is_supported)
        except Exception as e:
            return Result.error(f"Failed to check city support: {str(e)}")
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            health_data = {
                'status': 'healthy',
                'service': self.__class__.__name__,
                'cities_count': len(self._weather_data),
                'supported_cities': list(self._weather_data.keys())[:5]  # First 5 cities
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
