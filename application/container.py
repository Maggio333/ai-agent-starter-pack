# application/container.py
import logging
from typing import Optional, Dict, Any
from dependency_injector import containers, providers
from domain.services.rop_service import ROPService
from domain.repositories.chat_repository import ChatRepository
from infrastructure.data.storage.sqlite_chat_repository import SqliteChatRepository
from infrastructure.ai.llm.llm_factory import LLMFactory, LLMProvider
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
from application.services.chat_agent_service import ChatAgentService
from application.services.user_session_service import UserSessionService
from application.services.conversation_analysis_agent import ConversationAnalysisAgent
from application.services.prompt_service import PromptService
from application.services.dynamic_rag_service import DynamicRAGService
from application.services.json_embedding_service import JSONEmbeddingService
from infrastructure.services.text_cleaner_service import TextCleanerService
from infrastructure.services.email_service import EmailService
from infrastructure.services.voice_service import VoiceService
from application.services.web_server_manager_service import WebServerManagerService

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container - używany przez DIService"""
    
    # Configuration
    config = providers.Configuration()
    
    # Core Services - Interface + Implementation pattern (jak w ChatElioraSystem)
    rop_service = providers.Singleton(ROPService)
    config_service = providers.Singleton(ConfigService)
    
    # Text Cleaner Service - Implementation only (interface is abstract in Python)
    text_cleaner_service = providers.Singleton(TextCleanerService)
    
    # Embedding Services with Provider Choice
    embedding_factory = providers.Singleton(EmbeddingFactory)
    
    # Search Services with Provider Choice
    search_factory = providers.Singleton(SearchFactory)
    
    def _create_embedding_service():
        """Factory method to create embedding service based on config"""
        import logging
        logger = logging.getLogger(__name__)
        
        config_service = ConfigService()
        embedding_config = config_service.get_embedding_config()
        provider = embedding_config.get('provider', 'lmstudio')  # Changed default to lmstudio
        
        logger.info(f"Creating embedding service with provider: {provider}, config: {embedding_config}")
        
        factory = EmbeddingFactory()
        
        if provider == 'huggingface':
            result = factory.create_service(
                EmbeddingProvider.HUGGINGFACE,
                model_name=embedding_config.get('model_name', 'all-MiniLM-L6-v2')
            )
        elif provider == 'google':
            result = factory.create_service(
                EmbeddingProvider.GOOGLE,
                api_key=embedding_config.get('api_key'),
                model=embedding_config.get('model', 'textembedding-gecko@001')
            )
        elif provider == 'openai':
            result = factory.create_service(
                EmbeddingProvider.OPENAI,
                api_key=embedding_config.get('api_key'),
                model=embedding_config.get('model', 'text-embedding-ada-002')
            )
        elif provider == 'local':
            result = factory.create_service(
                EmbeddingProvider.LOCAL,
                model_path=embedding_config.get('model_path'),
                device=embedding_config.get('device', 'auto')
            )
        elif provider == 'lmstudio':
            logger.info(f"Creating LM Studio embedding service with proxy_url: {embedding_config.get('proxy_url', 'http://127.0.0.1:8123')}, model_name: {embedding_config.get('model_name', 'model:10')}")
            result = factory.create_service(
                EmbeddingProvider.LMSTUDIO,
                proxy_url=embedding_config.get('proxy_url', 'http://127.0.0.1:8123'),
                model_name=embedding_config.get('model_name', 'model:10')
            )
        else:
            # Fallback to LM Studio (our preferred local option)
            result = factory.create_service(
                EmbeddingProvider.LMSTUDIO,
                proxy_url='http://127.0.0.1:8123',
                model_name='model:10'
            )
        
        # Handle Result object
        logger.info(f"Embedding service creation result: success={result.is_success}, error={result.error if result.is_error else None}")
        if result.is_success:
            logger.info(f"Successfully created embedding service: {type(result.value).__name__}")
            return result.value
        else:
            # Log error and return None (will cause fallback to dummy vectors)
            logger.error(f"Failed to create embedding service: {result.error}")
            return None
    
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
        db_path=config_service().get_database_config().get('path', 'chat.db')
    )
    
    # LLM Services with Provider Choice
    def _create_llm_service():
        """Factory method to create LLM service based on config"""
        config_service = ConfigService()
        llm_config = config_service.get_llm_config()
        provider = llm_config.get('provider', 'lmstudio')
        
        if provider == 'google':
            return LLMFactory.create_service(
                LLMProvider.GOOGLE,
                api_key=llm_config.get('api_key', ''),
                model=llm_config.get('model', 'gemini-2.0-flash')
            )
        elif provider == 'lmstudio':
            return LLMFactory.create_service(
                LLMProvider.LMSTUDIO,
                proxy_url=llm_config.get('proxy_url', 'http://127.0.0.1:8123'),
                model_name=llm_config.get('model_name', 'model:1')
            )
        elif provider == 'ollama':
            return LLMFactory.create_service(
                LLMProvider.OLLAMA,
                base_url=llm_config.get('base_url', 'http://localhost:11434'),
                model=llm_config.get('model', 'llama2')
            )
        else:
            # Fallback to LM Studio (local option)
            return LLMFactory.create_service(
                LLMProvider.LMSTUDIO,
                proxy_url='http://127.0.0.1:8123',
                model_name='model:1'
            )
    
    llm_service = providers.Singleton(_create_llm_service)
    
    # Vector DB Services
    # Użyj LOCAL_SEARCH_INDEX dla głównej kolekcji (dynamic RAG)
    # QDRANT_COLLECTION_NAME jest dla innych celów (opcjonalne)
    vector_db_service = providers.Singleton(
        QdrantService,
        url=config_service().get_vector_db_config().get('url', 'http://localhost:6333'),
        collection_name=config_service().get_search_config().get('index_name', 'PierwszaKolekcjaOnline'),
        embedding_service=embedding_service,  # Inject embedding service
        text_cleaner_service=text_cleaner_service  # Inject text cleaner service
    )
    
    # Health Services
    health_service = providers.Singleton(
        HealthService,
        embedding_service=embedding_service,
        vector_db_service=vector_db_service
    )
    
    # Application Services
    city_service = providers.Singleton(CityService)
    weather_service = providers.Singleton(WeatherService)
    time_service = providers.Singleton(TimeService)
    knowledge_service = providers.Singleton(KnowledgeService, vector_db_service, text_cleaner_service)
    conversation_service = providers.Singleton(ConversationService, chat_repository)
    orchestration_service = providers.Singleton(
        OrchestrationService,
        conversation_service=conversation_service,
        weather_service=weather_service,
        time_service=time_service,
        city_service=city_service,
        knowledge_service=knowledge_service,
        rop_service=rop_service
    )
    
    # Email Service - TYLKO JEDNA LINIA!
    email_service = providers.Singleton(EmailService)
    
    # Voice Service
    voice_service = providers.Singleton(VoiceService)
    
    # Web Server Manager Service
    web_server_manager_service = providers.Singleton(WebServerManagerService)
    
    # Chat Agent Service
    chat_agent_service = providers.Singleton(
        ChatAgentService,
        rop_service=rop_service,
        chat_repository=chat_repository,
        llm_service=llm_service,
        vector_db_service=vector_db_service,
        orchestration_service=orchestration_service,
        conversation_service=conversation_service
    )
    
    # Conversation Analysis Agent
    conversation_analysis_agent = providers.Singleton(
        ConversationAnalysisAgent,
        chat_agent_service=chat_agent_service
    )
    
    # Prompt Service - nowy serwis do budowania promptów
    prompt_service = providers.Singleton(
        PromptService,
        knowledge_service=knowledge_service
    )
    
    # JSON Embedding Service - obsługa JSON z modelu i embeddingów
    json_embedding_service = providers.Singleton(
        JSONEmbeddingService,
        embedding_service=embedding_service
    )
    
    # Dynamic RAG Service - nowy serwis do dynamicznego RAG
    dynamic_rag_service = providers.Singleton(
        DynamicRAGService,
        llm_service=llm_service,
        knowledge_service=knowledge_service,
        conversation_service=conversation_service,
        json_embedding_service=json_embedding_service  # Inject JSONEmbeddingService instead of creating it
    )
