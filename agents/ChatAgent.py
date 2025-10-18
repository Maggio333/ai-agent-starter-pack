# agents/ChatAgent.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from application.services.di_service import DIService
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.entities.chat_message import ChatMessage, MessageRole
from application.services.orchestration_service import OrchestrationService
from application.services.conversation_service import ConversationService

class ChatAgent:
    """Advanced Agent with Microservices Architecture and sophisticated ROP patterns"""
    
    def __init__(self):
        self.di_service = DIService()
        self.rop_service = self.di_service.get_rop_service()
        self.chat_repository = self.di_service.get_chat_repository()
        self.llm_service = self.di_service.get_llm_service()
        self.vector_db_service = self.di_service.get_vector_db_service()
        
        # Initialize microservices using DI service
        self.conversation_service = self.di_service.get_conversation_service()
        self.orchestration_service = self.di_service.get_orchestration_service()
        
        # Service registry for easy access
        self._services = {
            "weather": self.orchestration_service.weather_service,
            "time": self.orchestration_service.time_service,
            "city": self.orchestration_service.city_service,
            "knowledge": self.orchestration_service.knowledge_service,
            "conversation": self.conversation_service,
            "orchestration": self.orchestration_service
        }
    
    # Weather Service Methods
    async def get_weather(self, city: str) -> Result[str, str]:
        """Get current weather for a city using Weather Service"""
        return await self.orchestration_service.process_weather_request(city, "current")
    
    async def get_weather_forecast(self, city: str) -> Result[List[Dict], str]:
        """Get weather forecast for a city"""
        return await self.orchestration_service.process_weather_request(city, "forecast")
    
    async def get_weather_alerts(self, city: str) -> Result[List[str], str]:
        """Get weather alerts for a city"""
        return await self.orchestration_service.process_weather_request(city, "alerts")
    
    # Time Service Methods
    async def get_current_time(self, city: str) -> Result[str, str]:
        """Get current time for a city using Time Service"""
        return await self.orchestration_service.process_time_request(city, "current")
    
    async def get_timezone_info(self, city: str) -> Result[Dict[str, Any], str]:
        """Get timezone information for a city"""
        return await self.orchestration_service.process_time_request(city, "timezone")
    
    async def get_world_clock(self) -> Result[List[Dict[str, Any]], str]:
        """Get current time for all supported cities"""
        return await self.orchestration_service.process_time_request("", "world_clock")
    
    # City Service Methods
    async def get_city_info(self, city: str) -> Result[Dict[str, Any], str]:
        """Get comprehensive city information using City Service"""
        return await self.orchestration_service.city_service.get_city_info(city)
    
    async def search_cities(self, query: str) -> Result[List[Dict[str, Any]], str]:
        """Search cities by name or attributes"""
        return await self.orchestration_service.city_service.search_cities(query)
    
    async def get_city_attractions(self, city: str) -> Result[List[str], str]:
        """Get list of attractions for a city"""
        return await self.orchestration_service.city_service.get_city_attractions(city)
    
    async def compare_cities(self, city1: str, city2: str) -> Result[Dict[str, Any], str]:
        """Compare two cities"""
        return await self.orchestration_service.city_service.compare_cities(city1, city2)
    
    # Knowledge Service Methods
    async def search_knowledge_base(self, query: str) -> Result[List[Dict[str, Any]], str]:
        """Search knowledge base using Knowledge Service"""
        return await self.orchestration_service.process_knowledge_request(query, "search")
    
    async def add_knowledge(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Result[None, str]:
        """Add new knowledge to the knowledge base"""
        return await self.orchestration_service.knowledge_service.add_knowledge(content, metadata)
    
    async def get_knowledge_stats(self) -> Result[Dict[str, Any], str]:
        """Get knowledge base statistics"""
        return await self.orchestration_service.process_knowledge_request("", "stats")
    
    # Conversation Service Methods
    async def start_conversation(self, context: Optional[Dict[str, Any]] = None) -> Result[str, str]:
        """Start a new conversation session"""
        return await self.orchestration_service.process_conversation_request("start", context=context)
    
    async def get_conversation_history(self, session_id: str, limit: int = 50) -> Result[List[ChatMessage], str]:
        """Get conversation history for a session"""
        return await self.orchestration_service.process_conversation_request("history", session_id=session_id, limit=limit)
    
    async def end_conversation(self, session_id: str) -> Result[None, str]:
        """End a conversation session"""
        return await self.orchestration_service.process_conversation_request("end", session_id=session_id)
    
    async def get_conversation_stats(self) -> Result[Dict[str, Any], str]:
        """Get conversation statistics"""
        return await self.orchestration_service.process_conversation_request("stats")
    
    # Orchestration Methods
    async def process_city_request(self, city: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Advanced ROP pipeline with multiple validations and data sources using Orchestration Service"""
        return await self.orchestration_service.process_city_request(city, session_id)
    
    async def get_service_health(self) -> Result[Dict[str, Any], str]:
        """Get health status of all microservices"""
        return await self.orchestration_service.get_service_health()
    
    async def get_service_capabilities(self) -> Result[Dict[str, List[str]], str]:
        """Get capabilities of all microservices"""
        return await self.orchestration_service.get_service_capabilities()
    
    # Utility Methods
    def get_service(self, service_name: str):
        """Get a specific microservice by name"""
        return self._services.get(service_name)
    
    def list_services(self) -> List[str]:
        """List all available microservices"""
        return list(self._services.keys())
    
    async def save_conversation(self, messages: List[ChatMessage], session_id: Optional[str] = None) -> Result[None, str]:
        """Save conversation to repository using Conversation Service"""
        return await self.conversation_service.save_conversation(messages, session_id)

# Create agent instance
chat_agent_instance = ChatAgent()

# Create Google ADK Agent with all microservice capabilities
root_agent = Agent(
    name="microservices_chat_agent",
    model=LiteLlm(
        model="lm_studio/model:1",
        api_base="http://127.0.0.1:1234/v1"
    ),
    description="Advanced AI agent with Microservices Architecture, sophisticated ROP patterns, DI, Clean Architecture, and comprehensive city data services.",
    instruction="You are an advanced microservices-based agent who can answer complex questions about cities using sophisticated ROP patterns, multiple specialized services, and Clean Architecture principles. You have access to weather, time, city information, knowledge base, and conversation management services.",
    tools=[
        # Weather Service Tools
        chat_agent_instance.get_weather,
        chat_agent_instance.get_weather_forecast,
        chat_agent_instance.get_weather_alerts,
        
        # Time Service Tools
        chat_agent_instance.get_current_time,
        chat_agent_instance.get_timezone_info,
        chat_agent_instance.get_world_clock,
        
        # City Service Tools
        chat_agent_instance.get_city_info,
        chat_agent_instance.search_cities,
        chat_agent_instance.get_city_attractions,
        chat_agent_instance.compare_cities,
        
        # Knowledge Service Tools
        chat_agent_instance.search_knowledge_base,
        chat_agent_instance.add_knowledge,
        chat_agent_instance.get_knowledge_stats,
        
        # Conversation Service Tools
        chat_agent_instance.start_conversation,
        chat_agent_instance.get_conversation_history,
        chat_agent_instance.end_conversation,
        chat_agent_instance.get_conversation_stats,
        
        # Orchestration Tools
        chat_agent_instance.process_city_request,
        chat_agent_instance.get_service_health,
        chat_agent_instance.get_service_capabilities,
    ],
)
