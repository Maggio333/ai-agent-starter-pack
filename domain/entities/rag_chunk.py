# domain/entities/rag_chunk.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import json
import re
from domain.entities.chat_message import ChatMessage
from domain.entities.quality_level import QualityLevel
from domain.models.metadata import RAGChunkMetadata, MetadataFactory

@dataclass
class RAGChunk:
    """Enhanced RAG chunk entity with validation and rich methods"""
    text_chunk: Optional[str]
    chat_messages: Optional[List[ChatMessage]]
    chunk_id: Optional[str] = None
    score: Optional[float] = None
    created_at: Optional[datetime] = None
    source: Optional[str] = None
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Initialize and validate chunk"""
        if self.chunk_id is None:
            self.chunk_id = f"chunk_{datetime.now().timestamp()}"
        
        if self.created_at is None:
            self.created_at = datetime.now()
        
        if self.metadata is None:
            self.metadata = {}
        
        # Validation
        if self.text_chunk and len(self.text_chunk.strip()) == 0:
            raise ValueError("Text chunk cannot be empty")
        
        # Note: Score can be negative for similarity search (cosine similarity)
        # We'll allow any float value for similarity scores
        # if self.score is not None and (self.score < 0 or self.score > 1):
        #     raise ValueError("Score must be between 0 and 1")
        
        if not self.text_chunk and not self.chat_messages:
            raise ValueError("Either text_chunk or chat_messages must be provided")
    
    # Rich Methods
    def is_high_quality(self) -> bool:
        """Check if chunk has high quality score"""
        return self.get_quality_level().is_high_quality
    
    def is_medium_quality(self) -> bool:
        """Check if chunk has medium quality score"""
        return self.get_quality_level().is_medium_quality
    
    def is_low_quality(self) -> bool:
        """Check if chunk has low quality score"""
        return self.get_quality_level().is_low_quality
    
    def has_chat_messages(self) -> bool:
        """Check if chunk has associated chat messages"""
        return self.chat_messages is not None and len(self.chat_messages) > 0
    
    def has_text_content(self) -> bool:
        """Check if chunk has text content"""
        return self.text_chunk is not None and len(self.text_chunk.strip()) > 0
    
    def is_empty(self) -> bool:
        """Check if chunk is empty"""
        return not self.has_text_content() and not self.has_chat_messages()
    
    # Content Analysis
    def get_text_length(self) -> int:
        """Get text length"""
        return len(self.text_chunk) if self.text_chunk else 0
    
    def get_word_count(self) -> int:
        """Get word count"""
        return len((self.text_chunk or "").split())
    
    def is_long_chunk(self) -> bool:
        """Check if chunk is considered long (>1000 chars)"""
        return self.get_text_length() > 1000
    
    def is_short_chunk(self) -> bool:
        """Check if chunk is considered short (<100 chars)"""
        return self.get_text_length() < 100
    
    def contains_code(self) -> bool:
        """Check if chunk contains code blocks"""
        return "```" in (self.text_chunk or "") or "<code>" in (self.text_chunk or "")
    
    def get_mentions(self) -> List[str]:
        """Extract @mentions from text"""
        return re.findall(r'@(\w+)', self.text_chunk or "")
    
    def get_hashtags(self) -> List[str]:
        """Extract #hashtags from text"""
        return re.findall(r'#(\w+)', self.text_chunk or "")
    
    def get_urls(self) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, self.text_chunk or "")
    
    def is_question(self) -> bool:
        """Check if chunk contains a question"""
        return (self.text_chunk or "").strip().endswith('?')
    
    def is_command(self) -> bool:
        """Check if chunk starts with command (/)"""
        return (self.text_chunk or "").strip().startswith('/')
    
    def get_command(self) -> Optional[str]:
        """Extract command if chunk is a command"""
        if self.is_command():
            parts = (self.text_chunk or "").strip().split()
            return parts[0][1:] if parts else None
        return None
    
    # Chat Message Analysis
    def get_user_messages_count(self) -> int:
        """Get count of user messages"""
        if not self.has_chat_messages():
            return 0
        return sum(1 for msg in self.chat_messages if msg.is_from_user())
    
    def get_assistant_messages_count(self) -> int:
        """Get count of assistant messages"""
        if not self.has_chat_messages():
            return 0
        return sum(1 for msg in self.chat_messages if msg.is_from_assistant())
    
    def get_system_messages_count(self) -> int:
        """Get count of system messages"""
        if not self.has_chat_messages():
            return 0
        return sum(1 for msg in self.chat_messages if msg.is_system_message())
    
    def get_total_messages_count(self) -> int:
        """Get total count of messages"""
        return len(self.chat_messages) if self.has_chat_messages() else 0
    
    # Serialization
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "text_chunk": self.text_chunk,
            "chat_messages": [msg.to_dict() for msg in (self.chat_messages or [])],
            "chunk_id": self.chunk_id,
            "score": self.score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "source": self.source,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RAGChunk':
        """Create from dictionary"""
        return cls(
            text_chunk=data.get("text_chunk"),
            chat_messages=[ChatMessage.from_dict(msg) for msg in (data.get("chat_messages") or [])],
            chunk_id=data.get("chunk_id"),
            score=data.get("score"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            source=data.get("source"),
            metadata=data.get("metadata")
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'RAGChunk':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    # Factory Methods
    @classmethod
    def create_from_text(cls, text: str, score: float = None, source: str = None) -> 'RAGChunk':
        """Create chunk from text"""
        return cls(
            text_chunk=text,
            chat_messages=None,
            score=score,
            source=source
        )
    
    @classmethod
    def create_from_messages(cls, messages: List[ChatMessage], score: float = None, source: str = None) -> 'RAGChunk':
        """Create chunk from chat messages"""
        return cls(
            text_chunk=None,
            chat_messages=messages,
            score=score,
            source=source
        )
    
    @classmethod
    def create_high_quality(cls, text: str, source: str = None) -> 'RAGChunk':
        """Create high quality chunk"""
        return cls(
            text_chunk=text,
            chat_messages=None,
            score=0.9,
            source=source
        )
    
    @classmethod
    def create_medium_quality(cls, text: str, source: str = None) -> 'RAGChunk':
        """Create medium quality chunk"""
        return cls(
            text_chunk=text,
            chat_messages=None,
            score=0.7,
            source=source
        )
    
    # Utility Methods
    def get_summary(self, max_length: int = 100) -> str:
        """Get summary of chunk content"""
        if self.text_chunk:
            if len(self.text_chunk) <= max_length:
                return self.text_chunk
            return self.text_chunk[:max_length-3] + "..."
        elif self.has_chat_messages():
            return f"Chat conversation with {self.get_total_messages_count()} messages"
        return "Empty chunk"
    
    def get_metadata(self) -> RAGChunkMetadata:
        """Get comprehensive chunk metadata using structured model"""
        return MetadataFactory.create_rag_chunk_metadata(
            chunk_id=self.chunk_id or "unknown",
            text_length=self.get_text_length(),
            word_count=self.get_word_count(),
            score=self.score,
            quality_level=self.get_quality_level().value,
            has_chat_messages=self.has_chat_messages(),
            has_text_content=self.has_text_content(),
            is_long=self.is_long_chunk(),
            is_short=self.is_short_chunk(),
            contains_code=self.contains_code(),
            is_question=self.is_question(),
            is_command=self.is_command(),
            mentions_count=len(self.get_mentions()),
            hashtags_count=len(self.get_hashtags()),
            urls_count=len(self.get_urls()),
            total_messages=self.get_total_messages_count(),
            user_messages=self.get_user_messages_count(),
            assistant_messages=self.get_assistant_messages_count(),
            system_messages=self.get_system_messages_count(),
            source=self.source,
            created_at=self.created_at or datetime.now()
        )
    
    def get_quality_level(self) -> QualityLevel:
        """Get quality level as enum"""
        return QualityLevel.from_score(self.score)
    
    def add_metadata(self, key: str, value: any) -> None:
        """Add metadata to chunk"""
        if self.metadata is None:
            self.metadata = {}
        self.metadata[key] = value
    
    def get_metadata_value(self, key: str, default: any = None) -> any:
        """Get metadata value"""
        return self.metadata.get(key, default) if self.metadata else default
    
    def __str__(self) -> str:
        """String representation"""
        quality = self.get_quality_level().value
        return f"[{quality}] {self.get_summary(50)}"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"RAGChunk(id={self.chunk_id}, score={self.score}, quality={self.get_quality_level().value}, content='{self.get_summary(30)}')"
