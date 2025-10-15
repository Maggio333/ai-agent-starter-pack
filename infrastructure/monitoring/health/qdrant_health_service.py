# infrastructure/monitoring/health/qdrant_health_service.py
import time
import logging
from typing import Dict, Any
from datetime import datetime
from domain.utils.result import Result
from .base_health_service import BaseHealthService, HealthCheck, HealthStatus
from ...ai.vector_db.qdrant_service import QdrantService

class QdrantHealthService(BaseHealthService):
    """Health service for Qdrant vector database"""
    
    def __init__(self, qdrant_service: QdrantService):
        super().__init__("QdrantService")
        self.qdrant_service = qdrant_service
        self.logger = logging.getLogger(__name__)
    
    async def check_health(self) -> Result[HealthCheck, str]:
        """Check Qdrant service health"""
        start_time = time.time()
        
        try:
            # Test collection info
            collection_info_result = await self.qdrant_service.get_collection_info()
            
            response_time_ms = (time.time() - start_time) * 1000
            
            if collection_info_result.is_success:
                collection_info = collection_info_result.value
                
                # Test search functionality
                search_start = time.time()
                search_result = await self.qdrant_service.search("health check test", limit=1)
                search_time_ms = (time.time() - search_start) * 1000
                
                health_check = HealthCheck(
                    service_name=self.service_name,
                    status=HealthStatus.HEALTHY,
                    message="Qdrant service is healthy",
                    timestamp=datetime.now(),
                    response_time_ms=response_time_ms,
                    details={
                        "collection_info": collection_info,
                        "search_test": {
                            "success": search_result.is_success,
                            "response_time_ms": search_time_ms,
                            "results_count": len(search_result.value) if search_result.is_success else 0
                        },
                        "url": self.qdrant_service.url,
                        "collection_name": self.qdrant_service.collection_name,
                        "vector_size": self.qdrant_service.vector_size
                    }
                )
                
                self.logger.info(f"Qdrant service health check passed: {response_time_ms:.2f}ms")
                return Result.success(health_check)
            else:
                health_check = HealthCheck(
                    service_name=self.service_name,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Qdrant service failed: {collection_info_result.error}",
                    timestamp=datetime.now(),
                    response_time_ms=response_time_ms,
                    details={
                        "error": collection_info_result.error,
                        "url": self.qdrant_service.url,
                        "collection_name": self.qdrant_service.collection_name
                    }
                )
                
                self.logger.error(f"Qdrant service health check failed: {collection_info_result.error}")
                return Result.success(health_check)
                
        except Exception as e:
            response_time_ms = (time.time() - start_time) * 1000
            
            health_check = HealthCheck(
                service_name=self.service_name,
                status=HealthStatus.UNHEALTHY,
                message=f"Qdrant service exception: {str(e)}",
                timestamp=datetime.now(),
                response_time_ms=response_time_ms,
                details={
                    "exception": str(e),
                    "exception_type": type(e).__name__,
                    "url": self.qdrant_service.url,
                    "collection_name": self.qdrant_service.collection_name
                }
            )
            
            self.logger.error(f"Qdrant service health check exception: {e}")
            return Result.success(health_check)
    
    async def get_service_info(self) -> Dict[str, Any]:
        """Get Qdrant service information"""
        base_info = await super().get_service_info()
        
        base_info.update({
            "url": self.qdrant_service.url,
            "collection_name": self.qdrant_service.collection_name,
            "vector_size": self.qdrant_service.vector_size,
            "has_embedding_service": self.qdrant_service.embedding_service_provider is not None
        })
        
        try:
            # Get collection stats
            stats_result = await self.qdrant_service.get_stats()
            if stats_result.is_success:
                base_info["collection_stats"] = stats_result.value
        except Exception as e:
            base_info["stats_error"] = str(e)
        
        return base_info
