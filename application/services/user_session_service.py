# application/services/user_session_service.py
from typing import Dict, List, Optional, Any
from datetime import datetime
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.entities.chat_message import ChatMessage, MessageRole
from application.services.conversation_service import ConversationService
from application.services.chat_agent_service import ChatAgentService
from application.services.orchestration_service import OrchestrationService

class UserSessionService:
    """Service for managing user sessions with context aggregation from multiple services"""
    
    def __init__(self, 
                 conversation_service: ConversationService,
                 chat_agent_service: ChatAgentService,
                 orchestration_service: OrchestrationService):
        self.rop_service = ROPService()
        self.conversation_service = conversation_service
        self.chat_agent_service = chat_agent_service
        self.orchestration_service = orchestration_service
        
        # Session context cache
        self._session_contexts = {}
        
    async def process_user_message(self, message: str, session_id: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Process user message with full context aggregation"""
        try:
            # Create session if not provided
            if not session_id:
                session_result = await self.conversation_service.start_conversation()
                if session_result.is_error:
                    return Result.error(f"Failed to create session: {session_result.error}")
                session_id = session_result.value
            
            # Get conversation history
            history_result = await self.conversation_service.get_conversation_history(session_id, limit=6)
            conversation_history = history_result.value if history_result.is_success else []
            
            # Determine if we need vector context (first message or new topic)
            vector_context = []
            if self._should_search_vector_db(conversation_history, message):
                vector_result = await self.chat_agent_service.search_knowledge_base(message)
                if vector_result.is_success:
                    vector_context = vector_result.value
                    # Cache vector context for this session
                    self._session_contexts[session_id] = {
                        'vector_context': vector_context,
                        'last_search': datetime.now(),
                        'search_query': message
                    }
            
            # Build enhanced message with all context
            enhanced_message = self._build_enhanced_message(
                message, 
                conversation_history, 
                vector_context
            )
            
            # Process through orchestration
            orchestration_result = await self.orchestration_service.process_request(enhanced_message, session_id)
            
            if orchestration_result.is_error:
                return Result.error(f"Orchestration failed: {orchestration_result.error}")
            
            response_data = orchestration_result.value
            ai_response = response_data.get("response", "No response available")
            
            # Save conversation to session
            user_message = ChatMessage(
                role=MessageRole.USER,
                content=message,
                timestamp=datetime.now()
            )
            ai_message = ChatMessage(
                role=MessageRole.ASSISTANT,
                content=ai_response,
                timestamp=datetime.now()
            )
            
            save_result = await self.conversation_service.save_conversation([user_message, ai_message], session_id)
            if save_result.is_error:
                return Result.error(f"Failed to save conversation: {save_result.error}")
            
            return Result.success({
                "response": ai_response,
                "session_id": session_id,
                "service_used": response_data.get("service_used", "unknown"),
                "metadata": response_data.get("metadata", {}),
                "vector_context_used": len(vector_context) > 0,
                "conversation_length": len(conversation_history) + 2
            })
            
        except Exception as e:
            return Result.error(f"Failed to process user message: {str(e)}")
    
    def _should_search_vector_db(self, conversation_history: List[ChatMessage], message: str) -> bool:
        """Determine if we should search vector database"""
        # Search vector DB if:
        # 1. First message in conversation
        # 2. New topic detected (simple keyword-based detection)
        # 3. No recent vector search
        
        if len(conversation_history) <= 2:
            return True
        
        # Simple topic detection
        message_lower = message.lower()
        topic_keywords = [
            "what", "how", "explain", "tell me", "describe", "define",
            "co to", "jak", "czym", "opisz", "wyjaśnij", "powiedz"
        ]
        
        if any(keyword in message_lower for keyword in topic_keywords):
            return True
        
        return False
    
    def _build_enhanced_message(self, 
                               message: str, 
                               conversation_history: List[ChatMessage], 
                               vector_context: List[Dict[str, Any]]) -> str:
        """Build enhanced message with all context"""
        enhanced_message = message
        
        # Add vector context if available
        if vector_context:
            vector_info = "\n".join([
                f"- {ctx.get('content', '')[:200]}..." 
                for ctx in vector_context[:3]
            ])
            enhanced_message = f"Relevant knowledge:\n{vector_info}\n\nUser question: {message}"
        
        # Add conversation history if available
        if conversation_history:
            context_info = "\n".join([
                f"{msg.role.value}: {msg.content[:100]}..."
                for msg in conversation_history[-3:]  # Last 3 messages
            ])
            enhanced_message = f"Previous conversation:\n{context_info}\n\nCurrent question: {message}"
        
        return enhanced_message
    
    async def get_session_summary(self, session_id: str) -> Result[Dict[str, Any], str]:
        """Get comprehensive session summary"""
        try:
            # Get session info
            session_result = await self.conversation_service.get_session_info(session_id)
            if session_result.is_error:
                return Result.error(f"Failed to get session info: {session_result.error}")
            
            # Get conversation history
            history_result = await self.conversation_service.get_conversation_history(session_id)
            conversation_history = history_result.value if history_result.is_success else []
            
            # Get cached context
            cached_context = self._session_contexts.get(session_id, {})
            
            return Result.success({
                "session_info": session_result.value,
                "message_count": len(conversation_history),
                "vector_context_cached": len(cached_context.get('vector_context', [])) > 0,
                "last_vector_search": cached_context.get('last_search'),
                "conversation_preview": [
                    {
                        "role": msg.role.value,
                        "content": msg.content[:100] + "..." if len(msg.content) > 100 else msg.content,
                        "timestamp": msg.timestamp.isoformat()
                    }
                    for msg in conversation_history[-5:]  # Last 5 messages
                ]
            })
            
        except Exception as e:
            return Result.error(f"Failed to get session summary: {str(e)}")
    
    async def clear_session_context(self, session_id: str) -> Result[None, str]:
        """Clear cached context for session"""
        try:
            if session_id in self._session_contexts:
                del self._session_contexts[session_id]
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to clear session context: {str(e)}")
    
    async def get_all_active_sessions(self) -> Result[List[Dict[str, Any]], str]:
        """Get all active sessions with their context"""
        try:
            sessions_result = await self.conversation_service.get_active_sessions()
            if sessions_result.is_error:
                return Result.error(f"Failed to get active sessions: {sessions_result.error}")
            
            sessions = sessions_result.value
            enhanced_sessions = []
            
            for session in sessions:
                session_id = session.get("session_id")
                if session_id:
                    summary_result = await self.get_session_summary(session_id)
                    if summary_result.is_success:
                        enhanced_sessions.append(summary_result.value)
            
            return Result.success(enhanced_sessions)
            
        except Exception as e:
            return Result.error(f"Failed to get enhanced sessions: {str(e)}")
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Health check for user session service"""
        try:
            # Check dependencies
            conversation_health = await self.conversation_service.health_check()
            orchestration_health = await self.orchestration_service.get_service_health()
            
            return Result.success({
                "service": "UserSessionService",
                "status": "healthy",
                "dependencies": {
                    "conversation_service": conversation_health.is_success,
                    "orchestration_service": orchestration_health.is_success,
                },
                "cached_sessions": len(self._session_contexts),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
