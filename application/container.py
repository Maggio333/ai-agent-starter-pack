# application/container.py
import logging
from typing import Optional, Dict, Any
from dependency_injector import containers, providers
from domain.services.rop_service import ROPService
from domain.repositories.chat_repository import ChatRepository
from domain.services.llm_service import LLMService
from domain.services.vector_db_service import VectorDbService
from infrastructure.data.storage.sqlite_chat_repository import SqliteChatRepository
from infrastructure.ai.llm.google_vertex_service import GoogleVertexService
from infrastructure.ai.vector_db.qdrant_service import QdrantService
from infrastructure.ai.embeddings.embedding_factory import EmbeddingFactory, EmbeddingProvider
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

class ContainerConfigurationError(Exception):
    """Custom exception for container configuration errors"""
    pass

class Container(containers.DeclarativeContainer):
    """Enhanced Dependency Injection Container with provider choice support"""
    
    # Configuration
    config = providers.Configuration()
    
    # Core Services
    rop_service = providers.Singleton(ROPService)
    config_service = providers.Singleton(ConfigService)
    
    # Embedding Services with Provider Choice
    embedding_factory = providers.Singleton(EmbeddingFactory)
    
    # Search Services with Provider Choice
    search_factory = providers.Singleton(SearchFactory)
    
    def _create_embedding_service():
        """Factory method to create embedding service based on config"""
        config_service = ConfigService()
        embedding_config = config_service.get_embedding_config()
        provider = embedding_config.get('provider', 'huggingface')
        
        factory = EmbeddingFactory()
        
        if provider == 'huggingface':
            return factory.create_service(
                EmbeddingProvider.HUGGINGFACE,
                model_name=embedding_config.get('model_name', 'all-MiniLM-L6-v2')
            )
        elif provider == 'google':
            return factory.create_service(
                EmbeddingProvider.GOOGLE,
                api_key=embedding_config.get('api_key'),
                model=embedding_config.get('model', 'textembedding-gecko@001')
            )
        elif provider == 'openai':
            return factory.create_service(
                EmbeddingProvider.OPENAI,
                api_key=embedding_config.get('api_key'),
                model=embedding_config.get('model', 'text-embedding-ada-002')
            )
        elif provider == 'local':
            return factory.create_service(
                EmbeddingProvider.LOCAL,
                model_path=embedding_config.get('model_path'),
                device=embedding_config.get('device', 'auto')
            )
        elif provider == 'lmstudio':
            return factory.create_service(
                EmbeddingProvider.LMSTUDIO,
                proxy_url=embedding_config.get('proxy_url', 'http://127.0.0.1:8123'),
                model_name=embedding_config.get('model_name', 'model:10')
            )
        else:
            # Fallback to LM Studio (our preferred local option)
            return factory.create_service(
                EmbeddingProvider.LMSTUDIO,
                proxy_url='http://127.0.0.1:8123',
                model_name='model:10'
            )
    
    embedding_service = providers.Singleton(_create_embedding_service)
    
    # Cache Services with Provider Choice
    def _create_cache_service():
        """Factory method to create cache service based on config"""
        config_service = ConfigService()
        cache_config = config_service.get_cache_config()
        provider = cache_config.get('provider', 'memory')
        
        if provider == 'memory':
            return MemoryCacheService(
                size=cache_config.get('size', 1000),
                ttl=cache_config.get('ttl', 3600)
            )
        elif provider == 'redis':
            # TODO: Implement RedisCacheService
            return MemoryCacheService()  # Fallback
        else:
            return MemoryCacheService()  # Default fallback
    
    cache_service = providers.Singleton(_create_cache_service)
    
    def _create_search_service():
        """Factory method to create search service based on config"""
        config_service = ConfigService()
        search_config = config_service.get_search_config()
        provider = search_config.get('provider', 'local')
        
        factory = SearchFactory()
        
        if provider == 'local':
            return factory.create_service(
                SearchProvider.LOCAL,
                index_name=search_config.get('index_name', 'default')
            )
        elif provider == 'whoosh':
            return factory.create_service(
                SearchProvider.WHOOSH,
                index_name=search_config.get('index_name', 'default'),
                index_dir=search_config.get('index_dir', './whoosh_index')
            )
        elif provider == 'elasticsearch':
            return factory.create_service(
                SearchProvider.ELASTICSEARCH,
                index_name=search_config.get('index_name', 'default'),
                url=search_config.get('url', 'http://localhost:9200'),
                api_key=search_config.get('api_key')
            )
        else:
            # Fallback to free option
            return factory.create_service(
                SearchProvider.LOCAL,
                index_name='default'
            )
    
    search_service = providers.Singleton(_create_search_service)
    
    # Repositories
    chat_repository = providers.Singleton(
        SqliteChatRepository,
        db_path=config.database.path
    )
    
    # LLM Services
    llm_service = providers.Singleton(
        GoogleVertexService,
        api_key=config.google.api_key,
        model=config.google.model
    )
    
    # Vector DB Services
    vector_db_service = providers.Singleton(
        QdrantService,
        url=config.qdrant.url,
        collection_name=config.qdrant.collection_name,
        embedding_service=embedding_service  # Inject embedding service
    )
    
    # Health Services
    health_service = providers.Singleton(HealthService)
    
    # Application Services
    city_service = providers.Singleton(CityService)
    weather_service = providers.Singleton(WeatherService)
    time_service = providers.Singleton(TimeService)
    knowledge_service = providers.Singleton(KnowledgeService)
    conversation_service = providers.Singleton(ConversationService, chat_repository)
    orchestration_service = providers.Singleton(OrchestrationService, conversation_service)

