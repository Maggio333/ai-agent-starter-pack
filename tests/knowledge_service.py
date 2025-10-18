# services/knowledge_service.py
import logging
from typing import Dict, List, Optional, Any
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.services.IVectorDbService import IVectorDbService
from domain.services.ITextCleanerService import ITextCleanerService
from domain.entities.rag_chunk import RAGChunk
from datetime import datetime # Import datetime for timestamp

class KnowledgeService:
    """Microservice for knowledge base operations and RAG functionality"""
    
    def __init__(self, vector_db_service: Optional[IVectorDbService] = None, text_cleaner_service: Optional[ITextCleanerService] = None):
        self.rop_service = ROPService()
        self.vector_db_service = vector_db_service
        self.text_cleaner_service = text_cleaner_service
        self.logger = logging.getLogger(__name__) # Add logger
        
        # Debug logging
        self.logger.info(f"KnowledgeService initialized with vector_db_service: {vector_db_service is not None}")
        if vector_db_service:
            self.logger.info(f"Vector DB service type: {type(vector_db_service).__name__}")
        else:
            self.logger.warning("Vector DB service is None - will use local knowledge base only")
        
        self._knowledge_base = {
            "artificial intelligence": [
                "AI is the simulation of human intelligence in machines",
                "Machine learning is a subset of AI that focuses on algorithms",
                "Deep learning uses neural networks with multiple layers",
                "Natural language processing enables computers to understand human language"
            ],
            "programming": [
                "Python is a high-level programming language known for its simplicity",
                "Clean Architecture separates concerns into distinct layers",
                "Dependency Injection improves testability and maintainability",
                "Railway Oriented Programming provides elegant error handling patterns"
            ],
            "cities": [
                "New York is known as the Big Apple and is a major financial center",
                "London is the capital of England and has a rich historical heritage",
                "Tokyo is the largest metropolitan area in the world",
                "Paris is called the City of Light and is famous for its art and culture"
            ],
            "weather": [
                "Weather patterns are influenced by atmospheric pressure and temperature",
                "Climate change affects global weather patterns and sea levels",
                "Meteorology is the scientific study of weather and atmospheric phenomena",
                "Weather forecasting uses computer models and historical data"
            ],
            "technology": [
                "Cloud computing provides scalable and flexible IT resources",
                "Microservices architecture enables independent service deployment",
                "API design follows REST principles for web service communication",
                "Containerization with Docker simplifies application deployment"
            ]
        }
        self._search_history = []
    
    async def search_knowledge_base(self, query: str) -> Result[List[Dict[str, Any]], str]:
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
                vector_results = await self.vector_db_service.search(clean_query, limit=5)
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
                            "topic": chunk.metadata.get("topic", "unknown"),
                            "score": chunk.score if hasattr(chunk, 'score') else 0.8,
                            "facts": [clean_text],  # Use cleaned text
                            "total_facts": 1,
                            "source": "vector_db"
                        })
                    
                    self.logger.info(f"KnowledgeService - returning {len(results)} results from vector database")
                    print(f"DEBUG: KnowledgeService - returning {len(results)} results from vector database")
                    
                    # Add to search history
                    self._search_history.append({
                        "query": query,
                        "results_count": len(results),
                        "timestamp": self._get_current_timestamp(),
                        "source": "vector_db"
                    })
                    
                    return Result.success(results)
                else:
                    self.logger.warning(f"KnowledgeService - Vector DB search failed, falling back to local KB: {vector_results.error}")
                    print(f"DEBUG: KnowledgeService - Vector DB search failed, falling back to local KB: {vector_results.error}")
            else:
                self.logger.warning(f"KnowledgeService - vector_db_service is None, using local KB only")
                print(f"DEBUG: KnowledgeService - vector_db_service is None, using local KB only")
            
            # Fallback: Search in local knowledge base
            self.logger.info(f"KnowledgeService - Falling back to local knowledge base for query: '{query}'")
            safe_query = query.encode('utf-8', errors='ignore').decode('utf-8')
            print(f"DEBUG: KnowledgeService - Falling back to local knowledge base for query: '{safe_query}'")
            results = []
            query_words = query_lower.split()
            
            for topic, facts in self._knowledge_base.items():
                topic_score = 0
                matching_facts = []
                
                # Calculate relevance score
                for word in query_words:
                    if word in topic:
                        topic_score += 0.3
                    for fact in facts:
                        if word in fact.lower():
                            topic_score += 0.1
                            if fact not in matching_facts:
                                matching_facts.append(fact)
                
                if topic_score > 0:
                    results.append({
                        "topic": topic,
                        "score": min(topic_score, 1.0),
                        "facts": matching_facts[:3],  # Limit to top 3 facts
                        "total_facts": len(facts),
                        "source": "local_kb"
                    })
            
            # Sort by score (highest first)
            results.sort(key=lambda x: x["score"], reverse=True)
            
            # Add to search history
            self._search_history.append({
                "query": query,
                "results_count": len(results),
                "timestamp": self._get_current_timestamp(),
                "source": "local_kb"
            })
            
            # Limit results
            top_results = results[:5]
            
            self.logger.info(f"KnowledgeService - Returning {len(top_results)} results from local KB")
            print(f"DEBUG: KnowledgeService - Returning {len(top_results)} results from local KB")
            
            return Result.success(top_results)
            
        except Exception as e:
            # Safely convert exception to string
            safe_exception_str = str(e).encode('utf-8', errors='ignore').decode('utf-8')
            error_msg = f"Failed to search knowledge base: {safe_exception_str}"
            safe_error_msg = error_msg.encode('utf-8', errors='ignore').decode('utf-8')
            self.logger.error(safe_error_msg)
            print(f"ERROR: KnowledgeService - {safe_error_msg}")
            return Result.error(safe_error_msg)
    
    async def add_knowledge(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Result[None, str]:
        """Add new knowledge to both vector database and local knowledge base"""
        try:
            content_lower = content.lower().strip()
            
            if not content_lower:
                return Result.error("Content cannot be empty")
            
            # Extract topic from content or metadata
            topic = "general"
            if metadata and "topic" in metadata:
                topic = metadata["topic"].lower()
            else:
                # Try to infer topic from content
                for known_topic in self._knowledge_base.keys():
                    if any(word in content_lower for word in known_topic.split()):
                        topic = known_topic
                        break
            
            # Add to local knowledge base
            if topic not in self._knowledge_base:
                self._knowledge_base[topic] = []
            
            self._knowledge_base[topic].append(content)
            
            # Also add to vector database
            try:
                chunk = RAGChunk(
                    text_chunk=content,
                    metadata={
                        "topic": topic,
                        "source": "knowledge_service",
                        "timestamp": self._get_current_timestamp(),
                        **(metadata or {})
                    }
                )
                
                vector_result = await self.vector_db_service.save_chunk(chunk)
                if vector_result.is_error:
                    # Log error but don't fail the operation
                    print(f"Warning: Failed to save to vector DB: {vector_result.error}")
                
            except Exception as e:
                # Log error but don't fail the operation
                print(f"Warning: Vector DB operation failed: {str(e)}")
            
            return Result.success(None)
            
        except Exception as e:
            return Result.error(f"Failed to add knowledge: {str(e)}")
    
    async def get_knowledge_stats(self) -> Result[Dict[str, Any], str]:
        """Get knowledge base statistics"""
        try:
            total_facts = sum(len(facts) for facts in self._knowledge_base.values())
            total_topics = len(self._knowledge_base)
            
            stats = {
                "total_topics": total_topics,
                "total_facts": total_facts,
                "topics": list(self._knowledge_base.keys()),
                "average_facts_per_topic": total_facts / total_topics if total_topics > 0 else 0,
                "search_history_count": len(self._search_history),
                "last_search": self._search_history[-1] if self._search_history else None
            }
            
            return Result.success(stats)
            
        except Exception as e:
            return Result.error(f"Failed to get knowledge stats: {str(e)}")
    
    async def get_topic_facts(self, topic: str) -> Result[List[str], str]:
        """Get all facts for a specific topic"""
        try:
            topic_lower = topic.lower().strip()
            
            if topic_lower not in self._knowledge_base:
                available_topics = list(self._knowledge_base.keys())
                return Result.error(f"Topic '{topic}' not found. Available topics: {', '.join(available_topics)}")
            
            facts = self._knowledge_base[topic_lower]
            return Result.success(facts)
            
        except Exception as e:
            return Result.error(f"Failed to get topic facts: {str(e)}")
    
    async def search_similar_topics(self, topic: str) -> Result[List[str], str]:
        """Find topics similar to the given topic"""
        try:
            topic_lower = topic.lower().strip()
            
            similar_topics = []
            topic_words = topic_lower.split()
            
            for known_topic in self._knowledge_base.keys():
                similarity_score = 0
                for word in topic_words:
                    if word in known_topic:
                        similarity_score += 1
                
                if similarity_score > 0:
                    similar_topics.append(known_topic)
            
            # Sort by similarity (number of matching words)
            similar_topics.sort(key=lambda t: sum(1 for word in topic_words if word in t), reverse=True)
            
            return Result.success(similar_topics)
            
        except Exception as e:
            return Result.error(f"Failed to search similar topics: {str(e)}")
    
    async def create_rag_chunk(self, text: str, score: Optional[float] = None, source: Optional[str] = None) -> Result[RAGChunk, str]:
        """Create a RAG chunk from text"""
        try:
            if not text.strip():
                return Result.error("Text cannot be empty")
            
            chunk = RAGChunk.create_from_text(
                text=text,
                score=score or 0.8,
                source=source or "knowledge_service"
            )
            
            return Result.success(chunk)
            
        except Exception as e:
            return Result.error(f"Failed to create RAG chunk: {str(e)}")
    
    async def get_search_history(self, limit: int = 10) -> Result[List[Dict[str, Any]], str]:
        """Get search history"""
        try:
            if limit <= 0:
                return Result.error("Limit must be positive")
            
            history = self._search_history[-limit:] if limit < len(self._search_history) else self._search_history
            return Result.success(history)
            
        except Exception as e:
            return Result.error(f"Failed to get search history: {str(e)}")
    
    async def clear_search_history(self) -> Result[None, str]:
        """Clear search history"""
        try:
            self._search_history.clear()
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to clear search history: {str(e)}")
    
    async def export_knowledge_base(self, format: str = "json") -> Result[str, str]:
        """Export knowledge base"""
        try:
            if format.lower() == "json":
                import json
                export_data = {
                    "knowledge_base": self._knowledge_base,
                    "search_history": self._search_history,
                    "exported_at": self._get_current_timestamp()
                }
                return Result.success(json.dumps(export_data, ensure_ascii=False, indent=2))
            else:
                return Result.error(f"Unsupported export format: {format}")
                
        except Exception as e:
            return Result.error(f"Failed to export knowledge base: {str(e)}")
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as string"""
        from datetime import datetime
        return datetime.now().isoformat()
