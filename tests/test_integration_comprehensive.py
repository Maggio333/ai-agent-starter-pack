# tests/test_integration_comprehensive.py
"""
Integration Tests for AI Agent Starter Pack

This test suite validates the integration between different components
of the AI Agent Starter Pack before releasing to Git.

Author: Arkadiusz Słota
Year: 2025
"""

import sys
import os
import asyncio
from datetime import datetime
from typing import List, Dict, Any

# Add project root to path
sys.path.append('.')

# Import all major components
from application.container import ContainerManager
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.entities.rag_chunk import RAGChunk
from domain.entities.quality_level import QualityLevel

class IntegrationTestSuite:
    """Integration test suite"""
    
    def __init__(self):
        self.container_manager = ContainerManager()
        self.container = self.container_manager.container
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        self.test_results.append({
            "test_name": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    async def test_embedding_vector_db_integration(self):
        """Test integration between embedding service and vector database"""
        try:
            # Get services
            embedding_result = self.container.embedding_service()
            if embedding_result.is_error:
                self.log_test_result("Embedding-VectorDB Integration", False, "Embedding service creation failed")
                return False
            
            embedding_service = embedding_result.value
            vector_db_service = self.container.vector_db_service()
            
            # Create collection
            collection_name = "integration_test_collection"
            create_result = await vector_db_service.create_collection(collection_name)
            if create_result.is_error:
                self.log_test_result("Embedding-VectorDB Integration", False, "Collection creation failed")
                return False
            
            # Create RAG chunk with real embedding
            test_text = "This is a test text for embedding-vector integration"
            embedding_result = await embedding_service.create_embedding(test_text)
            if embedding_result.is_error:
                self.log_test_result("Embedding-VectorDB Integration", False, "Embedding creation failed")
                return False
            
            embedding = embedding_result.value
            
            test_chunk = RAGChunk(
                chunk_id="integration_chunk_1",
                text_chunk=test_text,
                metadata={"integration_test": True, "embedding_dimension": len(embedding)},
                score=0.95,
                quality_level=QualityLevel.EXCELLENT
            )
            
            # Upsert chunk to vector database
            upsert_result = await vector_db_service.upsert_chunks([test_chunk])
            if upsert_result.is_error:
                self.log_test_result("Embedding-VectorDB Integration", False, "Vector upsert failed")
                return False
            
            # Search using the same text
            search_result = await vector_db_service.search(test_text, limit=5)
            if search_result.is_error:
                self.log_test_result("Embedding-VectorDB Integration", False, "Vector search failed")
                return False
            
            search_results = search_result.value
            assert len(search_results) > 0, "Should find the inserted chunk"
            
            # Verify the found chunk
            found_chunk = search_results[0]
            assert found_chunk.text_chunk == test_text, "Found chunk should match inserted text"
            
            # Clean up
            await vector_db_service.delete_collection(collection_name)
            
            self.log_test_result("Embedding-VectorDB Integration", True, f"Found {len(search_results)} results")
            return True
            
        except Exception as e:
            self.log_test_result("Embedding-VectorDB Integration", False, str(e))
            return False
    
    async def test_chat_repository_vector_db_integration(self):
        """Test integration between chat repository and vector database"""
        try:
            # Get services
            chat_repository = self.container.chat_repository()
            vector_db_service = self.container.vector_db_service()
            
            # Create a chat message
            test_message = ChatMessage(
                content="This is a test message for chat-vector integration",
                role=MessageRole.USER,
                thread_id="integration_test_thread"
            )
            
            # Save message to chat repository
            save_result = await chat_repository.save_message(test_message)
            if save_result.is_error:
                self.log_test_result("Chat-VectorDB Integration", False, "Message save failed")
                return False
            
            # Create collection for vector storage
            collection_name = "chat_integration_collection"
            create_result = await vector_db_service.create_collection(collection_name)
            if create_result.is_error:
                self.log_test_result("Chat-VectorDB Integration", False, "Collection creation failed")
                return False
            
            # Create RAG chunk from chat message
            test_chunk = RAGChunk(
                chunk_id=f"chat_chunk_{test_message.message_id}",
                text_chunk=test_message.content,
                metadata={
                    "message_id": test_message.message_id,
                    "thread_id": test_message.thread_id,
                    "role": test_message.role.value,
                    "integration_test": True
                },
                score=0.98,
                quality_level=QualityLevel.EXCELLENT
            )
            
            # Upsert chunk to vector database
            upsert_result = await vector_db_service.upsert_chunks([test_chunk])
            if upsert_result.is_error:
                self.log_test_result("Chat-VectorDB Integration", False, "Vector upsert failed")
                return False
            
            # Search for the message content in vector database
            search_result = await vector_db_service.search("test message", limit=5)
            if search_result.is_error:
                self.log_test_result("Chat-VectorDB Integration", False, "Vector search failed")
                return False
            
            search_results = search_result.value
            assert len(search_results) > 0, "Should find the message chunk"
            
            # Verify integration
            found_chunk = search_results[0]
            assert found_chunk.metadata["message_id"] == test_message.message_id, "Message ID should match"
            assert found_chunk.metadata["thread_id"] == test_message.thread_id, "Thread ID should match"
            
            # Clean up
            await vector_db_service.delete_collection(collection_name)
            
            self.log_test_result("Chat-VectorDB Integration", True, f"Found {len(search_results)} results")
            return True
            
        except Exception as e:
            self.log_test_result("Chat-VectorDB Integration", False, str(e))
            return False
    
    async def test_cache_embedding_integration(self):
        """Test integration between cache service and embedding service"""
        try:
            # Get services
            cache_service = self.container.cache_service()
            embedding_result = self.container.embedding_service()
            if embedding_result.is_error:
                self.log_test_result("Cache-Embedding Integration", False, "Embedding service creation failed")
                return False
            
            embedding_service = embedding_result.value
            
            # Test text for embedding
            test_text = "This is a test text for cache-embedding integration"
            
            # Create embedding
            embedding_result = await embedding_service.create_embedding(test_text)
            if embedding_result.is_error:
                self.log_test_result("Cache-Embedding Integration", False, "Embedding creation failed")
                return False
            
            embedding = embedding_result.value
            
            # Cache the embedding
            cache_key = f"embedding_{hash(test_text)}"
            cache_result = await cache_service.set(cache_key, embedding, ttl=300)
            if cache_result.is_error:
                self.log_test_result("Cache-Embedding Integration", False, "Cache set failed")
                return False
            
            # Retrieve from cache
            cached_result = await cache_service.get(cache_key)
            if cached_result.is_error:
                self.log_test_result("Cache-Embedding Integration", False, "Cache get failed")
                return False
            
            cached_embedding = cached_result.value
            assert cached_embedding == embedding, "Cached embedding should match original"
            
            # Test cache hit performance (should be faster than creating new embedding)
            import time
            cache_start = time.time()
            cached_result2 = await cache_service.get(cache_key)
            cache_duration = time.time() - cache_start
            
            assert cached_result2.is_success, "Second cache get should succeed"
            assert cached_result2.value == embedding, "Second cached embedding should match"
            
            # Clean up
            await cache_service.delete(cache_key)
            
            self.log_test_result("Cache-Embedding Integration", True, f"Cache hit in {cache_duration:.3f}s")
            return True
            
        except Exception as e:
            self.log_test_result("Cache-Embedding Integration", False, str(e))
            return False
    
    async def test_search_vector_db_integration(self):
        """Test integration between search service and vector database"""
        try:
            # Get services
            search_service = self.container.search_service()
            vector_db_service = self.container.vector_db_service()
            
            # Create collection
            collection_name = "search_integration_collection"
            create_result = await vector_db_service.create_collection(collection_name)
            if create_result.is_error:
                self.log_test_result("Search-VectorDB Integration", False, "Collection creation failed")
                return False
            
            # Create test documents
            test_documents = [
                {"id": "doc1", "content": "This is a test document about artificial intelligence"},
                {"id": "doc2", "content": "Another document about machine learning and AI"},
                {"id": "doc3", "content": "Third document about neural networks and deep learning"}
            ]
            
            # Index documents in search service
            for doc in test_documents:
                index_result = await search_service.index_document(doc["id"], doc)
                if index_result.is_error:
                    self.log_test_result("Search-VectorDB Integration", False, f"Document indexing failed: {doc['id']}")
                    return False
            
            # Create RAG chunks from documents
            test_chunks = []
            for doc in test_documents:
                chunk = RAGChunk(
                    chunk_id=f"search_chunk_{doc['id']}",
                    text_chunk=doc["content"],
                    metadata={"document_id": doc["id"], "search_integration": True},
                    score=0.9,
                    quality_level=QualityLevel.EXCELLENT
                )
                test_chunks.append(chunk)
            
            # Upsert chunks to vector database
            upsert_result = await vector_db_service.upsert_chunks(test_chunks)
            if upsert_result.is_error:
                self.log_test_result("Search-VectorDB Integration", False, "Vector upsert failed")
                return False
            
            # Test search in both services
            search_query = "artificial intelligence"
            
            # Search in search service
            search_result = await search_service.search(search_query, limit=5)
            if search_result.is_error:
                self.log_test_result("Search-VectorDB Integration", False, "Search service search failed")
                return False
            
            search_results = search_result.value
            assert len(search_results) > 0, "Search service should find documents"
            
            # Search in vector database
            vector_search_result = await vector_db_service.search(search_query, limit=5)
            if vector_search_result.is_error:
                self.log_test_result("Search-VectorDB Integration", False, "Vector search failed")
                return False
            
            vector_results = vector_search_result.value
            assert len(vector_results) > 0, "Vector database should find chunks"
            
            # Verify integration - both should find related content
            search_content = [doc["content"] for doc in search_results]
            vector_content = [chunk.text_chunk for chunk in vector_results]
            
            # Check if there's overlap in content
            content_overlap = any(content in search_content for content in vector_content)
            assert content_overlap, "Search and vector results should have content overlap"
            
            # Clean up
            await vector_db_service.delete_collection(collection_name)
            
            self.log_test_result("Search-VectorDB Integration", True, f"Search: {len(search_results)}, Vector: {len(vector_results)}")
            return True
            
        except Exception as e:
            self.log_test_result("Search-VectorDB Integration", False, str(e))
            return False
    
    async def test_application_services_integration(self):
        """Test integration between application services"""
        try:
            # Get services
            orchestration_service = self.container.orchestration_service()
            conversation_service = self.container.conversation_service()
            knowledge_service = self.container.knowledge_service()
            city_service = self.container.city_service()
            weather_service = self.container.weather_service()
            time_service = self.container.time_service()
            
            # Test orchestration service coordination
            test_request = "What is the weather like in Warsaw today?"
            thread_id = "integration_test_thread"
            
            # Process request through orchestration
            orchestration_result = await orchestration_service.process_request(test_request, thread_id)
            if orchestration_result.is_error:
                self.log_test_result("Application Services Integration", False, f"Orchestration failed: {orchestration_result.error}")
                return False
            
            # Verify conversation service integration
            conversation_result = await conversation_service.get_conversation_history(thread_id)
            if conversation_result.is_error:
                self.log_test_result("Application Services Integration", False, "Conversation service failed")
                return False
            
            conversation_history = conversation_result.value
            assert len(conversation_history) > 0, "Should have conversation history"
            
            # Verify knowledge service integration
            knowledge_result = await knowledge_service.search_knowledge("weather Warsaw")
            if knowledge_result.is_error:
                self.log_test_result("Application Services Integration", False, "Knowledge service failed")
                return False
            
            # Verify city service integration
            city_result = await city_service.get_city_info("Warsaw")
            if city_result.is_error:
                self.log_test_result("Application Services Integration", False, "City service failed")
                return False
            
            # Verify time service integration
            time_result = await time_service.get_current_time()
            if time_result.is_error:
                self.log_test_result("Application Services Integration", False, "Time service failed")
                return False
            
            # Verify weather service integration
            weather_result = await weather_service.get_weather("Warsaw")
            if weather_result.is_error:
                self.log_test_result("Application Services Integration", False, "Weather service failed")
                return False
            
            self.log_test_result("Application Services Integration", True, "All services integrated successfully")
            return True
            
        except Exception as e:
            self.log_test_result("Application Services Integration", False, str(e))
            return False
    
    async def test_health_monitoring_integration(self):
        """Test integration between health monitoring and all services"""
        try:
            # Get health service
            health_service = self.container.health_service()
            
            # Get all services for health monitoring
            embedding_service = self.container.embedding_service().value
            vector_db_service = self.container.vector_db_service()
            chat_repository = self.container.chat_repository()
            cache_service = self.container.cache_service()
            search_service = self.container.search_service()
            
            # Test overall health
            overall_health_result = await health_service.get_overall_health()
            if overall_health_result.is_error:
                self.log_test_result("Health Monitoring Integration", False, "Overall health check failed")
                return False
            
            overall_health = overall_health_result.value
            assert overall_health["status"] in ["healthy", "degraded"], "System should be healthy or degraded"
            
            # Test detailed health
            detailed_health_result = await health_service.get_detailed_health()
            if detailed_health_result.is_error:
                self.log_test_result("Health Monitoring Integration", False, "Detailed health check failed")
                return False
            
            detailed_health = detailed_health_result.value
            assert len(detailed_health) > 0, "Should have detailed health information"
            
            # Verify health checks cover all services
            health_service_names = [check.service_name for check in detailed_health]
            expected_services = ["embedding_service", "vector_db_service", "chat_repository", "cache_service", "search_service"]
            
            for expected_service in expected_services:
                assert any(expected_service in name for name in health_service_names), f"Health check should cover {expected_service}"
            
            self.log_test_result("Health Monitoring Integration", True, f"Status: {overall_health['status']}, Services: {len(detailed_health)}")
            return True
            
        except Exception as e:
            self.log_test_result("Health Monitoring Integration", False, str(e))
            return False
    
    async def test_end_to_end_integration(self):
        """Test complete end-to-end integration"""
        try:
            # Get all services
            embedding_service = self.container.embedding_service().value
            vector_db_service = self.container.vector_db_service()
            chat_repository = self.container.chat_repository()
            cache_service = self.container.cache_service()
            search_service = self.container.search_service()
            orchestration_service = self.container.orchestration_service()
            health_service = self.container.health_service()
            
            # Step 1: User asks a question
            user_question = "What is the weather like in Krakow today?"
            thread_id = "e2e_integration_thread"
            
            # Step 2: Save user message
            user_message = ChatMessage(
                content=user_question,
                role=MessageRole.USER,
                thread_id=thread_id
            )
            
            save_result = await chat_repository.save_message(user_message)
            if save_result.is_error:
                self.log_test_result("End-to-End Integration", False, "User message save failed")
                return False
            
            # Step 3: Create knowledge chunks
            knowledge_chunks = [
                RAGChunk(
                    chunk_id="weather_krakow_1",
                    text_chunk="Weather in Krakow today: Sunny, 22°C, light winds",
                    metadata={"city": "Krakow", "date": "today", "source": "weather_api"},
                    score=0.95,
                    quality_level=QualityLevel.EXCELLENT
                ),
                RAGChunk(
                    chunk_id="weather_krakow_2",
                    text_chunk="Krakow weather forecast: Partly cloudy, 20-25°C",
                    metadata={"city": "Krakow", "type": "forecast", "source": "weather_api"},
                    score=0.90,
                    quality_level=QualityLevel.GOOD
                )
            ]
            
            # Step 4: Store knowledge in vector database
            collection_name = "e2e_integration_collection"
            create_result = await vector_db_service.create_collection(collection_name)
            if create_result.is_error:
                self.log_test_result("End-to-End Integration", False, "Collection creation failed")
                return False
            
            upsert_result = await vector_db_service.upsert_chunks(knowledge_chunks)
            if upsert_result.is_error:
                self.log_test_result("End-to-End Integration", False, "Knowledge upsert failed")
                return False
            
            # Step 5: Cache embeddings for performance
            for chunk in knowledge_chunks:
                cache_key = f"embedding_{chunk.chunk_id}"
                embedding_result = await embedding_service.create_embedding(chunk.text_chunk)
                if embedding_result.is_success:
                    await cache_service.set(cache_key, embedding_result.value, ttl=300)
            
            # Step 6: Search for relevant knowledge
            search_result = await vector_db_service.search("weather Krakow today", limit=5)
            if search_result.is_error:
                self.log_test_result("End-to-End Integration", False, "Knowledge search failed")
                return False
            
            search_results = search_result.value
            assert len(search_results) > 0, "Should find relevant weather information"
            
            # Step 7: Process through orchestration
            orchestration_result = await orchestration_service.process_request(user_question, thread_id)
            if orchestration_result.is_error:
                self.log_test_result("End-to-End Integration", False, "Orchestration failed")
                return False
            
            # Step 8: Verify system health
            health_result = await health_service.get_overall_health()
            if health_result.is_error:
                self.log_test_result("End-to-End Integration", False, "Health check failed")
                return False
            
            health_status = health_result.value
            assert health_status["status"] in ["healthy", "degraded"], "System should be healthy"
            
            # Step 9: Verify conversation history
            conversation_result = await chat_repository.get_conversation_history(thread_id)
            if conversation_result.is_error:
                self.log_test_result("End-to-End Integration", False, "Conversation retrieval failed")
                return False
            
            conversation_history = conversation_result.value
            assert len(conversation_history) > 0, "Should have conversation history"
            
            # Clean up
            await vector_db_service.delete_collection(collection_name)
            
            self.log_test_result("End-to-End Integration", True, f"Found {len(search_results)} knowledge chunks")
            return True
            
        except Exception as e:
            self.log_test_result("End-to-End Integration", False, str(e))
            return False
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("🔗 Starting Comprehensive Integration Tests...")
        print("=" * 60)
        
        # Run all tests
        tests = [
            self.test_embedding_vector_db_integration,
            self.test_chat_repository_vector_db_integration,
            self.test_cache_embedding_integration,
            self.test_search_vector_db_integration,
            self.test_application_services_integration,
            self.test_health_monitoring_integration,
            self.test_end_to_end_integration
        ]
        
        for test in tests:
            try:
                await test()
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {e}")
                self.failed_tests += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {(self.passed_tests / (self.passed_tests + self.failed_tests)) * 100:.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL INTEGRATION TESTS PASSED! Components are properly integrated!")
            return True
        else:
            print(f"\n⚠️ {self.failed_tests} integration tests failed. Please fix before Git release.")
            return False

async def main():
    """Main integration test runner"""
    test_suite = IntegrationTestSuite()
    success = await test_suite.run_all_tests()
    
    if success:
        print("\n✅ All components are properly integrated for Git release!")
        return 0
    else:
        print("\n❌ Integration issues need to be fixed before Git release!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
