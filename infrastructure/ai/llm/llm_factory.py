# infrastructure/ai/llm/llm_factory.py
from typing import Dict, Any
from domain.services.ILLMService import ILLMService
from .google_vertex_service import GoogleVertexService
from .lmstudio_llm_service import LMStudioLLMService

class LLMProvider:
    """LLM provider types"""
    GOOGLE = "google"
    LMSTUDIO = "lmstudio"
    OLLAMA = "ollama"
    LOCAL = "local"

class LLMFactory:
    """Factory for creating LLM services"""
    
    @staticmethod
    def create_service(provider: str, **kwargs) -> ILLMService:
        """Create LLM service based on provider"""
        
        if provider == LLMProvider.GOOGLE:
            return GoogleVertexService(
                api_key=kwargs.get("api_key", ""),
                model=kwargs.get("model", "gemini-2.0-flash")
            )
        
        elif provider == LLMProvider.LMSTUDIO:
            return LMStudioLLMService(
                proxy_url=kwargs.get("proxy_url", "http://127.0.0.1:1234"),
                model_name=kwargs.get("model_name", "model:1")
            )
        
        elif provider == LLMProvider.OLLAMA:
            # TODO: Implement OllamaLLMService
            raise NotImplementedError("Ollama LLM service not implemented yet")
        
        elif provider == LLMProvider.LOCAL:
            # TODO: Implement LocalLLMService
            raise NotImplementedError("Local LLM service not implemented yet")
        
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    @staticmethod
    def get_supported_providers() -> list:
        """Get list of supported providers"""
        return [
            LLMProvider.GOOGLE,
            LLMProvider.LMSTUDIO,
            LLMProvider.OLLAMA,
            LLMProvider.LOCAL
        ]
