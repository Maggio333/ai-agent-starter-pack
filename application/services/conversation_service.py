# services/conversation_service.py
from typing import Dict, List, Optional, Any
from datetime import datetime
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.repositories.chat_repository import ChatRepository

class ConversationService:
    """Microservice for conversation management and chat operations"""
    
    def __init__(self, chat_repository: ChatRepository):
        self.rop_service = ROPService()
        self.chat_repository = chat_repository
        self._active_sessions = {}
        self._conversation_stats = {
            "total_sessions": 0,
            "total_messages": 0,
            "active_sessions": 0
        }
    
    async def start_conversation(self, context: Optional[Dict[str, Any]] = None) -> Result[str, str]:
        """Start a new conversation session"""
        try:
            # Generate unique session ID
            session_id = f"session_{datetime.now().timestamp()}_{id(self)}"
            
            # Initialize session data
            session_data = {
                "session_id": session_id,
                "started_at": datetime.now(),
                "last_activity": datetime.now(),
                "message_count": 0,
                "context": context or {},
                "status": "active"
            }
            
            self._active_sessions[session_id] = session_data
            self._conversation_stats["total_sessions"] += 1
            self._conversation_stats["active_sessions"] += 1
            
            # Create initial system message if context provided
            if context and "system_prompt" in context:
                system_message = ChatMessage.create_system_message(
                    content=context["system_prompt"],
                    thread_id=session_id
                )
                
                save_result = await self.chat_repository.save_message(system_message)
                if save_result.is_error:
                    return save_result
                
                session_data["message_count"] += 1
            
            return Result.success(session_id)
            
        except Exception as e:
            return Result.error(f"Failed to start conversation: {str(e)}")
    
    async def save_conversation(self, messages: List[ChatMessage], session_id: Optional[str] = None) -> Result[None, str]:
        """Save conversation messages using ROP"""
        try:
            if not messages:
                return Result.error("Messages list cannot be empty")
            
            # Validation using ROP
            messages_validator = self.rop_service.validate(
                lambda msgs: len(msgs) > 0 and all(isinstance(msg, ChatMessage) for msg in msgs),
                "Messages must be a non-empty list of ChatMessage objects"
            )
            
            validation_result = messages_validator(messages)
            if validation_result.is_error:
                return validation_result
            
            # Save messages using ROP pipeline
            def save_message(msg: ChatMessage) -> Result[None, str]:
                # Set session_id if provided
                if session_id:
                    msg.thread_id = session_id
                return self.chat_repository.save_message(msg)
            
            # Use ROP to save all messages
            pipeline = self.rop_service.pipeline(
                *[lambda msgs, i=i: save_message(msgs[i]) for i in range(len(messages))]
            )
            
            save_result = pipeline(messages)
            if save_result.is_error:
                return save_result
            
            # Update session data if session_id provided
            if session_id and session_id in self._active_sessions:
                self._active_sessions[session_id]["message_count"] += len(messages)
                self._active_sessions[session_id]["last_activity"] = datetime.now()
                self._conversation_stats["total_messages"] += len(messages)
            
            return Result.success(None)
            
        except Exception as e:
            return Result.error(f"Failed to save conversation: {str(e)}")
    
    async def get_conversation_history(self, session_id: str, limit: int = 50) -> Result[List[ChatMessage], str]:
        """Get conversation history for a session"""
        try:
            if not session_id.strip():
                return Result.error("Session ID cannot be empty")
            
            # Get messages by thread (session_id)
            messages_result = await self.chat_repository.get_messages_by_thread(session_id, limit)
            if messages_result.is_error:
                return messages_result
            
            # Update session activity
            if session_id in self._active_sessions:
                self._active_sessions[session_id]["last_activity"] = datetime.now()
            
            return Result.success(messages_result.value)
            
        except Exception as e:
            return Result.error(f"Failed to get conversation history: {str(e)}")
    
    async def end_conversation(self, session_id: str) -> Result[None, str]:
        """End a conversation session"""
        try:
            if not session_id.strip():
                return Result.error("Session ID cannot be empty")
            
            if session_id not in self._active_sessions:
                return Result.error(f"Session '{session_id}' not found or already ended")
            
            # Update session status
            self._active_sessions[session_id]["status"] = "ended"
            self._active_sessions[session_id]["ended_at"] = datetime.now()
            self._conversation_stats["active_sessions"] -= 1
            
            return Result.success(None)
            
        except Exception as e:
            return Result.error(f"Failed to end conversation: {str(e)}")
    
    async def get_session_info(self, session_id: str) -> Result[Dict[str, Any], str]:
        """Get session information and statistics"""
        try:
            if not session_id.strip():
                return Result.error("Session ID cannot be empty")
            
            if session_id not in self._active_sessions:
                return Result.error(f"Session '{session_id}' not found")
            
            session_data = self._active_sessions[session_id]
            
            # Get message count from repository
            count_result = await self.chat_repository.get_message_count_by_thread(session_id)
            if count_result.is_error:
                return count_result
            
            session_info = {
                "session_id": session_id,
                "status": session_data["status"],
                "started_at": session_data["started_at"].isoformat(),
                "last_activity": session_data["last_activity"].isoformat(),
                "message_count": count_result.value,
                "context": session_data["context"]
            }
            
            if "ended_at" in session_data:
                session_info["ended_at"] = session_data["ended_at"].isoformat()
                session_info["duration_minutes"] = (
                    session_data["ended_at"] - session_data["started_at"]
                ).total_seconds() / 60
            
            return Result.success(session_info)
            
        except Exception as e:
            return Result.error(f"Failed to get session info: {str(e)}")
    
    async def get_active_sessions(self) -> Result[List[Dict[str, Any]], str]:
        """Get list of active sessions"""
        try:
            active_sessions = []
            
            for session_id, session_data in self._active_sessions.items():
                if session_data["status"] == "active":
                    active_sessions.append({
                        "session_id": session_id,
                        "started_at": session_data["started_at"].isoformat(),
                        "last_activity": session_data["last_activity"].isoformat(),
                        "message_count": session_data["message_count"],
                        "context": session_data["context"]
                    })
            
            return Result.success(active_sessions)
            
        except Exception as e:
            return Result.error(f"Failed to get active sessions: {str(e)}")
    
    async def get_conversation_stats(self) -> Result[Dict[str, Any], str]:
        """Get conversation statistics"""
        try:
            # Get additional stats from repository
            repo_stats_result = await self.chat_repository.get_conversation_stats()
            if repo_stats_result.is_error:
                return repo_stats_result
            
            # Combine stats
            combined_stats = {
                **self._conversation_stats,
                "repository_stats": repo_stats_result.value,
                "timestamp": datetime.now().isoformat()
            }
            
            return Result.success(combined_stats)
            
        except Exception as e:
            return Result.error(f"Failed to get conversation stats: {str(e)}")
    
    async def cleanup_inactive_sessions(self, hours_threshold: int = 24) -> Result[int, str]:
        """Clean up inactive sessions"""
        try:
            if hours_threshold <= 0:
                return Result.error("Hours threshold must be positive")
            
            cutoff_time = datetime.now().timestamp() - (hours_threshold * 3600)
            cleaned_count = 0
            
            sessions_to_remove = []
            for session_id, session_data in self._active_sessions.items():
                if session_data["last_activity"].timestamp() < cutoff_time:
                    sessions_to_remove.append(session_id)
            
            for session_id in sessions_to_remove:
                await self.end_conversation(session_id)
                cleaned_count += 1
            
            return Result.success(cleaned_count)
            
        except Exception as e:
            return Result.error(f"Failed to cleanup inactive sessions: {str(e)}")
    
    async def export_conversation(self, session_id: str, format: str = "json") -> Result[str, str]:
        """Export conversation to specified format"""
        try:
            if not session_id.strip():
                return Result.error("Session ID cannot be empty")
            
            # Get conversation history
            history_result = await self.get_conversation_history(session_id, 1000)
            if history_result.is_error:
                return history_result
            
            # Get session info
            session_info_result = await self.get_session_info(session_id)
            if session_info_result.is_error:
                return session_info_result
            
            if format.lower() == "json":
                import json
                export_data = {
                    "session_info": session_info_result.value,
                    "messages": [msg.to_dict() for msg in history_result.value],
                    "exported_at": datetime.now().isoformat()
                }
                return Result.success(json.dumps(export_data, ensure_ascii=False, indent=2))
            else:
                return Result.error(f"Unsupported export format: {format}")
                
        except Exception as e:
            return Result.error(f"Failed to export conversation: {str(e)}")
    
    async def search_conversations(self, query: str, limit: int = 10) -> Result[List[Dict[str, Any]], str]:
        """Search across all conversations"""
        try:
            if not query.strip():
                return Result.error("Search query cannot be empty")
            
            # Use repository search
            search_result = await self.chat_repository.search_messages(query, limit)
            if search_result.is_error:
                return search_result
            
            # Group by session/thread
            conversations = {}
            for message in search_result.value:
                thread_id = message.thread_id or "no_thread"
                if thread_id not in conversations:
                    conversations[thread_id] = {
                        "thread_id": thread_id,
                        "messages": [],
                        "match_count": 0
                    }
                conversations[thread_id]["messages"].append(message.to_dict())
                conversations[thread_id]["match_count"] += 1
            
            # Convert to list and sort by match count
            conversation_list = list(conversations.values())
            conversation_list.sort(key=lambda x: x["match_count"], reverse=True)
            
            return Result.success(conversation_list)
            
        except Exception as e:
            return Result.error(f"Failed to search conversations: {str(e)}")
