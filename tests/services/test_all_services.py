# tests/services/test_all_services.py
import sys
sys.path.append('.')
import asyncio
from application.services.weather_service import WeatherService
from application.services.time_service import TimeService
from application.services.city_service import CityService
from application.services.knowledge_service import KnowledgeService
from application.services.conversation_service import ConversationService
from application.services.orchestration_service import OrchestrationService
from tests.services.test_conversation_service import MockChatRepository
from domain.utils.result import Result

async def test_weather_service():
    """Test Weather Service"""
    print("🌤️ Testing Weather Service...")
    weather_service = WeatherService()
    
    # Test successful weather retrieval
    result = await weather_service.get_weather("New York")
    assert result.is_success
    assert "sunny" in result.value.lower()
    
    # Test forecast
    result = await weather_service.get_weather_forecast("London", 2)
    assert result.is_success
    assert len(result.value) == 2
    
    # Test alerts
    result = await weather_service.get_weather_alerts("Moscow")
    assert result.is_success
    assert isinstance(result.value, list)
    
    print("✅ Weather Service tests passed!")

async def test_time_service():
    """Test Time Service"""
    print("⏰ Testing Time Service...")
    time_service = TimeService()
    
    # Test current time
    result = await time_service.get_current_time("New York")
    assert result.is_success
    assert isinstance(result.value, str)
    
    # Test timezone info
    result = await time_service.get_timezone_info("London")
    assert result.is_success
    assert "timezone" in result.value
    
    # Test world clock
    result = await time_service.get_world_clock()
    assert result.is_success
    assert isinstance(result.value, list)
    assert len(result.value) > 0
    
    print("✅ Time Service tests passed!")

async def test_city_service():
    """Test City Service"""
    print("🏙️ Testing City Service...")
    city_service = CityService()
    
    # Test city info
    result = await city_service.get_city_info("New York")
    assert result.is_success
    assert "population" in result.value
    assert "country" in result.value
    
    # Test search cities
    result = await city_service.search_cities("New")
    assert result.is_success
    assert len(result.value) > 0
    
    # Test coordinates
    result = await city_service.get_city_coordinates("London")
    assert result.is_success
    assert "lat" in result.value
    assert "lng" in result.value
    
    # Test attractions
    result = await city_service.get_city_attractions("Paris")
    assert result.is_success
    assert "Eiffel Tower" in result.value
    
    print("✅ City Service tests passed!")

async def test_knowledge_service():
    """Test Knowledge Service"""
    print("📚 Testing Knowledge Service...")
    knowledge_service = KnowledgeService()
    
    # Test search
    result = await knowledge_service.search_knowledge_base("artificial intelligence")
    assert result.is_success
    assert isinstance(result.value, list)
    
    # Test add knowledge
    result = await knowledge_service.add_knowledge("Test knowledge", {"topic": "test"})
    assert result.is_success
    
    # Test stats
    result = await knowledge_service.get_knowledge_stats()
    assert result.is_success
    assert "total_topics" in result.value
    
    # Test RAG chunk creation
    result = await knowledge_service.create_rag_chunk("Test text", 0.9, "test_source")
    assert result.is_success
    assert result.value.text_chunk == "Test text"
    
    print("✅ Knowledge Service tests passed!")

async def test_conversation_service():
    """Test Conversation Service"""
    print("💬 Testing Conversation Service...")
    mock_repo = MockChatRepository()
    conversation_service = ConversationService(mock_repo)
    
    # Test start conversation
    result = await conversation_service.start_conversation({"test": "context"})
    assert result.is_success
    session_id = result.value
    
    # Test get session info
    result = await conversation_service.get_session_info(session_id)
    assert result.is_success
    assert result.value["status"] == "active"
    
    # Test end conversation
    result = await conversation_service.end_conversation(session_id)
    assert result.is_success
    
    print("✅ Conversation Service tests passed!")

async def test_orchestration_service():
    """Test Orchestration Service"""
    print("🎭 Testing Orchestration Service...")
    mock_repo = MockChatRepository()
    conversation_service = ConversationService(mock_repo)
    orchestration_service = OrchestrationService(conversation_service)
    
    # Test city request processing
    result = await orchestration_service.process_city_request("New York")
    assert result.is_success
    city_data = result.value
    assert "city" in city_data
    assert "weather" in city_data
    assert "time" in city_data
    
    # Test weather request processing
    result = await orchestration_service.process_weather_request("London", "current")
    assert result.is_success
    assert isinstance(result.value, str)
    
    # Test time request processing
    result = await orchestration_service.process_time_request("Tokyo", "current")
    assert result.is_success
    assert isinstance(result.value, str)
    
    # Test knowledge request processing
    result = await orchestration_service.process_knowledge_request("AI", "search")
    assert result.is_success
    assert isinstance(result.value, list)
    
    # Test service health
    result = await orchestration_service.get_service_health()
    assert result.is_success
    assert "overall_status" in result.value
    
    # Test service capabilities
    result = await orchestration_service.get_service_capabilities()
    assert result.is_success
    assert isinstance(result.value, dict)
    
    print("✅ Orchestration Service tests passed!")

async def test_all_services():
    """Test all microservices"""
    print("🚀 Starting comprehensive microservices tests...\n")
    
    try:
        await test_weather_service()
        await test_time_service()
        await test_city_service()
        await test_knowledge_service()
        await test_conversation_service()
        await test_orchestration_service()
        
        print("\n🎉 ALL MICROSERVICES TESTS PASSED! 🎉")
        print("✅ Weather Service")
        print("✅ Time Service")
        print("✅ City Service")
        print("✅ Knowledge Service")
        print("✅ Conversation Service")
        print("✅ Orchestration Service")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_all_services())
    if success:
        print("\n🏆 MICROSERVICES ARCHITECTURE IS WORKING PERFECTLY! 🏆")
    else:
        print("\n💥 SOME TESTS FAILED!")
