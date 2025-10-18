# infrastructure/ai/embeddings/huggingface_embedding_service.py
import httpx
from typing import List, Dict, Any, Optional
from domain.utils.result import Result
from .IEmbeddingService import IEmbeddingService

class HuggingFaceEmbeddingService(IEmbeddingService):
    """Hugging Face embedding service (FREE)"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", 
                 api_token: Optional[str] = None):
        super().__init__(model_name, dimension=384)  # MiniLM has 384 dimensions
        self.api_token = api_token
        self.base_url = "https://api-inference.huggingface.co/models"
    
    async def create_embedding(self, text: str) -> Result[List[float], str]:
        """Create embedding for single text using HuggingFace"""
        return await self.embed_text(text)
    
    async def create_embeddings_batch(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Create embeddings for multiple texts using HuggingFace"""
        return await self.embed_texts(texts)
    
    async def get_model_info(self) -> Result[Dict[str, Any], str]:
        """Get model information"""
        info = {
            "provider": "HuggingFace",
            "model_name": self.model_name,
            "dimension": self.dimension,
            "type": "cloud",
            "cost": "free"
        }
        return Result.success(info)
    
    async def embed_text(self, text: str) -> Result[List[float], str]:
        """Embed single text using Hugging Face API (FREE)"""
        self.logger.info(f"Embedding text with HuggingFace: '{text[:50]}...'")
        
        if not self._validate_text(text):
            return Result.error("Invalid text input")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/{self.model_name}"
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                if self.api_token:
                    headers["Authorization"] = f"Bearer {self.api_token}"
                
                payload = {
                    "inputs": text
                }
                
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        embedding = data[0]
                        self.logger.info(f"Successfully embedded text with HuggingFace, dimension: {len(embedding)}")
                        return Result.success(embedding)
                    else:
                        return Result.error("No embedding data in response")
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    self.logger.warning("HuggingFace model is loading, retrying...")
                    await asyncio.sleep(5)
                    return await self.embed_text(text)  # Retry once
                else:
                    error_msg = f"HuggingFace API error: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    return Result.error(error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "HuggingFace embedding request timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def embed_texts(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Embed multiple texts using Hugging Face API (FREE)"""
        self.logger.info(f"Embedding {len(texts)} texts with HuggingFace")
        
        if not self._validate_texts(texts):
            return Result.error("Invalid texts input")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                url = f"{self.base_url}/{self.model_name}"
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                if self.api_token:
                    headers["Authorization"] = f"Bearer {self.api_token}"
                
                payload = {
                    "inputs": texts
                }
                
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        embeddings = data
                        self.logger.info(f"Successfully embedded {len(embeddings)} texts with HuggingFace")
                        return Result.success(embeddings)
                    else:
                        return Result.error("No embedding data in response")
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    self.logger.warning("HuggingFace model is loading, retrying...")
                    await asyncio.sleep(5)
                    return await self.embed_texts(texts)  # Retry once
                else:
                    error_msg = f"HuggingFace API error: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    return Result.error(error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "HuggingFace embedding request timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def get_embedding_dimension(self) -> Result[int, str]:
        """Get embedding dimension"""
        return Result.success(self.dimension)
