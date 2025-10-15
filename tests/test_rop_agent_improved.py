# tests/test_rop_agent_improved.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ChatAgent import ChatAgent, root_agent
from domain.entities.chat_message import ChatMessage, MessageRole
from datetime import datetime

def test_rop_agent_advanced_weather():
    """Test ROPAgent advanced weather functionality"""
    agent = ROPAgent()
    
    # Test all supported cities
    cities = ["new york", "london", "tokyo", "paris", "sydney", "moscow"]
    for city in cities:
        result = agent.get_weather(city)
        assert result.is_success
        assert "°C" in result.value or "°F" in result.value
    
    # Test error case
    result = agent.get_weather("warsaw")
    assert result.is_error
    assert "not available" in result.error
    assert "Supported cities" in result.error

def test_rop_agent_advanced_time():
    """Test ROPAgent advanced time functionality"""
    agent = ROPAgent()
    
    # Test all supported cities
    cities = ["new york", "london", "tokyo", "paris", "sydney", "moscow"]
    for city in cities:
        result = agent.get_current_time(city)
        assert result.is_success
        assert "2025" in result.value
    
    # Test error case
    result = agent.get_current_time("warsaw")
    assert result.is_error
    assert "not available" in result.error

def test_rop_agent_city_info():
    """Test ROPAgent city info functionality"""
    agent = ROPAgent()
    
    # Test city info
    result = agent.get_city_info("new york")
    assert result.is_success
    assert "population" in result.value
    assert "country" in result.value
    assert "currency" in result.value
    
    # Test error case
    result = agent.get_city_info("warsaw")
    assert result.is_error
    assert "not available" in result.error

def test_rop_agent_advanced_pipeline():
    """Test ROPAgent advanced pipeline"""
    agent = ROPAgent()
    
    # Test successful pipeline
    result = agent.process_city_request("new york")
    assert result.is_success
    assert result.value["city"] == "New York"
    assert "weather" in result.value
    assert "time" in result.value
    assert "population" in result.value
    assert "country" in result.value
    assert "currency" in result.value
    assert "timestamp" in result.value
    assert result.value["source"] == "ROP Agent v2.0"
    
    # Test validation error
    result = agent.process_city_request("")
    assert result.is_error
    assert "characters" in result.error
    
    # Test format validation error
    result = agent.process_city_request("123")
    assert result.is_error
    assert "letters" in result.error

def test_rop_agent_knowledge_base():
    """Test ROPAgent knowledge base search"""
    agent = ROPAgent()
    
    result = agent.search_knowledge_base("test query")
    assert result.is_success
    assert len(result.value) == 2
    assert "score" in result.value[0]
    assert "text" in result.value[0]

def test_rop_agent_root_agent():
    """Test Google ADK Agent"""
    assert root_agent.name == "rop_agent"
    assert root_agent.model == "gemini-2.0-flash"
    assert len(root_agent.tools) == 4  # 4 tools now
    assert "sophisticated" in root_agent.description.lower()
    assert "advanced" in root_agent.instruction.lower()
