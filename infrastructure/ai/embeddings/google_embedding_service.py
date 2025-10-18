# infrastructure/ai/embeddings/google_embedding_service.py
import httpx
from typing import List, Dict, Any, Optional
from domain.utils.result import Result
from .IEmbeddingService import IEmbeddingService

class GoogleEmbeddingService(IEmbeddingService):
    """Google Vertex AI embedding service"""
    
    def __init__(self, api_key: str, project_id: str, location: str = "us-central1", 
                 model_name: str = "textembedding-gecko@001"):
        super().__init__(model_name, dimension=768)  # Gecko model has 768 dimensions
        self.api_key = api_key
        self.project_id = project_id
        self.location = location
        self.base_url = f"https://{location}-aiplatform.googleapis.com/v1"
    
    async def embed_text(self, text: str) -> Result[List[float], str]:
        """Embed single text using Google Vertex AI"""
        self.logger.info(f"Embedding text: '{text[:50]}...'")
        
        if not self._validate_text(text):
            return Result.error("Invalid text input")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}:predict"
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "instances": [
                        {
                            "content": text
                        }
                    ],
                    "parameters": {
                        "taskType": "RETRIEVAL_DOCUMENT"
                    }
                }
                
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if "predictions" in data and len(data["predictions"]) > 0:
                        embedding = data["predictions"][0]["embeddings"]["values"]
                        self.logger.info(f"Successfully embedded text, dimension: {len(embedding)}")
                        return Result.success(embedding)
                    else:
                        return Result.error("No predictions in response")
                else:
                    error_msg = f"Google API error: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    return Result.error(error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "Google embedding request timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def embed_texts(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Embed multiple texts using Google Vertex AI"""
        self.logger.info(f"Embedding {len(texts)} texts")
        
        if not self._validate_texts(texts):
            return Result.error("Invalid texts input")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                url = f"{self.base_url}/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}:predict"
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "instances": [
                        {
                            "content": text
                        }
                        for text in texts
                    ],
                    "parameters": {
                        "taskType": "RETRIEVAL_DOCUMENT"
                    }
                }
                
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if "predictions" in data:
                        embeddings = [
                            prediction["embeddings"]["values"] 
                            for prediction in data["predictions"]
                        ]
                        self.logger.info(f"Successfully embedded {len(embeddings)} texts")
                        return Result.success(embeddings)
                    else:
                        return Result.error("No predictions in response")
                else:
                    error_msg = f"Google API error: {response.status_code} - {response.text}"
                    self.logger.error(error_msg)
                    return Result.error(error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "Google embedding request timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def get_embedding_dimension(self) -> Result[int, str]:
        """Get embedding dimension"""
        return Result.success(self.dimension)
