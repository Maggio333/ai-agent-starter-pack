# presentation/api/__init__.py
"""
API module for the presentation layer.

This module contains all REST API endpoints for the chat application.
"""

from .chat_endpoints import router as chat_router
from .models import (
    SessionCreateRequest,
    SessionResponse,
    ChatMessageResponse,
    ConversationHistoryResponse,
    ActiveSessionsResponse,
    ServiceHealthResponse,
    OverallHealthResponse,
    ServiceCapabilitiesResponse,
    ConversationStatsResponse,
    ErrorResponse,
    SuccessResponse
)

__all__ = [
    "chat_router",
    "SessionCreateRequest",
    "SessionResponse", 
    "ChatMessageResponse",
    "ConversationHistoryResponse",
    "ActiveSessionsResponse",
    "ServiceHealthResponse",
    "OverallHealthResponse",
    "ServiceCapabilitiesResponse",
    "ConversationStatsResponse",
    "ErrorResponse",
    "SuccessResponse"
]