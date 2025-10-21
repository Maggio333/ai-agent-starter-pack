# tests/test_di_rop.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.services.di_service import DIService
from domain.services.rop_service import ROPService
from application.services.chat_agent_service import ChatAgentService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.entities.rag_chunk import RAGChunk
from datetime import datetime

def test_di_service():
    """Test DI Service"""
    di_service = DIService()
    rop_service = di_service.get_rop_service()
    
    assert isinstance(rop_service, ROPService)
    assert di_service.get_container() is not None

def test_chat_agent():
    """Test Chat Agent with DI"""
    agent = ChatAgentService()
    
    # Test weather
    result = agent.get_weather("new york")
    assert result.is_success
    assert "sunny" in result.value
    
    # Test time
    result = agent.get_current_time("new york")
    assert result.is_success
    assert "2025" in result.value
    
    # Test pipeline
    result = agent.process_city_request("new york")
    assert result.is_success
    assert result.value["city"] == "New York"

def test_chat_message():
    """Test ChatMessage entity"""
    msg = ChatMessage(
        content="Hello world",
        role=MessageRole.USER,
        timestamp=datetime.now()
    )
    
    assert msg.content == "Hello world"
    assert msg.role == MessageRole.USER
    assert msg.message_id is not None
    
    # Test serialization
    data = msg.to_dict()
    assert data["content"] == "Hello world"
    assert data["role"] == "user"
    
    # Test deserialization
    msg2 = ChatMessage.from_dict(data)
    assert msg2.content == msg.content
    assert msg2.role == msg.role

def test_rag_chunk():
    """Test RAGChunk entity"""
    msg = ChatMessage(
        content="Test message",
        role=MessageRole.USER,
        timestamp=datetime.now()
    )
    
    chunk = RAGChunk(
        text_chunk="Test chunk",
        chat_messages=[msg],
        score=0.95
    )
    
    assert chunk.text_chunk == "Test chunk"
    assert len(chunk.chat_messages) == 1
    assert chunk.score == 0.95
    
    # Test serialization
    data = chunk.to_dict()
    assert data["text_chunk"] == "Test chunk"
    assert data["score"] == 0.95
    
    # Test deserialization
    chunk2 = RAGChunk.from_dict(data)
    assert chunk2.text_chunk == chunk.text_chunk
    assert chunk2.score == chunk.score
