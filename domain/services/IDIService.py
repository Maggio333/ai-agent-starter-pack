# domain/services/IDIService.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from domain.utils.result import Result

class IDIService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu Dependency Injection"""
    
    @abstractmethod
    def get_container(self):
        """Pobiera kontener DI"""
        pass
    
    @abstractmethod
    def reset_services(self) -> None:
        """Resetuje wszystkie lazy-loaded serwisy"""
        pass
    
    @abstractmethod
    def get_service_status(self) -> Dict[str, Any]:
        """Pobiera status wszystkich serwisów"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Sprawdza stan serwisu"""
        pass
