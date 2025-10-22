# application/services/di_service.py
import logging
from typing import Optional, Dict, Any
from application.container import Container
from domain.services.rop_service import ROPService
from domain.repositories.chat_repository import ChatRepository
from domain.services.ILLMService import ILLMService
from domain.services.IVectorDbService import IVectorDbService
from domain.services.ITextCleanerService import ITextCleanerService
from domain.services.IDIService import IDIService
from domain.utils.result import Result
from infrastructure.config.services.config_service import ConfigService
from infrastructure.data.cache.memory_cache_service import MemoryCacheService
from infrastructure.data.search.search_factory import SearchFactory, SearchProvider
from infrastructure.monitoring.health import HealthService
from application.services.city_service import CityService
from application.services.weather_service import WeatherService
from application.services.time_service import TimeService
from application.services.knowledge_service import KnowledgeService
from application.services.conversation_service import ConversationService
from application.services.orchestration_service import OrchestrationService
from infrastructure.ai.embeddings.embedding_factory import EmbeddingFactory, EmbeddingProvider
from application.services.web_server_manager_service import WebServerManagerService

class DIServiceInitializationError(Exception):
    """Custom exception for DI service initialization errors"""
    pass

class DIService(IDIService):
    """Unified Dependency Injection Service - jedyny punkt dostępu do wszystkich serwisów"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Unified DI Service...")
        
        try:
            self.container = Container()
            self.container.wire(modules=[__name__])
            
            # Initialize lazy-loaded services
            self._rop_service: Optional[ROPService] = None
            self._chat_repository: Optional[ChatRepository] = None
            self._llm_service: Optional[ILLMService] = None
            self._vector_db_service: Optional[IVectorDbService] = None
            self._text_cleaner_service: Optional[ITextCleanerService] = None
            self._config_service: Optional[ConfigService] = None
            self._embedding_factory: Optional[EmbeddingFactory] = None
            self._embedding_service: Optional[Any] = None
            self._cache_service: Optional[MemoryCacheService] = None
            self._search_factory: Optional[SearchFactory] = None
            self._web_server_manager_service: Optional[WebServerManagerService] = None
            self._health_service: Optional[HealthService] = None
            self._city_service: Optional[CityService] = None
            self._weather_service: Optional[WeatherService] = None
            self._time_service: Optional[TimeService] = None
            self._knowledge_service: Optional[KnowledgeService] = None
            self._conversation_service: Optional[ConversationService] = None
            self._orchestration_service: Optional[OrchestrationService] = None
            
            # Auto-discover all services from Container
            self._auto_discover_services()
            
            self.logger.info("Unified DI Service initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize DI service: {e}")
            raise DIServiceInitializationError(f"Failed to initialize DI service: {e}")
    
    # ===== CORE SERVICES =====
    
    def get_rop_service(self) -> ROPService:
        """Get ROP Service instance with lazy loading"""
        if self._rop_service is None:
            self.logger.debug("Creating ROP Service instance")
            self._rop_service = self.container.rop_service()
        return self._rop_service
    
    def get_config_service(self) -> ConfigService:
        """Get Config Service instance with lazy loading"""
        if self._config_service is None:
            self.logger.debug("Creating Config Service instance")
            self._config_service = self.container.config_service()
        return self._config_service
    
    def get_text_cleaner_service(self) -> ITextCleanerService:
        """Get Text Cleaner Service instance with lazy loading"""
        if self._text_cleaner_service is None:
            self.logger.debug("Creating Text Cleaner Service instance")
            self._text_cleaner_service = self.container.text_cleaner_service()
        return self._text_cleaner_service
    
    # ===== EMBEDDING SERVICES =====
    
    def get_embedding_factory(self) -> EmbeddingFactory:
        """Get Embedding Factory instance with lazy loading"""
        if self._embedding_factory is None:
            self.logger.debug("Creating Embedding Factory instance")
            self._embedding_factory = self.container.embedding_factory()
        return self._embedding_factory
    
    def get_embedding_service(self) -> Any:
        """Get Embedding Service instance with lazy loading"""
        if self._embedding_service is None:
            self.logger.debug("Creating Embedding Service instance")
            self._embedding_service = self.container.embedding_service()
        return self._embedding_service
    
    # ===== CACHE SERVICES =====
    
    def get_cache_service(self) -> MemoryCacheService:
        """Get Cache Service instance with lazy loading"""
        if self._cache_service is None:
            self.logger.debug("Creating Cache Service instance")
            self._cache_service = self.container.cache_service()
        return self._cache_service
    
    # ===== SEARCH SERVICES =====
    
    def get_search_factory(self) -> SearchFactory:
        """Get Search Factory instance with lazy loading"""
        if self._search_factory is None:
            self.logger.debug("Creating Search Factory instance")
            self._search_factory = self.container.search_factory()
        return self._search_factory
    
    def get_search_service(self) -> Any:
        """Get Search Service instance with lazy loading"""
        if self._search_service is None:
            self.logger.debug("Creating Search Service instance")
            self._search_service = self.container.search_service()
        return self._search_service
    
    # ===== REPOSITORIES =====
    
    def get_chat_repository(self) -> ChatRepository:
        """Get Chat Repository instance with lazy loading"""
        if self._chat_repository is None:
            self.logger.debug("Creating Chat Repository instance")
            self._chat_repository = self.container.chat_repository()
        return self._chat_repository
    
    # ===== LLM SERVICES =====
    
    def get_llm_service(self) -> ILLMService:
        """Get LLM Service instance with lazy loading"""
        if self._llm_service is None:
            self.logger.debug("Creating LLM Service instance")
            self._llm_service = self.container.llm_service()
        return self._llm_service
    
    # ===== VECTOR DB SERVICES =====
    
    def get_vector_db_service(self) -> IVectorDbService:
        """Get Vector DB Service instance with lazy loading"""
        if self._vector_db_service is None:
            self.logger.debug("Creating Vector DB Service instance")
            self._vector_db_service = self.container.vector_db_service()
        return self._vector_db_service
    
    # ===== HEALTH SERVICES =====
    
    def get_health_service(self) -> HealthService:
        """Get Health Service instance with lazy loading"""
        if self._health_service is None:
            self.logger.debug("Creating Health Service instance")
            self._health_service = self.container.health_service()
        return self._health_service
    
    # ===== APPLICATION SERVICES =====
    
    def get_city_service(self) -> CityService:
        """Get City Service instance with lazy loading"""
        if self._city_service is None:
            self.logger.debug("Creating City Service instance")
            self._city_service = self.container.city_service()
        return self._city_service
    
    def get_weather_service(self) -> WeatherService:
        """Get Weather Service instance with lazy loading"""
        if self._weather_service is None:
            self.logger.debug("Creating Weather Service instance")
            self._weather_service = self.container.weather_service()
        return self._weather_service
    
    def get_time_service(self) -> TimeService:
        """Get Time Service instance with lazy loading"""
        if self._time_service is None:
            self.logger.debug("Creating Time Service instance")
            self._time_service = self.container.time_service()
        return self._time_service
    
    def get_knowledge_service(self) -> KnowledgeService:
        """Get Knowledge Service instance with lazy loading"""
        if self._knowledge_service is None:
            self.logger.debug("Creating Knowledge Service instance")
            self._knowledge_service = self.container.knowledge_service()
        return self._knowledge_service
    
    def get_conversation_service(self) -> ConversationService:
        """Get Conversation Service instance with lazy loading"""
        if self._conversation_service is None:
            self.logger.debug("Creating Conversation Service instance")
            self._conversation_service = self.container.conversation_service()
        return self._conversation_service
    
    def get_orchestration_service(self) -> OrchestrationService:
        """Get Orchestration Service instance with lazy loading"""
        if self._orchestration_service is None:
            self.logger.debug("Creating Orchestration Service instance")
            self._orchestration_service = self.container.orchestration_service()
        return self._orchestration_service
    
    # ===== CONTAINER ACCESS =====
    
    def get_container(self) -> Container:
        """Get DI Container instance (for backward compatibility)"""
        return self.container
    
    # ===== UTILITY METHODS =====
    
    def reset_services(self):
        """Reset all lazy-loaded services (useful for testing)"""
        self.logger.info("Resetting all lazy-loaded services")
        
        # Reset all discovered services
        container_attrs = [attr for attr in dir(self.container) 
                          if not attr.startswith('_') and not callable(getattr(self.container, attr))]
        
        for service_name in container_attrs:
            if service_name not in ['config']:
                if hasattr(self, f"_{service_name}"):
                    setattr(self, f"_{service_name}", None)
    
    def _auto_discover_services(self):
        """Automatycznie wykrywa wszystkie serwisy z Container"""
        import inspect
        
        # Pobierz wszystkie providers z Container
        container_providers = [attr for attr in dir(self.container) 
                             if not attr.startswith('_') and 
                             hasattr(getattr(self.container, attr), '__call__') and
                             attr not in ['config', 'dependencies', 'overridden', 'parent', 'parent_name', 'providers', 'wired_to_modules', 'wired_to_packages', 'wiring_config']]
        
        # Dla każdego serwisu stwórz metodę get_*
        for service_name in container_providers:
            method_name = f"get_{service_name}"
            if not hasattr(self, method_name):
                # Stwórz metodę dynamicznie
                def create_getter(name):
                    def getter():
                        if not hasattr(self, f"_{name}") or getattr(self, f"_{name}") is None:
                            self.logger.debug(f"Creating {name} instance")
                            setattr(self, f"_{name}", getattr(self.container, name)())
                        return getattr(self, f"_{name}")
                    return getter
                
                setattr(self, method_name, create_getter(service_name))
                # Dodaj do lazy-loaded services
                setattr(self, f"_{service_name}", None)
        
        self.logger.info(f"Auto-discovered {len(container_providers)} services: {container_providers}")
    
    def get_service_status(self) -> dict:
        """Get status of all services"""
        status = {"container_initialized": self.container is not None}
        
        # Check all discovered services
        container_attrs = [attr for attr in dir(self.container) 
                          if not attr.startswith('_') and not callable(getattr(self.container, attr))]
        
        for service_name in container_attrs:
            if service_name not in ['config']:
                if hasattr(self, f"_{service_name}"):
                    status[service_name] = getattr(self, f"_{service_name}") is not None
                else:
                    status[service_name] = False
        
        return status
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            health_data = {
                'status': 'healthy',
                'service': self.__class__.__name__,
                'container_initialized': self.container is not None,
                'services_count': len(self.get_service_status())
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
    
    def get_web_server_manager_service(self) -> WebServerManagerService:
        """Get web server manager service"""
        if self._web_server_manager_service is None:
            self._web_server_manager_service = self.container.web_server_manager_service()
        return self._web_server_manager_service
