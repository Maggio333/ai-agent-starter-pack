# domain/services/IConversationService.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from domain.utils.result import Result
from domain.entities.chat_message import ChatMessage

class IConversationService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu zarządzania konwersacjami"""
    
    @abstractmethod
    async def start_conversation(self, session_id: str) -> Result[bool, str]:
        """Rozpoczyna nową konwersację"""
        pass
    
    @abstractmethod
    async def save_conversation(self, session_id: str, message: ChatMessage) -> Result[bool, str]:
        """Zapisuje wiadomość w konwersacji"""
        pass
    
    @abstractmethod
    async def get_conversation_history(self, session_id: str) -> Result[List[ChatMessage], str]:
        """Pobiera historię konwersacji"""
        pass
    
    @abstractmethod
    async def end_conversation(self, session_id: str) -> Result[bool, str]:
        """Kończy konwersację"""
        pass
    
    @abstractmethod
    async def get_session_info(self, session_id: str) -> Result[Dict[str, Any], str]:
        """Pobiera informacje o sesji"""
        pass
    
    @abstractmethod
    async def get_active_sessions(self) -> Result[List[Dict[str, Any]], str]:
        """Pobiera aktywne sesje"""
        pass
    
    @abstractmethod
    async def get_conversation_stats(self) -> Result[Dict[str, Any], str]:
        """Pobiera statystyki konwersacji"""
        pass
    
    @abstractmethod
    async def cleanup_inactive_sessions(self) -> Result[int, str]:
        """Czyści nieaktywne sesje"""
        pass
    
    @abstractmethod
    async def export_conversation(self, session_id: str) -> Result[Dict[str, Any], str]:
        """Eksportuje konwersację"""
        pass
    
    @abstractmethod
    async def search_conversations(self, query: str) -> Result[List[Dict[str, Any]], str]:
        """Wyszukuje w konwersacjach"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Sprawdza stan serwisu"""
        pass
