# domain/services/vector_db_service.py
from abc import ABC, abstractmethod
from typing import List, AsyncIterator
from domain.entities.rag_chunk import RAGChunk
from domain.utils.result import Result

class VectorDbService(ABC):
    """Vector database service interface"""
    
    @abstractmethod
    async def search(self, query: str, limit: int = 5) -> Result[List[RAGChunk], str]:
        """Search vector database"""
        pass
    
    @abstractmethod
    async def stream_search(self, query: str, limit: int = 5) -> AsyncIterator[Result[RAGChunk, str]]:
        """Stream search results"""
        pass
    
    @abstractmethod
    async def save_chunk(self, chunk: RAGChunk) -> Result[None, str]:
        """Save chunk to vector database"""
        pass
