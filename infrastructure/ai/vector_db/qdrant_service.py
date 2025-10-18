# infrastructure/ai/vector_db/qdrant_service.py
import logging
from typing import List, Optional, AsyncIterator
from domain.services.IVectorDbService import IVectorDbService
from domain.entities.rag_chunk import RAGChunk
from domain.utils.result import Result
from .qdrant.collection_service import CollectionService
from .qdrant.embedding_service import EmbeddingService
from .qdrant.search_service import SearchService
from .qdrant.monitoring_service import MonitoringService
from ..embeddings.IEmbeddingService import IEmbeddingService
from domain.services.ITextCleanerService import ITextCleanerService

class QdrantService(IVectorDbService):
    """Qdrant implementation of VectorDbService using microservices architecture"""
    
    def __init__(self, url: str = "http://localhost:6333", collection_name: str = "chat_collection", api_key: Optional[str] = None, embedding_service: Optional[IEmbeddingService] = None, text_cleaner_service: Optional[ITextCleanerService] = None):
        self.url = url
        self.collection_name = collection_name
        self.vector_size = 1024  # Match C# VectorSize
        self.logger = logging.getLogger(__name__)
        
        # Initialize microservices
        self.collection_service = CollectionService(url, api_key)
        self.embedding_service = EmbeddingService(url, api_key)
        self.search_service = SearchService(url, api_key, text_cleaner_service)
        self.monitoring_service = MonitoringService(url, api_key)
        
        # Store embedding service for real embeddings
        self.embedding_service_provider = embedding_service
        
        self.logger.info(f"QdrantService initialized with microservices architecture (vector_size: {self.vector_size})")
    
    # Collection Management - delegated to CollectionService
    async def create_collection(self, vector_size: int = None, distance: str = "Cosine") -> Result[None, str]:
        """Create collection"""
        if vector_size is None:
            vector_size = self.vector_size
        return await self.collection_service.create_collection(self.collection_name, vector_size, distance)
    
    async def delete_collection(self) -> Result[None, str]:
        """Delete collection"""
        return await self.collection_service.delete_collection(self.collection_name)
    
    async def collection_exists(self) -> Result[bool, str]:
        """Check if collection exists"""
        return await self.collection_service.collection_exists(self.collection_name)
    
    async def get_collection_info(self) -> Result[dict, str]:
        """Get collection information"""
        return await self.collection_service.get_collection_info(self.collection_name)
    
    # Embedding Operations - delegated to EmbeddingService
    async def upsert_chunks(self, chunks: List[RAGChunk]) -> Result[None, str]:
        """Upsert RAG chunks as vectors"""
        self.logger.info(f"Upserting {len(chunks)} chunks to collection: {self.collection_name}")
        
        import uuid
        
        points = []
        for chunk in chunks:
            # Convert string ID to UUID if needed
            try:
                # Try to parse as UUID first
                if isinstance(chunk.chunk_id, str):
                    point_id = uuid.UUID(chunk.chunk_id)
                else:
                    point_id = chunk.chunk_id
            except (ValueError, TypeError):
                # Generate new UUID if chunk_id is not valid
                point_id = uuid.uuid4()
            
            # Get real embedding if embedding service is available
            if self.embedding_service_provider:
                # Handle case where embedding_service_provider might be a Result
                if hasattr(self.embedding_service_provider, 'is_success'):
                    if self.embedding_service_provider.is_success:
                        actual_service = self.embedding_service_provider.value
                    else:
                        self.logger.warning(f"Embedding service not available: {self.embedding_service_provider.error}")
                        vector = [0.1] * self.vector_size
                        continue
                else:
                    actual_service = self.embedding_service_provider
                
                embedding_result = await actual_service.create_embedding(chunk.text_chunk)
                if embedding_result.is_success:
                    vector = embedding_result.value
                    self.logger.debug(f"Using real embedding for chunk: {len(vector)} dimensions")
                else:
                    self.logger.warning(f"Failed to create embedding, using dummy vector: {embedding_result.error}")
                    vector = [0.1] * self.vector_size
            else:
                self.logger.warning("No embedding service available, using dummy vector")
                vector = [0.1] * self.vector_size
            
            point = {
                "id": str(point_id),  # Qdrant expects string representation
                "vector": vector,  # Real embedding or dummy fallback
                "payload": {
                    "text": chunk.text_chunk,
                    "score": chunk.score,
                    "metadata": chunk.get_metadata().to_dict() if chunk.get_metadata() else {}
                }
            }
            points.append(point)
        
        return await self.embedding_service.upsert_points(self.collection_name, points)
    
    async def delete_chunks(self, chunk_ids: List[str]) -> Result[None, str]:
        """Delete chunks by IDs"""
        return await self.embedding_service.delete_points(self.collection_name, chunk_ids)
    
    async def get_chunks(self, chunk_ids: List[str]) -> Result[List[RAGChunk], str]:
        """Get chunks by IDs"""
        result = await self.embedding_service.get_points(self.collection_name, chunk_ids)
        
        if result.is_error:
            return result
        
        chunks = []
        for point in result.value:
            chunk = RAGChunk(
                text_chunk=point.get("payload", {}).get("text", ""),
                chat_messages=None,  # Would be populated from payload
                chunk_id=str(point.get("id", "")),
                score=point.get("payload", {}).get("score", 0.0)
            )
            chunks.append(chunk)
        
        return Result.success(chunks)
    
    # Search Operations - delegated to SearchService
    async def search(self, query: str, limit: int = 5) -> Result[List[RAGChunk], str]:
        """Search vector database"""
        self.logger.info(f"QdrantService - Starting search for: '{query}' with limit: {limit}")
        print(f"DEBUG: QdrantService - Starting search for: '{query}' with limit: {limit}")
        
        result = await self.search_service.search_by_text(self.collection_name, query, limit, vector_size=self.vector_size, embedding_service=self.embedding_service_provider)
        
        if result.is_success:
            self.logger.info(f"QdrantService - Search successful, found {len(result.value)} chunks")
            print(f"DEBUG: QdrantService - Search successful, found {len(result.value)} chunks")
        else:
            self.logger.error(f"QdrantService - Search failed: {result.error}")
            print(f"DEBUG: QdrantService - Search failed: {result.error}")
        
        return result
    
    async def stream_search(self, query: str, limit: int = 5) -> AsyncIterator[Result[RAGChunk, str]]:
        """Stream search results"""
        # Get real embedding if embedding service is available
        if self.embedding_service_provider:
            # Handle case where embedding_service_provider might be a Result
            if hasattr(self.embedding_service_provider, 'is_success'):
                if self.embedding_service_provider.is_success:
                    actual_service = self.embedding_service_provider.value
                else:
                    self.logger.warning(f"Embedding service not available: {self.embedding_service_provider.error}")
                    search_vector = [0.1] * self.vector_size
            else:
                actual_service = self.embedding_service_provider
            
            embedding_result = await actual_service.create_embedding(query)
            if embedding_result.is_success:
                search_vector = embedding_result.value
                self.logger.debug(f"Using real embedding for search: {len(search_vector)} dimensions")
            else:
                self.logger.warning(f"Failed to create search embedding, using dummy vector: {embedding_result.error}")
                search_vector = [0.1] * self.vector_size
        else:
            self.logger.warning("No embedding service available for search, using dummy vector")
            search_vector = [0.1] * self.vector_size
        async for result in self.search_service.stream_search(self.collection_name, search_vector, limit):
            yield result
    
    async def save_chunk(self, chunk: RAGChunk) -> Result[None, str]:
        """Save a single RAG chunk to Qdrant"""
        return await self.upsert_chunks([chunk])
    
    async def search_similar(self, query_vector: List[float], limit: int = 5, score_threshold: Optional[float] = None) -> Result[List[RAGChunk], str]:
        """Search by vector similarity"""
        search_result = await self.search_service.search_vectors(
            self.collection_name, query_vector, limit, score_threshold
        )
        
        if search_result.is_error:
            return search_result
        
        chunks = []
        for result in search_result.value:
            chunk = RAGChunk(
                text_chunk=result.get("payload", {}).get("text", ""),
                chat_messages=None,
                chunk_id=str(result.get("id", "")),
                score=result.get("score", 0.0)
            )
            chunks.append(chunk)
        
        return Result.success(chunks)
    
    # Monitoring Operations - delegated to MonitoringService
    async def get_stats(self) -> Result[dict, str]:
        """Get collection statistics"""
        return await self.monitoring_service.get_collection_metrics(self.collection_name)
    
    async def get_system_info(self) -> Result[dict, str]:
        """Get system information"""
        return await self.monitoring_service.get_system_metrics()
    
    async def health_check(self) -> Result[dict, str]:
        """Check service health"""
        try:
            # Check all microservices health
            collection_health = await self.collection_service.health_check()
            embedding_health = await self.embedding_service.health_check()
            search_health = await self.search_service.health_check()
            monitoring_health = await self.monitoring_service.health_check()
            
            services_status = {
                'collection_service': {'status': 'healthy' if collection_health.is_success else 'error', 'error': collection_health.error if collection_health.is_error else None},
                'embedding_service': {'status': 'healthy' if embedding_health.is_success else 'error', 'error': embedding_health.error if embedding_health.is_error else None},
                'search_service': {'status': 'healthy' if search_health.is_success else 'error', 'error': search_health.error if search_health.is_error else None},
                'monitoring_service': {'status': 'healthy' if monitoring_health.is_success else 'error', 'error': monitoring_health.error if monitoring_health.is_error else None}
            }
            
            overall_status = 'healthy' if all(
                status.get('status') == 'healthy' for status in services_status.values()
            ) else 'degraded'
            
            health_data = {
                'status': overall_status,
                'url': self.url,
                'collection_name': self.collection_name,
                'architecture': 'microservices',
                'services': services_status,
                'timestamp': self.monitoring_service._get_timestamp()
            }
            
            return Result.success(health_data)
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return Result.error(f"Health check failed: {str(e)}")
    
    # Additional utility methods
    async def batch_search(self, queries: List[str], limit: int = 5) -> Result[List[List[RAGChunk]], str]:
        """Batch search multiple queries"""
        # Generate dummy vectors for batch search
        dummy_vectors = [[0.1] * self.vector_size for _ in queries]
        
        batch_result = await self.search_service.batch_search(self.collection_name, dummy_vectors, limit)
        
        if batch_result.is_error:
            return batch_result
        
        # Convert results to RAGChunk lists
        chunk_lists = []
        for result_set in batch_result.value:
            chunks = []
            for result in result_set:
                chunk = RAGChunk(
                    text_chunk=result.get("payload", {}).get("text", ""),
                    chat_messages=None,
                    chunk_id=str(result.get("id", "")),
                    score=result.get("score", 0.0)
                )
                chunks.append(chunk)
            chunk_lists.append(chunks)
        
        return Result.success(chunk_lists)
    
    async def recommend_similar(self, positive_chunk_ids: List[str], negative_chunk_ids: Optional[List[str]] = None, limit: int = 5) -> Result[List[RAGChunk], str]:
        """Recommend similar chunks"""
        recommend_result = await self.search_service.recommend_points(
            self.collection_name, positive_chunk_ids, negative_chunk_ids, limit
        )
        
        if recommend_result.is_error:
            return recommend_result
        
        chunks = []
        for result in recommend_result.value:
            chunk = RAGChunk(
                text_chunk=result.get("payload", {}).get("text", ""),
                chat_messages=None,
                chunk_id=str(result.get("id", "")),
                score=result.get("score", 0.0)
            )
            chunks.append(chunk)
        
        return Result.success(chunks)
