# tests/services/test_conversation_service.py
import sys
sys.path.append('.')
import pytest
import asyncio
from datetime import datetime
from application.services.conversation_service import ConversationService
from domain.utils.result import Result
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.repositories.chat_repository import ChatRepository

class MockChatRepository(ChatRepository):
    """Mock implementation of ChatRepository for testing"""
    
    def __init__(self):
        self.messages = {}
        self.message_count = 0
    
    async def save_message(self, message: ChatMessage) -> Result[None, str]:
        self.messages[message.message_id] = message
        self.message_count += 1
        return Result.success(None)
    
    async def get_message_by_id(self, message_id: str) -> Result[ChatMessage, str]:
        if message_id in self.messages:
            return Result.success(self.messages[message_id])
        return Result.error("Message not found")
    
    async def get_messages_by_thread(self, thread_id: str, limit: int = 10, offset: int = 0) -> Result[list, str]:
        thread_messages = [msg for msg in self.messages.values() if msg.thread_id == thread_id]
        thread_messages.sort(key=lambda x: x.timestamp)
        return Result.success(thread_messages[offset:offset+limit])
    
    async def get_message_count_by_thread(self, thread_id: str) -> Result[int, str]:
        count = sum(1 for msg in self.messages.values() if msg.thread_id == thread_id)
        return Result.success(count)
    
    async def search_messages(self, query: str, limit: int = 10, offset: int = 0) -> Result[list, str]:
        matching_messages = [msg for msg in self.messages.values() if query.lower() in msg.content.lower()]
        return Result.success(matching_messages[offset:offset+limit])
    
    # Implement other required methods as no-ops for testing
    async def get_messages(self, limit: int = 10, offset: int = 0) -> Result[list, str]:
        return Result.success(list(self.messages.values())[offset:offset+limit])
    
    async def update_message(self, message: ChatMessage) -> Result[None, str]:
        if message.message_id in self.messages:
            self.messages[message.message_id] = message
            return Result.success(None)
        return Result.error("Message not found")
    
    async def delete_message(self, message_id: str) -> Result[None, str]:
        if message_id in self.messages:
            del self.messages[message_id]
            return Result.success(None)
        return Result.error("Message not found")
    
    async def get_messages_by_role(self, role: MessageRole, limit: int = 10, offset: int = 0) -> Result[list, str]:
        role_messages = [msg for msg in self.messages.values() if msg.role == role]
        return Result.success(role_messages[offset:offset+limit])
    
    async def get_messages_by_date_range(self, start_date: datetime, end_date: datetime, limit: int = 100) -> Result[list, str]:
        range_messages = [msg for msg in self.messages.values() if start_date <= msg.timestamp <= end_date]
        return Result.success(range_messages[:limit])
    
    async def get_messages_by_user(self, user_id: str, limit: int = 10, offset: int = 0) -> Result[list, str]:
        return await self.get_messages_by_thread(user_id, limit, offset)
    
    async def save_messages_bulk(self, messages: list) -> Result[None, str]:
        for message in messages:
            await self.save_message(message)
        return Result.success(None)
    
    async def delete_messages_bulk(self, message_ids: list) -> Result[None, str]:
        for message_id in message_ids:
            await self.delete_message(message_id)
        return Result.success(None)
    
    async def update_messages_bulk(self, messages: list) -> Result[None, str]:
        for message in messages:
            await self.update_message(message)
        return Result.success(None)
    
    async def get_message_count(self) -> Result[int, str]:
        return Result.success(len(self.messages))
    
    async def get_message_count_by_role(self, role: MessageRole) -> Result[int, str]:
        count = sum(1 for msg in self.messages.values() if msg.role == role)
        return Result.success(count)
    
    async def get_conversation_stats(self) -> Result[dict, str]:
        return Result.success({
            "total_messages": len(self.messages),
            "role_counts": {"user": 0, "assistant": 0, "system": 0},
            "thread_count": len(set(msg.thread_id for msg in self.messages.values() if msg.thread_id)),
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_user_stats(self, user_id: str) -> Result[dict, str]:
        return Result.success({
            "user_id": user_id,
            "message_count": await self.get_message_count_by_thread(user_id),
            "timestamp": datetime.now().isoformat()
        })
    
    async def get_messages_paginated(self, page: int, page_size: int) -> Result[dict, str]:
        offset = (page - 1) * page_size
        messages = await self.get_messages(page_size, offset)
        total_count = await self.get_message_count()
        
        return Result.success({
            "messages": messages.value,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count.value,
                "total_pages": (total_count.value + page_size - 1) // page_size,
                "has_next": page < (total_count.value + page_size - 1) // page_size,
                "has_prev": page > 1
            }
        })
    
    async def get_messages_by_thread_paginated(self, thread_id: str, page: int, page_size: int) -> Result[dict, str]:
        offset = (page - 1) * page_size
        messages = await self.get_messages_by_thread(thread_id, page_size, offset)
        total_count = await self.get_message_count_by_thread(thread_id)
        
        return Result.success({
            "messages": messages.value,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count.value,
                "total_pages": (total_count.value + page_size - 1) // page_size,
                "has_next": page < (total_count.value + page_size - 1) // page_size,
                "has_prev": page > 1
            }
        })
    
    async def get_recent_messages(self, hours: int = 24, limit: int = 50) -> Result[list, str]:
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        recent_messages = [msg for msg in self.messages.values() if msg.timestamp.timestamp() > cutoff_time]
        return Result.success(recent_messages[:limit])
    
    async def get_messages_with_attachments(self, limit: int = 10) -> Result[list, str]:
        attachment_messages = [msg for msg in self.messages.values() if msg.file_name is not None]
        return Result.success(attachment_messages[:limit])
    
    async def get_messages_by_command(self, command: str, limit: int = 10) -> Result[list, str]:
        command_messages = [msg for msg in self.messages.values() if msg.content.startswith(f"/{command}")]
        return Result.success(command_messages[:limit])
    
    async def get_messages_by_mentions(self, mention: str, limit: int = 10) -> Result[list, str]:
        mention_messages = [msg for msg in self.messages.values() if f"@{mention}" in msg.content]
        return Result.success(mention_messages[:limit])
    
    async def get_messages_by_hashtags(self, hashtag: str, limit: int = 10) -> Result[list, str]:
        hashtag_messages = [msg for msg in self.messages.values() if f"#{hashtag}" in msg.content]
        return Result.success(hashtag_messages[:limit])
    
    async def create_thread(self, thread_id: str, initial_message: ChatMessage) -> Result[None, str]:
        initial_message.thread_id = thread_id
        return await self.save_message(initial_message)
    
    async def get_threads(self, limit: int = 10) -> Result[list, str]:
        thread_ids = list(set(msg.thread_id for msg in self.messages.values() if msg.thread_id))
        return Result.success(thread_ids[:limit])
    
    async def delete_thread(self, thread_id: str) -> Result[None, str]:
        messages_to_delete = [msg for msg in self.messages.values() if msg.thread_id == thread_id]
        for msg in messages_to_delete:
            del self.messages[msg.message_id]
        return Result.success(None)
    
    async def get_thread_info(self, thread_id: str) -> Result[dict, str]:
        thread_messages = [msg for msg in self.messages.values() if msg.thread_id == thread_id]
        if not thread_messages:
            return Result.error("Thread not found")
        
        thread_messages.sort(key=lambda x: x.timestamp)
        return Result.success({
            "thread_id": thread_id,
            "message_count": len(thread_messages),
            "first_message_time": thread_messages[0].timestamp.isoformat(),
            "last_message_time": thread_messages[-1].timestamp.isoformat(),
            "timestamp": datetime.now().isoformat()
        })
    
    async def begin_transaction(self) -> Result[any, str]:
        return Result.success("mock_transaction")
    
    async def commit_transaction(self, transaction: any) -> Result[None, str]:
        return Result.success(None)
    
    async def rollback_transaction(self, transaction: any) -> Result[None, str]:
        return Result.success(None)
    
    async def health_check(self) -> Result[dict, str]:
        return Result.success({
            "status": "healthy",
            "database_path": "mock",
            "timestamp": datetime.now().isoformat()
        })
    
    async def cleanup_old_messages(self, days_old: int = 30) -> Result[int, str]:
        return Result.success(0)
    
    async def optimize_database(self) -> Result[None, str]:
        return Result.success(None)
    
    async def export_messages(self, thread_id: str = None, format: str = "json") -> Result[str, str]:
        return Result.success('{"messages": []}')
    
    async def import_messages(self, data: str, format: str = "json") -> Result[int, str]:
        return Result.success(0)

