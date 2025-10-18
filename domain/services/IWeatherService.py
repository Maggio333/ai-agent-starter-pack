# domain/services/IWeatherService.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from domain.utils.result import Result

class IWeatherService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu informacji o pogodzie"""
    
    @abstractmethod
    async def get_weather(self, city: str) -> Result[Dict[str, Any], str]:
        """Pobiera aktualną pogodę dla miasta"""
        pass
    
    @abstractmethod
    async def get_weather_forecast(self, city: str, days: int = 5) -> Result[List[Dict[str, Any]], str]:
        """Pobiera prognozę pogody dla miasta"""
        pass
    
    @abstractmethod
    async def get_weather_alerts(self, city: str) -> Result[List[Dict[str, Any]], str]:
        """Pobiera alerty pogodowe dla miasta"""
        pass
    
    @abstractmethod
    async def get_weather_summary(self, city: str) -> Result[Dict[str, Any], str]:
        """Pobiera podsumowanie pogody dla miasta"""
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
