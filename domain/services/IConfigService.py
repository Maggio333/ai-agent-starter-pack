# domain/services/IConfigService.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from domain.utils.result import Result

class IConfigService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu konfiguracji"""
    
    @abstractmethod
    def get_llm_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację LLM"""
        pass
    
    @abstractmethod
    def get_embedding_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację embeddingów"""
        pass
    
    @abstractmethod
    def get_vector_db_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację bazy wektorowej"""
        pass
    
    @abstractmethod
    def get_cache_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację cache"""
        pass
    
    @abstractmethod
    def get_search_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację wyszukiwania"""
        pass
    
    @abstractmethod
    def get_database_config(self) -> Dict[str, Any]:
        """Pobiera konfigurację bazy danych"""
        pass
    
    @abstractmethod
    def get_config(self, key: str, default: Any = None) -> Any:
        """Pobiera wartość konfiguracji"""
        pass
    
    @abstractmethod
    def set_config(self, key: str, value: Any) -> None:
        """Ustawia wartość konfiguracji"""
        pass
    
    @abstractmethod
    def reload_config(self) -> Result[bool, str]:
        """Przeładowuje konfigurację"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Sprawdza stan serwisu"""
        pass
