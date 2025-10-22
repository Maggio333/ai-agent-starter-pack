# infrastructure/monitoring/health/health_service.py
import logging
from typing import Dict, Any, List
from datetime import datetime
from domain.utils.result import Result
from .IHealthService import IHealthService, HealthCheck, HealthStatus
from .embedding_health_service import EmbeddingHealthService
from .qdrant_health_service import QdrantHealthService

class HealthService(IHealthService):
    """Main health service that coordinates all health checks"""
    
    def __init__(self):
        super().__init__("SystemHealth")
        self.logger = logging.getLogger(__name__)
        self._health_services: List[IHealthService] = []
    
    def register_service(self, health_service: IHealthService) -> None:
        """Register a health service"""
        self._health_services.append(health_service)
        self.logger.info(f"Registered health service: {health_service.service_name}")
    
    def register_embedding_service(self, embedding_service) -> None:
        """Register embedding service health check"""
        embedding_health = EmbeddingHealthService(embedding_service)
        self.register_service(embedding_health)
    
    def register_qdrant_service(self, qdrant_service) -> None:
        """Register Qdrant service health check"""
        qdrant_health = QdrantHealthService(qdrant_service)
        self.register_service(qdrant_health)
    
    async def check_health(self) -> Result[HealthCheck, str]:
        """Check overall system health"""
        start_time = datetime.now()
        
        try:
            # Run all health checks
            health_checks = []
            overall_status = HealthStatus.HEALTHY
            
            for service in self._health_services:
                try:
                    result = await service.check_health()
                    if result.is_success:
                        health_check = result.value
                        health_checks.append(health_check)
                        
                        # Determine overall status
                        if health_check.status == HealthStatus.UNHEALTHY:
                            overall_status = HealthStatus.UNHEALTHY
                        elif health_check.status == HealthStatus.DEGRADED and overall_status == HealthStatus.HEALTHY:
                            overall_status = HealthStatus.DEGRADED
                    else:
                        # Service check failed
                        failed_check = HealthCheck(
                            service_name=service.service_name,
                            status=HealthStatus.UNHEALTHY,
                            message=f"Health check failed: {result.error}",
                            timestamp=datetime.now(),
                            response_time_ms=0,
                            details={"error": result.error}
                        )
                        health_checks.append(failed_check)
                        overall_status = HealthStatus.UNHEALTHY
                        
                except Exception as e:
                    # Service check exception
                    failed_check = HealthCheck(
                        service_name=service.service_name,
                        status=HealthStatus.UNHEALTHY,
                        message=f"Health check exception: {str(e)}",
                        timestamp=datetime.now(),
                        response_time_ms=0,
                        details={"exception": str(e), "exception_type": type(e).__name__}
                    )
                    health_checks.append(failed_check)
                    overall_status = HealthStatus.UNHEALTHY
            
            # Calculate response time
            response_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # Determine message
            if overall_status == HealthStatus.HEALTHY:
                message = f"All {len(health_checks)} services are healthy"
            elif overall_status == HealthStatus.DEGRADED:
                message = f"Some services are degraded, {len(health_checks)} services checked"
            else:
                message = f"Some services are unhealthy, {len(health_checks)} services checked"
            
            # Create overall health check
            overall_health_check = HealthCheck(
                service_name=self.service_name,
                status=overall_status,
                message=message,
                timestamp=datetime.now(),
                response_time_ms=response_time_ms,
                details={
                    "total_services": len(self._health_services),
                    "checked_services": len(health_checks),
                    "healthy_services": len([h for h in health_checks if h.status == HealthStatus.HEALTHY]),
                    "unhealthy_services": len([h for h in health_checks if h.status == HealthStatus.UNHEALTHY]),
                    "degraded_services": len([h for h in health_checks if h.status == HealthStatus.DEGRADED]),
                    "service_checks": [
                        {
                            "service_name": h.service_name,
                            "status": h.status.value,
                            "message": h.message,
                            "response_time_ms": h.response_time_ms
                        }
                        for h in health_checks
                    ]
                }
            )
            
            self.logger.info(f"System health check completed: {overall_status.value} ({response_time_ms:.2f}ms)")
            return Result.success(overall_health_check)
            
        except Exception as e:
            response_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            health_check = HealthCheck(
                service_name=self.service_name,
                status=HealthStatus.UNHEALTHY,
                message=f"System health check exception: {str(e)}",
                timestamp=datetime.now(),
                response_time_ms=response_time_ms,
                details={
                    "exception": str(e),
                    "exception_type": type(e).__name__,
                    "registered_services": len(self._health_services)
                }
            )
            
            self.logger.error(f"System health check exception: {e}")
            return Result.success(health_check)
    
    async def get_service_info(self) -> Dict[str, Any]:
        """Get system health information"""
        base_info = await super().get_service_info()
        
        base_info.update({
            "registered_services": len(self._health_services),
            "service_names": [service.service_name for service in self._health_services],
            "service_types": [service.__class__.__name__ for service in self._health_services]
        })
        
        return base_info
    
    async def get_overall_health(self) -> Result[Dict[str, Any], str]:
        """Get overall system health status"""
        try:
            overall_result = await self.check_health()
            if overall_result.is_error:
                return Result.error(overall_result.error)
            
            overall_health = overall_result.value
            
            # Get detailed health for all services
            detailed_result = await self.get_detailed_health()
            services_data = []
            if detailed_result.is_success:
                services_data = [
                    {
                        "service_name": check.service_name,
                        "status": check.status.value,
                        "response_time_ms": check.response_time_ms,
                        "message": check.message,
                        "last_check": check.timestamp.isoformat()
                    }
                    for check in detailed_result.value
                ]
            
            return Result.success({
                "status": overall_health.status.value,
                "message": overall_health.message,
                "timestamp": overall_health.timestamp.isoformat(),
                "response_time_ms": overall_health.response_time_ms,
                "services": services_data,
                "services_checked": overall_health.details.get("checked_services", 0),
                "healthy_services": overall_health.details.get("healthy_services", 0),
                "unhealthy_services": overall_health.details.get("unhealthy_services", 0),
                "degraded_services": overall_health.details.get("degraded_services", 0)
            })
            
        except Exception as e:
            return Result.error(str(e))
    
    async def get_detailed_health(self) -> Result[List[HealthCheck], str]:
        """Get detailed health information for all services"""
        try:
            # Get overall health
            overall_result = await self.check_health()
            if overall_result.is_error:
                return Result.error(overall_result.error)
            
            overall_health = overall_result.value
            
            # Extract individual health checks from details
            health_checks = []
            if "service_checks" in overall_health.details:
                for service_check in overall_health.details["service_checks"]:
                    health_check = HealthCheck(
                        service_name=service_check["service_name"],
                        status=HealthStatus(service_check["status"]),
                        message=service_check["message"],
                        timestamp=datetime.now(),
                        response_time_ms=service_check["response_time_ms"]
                    )
                    health_checks.append(health_check)
            
            return Result.success(health_checks)
            
        except Exception as e:
            return Result.error(str(e))