class ContainerManager:
    """Manager for Container with enhanced functionality"""
    
    def __init__(self):
        self.container = Container()
        self.logger = logging.getLogger(__name__)
        self._test_mode = False
        self._overrides: Dict[str, Any] = {}
        
        # Load configuration from .env file
        self.load_from_env()
    
    def load_from_env(self) -> None:
        """Load configuration from environment variables"""
        self.logger.info("Loading configuration from environment variables...")
        
        # Get config service to read environment variables
        config_service = ConfigService()
        
        # Load database configuration
        db_config = config_service.get_database_config()
        self.container.config.database.path.override(db_config.get('path', 'chat.db'))
        
        # Load Google configuration
        google_config = config_service.get_llm_config()
        self.container.config.google.api_key.override(google_config.get('api_key', ''))
        self.container.config.google.model.override(google_config.get('model', 'gemini-pro'))
        self.container.config.google.project_id.override(google_config.get('project_id', ''))
        self.container.config.google.location.override('us-central1')
        
        # Load Qdrant configuration
        qdrant_config = config_service.get_vector_db_config()
        self.container.config.qdrant.url.override(qdrant_config.get('url', 'http://localhost:6333'))
        self.container.config.qdrant.collection_name.override(qdrant_config.get('collection_name', 'chat_collection'))
        self.container.config.qdrant.api_key.override(qdrant_config.get('api_key', ''))
        
        self.logger.info("Configuration loaded from environment variables")
    
    def validate_configuration(self) -> None:
        """Validate required configuration parameters"""
        self.logger.info("Validating container configuration...")
        
        # Check required Google configuration
        if not self.container.config.google.api_key():
            self.logger.warning("GOOGLE_API_KEY not set - LLM service may not work")
        
        if not self.container.config.google.project_id():
            self.logger.warning("GOOGLE_PROJECT_ID not set - using default")
        
        if not self.container.config.google.location():
            self.logger.warning("GOOGLE_LOCATION not set - using default")
        
        # Check Qdrant configuration
        if not self.container.config.qdrant.url():
            self.logger.warning("QDRANT_URL not set - using default localhost")
        
        self.logger.info("Configuration validation completed")
    
    def set_test_mode(self, enabled: bool = True) -> None:
        """Enable test mode for easier testing"""
        self._test_mode = enabled
        self.logger.info(f"Test mode {'enabled' if enabled else 'disabled'}")
    
    def override_service(self, service_name: str, provider: Any) -> None:
        """Override a service for testing or special cases"""
        if hasattr(self.container, service_name):
            setattr(self.container, service_name, provider)
            self._overrides[service_name] = provider
            self.logger.info(f"Service '{service_name}' overridden")
        else:
            raise ValueError(f"Service '{service_name}' not found")
    
    def reset_overrides(self) -> None:
        """Reset all service overrides"""
        for service_name, original_provider in self._overrides.items():
            # Restore original provider (simplified - in real implementation you'd store originals)
            pass
        self._overrides.clear()
        self.logger.info("All service overrides reset")
    
    def get_service_status(self) -> Dict[str, bool]:
        """Get status of all registered services"""
        services = [
            'rop_service', 'config_service', 'embedding_factory', 'embedding_service',
            'cache_service', 'search_factory', 'search_service', 'chat_repository', 
            'llm_service', 'vector_db_service', 'health_service',
            'city_service', 'weather_service', 'time_service', 'knowledge_service',
            'conversation_service', 'orchestration_service'
        ]
        
        status = {}
        for service_name in services:
            try:
                service = getattr(self.container, service_name)
                # Try to get the service to check if it's properly configured
                service()
                status[service_name] = True
            except Exception as e:
                self.logger.warning(f"Service '{service_name}' not available: {e}")
                status[service_name] = False
        
        return status
    
    def configure_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Configure container from dictionary"""
        self.logger.info("Configuring container from dictionary")
        
        # Set configuration values
        for key, value in config_dict.items():
            if hasattr(self.container.config, key):
                getattr(self.container.config, key).override(value)
                self.logger.debug(f"Set config.{key} = {value}")
        
        # Validate after configuration
        self.validate_configuration()
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get summary of current configuration"""
        config_service = ConfigService()
        
        return {
            "database": {
                "path": self.container.config.database.path()
            },
            "google": {
                "api_key": "***" if self.container.config.google.api_key() else None,
                "model": self.container.config.google.model(),
                "project_id": self.container.config.google.project_id(),
                "location": self.container.config.google.location()
            },
            "qdrant": {
                "url": self.container.config.qdrant.url(),
                "collection_name": self.container.config.qdrant.collection_name(),
                "api_key": self.container.config.qdrant.api_key()
            },
                "embedding": config_service.get_embedding_config(),
                "cache": config_service.get_cache_config(),
                "search": config_service.get_search_config(),
                "llm": config_service.get_llm_config(),
                "vector_db": config_service.get_vector_db_config(),
            "test_mode": self._test_mode,
            "overrides_count": len(self._overrides)
        }
