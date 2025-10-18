# infrastructure/ai/vector_db/qdrant/search_service.py
import logging
from typing import List, Dict, Any, Optional, AsyncIterator
from domain.entities.rag_chunk import RAGChunk
from domain.utils.result import Result
from .BaseQdrantService import BaseQdrantService
from infrastructure.ai.embeddings.IEmbeddingService import IEmbeddingService
from domain.services.ITextCleanerService import ITextCleanerService

class SearchService(BaseQdrantService):
    """Service for searching vectors in Qdrant"""
    
    def __init__(self, url: str, api_key: Optional[str] = None, text_cleaner_service: Optional[ITextCleanerService] = None):
        super().__init__(url, api_key)
        self.text_cleaner_service = text_cleaner_service
    
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
                           score_threshold: Optional[float] = None, vector_size: int = 1024, embedding_service=None) -> Result[List[RAGChunk], str]:
        """Search by text using embedding service"""
        self.logger.info(f"SearchService - Searching by text in collection: {collection_name}, query: '{query_text[:50]}...'")
        print(f"DEBUG: SearchService - Searching by text in collection: {collection_name}, query: '{query_text[:50]}...'")
        
        # Try to get real embedding if embedding service is available
        if embedding_service:
            self.logger.info(f"SearchService - Using embedding service: {type(embedding_service).__name__}")
            print(f"DEBUG: SearchService - Using embedding service: {type(embedding_service).__name__}")
            
            try:
                embedding_result = await embedding_service.create_embedding(query_text)
                if embedding_result.is_success:
                    query_vector = embedding_result.value
                    self.logger.info(f"SearchService - Created real embedding: {len(query_vector)} dimensions")
                    print(f"DEBUG: SearchService - Created real embedding: {len(query_vector)} dimensions")
                else:
                    self.logger.warning(f"SearchService - Failed to create embedding, using dummy vector: {embedding_result.error}")
                    print(f"DEBUG: SearchService - Failed to create embedding, using dummy vector: {embedding_result.error}")
                    query_vector = [0.1] * vector_size
            except Exception as e:
                self.logger.warning(f"SearchService - Embedding service error, using dummy vector: {str(e)}")
                print(f"DEBUG: SearchService - Embedding service error, using dummy vector: {str(e)}")
                query_vector = [0.1] * vector_size
        else:
            self.logger.warning(f"SearchService - No embedding service available, using dummy vector")
            print(f"DEBUG: SearchService - No embedding service available, using dummy vector")
            query_vector = [0.1] * vector_size
        
        self.logger.info(f"SearchService - Starting vector search with {len(query_vector)} dimensions")
        print(f"DEBUG: SearchService - Starting vector search with {len(query_vector)} dimensions")
        
        search_result = await self.search_vectors(collection_name, query_vector, limit, score_threshold)
        
        if search_result.is_error:
            self.logger.error(f"SearchService - Vector search failed: {search_result.error}")
            print(f"DEBUG: SearchService - Vector search failed: {search_result.error}")
            return search_result
        
        self.logger.info(f"SearchService - Vector search returned {len(search_result.value)} raw results")
        print(f"DEBUG: SearchService - Vector search returned {len(search_result.value)} raw results")
        
        # Convert search results to RAGChunk objects
        self.logger.info(f"SearchService - Converting {len(search_result.value)} raw results to RAGChunk objects")
        print(f"DEBUG: SearchService - Converting {len(search_result.value)} raw results to RAGChunk objects")
        
        chunks = []
        for i, result in enumerate(search_result.value):
            payload = result.get("payload", {})
            
            # Extract text from different payload structures with encoding safety
            text_content = ""
            try:
                if "text" in payload:
                    raw_text = payload.get("text", "")
                    # Clean the text before processing
                    if self.text_cleaner_service:
                        clean_result = await self.text_cleaner_service.clean_text(str(raw_text))
                        if clean_result.is_success:
                            text_content = clean_result.value
                        else:
                            self.logger.warning(f"Failed to clean text from payload: {clean_result.error}")
                            text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
                    else:
                        text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
                elif "Akcja" in payload and isinstance(payload["Akcja"], dict):
                    # Handle Polish structure: payload.Akcja.Payload
                    akcja = payload["Akcja"]
                    if "Payload" in akcja:
                        raw_text = akcja["Payload"]
                        # Clean the text before processing
                        if self.text_cleaner_service:
                            clean_result = await self.text_cleaner_service.clean_text(str(raw_text))
                            if clean_result.is_success:
                                text_content = clean_result.value
                            else:
                                self.logger.warning(f"Failed to clean Payload text: {clean_result.error}")
                                text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
                        else:
                            text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
                    elif "Temat" in akcja:
                        raw_text = akcja["Temat"]
                        # Clean the text before processing
                        if self.text_cleaner_service:
                            clean_result = await self.text_cleaner_service.clean_text(str(raw_text))
                            if clean_result.is_success:
                                text_content = clean_result.value
                            else:
                                self.logger.warning(f"Failed to clean Temat text: {clean_result.error}")
                                text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
                        else:
                            text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
            except Exception as e:
                safe_exception_str = str(e).encode('utf-8', errors='ignore').decode('utf-8')
                self.logger.warning(f"Failed to extract text from payload: {safe_exception_str}")
                text_content = f"Chunk {result.get('id', 'unknown')}"
            
            # If still no text, use a fallback
            if not text_content:
                text_content = f"Chunk {result.get('id', 'unknown')}"
            
            # Clean text to avoid encoding issues
            clean_text = text_content.encode('utf-8', errors='ignore').decode('utf-8')
            self.logger.info(f"SearchService - Processing result {i+1}: {clean_text[:50]}...")
            safe_text = clean_text[:50].encode('utf-8', errors='ignore').decode('utf-8')
            print(f"DEBUG: SearchService - Processing result {i+1}: {safe_text}...")
            
            # Clean all fields to avoid encoding issues
            safe_chunk_id = str(result.get("id", "")).encode('utf-8', errors='ignore').decode('utf-8')
            safe_score = result.get("score", 0.0)
            
            chunk = RAGChunk(
                text_chunk=clean_text,  # Use cleaned text
                chat_messages=None,  # Would be populated from payload
                chunk_id=safe_chunk_id,
                score=safe_score
            )
            chunks.append(chunk)
        
        self.logger.info(f"SearchService - Successfully converted {len(chunks)} results to RAGChunk objects")
        safe_count = str(len(chunks)).encode('utf-8', errors='ignore').decode('utf-8')
        print(f"DEBUG: SearchService - Successfully converted {safe_count} results to RAGChunk objects")
        
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
