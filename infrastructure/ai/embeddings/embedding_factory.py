# infrastructure/ai/embeddings/embedding_factory.py
import logging
from typing import Optional, Dict, Any
from domain.utils.result import Result
from .base_embedding_service import BaseEmbeddingService
from .huggingface_embedding_service import HuggingFaceEmbeddingService
from .google_embedding_service import GoogleEmbeddingService
from .openai_embedding_service import OpenAIEmbeddingService
from .local_embedding_service import LocalEmbeddingService
from .lmstudio_embedding_service import LMStudioEmbeddingService

class EmbeddingProvider:
    """Enum-like class for embedding providers"""
    HUGGINGFACE = "huggingface"
    GOOGLE = "google"
    OPENAI = "openai"
    LOCAL = "local"
    LMSTUDIO = "lmstudio"

class EmbeddingFactory:
    """Factory for creating embedding services based on configuration"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._services: Dict[str, BaseEmbeddingService] = {}
    
    def create_service(self, provider: str, **kwargs) -> Result[BaseEmbeddingService, str]:
        """
        Creates an embedding service based on the provider.
        
        Args:
            provider (str): The embedding provider to use
            **kwargs: Additional configuration parameters
            
        Returns:
            Result[BaseEmbeddingService, str]: The created service or error
        """
        try:
            if provider == EmbeddingProvider.HUGGINGFACE:
                model_name = kwargs.get('model_name', 'all-MiniLM-L6-v2')
                service = HuggingFaceEmbeddingService(model_name)
                self.logger.info(f"Created HuggingFace embedding service with model: {model_name}")
                
            elif provider == EmbeddingProvider.GOOGLE:
                api_key = kwargs.get('api_key')
                model = kwargs.get('model', 'textembedding-gecko@001')
                if not api_key:
                    return Result.error("Google API key is required")
                service = GoogleEmbeddingService(api_key, model)
                self.logger.info(f"Created Google embedding service with model: {model}")
                
            elif provider == EmbeddingProvider.OPENAI:
                api_key = kwargs.get('api_key')
                model = kwargs.get('model', 'text-embedding-ada-002')
                if not api_key:
                    return Result.error("OpenAI API key is required")
                service = OpenAIEmbeddingService(api_key, model)
                self.logger.info(f"Created OpenAI embedding service with model: {model}")
                
            elif provider == EmbeddingProvider.LOCAL:
                model_path = kwargs.get('model_path')
                if not model_path:
                    return Result.error("Local model path is required")
                service = LocalEmbeddingService(model_path)
                self.logger.info(f"Created local embedding service with model: {model_path}")
                
            elif provider == EmbeddingProvider.LMSTUDIO:
                proxy_url = kwargs.get('proxy_url', 'http://127.0.0.1:8123')
                model_name = kwargs.get('model_name', 'model:10')
                service = LMStudioEmbeddingService(proxy_url, model_name)
                self.logger.info(f"Created LM Studio embedding service with proxy: {proxy_url}, model: {model_name}")
                
            else:
                return Result.error(f"Unsupported embedding provider: {provider}")
            
            # Cache the service
            self._services[provider] = service
            return Result.success(service)
            
        except Exception as e:
            self.logger.error(f"Failed to create embedding service for provider {provider}: {e}")
            return Result.error(f"Failed to create embedding service: {str(e)}")
    
    def get_service(self, provider: str) -> Optional[BaseEmbeddingService]:
        """Get a cached service by provider"""
        return self._services.get(provider)
    
    def get_available_providers(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available providers"""
        return {
            EmbeddingProvider.HUGGINGFACE: {
                "name": "HuggingFace",
                "type": "free",
                "description": "Free local models using Sentence Transformers",
                "requirements": ["sentence-transformers"],
                "default_model": "all-MiniLM-L6-v2"
            },
            EmbeddingProvider.GOOGLE: {
                "name": "Google Vertex AI",
                "type": "paid",
                "description": "Google's embedding models via Vertex AI",
                "requirements": ["google-cloud-aiplatform"],
                "default_model": "textembedding-gecko@001"
            },
            EmbeddingProvider.OPENAI: {
                "name": "OpenAI",
                "type": "paid",
                "description": "OpenAI's embedding models",
                "requirements": ["openai"],
                "default_model": "text-embedding-ada-002"
            },
            EmbeddingProvider.LOCAL: {
                "name": "Local Model",
                "type": "free",
                "description": "Custom local embedding model",
                "requirements": ["torch", "transformers"],
                "default_model": "custom"
            },
            EmbeddingProvider.LMSTUDIO: {
                "name": "LM Studio",
                "type": "free",
                "description": "LM Studio embedding model via proxy",
                "requirements": ["httpx"],
                "default_model": "model:10",
                "proxy_url": "http://127.0.0.1:8123"
            }
        }
    
    def get_recommended_provider(self, budget: str = "free") -> str:
        """Get recommended provider based on budget"""
        if budget.lower() == "free":
            return EmbeddingProvider.HUGGINGFACE
        elif budget.lower() == "paid":
            return EmbeddingProvider.GOOGLE
        else:
            return EmbeddingProvider.HUGGINGFACE  # Default to free

# Global factory instance
embedding_factory = EmbeddingFactory()