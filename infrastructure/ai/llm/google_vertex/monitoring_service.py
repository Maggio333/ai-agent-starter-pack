# infrastructure/llm/google_vertex/monitoring_service.py
import httpx
import time
from typing import List, Dict, Any
from domain.utils.result import Result
from .base_vertex_service import BaseVertexService

class MonitoringService(BaseVertexService):
    """Google Vertex AI service for monitoring and health checks"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        super().__init__(api_key, model)
        self._error_history = []
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"X-Goog-Api-Key": self.api_key}
                )
                
                health_data = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "api_status": response.status_code,
                    "model": self.model,
                    "timestamp": time.time()
                }
                
                return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
    
    async def get_error_history(self) -> Result[List[Dict[str, Any]], str]:
        """Get error history"""
        try:
            return Result.success(self._error_history.copy())
        except Exception as e:
            return Result.error(f"Failed to get error history: {str(e)}")
    
    async def clear_error_history(self) -> Result[None, str]:
        """Clear error history"""
        try:
            self._error_history.clear()
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to clear error history: {str(e)}")
    
    async def get_performance_metrics(self) -> Result[Dict[str, Any], str]:
        """Get performance metrics"""
        try:
            metrics = {
                "total_requests": 0,  # Would be injected from usage stats
                "average_response_time": 0.5,  # Placeholder
                "cache_hit_rate": 0.0,
                "error_rate": len(self._error_history) / max(1, 1)  # Would use actual request count
            }
            return Result.success(metrics)
        except Exception as e:
            return Result.error(f"Failed to get performance metrics: {str(e)}")
    
    def log_error(self, error: str, context: Dict[str, Any] = None):
        """Log error to history"""
        error_entry = {
            "error": error,
            "context": context or {},
            "timestamp": time.time()
        }
        self._error_history.append(error_entry)
