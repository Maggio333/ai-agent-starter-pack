# application/services/di_service.py
import logging
from typing import Optional
from application.container import Container
from domain.services.rop_service import ROPService
from domain.repositories.chat_repository import ChatRepository
from domain.services.llm_service import LLMService
from domain.services.vector_db_service import VectorDbService

class DIServiceInitializationError(Exception):
    """Custom exception for DI service initialization errors"""
    pass

class DIService:
    """Dependency Injection Service with enhanced error handling and logging"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing DI Service...")
        
        try:
            self.container = Container()
            self.container.wire(modules=[__name__])
            
            # Set default configuration
            self.container.config.database.path.from_env("DATABASE_PATH", default="chat.db")
            self.container.config.google.api_key.from_env("GOOGLE_API_KEY", default="")
            self.container.config.google.model.from_env("GOOGLE_MODEL", default="gemini-2.0-flash")
            self.container.config.google.project_id.from_env("GOOGLE_PROJECT_ID", default="")
            self.container.config.google.location.from_env("GOOGLE_LOCATION", default="us-central1")
            self.container.config.qdrant.url.from_env("QDRANT_URL", default="http://localhost:6333")
            self.container.config.qdrant.collection_name.from_env("QDRANT_COLLECTION", default="chat_collection")
            self.container.config.qdrant.api_key.from_env("QDRANT_API_KEY", default="")
            
            # Validate configuration
            self._validate_config()
            
            # Initialize lazy-loaded services
            self._rop_service: Optional[ROPService] = None
            self._chat_repository: Optional[ChatRepository] = None
            self._llm_service: Optional[LLMService] = None
            self._vector_db_service: Optional[VectorDbService] = None
            
            self.logger.info("DI Service initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize DI service: {e}")
            raise DIServiceInitializationError(f"Failed to initialize DI service: {e}")
    
    def _validate_config(self):
        """Validate required configuration"""
        if not self.container.config.google.api_key():
            self.logger.warning("GOOGLE_API_KEY not set - LLM service may not work properly")
        
        if not self.container.config.qdrant.url():
            self.logger.warning("QDRANT_URL not set - Vector DB service may not work properly")
        
        self.logger.info("Configuration validation completed")
    
    def get_rop_service(self) -> ROPService:
        """Get ROP Service instance with lazy loading"""
        if self._rop_service is None:
            self.logger.debug("Creating ROP Service instance")
            self._rop_service = self.container.rop_service()
        return self._rop_service
    
    def get_chat_repository(self) -> ChatRepository:
        """Get Chat Repository instance with lazy loading"""
        if self._chat_repository is None:
            self.logger.debug("Creating Chat Repository instance")
            self._chat_repository = self.container.chat_repository()
        return self._chat_repository
    
    def get_llm_service(self) -> LLMService:
        """Get LLM Service instance with lazy loading"""
        if self._llm_service is None:
            self.logger.debug("Creating LLM Service instance")
            self._llm_service = self.container.llm_service()
        return self._llm_service
    
    def get_vector_db_service(self) -> VectorDbService:
        """Get Vector DB Service instance with lazy loading"""
        if self._vector_db_service is None:
            self.logger.debug("Creating Vector DB Service instance")
            self._vector_db_service = self.container.vector_db_service()
        return self._vector_db_service
    
    def get_container(self) -> Container:
        """Get DI Container instance"""
        return self.container
    
    def reset_services(self):
        """Reset all lazy-loaded services (useful for testing)"""
        self.logger.info("Resetting all lazy-loaded services")
        self._rop_service = None
        self._chat_repository = None
        self._llm_service = None
        self._vector_db_service = None
    
    def get_service_status(self) -> dict:
        """Get status of all services"""
        return {
            "rop_service": self._rop_service is not None,
            "chat_repository": self._chat_repository is not None,
            "llm_service": self._llm_service is not None,
            "vector_db_service": self._vector_db_service is not None,
            "container_initialized": self.container is not None
        }
