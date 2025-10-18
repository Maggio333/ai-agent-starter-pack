# domain/services/text_cleaner_service.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from domain.utils.result import Result

class ITextCleanerService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Abstrakcyjny interfejs serwisu czyszczenia tekstu"""
    
    @abstractmethod
    async def clean_text(self, text: str) -> Result[str, str]:
        """Czyści tekst z problematycznych znaków (emotki, symbole Unicode)"""
        pass
    
    @abstractmethod
    async def clean_text_batch(self, texts: List[str]) -> Result[List[str], str]:
        """Czyści wiele tekstów jednocześnie"""
        pass
    
    @abstractmethod
    async def clean_dict_values(self, data: Dict[str, Any]) -> Result[Dict[str, Any], str]:
        """Czyści wartości tekstowe w słowniku"""
        pass
    
    @abstractmethod
    async def is_text_safe(self, text: str) -> Result[bool, str]:
        """Sprawdza czy tekst jest bezpieczny dla kodowania"""
        pass
    
    @abstractmethod
    async def get_cleaning_stats(self, original_text: str, cleaned_text: str) -> Result[Dict[str, Any], str]:
        """Zwraca statystyki czyszczenia tekstu"""
        pass
