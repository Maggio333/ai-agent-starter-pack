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
        
        self._knowledge_base = {
            "artificial intelligence": [
                "AI is the simulation of human intelligence in machines",
                "Machine learning is a subset of AI that focuses on algorithms",
                "Deep learning uses neural networks with multiple layers",
                "Natural language processing enables computers to understand human language"
            ],
            "programming": [
                "Python is a high-level, interpreted programming language",
                "C# is a modern, object-oriented programming language developed by Microsoft",
                "JavaScript is a programming language that is one of the core technologies of the World Wide Web",
                "Java is a class-based, object-oriented programming language designed for having as few implementation dependencies as possible"
            ],
            "cities": [
                "New York City is the most populous city in the United States",
                "London is the capital and largest city of England and the United Kingdom",
                "Tokyo is the capital and most populous prefecture of Japan",
                "Paris is the capital and most populous city of France",
                "Sydney is the capital city of New South Wales and the most populous city in Australia",
                "Moscow is the capital and largest city of Russia"
            ],
            "weather": [
                "Weather is the state of the atmosphere, describing for example the degree to which it is hot or cold, wet or dry, calm or stormy, clear or cloudy.",
                "Climate is the long-term average of weather, typically averaged over a period of 30 years.",
                "Temperature is a physical quantity that expresses hot and cold.",
                "Humidity is the amount of water vapor in the air."
            ],
            "technology": [
                "Technology is the application of scientific knowledge for practical purposes, especially in industry.",
                "The internet is a global computer network providing a variety of information and communication facilities.",
                "Cloud computing is the on-demand availability of computer system resources, especially data storage and computing power, without direct active management by the user.",
                "Blockchain is a decentralized, distributed, and often public, digital ledger that is used to record transactions across many computers so that any involved record cannot be altered retroactively, without the alteration of all subsequent blocks and the consensus of the network."
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
                    # Fallback to local knowledge base if vector search fails or returns no results
                    return self._search_local_knowledge_base(query_lower)
            else:
                self.logger.warning("KnowledgeService - Vector DB service not available, using local knowledge base only.")
                print("DEBUG: KnowledgeService - Vector DB service not available, using local knowledge base only.")
                return self._search_local_knowledge_base(query_lower)
        except Exception as e:
            error_message = f"Failed to search knowledge base: {str(e)}"
            self.logger.error(error_message)
            print(f"ERROR: KnowledgeService - {error_message}")
            return Result.error(error_message)
    
    def _search_local_knowledge_base(self, query: str) -> Result[List[Dict[str, Any]], str]:
        """Search local knowledge base (mock data)"""
        self.logger.info(f"Searching local knowledge base for: '{query}'")
        results = []
        for topic, facts in self._knowledge_base.items():
            if query in topic.lower():
                results.append({
                    "topic": topic,
                    "score": 1.0,  # Perfect match for local search
                    "facts": facts,
                    "total_facts": len(facts),
                    "source": "local_kb"
                })
            else:
                for fact in facts:
                    if query in fact.lower():
                        results.append({
                            "topic": topic,
                            "score": 0.8,  # Partial match for local search
                            "facts": [fact],
                            "total_facts": 1,
                            "source": "local_kb"
                        })
        
        if results:
            self.logger.info(f"Found {len(results)} results in local knowledge base.")
            return Result.success(results)
        else:
            self.logger.warning("No results found in local knowledge base.")
            return Result.error("No results found in local knowledge base.")
    
    async def add_knowledge(self, topic: str, facts: List[str]) -> Result[bool, str]:
        """Add knowledge to the base"""
        try:
            if topic not in self._knowledge_base:
                self._knowledge_base[topic] = []
            self._knowledge_base[topic].extend(facts)
            return Result.success(True)
        except Exception as e:
            return Result.error(f"Failed to add knowledge: {str(e)}")
    
    async def get_knowledge_stats(self) -> Result[Dict[str, Any], str]:
        """Get statistics about the knowledge base"""
        try:
            total_topics = len(self._knowledge_base)
            total_facts = sum(len(facts) for facts in self._knowledge_base.values())
            average_facts_per_topic = total_facts / total_topics if total_topics > 0 else 0
            
            stats = {
                "total_topics": total_topics,
                "total_facts": total_facts,
                "topics": list(self._knowledge_base.keys()),
                "average_facts_per_topic": average_facts_per_topic,
                "search_history_count": len(self._search_history),
                "last_search": self._search_history[-1] if self._search_history else None
            }
            return Result.success(stats)
        except Exception as e:
            error_message = f"Failed to get knowledge stats: {str(e)}"
            self.logger.error(error_message)
            return Result.error(error_message)
    
    async def get_topic_facts(self, topic: str) -> Result[List[str], str]:
        """Get facts for a specific topic"""
        try:
            if topic in self._knowledge_base:
                return Result.success(self._knowledge_base[topic])
            else:
                return Result.error(f"Topic '{topic}' not found")
        except Exception as e:
            return Result.error(f"Failed to get topic facts: {str(e)}")
    
    async def search_similar_topics(self, topic: str) -> Result[List[Dict[str, Any]], str]:
        """Search for similar topics"""
        try:
            similar_topics = []
            for t in self._knowledge_base.keys():
                if topic.lower() in t.lower() or t.lower() in topic.lower():
                    similar_topics.append({
                        "topic": t,
                        "similarity": 0.8,
                        "facts_count": len(self._knowledge_base[t])
                    })
            return Result.success(similar_topics)
        except Exception as e:
            return Result.error(f"Failed to search similar topics: {str(e)}")
    
    async def create_rag_chunk(self, text: str, topic: str) -> Result[Dict[str, Any], str]:
        """Create a RAG chunk"""
        try:
            chunk = {
                "text": text,
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "id": f"chunk_{len(self._search_history)}"
            }
            return Result.success(chunk)
        except Exception as e:
            return Result.error(f"Failed to create RAG chunk: {str(e)}")
    
    async def get_search_history(self) -> Result[List[Dict[str, Any]], str]:
        """Get search history"""
        try:
            return Result.success(self._search_history)
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
        """Export knowledge base"""
        try:
            export_data = {
                "knowledge_base": self._knowledge_base,
                "search_history": self._search_history,
                "export_timestamp": datetime.now().isoformat()
            }
            return Result.success(export_data)
        except Exception as e:
            return Result.error(f"Failed to export knowledge base: {str(e)}")
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            health_data = {
                'status': 'healthy',
                'service': self.__class__.__name__,
                'vector_db_available': self.vector_db_service is not None,
                'text_cleaner_available': self.text_cleaner_service is not None,
                'knowledge_base_size': len(self._knowledge_base)
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
