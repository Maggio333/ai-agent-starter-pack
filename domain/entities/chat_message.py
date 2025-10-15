# domain/entities/chat_message.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum
import re
import json
from domain.models.metadata import ChatMessageMetadata, MetadataFactory

class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

@dataclass
class ChatMessage:
    """Enhanced Chat message entity with validation and rich methods"""
    content: str
    role: MessageRole
    timestamp: datetime
    message_id: Optional[str] = None
    file_name: Optional[str] = None
    thread_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    
    def __post_init__(self):
        """Initialize and validate message"""
        if self.message_id is None:
            self.message_id = f"{self.timestamp.timestamp()}_{self.role.value}"
        
        # Validation
        if not self.content or not self.content.strip():
            raise ValueError("Content cannot be empty")
        
        if len(self.content) > 50000:  # 50KB limit
            raise ValueError("Content too long (max 50KB)")
    
    # Rich Methods
    def is_from_user(self) -> bool:
        """Check if message is from user"""
        return self.role == MessageRole.USER
    
    def is_from_assistant(self) -> bool:
        """Check if message is from assistant"""
        return self.role == MessageRole.ASSISTANT
    
    def is_system_message(self) -> bool:
        """Check if message is system message"""
        return self.role == MessageRole.SYSTEM
    
    def is_tool_message(self) -> bool:
        """Check if message is tool message"""
        return self.role == MessageRole.TOOL
    
    def has_attachment(self) -> bool:
        """Check if message has file attachment"""
        return self.file_name is not None
    
    def is_reply(self) -> bool:
        """Check if message is a reply to another message"""
        return self.parent_message_id is not None
    
    def is_thread_starter(self) -> bool:
        """Check if message starts a new thread"""
        return self.thread_id is not None and not self.is_reply()
    
    # Content Analysis
    def get_word_count(self) -> int:
        """Get word count of content"""
        return len(self.content.split())
    
    def get_character_count(self) -> int:
        """Get character count of content"""
        return len(self.content)
    
    def is_long_message(self) -> bool:
        """Check if message is considered long (>1000 chars)"""
        return self.get_character_count() > 1000
    
    def contains_code(self) -> bool:
        """Check if message contains code blocks"""
        return "```" in self.content or "<code>" in self.content
    
    def get_mentions(self) -> List[str]:
        """Extract @mentions from content"""
        return re.findall(r'@(\w+)', self.content)
    
    def get_hashtags(self) -> List[str]:
        """Extract #hashtags from content"""
        return re.findall(r'#(\w+)', self.content)
    
    def get_urls(self) -> List[str]:
        """Extract URLs from content"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, self.content)
    
    def is_question(self) -> bool:
        """Check if message is a question"""
        return self.content.strip().endswith('?')
    
    def is_command(self) -> bool:
        """Check if message starts with command (/)"""
        return self.content.strip().startswith('/')
    
    def get_command(self) -> Optional[str]:
        """Extract command if message is a command"""
        if self.is_command():
            parts = self.content.strip().split()
            return parts[0][1:] if parts else None
        return None
    
    # Serialization
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "content": self.content,
            "role": self.role.value,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
            "file_name": self.file_name,
            "thread_id": self.thread_id,
            "parent_message_id": self.parent_message_id
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ChatMessage':
        """Create from dictionary"""
        return cls(
            content=data["content"],
            role=MessageRole(data["role"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            message_id=data.get("message_id"),
            file_name=data.get("file_name"),
            thread_id=data.get("thread_id"),
            parent_message_id=data.get("parent_message_id")
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ChatMessage':
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    # Factory Methods
    @classmethod
    def create_user_message(cls, content: str, thread_id: Optional[str] = None, 
                          parent_message_id: Optional[str] = None) -> 'ChatMessage':
        """Create user message"""
        return cls(
            content=content,
            role=MessageRole.USER,
            timestamp=datetime.now(),
            thread_id=thread_id,
            parent_message_id=parent_message_id
        )
    
    @classmethod
    def create_assistant_message(cls, content: str, thread_id: Optional[str] = None,
                               parent_message_id: Optional[str] = None) -> 'ChatMessage':
        """Create assistant message"""
        return cls(
            content=content,
            role=MessageRole.ASSISTANT,
            timestamp=datetime.now(),
            thread_id=thread_id,
            parent_message_id=parent_message_id
        )
    
    @classmethod
    def create_system_message(cls, content: str) -> 'ChatMessage':
        """Create system message"""
        return cls(
            content=content,
            role=MessageRole.SYSTEM,
            timestamp=datetime.now()
        )
    
    # Utility Methods
    def get_summary(self, max_length: int = 100) -> str:
        """Get summary of message content"""
        if len(self.content) <= max_length:
            return self.content
        
        return self.content[:max_length-3] + "..."
    
    def get_metadata(self) -> ChatMessageMetadata:
        """Get message metadata using structured model"""
        return MetadataFactory.create_chat_message_metadata(
            message_id=self.message_id or "unknown",
            word_count=self.get_word_count(),
            character_count=self.get_character_count(),
            has_attachment=self.has_attachment(),
            is_reply=self.is_reply(),
            is_long_message=self.is_long_message(),
            contains_code=self.contains_code(),
            is_question=self.is_question(),
            is_command=self.is_command(),
            mentions_count=len(self.get_mentions()),
            hashtags_count=len(self.get_hashtags()),
            urls_count=len(self.get_urls()),
            thread_id=self.thread_id,
            parent_message_id=self.parent_message_id,
            created_at=self.timestamp
        )
    
    def __str__(self) -> str:
        """String representation"""
        return f"[{self.role.value}] {self.get_summary(50)}"
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"ChatMessage(id={self.message_id}, role={self.role.value}, content='{self.get_summary(30)}')"
