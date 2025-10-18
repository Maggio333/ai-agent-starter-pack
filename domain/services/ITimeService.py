# domain/services/ITimeService.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from domain.utils.result import Result

class ITimeService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu operacji czasowych"""
    
    @abstractmethod
    async def get_current_time(self, city: str) -> Result[Dict[str, Any], str]:
        """Pobiera aktualny czas dla miasta"""
        pass
    
    @abstractmethod
    async def get_timezone_info(self, city: str) -> Result[Dict[str, Any], str]:
        """Pobiera informacje o strefie czasowej miasta"""
        pass
    
    @abstractmethod
    async def convert_time(self, time: str, from_city: str, to_city: str) -> Result[Dict[str, Any], str]:
        """Konwertuje czas między miastami"""
        pass
    
    @abstractmethod
    async def get_world_clock(self, cities: List[str]) -> Result[List[Dict[str, Any]], str]:
        """Pobiera czas dla wielu miast"""
        pass
    
    @abstractmethod
    async def get_time_difference(self, city1: str, city2: str) -> Result[Dict[str, Any], str]:
        """Pobiera różnicę czasu między miastami"""
        pass
    
    @abstractmethod
    async def get_supported_cities(self) -> Result[List[str], str]:
        """Pobiera listę obsługiwanych miast"""
        pass
    
    @abstractmethod
    async def is_city_supported(self, city: str) -> Result[bool, str]:
        """Sprawdza czy miasto jest obsługiwane"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Sprawdza stan serwisu"""
        pass
