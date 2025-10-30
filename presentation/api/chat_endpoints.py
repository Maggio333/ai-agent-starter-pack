"""
Chat API Endpoints - FastAPI routes for chat operations
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import json
import asyncio
from pydantic import BaseModel

from application.services.di_service import DIService
from application.container import Container
from application.services.conversation_service import ConversationService
from application.services.orchestration_service import OrchestrationService
from application.services.chat_agent_service import ChatAgentService
from application.services.prompt_service import PromptService
from application.services.dynamic_rag_service import DynamicRAGService
from domain.models.rag_result import RAGResult, RAGContextFormatter
from infrastructure.monitoring.health.health_service import HealthService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.utils.result import Result

from .models import (
    SessionCreateRequest, SessionResponse, ChatMessageResponse, 
    ConversationHistoryResponse, ActiveSessionsResponse,
    ServiceHealthResponse, OverallHealthResponse, ServiceCapabilitiesResponse,
    ConversationStatsResponse, ErrorResponse, SuccessResponse
)

# Initialize router
# Pydantic models for request/response
class MessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency injection
def get_container() -> Container:
    """Get Container instance"""
    return Container()

def get_conversation_service(container: Container = Depends(get_container)) -> ConversationService:
    """Get conversation service instance"""
    return container.conversation_service()

def get_orchestration_service(container: Container = Depends(get_container)) -> OrchestrationService:
    """Get orchestration service instance"""
    return container.orchestration_service()

def get_chat_agent_service(container: Container = Depends(get_container)):
    """Get ChatAgentService instance"""
    return container.chat_agent_service()

def get_health_service(container: Container = Depends(get_container)) -> HealthService:
    """Get health service instance"""
    return container.health_service()


# Session Management Endpoints
@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    request: SessionCreateRequest,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Create a new chat session"""
    try:
        context = {}
        if request.context:
            context.update(request.context)
        if request.system_prompt:
            context["system_prompt"] = request.system_prompt
        
        result = await conversation_service.start_conversation(context)
        if result.is_error:
            raise HTTPException(status_code=400, detail=result.error)
        
        session_id = result.value
        
        # Get session info
        session_info_result = await conversation_service.get_session_info(session_id)
        if session_info_result.is_error:
            raise HTTPException(status_code=500, detail=session_info_result.error)
        
        session_info = session_info_result.value
        return SessionResponse(**session_info)
        
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Get session information"""
    try:
        result = await conversation_service.get_session_info(session_id)
        if result.is_error:
            raise HTTPException(status_code=404, detail=result.error)
        
        session_info = result.value
        return SessionResponse(**session_info)
        
    except Exception as e:
        logger.error(f"Failed to get session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/history", response_model=ConversationHistoryResponse)
async def get_session_history(
    session_id: str,
    limit: int = 50,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Get session conversation history"""
    try:
        result = await conversation_service.get_conversation_history(session_id, limit)
        if result.is_error:
            raise HTTPException(status_code=404, detail=result.error)
        
        history = result.value
        return ConversationHistoryResponse(
            session_id=session_id,
            messages=history,
            total_messages=len(history)
        )
        
    except Exception as e:
        logger.error(f"Failed to get session history {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/active", response_model=ActiveSessionsResponse)
