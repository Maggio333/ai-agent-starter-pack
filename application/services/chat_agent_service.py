# application/services/chat_agent_service.py
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.entities.chat_message import ChatMessage, MessageRole
from application.services.orchestration_service import OrchestrationService
from application.services.conversation_service import ConversationService
from domain.repositories.chat_repository import ChatRepository
from domain.services.ILLMService import ILLMService
from domain.services.IVectorDbService import IVectorDbService

class ChatAgentService:
    """Advanced Agent with Microservices Architecture and sophisticated ROP patterns"""
    
    def __init__(self, 
                 rop_service: ROPService = None,
                 chat_repository: ChatRepository = None,
                 llm_service: ILLMService = None,
                 vector_db_service: IVectorDbService = None,
                 orchestration_service: OrchestrationService = None,
                 conversation_service: ConversationService = None):
        """Initialize with dependency injection"""
        self.rop_service = rop_service
        self.chat_repository = chat_repository
        self.llm_service = llm_service
        self.vector_db_service = vector_db_service
        self.conversation_service = conversation_service
        self.orchestration_service = orchestration_service
        
        # Service registry for easy access
        self._services = {}
        if self.orchestration_service:
            self._services.update({
                "weather": self.orchestration_service.weather_service,
                "time": self.orchestration_service.time_service,
                "city": self.orchestration_service.city_service,
                "knowledge": self.orchestration_service.knowledge_service,
            })
        if self.conversation_service:
            self._services["conversation"] = self.conversation_service
        if self.orchestration_service:
            self._services["orchestration"] = self.orchestration_service
    
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
    async def search_knowledge_base(self, query: str, limit: int = 5) -> Result[List[Dict[str, Any]], str]:
        """Search knowledge base using Knowledge Service"""
        return await self.orchestration_service.process_knowledge_request(query, "search", limit=limit)
    
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

# Note: ChatAgentService should be created via DI Container, not as global instance