class TestConversationService:
    """Test suite for Conversation Service"""
    
    @pytest.fixture
    def mock_repository(self):
        """Create mock repository for testing"""
        return MockChatRepository()
    
    @pytest.fixture
    def conversation_service(self, mock_repository):
        """Create ConversationService instance for testing"""
        return ConversationService(mock_repository)
    
    @pytest.mark.asyncio
    async def test_start_conversation_success(self, conversation_service):
        """Test successful conversation start"""
        context = {"system_prompt": "You are a helpful assistant"}
        
        result = await conversation_service.start_conversation(context)
        
        assert result.is_success
        session_id = result.value
        assert isinstance(session_id, str)
        assert session_id.startswith("session_")
    
    @pytest.mark.asyncio
    async def test_start_conversation_no_context(self, conversation_service):
        """Test conversation start without context"""
        result = await conversation_service.start_conversation()
        
        assert result.is_success
        session_id = result.value
        assert isinstance(session_id, str)
    
    @pytest.mark.asyncio
    async def test_save_conversation_success(self, conversation_service):
        """Test successful conversation saving"""
        messages = [
            ChatMessage.create_user_message("Hello", "test_session"),
            ChatMessage.create_assistant_message("Hi there!", "test_session")
        ]
        
        result = await conversation_service.save_conversation(messages, "test_session")
        
        assert result.is_success
    
    @pytest.mark.asyncio
    async def test_save_conversation_empty_messages(self, conversation_service):
        """Test conversation saving with empty messages"""
        result = await conversation_service.save_conversation([])
        
        assert result.is_error
        assert "Messages list cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_save_conversation_invalid_messages(self, conversation_service):
        """Test conversation saving with invalid messages"""
        result = await conversation_service.save_conversation(["invalid_message"])
        
        assert result.is_error
        assert "Messages must be a non-empty list of ChatMessage objects" in result.error
    
    @pytest.mark.asyncio
    async def test_get_conversation_history_success(self, conversation_service):
        """Test successful conversation history retrieval"""
        # First save some messages
        messages = [
            ChatMessage.create_user_message("Hello", "test_session"),
            ChatMessage.create_assistant_message("Hi there!", "test_session")
        ]
        await conversation_service.save_conversation(messages, "test_session")
        
        result = await conversation_service.get_conversation_history("test_session", 10)
        
        assert result.is_success
        history = result.value
        assert isinstance(history, list)
        assert len(history) == 2
    
    @pytest.mark.asyncio
    async def test_get_conversation_history_empty_session(self, conversation_service):
        """Test conversation history for empty session"""
        result = await conversation_service.get_conversation_history("empty_session")
        
        assert result.is_success
        history = result.value
        assert isinstance(history, list)
        assert len(history) == 0
    
    @pytest.mark.asyncio
    async def test_get_conversation_history_invalid_session(self, conversation_service):
        """Test conversation history with invalid session ID"""
        result = await conversation_service.get_conversation_history("")
        
        assert result.is_error
        assert "Session ID cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_end_conversation_success(self, conversation_service):
        """Test successful conversation end"""
        # Start a conversation first
        start_result = await conversation_service.start_conversation()
        assert start_result.is_success
        session_id = start_result.value
        
        result = await conversation_service.end_conversation(session_id)
        
        assert result.is_success
    
    @pytest.mark.asyncio
    async def test_end_conversation_invalid_session(self, conversation_service):
        """Test conversation end with invalid session"""
        result = await conversation_service.end_conversation("invalid_session")
        
        assert result.is_error
        assert "not found or already ended" in result.error
    
    @pytest.mark.asyncio
    async def test_end_conversation_empty_session(self, conversation_service):
        """Test conversation end with empty session ID"""
        result = await conversation_service.end_conversation("")
        
        assert result.is_error
        assert "Session ID cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_get_session_info_success(self, conversation_service):
        """Test successful session info retrieval"""
        # Start a conversation and save some messages
        start_result = await conversation_service.start_conversation()
        session_id = start_result.value
        
        messages = [
            ChatMessage.create_user_message("Hello", session_id),
            ChatMessage.create_assistant_message("Hi there!", session_id)
        ]
        await conversation_service.save_conversation(messages, session_id)
        
        result = await conversation_service.get_session_info(session_id)
        
        assert result.is_success
        info = result.value
        assert "session_id" in info
        assert "status" in info
        assert "started_at" in info
        assert "last_activity" in info
        assert "message_count" in info
        assert info["session_id"] == session_id
        assert info["status"] == "active"
        assert info["message_count"] == 2
    
    @pytest.mark.asyncio
    async def test_get_session_info_invalid_session(self, conversation_service):
        """Test session info for invalid session"""
        result = await conversation_service.get_session_info("invalid_session")
        
        assert result.is_error
        assert "not found" in result.error
    
    @pytest.mark.asyncio
    async def test_get_active_sessions(self, conversation_service):
        """Test getting active sessions"""
        # Start multiple conversations
        session1 = await conversation_service.start_conversation()
        session2 = await conversation_service.start_conversation()
        
        result = await conversation_service.get_active_sessions()
        
        assert result.is_success
        active_sessions = result.value
        assert isinstance(active_sessions, list)
        assert len(active_sessions) >= 2
        
        # Check structure
        for session in active_sessions:
            assert "session_id" in session
            assert "started_at" in session
            assert "last_activity" in session
            assert "message_count" in session
            assert "context" in session
    
    @pytest.mark.asyncio
    async def test_get_conversation_stats(self, conversation_service):
        """Test conversation statistics retrieval"""
        result = await conversation_service.get_conversation_stats()
        
        assert result.is_success
        stats = result.value
        assert "total_sessions" in stats
        assert "total_messages" in stats
        assert "active_sessions" in stats
        assert "repository_stats" in stats
        assert "timestamp" in stats
    
    @pytest.mark.asyncio
    async def test_cleanup_inactive_sessions(self, conversation_service):
        """Test cleanup of inactive sessions"""
        result = await conversation_service.cleanup_inactive_sessions(1)  # 1 hour threshold
        
        assert result.is_success
        cleaned_count = result.value
        assert isinstance(cleaned_count, int)
        assert cleaned_count >= 0
    
    @pytest.mark.asyncio
    async def test_cleanup_inactive_sessions_invalid_threshold(self, conversation_service):
        """Test cleanup with invalid threshold"""
        result = await conversation_service.cleanup_inactive_sessions(0)
        
        assert result.is_error
        assert "Hours threshold must be positive" in result.error
    
    @pytest.mark.asyncio
    async def test_export_conversation_success(self, conversation_service):
        """Test successful conversation export"""
        # Start a conversation and save messages
        start_result = await conversation_service.start_conversation()
        session_id = start_result.value
        
        messages = [
            ChatMessage.create_user_message("Hello", session_id),
            ChatMessage.create_assistant_message("Hi there!", session_id)
        ]
        await conversation_service.save_conversation(messages, session_id)
        
        result = await conversation_service.export_conversation(session_id, "json")
        
        assert result.is_success
        export_data = result.value
        assert isinstance(export_data, str)
        assert "session_info" in export_data
        assert "messages" in export_data
        assert "exported_at" in export_data
    
    @pytest.mark.asyncio
    async def test_export_conversation_invalid_session(self, conversation_service):
        """Test conversation export with invalid session"""
        result = await conversation_service.export_conversation("invalid_session")
        
        assert result.is_error
        assert "Session ID cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_export_conversation_invalid_format(self, conversation_service):
        """Test conversation export with invalid format"""
        start_result = await conversation_service.start_conversation()
        session_id = start_result.value
        
        result = await conversation_service.export_conversation(session_id, "invalid_format")
        
        assert result.is_error
        assert "Unsupported export format" in result.error
    
    @pytest.mark.asyncio
    async def test_search_conversations_success(self, conversation_service):
        """Test successful conversation search"""
        # Save some messages with searchable content
        messages = [
            ChatMessage.create_user_message("Hello world", "test_session"),
            ChatMessage.create_assistant_message("Hi there!", "test_session")
        ]
        await conversation_service.save_conversation(messages, "test_session")
        
        result = await conversation_service.search_conversations("Hello")
        
        assert result.is_success
        conversations = result.value
        assert isinstance(conversations, list)
        assert len(conversations) > 0
    
    @pytest.mark.asyncio
    async def test_search_conversations_empty_query(self, conversation_service):
        """Test conversation search with empty query"""
        result = await conversation_service.search_conversations("")
        
        assert result.is_error
        assert "Search query cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_conversation_service_performance(self, conversation_service):
        """Test conversation service performance"""
        import time
        
        start_time = time.time()
        
        # Start multiple conversations
        tasks = [conversation_service.start_conversation() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # Should complete quickly
        assert duration < 2.0, f"Performance test failed: {duration:.2f}s for 10 requests"
    
    @pytest.mark.asyncio
    async def test_conversation_service_concurrent_access(self, conversation_service):
        """Test concurrent access to conversation service"""
        # Test concurrent conversation starts
        tasks = [conversation_service.start_conversation() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # All session IDs should be unique
        session_ids = [result.value for result in results]
        assert len(set(session_ids)) == len(session_ids)
    
    @pytest.mark.asyncio
    async def test_conversation_service_session_lifecycle(self, conversation_service):
        """Test complete session lifecycle"""
        # Start conversation
        start_result = await conversation_service.start_conversation({"test": "context"})
        assert start_result.is_success
        session_id = start_result.value
        
        # Save messages
        messages = [
            ChatMessage.create_user_message("Hello", session_id),
            ChatMessage.create_assistant_message("Hi there!", session_id)
        ]
        save_result = await conversation_service.save_conversation(messages, session_id)
        assert save_result.is_success
        
        # Get history
        history_result = await conversation_service.get_conversation_history(session_id)
        assert history_result.is_success
        assert len(history_result.value) == 2
        
        # Get session info
        info_result = await conversation_service.get_session_info(session_id)
        assert info_result.is_success
        assert info_result.value["message_count"] == 2
        
        # End conversation
        end_result = await conversation_service.end_conversation(session_id)
        assert end_result.is_success
        
        # Verify session is ended
        info_result = await conversation_service.get_session_info(session_id)
        assert info_result.is_success
        assert info_result.value["status"] == "ended"
