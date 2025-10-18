# infrastructure/services/text_cleaner_service.py
import logging
from typing import List, Dict, Any
from domain.services.ITextCleanerService import ITextCleanerService
from domain.utils.result import Result
from infrastructure.utils.text_cleaner import TextCleaner

class TextCleanerService(ITextCleanerService):  # Implementacja ITextCleanerService używająca TextCleaner utility
    """Implementacja ITextCleanerService używająca TextCleaner utility"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.text_cleaner = TextCleaner()
        self.logger.info("TextCleanerService zainicjalizowany")  # Polskie logi
    
    async def clean_text(self, text: str) -> Result[str, str]:
        """Czyści tekst z problematycznych znaków (emotki, symbole Unicode)"""
        try:
            result = self.text_cleaner.clean_text(text)
            if result.is_success:
                self.logger.debug(f"Tekst wyczyszczony pomyślnie: '{text[:50]}...' -> '{result.value[:50]}...'")
            else:
                self.logger.warning(f"Nie udało się wyczyścić tekstu: {result.error}")
            return result
        except Exception as e:
            error_msg = f"Błąd TextCleanerService: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def clean_text_batch(self, texts: List[str]) -> Result[List[str], str]:
        """Czyści wiele tekstów jednocześnie"""
        try:
            result = self.text_cleaner.clean_text_batch(texts)
            if result.is_success:
                self.logger.debug(f"Wyczyszczono pomyślnie {len(texts)} tekstów")
            else:
                self.logger.warning(f"Nie udało się wyczyścić partii tekstów: {result.error}")
            return result
        except Exception as e:
            error_msg = f"Błąd TextCleanerService przy czyszczeniu partii: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def clean_dict_values(self, data: Dict[str, Any]) -> Result[Dict[str, Any], str]:
        """Czyści wartości tekstowe w słowniku"""
        try:
            result = self.text_cleaner.clean_dict_values(data)
            if result.is_success:
                self.logger.debug("Wartości słownika wyczyszczone pomyślnie")
            else:
                self.logger.warning(f"Nie udało się wyczyścić wartości słownika: {result.error}")
            return result
        except Exception as e:
            error_msg = f"Błąd TextCleanerService przy czyszczeniu słownika: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def is_text_safe(self, text: str) -> Result[bool, str]:
        """Sprawdza czy tekst jest bezpieczny dla kodowania"""
        try:
            result = self.text_cleaner.is_text_safe(text)
            return result
        except Exception as e:
            error_msg = f"Błąd TextCleanerService przy sprawdzaniu bezpieczeństwa: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def get_cleaning_stats(self, original_text: str, cleaned_text: str) -> Result[Dict[str, Any], str]:
        """Zwraca statystyki czyszczenia tekstu"""
        try:
            result = self.text_cleaner.get_cleaning_stats(original_text, cleaned_text)
            return result
        except Exception as e:
            error_msg = f"Błąd TextCleanerService przy pobieraniu statystyk: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
