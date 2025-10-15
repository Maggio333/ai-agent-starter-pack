# infrastructure/ai/embeddings/openai_embedding_service.py
import httpx
from typing import List, Dict, Any, Optional
from domain.utils.result import Result
from .base_embedding_service import BaseEmbeddingService

class OpenAIEmbeddingService(BaseEmbeddingService):
    """OpenAI embedding service"""
    
    def __init__(self, api_key: str, model_name: str = "text-embedding-ada-002"):
        super().__init__(model_name, dimension=1536)  # Ada-002 has 1536 dimensions
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
    
    async def embed_text(self, text: str) -> Result[List[float], str]:
        """Embed single text using OpenAI API"""
        self.logger.info(f"Embedding text: '{text[:50]}...'")
        
        if not self._validate_text(text):
            return Result.error("Invalid text input")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/embeddings"
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "input": text,
                    "model": self.model_name
                }
                
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if "data" in data and len(data["data"]) > 0:
                        embedding = data["data"][0]["embedding"]
                        self.logger.info(f"Successfully embedded text, dimension: {len(embedding)}")
                        return Result.success(embedding)
                    else:
                        return Result.error("No embedding data in response")
                else:
                    error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    return Result.error(error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "OpenAI embedding request timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def embed_texts(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Embed multiple texts using OpenAI API"""
        self.logger.info(f"Embedding {len(texts)} texts")
        
        if not self._validate_texts(texts):
            return Result.error("Invalid texts input")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                url = f"{self.base_url}/embeddings"
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "input": texts,
                    "model": self.model_name
                }
                
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if "data" in data:
                        embeddings = [item["embedding"] for item in data["data"]]
                        self.logger.info(f"Successfully embedded {len(embeddings)} texts")
                        return Result.success(embeddings)
                    else:
                        return Result.error("No embedding data in response")
                else:
                    error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    return Result.error(error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "OpenAI embedding request timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def get_embedding_dimension(self) -> Result[int, str]:
        """Get embedding dimension"""
        return Result.success(self.dimension)
