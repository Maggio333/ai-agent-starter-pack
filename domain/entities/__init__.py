# domain/entities/__init__.py
from .chat_message import ChatMessage, MessageRole
from .rag_chunk import RAGChunk
from .quality_level import QualityLevel

__all__ = [
    'ChatMessage',
    'MessageRole', 
    'RAGChunk',
    'QualityLevel'
]
