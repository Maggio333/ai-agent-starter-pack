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
            return Result.error(f"Nieprawidłowa nazwa kolekcji: {collection_name}")
        
        if not self._validate_vector_dimension(query_vector):
            return Result.error("Nieprawidłowy wektor zapytania")
        
        if limit <= 0:
            return Result.error(f"Nieprawidłowy limit: {limit}")
        
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
        self.logger.info("=" * 80)
        self.logger.info(f"🔍 SEARCH SERVICE: search_by_text")
        self.logger.info(f"   Collection: {collection_name}")
        self.logger.info(f"   Query: '{query_text[:100]}...'")
        self.logger.info(f"   Limit: {limit}")
        self.logger.info(f"   Score threshold: {score_threshold}")
        self.logger.info(f"   Embedding service: {type(embedding_service).__name__ if embedding_service else 'None'}")
        self.logger.info("=" * 80)
        
        # Try to get real embedding if embedding service is available
        if embedding_service:
            self.logger.info(f"✅ Embedding service dostępny: {type(embedding_service).__name__}")
            
            try:
                self.logger.info(f"📤 Tworzę embedding dla zapytania: '{query_text[:100]}...'")
                embedding_result = await embedding_service.create_embedding(query_text)
                
                if embedding_result.is_success:
                    query_vector = embedding_result.value
                    self.logger.info(f"✅ Utworzono embedding: {len(query_vector)} wymiarów")
                    self.logger.info(f"   Przykładowe wartości: {query_vector[:5]}...")
                else:
                    self.logger.warning(f"⚠️ Nie udało się utworzyć embedding: {embedding_result.error}")
                    self.logger.warning(f"   Używam dummy vector!")
                    query_vector = [0.1] * vector_size
            except Exception as e:
                self.logger.error(f"❌ Błąd embedding service: {str(e)}")
                import traceback
                self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
                self.logger.warning(f"   Używam dummy vector!")
                query_vector = [0.1] * vector_size
        else:
            self.logger.warning("=" * 80)
            self.logger.warning("⚠️ BRAK EMBEDDING SERVICE - Używam dummy vector!")
            self.logger.warning("   To oznacza, że wyszukiwanie może nie działać poprawnie!")
            self.logger.warning("=" * 80)
            query_vector = [0.1] * vector_size
        
        self.logger.info(f"🔎 Rozpoczynam wyszukiwanie wektorowe z {len(query_vector)} wymiarami")
        
        search_result = await self.search_vectors(collection_name, query_vector, limit, score_threshold)
        
        if search_result.is_error:
            self.logger.error("=" * 80)
            self.logger.error(f"❌ BŁĄD WYSZUKIWANIA WEKTOROWEGO: {search_result.error}")
            self.logger.error("=" * 80)
            return search_result
        
        self.logger.info("=" * 80)
        self.logger.info(f"📥 Wyszukiwanie zwróciło {len(search_result.value)} surowych wyników")
        self.logger.info("=" * 80)
        
        if search_result.value:
            for i, result in enumerate(search_result.value[:3], 1):
                score = result.get('score', 0.0)
                result_id = result.get('id', 'N/A')
                self.logger.info(f"   Wynik {i}: ID={result_id}, Score={score:.4f}")
        else:
            self.logger.warning("⚠️ Brak wyników z wyszukiwania wektorowego!")
        
        # Convert search results to RAGChunk objects
        self.logger.info("=" * 80)
        self.logger.info(f"🔄 Konwertuję {len(search_result.value)} surowych wyników na RAGChunk")
        self.logger.info("=" * 80)
        
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
                            self.logger.warning(f"Nie udało się wyczyścić tekstu z payload: {clean_result.error}")
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
                                self.logger.warning(f"Nie udało się wyczyścić tekstu Payload: {clean_result.error}")
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
                                self.logger.warning(f"Nie udało się wyczyścić tekstu Temat: {clean_result.error}")
                                text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
                        else:
                            text_content = str(raw_text).encode('utf-8', errors='ignore').decode('utf-8')
            except Exception as e:
                safe_exception_str = str(e).encode('utf-8', errors='ignore').decode('utf-8')
                self.logger.warning(f"Nie udało się wyodrębnić tekstu z payload: {safe_exception_str}")
                text_content = f"Fragment {result.get('id', 'nieznany')}"
            
            # If still no text, use a fallback
            if not text_content:
                text_content = f"Fragment {result.get('id', 'nieznany')}"
            
            # Clean text to avoid encoding issues
            clean_text = text_content.encode('utf-8', errors='ignore').decode('utf-8')
            self.logger.info(f"SearchService - Processing result {i+1}: {clean_text[:50]}...")
            
            # Clean all fields to avoid encoding issues
            safe_chunk_id = str(result.get("id", "")).encode('utf-8', errors='ignore').decode('utf-8')
            safe_score = result.get("score", 0.0)
            
            # Extract metadata from payload
            metadata = {}
            if "metadata" in payload:
                metadata = payload["metadata"]
            elif "meta" in payload:
                metadata = payload["meta"]
            elif "Meta" in payload:
                metadata = payload["Meta"]
            
            chunk = RAGChunk(
                text_chunk=clean_text,  # Use cleaned text
                chat_messages=None,  # Would be populated from payload
                chunk_id=safe_chunk_id,
                metadata=metadata,  # Include metadata from payload
                score=safe_score
            )
            chunks.append(chunk)
        
        self.logger.info("=" * 80)
        self.logger.info(f"✅ Skonwertowano {len(chunks)} wyników na RAGChunk")
        if chunks:
            for i, chunk in enumerate(chunks[:3], 1):
                self.logger.info(f"   Chunk {i}: ID={chunk.chunk_id}, Score={chunk.score:.4f}, Text='{chunk.text_chunk[:80]}...'")
        self.logger.info("=" * 80)
        
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
            return Result.error(f"Nieprawidłowa nazwa kolekcji: {collection_name}")
        
        if not query_vectors:
            return Result.error("Nie podano wektorów zapytania")
        
        # Validate all vectors
        for i, vector in enumerate(query_vectors):
            if not self._validate_vector_dimension(vector):
                return Result.error(f"Nieprawidłowy wektor na indeksie {i}")
        
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
            return Result.error(f"Nieprawidłowa nazwa kolekcji: {collection_name}")
        
        if not positive_ids:
            return Result.error("Nie podano pozytywnych ID")
        
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
