# tests/services/test_knowledge_service.py
import sys
sys.path.append('.')
import pytest
import asyncio
import json
from application.services.knowledge_service import KnowledgeService
from domain.utils.result import Result
from domain.entities.rag_chunk import RAGChunk

class TestKnowledgeService:
    """Test suite for Knowledge Service"""
    
    @pytest.fixture
    def knowledge_service(self):
        """Create KnowledgeService instance for testing"""
        return KnowledgeService()
    
    @pytest.mark.asyncio
    async def test_search_knowledge_base_success(self, knowledge_service):
        """Test successful knowledge base search"""
        result = await knowledge_service.search_knowledge_base("artificial intelligence")
        
        assert result.is_success
        results = result.value
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Check structure
        for knowledge_result in results:
            assert "topic" in knowledge_result
            assert "score" in knowledge_result
            assert "facts" in knowledge_result
            assert "total_facts" in knowledge_result
    
    @pytest.mark.asyncio
    async def test_search_knowledge_base_empty_query(self, knowledge_service):
        """Test knowledge base search with empty query"""
        result = await knowledge_service.search_knowledge_base("")
        
        assert result.is_error
        assert "Query cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_search_knowledge_base_long_query(self, knowledge_service):
        """Test knowledge base search with very long query"""
        long_query = "A" * 2500  # Over 2000 character limit
        result = await knowledge_service.search_knowledge_base(long_query)
        
        assert result.is_error
        assert "Query must be between 1 and 2000 characters" in result.error
    
    @pytest.mark.asyncio
    async def test_search_knowledge_base_no_results(self, knowledge_service):
        """Test knowledge base search with no matching results"""
        result = await knowledge_service.search_knowledge_base("nonexistent_topic_xyz")
        
        assert result.is_success
        results = result.value
        assert isinstance(results, list)
        assert len(results) == 0
    
    @pytest.mark.asyncio
    async def test_add_knowledge_success(self, knowledge_service):
        """Test successful knowledge addition"""
        content = "Test knowledge content"
        metadata = {"topic": "test_topic"}
        
        result = await knowledge_service.add_knowledge(content, metadata)
        
        assert result.is_success
        
        # Verify knowledge was added
        search_result = await knowledge_service.search_knowledge_base("test_topic")
        assert search_result.is_success
        assert len(search_result.value) > 0
    
    @pytest.mark.asyncio
    async def test_add_knowledge_empty_content(self, knowledge_service):
        """Test knowledge addition with empty content"""
        result = await knowledge_service.add_knowledge("")
        
        assert result.is_error
        assert "Content cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_add_knowledge_no_metadata(self, knowledge_service):
        """Test knowledge addition without metadata"""
        content = "Test knowledge without metadata"
        
        result = await knowledge_service.add_knowledge(content)
        
        assert result.is_success
        
        # Should be added to general topic
        search_result = await knowledge_service.search_knowledge_base("general")
        assert search_result.is_success
    
    @pytest.mark.asyncio
    async def test_get_knowledge_stats(self, knowledge_service):
        """Test knowledge base statistics retrieval"""
        result = await knowledge_service.get_knowledge_stats()
        
        assert result.is_success
        stats = result.value
        assert "total_topics" in stats
        assert "total_facts" in stats
        assert "topics" in stats
        assert "average_facts_per_topic" in stats
        assert "search_history_count" in stats
        assert isinstance(stats["topics"], list)
        assert stats["total_topics"] > 0
        assert stats["total_facts"] > 0
    
    @pytest.mark.asyncio
    async def test_get_topic_facts(self, knowledge_service):
        """Test getting facts for specific topic"""
        result = await knowledge_service.get_topic_facts("artificial intelligence")
        
        assert result.is_success
        facts = result.value
        assert isinstance(facts, list)
        assert len(facts) > 0
        assert all(isinstance(fact, str) for fact in facts)
    
    @pytest.mark.asyncio
    async def test_get_topic_facts_invalid_topic(self, knowledge_service):
        """Test getting facts for invalid topic"""
        result = await knowledge_service.get_topic_facts("invalid_topic")
        
        assert result.is_error
        assert "not found" in result.error
        assert "Available topics" in result.error
    
    @pytest.mark.asyncio
    async def test_search_similar_topics(self, knowledge_service):
        """Test searching for similar topics"""
        result = await knowledge_service.search_similar_topics("AI")
        
        assert result.is_success
        similar_topics = result.value
        assert isinstance(similar_topics, list)
        assert "artificial intelligence" in similar_topics
    
    @pytest.mark.asyncio
    async def test_search_similar_topics_no_matches(self, knowledge_service):
        """Test searching for similar topics with no matches"""
        result = await knowledge_service.search_similar_topics("nonexistent_xyz")
        
        assert result.is_success
        similar_topics = result.value
        assert isinstance(similar_topics, list)
        assert len(similar_topics) == 0
    
    @pytest.mark.asyncio
    async def test_create_rag_chunk_success(self, knowledge_service):
        """Test successful RAG chunk creation"""
        text = "This is test text for RAG chunk"
        score = 0.9
        source = "test_source"
        
        result = await knowledge_service.create_rag_chunk(text, score, source)
        
        assert result.is_success
        chunk = result.value
        assert isinstance(chunk, RAGChunk)
        assert chunk.text_chunk == text
        assert chunk.score == score
        assert chunk.source == source
    
    @pytest.mark.asyncio
    async def test_create_rag_chunk_empty_text(self, knowledge_service):
        """Test RAG chunk creation with empty text"""
        result = await knowledge_service.create_rag_chunk("")
        
        assert result.is_error
        assert "Text cannot be empty" in result.error
    
    @pytest.mark.asyncio
    async def test_create_rag_chunk_default_values(self, knowledge_service):
        """Test RAG chunk creation with default values"""
        text = "Test text"
        
        result = await knowledge_service.create_rag_chunk(text)
        
        assert result.is_success
        chunk = result.value
        assert chunk.text_chunk == text
        assert chunk.score == 0.8  # Default score
        assert chunk.source == "knowledge_service"  # Default source
    
    @pytest.mark.asyncio
    async def test_get_search_history(self, knowledge_service):
        """Test getting search history"""
        # Perform some searches first
        await knowledge_service.search_knowledge_base("AI")
        await knowledge_service.search_knowledge_base("programming")
        
        result = await knowledge_service.get_search_history(5)
        
        assert result.is_success
        history = result.value
        assert isinstance(history, list)
        assert len(history) > 0
        
        # Check structure
        for entry in history:
            assert "query" in entry
            assert "results_count" in entry
            assert "timestamp" in entry
    
    @pytest.mark.asyncio
    async def test_get_search_history_limit(self, knowledge_service):
        """Test search history with limit"""
        # Perform multiple searches
        for i in range(10):
            await knowledge_service.search_knowledge_base(f"query_{i}")
        
        result = await knowledge_service.get_search_history(3)
        
        assert result.is_success
        history = result.value
        assert len(history) == 3
    
    @pytest.mark.asyncio
    async def test_clear_search_history(self, knowledge_service):
        """Test clearing search history"""
        # Perform some searches
        await knowledge_service.search_knowledge_base("AI")
        await knowledge_service.search_knowledge_base("programming")
        
        # Clear history
        result = await knowledge_service.clear_search_history()
        assert result.is_success
        
        # Check history is empty
        history_result = await knowledge_service.get_search_history()
        assert history_result.is_success
        assert len(history_result.value) == 0
    
    @pytest.mark.asyncio
    async def test_export_knowledge_base(self, knowledge_service):
        """Test knowledge base export"""
        result = await knowledge_service.export_knowledge_base("json")
        
        assert result.is_success
        export_data = result.value
        
        # Should be valid JSON
        parsed_data = json.loads(export_data)
        assert "knowledge_base" in parsed_data
        assert "search_history" in parsed_data
        assert "exported_at" in parsed_data
    
    @pytest.mark.asyncio
    async def test_export_knowledge_base_invalid_format(self, knowledge_service):
        """Test knowledge base export with invalid format"""
        result = await knowledge_service.export_knowledge_base("invalid_format")
        
        assert result.is_error
        assert "Unsupported export format" in result.error
    
    @pytest.mark.asyncio
    async def test_knowledge_service_search_accuracy(self, knowledge_service):
        """Test search accuracy and relevance scoring"""
        result = await knowledge_service.search_knowledge_base("machine learning")
        
        assert result.is_success
        results = result.value
        
        # Should find AI-related topics
        topics = [r["topic"] for r in results]
        assert "artificial intelligence" in topics
        
        # Scores should be in valid range
        for result_item in results:
            assert 0 <= result_item["score"] <= 1
    
    @pytest.mark.asyncio
    async def test_knowledge_service_case_insensitive(self, knowledge_service):
        """Test that knowledge service is case insensitive"""
        queries = ["ARTIFICIAL INTELLIGENCE", "Programming", "CiTiEs"]
        
        for query in queries:
            result = await knowledge_service.search_knowledge_base(query)
            assert result.is_success, f"Failed for query: {query}"
    
    @pytest.mark.asyncio
    async def test_knowledge_service_whitespace_handling(self, knowledge_service):
        """Test that knowledge service handles whitespace correctly"""
        queries = ["  artificial intelligence  ", "\tprogramming\t", "\ncities\n"]
        
        for query in queries:
            result = await knowledge_service.search_knowledge_base(query)
            assert result.is_success, f"Failed for query with whitespace: '{query}'"
    
    @pytest.mark.asyncio
    async def test_knowledge_service_performance(self, knowledge_service):
        """Test knowledge service performance with multiple requests"""
        import time
        
        queries = ["AI", "programming", "cities", "weather", "technology", "artificial intelligence"]
        start_time = time.time()
        
        # Make multiple requests
        tasks = [knowledge_service.search_knowledge_base(query) for query in queries]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        
        # Should complete quickly (less than 1 second for 6 requests)
        assert duration < 1.0, f"Performance test failed: {duration:.2f}s for 6 requests"
    
    @pytest.mark.asyncio
    async def test_knowledge_service_concurrent_access(self, knowledge_service):
        """Test concurrent access to knowledge service"""
        # Test concurrent access to same query
        tasks = [knowledge_service.search_knowledge_base("AI") for _ in range(5)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(result.is_success for result in results)
        # Results should be consistent
        assert all(result.value == results[0].value for result in results)
    
    @pytest.mark.asyncio
    async def test_knowledge_service_data_completeness(self, knowledge_service):
        """Test that knowledge base has complete data"""
        stats_result = await knowledge_service.get_knowledge_stats()
        assert stats_result.is_success
        
        stats = stats_result.value
        topics = stats["topics"]
        
        for topic in topics:
            # Test topic facts
            facts_result = await knowledge_service.get_topic_facts(topic)
            assert facts_result.is_success
            
            facts = facts_result.value
            assert len(facts) > 0
            assert all(isinstance(fact, str) for fact in facts)
    
    @pytest.mark.asyncio
    async def test_knowledge_service_search_history_tracking(self, knowledge_service):
        """Test that search history is properly tracked"""
        # Clear history first
        await knowledge_service.clear_search_history()
        
        # Perform searches
        await knowledge_service.search_knowledge_base("AI")
        await knowledge_service.search_knowledge_base("programming")
        
        # Check history
        history_result = await knowledge_service.get_search_history()
        assert history_result.is_success
        
        history = history_result.value
        assert len(history) == 2
        
        # Check queries
        queries = [entry["query"] for entry in history]
        assert "AI" in queries
        assert "programming" in queries
    
    @pytest.mark.asyncio
    async def test_knowledge_service_rag_chunk_quality(self, knowledge_service):
        """Test RAG chunk quality and validation"""
        text = "This is a test text for RAG chunk creation"
        
        result = await knowledge_service.create_rag_chunk(text, 0.9, "test_source")
        assert result.is_success
        
        chunk = result.value
        assert chunk.is_high_quality()  # Score > 0.8
        assert chunk.has_text_content()
        assert not chunk.is_empty()
        assert chunk.get_text_length() == len(text)
