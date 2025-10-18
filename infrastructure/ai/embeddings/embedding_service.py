# infrastructure/ai/embeddings/embedding_service.py
import logging
from typing import List, Dict, Any, Optional
from domain.utils.result import Result
from .IEmbeddingService import IEmbeddingService
from .google_embedding_service import GoogleEmbeddingService
from .openai_embedding_service import OpenAIEmbeddingService
from .local_embedding_service import LocalEmbeddingService

class EmbeddingService(IEmbeddingService):
    """Facade for embedding services with provider selection"""
    
    def __init__(self, provider: str = "local", **kwargs):
        super().__init__()
        self.provider = provider
        self.logger = logging.getLogger(__name__)
        
        # Initialize the selected provider
        if provider == "google":
            self.service = GoogleEmbeddingService(
                api_key=kwargs.get("api_key", ""),
                project_id=kwargs.get("project_id", ""),
                location=kwargs.get("location", "us-central1"),
                model_name=kwargs.get("model_name", "textembedding-gecko@001")
            )
        elif provider == "openai":
            self.service = OpenAIEmbeddingService(
                api_key=kwargs.get("api_key", ""),
                model_name=kwargs.get("model_name", "text-embedding-ada-002")
            )
        elif provider == "local":
            self.service = LocalEmbeddingService(
                model_name=kwargs.get("model_name", "local-tfidf"),
                dimension=kwargs.get("dimension", 384)
            )
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
        
        self.logger.info(f"EmbeddingService initialized with provider: {provider}")
    
    async def embed_text(self, text: str) -> Result[List[float], str]:
        """Embed single text using selected provider"""
        return await self.service.embed_text(text)
    
    async def embed_texts(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Embed multiple texts using selected provider"""
        return await self.service.embed_texts(texts)
    
    async def get_embedding_dimension(self) -> Result[int, str]:
        """Get embedding dimension"""
        return await self.service.get_embedding_dimension()
    
    async def health_check(self) -> Result[dict, str]:
        """Check service health"""
        try:
            health_result = await self.service.health_check()
            if health_result.is_success:
                health_data = health_result.value
                health_data['provider'] = self.provider
                health_data['facade'] = 'EmbeddingService'
                return Result.success(health_data)
            else:
                return health_result
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return Result.error(f"Health check failed: {str(e)}")
    
    def switch_provider(self, provider: str, **kwargs):
        """Switch to different embedding provider"""
        self.logger.info(f"Switching embedding provider from {self.provider} to {provider}")
        
        if provider == "google":
            self.service = GoogleEmbeddingService(
                api_key=kwargs.get("api_key", ""),
                project_id=kwargs.get("project_id", ""),
                location=kwargs.get("location", "us-central1"),
                model_name=kwargs.get("model_name", "textembedding-gecko@001")
            )
        elif provider == "openai":
            self.service = OpenAIEmbeddingService(
                api_key=kwargs.get("api_key", ""),
                model_name=kwargs.get("model_name", "text-embedding-ada-002")
            )
        elif provider == "local":
            self.service = LocalEmbeddingService(
                model_name=kwargs.get("model_name", "local-tfidf"),
                dimension=kwargs.get("dimension", 384)
            )
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")
        
        self.provider = provider
        self.logger.info(f"Successfully switched to provider: {provider}")
    
    async def compare_embeddings(self, text1: str, text2: str) -> Result[float, str]:
        """Compare similarity between two texts"""
        try:
            # Get embeddings for both texts
            embed1_result = await self.embed_text(text1)
            embed2_result = await self.embed_text(text2)
            
            if embed1_result.is_error:
                return embed1_result
            if embed2_result.is_error:
                return embed2_result
            
            # Calculate cosine similarity
            import numpy as np
            
            vec1 = np.array(embed1_result.value)
            vec2 = np.array(embed2_result.value)
            
            # Cosine similarity
            similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            
            return Result.success(float(similarity))
        except Exception as e:
            self.logger.error(f"Embedding comparison failed: {e}")
            return Result.error(f"Embedding comparison failed: {str(e)}")
    
    async def batch_compare(self, query_text: str, candidate_texts: List[str]) -> Result[List[float], str]:
        """Compare query text with multiple candidate texts"""
        try:
            # Get query embedding
            query_result = await self.embed_text(query_text)
            if query_result.is_error:
                return query_result
            
            # Get candidate embeddings
            candidates_result = await self.embed_texts(candidate_texts)
            if candidates_result.is_error:
                return candidates_result
            
            # Calculate similarities
            import numpy as np
            
            query_vec = np.array(query_result.value)
            similarities = []
            
            for candidate_vec in candidates_result.value:
                candidate_array = np.array(candidate_vec)
                similarity = np.dot(query_vec, candidate_array) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(candidate_array)
                )
                similarities.append(float(similarity))
            
            return Result.success(similarities)
        except Exception as e:
            self.logger.error(f"Batch comparison failed: {e}")
            return Result.error(f"Batch comparison failed: {str(e)}")
