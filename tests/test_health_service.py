#!/usr/bin/env python3
"""Test Health Service"""

import sys
import os
sys.path.append('.')

import asyncio
from application.services.di_service import DIService

async def test_health_service():
    print('🏥 Testing Health Service...')
    print('=' * 60)
    
    # Initialize DI Service
    di_service = DIService()
    container = di_service.get_container()
    
    # Get services
    embedding_service = di_service.get_embedding_service()
    vector_db_service = di_service.get_vector_db_service()
    health_service = di_service.get_health_service()
    
    if embedding_service is None:
        print('❌ Failed to get embedding service')
        return
    
    # Register services with health service
    print('📋 Registering services with health service...')
    health_service.register_embedding_service(embedding_service)
    health_service.register_qdrant_service(vector_db_service)
    
    print(f'✅ Registered {len(health_service._health_services)} services')
    
    # Test individual service health checks
    print('\n🔍 Testing individual service health checks...')
    for service in health_service._health_services:
        print(f'\n📊 Checking {service.service_name}...')
        result = await service.check_health()
        
        if result.is_success:
            health_check = result.value
            print(f'   Status: {health_check.status.value}')
            print(f'   Message: {health_check.message}')
            print(f'   Response time: {health_check.response_time_ms:.2f}ms')
            
            if health_check.details:
                print(f'   Details: {health_check.details}')
        else:
            print(f'   ❌ Health check failed: {result.error}')
    
    # Test overall system health
    print('\n🎯 Testing overall system health...')
    overall_result = await health_service.check_health()
    
    if overall_result.is_success:
        overall_health = overall_result.value
        print(f'✅ Overall Status: {overall_health.status.value}')
        print(f'📝 Message: {overall_health.message}')
        print(f'⏱️ Response time: {overall_health.response_time_ms:.2f}ms')
        
        if overall_health.details:
            details = overall_health.details
            print(f'📊 Services: {details.get("checked_services", 0)} checked')
            print(f'✅ Healthy: {details.get("healthy_services", 0)}')
            print(f'❌ Unhealthy: {details.get("unhealthy_services", 0)}')
            print(f'⚠️ Degraded: {details.get("degraded_services", 0)}')
    else:
        print(f'❌ Overall health check failed: {overall_result.error}')
    
    # Test detailed health info
    print('\n📋 Testing detailed health info...')
    detailed_info = await health_service.get_detailed_health()
    
    if "error" not in detailed_info:
        print('✅ Detailed health info retrieved successfully')
        print(f'📊 Overall status: {detailed_info["overall_health"]["status"]}')
        print(f'🔧 Service info available for {len(detailed_info["service_info"])} services')
    else:
        print(f'❌ Detailed health info failed: {detailed_info["error"]}')
    
    print('\n🎉 Health Service test completed!')
    print('=' * 60)

if __name__ == "__main__":
    asyncio.run(test_health_service())
