#!/usr/bin/env python3
"""
Individual Services Tests
"""
import asyncio
from application.container import Container

class IndividualServicesTestSuite:
    """Test suite for individual services"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_total = 0
        
    async def test_configuration_service(self):
        """Test Configuration Service"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            config_service = container.config_service()
            vector_config = config_service.get_vector_db_config()
            if vector_config and 'provider' in vector_config:
                print('✅ Configuration Service: OK')
                self.tests_passed += 1
                return True
            else:
                print('❌ Configuration Service: Failed')
                return False
        except Exception as e:
            print(f'❌ Configuration Service: {e}')
            return False
    
    async def test_weather_service(self):
        """Test Weather Service"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            weather_service = container.weather_service()
            weather_result = await weather_service.get_weather("New York")
            if weather_result.is_success:
                print('✅ Weather Service: OK')
                self.tests_passed += 1
                return True
            else:
                print('❌ Weather Service: Failed')
                return False
        except Exception as e:
            print(f'❌ Weather Service: {e}')
            return False
    
    async def test_time_service(self):
        """Test Time Service"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            time_service = container.time_service()
            time_result = await time_service.get_current_time("New York")
            if time_result.is_success:
                print('✅ Time Service: OK')
                self.tests_passed += 1
                return True
            else:
                print('❌ Time Service: Failed')
                return False
        except Exception as e:
            print(f'❌ Time Service: {e}')
            return False
    
    async def test_city_service(self):
        """Test City Service"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            city_service = container.city_service()
            cities_result = await city_service.get_supported_cities()
            if cities_result.is_success and len(cities_result.value) > 0:
                print('✅ City Service: OK')
                self.tests_passed += 1
                return True
            else:
                print('❌ City Service: Failed')
                return False
        except Exception as e:
            print(f'❌ City Service: {e}')
            return False
    
    async def test_cache_service(self):
        """Test Cache Service"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            cache_service = container.cache_service()
            
            # Test set
            set_result = await cache_service.set("test_key", "test_value", 60)
            if set_result.is_error:
                print(f'❌ Cache Service: Set failed - {set_result.error}')
                return False
            
            # Test get
            get_result = await cache_service.get("test_key")
            if get_result.is_error:
                print(f'❌ Cache Service: Get failed - {get_result.error}')
                return False
            
            if get_result.value == "test_value":
                print('✅ Cache Service: OK')
                self.tests_passed += 1
                return True
            else:
                print(f'❌ Cache Service: Value mismatch - expected "test_value", got {get_result.value}')
                return False
        except Exception as e:
            print(f'❌ Cache Service: {e}')
            return False
    
    async def run_all_tests(self):
        """Run all individual service tests"""
        print('\n🔧 Individual Services Tests:')
        
        tests = [
            self.test_configuration_service,
            self.test_weather_service,
            self.test_time_service,
            self.test_city_service,
            self.test_cache_service
        ]
        
        for test in tests:
            await test()
        
        print(f'Individual Services: {self.tests_passed}/{self.tests_total} passed')
        return self.tests_passed == self.tests_total

if __name__ == "__main__":
    async def main():
        suite = IndividualServicesTestSuite()
        success = await suite.run_all_tests()
        return success
    
    asyncio.run(main())
