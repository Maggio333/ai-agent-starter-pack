# tests/test_rop.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.utils.result import Result
from domain.services.rop_service import ROPService
from application.services.chat_agent_service import ChatAgentService

def test_result_success():
    """Test Result.success()"""
    result = Result.success("test")
    assert result.is_success
    assert result.value == "test"
    assert result.error is None

def test_result_error():
    """Test Result.error()"""
    result = Result.error("test error")
    assert result.is_error
    assert result.value is None
    assert result.error == "test error"

def test_result_map():
    """Test Result.map()"""
    result = Result.success("hello")
    mapped = result.map(lambda x: x.upper())
    assert mapped.is_success
    assert mapped.value == "HELLO"

def test_result_bind():
    """Test Result.bind()"""
    result = Result.success("hello")
    bound = result.bind(lambda x: Result.success(x.upper()))
    assert bound.is_success
    assert bound.value == "HELLO"

def test_get_weather_success():
    """Test get_weather with ROP"""
    agent = ChatAgentService()
    result = agent.get_weather("new york")
    assert result.is_success
    assert "sunny" in result.value

def test_get_weather_error():
    """Test get_weather error with ROP"""
    agent = ChatAgentService()
    result = agent.get_weather("warsaw")
    assert result.is_error
    assert "not available" in result.error

def test_process_city_request_success():
    """Test ROP pipeline success"""
    agent = ChatAgentService()
    result = agent.process_city_request("new york")
    assert result.is_success
    assert result.value["city"] == "New York"
    assert "weather" in result.value
    assert "time" in result.value

def test_process_city_request_error():
    """Test ROP pipeline error"""
    agent = ChatAgentService()
    result = agent.process_city_request("")
    assert result.is_error
    assert "empty" in result.error