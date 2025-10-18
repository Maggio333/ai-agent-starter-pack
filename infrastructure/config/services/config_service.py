# infrastructure/config/services/config_service.py
import logging
import os
from typing import Dict, Any, Optional
from domain.utils.result import Result
from domain.services.IConfigService import IConfigService
from ..environment.env_loader import EnvironmentLoader

class ConfigService(IConfigService):
    """Service for managing application configuration and service selection"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_loader = EnvironmentLoader()
        self.logger = logging.getLogger(__name__)
        self._config_cache: Dict[str, Any] = {}
    
    def get_embedding_config(self) -> Dict[str, Any]:
        """Get embedding service configuration"""
        config = self.env_loader.get_config()
        provider = os.getenv("EMBEDDING_PROVIDER", "lmstudio")
        budget_preference = os.getenv("BUDGET_PREFERENCE", "free")
        
        result = {
            "provider": provider,
            "budget_preference": budget_preference
        }
        
        if provider == "huggingface":
            result.update({
                "model_name": os.getenv("HUGGINGFACE_MODEL_NAME", "all-MiniLM-L6-v2")
            })
        elif provider == "google":
            result.update({
                "api_key": config.api_keys.get("google_api_key"),
                "model": os.getenv("GOOGLE_MODEL", "textembedding-gecko@001"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID")
            })
        elif provider == "openai":
            result.update({
                "api_key": config.api_keys.get("openai_api_key"),
                "model": os.getenv("OPENAI_MODEL", "text-embedding-ada-002")
            })
        elif provider == "local":
            result.update({
                "model_path": os.getenv("LOCAL_MODEL_PATH"),
                "device": os.getenv("LOCAL_DEVICE", "auto")
            })
        elif provider == "lmstudio":
            result.update({
                "proxy_url": os.getenv("LMSTUDIO_PROXY_URL", "http://127.0.0.1:8123"),
                "model_name": os.getenv("LMSTUDIO_MODEL_NAME", "model:10")
            })
        
        return result
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM service configuration"""
        config = self.env_loader.get_config()
        provider = os.getenv("LLM_PROVIDER", "lmstudio")
        budget_preference = os.getenv("BUDGET_PREFERENCE", "free")
        
        result = {
            "provider": provider,
            "budget_preference": budget_preference
        }
        
        if provider == "google":
            result.update({
                "api_key": config.api_keys.get("google_api_key"),
                "model": os.getenv("GOOGLE_LLM_MODEL", "gemini-pro"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID")
            })
        elif provider == "openai":
            result.update({
                "api_key": config.api_keys.get("openai_api_key"),
                "model": os.getenv("OPENAI_LLM_MODEL", "gpt-3.5-turbo")
            })
        elif provider == "lmstudio":
            result.update({
                "proxy_url": os.getenv("LMSTUDIO_LLM_PROXY_URL", "http://127.0.0.1:1234"),
                "model_name": os.getenv("LMSTUDIO_LLM_MODEL_NAME", "model:1")
            })
        elif provider == "ollama":
            result.update({
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                "model": os.getenv("OLLAMA_MODEL", "llama2")
            })
        elif provider == "local":
            result.update({
                "model_path": os.getenv("LOCAL_LLM_MODEL_PATH")
            })
        
        return result
    
    def get_vector_db_config(self) -> Dict[str, Any]:
        """Get vector database configuration"""
        provider = self.env_loader.get("VECTOR_DB_PROVIDER", "qdrant")
        budget_preference = self.env_loader.get("BUDGET_PREFERENCE", "free")
        
        config = {
            "provider": provider,
            "budget_preference": budget_preference
        }
        
        if provider == "qdrant":
            config.update({
                "url": self.env_loader.get("QDRANT_URL", "http://localhost:6333"),
                "collection_name": self.env_loader.get("QDRANT_COLLECTION_NAME", "chat_collection"),
                "api_key": self.env_loader.get("QDRANT_API_KEY")
            })
        elif provider == "chroma":
            config.update({
                "persist_directory": self.env_loader.get("CHROMA_PERSIST_DIRECTORY", "./chroma_db"),
                "collection_name": self.env_loader.get("CHROMA_COLLECTION_NAME", "chat_collection")
            })
        elif provider == "faiss":
            config.update({
                "index_path": self.env_loader.get("FAISS_INDEX_PATH", "./faiss_index"),
                "index_type": self.env_loader.get("FAISS_INDEX_TYPE", "FlatL2")
            })
        elif provider == "pinecone":
            config.update({
                "api_key": self.env_loader.get("PINECONE_API_KEY"),
                "environment": self.env_loader.get("PINECONE_ENVIRONMENT"),
                "index_name": self.env_loader.get("PINECONE_INDEX_NAME", "chat_index")
            })
        
        return config
    
    def get_cache_config(self) -> Dict[str, Any]:
        """Get cache service configuration"""
        provider = self.env_loader.get("CACHE_PROVIDER", "memory")
        
        config = {"provider": provider}
        
        if provider == "redis":
            config.update({
                "host": self.env_loader.get("REDIS_HOST", "localhost"),
                "port": self.env_loader.get_int("REDIS_PORT", 6379),
                "password": self.env_loader.get("REDIS_PASSWORD"),
                "db": self.env_loader.get_int("REDIS_DB", 0)
            })
        elif provider == "memory":
            config.update({
                "size": self.env_loader.get_int("MEMORY_CACHE_SIZE", 1000),
                "ttl": self.env_loader.get_int("MEMORY_CACHE_TTL", 3600)
            })
        
        return config
    
    def get_search_config(self) -> Dict[str, Any]:
        """Get search service configuration"""
        provider = self.env_loader.get("SEARCH_PROVIDER", "local")
        budget_preference = self.env_loader.get("BUDGET_PREFERENCE", "free")
        
        config = {
            "provider": provider,
            "budget_preference": budget_preference
        }
        
        if provider == "local":
            config.update({
                "index_name": self.env_loader.get("LOCAL_SEARCH_INDEX", "default")
            })
        elif provider == "whoosh":
            config.update({
                "index_name": self.env_loader.get("WHOOSH_INDEX_NAME", "default"),
                "index_dir": self.env_loader.get("WHOOSH_INDEX_DIR", "./whoosh_index")
            })
        elif provider == "elasticsearch":
            config.update({
                "index_name": self.env_loader.get("ELASTICSEARCH_INDEX", "default"),
                "url": self.env_loader.get("ELASTICSEARCH_URL", "http://localhost:9200"),
                "api_key": self.env_loader.get("ELASTICSEARCH_API_KEY")
            })
        elif provider == "solr":
            config.update({
                "index_name": self.env_loader.get("SOLR_COLLECTION", "default"),
                "url": self.env_loader.get("SOLR_URL", "http://localhost:8983"),
                "api_key": self.env_loader.get("SOLR_API_KEY")
            })
        elif provider == "algolia":
            config.update({
                "index_name": self.env_loader.get("ALGOLIA_INDEX", "default"),
                "app_id": self.env_loader.get("ALGOLIA_APP_ID"),
                "api_key": self.env_loader.get("ALGOLIA_API_KEY")
            })
        
        return config
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        db_type = self.env_loader.get("DATABASE_TYPE", "sqlite")
        
        config = {"type": db_type}
        
        if db_type == "sqlite":
            config.update({
                "path": self.env_loader.get("DATABASE_PATH", "chat.db")
            })
        elif db_type == "postgresql":
            config.update({
                "host": self.env_loader.get("POSTGRES_HOST", "localhost"),
                "port": self.env_loader.get_int("POSTGRES_PORT", 5432),
                "database": self.env_loader.get("POSTGRES_DB", "chat_db"),
                "user": self.env_loader.get("POSTGRES_USER", "chat_user"),
                "password": self.env_loader.get("POSTGRES_PASSWORD")
            })
        
        return config
    
    def get_app_config(self) -> Dict[str, Any]:
        """Get application configuration"""
        return {
            "debug": self.env_loader.get_bool("DEBUG", False),
            "log_level": self.env_loader.get("LOG_LEVEL", "INFO"),
            "api_host": self.env_loader.get("API_HOST", "0.0.0.0"),
            "api_port": self.env_loader.get_int("API_PORT", 8000),
            "max_concurrent_requests": self.env_loader.get_int("MAX_CONCURRENT_REQUESTS", 10),
            "request_timeout": self.env_loader.get_int("REQUEST_TIMEOUT", 30),
            "batch_size": self.env_loader.get_int("BATCH_SIZE", 32),
            "embedding_batch_size": self.env_loader.get_int("EMBEDDING_BATCH_SIZE", 16)
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return {
            "secret_key": self.env_loader.get("SECRET_KEY"),
            "jwt_secret": self.env_loader.get("JWT_SECRET"),
            "encryption_key": self.env_loader.get("ENCRYPTION_KEY")
        }
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration"""
        return {
            "enable_metrics": self.env_loader.get_bool("ENABLE_METRICS", True),
            "metrics_port": self.env_loader.get_int("METRICS_PORT", 9090),
            "health_check_interval": self.env_loader.get_int("HEALTH_CHECK_INTERVAL", 30)
        }
    
    def validate_config(self) -> Result[None, str]:
        """Validate the current configuration"""
        try:
            # Check required configurations
            embedding_config = self.get_embedding_config()
            if embedding_config["provider"] in ["google", "openai"]:
                if not embedding_config.get("api_key"):
                    return Result.error(f"API key required for {embedding_config['provider']} embedding service")
            
            llm_config = self.get_llm_config()
            if llm_config["provider"] in ["google", "openai"]:
                if not llm_config.get("api_key"):
                    return Result.error(f"API key required for {llm_config['provider']} LLM service")
            
            vector_db_config = self.get_vector_db_config()
            if vector_db_config["provider"] == "pinecone":
                if not vector_db_config.get("api_key"):
                    return Result.error("API key required for Pinecone vector database")
            
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Configuration validation failed: {str(e)}")
    
    def get_recommended_config(self, budget: str = "free") -> Dict[str, str]:
        """Get recommended configuration based on budget"""
        if budget.lower() == "free":
            return {
                "embedding_provider": "huggingface",
                "llm_provider": "ollama",
                "vector_db_provider": "qdrant",
                "cache_provider": "memory",
                "database_type": "sqlite"
            }
        else:
            return {
                "embedding_provider": "google",
                "llm_provider": "google",
                "vector_db_provider": "pinecone",
                "cache_provider": "redis",
                "database_type": "postgresql"
            }
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self._config_cache.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value by key"""
        self._config_cache[key] = value
    
    def reload_config(self) -> Result[bool, str]:
        """Reload configuration from environment file"""
        try:
            self.env_loader.reload()
            self._config_cache.clear()
            self.logger.info("Configuration reloaded")
            return Result.success(True)
        except Exception as e:
            return Result.error(f"Failed to reload config: {str(e)}")
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            health_data = {
                'status': 'healthy',
                'service': self.__class__.__name__,
                'config_cache_size': len(self._config_cache),
                'environment_loaded': self.env_loader is not None
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
