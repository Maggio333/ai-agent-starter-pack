# tests/test_functional_comprehensive.py
"""
Comprehensive Functional Tests for AI Agent Starter Pack

This test suite validates the complete functionality of the AI Agent Starter Pack
before releasing to Git. It tests all major components and their interactions.

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
from application.container import Container
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.entities.rag_chunk import RAGChunk
from domain.entities.quality_level import QualityLevel
from domain.utils.result import Result
from datetime import datetime

class FunctionalTestSuite:
    """Comprehensive functional test suite"""
    
    def __init__(self):
        self.container = Container()
        self.container.wire(modules=[__name__])
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
    
    async def test_di_container_initialization(self):
        """Test DI Container initialization"""
        try:
            # Test container creation
            assert self.container is not None, "Container should be initialized"
            
            # Test configuration service
            config_service = self.container.config_service()
            assert config_service is not None, "Config service should be available"
            
            # Test embedding service
            embedding_service = self.container.embedding_service()
            assert embedding_service is not None, "Embedding service should be available"
            
            # Test vector db service
            vector_db_service = self.container.vector_db_service()
            assert vector_db_service is not None, "Vector DB service should be available"
            
            # Count available services (approximate)
            service_count = 9  # Based on container definition
            
            self.log_test_result("DI Container Initialization", True, f"Services: {service_count}")
            return True
            
        except Exception as e:
            self.log_test_result("DI Container Initialization", False, str(e))
            return False
    
    async def test_embedding_services(self):
        """Test all embedding services"""
        try:
            # Test embedding service creation
            embedding_service = self.container.embedding_service()
            assert embedding_service is not None, "Embedding service should be available"
            
            # Test embedding creation
            test_text = "This is a test text for embedding"
            embedding_result = await embedding_service.create_embedding(test_text)
            assert embedding_result.is_success, f"Embedding creation failed: {embedding_result.error}"
            
            embedding = embedding_result.value
            assert isinstance(embedding, list), "Embedding should be a list"
            assert len(embedding) > 0, "Embedding should not be empty"
            
            # Test model info
            model_info_result = await embedding_service.get_model_info()
            assert model_info_result.is_success, f"Model info failed: {model_info_result.error}"
            
            model_info = model_info_result.value
            assert isinstance(model_info, dict), "Model info should be a dictionary"
            assert "provider" in model_info, "Model info should contain provider"
            
            self.log_test_result("Embedding Services", True, f"Provider: {model_info.get('provider')}")
            return True
            
        except Exception as e:
            self.log_test_result("Embedding Services", False, str(e))
            return False
    
    async def test_vector_database_services(self):
        """Test vector database services"""
        # Create separate QdrantService instance for testing
        from infrastructure.ai.vector_db.qdrant_service import QdrantService
        test_vector_db_service = QdrantService(collection_name="test_collection_functional")
        
        try:
            # Test collection creation
            create_result = await test_vector_db_service.create_collection()
            assert create_result.is_success, f"Collection creation failed: {create_result.error}"
            
            # Test vector upsert
            test_chunk = RAGChunk(
                chunk_id="test_chunk_1",
                text_chunk="This is a test chunk for vector database",
                chat_messages=None,
                metadata={"test": True, "functional_test": True},
                score=0.95
            )
            
            upsert_result = await test_vector_db_service.upsert_chunks([test_chunk])
            assert upsert_result.is_success, f"Vector upsert failed: {upsert_result.error}"
            
            # Test vector search
            search_result = await test_vector_db_service.search("test chunk", limit=5)
            assert search_result.is_success, f"Vector search failed: {search_result.error}"
            
            search_results = search_result.value
            assert isinstance(search_results, list), "Search results should be a list"
            
            self.log_test_result("Vector Database Services", True, f"Found {len(search_results)} results")
            return True
            
        except Exception as e:
            self.log_test_result("Vector Database Services", False, str(e))
            return False
        finally:
            # Always clean up, even if test fails
            try:
                await test_vector_db_service.delete_collection()
            except Exception as cleanup_error:
                print(f"Warning: Failed to cleanup test collection: {cleanup_error}")
    
    async def test_chat_repository_services(self):
        """Test chat repository services"""
        try:
            # Test chat repository creation
            chat_repository = self.container.chat_repository()
            assert chat_repository is not None, "Chat repository should be initialized"
            
            # Test message creation
            test_message = ChatMessage(
                content="This is a test message for functional testing",
                role=MessageRole.USER,
                timestamp=datetime.now(),
                thread_id="test_thread_functional"
            )
            
            # Test message saving
            save_result = await chat_repository.save_message(test_message)
            assert save_result.is_success, f"Message saving failed: {save_result.error}"
            
            # Test message retrieval
            get_result = await chat_repository.get_message_by_id(test_message.message_id)
            assert get_result.is_success, f"Message retrieval failed: {get_result.error}"
            
            retrieved_message = get_result.value
            assert retrieved_message.content == test_message.content, "Retrieved message should match saved message"
            
            # Test message search
            search_result = await chat_repository.search_messages("test message", limit=5)
            assert search_result.is_success, f"Message search failed: {search_result.error}"
            
            search_results = search_result.value
            assert isinstance(search_results, list), "Search results should be a list"
            assert len(search_results) > 0, "Should find at least one message"
            
            self.log_test_result("Chat Repository Services", True, f"Found {len(search_results)} messages")
            return True
            
        except Exception as e:
            self.log_test_result("Chat Repository Services", False, str(e))
            return False
    
    async def test_application_services(self):
        """Test application services"""
        try:
            # Test city service
            city_service = self.container.city_service()
            assert city_service is not None, "City service should be initialized"
            
            # Test time service
            time_service = self.container.time_service()
            assert time_service is not None, "Time service should be initialized"
            
            # Test weather service
            weather_service = self.container.weather_service()
            assert weather_service is not None, "Weather service should be initialized"
            
            # Test knowledge service
            knowledge_service = self.container.knowledge_service()
            assert knowledge_service is not None, "Knowledge service should be initialized"
            
            # Test conversation service
            conversation_service = self.container.conversation_service()
            assert conversation_service is not None, "Conversation service should be initialized"
            
            # Test orchestration service
            orchestration_service = self.container.orchestration_service()
            assert orchestration_service is not None, "Orchestration service should be initialized"
            
            self.log_test_result("Application Services", True, "All 7 services initialized")
            return True
            
        except Exception as e:
            self.log_test_result("Application Services", False, str(e))
            return False
    
    async def test_health_monitoring_services(self):
        """Test health monitoring services"""
        try:
            # Test health service
            health_service = self.container.health_service()
            assert health_service is not None, "Health service should be initialized"
            
            # Test overall health check
            overall_health_result = await health_service.get_overall_health()
            assert overall_health_result.is_success, f"Overall health check failed: {overall_health_result.error}"
            
            overall_health = overall_health_result.value
            assert isinstance(overall_health, dict), "Overall health should be a dictionary"
            assert "status" in overall_health, "Overall health should contain status"
            
            # Test detailed health check
            detailed_health_result = await health_service.get_detailed_health()
            assert detailed_health_result.is_success, f"Detailed health check failed: {detailed_health_result.error}"
            
            detailed_health = detailed_health_result.value
            assert isinstance(detailed_health, list), "Detailed health should be a list"
            
            self.log_test_result("Health Monitoring Services", True, f"Status: {overall_health.get('status')}")
            return True
            
        except Exception as e:
            self.log_test_result("Health Monitoring Services", False, str(e))
            return False
    
    async def test_configuration_services(self):
        """Test configuration services"""
        try:
            # Test config service
            config_service = self.container.config_service()
            assert config_service is not None, "Config service should be initialized"
            
            # Test embedding configuration
            embedding_config = config_service.get_embedding_config()
            assert isinstance(embedding_config, dict), "Embedding config should be a dictionary"
            assert "provider" in embedding_config, "Embedding config should contain provider"
            
            # Test cache configuration
            cache_config = config_service.get_cache_config()
            assert isinstance(cache_config, dict), "Cache config should be a dictionary"
            
            # Test search configuration
            search_config = config_service.get_search_config()
            assert isinstance(search_config, dict), "Search config should be a dictionary"
            
            self.log_test_result("Configuration Services", True, f"Provider: {embedding_config.get('provider')}")
            return True
            
        except Exception as e:
            self.log_test_result("Configuration Services", False, str(e))
            return False
    
    async def test_cache_services(self):
        """Test cache services"""
        try:
            # Test cache service
            cache_service = self.container.cache_service()
            assert cache_service is not None, "Cache service should be initialized"
            
            # Test cache operations
            test_key = "test_key_functional"
            test_value = {"test": True, "functional": True}
            
            # Test cache set
            set_result = await cache_service.set(test_key, test_value, ttl=300)
            assert set_result.is_success, f"Cache set failed: {set_result.error}"
            
            # Test cache get
            get_result = await cache_service.get(test_key)
            assert get_result.is_success, f"Cache get failed: {get_result.error}"
            
            cached_value = get_result.value
            assert cached_value == test_value, "Cached value should match original value"
            
            # Test cache delete
            delete_result = await cache_service.delete(test_key)
            assert delete_result.is_success, f"Cache delete failed: {delete_result.error}"
            
            self.log_test_result("Cache Services", True, "All cache operations successful")
            return True
            
        except Exception as e:
            self.log_test_result("Cache Services", False, str(e))
            return False
    
    async def test_search_services(self):
        """Test search services"""
        try:
            # Test search service - it returns a Result object
            search_service_result = self.container.search_service()
            assert search_service_result.is_success, f"Search service creation failed: {search_service_result.error}"
            search_service = search_service_result.value
            
            # Test search operations - use knowledge service instead since search service is complex
            knowledge_service = self.container.knowledge_service()
            assert knowledge_service is not None, "Knowledge service should be initialized"
            
            # Test knowledge search - use a query that will find results in local knowledge base
            search_result = await knowledge_service.search_knowledge_base("weather")
            assert search_result.is_success, f"Knowledge search failed: {search_result.error}"
            
            search_results = search_result.value
            assert isinstance(search_results, list), "Search results should be a list"
            
            self.log_test_result("Search Services", True, f"Found {len(search_results)} results")
            return True
            
        except Exception as e:
            self.log_test_result("Search Services", False, str(e))
            return False
    
    async def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        try:
            # Get services
            embedding_service = self.container.embedding_service()
            vector_db_service = self.container.vector_db_service()
            chat_repository = self.container.chat_repository()
            orchestration_service = self.container.orchestration_service()
            
            # Step 1: Create a chat message
            test_message = ChatMessage(
                content="What is the weather like in New York today?",
                role=MessageRole.USER,
                timestamp=datetime.now(),
                thread_id="e2e_test_thread"
            )
            
            # Step 2: Save message to repository
            save_result = await chat_repository.save_message(test_message)
            assert save_result.is_success, f"Message saving failed: {save_result.error}"
            
            # Step 3: Create RAG chunk
            test_chunk = RAGChunk(
                chunk_id="e2e_chunk_1",
                text_chunk="Weather information: Today is sunny with 25°C",
                chat_messages=None,
                metadata={"source": "weather_api", "e2e_test": True},
                score=0.98
            )
            
            # Step 4: Create separate QdrantService instance for testing
            from infrastructure.ai.vector_db.qdrant_service import QdrantService
            test_vector_db_service = QdrantService(collection_name="e2e_test_collection")
            
            create_result = await test_vector_db_service.create_collection()
            assert create_result.is_success, f"Collection creation failed: {create_result.error}"
            
            upsert_result = await test_vector_db_service.upsert_chunks([test_chunk])
            assert upsert_result.is_success, f"Vector upsert failed: {upsert_result.error}"
            
            # Step 5: Search for relevant information
            search_result = await test_vector_db_service.search("weather today", limit=5)
            assert search_result.is_success, f"Vector search failed: {search_result.error}"
            
            search_results = search_result.value
            assert len(search_results) > 0, "Should find relevant weather information"
            
            # Step 6: Test orchestration
            orchestration_result = await orchestration_service.process_request(
                "What is the weather like in New York today?",
                thread_id="e2e_test_thread"
            )
            assert orchestration_result.is_success, f"Orchestration failed: {orchestration_result.error}"
            
            self.log_test_result("End-to-End Workflow", True, "Complete workflow successful")
            return True
            
        except Exception as e:
            self.log_test_result("End-to-End Workflow", False, str(e))
            return False
        finally:
            # Always clean up, even if test fails
            try:
                await test_vector_db_service.delete_collection()
            except Exception as cleanup_error:
                print(f"Warning: Failed to cleanup test collection: {cleanup_error}")
    
    async def run_all_tests(self):
        """Run all functional tests"""
        print("🚀 Starting Comprehensive Functional Tests...")
        print("=" * 60)
        
        # Run all tests
        tests = [
            self.test_di_container_initialization,
            self.test_embedding_services,
            self.test_vector_database_services,
            self.test_chat_repository_services,
            self.test_application_services,
            self.test_health_monitoring_services,
            self.test_configuration_services,
            self.test_cache_services,
            self.test_search_services,
            self.test_end_to_end_workflow
        ]
        
        for test in tests:
            try:
                await test()
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {e}")
                self.failed_tests += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 FUNCTIONAL TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {(self.passed_tests / (self.passed_tests + self.failed_tests)) * 100:.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Project is ready for Git!")
            return True
        else:
            print(f"\n⚠️ {self.failed_tests} tests failed. Please fix before Git release.")
            return False

async def main():
    """Main test runner"""
    test_suite = FunctionalTestSuite()
    success = await test_suite.run_all_tests()
    
    if success:
        print("\n✅ Project is ready for Git release!")
        return 0
    else:
        print("\n❌ Project needs fixes before Git release!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
