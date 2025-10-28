#!/usr/bin/env python3
"""
Comprehensive Test Suite - All tests with collection checking
"""
import asyncio
import pytest
from application.container import Container

async def check_collection():
    """Check if main collection exists"""
    print('🔍 Sprawdzam kolekcję...')
    container = Container()
    container.wire(modules=[__name__])
    vector_db_service = container.vector_db_service()
    search_result = await vector_db_service.search('weather', limit=1)
    if search_result.is_success:
        print('✅ Kolekcja istnieje!')
        return True
    else:
        print('❌ Kolekcja nie istnieje!')
        return False

@pytest.mark.asyncio
async def test_all():
    """Test all suites with collection monitoring"""
    print('🚀 Testuję wszystkie testy...')
    
    # Test 1: Functional
    print('\n📋 Functional Tests:')
    before = await check_collection()
    from tests.test_functional_comprehensive import FunctionalTestSuite
    suite1 = FunctionalTestSuite()
    success1 = await suite1.run_all_tests()
    after = await check_collection()
    status1 = "PASSED" if success1 else "FAILED"
    collection1 = "OK" if before == after else "ZMIENIONA"
    print(f'Wynik: {status1} | Kolekcja: {collection1}')
    
    # Test 2: Integration
    print('\n📋 Integration Tests:')
    before = await check_collection()
    from tests.test_integration_comprehensive import IntegrationTestSuite
    suite2 = IntegrationTestSuite()
    success2 = await suite2.run_all_tests()
    after = await check_collection()
    status2 = "PASSED" if success2 else "FAILED"
    collection2 = "OK" if before == after else "ZMIENIONA"
    print(f'Wynik: {status2} | Kolekcja: {collection2}')
    
    # Test 3: Performance
    print('\n📋 Performance Tests:')
    before = await check_collection()
    from tests.test_performance_comprehensive import PerformanceTestSuite
    suite3 = PerformanceTestSuite()
    success3 = await suite3.run_all_tests()
    after = await check_collection()
    status3 = "PASSED" if success3 else "FAILED"
    collection3 = "OK" if before == after else "ZMIENIONA"
    print(f'Wynik: {status3} | Kolekcja: {collection3}')
    
    # Test 4: Individual Services
    print('\n📋 Individual Services Tests:')
    before = await check_collection()
    from tests.test_individual_services import IndividualServicesTestSuite
    suite4 = IndividualServicesTestSuite()
    success4 = await suite4.run_all_tests()
    after = await check_collection()
    status4 = "PASSED" if success4 else "FAILED"
    collection4 = "OK" if before == after else "ZMIENIONA"
    print(f'Wynik: {status4} | Kolekcja: {collection4}')
    
    # Test 5: Error Handling
    print('\n📋 Error Handling Tests:')
    before = await check_collection()
    from tests.test_error_handling import ErrorHandlingTestSuite
    suite5 = ErrorHandlingTestSuite()
    success5 = await suite5.run_all_tests()
    after = await check_collection()
    status5 = "PASSED" if success5 else "FAILED"
    collection5 = "OK" if before == after else "ZMIENIONA"
    print(f'Wynik: {status5} | Kolekcja: {collection5}')
    
    # Test 6: Concurrent Operations
    print('\n📋 Concurrent Operations Tests:')
    before = await check_collection()
    from tests.test_concurrent_operations import ConcurrentOperationsTestSuite
    suite6 = ConcurrentOperationsTestSuite()
    success6 = await suite6.run_all_tests()
    after = await check_collection()
    status6 = "PASSED" if success6 else "FAILED"
    collection6 = "OK" if before == after else "ZMIENIONA"
    print(f'Wynik: {status6} | Kolekcja: {collection6}')
    
    # Test 7: Business Logic
    print('\n📋 Business Logic Tests:')
    before = await check_collection()
    from tests.test_business_logic import BusinessLogicTestSuite
    suite7 = BusinessLogicTestSuite()
    success7 = await suite7.run_all_tests()
    after = await check_collection()
    status7 = "PASSED" if success7 else "FAILED"
    collection7 = "OK" if before == after else "ZMIENIONA"
    print(f'Wynik: {status7} | Kolekcja: {collection7}')
    
    print('\n🎯 PODSUMOWANIE:')
    print(f'Functional: {"✅" if success1 else "❌"}')
    print(f'Integration: {"✅" if success2 else "❌"}')
    print(f'Performance: {"✅" if success3 else "❌"}')
    print(f'Individual Services: {"✅" if success4 else "❌"}')
    print(f'Error Handling: {"✅" if success5 else "❌"}')
    print(f'Concurrent Operations: {"✅" if success6 else "❌"}')
    print(f'Business Logic: {"✅" if success7 else "❌"}')
    
    total_tests = 7
    passed_tests = sum([success1, success2, success3, success4, success5, success6, success7])
    print(f'\n📊 OVERALL: {passed_tests}/{total_tests} test suites passed')
    
    final = await check_collection()
    print(f'\nFinalna kolekcja: {"✅ ISTNIEJE" if final else "❌ NIE ISTNIEJE"}')

if __name__ == "__main__":
    asyncio.run(test_all())
