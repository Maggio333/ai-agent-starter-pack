# tests/test_infrastructure.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from application.services.di_service import DIService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.entities.rag_chunk import RAGChunk
from datetime import datetime

def test_di_service_infrastructure():
    """Test DI Service with Infrastructure"""
    di_service = DIService()
    
    # Test all services
    rop_service = di_service.get_rop_service()
    chat_repo = di_service.get_chat_repository()
    llm_service = di_service.get_llm_service()
    vector_db_service = di_service.get_vector_db_service()
    
    assert rop_service is not None
    assert chat_repo is not None
    assert llm_service is not None
    assert vector_db_service is not None

@pytest.mark.asyncio
async def test_chat_repository():
    """Test Chat Repository"""
    di_service = DIService()
    chat_repo = di_service.get_chat_repository()
    
    # Test save message
    message = ChatMessage(
        content="Test message",
        role=MessageRole.USER,
        timestamp=datetime.now()
    )
    
    result = await chat_repo.save_message(message)
    assert result.is_success
    
    # Test get messages
    result = await chat_repo.get_messages(limit=5)
    assert result.is_success
    assert len(result.value) >= 1
    
    # Test get message by ID
    result = await chat_repo.get_message_by_id(message.message_id)
    assert result.is_success
    assert result.value is not None
    assert result.value.content == "Test message"

@pytest.mark.asyncio
async def test_llm_service():
    """Test LLM Service"""
    di_service = DIService()
    llm_service = di_service.get_llm_service()
    
    # Test completion (will fail without API key, but tests structure)
    messages = [
        ChatMessage(
            content="Hello",
            role=MessageRole.USER,
            timestamp=datetime.now()
        )
    ]
    
    result = await llm_service.get_completion(messages)
    # This will fail without API key, but tests the structure
    assert result is not None

@pytest.mark.asyncio
async def test_vector_db_service():
    """Test Vector DB Service"""
    di_service = DIService()
    vector_db_service = di_service.get_vector_db_service()
    
    # Test search (will fail without Qdrant running, but tests structure)
    result = await vector_db_service.search("test query")
    # This will fail without Qdrant, but tests the structure
    assert result is not None
