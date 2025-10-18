# infrastructure/ai/embeddings/IEmbeddingService.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging
from domain.utils.result import Result

class IEmbeddingService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Abstrakcyjny interfejs serwisu embeddingów"""
    
    def __init__(self, model_name: str = "default", dimension: int = 384):
        self.model_name = model_name
        self.dimension = dimension
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def create_embedding(self, text: str) -> Result[List[float], str]:
        """Tworzy embedding dla pojedynczego tekstu"""
        pass
    
    @abstractmethod
    async def create_embeddings_batch(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Tworzy embeddingi dla wielu tekstów jednocześnie"""
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Result[Dict[str, Any], str]:
        """Zwraca informacje o modelu"""
        pass
    
    async def health_check(self) -> Result[dict, str]:
        """Sprawdza stan serwisu"""
        try:
            # Test embedding z prostym tekstem
            test_result = await self.embed_text("test")
            if test_result.is_success:
                health_data = {
                    'status': 'healthy',
                    'service': self.__class__.__name__,
                    'model': self.model_name,
                    'dimension': self.dimension
                }
                return Result.success(health_data)
            else:
                return Result.error(f"Health check failed: {test_result.error}")
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return Result.error(f"Health check failed: {str(e)}")
    
    def _validate_text(self, text: str) -> bool:
        """Waliduje tekst wejściowy"""
        if not text or not isinstance(text, str):
            return False
        return len(text.strip()) > 0
    
    def _validate_texts(self, texts: List[str]) -> bool:
        """Waliduje listę tekstów wejściowych"""
        if not texts or not isinstance(texts, list):
            return False
        return all(self._validate_text(text) for text in texts)
