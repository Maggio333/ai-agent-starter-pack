#!/usr/bin/env python3
"""
Concurrent Operations Tests
"""
import asyncio
import time
from application.container import Container

class ConcurrentOperationsTestSuite:
    """Test suite for concurrent operations"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_total = 0
        
    async def test_concurrent_embeddings(self):
        """Test concurrent embedding operations"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            embedding_service = container.embedding_service()
            
            async def create_embedding(text):
                return await embedding_service.create_embedding(text)
            
            # Run 5 concurrent embedding operations
            tasks = [create_embedding(f"Concurrent test {i}") for i in range(5)]
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            duration = time.time() - start_time
            
            success_count = sum(1 for r in results if not isinstance(r, Exception) and r.is_success)
            if success_count >= 4:  # At least 4 out of 5 should succeed
                print(f'✅ Concurrent Embeddings: {success_count}/5 succeeded in {duration:.2f}s')
                self.tests_passed += 1
                return True
            else:
                print(f'❌ Concurrent Embeddings: Only {success_count}/5 succeeded')
                return False
        except Exception as e:
            print(f'❌ Concurrent Embeddings: {e}')
            return False
    
    async def test_concurrent_cache(self):
        """Test concurrent cache operations"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            cache_service = container.cache_service()
            
            async def cache_operation(key, value):
                set_result = await cache_service.set(key, value, 60)
                if set_result.is_error:
                    return None
                get_result = await cache_service.get(key)
                if get_result.is_error:
                    return None
                return get_result.value
            
            # Run 10 concurrent cache operations
            tasks = [cache_operation(f"cache_key_{i}", f"value_{i}") for i in range(10)]
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            duration = time.time() - start_time
            
            success_count = sum(1 for r in results if not isinstance(r, Exception) and r is not None)
            if success_count >= 9:  # At least 9 out of 10 should succeed
                print(f'✅ Concurrent Cache: {success_count}/10 succeeded in {duration:.2f}s')
                self.tests_passed += 1
                return True
            else:
                print(f'❌ Concurrent Cache: Only {success_count}/10 succeeded')
                return False
        except Exception as e:
            print(f'❌ Concurrent Cache: {e}')
            return False
    
    async def test_concurrent_weather(self):
        """Test concurrent weather operations"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            weather_service = container.weather_service()
            
            async def get_weather(city):
                return await weather_service.get_weather(city)
            
            # Run 3 concurrent weather operations
            cities = ["New York", "London", "Tokyo"]
            tasks = [get_weather(city) for city in cities]
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            duration = time.time() - start_time
            
            success_count = sum(1 for r in results if not isinstance(r, Exception) and r.is_success)
            if success_count >= 2:  # At least 2 out of 3 should succeed
                print(f'✅ Concurrent Weather: {success_count}/3 succeeded in {duration:.2f}s')
                self.tests_passed += 1
                return True
            else:
                print(f'❌ Concurrent Weather: Only {success_count}/3 succeeded')
                return False
        except Exception as e:
            print(f'❌ Concurrent Weather: {e}')
            return False
    
    async def test_mixed_concurrent_operations(self):
        """Test mixed concurrent operations"""
        self.tests_total += 1
        try:
            container = Container()
            container.wire(modules=[__name__])
            
            async def mixed_operation(operation_id):
                if operation_id % 3 == 0:
                    # Cache operation
                    cache_service = container.cache_service()
                    set_result = await cache_service.set(f"mixed_key_{operation_id}", f"mixed_value_{operation_id}", 60)
                    if set_result.is_error:
                        return None
                    get_result = await cache_service.get(f"mixed_key_{operation_id}")
                    if get_result.is_error:
                        return None
                    return get_result.value
                elif operation_id % 3 == 1:
                    # Weather operation
                    weather_service = container.weather_service()
                    return await weather_service.get_weather("New York")
                else:
                    # Time operation
                    time_service = container.time_service()
                    return await time_service.get_current_time("New York")
            
            # Run 6 mixed concurrent operations
            tasks = [mixed_operation(i) for i in range(6)]
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            duration = time.time() - start_time
            
            success_count = sum(1 for r in results if not isinstance(r, Exception))
            if success_count >= 5:  # At least 5 out of 6 should succeed
                print(f'✅ Mixed Concurrent: {success_count}/6 succeeded in {duration:.2f}s')
                self.tests_passed += 1
                return True
            else:
                print(f'❌ Mixed Concurrent: Only {success_count}/6 succeeded')
                return False
        except Exception as e:
            print(f'❌ Mixed Concurrent: {e}')
            return False
    
    async def run_all_tests(self):
        """Run all concurrent operation tests"""
        print('\n⚡ Concurrent Operations Tests:')
        
        tests = [
            self.test_concurrent_embeddings,
            self.test_concurrent_cache,
            self.test_concurrent_weather,
            self.test_mixed_concurrent_operations
        ]
        
        for test in tests:
            await test()
        
        print(f'Concurrent Operations: {self.tests_passed}/{self.tests_total} passed')
        return self.tests_passed == self.tests_total

if __name__ == "__main__":
    async def main():
        suite = ConcurrentOperationsTestSuite()
        success = await suite.run_all_tests()
        return success
    
    asyncio.run(main())
