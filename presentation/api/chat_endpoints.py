# presentation/api/chat_endpoints.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from application.services.di_service import DIService
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
def get_di_service() -> DIService:
    """Get DI service instance"""
    return DIService()

def get_conversation_service(di_service: DIService = Depends(get_di_service)) -> ConversationService:
    """Get conversation service from DI service"""
    return di_service.get_conversation_service()

def get_orchestration_service(di_service: DIService = Depends(get_di_service)) -> OrchestrationService:
    """Get orchestration service from DI service"""
    return di_service.get_orchestration_service()

def get_health_service(di_service: DIService = Depends(get_di_service)) -> HealthService:
    """Get health service from DI service"""
    return di_service.get_health_service()

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
async def get_conversation_history(
    session_id: str,
    limit: int = 50,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Get conversation history for a session"""
    try:
        result = await conversation_service.get_conversation_history(session_id, limit)
        if result.is_error:
            raise HTTPException(status_code=404, detail=result.error)
        
        messages = result.value
        message_responses = [
            ChatMessageResponse(
                message_id=msg.message_id or "",
                content=msg.content,
                role=msg.role.value,
                timestamp=msg.timestamp.isoformat(),
                thread_id=msg.thread_id,
                parent_message_id=msg.parent_message_id,
                metadata=msg.get_metadata().to_dict() if hasattr(msg, 'get_metadata') else None
            )
            for msg in messages
        ]
        
        return ConversationHistoryResponse(
            session_id=session_id,
            messages=message_responses,
            total_count=len(message_responses)
        )
        
    except Exception as e:
        logger.error(f"Failed to get conversation history for {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/active", response_model=ActiveSessionsResponse)
async def get_active_sessions(
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """Get list of active sessions"""
    try:
        result = await conversation_service.get_active_sessions()
        if result.is_error:
            raise HTTPException(status_code=500, detail=result.error)
        
        sessions = result.value
        session_responses = [
            SessionResponse(
                session_id=session["session_id"],
                status=session.get("status", "active"),
                started_at=session["started_at"],
                last_activity=session["last_activity"],
                message_count=session["message_count"],
                context=session.get("context")
            )
            for session in sessions
        ]
        
        return ActiveSessionsResponse(
            sessions=session_responses,
            total_count=len(session_responses)
        )
        
    except Exception as e:
        logger.error(f"Failed to get active sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}", response_model=SuccessResponse)
async def end_session(
    session_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """End a conversation session"""
    try:
        result = await conversation_service.end_conversation(session_id)
        if result.is_error:
            raise HTTPException(status_code=404, detail=result.error)
        
        return SuccessResponse(
            message=f"Session {session_id} ended successfully",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Failed to end session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Statistics Endpoints
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

# Health Check Endpoints
@router.get("/health", response_model=OverallHealthResponse)
async def get_system_health(
    health_service: HealthService = Depends(get_health_service)
):
    """Get overall system health"""
    try:
        result = await health_service.get_overall_health()
        if result.is_error:
            raise HTTPException(status_code=500, detail=result.error)
        
        health_data = result.value
        
        # Get detailed health for individual services
        detailed_result = await health_service.get_detailed_health()
        services = []
        if detailed_result.is_success:
            for health_check in detailed_result.value:
                services.append(ServiceHealthResponse(
                    service_name=health_check.service_name,
                    status=health_check.status.value,
                    response_time_ms=health_check.response_time_ms,
                    message=health_check.message,
                    last_check=health_check.timestamp.isoformat()
                ))
        
        return OverallHealthResponse(
            status=health_data["status"],
            message=health_data["message"],
            response_time_ms=health_data["response_time_ms"],
            services=services,
            timestamp=health_data["timestamp"]
        )
        
    except Exception as e:
        logger.error(f"Failed to get system health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/capabilities", response_model=ServiceCapabilitiesResponse)
async def get_service_capabilities(
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Get service capabilities"""
    try:
        result = await orchestration_service.get_service_capabilities()
        if result.is_error:
            raise HTTPException(status_code=500, detail=result.error)
        
        capabilities = result.value
        service_capabilities = [
            ServiceCapabilityResponse(
                service_name=service_name,
                capabilities=service_caps,
                description=f"{service_name.title()} service capabilities"
            )
            for service_name, service_caps in capabilities.items()
        ]
        
        return ServiceCapabilitiesResponse(
            services=service_capabilities,
            total_services=len(service_capabilities)
        )
        
    except Exception as e:
        logger.error(f"Failed to get service capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Agent-specific Endpoints
@router.post("/agent/city-request")
async def process_city_request(
    city: str,
    session_id: Optional[str] = None,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Process a city information request using the agent"""
    try:
        result = await orchestration_service.process_city_request(city, session_id)
        if result.is_error:
            raise HTTPException(status_code=400, detail=result.error)
        
        return {
            "city": city,
            "data": result.value,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to process city request for {city}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent/weather/{city}")
async def get_weather(
    city: str,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Get weather information for a city"""
    try:
        result = await orchestration_service.process_weather_request(city, "current")
        if result.is_error:
            raise HTTPException(status_code=400, detail=result.error)
        
        return {
            "city": city,
            "weather": result.value,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get weather for {city}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent/time/{city}")
async def get_current_time(
    city: str,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """Get current time for a city"""
    try:
        result = await orchestration_service.process_time_request(city, "current")
        if result.is_error:
            raise HTTPException(status_code=400, detail=result.error)
        
        return {
            "city": city,
            "time": result.value,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get time for {city}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Utility Endpoints
@router.get("/ping", response_model=SuccessResponse)
async def ping():
    """Simple ping endpoint for health checks"""
    return SuccessResponse(
        message="Pong! API is running",
        timestamp=datetime.now().isoformat()
    )

@router.get("/info")
async def get_api_info():
    """Get API information"""
    return {
        "name": "ATS Reflectum Agent API",
        "version": "1.0.0",
        "description": "Advanced AI agent with Microservices Architecture",
        "features": [
            "Session Management",
            "Conversation History",
            "Health Monitoring",
            "Service Capabilities",
            "City Information",
            "Weather Data",
            "Time Services",
            "Knowledge Base"
        ],
        "architecture": "Clean Architecture with Microservices",
        "timestamp": datetime.now().isoformat()
    }
