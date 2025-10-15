# tests/services/test_city_service.py
import sys
sys.path.append('.')
import pytest
import asyncio
from application.services.city_service import CityService
from domain.utils.result import Result

class TestCityService:
    """Test suite for City Service"""
    
    @pytest.fixture
    def city_service(self):
        """Create CityService instance for testing"""
        return CityService()
    
    @pytest.mark.asyncio
    async def test_get_city_info_success(self, city_service):
        """Test successful city information retrieval"""
        result = await city_service.get_city_info("New York")
        
        assert result.is_success
        city_info = result.value
        assert "city_name" in city_info
        assert "population" in city_info
        assert "country" in city_info
        assert "currency" in city_info
        assert "coordinates" in city_info
        assert city_info["city_name"] == "New York"
    
    @pytest.mark.asyncio
    async def test_get_city_info_invalid_city(self, city_service):
        """Test city info retrieval for unsupported city"""
        result = await city_service.get_city_info("InvalidCity")
        
        assert result.is_error
        assert "not available" in result.error
        assert "Supported cities" in result.error
    
    @pytest.mark.asyncio
    async def test_get_city_info_empty_city(self, city_service):
        """Test city info retrieval with empty city name"""
        result = await city_service.get_city_info("")
        
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_search_cities(self, city_service):
        """Test city search functionality"""
        result = await city_service.search_cities("New")
        
        assert result.is_success
        results = result.value
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Check structure
        for city_result in results:
            assert "city_name" in city_result
            assert "match_type" in city_result
            assert "data" in city_result
    
    @pytest.mark.asyncio
    async def test_search_cities_empty_query(self, city_service):
        """Test city search with empty query"""
        result = await city_service.search_cities("")
        
        assert result.is_error
        assert "Search query cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_search_cities_by_country(self, city_service):
        """Test city search by country"""
        result = await city_service.search_cities("USA")
        
        assert result.is_success
        results = result.value
        assert len(results) > 0
        
        # Should find New York
        city_names = [r["city_name"] for r in results]
        assert "New York" in city_names
    
    @pytest.mark.asyncio
    async def test_search_cities_by_attraction(self, city_service):
        """Test city search by attraction"""
        result = await city_service.search_cities("Statue of Liberty")
        
        assert result.is_success
        results = result.value
        assert len(results) > 0
        
        # Should find New York
        city_names = [r["city_name"] for r in results]
        assert "New York" in city_names
    
    @pytest.mark.asyncio
    async def test_get_city_coordinates(self, city_service):
        """Test city coordinates retrieval"""
        result = await city_service.get_city_coordinates("London")
        
        assert result.is_success
        coordinates = result.value
        assert "lat" in coordinates
        assert "lng" in coordinates
        assert isinstance(coordinates["lat"], float)
        assert isinstance(coordinates["lng"], float)
    
    @pytest.mark.asyncio
    async def test_get_city_coordinates_invalid_city(self, city_service):
        """Test city coordinates for invalid city"""
        result = await city_service.get_city_coordinates("InvalidCity")
        
        assert result.is_error
        assert "not available" in result.error
    
    @pytest.mark.asyncio
    async def test_get_city_attractions(self, city_service):
        """Test city attractions retrieval"""
        result = await city_service.get_city_attractions("Paris")
        
        assert result.is_success
        attractions = result.value
        assert isinstance(attractions, list)
        assert len(attractions) > 0
        assert "Eiffel Tower" in attractions
    
    @pytest.mark.asyncio
    async def test_get_city_airports(self, city_service):
        """Test city airports retrieval"""
        result = await city_service.get_city_airports("New York")
        
        assert result.is_success
        airports = result.value
        assert isinstance(airports, list)
        assert len(airports) > 0
        assert "JFK" in airports
    
    @pytest.mark.asyncio
    async def test_compare_cities(self, city_service):
        """Test city comparison functionality"""
        result = await city_service.compare_cities("New York", "London")
        
        assert result.is_success
        comparison = result.value
        assert "city1" in comparison
        assert "city2" in comparison
        assert "comparison" in comparison
        
        assert comparison["city1"]["name"] == "New York"
        assert comparison["city2"]["name"] == "London"
        assert "same_country" in comparison["comparison"]
        assert "same_currency" in comparison["comparison"]
    
    @pytest.mark.asyncio
    async def test_compare_cities_invalid(self, city_service):
        """Test city comparison with invalid cities"""
        result = await city_service.compare_cities("InvalidCity1", "InvalidCity2")
        
        assert result.is_error
        assert "not supported" in result.error
    
    @pytest.mark.asyncio
    async def test_get_cities_by_country(self, city_service):
        """Test getting cities by country"""
        result = await city_service.get_cities_by_country("USA")
        
        assert result.is_success
        cities = result.value
        assert isinstance(cities, list)
        assert len(cities) > 0
        
        # Should find New York
        city_names = [c["city_name"] for c in cities]
        assert "New York" in city_names
    
    @pytest.mark.asyncio
    async def test_get_cities_by_country_invalid(self, city_service):
        """Test getting cities by invalid country"""
        result = await city_service.get_cities_by_country("InvalidCountry")
        
        assert result.is_error
        assert "No cities found" in result.error
        assert "Available countries" in result.error
    
    @pytest.mark.asyncio
    async def test_get_supported_cities(self, city_service):
        """Test getting list of supported cities"""
        result = await city_service.get_supported_cities()
        
        assert result.is_success
        cities = result.value
        assert isinstance(cities, list)
        assert len(cities) > 0
        assert "new york" in cities
        assert "london" in cities
        assert "tokyo" in cities
    
    @pytest.mark.asyncio
    async def test_is_city_supported(self, city_service):
        """Test city support checking"""
        # Test supported city
        result = await city_service.is_city_supported("Paris")
        assert result.is_success
        assert result.value is True
        
        # Test unsupported city
        result = await city_service.is_city_supported("InvalidCity")
        assert result.is_success
        assert result.value is False
    
    @pytest.mark.asyncio
    async def test_city_data_completeness(self, city_service):
        """Test that all cities have complete data"""
        cities_result = await city_service.get_supported_cities()
        assert cities_result.is_success
        
        cities = cities_result.value
        
        for city in cities:
            # Test city info
            info_result = await city_service.get_city_info(city)
            assert info_result.is_success
            
            city_info = info_result.value
            required_fields = [
                "population", "country", "currency", "coordinates",
                "area", "founded", "mayor", "language", "climate",
                "attractions", "airports", "timezone"
            ]
            
            for field in required_fields:
                assert field in city_info, f"Missing field {field} for city {city}"
    
    @pytest.mark.asyncio
    async def test_city_service_case_insensitive(self, city_service):
        """Test that city service is case insensitive"""
        cities = ["NEW YORK", "london", "ToKyO", "pArIs"]
        
        for city in cities:
            result = await city_service.get_city_info(city)
            assert result.is_success, f"Failed for city: {city}"
    
    @pytest.mark.asyncio
    async def test_city_service_whitespace_handling(self, city_service):
        """Test that city service handles whitespace correctly"""
        cities = ["  New York  ", "\tLondon\t", "\nTokyo\n"]
        
        for city in cities:
            result = await city_service.get_city_info(city)
            assert result.is_success, f"Failed for city with whitespace: '{city}'"
    
    @pytest.mark.asyncio
    async def test_city_service_error_handling(self, city_service):
        """Test error handling in city service"""
        # Test with None input
        result = await city_service.get_city_info(None)
        assert result.is_error
        
        # Test with very long city name
        long_city = "A" * 200
        result = await city_service.get_city_info(long_city)
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_city_service_performance(self, city_service):
        """Test city service performance with multiple requests"""
        import time
        
        cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Moscow"]
        start_time = time.time()
        
        # Make multiple requests
        tasks = [city_service.get_city_info(city) for city in cities]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # Should complete quickly (less than 1 second for 6 requests)
        assert duration < 1.0, f"Performance test failed: {duration:.2f}s for 6 requests"
    
    @pytest.mark.asyncio
    async def test_city_service_concurrent_access(self, city_service):
        """Test concurrent access to city service"""
        # Test concurrent access to same city
        tasks = [city_service.get_city_info("London") for _ in range(5)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed and return same data
        assert all(result.is_success for result in results)
        assert all(result.value == results[0].value for result in results)
    
    @pytest.mark.asyncio
    async def test_city_service_search_comprehensive(self, city_service):
        """Test comprehensive city search functionality"""
        # Test search by city name
        result = await city_service.search_cities("New")
        assert result.is_success
        assert len(result.value) > 0
        
        # Test search by country
        result = await city_service.search_cities("Japan")
        assert result.is_success
        assert len(result.value) > 0
        
        # Test search by attraction
        result = await city_service.search_cities("Big Ben")
        assert result.is_success
        assert len(result.value) > 0
    
    @pytest.mark.asyncio
    async def test_city_service_coordinates_accuracy(self, city_service):
        """Test city coordinates accuracy"""
        # Test New York coordinates
        result = await city_service.get_city_coordinates("New York")
        assert result.is_success
        
        coordinates = result.value
        assert abs(coordinates["lat"] - 40.7128) < 0.1
        assert abs(coordinates["lng"] - (-74.0060)) < 0.1
    
    @pytest.mark.asyncio
    async def test_city_service_attractions_completeness(self, city_service):
        """Test that city attractions are complete"""
        result = await city_service.get_city_attractions("Paris")
        assert result.is_success
        
        attractions = result.value
        expected_attractions = ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Champs-Élysées"]
        
        for attraction in expected_attractions:
            assert attraction in attractions
    
    @pytest.mark.asyncio
    async def test_city_service_airports_completeness(self, city_service):
        """Test that city airports are complete"""
        result = await city_service.get_city_airports("London")
        assert result.is_success
        
        airports = result.value
        expected_airports = ["LHR", "LGW", "STN"]
        
        for airport in expected_airports:
            assert airport in airports
