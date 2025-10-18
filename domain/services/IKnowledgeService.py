# domain/services/IKnowledgeService.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from domain.utils.result import Result

class IKnowledgeService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu zarządzania bazą wiedzy"""
    
    @abstractmethod
    async def search_knowledge_base(self, query: str) -> Result[List[Dict[str, Any]], str]:
        """Wyszukuje w bazie wiedzy"""
        pass
    
    @abstractmethod
    async def add_knowledge(self, topic: str, facts: List[str]) -> Result[bool, str]:
        """Dodaje wiedzę do bazy"""
        pass
    
    @abstractmethod
    async def get_knowledge_stats(self) -> Result[Dict[str, Any], str]:
        """Pobiera statystyki bazy wiedzy"""
        pass
    
    @abstractmethod
    async def get_topic_facts(self, topic: str) -> Result[List[str], str]:
        """Pobiera fakty dla tematu"""
        pass
    
    @abstractmethod
    async def search_similar_topics(self, topic: str) -> Result[List[Dict[str, Any]], str]:
        """Wyszukuje podobne tematy"""
        pass
    
    @abstractmethod
    async def create_rag_chunk(self, text: str, topic: str) -> Result[Dict[str, Any], str]:
        """Tworzy chunk RAG"""
        pass
    
    @abstractmethod
    async def get_search_history(self) -> Result[List[Dict[str, Any]], str]:
        """Pobiera historię wyszukiwań"""
        pass
    
    @abstractmethod
    async def clear_search_history(self) -> Result[bool, str]:
        """Czyści historię wyszukiwań"""
        pass
    
    @abstractmethod
    async def export_knowledge_base(self) -> Result[Dict[str, Any], str]:
        """Eksportuje bazę wiedzy"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Sprawdza stan serwisu"""
        pass
