# services/time_service.py
from datetime import datetime
from typing import Dict, List, Optional
from domain.utils.result import Result
from domain.services.rop_service import ROPService

class TimeService:
    """Microservice for time and timezone operations"""
    
    def __init__(self):
        self.rop_service = ROPService()
        self._timezone_data = {
            "new york": {
                "timezone": "America/New_York",
                "utc_offset": "-5:00",
                "dst": True,
                "country": "USA"
            },
            "london": {
                "timezone": "Europe/London", 
                "utc_offset": "+0:00",
                "dst": True,
                "country": "UK"
            },
            "tokyo": {
                "timezone": "Asia/Tokyo",
                "utc_offset": "+9:00", 
                "dst": False,
                "country": "Japan"
            },
            "paris": {
                "timezone": "Europe/Paris",
                "utc_offset": "+1:00",
                "dst": True,
                "country": "France"
            },
            "sydney": {
                "timezone": "Australia/Sydney",
                "utc_offset": "+10:00",
                "dst": True,
                "country": "Australia"
            },
            "moscow": {
                "timezone": "Europe/Moscow",
                "utc_offset": "+3:00",
                "dst": False,
                "country": "Russia"
            }
        }
    
    async def get_current_time(self, city: str) -> Result[str, str]:
        """Get current time for a city with timezone support"""
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
            
            if city_lower not in self._timezone_data:
                available_cities = list(self._timezone_data.keys())
                return Result.error(f"Timezone for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            try:
                from zoneinfo import ZoneInfo
                tz_info = self._timezone_data[city_lower]
                tz = ZoneInfo(tz_info["timezone"])
                now = datetime.now(tz)
                time_str = now.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
                return Result.success(time_str)
            except ImportError:
                # Fallback if zoneinfo not available
                time_str = datetime.now().strftime("%A, %B %d, %Y at %I:%M:%S %p (UTC)")
                return Result.success(time_str)
                
        except Exception as e:
            return Result.error(f"Failed to get current time: {str(e)}")
    
    async def get_timezone_info(self, city: str) -> Result[Dict[str, any], str]:
        """Get timezone information for a city"""
        try:
            city_lower = city.lower().strip()
            
            if city_lower not in self._timezone_data:
                available_cities = list(self._timezone_data.keys())
                return Result.error(f"Timezone info for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            tz_info = self._timezone_data[city_lower]
            return Result.success(tz_info)
            
        except Exception as e:
            return Result.error(f"Failed to get timezone info: {str(e)}")
    
    async def convert_time(self, time_str: str, from_city: str, to_city: str) -> Result[str, str]:
        """Convert time from one city to another"""
        try:
            from_city_lower = from_city.lower().strip()
            to_city_lower = to_city.lower().strip()
            
            if from_city_lower not in self._timezone_data or to_city_lower not in self._timezone_data:
                available_cities = list(self._timezone_data.keys())
                return Result.error(f"One or both cities not supported. Available cities: {', '.join(available_cities)}")
            
            try:
                from zoneinfo import ZoneInfo
                from_tz = ZoneInfo(self._timezone_data[from_city_lower]["timezone"])
                to_tz = ZoneInfo(self._timezone_data[to_city_lower]["timezone"])
                
                # Parse input time (simplified - assumes current date)
                input_time = datetime.strptime(time_str, "%H:%M")
                input_time = input_time.replace(tzinfo=from_tz)
                
                # Convert to target timezone
                converted_time = input_time.astimezone(to_tz)
                result_str = converted_time.strftime("%H:%M %Z")
                
                return Result.success(result_str)
                
            except ImportError:
                return Result.error("Timezone conversion requires zoneinfo module")
            except ValueError:
                return Result.error("Invalid time format. Use HH:MM format")
                
        except Exception as e:
            return Result.error(f"Failed to convert time: {str(e)}")
    
    async def get_world_clock(self) -> Result[List[Dict[str, any]], str]:
        """Get current time for all supported cities"""
        try:
            world_times = []
            
            for city, tz_info in self._timezone_data.items():
                try:
                    from zoneinfo import ZoneInfo
                    tz = ZoneInfo(tz_info["timezone"])
                    now = datetime.now(tz)
                    time_str = now.strftime("%H:%M:%S %Z")
                    
                    world_times.append({
                        "city": city.title(),
                        "time": time_str,
                        "timezone": tz_info["timezone"],
                        "utc_offset": tz_info["utc_offset"],
                        "country": tz_info["country"]
                    })
                except ImportError:
                    # Fallback
                    world_times.append({
                        "city": city.title(),
                        "time": datetime.now().strftime("%H:%M:%S UTC"),
                        "timezone": tz_info["timezone"],
                        "utc_offset": tz_info["utc_offset"],
                        "country": tz_info["country"]
                    })
            
            return Result.success(world_times)
            
        except Exception as e:
            return Result.error(f"Failed to get world clock: {str(e)}")
    
    async def get_time_difference(self, city1: str, city2: str) -> Result[str, str]:
        """Get time difference between two cities"""
        try:
            city1_lower = city1.lower().strip()
            city2_lower = city2.lower().strip()
            
            if city1_lower not in self._timezone_data or city2_lower not in self._timezone_data:
                available_cities = list(self._timezone_data.keys())
                return Result.error(f"One or both cities not supported. Available cities: {', '.join(available_cities)}")
            
            tz1_info = self._timezone_data[city1_lower]
            tz2_info = self._timezone_data[city2_lower]
            
            # Simple offset comparison (this could be more sophisticated)
            offset1 = tz1_info["utc_offset"]
            offset2 = tz2_info["utc_offset"]
            
            difference_info = {
                "city1": city1.title(),
                "city2": city2.title(),
                "offset1": offset1,
                "offset2": offset2,
                "timezone1": tz1_info["timezone"],
                "timezone2": tz2_info["timezone"]
            }
            
            return Result.success(difference_info)
            
        except Exception as e:
            return Result.error(f"Failed to get time difference: {str(e)}")
    
    async def get_supported_cities(self) -> Result[List[str], str]:
        """Get list of supported cities"""
        try:
            cities = list(self._timezone_data.keys())
            return Result.success(cities)
        except Exception as e:
            return Result.error(f"Failed to get supported cities: {str(e)}")
    
    async def is_city_supported(self, city: str) -> Result[bool, str]:
        """Check if city is supported"""
        try:
            city_lower = city.lower().strip()
            is_supported = city_lower in self._timezone_data
            return Result.success(is_supported)
        except Exception as e:
            return Result.error(f"Failed to check city support: {str(e)}")
