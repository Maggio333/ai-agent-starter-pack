# infrastructure/llm/google_vertex/model_management_service.py
import httpx
from typing import List, Dict, Any
from domain.utils.result import Result
from .base_vertex_service import BaseVertexService

class ModelManagementService(BaseVertexService):
    """Google Vertex AI service for model management operations"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        super().__init__(api_key, model)
        self._current_model = model
    
    async def list_models(self) -> Result[List[Dict[str, Any]], str]:
        """List available models"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"X-Goog-Api-Key": self.api_key}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return Result.success(data.get("models", []))
                else:
                    return Result.error(f"API error: {response.status_code}")
        except Exception as e:
            return Result.error(f"Failed to list models: {str(e)}")
    
    async def get_model_info(self, model_name: str) -> Result[Dict[str, Any], str]:
        """Get model information"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models/{model_name}",
                    headers={"X-Goog-Api-Key": self.api_key}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return Result.success(data)
                else:
                    return Result.error(f"API error: {response.status_code}")
        except Exception as e:
            return Result.error(f"Failed to get model info: {str(e)}")
    
    async def set_model(self, model_name: str) -> Result[None, str]:
        """Set active model"""
        try:
            self._current_model = model_name
            self.model = model_name
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to set model: {str(e)}")
    
    async def get_current_model(self) -> Result[str, str]:
        """Get current active model"""
        try:
            return Result.success(self._current_model)
        except Exception as e:
            return Result.error(f"Failed to get current model: {str(e)}")
