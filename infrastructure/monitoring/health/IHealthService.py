# infrastructure/monitoring/health/IHealthService.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from domain.utils.result import Result

class HealthStatus(Enum):
    """Status zdrowia serwisu"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"

@dataclass
class HealthCheck:
    """Wynik sprawdzenia zdrowia serwisu"""
    service_name: str
    status: HealthStatus
    message: str
    timestamp: datetime
    response_time_ms: float
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}

class IHealthService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Abstrakcyjny interfejs serwisu monitorowania zdrowia"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    @abstractmethod
    async def check_health(self) -> Result[HealthCheck, str]:
        """Sprawdza stan zdrowia serwisu"""
        pass
    
    async def get_service_info(self) -> Dict[str, Any]:
        """Zwraca informacje o serwisie"""
        return {
            "service_name": self.service_name,
            "type": self.__class__.__name__,
            "timestamp": datetime.now().isoformat()
        }
