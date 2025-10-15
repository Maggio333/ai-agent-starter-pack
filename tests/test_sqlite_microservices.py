# tests/test_sqlite_microservices.py
import asyncio
import sys
import os
sys.path.append('.')

from infrastructure.data.storage.sqlite_chat_repository import SqliteChatRepository
from infrastructure.data.storage.sqlite import CRUDService, BulkOperationsService, SearchService, ThreadManagementService, StatisticsService
from domain.entities.chat_message import ChatMessage, MessageRole
from datetime import datetime

async def test_microservices():
    """Test all SQLite microservices"""
    print("🚀 Testing SQLite Microservices Architecture")
    print("=" * 50)
    
    # Initialize repository with microservices
    repo = SqliteChatRepository("test_microservices.db")
    
    print("✅ Repository initialized with microservices")
    
    # Test CRUD Service
    print("\n📝 Testing CRUD Service...")
    test_message = ChatMessage(
        content="Hello from microservices!",
        role=MessageRole.USER,
        message_id="test_msg_1",
        thread_id="test_thread_1",
        timestamp=datetime.now()
    )
    
    # Save message
    result = await repo.crud_service.save_message(test_message)
    print(f"Save message: {'✅' if result.is_success else '❌'}")
    
    # Get message
    result = await repo.crud_service.get_message_by_id("test_msg_1")
    print(f"Get message: {'✅' if result.is_success else '❌'}")
    if result.is_success and result.value:
        print(f"  Message content: {result.value.content}")
    
    # Test Bulk Operations Service
    print("\n📦 Testing Bulk Operations Service...")
    bulk_messages = [
        ChatMessage(content=f"Bulk message {i}", role=MessageRole.USER, message_id=f"bulk_{i}", thread_id="bulk_thread", timestamp=datetime.now())
        for i in range(1, 4)
    ]
    
    result = await repo.bulk_service.save_messages_bulk(bulk_messages)
    print(f"Bulk save: {'✅' if result.is_success else '❌'}")
    
    # Test Search Service
    print("\n🔍 Testing Search Service...")
    result = await repo.search_service.search_messages("Bulk")
    print(f"Search messages: {'✅' if result.is_success else '❌'}")
    if result.is_success:
        print(f"  Found {len(result.value)} messages")
    
    # Test Thread Management Service
    print("\n🧵 Testing Thread Management Service...")
    result = await repo.thread_service.get_messages_by_thread("bulk_thread")
    print(f"Get thread messages: {'✅' if result.is_success else '❌'}")
    if result.is_success:
        print(f"  Thread has {len(result.value)} messages")
    
    # Test Statistics Service
    print("\n📊 Testing Statistics Service...")
    result = await repo.stats_service.get_message_count()
    print(f"Get message count: {'✅' if result.is_success else '❌'}")
    if result.is_success:
        print(f"  Total messages: {result.value}")
    
    # Test Facade (main repository)
    print("\n🎭 Testing Facade Pattern...")
    result = await repo.get_conversation_stats()
    print(f"Get conversation stats: {'✅' if result.is_success else '❌'}")
    if result.is_success:
        stats = result.value
        print(f"  Total messages: {stats.get('total_messages', 0)}")
        print(f"  Total threads: {stats.get('total_threads', 0)}")
    
    # Test Health Check
    print("\n🏥 Testing Health Check...")
    result = await repo.health_check()
    print(f"Health check: {'✅' if result.is_success else '❌'}")
    if result.is_success:
        health = result.value
        print(f"  Status: {health['status']}")
        print(f"  Architecture: {health['architecture']}")
        print(f"  Services: {len(health['services'])}")
    
    print("\n🎉 All microservices tests completed!")
    
    # Cleanup
    import os
    if os.path.exists("test_microservices.db"):
        os.remove("test_microservices.db")
        print("🧹 Test database cleaned up")

if __name__ == "__main__":
    asyncio.run(test_microservices())
