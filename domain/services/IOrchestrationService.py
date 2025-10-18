# domain/services/IOrchestrationService.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from domain.utils.result import Result

class IOrchestrationService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu orchestracji wszystkich serwisów"""
    
    @abstractmethod
    async def process_city_request(self, city: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Przetwarza żądanie dotyczące miasta"""
        pass
    
    @abstractmethod
    async def process_weather_request(self, city: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Przetwarza żądanie dotyczące pogody"""
        pass
    
    @abstractmethod
    async def process_time_request(self, city: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Przetwarza żądanie dotyczące czasu"""
        pass
    
    @abstractmethod
    async def process_knowledge_request(self, query: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Przetwarza żądanie dotyczące wiedzy"""
        pass
    
    @abstractmethod
    async def process_conversation_request(self, message: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Przetwarza żądanie dotyczące konwersacji"""
        pass
    
    @abstractmethod
    async def get_service_health(self) -> Result[Dict[str, Any], str]:
        """Pobiera stan zdrowia wszystkich serwisów"""
        pass
    
    @abstractmethod
    async def get_service_capabilities(self) -> Result[Dict[str, List[str]], str]:
        """Pobiera możliwości wszystkich serwisów"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Sprawdza stan serwisu"""
        pass
