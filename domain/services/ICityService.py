# domain/services/ICityService.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from domain.utils.result import Result

class ICityService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu zarządzania informacjami o miastach"""
    
    @abstractmethod
    async def get_city_info(self, city_name: str) -> Result[Dict[str, Any], str]:
        """Pobiera informacje o mieście"""
        pass
    
    @abstractmethod
    async def search_cities(self, query: str) -> Result[List[Dict[str, Any]], str]:
        """Wyszukuje miasta na podstawie zapytania"""
        pass
    
    @abstractmethod
    async def get_city_coordinates(self, city_name: str) -> Result[Dict[str, float], str]:
        """Pobiera współrzędne miasta"""
        pass
    
    @abstractmethod
    async def get_city_attractions(self, city_name: str) -> Result[List[Dict[str, Any]], str]:
        """Pobiera atrakcje miasta"""
        pass
    
    @abstractmethod
    async def get_city_airports(self, city_name: str) -> Result[List[Dict[str, Any]], str]:
        """Pobiera lotniska miasta"""
        pass
    
    @abstractmethod
    async def compare_cities(self, city1: str, city2: str) -> Result[Dict[str, Any], str]:
        """Porównuje dwa miasta"""
        pass
    
    @abstractmethod
    async def get_cities_by_country(self, country: str) -> Result[List[Dict[str, Any]], str]:
        """Pobiera miasta z danego kraju"""
        pass
    
    @abstractmethod
    async def get_supported_cities(self) -> Result[List[str], str]:
        """Pobiera listę obsługiwanych miast"""
        pass
    
    @abstractmethod
    async def is_city_supported(self, city_name: str) -> Result[bool, str]:
        """Sprawdza czy miasto jest obsługiwane"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Sprawdza stan serwisu"""
        pass
