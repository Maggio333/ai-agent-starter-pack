"""
Chat API Endpoints - FastAPI routes for chat operations
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from application.services.di_service import DIService
from application.container import Container
from application.services.conversation_service import ConversationService
from application.services.orchestration_service import OrchestrationService
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
    orchestration_service: OrchestrationService = Depends(get_orchestration_service),
    container: Container = Depends(get_container)
):
    """Send a message to the AI agent using our LMStudioLLMService"""
    try:
        message = request.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        logger.info(f"Received message: {message}")
        
        # Use our LLM service from DI
        llm_service = container.llm_service()
        
        # Create ChatMessage
        chat_message = ChatMessage(
            role=MessageRole.USER,
            content=message,
            timestamp=datetime.now()
        )
        
        # Get completion using our service
        result = await llm_service.get_completion([chat_message])
        
        if result.is_success:
            response = result.value
            logger.info(f"AI response: {response}")
            return {
                "status": "ok",
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
        else:
            logger.error(f"LLM service error: {result.error}")
            raise HTTPException(status_code=500, detail=result.error)
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/send")
async def send_chat_message(
    request: Dict[str, Any],
    orchestration_service: OrchestrationService = Depends(get_orchestration_service),
    container: Container = Depends(get_container)
):
    """Send a message to the AI agent - Flutter app endpoint"""
    # Delegate to the main send_message function
    return await send_message(request, orchestration_service, container)


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