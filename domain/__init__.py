# domain/__init__.py
from .entities import ChatMessage, MessageRole, RAGChunk, QualityLevel
from .models import (
    BaseMetadata, RAGChunkMetadata, ChatMessageMetadata, 
    RAGMetadata, MessageMetadata,  # Clearer aliases
    MetadataFactory, MetadataType, MetadataField, 
    MetadataFieldRegistry, MetadataFieldMapper
)
from .utils.result import Result
from .services.rop_service import ROPService

__all__ = [
    'ChatMessage',
    'MessageRole',
    'RAGChunk', 
    'QualityLevel',
    'BaseMetadata',
    'RAGChunkMetadata',
    'RAGMetadata',  # Clearer alias
    'ChatMessageMetadata',
    'MessageMetadata',  # Clearer alias
    'MetadataFactory',
    'MetadataType',
    'MetadataField',
    'MetadataFieldRegistry',
    'MetadataFieldMapper',
    'Result',
    'ROPService'
]
