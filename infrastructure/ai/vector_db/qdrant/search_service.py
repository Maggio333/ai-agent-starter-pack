# infrastructure/ai/vector_db/qdrant/search_service.py
from typing import List, Dict, Any, Optional, AsyncIterator
from domain.entities.rag_chunk import RAGChunk
from domain.utils.result import Result
from .base_qdrant_service import BaseQdrantService

class SearchService(BaseQdrantService):
    """Service for searching vectors in Qdrant"""
    
    async def search_vectors(self, collection_name: str, query_vector: List[float], limit: int = 5, 
                           score_threshold: Optional[float] = None, filter_conditions: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]], str]:
        """Search for similar vectors"""
        self.logger.info(f"Searching vectors in collection: {collection_name}, limit: {limit}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        if not self._validate_vector_dimension(query_vector):
            return Result.error("Invalid query vector")
        
        if limit <= 0:
            return Result.error(f"Invalid limit: {limit}")
        
        data = {
            "vector": query_vector,
            "limit": limit,
            "with_payload": True,
            "with_vector": False
        }
        
        if score_threshold is not None:
            data["score_threshold"] = score_threshold
        
        if filter_conditions:
            data["filter"] = filter_conditions
        
        result = await self._make_request("POST", f"/collections/{collection_name}/points/search", data)
        
        if result.is_success:
            search_results = result.value.get("result", [])
            self.logger.info(f"Found {len(search_results)} results in {collection_name}")
            return Result.success(search_results)
        else:
            self.logger.error(f"Search failed: {result.error}")
            return result
    
    async def search_by_text(self, collection_name: str, query_text: str, limit: int = 5, 
                           score_threshold: Optional[float] = None, vector_size: int = 1024) -> Result[List[RAGChunk], str]:
        """Search by text (requires text embedding)"""
        self.logger.info(f"Searching by text in collection: {collection_name}, query: '{query_text[:50]}...'")
        
        # In a real implementation, you would embed the text here
        # For now, we'll use a dummy vector with correct size
        dummy_vector = [0.1] * vector_size  # Use correct vector size
        
        search_result = await self.search_vectors(collection_name, dummy_vector, limit, score_threshold)
        
        if search_result.is_error:
            return search_result
        
        # Convert search results to RAGChunk objects
        chunks = []
        for result in search_result.value:
            payload = result.get("payload", {})
            
            # Extract text from different payload structures
            text_content = ""
            if "text" in payload:
                text_content = payload.get("text", "")
            elif "Akcja" in payload and isinstance(payload["Akcja"], dict):
                # Handle Polish structure: payload.Akcja.Payload
                akcja = payload["Akcja"]
                if "Payload" in akcja:
                    text_content = akcja["Payload"]
                elif "Temat" in akcja:
                    text_content = akcja["Temat"]
            
            # If still no text, use a fallback
            if not text_content:
                text_content = f"Chunk {result.get('id', 'unknown')}"
            
            chunk = RAGChunk(
                text_chunk=text_content,
                chat_messages=None,  # Would be populated from payload
                chunk_id=str(result.get("id", "")),
                score=result.get("score", 0.0)
            )
            chunks.append(chunk)
        
        self.logger.info(f"Converted {len(chunks)} search results to RAGChunk objects")
        return Result.success(chunks)
    
    async def stream_search(self, collection_name: str, query_vector: List[float], limit: int = 5) -> AsyncIterator[Result[RAGChunk, str]]:
        """Stream search results"""
        self.logger.info(f"Streaming search results from collection: {collection_name}")
        
        search_result = await self.search_vectors(collection_name, query_vector, limit)
        
        if search_result.is_error:
            yield search_result
            return
        
        # Yield results one by one
        for result in search_result.value:
            chunk = RAGChunk(
                text_chunk=result.get("payload", {}).get("text", ""),
                chat_messages=None,
                chunk_id=str(result.get("id", "")),
                score=result.get("score", 0.0)
            )
            yield Result.success(chunk)
    
    async def batch_search(self, collection_name: str, query_vectors: List[List[float]], limit: int = 5) -> Result[List[List[Dict[str, Any]]], str]:
        """Batch search multiple queries"""
        self.logger.info(f"Batch searching {len(query_vectors)} queries in collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        if not query_vectors:
            return Result.error("No query vectors provided")
        
        # Validate all vectors
        for i, vector in enumerate(query_vectors):
            if not self._validate_vector_dimension(vector):
                return Result.error(f"Invalid vector at index {i}")
        
        data = {
            "searches": [
                {
                    "vector": vector,
                    "limit": limit,
                    "with_payload": True,
                    "with_vector": False
                }
                for vector in query_vectors
            ]
        }
        
        result = await self._make_request("POST", f"/collections/{collection_name}/points/search/batch", data)
        
        if result.is_success:
            batch_results = result.value.get("result", [])
            self.logger.info(f"Batch search completed: {len(batch_results)} result sets")
            return Result.success(batch_results)
        else:
            self.logger.error(f"Batch search failed: {result.error}")
            return result
    
    async def recommend_points(self, collection_name: str, positive_ids: List[str], negative_ids: Optional[List[str]] = None, 
                              limit: int = 5) -> Result[List[Dict[str, Any]], str]:
        """Recommend points based on positive and negative examples"""
        self.logger.info(f"Recommending points in collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        if not positive_ids:
            return Result.error("No positive IDs provided")
        
        data = {
            "positive": positive_ids,
            "limit": limit,
            "with_payload": True,
            "with_vector": False
        }
        
        if negative_ids:
            data["negative"] = negative_ids
        
        result = await self._make_request("POST", f"/collections/{collection_name}/points/recommend", data)
        
        if result.is_success:
            recommendations = result.value.get("result", [])
            self.logger.info(f"Generated {len(recommendations)} recommendations")
            return Result.success(recommendations)
        else:
            self.logger.error(f"Recommendation failed: {result.error}")
            return result
