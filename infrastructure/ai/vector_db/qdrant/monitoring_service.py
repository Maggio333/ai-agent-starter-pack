# infrastructure/ai/vector_db/qdrant/monitoring_service.py
from typing import Dict, Any, List
from domain.utils.result import Result
from .base_qdrant_service import BaseQdrantService

class MonitoringService(BaseQdrantService):
    """Service for monitoring Qdrant performance and health"""
    
    async def get_cluster_info(self) -> Result[Dict[str, Any], str]:
        """Get cluster information"""
        self.logger.info("Getting cluster information")
        
        result = await self._make_request("GET", "/cluster")
        
        if result.is_success:
            cluster_info = result.value.get("result", {})
            self.logger.info("Cluster information retrieved")
            return Result.success(cluster_info)
        else:
            self.logger.error(f"Failed to get cluster info: {result.error}")
            return result
    
    async def get_telemetry(self) -> Result[Dict[str, Any], str]:
        """Get telemetry data"""
        self.logger.info("Getting telemetry data")
        
        result = await self._make_request("GET", "/telemetry")
        
        if result.is_success:
            telemetry = result.value.get("result", {})
            self.logger.info("Telemetry data retrieved")
            return Result.success(telemetry)
        else:
            self.logger.error(f"Failed to get telemetry: {result.error}")
            return result
    
    async def get_collection_metrics(self, collection_name: str) -> Result[Dict[str, Any], str]:
        """Get collection metrics"""
        self.logger.info(f"Getting metrics for collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        # Get collection stats
        stats_result = await self._make_request("GET", f"/collections/{collection_name}/stats")
        if stats_result.is_error:
            return stats_result
        
        # Get collection info
        info_result = await self._make_request("GET", f"/collections/{collection_name}")
        if info_result.is_error:
            return info_result
        
        metrics = {
            "collection_name": collection_name,
            "stats": stats_result.value.get("result", {}),
            "info": info_result.value.get("result", {}),
            "timestamp": self._get_timestamp()
        }
        
        self.logger.info(f"Metrics retrieved for collection: {collection_name}")
        return Result.success(metrics)
    
    async def get_system_metrics(self) -> Result[Dict[str, Any], str]:
        """Get system-wide metrics"""
        self.logger.info("Getting system metrics")
        
        # Get cluster info
        cluster_result = await self.get_cluster_info()
        if cluster_result.is_error:
            return cluster_result
        
        # Get telemetry
        telemetry_result = await self.get_telemetry()
        if telemetry_result.is_error:
            return telemetry_result
        
        # List collections to get count
        collections_result = await self._make_request("GET", "/collections")
        collections_count = 0
        if collections_result.is_success:
            collections_count = len(collections_result.value.get("result", {}).get("collections", []))
        
        system_metrics = {
            "cluster": cluster_result.value,
            "telemetry": telemetry_result.value,
            "collections_count": collections_count,
            "timestamp": self._get_timestamp()
        }
        
        self.logger.info("System metrics retrieved")
        return Result.success(system_metrics)
    
    async def check_performance(self, collection_name: str, test_queries: int = 5) -> Result[Dict[str, Any], str]:
        """Check collection performance with test queries"""
        self.logger.info(f"Checking performance for collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        import time
        
        # Generate test vectors
        test_vectors = [[0.1] * 384 for _ in range(test_queries)]
        
        start_time = time.time()
        
        # Perform batch search
        search_result = await self._make_request("POST", f"/collections/{collection_name}/points/search/batch", {
            "searches": [
                {
                    "vector": vector,
                    "limit": 5,
                    "with_payload": True,
                    "with_vector": False
                }
                for vector in test_vectors
            ]
        })
        
        end_time = time.time()
        
        if search_result.is_error:
            return search_result
        
        performance_metrics = {
            "collection_name": collection_name,
            "test_queries": test_queries,
            "total_time_ms": (end_time - start_time) * 1000,
            "avg_time_per_query_ms": ((end_time - start_time) * 1000) / test_queries,
            "queries_per_second": test_queries / (end_time - start_time),
            "timestamp": self._get_timestamp()
        }
        
        self.logger.info(f"Performance check completed for {collection_name}: {performance_metrics['avg_time_per_query_ms']:.2f}ms per query")
        return Result.success(performance_metrics)
    
    async def get_health_summary(self) -> Result[Dict[str, Any], str]:
        """Get comprehensive health summary"""
        self.logger.info("Getting health summary")
        
        try:
            # Basic health check
            health_result = await self.health_check()
            if health_result.is_error:
                return health_result
            
            # Get system metrics
            system_result = await self.get_system_metrics()
            if system_result.is_error:
                return system_result
            
            # Get collections list
            collections_result = await self._make_request("GET", "/collections")
            collections = []
            if collections_result.is_success:
                collections = [col["name"] for col in collections_result.value.get("result", {}).get("collections", [])]
            
            health_summary = {
                "status": "healthy",
                "url": self.url,
                "collections": collections,
                "collections_count": len(collections),
                "system_metrics": system_result.value,
                "timestamp": self._get_timestamp()
            }
            
            self.logger.info(f"Health summary generated: {len(collections)} collections")
            return Result.success(health_summary)
            
        except Exception as e:
            self.logger.error(f"Failed to get health summary: {e}")
            return Result.error(f"Failed to get health summary: {str(e)}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
