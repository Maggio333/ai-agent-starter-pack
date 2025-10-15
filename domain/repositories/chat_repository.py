# domain/repositories/chat_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from datetime import datetime
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.utils.result import Result

class ChatRepository(ABC):
    """Enhanced Chat repository interface with comprehensive CRUD operations"""
    
    # Basic CRUD Operations
    @abstractmethod
    async def save_message(self, message: ChatMessage) -> Result[None, str]:
        """Save chat message"""
        pass
    
    @abstractmethod
    async def get_message_by_id(self, message_id: str) -> Result[Optional[ChatMessage], str]:
        """Get message by ID"""
        pass
    
    @abstractmethod
    async def update_message(self, message: ChatMessage) -> Result[None, str]:
        """Update existing message"""
        pass
    
    @abstractmethod
    async def delete_message(self, message_id: str) -> Result[None, str]:
        """Delete message by ID"""
        pass
    
    # Query Operations
    @abstractmethod
    async def get_messages(self, limit: int = 10, offset: int = 0) -> Result[List[ChatMessage], str]:
        """Get chat messages with pagination"""
        pass
    
    @abstractmethod
    async def get_messages_by_thread(self, thread_id: str, limit: int = 10, offset: int = 0) -> Result[List[ChatMessage], str]:
        """Get messages by thread ID"""
        pass
    
    @abstractmethod
    async def get_messages_by_role(self, role: MessageRole, limit: int = 10, offset: int = 0) -> Result[List[ChatMessage], str]:
        """Get messages by role"""
        pass
    
    @abstractmethod
    async def get_messages_by_date_range(self, start_date: datetime, end_date: datetime, limit: int = 100) -> Result[List[ChatMessage], str]:
        """Get messages by date range"""
        pass
    
    @abstractmethod
    async def search_messages(self, query: str, limit: int = 10, offset: int = 0) -> Result[List[ChatMessage], str]:
        """Search messages by content"""
        pass
    
    @abstractmethod
    async def get_messages_by_user(self, user_id: str, limit: int = 10, offset: int = 0) -> Result[List[ChatMessage], str]:
        """Get messages by user ID"""
        pass
    
    # Bulk Operations
    @abstractmethod
    async def save_messages_bulk(self, messages: List[ChatMessage]) -> Result[None, str]:
        """Save multiple messages at once"""
        pass
    
    @abstractmethod
    async def delete_messages_bulk(self, message_ids: List[str]) -> Result[None, str]:
        """Delete multiple messages at once"""
        pass
    
    @abstractmethod
    async def update_messages_bulk(self, messages: List[ChatMessage]) -> Result[None, str]:
        """Update multiple messages at once"""
        pass
    
    # Statistics & Analytics
    @abstractmethod
    async def get_message_count(self) -> Result[int, str]:
        """Get total message count"""
        pass
    
    @abstractmethod
    async def get_message_count_by_thread(self, thread_id: str) -> Result[int, str]:
        """Get message count by thread"""
        pass
    
    @abstractmethod
    async def get_message_count_by_role(self, role: MessageRole) -> Result[int, str]:
        """Get message count by role"""
        pass
    
    @abstractmethod
    async def get_conversation_stats(self) -> Result[Dict[str, Any], str]:
        """Get conversation statistics"""
        pass
    
    @abstractmethod
    async def get_user_stats(self, user_id: str) -> Result[Dict[str, Any], str]:
        """Get user-specific statistics"""
        pass
    
    # Pagination Support
    @abstractmethod
    async def get_messages_paginated(self, page: int, page_size: int) -> Result[Dict[str, Any], str]:
        """Get messages with pagination metadata"""
        pass
    
    @abstractmethod
    async def get_messages_by_thread_paginated(self, thread_id: str, page: int, page_size: int) -> Result[Dict[str, Any], str]:
        """Get thread messages with pagination"""
        pass
    
    # Advanced Querying
    @abstractmethod
    async def get_recent_messages(self, hours: int = 24, limit: int = 50) -> Result[List[ChatMessage], str]:
        """Get recent messages within specified hours"""
        pass
    
    @abstractmethod
    async def get_messages_with_attachments(self, limit: int = 10) -> Result[List[ChatMessage], str]:
        """Get messages that have file attachments"""
        pass
    
    @abstractmethod
    async def get_messages_by_command(self, command: str, limit: int = 10) -> Result[List[ChatMessage], str]:
        """Get messages that are commands"""
        pass
    
    @abstractmethod
    async def get_messages_by_mentions(self, mention: str, limit: int = 10) -> Result[List[ChatMessage], str]:
        """Get messages containing specific mentions"""
        pass
    
    @abstractmethod
    async def get_messages_by_hashtags(self, hashtag: str, limit: int = 10) -> Result[List[ChatMessage], str]:
        """Get messages containing specific hashtags"""
        pass
    
    # Thread Management
    @abstractmethod
    async def create_thread(self, thread_id: str, initial_message: ChatMessage) -> Result[None, str]:
        """Create new conversation thread"""
        pass
    
    @abstractmethod
    async def get_threads(self, limit: int = 10) -> Result[List[str], str]:
        """Get list of thread IDs"""
        pass
    
    @abstractmethod
    async def delete_thread(self, thread_id: str) -> Result[None, str]:
        """Delete entire thread"""
        pass
    
    @abstractmethod
    async def get_thread_info(self, thread_id: str) -> Result[Dict[str, Any], str]:
        """Get thread metadata and statistics"""
        pass
    
    # Transaction Support
    @abstractmethod
    async def begin_transaction(self) -> Result[Any, str]:
        """Begin database transaction"""
        pass
    
    @abstractmethod
    async def commit_transaction(self, transaction: Any) -> Result[None, str]:
        """Commit transaction"""
        pass
    
    @abstractmethod
    async def rollback_transaction(self, transaction: Any) -> Result[None, str]:
        """Rollback transaction"""
        pass
    
    # Health & Maintenance
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check repository health"""
        pass
    
    @abstractmethod
    async def cleanup_old_messages(self, days_old: int = 30) -> Result[int, str]:
        """Clean up messages older than specified days"""
        pass
    
    @abstractmethod
    async def optimize_database(self) -> Result[None, str]:
        """Optimize database performance"""
        pass
    
    # Export/Import
    @abstractmethod
    async def export_messages(self, thread_id: Optional[str] = None, format: str = "json") -> Result[str, str]:
        """Export messages to specified format"""
        pass
    
    @abstractmethod
    async def import_messages(self, data: str, format: str = "json") -> Result[int, str]:
        """Import messages from specified format"""
        pass
