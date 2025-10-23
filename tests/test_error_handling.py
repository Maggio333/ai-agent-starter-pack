#!/usr/bin/env python3
"""
Error Handling Tests
"""
import asyncio
from application.container import Container

class ErrorHandlingTestSuite:
    """Test suite for error handling and resilience"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_total = 0
        
    async def test_invalid_city_weather(self):
        """Test invalid city weather handling"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            weather_service = container.weather_service()
            invalid_result = await weather_service.get_weather("InvalidCity123")
            if not invalid_result.is_success:  # Should fail gracefully
                print('✅ Invalid City Weather: Handled gracefully')
                self.tests_passed += 1
                return True
            else:
                print('❌ Invalid City Weather: Should have failed')
                return False
        except Exception as e:
            print(f'❌ Invalid City Weather: {e}')
            return False
    
    async def test_invalid_time_zone(self):
        """Test invalid time zone handling"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            time_service = container.time_service()
            invalid_result = await time_service.get_current_time("InvalidCity123")
            if not invalid_result.is_success:  # Should fail gracefully
                print('✅ Invalid Time Zone: Handled gracefully')
                self.tests_passed += 1
                return True
            else:
                print('❌ Invalid Time Zone: Should have failed')
                return False
        except Exception as e:
            print(f'❌ Invalid Time Zone: {e}')
            return False
    
    async def test_cache_invalid_key(self):
        """Test cache invalid key handling"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            cache_service = container.cache_service()
            
            # Test getting non-existent key
            get_result = await cache_service.get("nonexistent_key")
            if get_result.is_error:
                print(f'❌ Cache Invalid Key: Get failed - {get_result.error}')
                return False
            
            if get_result.value is None:  # Should return None for missing key
                print('✅ Cache Invalid Key: Handled gracefully')
                self.tests_passed += 1
                return True
            else:
                print(f'❌ Cache Invalid Key: Should return None, got {get_result.value}')
                return False
        except Exception as e:
            print(f'❌ Cache Invalid Key: {e}')
            return False
    
    async def test_embedding_service_error(self):
        """Test embedding service error handling"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            embedding_service = container.embedding_service()
            # Test with empty string
            empty_result = await embedding_service.create_embedding("")
            if not empty_result.is_success:  # Should fail gracefully
                print('✅ Empty Embedding: Handled gracefully')
                self.tests_passed += 1
                return True
            else:
                print('❌ Empty Embedding: Should have failed')
                return False
        except Exception as e:
            print(f'❌ Empty Embedding: {e}')
            return False
    
    async def run_all_tests(self):
        """Run all error handling tests"""
        print('\n🛡️ Error Handling Tests:')
        
        tests = [
            self.test_invalid_city_weather,
            self.test_invalid_time_zone,
            self.test_cache_invalid_key,
            self.test_embedding_service_error
        ]
        
        for test in tests:
            await test()
        
        print(f'Error Handling: {self.tests_passed}/{self.tests_total} passed')
        return self.tests_passed == self.tests_total

if __name__ == "__main__":
    async def main():
        suite = ErrorHandlingTestSuite()
        success = await suite.run_all_tests()
        return success
    
    asyncio.run(main())
