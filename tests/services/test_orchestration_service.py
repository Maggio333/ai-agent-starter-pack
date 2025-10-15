# tests/services/test_orchestration_service.py
import sys
sys.path.append('.')
import pytest
import asyncio
from application.services.orchestration_service import OrchestrationService
from application.services.conversation_service import ConversationService
from tests.services.test_conversation_service import MockChatRepository
from domain.utils.result import Result

class TestOrchestrationService:
    """Test suite for Orchestration Service"""
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository for testing"""
        return MockChatRepository()
    
    @pytest.fixture
    def conversation_service(self, mock_repository):
        """Create ConversationService instance for testing"""
        return ConversationService(mock_repository)
    
    @pytest.fixture
    def orchestration_service(self, conversation_service):
        """Create OrchestrationService instance for testing"""
        return OrchestrationService(conversation_service)
    
    @pytest.mark.asyncio
    async def test_process_city_request_success(self, orchestration_service):
        """Test successful city request processing"""
        result = await orchestration_service.process_city_request("New York")
        
        assert result.is_success
        city_data = result.value
        assert "city" in city_data
        assert "timestamp" in city_data
        assert "source" in city_data
        assert city_data["city"] == "New York"
        assert city_data["source"] == "Microservices Orchestration v1.0"
    
    @pytest.mark.asyncio
    async def test_process_city_request_invalid_city(self, orchestration_service):
        """Test city request processing with invalid city"""
        result = await orchestration_service.process_city_request("InvalidCity")
        
        assert result.is_success  # Should still succeed but with error fields
        city_data = result.value
        assert "city" in city_data
        assert "weather_error" in city_data or "time_error" in city_data or "city_info_error" in city_data
    
    @pytest.mark.asyncio
    async def test_process_city_request_empty_city(self, orchestration_service):
        """Test city request processing with empty city"""
        result = await orchestration_service.process_city_request("")
        
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_process_city_request_with_session(self, orchestration_service):
        """Test city request processing with session ID"""
        # Start a conversation first
        start_result = await orchestration_service.conversation_service.start_conversation()
        session_id = start_result.value
        
        result = await orchestration_service.process_city_request("London", session_id)
        
        assert result.is_success
        city_data = result.value
        assert "city" in city_data
        assert city_data["city"] == "London"
    
    @pytest.mark.asyncio
    async def test_process_weather_request_current(self, orchestration_service):
        """Test weather request processing - current"""
        result = await orchestration_service.process_weather_request("Tokyo", "current")
        
        assert result.is_success
        weather = result.value
        assert isinstance(weather, str)
        assert "rainy" in weather.lower()
    
    @pytest.mark.asyncio
    async def test_process_weather_request_forecast(self, orchestration_service):
        """Test weather request processing - forecast"""
        result = await orchestration_service.process_weather_request("Paris", "forecast")
        
        assert result.is_success
        forecast = result.value
        assert isinstance(forecast, list)
        assert len(forecast) > 0
    
    @pytest.mark.asyncio
    async def test_process_weather_request_alerts(self, orchestration_service):
        """Test weather request processing - alerts"""
        result = await orchestration_service.process_weather_request("Moscow", "alerts")
        
        assert result.is_success
        alerts = result.value
        assert isinstance(alerts, list)
    
    @pytest.mark.asyncio
    async def test_process_weather_request_summary(self, orchestration_service):
        """Test weather request processing - summary"""
        result = await orchestration_service.process_weather_request("Sydney", "summary")
        
        assert result.is_success
        summary = result.value
        assert isinstance(summary, dict)
        assert "city" in summary
        assert "current_weather" in summary
    
    @pytest.mark.asyncio
    async def test_process_weather_request_invalid_type(self, orchestration_service):
        """Test weather request processing with invalid type"""
        result = await orchestration_service.process_weather_request("London", "invalid_type")
        
        assert result.is_error
        assert "Unsupported weather request type" in result.error
    
    @pytest.mark.asyncio
    async def test_process_time_request_current(self, orchestration_service):
        """Test time request processing - current"""
        result = await orchestration_service.process_time_request("New York", "current")
        
        assert result.is_success
        time_str = result.value
        assert isinstance(time_str, str)
        assert len(time_str) > 0
    
    @pytest.mark.asyncio
    async def test_process_time_request_timezone(self, orchestration_service):
        """Test time request processing - timezone"""
        result = await orchestration_service.process_time_request("London", "timezone")
        
        assert result.is_success
        tz_info = result.value
        assert isinstance(tz_info, dict)
        assert "timezone" in tz_info
    
    @pytest.mark.asyncio
    async def test_process_time_request_world_clock(self, orchestration_service):
        """Test time request processing - world clock"""
        result = await orchestration_service.process_time_request("", "world_clock")
        
        assert result.is_success
        world_times = result.value
        assert isinstance(world_times, list)
        assert len(world_times) > 0
    
    @pytest.mark.asyncio
    async def test_process_time_request_invalid_type(self, orchestration_service):
        """Test time request processing with invalid type"""
        result = await orchestration_service.process_time_request("Tokyo", "invalid_type")
        
        assert result.is_error
        assert "Unsupported time request type" in result.error
    
    @pytest.mark.asyncio
    async def test_process_knowledge_request_search(self, orchestration_service):
        """Test knowledge request processing - search"""
        result = await orchestration_service.process_knowledge_request("artificial intelligence", "search")
        
        assert result.is_success
        search_results = result.value
        assert isinstance(search_results, list)
    
    @pytest.mark.asyncio
    async def test_process_knowledge_request_add(self, orchestration_service):
        """Test knowledge request processing - add"""
        result = await orchestration_service.process_knowledge_request("Test knowledge content", "add")
        
        assert result.is_success
    
    @pytest.mark.asyncio
    async def test_process_knowledge_request_stats(self, orchestration_service):
        """Test knowledge request processing - stats"""
        result = await orchestration_service.process_knowledge_request("", "stats")
        
        assert result.is_success
        stats = result.value
        assert isinstance(stats, dict)
        assert "total_topics" in stats
    
    @pytest.mark.asyncio
    async def test_process_knowledge_request_topics(self, orchestration_service):
        """Test knowledge request processing - topics"""
        result = await orchestration_service.process_knowledge_request("AI", "topics")
        
        assert result.is_success
        topics = result.value
        assert isinstance(topics, list)
    
    @pytest.mark.asyncio
    async def test_process_knowledge_request_invalid_type(self, orchestration_service):
        """Test knowledge request processing with invalid type"""
        result = await orchestration_service.process_knowledge_request("test", "invalid_type")
        
        assert result.is_error
        assert "Unsupported knowledge request type" in result.error
    
    @pytest.mark.asyncio
    async def test_process_conversation_request_start(self, orchestration_service):
        """Test conversation request processing - start"""
        context = {"test": "context"}
        result = await orchestration_service.process_conversation_request("start", context=context)
        
        assert result.is_success
        session_id = result.value
        assert isinstance(session_id, str)
        assert session_id.startswith("session_")
    
    @pytest.mark.asyncio
    async def test_process_conversation_request_history(self, orchestration_service):
        """Test conversation request processing - history"""
        # Start a conversation first
        start_result = await orchestration_service.process_conversation_request("start")
        session_id = start_result.value
        
        result = await orchestration_service.process_conversation_request("history", session_id=session_id, limit=10)
        
        assert result.is_success
        history = result.value
        assert isinstance(history, list)
    
    @pytest.mark.asyncio
    async def test_process_conversation_request_end(self, orchestration_service):
        """Test conversation request processing - end"""
        # Start a conversation first
        start_result = await orchestration_service.process_conversation_request("start")
        session_id = start_result.value
        
        result = await orchestration_service.process_conversation_request("end", session_id=session_id)
        
        assert result.is_success
    
    @pytest.mark.asyncio
    async def test_process_conversation_request_stats(self, orchestration_service):
        """Test conversation request processing - stats"""
        result = await orchestration_service.process_conversation_request("stats")
        
        assert result.is_success
        stats = result.value
        assert isinstance(stats, dict)
        assert "total_sessions" in stats
    
    @pytest.mark.asyncio
    async def test_process_conversation_request_active_sessions(self, orchestration_service):
        """Test conversation request processing - active sessions"""
        result = await orchestration_service.process_conversation_request("active_sessions")
        
        assert result.is_success
        sessions = result.value
        assert isinstance(sessions, list)
    
    @pytest.mark.asyncio
    async def test_process_conversation_request_invalid_type(self, orchestration_service):
        """Test conversation request processing with invalid type"""
        result = await orchestration_service.process_conversation_request("invalid_type")
        
        assert result.is_error
        assert "Unsupported conversation request type" in result.error
    
    @pytest.mark.asyncio
    async def test_get_service_health(self, orchestration_service):
        """Test service health check"""
        result = await orchestration_service.get_service_health()
        
        assert result.is_success
        health = result.value
        assert "overall_status" in health
        assert "services" in health
        assert "timestamp" in health
        assert isinstance(health["services"], dict)
    
    @pytest.mark.asyncio
    async def test_get_service_capabilities(self, orchestration_service):
        """Test service capabilities retrieval"""
        result = await orchestration_service.get_service_capabilities()
        
        assert result.is_success
        capabilities = result.value
        assert isinstance(capabilities, dict)
        
        # Check that all services are listed
        expected_services = [
            "weather_service", "time_service", "city_service",
            "knowledge_service", "conversation_service", "orchestration_service"
        ]
        
        for service in expected_services:
            assert service in capabilities
            assert isinstance(capabilities[service], list)
            assert len(capabilities[service]) > 0
    
    @pytest.mark.asyncio
    async def test_get_service(self, orchestration_service):
        """Test getting specific service"""
        weather_service = orchestration_service.get_service("weather")
        assert weather_service is not None
        assert hasattr(weather_service, "get_weather")
        
        time_service = orchestration_service.get_service("time")
        assert time_service is not None
        assert hasattr(time_service, "get_current_time")
        
        city_service = orchestration_service.get_service("city")
        assert city_service is not None
        assert hasattr(city_service, "get_city_info")
        
        knowledge_service = orchestration_service.get_service("knowledge")
        assert knowledge_service is not None
        assert hasattr(knowledge_service, "search_knowledge_base")
        
        conversation_service = orchestration_service.get_service("conversation")
        assert conversation_service is not None
        assert hasattr(conversation_service, "start_conversation")
        
        orchestration_service_ref = orchestration_service.get_service("orchestration")
        assert orchestration_service_ref is not None
        assert orchestration_service_ref == orchestration_service
    
    @pytest.mark.asyncio
    async def test_get_service_invalid_name(self, orchestration_service):
        """Test getting service with invalid name"""
        service = orchestration_service.get_service("invalid_service")
        assert service is None
    
    @pytest.mark.asyncio
    async def test_list_services(self, orchestration_service):
        """Test listing all services"""
        services = orchestration_service.list_services()
        
        assert isinstance(services, list)
        assert len(services) == 6
        
        expected_services = [
            "weather", "time", "city", "knowledge", "conversation", "orchestration"
        ]
        
        for service in expected_services:
            assert service in services
    
    @pytest.mark.asyncio
    async def test_orchestration_service_performance(self, orchestration_service):
        """Test orchestration service performance"""
        import time
        
        start_time = time.time()
        
        # Make multiple requests
        tasks = [
            orchestration_service.process_city_request("New York"),
            orchestration_service.process_weather_request("London", "current"),
            orchestration_service.process_time_request("Tokyo", "current"),
            orchestration_service.process_knowledge_request("AI", "search"),
            orchestration_service.process_conversation_request("stats")
        ]
        
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # Should complete quickly (less than 2 seconds for 5 requests)
        assert duration < 2.0, f"Performance test failed: {duration:.2f}s for 5 requests"
    
    @pytest.mark.asyncio
    async def test_orchestration_service_concurrent_access(self, orchestration_service):
        """Test concurrent access to orchestration service"""
        # Test concurrent city requests
        tasks = [orchestration_service.process_city_request("London") for _ in range(3)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # Results should be consistent
        assert all(result.value == results[0].value for result in results)
    
    @pytest.mark.asyncio
    async def test_orchestration_service_error_handling(self, orchestration_service):
        """Test error handling in orchestration service"""
        # Test with None input
        result = await orchestration_service.process_city_request(None)
        assert result.is_error
        
        # Test with very long city name
        long_city = "A" * 200
        result = await orchestration_service.process_city_request(long_city)
        assert result.is_error
        assert "City name must be between 1 and 100 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_orchestration_service_data_consistency(self, orchestration_service):
        """Test data consistency across orchestration service"""
        city = "Paris"
        
        # Get city data through orchestration
        orchestration_result = await orchestration_service.process_city_request(city)
        assert orchestration_result.is_success
        
        # Get individual service data
        weather_result = await orchestration_service.process_weather_request(city, "current")
        time_result = await orchestration_service.process_time_request(city, "current")
        city_info_result = await orchestration_service.city_service.get_city_info(city)
        
        assert weather_result.is_success
        assert time_result.is_success
        assert city_info_result.is_success
        
        # Check consistency
        orchestration_data = orchestration_result.value
        assert orchestration_data["weather"] == weather_result.value
        assert orchestration_data["time"] == time_result.value
        assert orchestration_data["country"] == city_info_result.value["country"]
    
    @pytest.mark.asyncio
    async def test_orchestration_service_service_integration(self, orchestration_service):
        """Test integration between orchestration service and individual services"""
        # Test that orchestration service properly delegates to individual services
        city = "Tokyo"
        
        # Direct service call
        direct_weather = await orchestration_service.weather_service.get_weather(city)
        assert direct_weather.is_success
        
        # Orchestration service call
        orchestration_weather = await orchestration_service.process_weather_request(city, "current")
        assert orchestration_weather.is_success
        
        # Results should be the same
        assert direct_weather.value == orchestration_weather.value
    
    @pytest.mark.asyncio
    async def test_orchestration_service_comprehensive_city_data(self, orchestration_service):
        """Test comprehensive city data gathering"""
        city = "Sydney"
        
        result = await orchestration_service.process_city_request(city)
        assert result.is_success
        
        city_data = result.value
        
        # Check that all expected fields are present
        expected_fields = [
            "city", "timestamp", "source", "weather", "time",
            "population", "country", "currency", "coordinates",
            "attractions", "airports", "knowledge"
        ]
        
        for field in expected_fields:
            assert field in city_data, f"Missing field: {field}"
        
        # Check data quality
        assert city_data["city"] == "Sydney"
        assert city_data["source"] == "Microservices Orchestration v1.0"
        assert isinstance(city_data["coordinates"], dict)
        assert isinstance(city_data["attractions"], list)
        assert isinstance(city_data["airports"], list)
        assert isinstance(city_data["knowledge"], list)
