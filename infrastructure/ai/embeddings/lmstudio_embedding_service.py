# infrastructure/ai/embeddings/lmstudio_embedding_service.py
import httpx
import logging
from typing import List, Dict, Any, Optional
from domain.utils.result import Result
from .IEmbeddingService import IEmbeddingService

class LMStudioEmbeddingService(IEmbeddingService):
    """LM Studio embedding service via proxy"""
    
    def __init__(self, proxy_url: str = "http://127.0.0.1:8123", model_name: str = "model:10"):
        super().__init__(model_name, dimension=1024)  # LM Studio model has 1024 dimensions
        self.proxy_url = proxy_url
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"LMStudioEmbeddingService initialized with proxy: {proxy_url}, model: {model_name}")
    
    async def create_embedding(self, text: str) -> Result[List[float], str]:
        """Create embedding for single text using LM Studio proxy"""
        return await self._create_embedding_single(text)
    
    async def create_embeddings_batch(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Create embeddings for multiple texts using LM Studio proxy"""
        embeddings = []
        for text in texts:
            result = await self._create_embedding_single(text)
            if result.is_error:
                return result
            embeddings.append(result.value)
        return Result.success(embeddings)
    
    async def get_model_info(self) -> Result[Dict[str, Any], str]:
        """Get model information"""
        info = {
            "provider": "LM Studio",
            "model_name": self.model_name,
            "dimension": self.dimension,
            "proxy_url": self.proxy_url,
            "type": "local_proxy",
            "cost": "free"
        }
        return Result.success(info)
    
    async def _create_embedding_single(self, text: str) -> Result[List[float], str]:
        """Create embedding for single text"""
        safe_text = text[:50].encode('utf-8', errors='ignore').decode('utf-8')
        self.logger.info(f"LMStudioEmbeddingService - Creating embedding with LM Studio: '{safe_text}...'")
        
        if not text or not text.strip():
            return Result.error("Text cannot be empty")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.proxy_url}/v1/embeddings"
                
                request_body = {
                    "model": self.model_name,
                    "input": text
                }
                
                self.logger.info(f"LMStudioEmbeddingService - Sending request to: {url}")
                
                response = await client.post(url, json=request_body)
                
                if response.status_code == 200:
                    data = response.json()
                    self.logger.info(f"LMStudioEmbeddingService - Response received: {response.status_code}")
                    
                    if 'data' in data and len(data['data']) > 0:
                        embedding = data['data'][0]['embedding']
                        self.logger.info(f"LMStudioEmbeddingService - Embedding created successfully, dimension: {len(embedding)}")
                        return Result.success(embedding)
                    else:
                        error_msg = "No embedding data in response"
                        self.logger.error(f"LMStudioEmbeddingService - {error_msg}")
                        return Result.error(error_msg)
                else:
                    error_msg = f"LM Studio API error: {response.status_code} - {response.text}"
                    safe_error_msg = error_msg.encode('utf-8', errors='ignore').decode('utf-8')
                    self.logger.error(f"LMStudioEmbeddingService - {safe_error_msg}")
                    return Result.error(safe_error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "LM Studio API timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except httpx.RequestError as e:
            error_msg = f"LM Studio API request error: {e}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"LM Studio embedding creation failed: {e}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def health_check(self) -> Result[dict, str]:
        """Check service health"""
        try:
            # Test with simple text
            result = await self.create_embedding("health check")
            
            if result.is_success:
                return Result.success({
                    "status": "healthy",
                    "provider": "LM Studio",
                    "model": self.model_name,
                    "proxy_url": self.proxy_url,
                    "dimension": len(result.value)
                })
            else:
                return Result.error(f"Health check failed: {result.error}")
                
        except Exception as e:
            return Result.error(f"Health check failed: {e}")
