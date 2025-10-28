# services/knowledge_service.py
import logging
from typing import Dict, List, Optional, Any
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.services.IVectorDbService import IVectorDbService
from domain.services.ITextCleanerService import ITextCleanerService
from domain.services.IKnowledgeService import IKnowledgeService
from domain.entities.rag_chunk import RAGChunk
from datetime import datetime

class KnowledgeService(IKnowledgeService):
    """Microservice for knowledge base operations and RAG functionality"""
    
    def __init__(self, vector_db_service: Optional[IVectorDbService] = None, text_cleaner_service: Optional[ITextCleanerService] = None):
        self.rop_service = ROPService()
        self.vector_db_service = vector_db_service
        self.text_cleaner_service = text_cleaner_service
        self.logger = logging.getLogger(__name__)
        
        # Debug logging
        self.logger.info(f"KnowledgeService initialized with vector_db_service: {vector_db_service is not None}")
        if vector_db_service:
            self.logger.info(f"Vector DB service type: {type(vector_db_service).__name__}")
        else:
            self.logger.warning("Vector DB service is None - will use local knowledge base only")
        
        self._search_history = []
    
    async def search_knowledge_base(self, query: str, limit: int = 5) -> Result[List[Dict[str, Any]], str]:
        """Search knowledge base using vector database and ROP patterns"""
        try:
            query_lower = query.lower().strip()
            
            # Validation using ROP
            query_validator = self.rop_service.validate(
                lambda q: len(q.strip()) > 0 and len(q.strip()) < 2000,
                "Query must be between 1 and 2000 characters"
            )
            
            validation_result = query_validator(query_lower)
            if validation_result.is_error:
                return validation_result
            
            # Try vector database search first using ROP
            if self.vector_db_service:
                # Clean query using TextCleanerService to avoid Unicode issues
                if self.text_cleaner_service:
                    clean_result = await self.text_cleaner_service.clean_text(query)
                    if clean_result.is_success:
                        clean_query = clean_result.value
                        self.logger.info(f"KnowledgeService - cleaned query: '{clean_query[:100]}...'")
                    else:
                        clean_query = query.encode('utf-8', errors='ignore').decode('utf-8')
                        self.logger.warning(f"KnowledgeService - TextCleanerService failed: {clean_result.error}, using basic UTF-8 cleaning")
                else:
                    clean_query = query.encode('utf-8', errors='ignore').decode('utf-8')
                    self.logger.warning("KnowledgeService - TextCleanerService not available, using basic UTF-8 cleaning")
                
                self.logger.info(f"KnowledgeService - vector_db_service is available, searching for: '{clean_query[:100]}...'")
                print(f"DEBUG: KnowledgeService - vector_db_service is available, searching for: '{clean_query[:100]}...'")
                
                # Search vector database directly with cleaned query
                vector_results = await self.vector_db_service.search(clean_query, limit=limit)
                self.logger.info(f"KnowledgeService - vector search result: success={vector_results.is_success}, value_count={len(vector_results.value) if vector_results.is_success else 0}")
                print(f"DEBUG: KnowledgeService - vector search result: success={vector_results.is_success}, value_count={len(vector_results.value) if vector_results.is_success else 0}")
                
                if vector_results.is_success and vector_results.value:
                    # Convert vector results to knowledge base format
                    self.logger.info(f"KnowledgeService - converting {len(vector_results.value)} vector results to knowledge base format")
                    print(f"DEBUG: KnowledgeService - converting {len(vector_results.value)} vector results to knowledge base format")
                    
                    results = []
                    for i, chunk in enumerate(vector_results.value):
                        # Clean text to avoid encoding issues
                        clean_text = chunk.text_chunk.encode('utf-8', errors='ignore').decode('utf-8')
                        self.logger.info(f"KnowledgeService - processing chunk {i+1}: {clean_text[:50]}...")
                        safe_text = clean_text[:50].encode('utf-8', errors='ignore').decode('utf-8')
                        print(f"DEBUG: KnowledgeService - processing chunk {i+1}: {safe_text}...")
                        
                        results.append({
                            "topic": chunk.source or "unknown",  # Używamy source zamiast topic
                            "score": chunk.score,
                            "facts": [clean_text],
                            "total_facts": 1,
                            "source": "vector_db"
                        })
                    
                    self.logger.info(f"KnowledgeService - returning {len(results)} results from vector database")
                    print(f"DEBUG: KnowledgeService - returning {len(results)} results from vector database")
                    return Result.success(results)
                else:
                    self.logger.warning("KnowledgeService - Vector database search returned no results or failed.")
                    print("DEBUG: KnowledgeService - Vector database search returned no results or failed.")
                    # No fallback - return empty results
                    return Result.success([])
            else:
                self.logger.warning("KnowledgeService - Vector DB service not available.")
                print("DEBUG: KnowledgeService - Vector DB service not available.")
                # No fallback - return empty results
                return Result.success([])
        except Exception as e:
            error_message = f"Failed to search knowledge base: {str(e)}"
            self.logger.error(error_message)
            print(f"ERROR: KnowledgeService - {error_message}")
            return Result.error(error_message)
    
    async def add_knowledge(self, topic: str, facts: List[str]) -> Result[bool, str]:
        """Add knowledge to the base - not implemented (vector DB only)"""
        self.logger.warning("add_knowledge not implemented - using vector DB only")
        return Result.success(True)
    
    async def get_knowledge_stats(self) -> Result[Dict[str, Any], str]:
        """Get knowledge base statistics"""
        try:
            stats = {
                'vector_db_available': self.vector_db_service is not None,
                'text_cleaner_available': self.text_cleaner_service is not None,
                'search_history_count': len(self._search_history),
                'service_type': 'vector_db_only'
            }
            return Result.success(stats)
        except Exception as e:
            return Result.error(f"Failed to get knowledge stats: {str(e)}")
    
    async def get_topic_facts(self, topic: str) -> Result[List[str], str]:
        """Get facts for a topic - not implemented (vector DB only)"""
        self.logger.warning("get_topic_facts not implemented - using vector DB only")
        return Result.success([])
    
    async def search_similar_topics(self, topic: str) -> Result[List[Dict[str, Any]], str]:
        """Search similar topics - not implemented (vector DB only)"""
        self.logger.warning("search_similar_topics not implemented - using vector DB only")
        return Result.success([])
    
    async def create_rag_chunk(self, text: str, topic: str) -> Result[Dict[str, Any], str]:
        """Create RAG chunk - not implemented (vector DB only)"""
        self.logger.warning("create_rag_chunk not implemented - using vector DB only")
        return Result.success({"text": text, "topic": topic, "created_at": datetime.now().isoformat()})
    
    async def get_search_history(self) -> Result[List[Dict[str, Any]], str]:
        """Get search history"""
        try:
            history = [
                {
                    "query": entry.get("query", ""),
                    "timestamp": entry.get("timestamp", ""),
                    "results_count": entry.get("results_count", 0)
                }
                for entry in self._search_history
            ]
            return Result.success(history)
        except Exception as e:
            return Result.error(f"Failed to get search history: {str(e)}")
    
    async def clear_search_history(self) -> Result[bool, str]:
        """Clear search history"""
        try:
            self._search_history.clear()
            return Result.success(True)
        except Exception as e:
            return Result.error(f"Failed to clear search history: {str(e)}")
    
    async def export_knowledge_base(self) -> Result[Dict[str, Any], str]:
        """Export knowledge base - not implemented (vector DB only)"""
        self.logger.warning("export_knowledge_base not implemented - using vector DB only")
        return Result.success({
            "message": "Vector DB only mode - no local knowledge base to export",
            "vector_db_available": self.vector_db_service is not None,
            "exported_at": datetime.now().isoformat()
        })

    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            health_data = {
                'status': 'healthy',
                'service': self.__class__.__name__,
                'vector_db_available': self.vector_db_service is not None,
                'text_cleaner_available': self.text_cleaner_service is not None,
                'search_history_count': len(self._search_history)
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
