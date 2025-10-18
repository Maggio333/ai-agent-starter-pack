#!/usr/bin/env python3
"""Test Email Service z nową architekturą DI"""

import sys
import os
sys.path.append('.')

import asyncio
from application.services.di_service import DIService

async def test_email_service():
    print('Testing Email Service with Auto-Discovery...')
    print('=' * 60)
    
    # Initialize DI Service
    print('Initializing DI Service...')
    di_service = DIService()
    
    # Auto-discovered email service!
    print('Getting email service (auto-discovered)...')
    email_service = di_service.get_email_service()
    
    print(f'Email Service: {type(email_service).__name__}')
    
    # Test email validation
    print('\nTesting email validation...')
    valid_result = await email_service.validate_email("test@example.com")
    invalid_result = await email_service.validate_email("invalid-email")
    
    print(f'Valid email test: {valid_result.is_success}')
    print(f'Invalid email test: {not invalid_result.is_success}')
    
    # Test sending email
    print('\nTesting email sending...')
    send_result = await email_service.send_email(
        to="user@example.com",
        subject="Test Email",
        body="To jest testowy email z nowej architektury DI!"
    )
    
    print(f'Email sent: {send_result.is_success}')
    if send_result.is_error:
        print(f'   Error: {send_result.error}')
    
    # Test template email
    print('\nTesting template email...')
    template_result = await email_service.send_template_email(
        to="user@example.com",
        template_name="welcome",
        template_data={
            "name": "Arek",
            "app_name": "ATSReflectumAgentStarterPack"
        }
    )
    
    print(f'Template email sent: {template_result.is_success}')
    
    # Test bulk email
    print('\nTesting bulk email...')
    bulk_emails = [
        {"to": "user1@example.com", "subject": "Bulk 1", "body": "Email 1"},
        {"to": "user2@example.com", "subject": "Bulk 2", "body": "Email 2"},
        {"to": "invalid-email", "subject": "Bulk 3", "body": "Email 3"}  # Invalid
    ]
    
    bulk_result = await email_service.send_bulk_email(bulk_emails)
    print(f'Bulk email results: {bulk_result.value if bulk_result.is_success else "Failed"}')
    
    # Test health check
    print('\nTesting health check...')
    health_result = await email_service.health_check()
    print(f'Health check: {health_result.is_success}')
    if health_result.is_success:
        print(f'   Status: {health_result.value["status"]}')
    
    # Test service status
    print('\nTesting service status...')
    status = di_service.get_service_status()
    print(f'Email service in status: {status.get("email_service", False)}')
    
    print('\nEmail Service test completed!')
    print('=' * 60)

if __name__ == "__main__":
    asyncio.run(test_email_service())
