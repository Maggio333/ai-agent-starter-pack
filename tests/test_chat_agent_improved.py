# tests/test_chat_agent_improved.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.ChatAgent import ChatAgent, root_agent

def test_chat_agent_class():
    """Test ChatAgent class"""
    agent = ChatAgent()
    
    # Test weather for multiple cities
    result = agent.get_weather("new york")
    assert result.is_success
    assert "sunny" in result.value
    
    result = agent.get_weather("london")
    assert result.is_success
    assert "cloudy" in result.value
    
    result = agent.get_weather("tokyo")
    assert result.is_success
    assert "rainy" in result.value
    
    result = agent.get_weather("paris")
    assert result.is_success
    assert "partly cloudy" in result.value
    
    # Test error case
    result = agent.get_weather("warsaw")
    assert result.is_error
    assert "not available" in result.error

def test_chat_agent_time():
    """Test ChatAgent time functionality"""
    agent = ChatAgent()
    
    # Test time for multiple cities
    result = agent.get_current_time("new york")
    assert result.is_success
    assert "2025" in result.value
    
    result = agent.get_current_time("london")
    assert result.is_success
    assert "2025" in result.value
    
    result = agent.get_current_time("tokyo")
    assert result.is_success
    assert "2025" in result.value
    
    result = agent.get_current_time("paris")
    assert result.is_success
    assert "2025" in result.value
    
    # Test error case
    result = agent.get_current_time("warsaw")
    assert result.is_error
    assert "not available" in result.error

def test_chat_agent_pipeline():
    """Test ChatAgent pipeline"""
    agent = ChatAgent()
    
    # Test successful pipeline
    result = agent.process_city_request("new york")
    assert result.is_success
    assert result.value["city"] == "New York"
    assert "weather" in result.value
    assert "time" in result.value
    assert "timestamp" in result.value
    
    # Test validation error
    result = agent.process_city_request("")
    assert result.is_error
    assert "characters" in result.error
    
    # Test city not found
    result = agent.process_city_request("warsaw")
    assert result.is_error

def test_root_agent():
    """Test Google ADK Agent"""
    assert root_agent.name == "chat_agent"
    assert root_agent.model == "gemini-2.0-flash"
    assert len(root_agent.tools) == 2
    assert "weather" in root_agent.description.lower()
    assert "time" in root_agent.description.lower()
