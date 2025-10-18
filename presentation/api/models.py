# presentation/api/models.py
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from domain.entities.chat_message import MessageRole


class SessionCreateRequest(BaseModel):
    """Request model for creating a new chat session"""
    context: Optional[Dict[str, Any]] = Field(default=None, description="Optional context for the session")
    system_prompt: Optional[str] = Field(default=None, description="Optional system prompt for the session")


class SessionResponse(BaseModel):
    """Response model for session information"""
    session_id: str = Field(..., description="Unique session identifier")
    status: str = Field(..., description="Session status (active, ended)")
    started_at: str = Field(..., description="Session start timestamp")
    last_activity: str = Field(..., description="Last activity timestamp")
    message_count: int = Field(..., description="Number of messages in session")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Session context")
    ended_at: Optional[str] = Field(default=None, description="Session end timestamp")
    duration_minutes: Optional[float] = Field(default=None, description="Session duration in minutes")


class ChatMessageResponse(BaseModel):
    """Response model for chat message"""
    message_id: str = Field(..., description="Unique message identifier")
    content: str = Field(..., description="Message content")
    role: str = Field(..., description="Message role (user, assistant, system, tool)")
    timestamp: str = Field(..., description="Message timestamp")
    thread_id: Optional[str] = Field(default=None, description="Thread/session identifier")
    parent_message_id: Optional[str] = Field(default=None, description="Parent message identifier")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Message metadata")


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history"""
    session_id: str = Field(..., description="Session identifier")
    messages: List[ChatMessageResponse] = Field(..., description="List of messages")
    total_count: int = Field(..., description="Total number of messages")


class ActiveSessionsResponse(BaseModel):
    """Response model for active sessions list"""
    sessions: List[SessionResponse] = Field(..., description="List of active sessions")
    total_count: int = Field(..., description="Total number of active sessions")


class ServiceHealthResponse(BaseModel):
    """Response model for service health check"""
    service_name: str = Field(..., description="Service name")
    status: str = Field(..., description="Service status (healthy, unhealthy, unknown)")
    response_time_ms: float = Field(..., description="Response time in milliseconds")
    message: str = Field(..., description="Status message")
    last_check: str = Field(..., description="Last check timestamp")


class OverallHealthResponse(BaseModel):
    """Response model for overall system health"""
    status: str = Field(..., description="Overall system status")
    message: str = Field(..., description="Overall status message")
    response_time_ms: float = Field(..., description="Overall response time")
    services: List[ServiceHealthResponse] = Field(..., description="Individual service health")
    timestamp: str = Field(..., description="Health check timestamp")


class ServiceCapabilityResponse(BaseModel):
    """Response model for service capabilities"""
    service_name: str = Field(..., description="Service name")
    capabilities: List[str] = Field(..., description="List of service capabilities")
    description: str = Field(..., description="Service description")


class ServiceCapabilitiesResponse(BaseModel):
    """Response model for all service capabilities"""
    services: List[ServiceCapabilityResponse] = Field(..., description="List of services and their capabilities")
    total_services: int = Field(..., description="Total number of services")


class ConversationStatsResponse(BaseModel):
    """Response model for conversation statistics"""
    total_sessions: int = Field(..., description="Total number of sessions")
    total_messages: int = Field(..., description="Total number of messages")
    active_sessions: int = Field(..., description="Number of active sessions")
    repository_stats: Dict[str, Any] = Field(..., description="Repository statistics")
    timestamp: str = Field(..., description="Statistics timestamp")


class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Error details")
    timestamp: str = Field(..., description="Error timestamp")


class SuccessResponse(BaseModel):
    """Response model for successful operations"""
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional data")
    timestamp: str = Field(..., description="Response timestamp")
