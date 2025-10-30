# services/orchestration_service.py
from typing import Dict, List, Optional, Any
from datetime import datetime
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.services.IOrchestrationService import IOrchestrationService
from .weather_service import WeatherService
from .time_service import TimeService
from .city_service import CityService
from .knowledge_service import KnowledgeService
from .conversation_service import ConversationService


class OrchestrationService(IOrchestrationService):
    """Microservice orchestrator that coordinates all other services"""
    
    def __init__(
        self,
        conversation_service: ConversationService,
        weather_service: WeatherService,
        time_service: TimeService,
        city_service: CityService,
        knowledge_service: KnowledgeService,
        rop_service: Optional[ROPService] = None
    ):
        """Initialize OrchestrationService with injected dependencies"""
        self.rop_service = rop_service if rop_service is not None else ROPService()
        self.conversation_service = conversation_service
        self.weather_service = weather_service
        self.time_service = time_service
        self.city_service = city_service
        self.knowledge_service = knowledge_service
        
        # Service registry for easy access
        self._services = {
            "weather": self.weather_service,
            "time": self.time_service,
            "city": self.city_service,
            "knowledge": self.knowledge_service,
            "conversation": self.conversation_service
        }
    
    async def process_city_request(self, city: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Advanced ROP pipeline with multiple validations and data sources"""
        try:
            city_lower = city.lower().strip()
            
            # Multi-step validation using ROP
            city_validator = self.rop_service.validate(
                lambda c: len(c.strip()) > 0 and len(c.strip()) < 100,
                "City name must be between 1 and 100 characters"
            )
            
            city_format_validator = self.rop_service.validate(
                lambda c: c.replace(" ", "").replace("-", "").isalpha(),
                "City name must contain only letters, spaces, and hyphens"
            )
            
            # Advanced pipeline with multiple data sources
            pipeline = self.rop_service.pipeline(
                city_validator,
                city_format_validator
            )
            
            validation_result = pipeline(city_lower)
            if validation_result.is_error:
                return validation_result
            
            # Gather city data (async operation)
            city_data_result = await self._gather_city_data(city_lower)
            if city_data_result.is_error:
                return city_data_result
            
            city_data = city_data_result.value
            
            # Save conversation if session_id provided
            if session_id:
                user_message = ChatMessage.create_user_message(
                    content=f"Tell me about {city}",
                    thread_id=session_id
                )
                
                assistant_message = ChatMessage.create_assistant_message(
                    content=f"Here's comprehensive information about {city.title()}: {city_data}",
                    thread_id=session_id,
                    parent_message_id=user_message.message_id
                )
                
                save_result = await self.conversation_service.save_conversation(
                    [user_message, assistant_message], session_id
                )
                if save_result.is_error:
                    # Log error but don't fail the main operation
                    print(f"Warning: Failed to save conversation: {save_result.error}")
            
            return Result.success(city_data)
            
        except Exception as e:
            return Result.error(f"Failed to process city request: {str(e)}")
    
    async def _gather_city_data(self, city: str) -> Result[Dict[str, Any], str]:
        """Gather data from all city-related services"""
        try:
            # Parallel data gathering using ROP
            weather_result = await self.weather_service.get_weather(city)
            time_result = await self.time_service.get_current_time(city)
            city_info_result = await self.city_service.get_city_info(city)
            knowledge_result = await self.knowledge_service.search_knowledge_base(city)
            
            # Combine results
            city_data = {
                "city": city.title(),
                "timestamp": datetime.now().isoformat(),
                "source": "Microservices Orchestration v1.0"
            }
            
            # Add weather data
            if weather_result.is_success:
                city_data["weather"] = weather_result.value
            else:
                city_data["weather_error"] = weather_result.error
            
            # Add time data
            if time_result.is_success:
                city_data["time"] = time_result.value
            else:
                city_data["time_error"] = time_result.error
            
            # Add city information
            if city_info_result.is_success:
                city_info = city_info_result.value
                city_data.update({
                    "population": city_info.get("population", "N/A"),
                    "country": city_info.get("country", "N/A"),
                    "currency": city_info.get("currency", "N/A"),
                    "coordinates": city_info.get("coordinates", {}),
                    "attractions": city_info.get("attractions", []),
                    "airports": city_info.get("airports", [])
                })
            else:
                city_data["city_info_error"] = city_info_result.error
            
            # Add knowledge base results
            if knowledge_result.is_success:
                city_data["knowledge"] = knowledge_result.value
            else:
                city_data["knowledge_error"] = knowledge_result.error
            
            return Result.success(city_data)
            
        except Exception as e:
            return Result.error(f"Failed to gather city data: {str(e)}")
    
    async def process_weather_request(self, city: str, request_type: str = "current") -> Result[Dict[str, Any], str]:
        """Process weather-related requests"""
        try:
            if request_type == "current":
                result = await self.weather_service.get_weather(city)
            elif request_type == "forecast":
                result = await self.weather_service.get_weather_forecast(city)
            elif request_type == "alerts":
                result = await self.weather_service.get_weather_alerts(city)
            elif request_type == "summary":
                result = await self.weather_service.get_weather_summary(city)
            else:
                return Result.error(f"Unsupported weather request type: {request_type}")
            
            return result
            
        except Exception as e:
            return Result.error(f"Failed to process weather request: {str(e)}")
    
    async def process_time_request(self, city: str, request_type: str = "current") -> Result[Dict[str, Any], str]:
        """Process time-related requests"""
        try:
            if request_type == "current":
                result = await self.time_service.get_current_time(city)
            elif request_type == "timezone":
                result = await self.time_service.get_timezone_info(city)
            elif request_type == "world_clock":
                result = await self.time_service.get_world_clock()
            else:
                return Result.error(f"Unsupported time request type: {request_type}")
            
            return result
            
        except Exception as e:
            return Result.error(f"Failed to process time request: {str(e)}")
    
    async def process_knowledge_request(self, query: str, request_type: str = "search", limit: int = 5) -> Result[Dict[str, Any], str]:
        """Process knowledge base requests"""
        try:
            if request_type == "search":
                result = await self.knowledge_service.search_knowledge_base(query, limit=limit)
            elif request_type == "add":
                result = await self.knowledge_service.add_knowledge(query)
            elif request_type == "stats":
                result = await self.knowledge_service.get_knowledge_stats()
            elif request_type == "topics":
                result = await self.knowledge_service.search_similar_topics(query)
            else:
                return Result.error(f"Unsupported knowledge request type: {request_type}")
            
            return result
            
        except Exception as e:
            return Result.error(f"Failed to process knowledge request: {str(e)}")
    
    async def process_request(self, request: str, thread_id: str = None) -> Result[Dict[str, Any], str]:
        """Process a general request by analyzing and routing to appropriate services"""
        try:
            # Simple request analysis and routing
            request_lower = request.lower()
            
            if "weather" in request_lower:
                # Extract city from request
                city = "new york"  # Default city
                if "krakow" in request_lower or "kraków" in request_lower:
                    city = "krakow"
                elif "warsaw" in request_lower or "warszawa" in request_lower:
                    city = "warsaw"
                elif "gdansk" in request_lower or "gdańsk" in request_lower:
                    city = "gdansk"
                elif "new york" in request_lower:
                    city = "new york"
                elif "london" in request_lower:
                    city = "london"
                elif "tokyo" in request_lower:
                    city = "tokyo"
                elif "paris" in request_lower:
                    city = "paris"
                elif "sydney" in request_lower:
                    city = "sydney"
                elif "moscow" in request_lower:
                    city = "moscow"
                
                return await self.process_weather_request(city)
            
            elif "time" in request_lower:
                city = "New York"  # Default city
                if "krakow" in request_lower or "kraków" in request_lower:
                    city = "Krakow"
                elif "warsaw" in request_lower or "warszawa" in request_lower:
                    city = "Warsaw"
                elif "gdansk" in request_lower or "gdańsk" in request_lower:
                    city = "Gdansk"
                elif "london" in request_lower:
                    city = "London"
                elif "tokyo" in request_lower:
                    city = "Tokyo"
                elif "sydney" in request_lower:
                    city = "Sydney"
                elif "moscow" in request_lower:
                    city = "Moscow"
                
                return await self.process_time_request(city)
            
            elif "city" in request_lower or "location" in request_lower:
                city = "Warsaw"  # Default city
                if "krakow" in request_lower or "kraków" in request_lower:
                    city = "Krakow"
                elif "warsaw" in request_lower or "warszawa" in request_lower:
                    city = "Warsaw"
                elif "gdansk" in request_lower or "gdańsk" in request_lower:
                    city = "Gdansk"
                
                return await self.process_city_request(city)
            
            elif "knowledge" in request_lower or "search" in request_lower or "find" in request_lower:
                return await self.process_knowledge_request(request)
            
            else:
                # Default to conversation processing
                return await self.process_conversation_request("start", context={"request": request, "thread_id": thread_id})
            
        except Exception as e:
            return Result.error(f"Failed to process request: {str(e)}")
    
    async def process_conversation_request(self, request_type: str, **kwargs) -> Result[Dict[str, Any], str]:
        """Process conversation-related requests"""
        try:
            if request_type == "start":
                context = kwargs.get("context", {})
                result = await self.conversation_service.start_conversation(context)
            elif request_type == "history":
                session_id = kwargs.get("session_id")
                limit = kwargs.get("limit", 50)
                result = await self.conversation_service.get_conversation_history(session_id, limit)
            elif request_type == "end":
                session_id = kwargs.get("session_id")
                result = await self.conversation_service.end_conversation(session_id)
            elif request_type == "stats":
                result = await self.conversation_service.get_conversation_stats()
            elif request_type == "active_sessions":
                result = await self.conversation_service.get_active_sessions()
            else:
                return Result.error(f"Unsupported conversation request type: {request_type}")
            
            return result
            
        except Exception as e:
            return Result.error(f"Failed to process conversation request: {str(e)}")
    
    async def get_service_health(self) -> Result[Dict[str, Any], str]:
        """Get health status of all services"""
        try:
            health_status = {}
            
            for service_name, service in self._services.items():
                try:
                    # Try to call a simple method on each service
                    if hasattr(service, 'get_supported_cities'):
                        result = await service.get_supported_cities()
                        health_status[service_name] = {
                            "status": "healthy" if result.is_success else "unhealthy",
                            "error": result.error if result.is_error else None
                        }
                    else:
                        health_status[service_name] = {
                            "status": "healthy",
                            "error": None
                        }
                except Exception as e:
                    health_status[service_name] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }
            
            overall_status = "healthy" if all(
                status["status"] == "healthy" for status in health_status.values()
            ) else "unhealthy"
            
            return Result.success({
                "overall_status": overall_status,
                "services": health_status,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return Result.error(f"Failed to get service health: {str(e)}")
    
    async def get_service_capabilities(self) -> Result[Dict[str, List[str]], str]:
        """Get capabilities of all services"""
        try:
            capabilities = {
                "weather_service": [
                    "get_weather", "get_weather_forecast", "get_weather_alerts", 
                    "get_weather_summary", "get_supported_cities", "is_city_supported"
                ],
                "time_service": [
                    "get_current_time", "get_timezone_info", "convert_time",
                    "get_world_clock", "get_time_difference", "get_supported_cities", "is_city_supported"
                ],
                "city_service": [
                    "get_city_info", "search_cities", "get_city_coordinates",
                    "get_city_attractions", "get_city_airports", "compare_cities",
                    "get_cities_by_country", "get_supported_cities", "is_city_supported"
                ],
                "knowledge_service": [
                    "search_knowledge_base", "add_knowledge", "get_knowledge_stats",
                    "get_topic_facts", "search_similar_topics", "create_rag_chunk",
                    "get_search_history", "clear_search_history", "export_knowledge_base"
                ],
                "conversation_service": [
                    "start_conversation", "save_conversation", "get_conversation_history",
                    "end_conversation", "get_session_info", "get_active_sessions",
                    "get_conversation_stats", "cleanup_inactive_sessions", "export_conversation",
                    "search_conversations"
                ],
                "orchestration_service": [
                    "process_city_request", "process_weather_request", "process_time_request",
                    "process_knowledge_request", "process_conversation_request",
                    "get_service_health", "get_service_capabilities"
                ]
            }
            
            return Result.success(capabilities)
            
        except Exception as e:
            return Result.error(f"Failed to get service capabilities: {str(e)}")
    
    def get_service(self, service_name: str):
        """Get a specific service by name"""
        return self._services.get(service_name)
    
    def list_services(self) -> List[str]:
        """List all available services"""
        return list(self._services.keys())
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            health_data = {
                'status': 'healthy',
                'service': self.__class__.__name__,
                'services_count': len(self._services),
                'available_services': list(self._services.keys())
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
