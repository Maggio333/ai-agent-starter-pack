# infrastructure/monitoring/health/embedding_health_service.py
import time
import logging
from typing import Dict, Any
from datetime import datetime
from domain.utils.result import Result
from .IHealthService import IHealthService, HealthCheck, HealthStatus
from ...ai.embeddings.IEmbeddingService import IEmbeddingService

class EmbeddingHealthService(IHealthService):
    """Health service for embedding services"""
    
    def __init__(self, embedding_service: IEmbeddingService):
        super().__init__("EmbeddingService")
        self.embedding_service = embedding_service
        self.logger = logging.getLogger(__name__)
    
    async def check_health(self) -> Result[HealthCheck, str]:
        """Check embedding service health"""
        start_time = time.time()
        
        try:
            # Test embedding creation
            test_text = "Health check test"
            embedding_result = await self.embedding_service.create_embedding(test_text)
            
            response_time_ms = (time.time() - start_time) * 1000
            
            if embedding_result.is_success:
                embedding = embedding_result.value
                
                # Get model info
                model_info_result = await self.embedding_service.get_model_info()
                model_info = model_info_result.value if model_info_result.is_success else {}
                
                health_check = HealthCheck(
                    service_name=self.service_name,
                    status=HealthStatus.HEALTHY,
                    message="Embedding service is healthy",
                    timestamp=datetime.now(),
                    response_time_ms=response_time_ms,
                    details={
                        "embedding_dimension": len(embedding),
                        "model_info": model_info,
                        "test_text": test_text,
                        "first_embedding_values": embedding[:5] if len(embedding) >= 5 else embedding
                    }
                )
                
                self.logger.info(f"Embedding service health check passed: {response_time_ms:.2f}ms")
                return Result.success(health_check)
            else:
                health_check = HealthCheck(
                    service_name=self.service_name,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Embedding service failed: {embedding_result.error}",
                    timestamp=datetime.now(),
                    response_time_ms=response_time_ms,
                    details={
                        "error": embedding_result.error,
                        "test_text": test_text
                    }
                )
                
                self.logger.error(f"Embedding service health check failed: {embedding_result.error}")
                return Result.success(health_check)
                
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            
            health_check = HealthCheck(
                service_name=self.service_name,
                status=HealthStatus.UNHEALTHY,
                message=f"Embedding service exception: {str(e)}",
                timestamp=datetime.now(),
                response_time_ms=response_time_ms,
                details={
                    "exception": str(e),
                    "exception_type": type(e).__name__
                }
            )
            
            self.logger.error(f"Embedding service health check exception: {e}")
            return Result.success(health_check)
    
    async def get_service_info(self) -> Dict[str, Any]:
        """Get embedding service information"""
        base_info = await super().get_service_info()
        
        try:
            model_info_result = await self.embedding_service.get_model_info()
            if model_info_result.is_success:
                base_info.update({
                    "model_info": model_info_result.value,
                    "provider": model_info_result.value.get("provider", "unknown"),
                    "model_name": model_info_result.value.get("model_name", "unknown"),
                    "dimension": model_info_result.value.get("dimension", "unknown")
                })
        except Exception as e:
            base_info["model_info_error"] = str(e)
        
        return base_info