async def get_active_sessions(
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Get all active sessions"""
    try:
        result = await conversation_service.get_active_sessions()
        if result.is_error:
            raise HTTPException(status_code=500, detail=result.error)
        
        sessions = result.value
        return ActiveSessionsResponse(
            sessions=sessions,
            total_active=len(sessions)
        )
        
    except Exception as e:
        logger.error(f"Failed to get active sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}", response_model=SuccessResponse)
async def delete_session(
    session_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Delete a session"""
    try:
        result = await conversation_service.end_conversation(session_id)
        if result.is_error:
            raise HTTPException(status_code=404, detail=result.error)
        
        return SuccessResponse(message=f"Session {session_id} deleted successfully")
        
    except Exception as e:
        logger.error(f"Failed to delete session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Statistics and Health Endpoints
@router.get("/stats", response_model=ConversationStatsResponse)
async def get_conversation_stats(
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Get conversation statistics"""
    try:
        result = await conversation_service.get_conversation_stats()
        if result.is_error:
            raise HTTPException(status_code=500, detail=result.error)
        
        stats = result.value
        return ConversationStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Failed to get conversation stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=OverallHealthResponse)
async def get_overall_health(
    health_service: HealthService = Depends(get_health_service)
):
    """Get overall system health"""
    try:
        result = await health_service.get_overall_health()
        if result.is_error:
            raise HTTPException(status_code=500, detail=result.error)
        
        health_data = result.value
        return OverallHealthResponse(**health_data)
        
    except Exception as e:
        logger.error(f"Failed to get overall health: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities", response_model=ServiceCapabilitiesResponse)
async def get_service_capabilities(
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Get service capabilities"""
    try:
        result = await orchestration_service.get_capabilities()
        if result.is_error:
            raise HTTPException(status_code=500, detail=result.error)
        
        capabilities = result.value
        return ServiceCapabilitiesResponse(**capabilities)
        
    except Exception as e:
        logger.error(f"Failed to get service capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Agent Endpoints
@router.post("/agent/city-request")
async def city_request(
    request: Dict[str, Any],
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Handle city-related requests"""
    try:
        city = request.get("city", "")
        if not city:
            raise HTTPException(status_code=400, detail="City is required")
        
        result = await orchestration_service.handle_city_request(city)
        if result.is_error:
            raise HTTPException(status_code=400, detail=result.error)
        
        return {"status": "ok", "result": result.value}
        
    except Exception as e:
        logger.error(f"City request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/weather/{city}")
async def get_weather(
    city: str,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Get weather for a city"""
    try:
        result = await orchestration_service.get_weather(city)
        if result.is_error:
            raise HTTPException(status_code=400, detail=result.error)
        
        return {"status": "ok", "weather": result.value}
        
    except Exception as e:
        logger.error(f"Weather request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/time/{city}")
async def get_time(
    city: str,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Get time for a city"""
    try:
        result = await orchestration_service.get_time(city)
        if result.is_error:
            raise HTTPException(status_code=400, detail=result.error)
        
        return {"status": "ok", "time": result.value}
        
    except Exception as e:
        logger.error(f"Time request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Core Chat Endpoints
@router.get("/ping", response_model=SuccessResponse)
async def ping():
    """Simple ping endpoint"""
    return SuccessResponse(message="pong", timestamp=datetime.now().isoformat())


@router.post("/send")
async def send_message(
    request: Dict[str, Any],
    chat_agent_service = Depends(get_chat_agent_service),
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Send a message to the AI agent with conversation context and vector search using ChatAgentService"""
    try:
        message = request.get("message", "")
        conversation_context = request.get("conversation_context", [])
        vector_context = request.get("vector_context", [])
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        logger.info(f"Received message: {message}")
        logger.info(f"Conversation context: {len(conversation_context)} messages")
        logger.info(f"Vector context: {len(vector_context)} results")
        
        # Use ChatAgentService for knowledge search if vector context is empty
        if not vector_context and conversation_context:
            # Search knowledge base using ChatAgentService
            knowledge_result = await chat_agent_service.search_knowledge_base(message)
            if knowledge_result.is_success:
                vector_context = knowledge_result.value
        
        # Build enhanced message with context
        enhanced_message = message
        
        # Add vector context to message if available
        if vector_context:
            vector_info = "\n".join([
                f"- {ctx.get('content', '')[:200]}..." 
                for ctx in vector_context[:3]  # Limit to top 3 results
            ])
            enhanced_message = f"Context from knowledge base:\n{vector_info}\n\nUser question: {message}"
        
        # Use orchestration service to process the request
        result = await orchestration_service.process_request(enhanced_message)
        
        if result.is_success:
            response = result.value.get("response", "No response available")
            logger.info(f"AI response: {response}")
            return {
                "status": "ok",
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.error(f"Orchestration service error: {result.error}")
            raise HTTPException(status_code=500, detail=result.error)
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/send")
async def send_chat_message(
    request: Dict[str, Any],
    chat_agent_service: ChatAgentService = Depends(get_chat_agent_service),
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Send a message to the AI agent - Flutter app endpoint"""
    # Delegate to the main send_message function
    return await send_message(request, chat_agent_service, orchestration_service)


@router.post("/vector/search")
async def search_vector_database(
    request: Dict[str, Any],
    chat_agent_service: ChatAgentService = Depends(get_chat_agent_service)
):
    """Search vector database for relevant knowledge using ChatAgentService"""
    try:
        query = request.get("query", "")
        limit = request.get("limit", 5)
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        logger.info(f"Vector search query: {query}")
        
        # Use ChatAgentService for knowledge search
        result = await chat_agent_service.search_knowledge_base(query)
        
        if result.is_success:
            # Convert knowledge base results to simple dictionaries
            results = []
            for knowledge_item in result.value:
                # Extract facts from knowledge item
                facts = knowledge_item.get("facts", [])
                for fact in facts[:limit]:  # Limit facts per item
                    results.append({
                        "content": fact,
                        "source": knowledge_item.get("topic", "unknown"),
                        "score": knowledge_item.get("score", 0.0),
                        "metadata": {"source": "knowledge_base"}
                    })
            
            # Limit total results
            results = results[:limit]
            
            logger.info(f"Vector search returned {len(results)} results")
            return {
                "status": "ok",
                "results": results,
                "query": query,
                "count": len(results),
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.error(f"Knowledge search error: {result.error}")
            raise HTTPException(status_code=500, detail=result.error)
            
    except Exception as e:
        logger.error(f"Error in vector search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_chat_info():
    """Get chat service information"""
    return {
        "service": "Chat API",
        "version": "1.0.0",
        "description": "AI Chat API using LM Studio",
        "endpoints": [
            "/sessions - Session management",
            "/send - Send messages",
            "/health - Health check",
            "/capabilities - Service capabilities"
        ],
        "status": "active"
    }


@router.get("/knowledge/stats")
async def get_knowledge_stats(
    chat_agent_service: ChatAgentService = Depends(get_chat_agent_service)
):
    """Get knowledge base statistics using ChatAgentService"""
    try:
        result = await chat_agent_service.get_knowledge_stats()
        
        if result.is_success:
            return {
                "status": "ok",
                "stats": result.value,
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.error(f"Knowledge stats error: {result.error}")
            raise HTTPException(status_code=500, detail=result.error)
            
    except Exception as e:
        logger.error(f"Error getting knowledge stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities")
async def get_service_capabilities(
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Get capabilities of all services using OrchestrationService"""
    try:
        result = await orchestration_service.get_service_capabilities()
        
        if result.is_success:
            return {
                "status": "ok",
                "capabilities": result.value,
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.error(f"Capabilities error: {result.error}")
            raise HTTPException(status_code=500, detail=result.error)
            
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def _get_idioms_context(chat_agent_service: ChatAgentService, collection_name: str = "CuratedIdiomsForAI"):
    """Pobiera idiomy z wybranej kolekcji - centralizowana funkcja"""
    # Użyj bezpiecznego zapytania bez specjalnych znaków
    general_query = "IDIOM_REFLECT REFLECTIVE THINKING CONCEPTS"
    
    logger.info(f"🔍 KROK 3: Pobieranie idiomów z kolekcji '{collection_name}'...")
    
    # Pobierz vector_db_service bezpośrednio z knowledge_service
    knowledge_service = chat_agent_service.orchestration_service.knowledge_service
    
    if knowledge_service and knowledge_service.vector_db_service:
        # Użyj search_by_text z konkretną nazwą kolekcji
        from infrastructure.ai.vector_db.qdrant.search_service import SearchService
        from domain.services.ITextCleanerService import ITextCleanerService
        
        # Stwórz tymczasowy serwis wyszukiwania dla konkretnej kolekcji
        search_service = SearchService(
            url="http://localhost:6333",
            text_cleaner_service=knowledge_service.text_cleaner_service
        )
        
        # Wykonaj wyszukiwanie w docelowej kolekcji
        search_result = await search_service.search_by_text(
            collection_name=collection_name,
            query_text=general_query,
            limit=20,  # TopK20
            vector_size=1024,
            embedding_service=knowledge_service.vector_db_service.embedding_service_provider
        )
        
        if search_result.is_success:
            idioms_chunks = search_result.value
            logger.info(f"✅ Znaleziono {len(idioms_chunks)} idiomów w kolekcji '{collection_name}'")
            return idioms_chunks
        else:
            logger.warning(f"⚠️ Błąd wyszukiwania w kolekcji '{collection_name}': {search_result.error}")
            return []
    else:
        logger.warning("⚠️ Vector DB Service nie jest dostępny")
        return []

@router.post("/message")
async def send_simple_message(
    request: MessageRequest,
    container: Container = Depends(get_container),
    orchestration_service: OrchestrationService = Depends(get_orchestration_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
    chat_agent_service: ChatAgentService = Depends(get_chat_agent_service)
):
    """Ulepszony endpoint wiadomości z przetwarzaniem RAG w stylu ChatElioraReflect"""
    try:
        message = request.message
        session_id = request.session_id
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        logger.info(f"🔄 Processing message: {message}")
        
        # STEP 1: Create session if not provided
        if not session_id:
            session_result = await conversation_service.start_conversation()
            if session_result.is_error:
                raise HTTPException(status_code=500, detail=session_result.error)
            session_id = session_result.value
            logger.info(f"📝 Created new session: {session_id}")
        
        # KROK 2: Pobieranie serwisów z Container (w stylu ChatElioraReflect)
        prompt_service = container.prompt_service()
        dynamic_rag_service = container.dynamic_rag_service()
        
        # TODO: Pobierać kontekst użytkownika gdy system logowania zostanie zaimplementowany
        user_context = None  # {"role": "user", "permissions": ["read_chat"]}
        
        # KROK 3: Pobieranie idiomów z bazy wektorowej (Prompt Systemowy) - centralizowana funkcja
        idioms_context = await _get_idioms_context(chat_agent_service)
        logger.info(f"📚 Znaleziono {len(idioms_context)} wyników idiomów")
        
        # Konwertuje idiomy na listę stringów dla PromptService
        idioms_strings = []
        if idioms_context:
            from domain.entities.rag_chunk import RAGChunk
            logger.info(f"🔍 DEBUG: Znaleziono {len(idioms_context)} idiomów")
            
            for i, chunk in enumerate(idioms_context):
                if isinstance(chunk, RAGChunk):
                    content = chunk.text_chunk
                    logger.info(f"📝 Idiom {i+1}/{len(idioms_context)}: '{content[:100]}...'")
                    idioms_strings.append(content)
                else:
                    logger.warning(f"⚠️ Nieoczekiwany typ: {type(chunk)}")
                    idioms_strings.append(str(chunk) if chunk else "")
        
        # KROK 4: Pobieranie historii rozmowy
        logger.info(f"💬 KROK 4: Pobieranie historii dla session_id: {session_id}")
        history_result = await conversation_service.get_conversation_history(session_id, limit=6)
        conversation_history = history_result.value if history_result.is_success else []
        if history_result.is_error:
            logger.error(f"❌ Błąd pobierania historii: {history_result.error}")
        logger.info(f"💬 KROK 4: Pobrano {len(conversation_history)} wiadomości rozmowy")
        for i, msg in enumerate(conversation_history, 1):
            logger.info(f"💬   Wiadomość {i}: {msg.role.value} - thread_id: {msg.thread_id} - {msg.content[:50]}...")
        
        # KROK 5: Użycie Dynamic RAG Service do decyzji o zapytaniu wektorowym (w stylu ChatElioraReflect)
        logger.info(f"🤖 KROK 5: Używanie Dynamic RAG Service do decyzji o zapytaniu wektorowym...")
        dynamic_query_result = await dynamic_rag_service.decide_vector_query(
            conversation_context=conversation_history,
            current_message=message,
            user_context=user_context
        )
        
        dynamic_vector_results = []
        if dynamic_query_result.is_success:
            dynamic_query = dynamic_query_result.value
            logger.info(f"🧠 Dynamic RAG zdecydował o zapytaniu: {dynamic_query}")
            
            # Wykonuje dynamiczne wyszukiwanie wektorowe z filtrowaniem
            dynamic_search_result = await dynamic_rag_service.search_with_filtering(
                query=dynamic_query,
                score_threshold=0.75,  # Zmniejszone z 0.85 dla lepszej ilości wyników
                limit=5,  # TopK5
                user_context=user_context
            )
            
            if dynamic_search_result.is_success:
                dynamic_vector_results = dynamic_search_result.value
                logger.info(f"📚 Dynamic RAG znalazł {len(dynamic_vector_results)} przefiltrowanych wyników (TopK5)")
            else:
                logger.warning(f"⚠️ Dynamic RAG search nie powiodło się: {dynamic_search_result.error}")
        else:
            logger.warning(f"⚠️ Dynamic RAG query decision nie powiodło się: {dynamic_query_result.error}")
        
        # KROK 6: Budowanie kompletnej listy wiadomości używając PromptService (w stylu ChatElioraReflect)
        logger.info(f"🎭 KROK 6: Budowanie kompletnej listy wiadomości z PromptService")
        complete_messages = prompt_service.build_complete_message_list(
            user_message=message,
            idioms=idioms_strings,
            conversation_history=conversation_history,
            user_context=user_context
        )
        
        # Dodaje dynamiczny kontekst RAG jeśli dostępny
        if dynamic_vector_results:
            # Konwertuje na obiekty RAGResult
            rag_results = [RAGResult.from_vector_result(result) for result in dynamic_vector_results]
            
            # Formatuje jako wiadomość systemową
            rag_context = RAGContextFormatter.format_as_system_message(
                rag_results=rag_results,
                system_query=dynamic_query_result.value if dynamic_query_result.is_success else "",
                user_context=user_context
            )

            logger.info(f"Dynamic RAG: {rag_context}")
            
            # Dodaje jako wiadomość systemową
            complete_messages.insert(-1, ChatMessage(
                role=MessageRole.SYSTEM,
                content=rag_context,
                timestamp=datetime.now()
            ))        
        
        # KROK 7: Przetwarzanie przez LLM
        llm_service = chat_agent_service.llm_service
        response_parts = []
        async for chunk in prompt_service.send_to_llm_streaming(complete_messages, llm_service):
            response_parts.append(chunk)
        
        response = "".join(response_parts)
        
        # KROK 8: Zapisywanie rozmowy
        user_message = ChatMessage(
            role=MessageRole.USER,
            content=message,
            timestamp=datetime.now()
        )
        ai_message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response,
            timestamp=datetime.now()
        )
        
        save_result = await conversation_service.save_conversation([user_message, ai_message], session_id)
        if save_result.is_error:
            logger.error(f"Błąd zapisywania rozmowy: {save_result.error}")
        
        # Pobiera liczbę wyników wektorowych bezpiecznie
        dynamic_vector_count = len(dynamic_vector_results) if dynamic_vector_results else 0
        
        return {
            "status": "ok",
            "response": response,
            "session_id": session_id,
            "service_used": "prompt_service_streaming",
            "idioms_used": len(idioms_strings) > 0,
            "dynamic_rag_performed": dynamic_query_result.is_success,
            "dynamic_vector_results_count": dynamic_vector_count,
            "conversation_length": len(conversation_history) + 2,
            "user_context": user_context,  # TODO: Usunąć gdy system logowania zostanie zaimplementowany
            "timestamp": datetime.now().isoformat()
        }
            
    except Exception as e:
        logger.error(f"Błąd przetwarzania wiadomości: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message/stream")
async def send_message_streaming(
    request: MessageRequest,
    container: Container = Depends(get_container),
    orchestration_service: OrchestrationService = Depends(get_orchestration_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
    chat_agent_service: ChatAgentService = Depends(get_chat_agent_service)
):
    """Streaming endpoint z Server-Sent Events (SSE) dla czasu rzeczywistego"""
    
    async def generate_stream():
        try:
            message = request.message
            session_id = request.session_id
            
            if not message:
                yield f"data: {json.dumps({'error': 'Message is required'})}\n\n"
                return
           
            if not session_id:
                session_result = await conversation_service.start_conversation()
                if session_result.is_error:
                    yield f"data: {json.dumps({'error': session_result.error})}\n\n"
                    return
                session_id = session_result.value     

            # Wyślij informację o sesji
            yield f"data: {json.dumps({'type': 'session', 'session_id': session_id})}\n\n"
            
            # KROK 2: Pobieranie serwisów z Container
            prompt_service = container.prompt_service()
            dynamic_rag_service = container.dynamic_rag_service()
            user_context = None
            
            # KROK 3: Pobieranie idiomów - centralizowana funkcja
            yield f"data: {json.dumps({'type': 'status', 'message': 'Pobieranie idiomów...'})}\n\n"
            
            idioms_context = await _get_idioms_context(chat_agent_service)
            
            idioms_strings = []
            if idioms_context:
                from domain.entities.rag_chunk import RAGChunk
                for chunk in idioms_context:
                    if isinstance(chunk, RAGChunk):
                        idioms_strings.append(chunk.text_chunk)
                    else:
                        idioms_strings.append(str(chunk) if chunk else "")
            
            yield f"data: {json.dumps({'type': 'status', 'message': f'Znaleziono {len(idioms_strings)} idiomów'})}\n\n"
            
            # KROK 4: Historia rozmowy
            history_result = await conversation_service.get_conversation_history(session_id, limit=6)
            conversation_history = history_result.value if history_result.is_success else []
            if history_result.is_error:
                logger.error(f"Błąd pobierania historii: {history_result.error}")
            
            # # KROK 5: Dynamic RAG
            # yield f"data: {json.dumps({'type': 'status', 'message': 'Analizowanie kontekstu...'})}\n\n"
            
            dynamic_query_result = await dynamic_rag_service.decide_vector_query(
                conversation_context=conversation_history,
                current_message=message,
                user_context=user_context
            )
            
            dynamic_vector_results = []
            if dynamic_query_result.is_success:
                dynamic_query = dynamic_query_result.value
                yield f"data: {json.dumps({'type': 'status', 'message': f'Dynamic RAG: {dynamic_query[:50]}...'})}\n\n"
                dynamic_search_result = await dynamic_rag_service.search_with_filtering(
                    query=dynamic_query,
                    score_threshold=0.75,  # Zmniejszone z 0.85 dla lepszej ilości wyników
                    limit=5,
                    user_context=user_context
                )
                if dynamic_search_result.is_success:
                    dynamic_vector_results = dynamic_search_result.value
                    yield f"data: {json.dumps({'type': 'status', 'message': f'Znaleziono {len(dynamic_vector_results)} wyników RAG'})}\n\n"
                

            # KROK 6: Budowanie wiadomości
            complete_messages = prompt_service.build_complete_message_list(
                user_message=message,
                idioms=idioms_strings,
                conversation_history=conversation_history,
                user_context=user_context
            )
            
            if dynamic_vector_results:
                 from domain.models.rag_result import RAGResult, RAGContextFormatter
                 rag_results = [RAGResult.from_vector_result(result) for result in dynamic_vector_results]
                 rag_context = RAGContextFormatter.format_as_system_message(
                     rag_results=rag_results,
                     system_query=dynamic_query_result.value if dynamic_query_result.is_success else "",
                     user_context=user_context
                 )
                
                 complete_messages.insert(-1, ChatMessage(
                     role=MessageRole.SYSTEM,
                     content=rag_context,
                     timestamp=datetime.now()
                 ))
            
            # KROK 7: Streaming LLM
            yield f"data: {json.dumps({'type': 'status', 'message': 'Generowanie odpowiedzi...'})}\n\n"
            
            # 🎯 LOGOWANIE KOŃCOWEJ STRUKTURY KONTEKSTU
            #logger.info(f"🎯 KOŃCOWA STRUKTURA KONTEKSTU ({len(complete_messages)} wiadomości):")
            #for i, msg in enumerate(complete_messages, 1):
            #    logger.info(f"   {i}. {msg.role.value.upper()}: {len(msg.content)} znaków")
            #    if msg.role == MessageRole.SYSTEM and "KONTEKST Z PAMIĘCI" in msg.content:
            #        logger.info(f"      ⭐ TO JEST RAG CONTEXT!")
            
            llm_service = chat_agent_service.llm_service
            response_parts = []
            chunk_count = 0
            
            logger.info(f"🔄 Rozpoczynam streaming z LLM...") 
            async for chunk in prompt_service.send_to_llm_streaming(complete_messages, llm_service):
                chunk_count += 1
                if chunk:
                    response_parts.append(chunk)
                    # Wyślij chunk do klienta
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                    await asyncio.sleep(0.01)  # Małe opóźnienie dla płynności
            
            response = "".join(response_parts)
            #logger.info(f"✅ Streaming zakończony: {chunk_count} chunków, {response.count} znaków odpowiedzi")
            
            #if not response or not response.strip():
            #    logger.error(f"❌ CRITICAL: LLM zwróciło pustą odpowiedź! chunk_count={chunk_count}, response_parts={len(response_parts)}")
            
            # KROK 8: Zapisywanie
            user_message = ChatMessage(
                role=MessageRole.USER,
                content=message,
                timestamp=datetime.now()
            )
            
            if response and response.strip():
                ai_message = ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=response,
                    timestamp=datetime.now()
                )
                
                save_result = await conversation_service.save_conversation([user_message, ai_message], session_id)
                if save_result.is_error:
                    logger.error(f"Błąd zapisywania rozmowy: {save_result.error}")
            
            # Koniec streamingu
            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"
            
        except Exception as e:
            logger.error(f"Błąd streamingu: {e}")
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )