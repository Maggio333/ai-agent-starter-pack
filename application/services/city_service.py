# services/city_service.py
from typing import Dict, List, Optional, Any
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.services.ICityService import ICityService

class CityService(ICityService):
    """Microservice for city information and data operations"""
    
    def __init__(self):
        self.rop_service = ROPService()
        self._city_data = {
            "new york": {
                "population": "8.4M",
                "country": "USA",
                "currency": "USD",
                "coordinates": {"lat": 40.7128, "lng": -74.0060},
                "area": "468.9 sq mi",
                "founded": "1624",
                "mayor": "Eric Adams",
                "language": "English",
                "climate": "Humid subtropical",
                "attractions": ["Statue of Liberty", "Central Park", "Times Square", "Brooklyn Bridge"],
                "airports": ["JFK", "LGA", "EWR"],
                "timezone": "America/New_York"
            },
            "london": {
                "population": "9.5M",
                "country": "UK", 
                "currency": "GBP",
                "coordinates": {"lat": 51.5074, "lng": -0.1278},
                "area": "607 sq mi",
                "founded": "43 AD",
                "mayor": "Sadiq Khan",
                "language": "English",
                "climate": "Oceanic",
                "attractions": ["Big Ben", "Tower Bridge", "London Eye", "Buckingham Palace"],
                "airports": ["LHR", "LGW", "STN"],
                "timezone": "Europe/London"
            },
            "tokyo": {
                "population": "14M",
                "country": "Japan",
                "currency": "JPY", 
                "coordinates": {"lat": 35.6762, "lng": 139.6503},
                "area": "845 sq mi",
                "founded": "1457",
                "mayor": "Yuriko Koike",
                "language": "Japanese",
                "climate": "Humid subtropical",
                "attractions": ["Tokyo Tower", "Senso-ji Temple", "Shibuya Crossing", "Imperial Palace"],
                "airports": ["NRT", "HND"],
                "timezone": "Asia/Tokyo"
            },
            "paris": {
                "population": "2.1M",
                "country": "France",
                "currency": "EUR",
                "coordinates": {"lat": 48.8566, "lng": 2.3522},
                "area": "40.7 sq mi", 
                "founded": "3rd century BC",
                "mayor": "Anne Hidalgo",
                "language": "French",
                "climate": "Oceanic",
                "attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Champs-Élysées"],
                "airports": ["CDG", "ORY"],
                "timezone": "Europe/Paris"
            },
            "sydney": {
                "population": "5.3M",
                "country": "Australia",
                "currency": "AUD",
                "coordinates": {"lat": -33.8688, "lng": 151.2093},
                "area": "4,775 sq mi",
                "founded": "1788",
                "mayor": "Clover Moore",
                "language": "English",
                "climate": "Oceanic",
                "attractions": ["Sydney Opera House", "Harbour Bridge", "Bondi Beach", "Royal Botanic Gardens"],
                "airports": ["SYD"],
                "timezone": "Australia/Sydney"
            },
            "moscow": {
                "population": "12.5M",
                "country": "Russia",
                "currency": "RUB",
                "coordinates": {"lat": 55.7558, "lng": 37.6176},
                "area": "970 sq mi",
                "founded": "1147",
                "mayor": "Sergey Sobyanin",
                "language": "Russian",
                "climate": "Humid continental",
                "attractions": ["Red Square", "Kremlin", "St. Basil's Cathedral", "Bolshoi Theatre"],
                "airports": ["SVO", "DME", "VKO"],
                "timezone": "Europe/Moscow"
            }
        }
    
    async def get_city_info(self, city: str) -> Result[Dict[str, Any], str]:
        """Get comprehensive city information"""
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
            
            if city_lower not in self._city_data:
                available_cities = list(self._city_data.keys())
                return Result.error(f"City data for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            city_info = self._city_data[city_lower].copy()
            city_info["city_name"] = city.title()
            
            return Result.success(city_info)
            
        except Exception as e:
            return Result.error(f"Failed to get city info: {str(e)}")
    
    async def search_cities(self, query: str) -> Result[List[Dict[str, Any]], str]:
        """Search cities by name or attributes"""
        try:
            query_lower = query.lower().strip()
            
            if not query_lower:
                return Result.error("Search query cannot be empty")
            
            matching_cities = []
            
            for city_name, city_data in self._city_data.items():
                # Search in city name
                if query_lower in city_name:
                    matching_cities.append({
                        "city_name": city_name.title(),
                        "match_type": "name",
                        "data": city_data
                    })
                    continue
                
                # Search in country
                if query_lower in city_data["country"].lower():
                    matching_cities.append({
                        "city_name": city_name.title(),
                        "match_type": "country",
                        "data": city_data
                    })
                    continue
                
                # Search in attractions
                for attraction in city_data["attractions"]:
                    if query_lower in attraction.lower():
                        matching_cities.append({
                            "city_name": city_name.title(),
                            "match_type": "attraction",
                            "attraction": attraction,
                            "data": city_data
                        })
                        break
            
            return Result.success(matching_cities)
            
        except Exception as e:
            return Result.error(f"Failed to search cities: {str(e)}")
    
    async def get_city_coordinates(self, city: str) -> Result[Dict[str, float], str]:
        """Get city coordinates (latitude and longitude)"""
        try:
            city_lower = city.lower().strip()
            
            if city_lower not in self._city_data:
                available_cities = list(self._city_data.keys())
                return Result.error(f"Coordinates for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            coordinates = self._city_data[city_lower]["coordinates"]
            return Result.success(coordinates)
            
        except Exception as e:
            return Result.error(f"Failed to get city coordinates: {str(e)}")
    
    async def get_city_attractions(self, city: str) -> Result[List[str], str]:
        """Get list of attractions for a city"""
        try:
            city_lower = city.lower().strip()
            
            if city_lower not in self._city_data:
                available_cities = list(self._city_data.keys())
                return Result.error(f"Attractions for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            attractions = self._city_data[city_lower]["attractions"]
            return Result.success(attractions)
            
        except Exception as e:
            return Result.error(f"Failed to get city attractions: {str(e)}")
    
    async def get_city_airports(self, city: str) -> Result[List[str], str]:
        """Get list of airports for a city"""
        try:
            city_lower = city.lower().strip()
            
            if city_lower not in self._city_data:
                available_cities = list(self._city_data.keys())
                return Result.error(f"Airports for '{city}' not available. Supported cities: {', '.join(available_cities)}")
            
            airports = self._city_data[city_lower]["airports"]
            return Result.success(airports)
            
        except Exception as e:
            return Result.error(f"Failed to get city airports: {str(e)}")
    
    async def compare_cities(self, city1: str, city2: str) -> Result[Dict[str, Any], str]:
        """Compare two cities"""
        try:
            city1_lower = city1.lower().strip()
            city2_lower = city2.lower().strip()
            
            if city1_lower not in self._city_data or city2_lower not in self._city_data:
                available_cities = list(self._city_data.keys())
                return Result.error(f"One or both cities not supported. Available cities: {', '.join(available_cities)}")
            
            city1_data = self._city_data[city1_lower]
            city2_data = self._city_data[city2_lower]
            
            comparison = {
                "city1": {
                    "name": city1.title(),
                    "population": city1_data["population"],
                    "country": city1_data["country"],
                    "currency": city1_data["currency"],
                    "area": city1_data["area"],
                    "climate": city1_data["climate"]
                },
                "city2": {
                    "name": city2.title(),
                    "population": city2_data["population"],
                    "country": city2_data["country"],
                    "currency": city2_data["currency"],
                    "area": city2_data["area"],
                    "climate": city2_data["climate"]
                },
                "comparison": {
                    "same_country": city1_data["country"] == city2_data["country"],
                    "same_currency": city1_data["currency"] == city2_data["currency"],
                    "same_climate": city1_data["climate"] == city2_data["climate"]
                }
            }
            
            return Result.success(comparison)
            
        except Exception as e:
            return Result.error(f"Failed to compare cities: {str(e)}")
    
    async def get_cities_by_country(self, country: str) -> Result[List[Dict[str, Any]], str]:
        """Get all cities in a specific country"""
        try:
            country_lower = country.lower().strip()
            
            cities_in_country = []
            
            for city_name, city_data in self._city_data.items():
                if country_lower in city_data["country"].lower():
                    cities_in_country.append({
                        "city_name": city_name.title(),
                        "data": city_data
                    })
            
            if not cities_in_country:
                available_countries = list(set(data["country"] for data in self._city_data.values()))
                return Result.error(f"No cities found for country '{country}'. Available countries: {', '.join(available_countries)}")
            
            return Result.success(cities_in_country)
            
        except Exception as e:
            return Result.error(f"Failed to get cities by country: {str(e)}")
    
    async def get_supported_cities(self) -> Result[List[str], str]:
        """Get list of supported cities"""
        try:
            cities = list(self._city_data.keys())
            return Result.success(cities)
        except Exception as e:
            return Result.error(f"Failed to get supported cities: {str(e)}")
    
    async def is_city_supported(self, city: str) -> Result[bool, str]:
        """Check if city is supported"""
        try:
            city_lower = city.lower().strip()
            is_supported = city_lower in self._city_data
            return Result.success(is_supported)
        except Exception as e:
            return Result.error(f"Failed to check city support: {str(e)}")
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            health_data = {
                'status': 'healthy',
                'service': self.__class__.__name__,
                'cities_count': len(self._city_data),
                'supported_cities': list(self._city_data.keys())[:5]  # First 5 cities
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
