# tests/test_performance_comprehensive.py
"""
Performance Tests for AI Agent Starter Pack

This test suite validates the performance characteristics of the AI Agent Starter Pack
before releasing to Git. It tests response times, throughput, and resource usage.

Author: Arkadiusz Słota
Year: 2025
"""

import sys
import os
import asyncio
import time
import psutil
from datetime import datetime
from typing import List, Dict, Any

# Add project root to path
sys.path.append('.')

# Import all major components
from application.services.di_service import DIService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.entities.rag_chunk import RAGChunk
from domain.entities.quality_level import QualityLevel

class PerformanceTestSuite:
    """Performance test suite"""
    
    def __init__(self):
        self.di_service = DIService()
        self.container = self.di_service.get_container()
        self.test_results = []
        self.performance_metrics = {}
        
    def log_performance_result(self, test_name: str, duration: float, success: bool, message: str = ""):
        """Log performance test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {duration:.3f}s - {message}")
        
        self.test_results.append({
            "test_name": test_name,
            "duration": duration,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        self.performance_metrics[test_name] = duration
    
    async def test_embedding_performance(self):
        """Test embedding service performance"""
        try:
            start_time = time.time()
            
            # Get embedding service
            embedding_service = self.di_service.get_embedding_service()
            if embedding_result.is_error:
                self.log_performance_result("Embedding Performance", 0, False, "Service creation failed")
                return False
            
            embedding_service = embedding_result.value
            
            # Test single embedding
            single_start = time.time()
            embedding_result = await embedding_service.create_embedding("Performance test text")
            single_duration = time.time() - single_start
            
            if embedding_result.is_error:
                self.log_performance_result("Embedding Performance", single_duration, False, "Single embedding failed")
                return False
            
            # Test batch embeddings
            batch_texts = [f"Batch test text {i}" for i in range(10)]
            batch_start = time.time()
            batch_result = await embedding_service.create_embeddings_batch(batch_texts)
            batch_duration = time.time() - batch_start
            
            if batch_result.is_error:
                self.log_performance_result("Embedding Performance", batch_duration, False, "Batch embedding failed")
                return False
            
            total_duration = time.time() - start_time
            
            # Performance thresholds
            single_threshold = 2.0  # 2 seconds for single embedding
            batch_threshold = 5.0  # 5 seconds for batch of 10
            
            success = single_duration < single_threshold and batch_duration < batch_threshold
            
            self.log_performance_result(
                "Embedding Performance", 
                total_duration, 
                success, 
                f"Single: {single_duration:.3f}s, Batch: {batch_duration:.3f}s"
            )
            return success
            
        except Exception as e:
            self.log_performance_result("Embedding Performance", 0, False, str(e))
            return False
    
    async def test_vector_db_performance(self):
        """Test vector database performance"""
        try:
            start_time = time.time()
            
            # Get vector DB service
            vector_db_service = self.di_service.get_vector_db_service()
            
            # Test collection creation
            collection_name = "perf_test_collection"
            create_start = time.time()
            create_result = await vector_db_service.create_collection(collection_name)
            create_duration = time.time() - create_start
            
            if create_result.is_error:
                self.log_performance_result("Vector DB Performance", create_duration, False, "Collection creation failed")
                return False
            
            # Test bulk upsert
            test_chunks = [
                RAGChunk(
                    chunk_id=f"perf_chunk_{i}",
                    text_chunk=f"Performance test chunk {i}",
                    metadata={"test": True, "performance": True},
                    score=0.9,
                    quality_level=QualityLevel.EXCELLENT
                )
                for i in range(100)  # Test with 100 chunks
            ]
            
            upsert_start = time.time()
            upsert_result = await vector_db_service.upsert_chunks(test_chunks)
            upsert_duration = time.time() - upsert_start
            
            if upsert_result.is_error:
                self.log_performance_result("Vector DB Performance", upsert_duration, False, "Bulk upsert failed")
                return False
            
            # Test search performance
            search_start = time.time()
            search_result = await vector_db_service.search("performance test", limit=10)
            search_duration = time.time() - search_start
            
            if search_result.is_error:
                self.log_performance_result("Vector DB Performance", search_duration, False, "Search failed")
                return False
            
            # Clean up
            await vector_db_service.delete_collection(collection_name)
            
            total_duration = time.time() - start_time
            
            # Performance thresholds
            create_threshold = 1.0  # 1 second for collection creation
            upsert_threshold = 10.0  # 10 seconds for 100 chunks
            search_threshold = 2.0  # 2 seconds for search
            
            success = (create_duration < create_threshold and 
                      upsert_duration < upsert_threshold and 
                      search_duration < search_threshold)
            
            self.log_performance_result(
                "Vector DB Performance", 
                total_duration, 
                success, 
                f"Create: {create_duration:.3f}s, Upsert: {upsert_duration:.3f}s, Search: {search_duration:.3f}s"
            )
            return success
            
        except Exception as e:
            self.log_performance_result("Vector DB Performance", 0, False, str(e))
            return False
    
    async def test_chat_repository_performance(self):
        """Test chat repository performance"""
        try:
            start_time = time.time()
            
            # Get chat repository
            chat_repository = self.di_service.get_chat_repository()
            
            # Test bulk message operations
            test_messages = [
                ChatMessage(
                    content=f"Performance test message {i}",
                    role=MessageRole.USER,
                    thread_id="perf_test_thread"
                )
                for i in range(50)  # Test with 50 messages
            ]
            
            # Test bulk save
            save_start = time.time()
            for message in test_messages:
                save_result = await chat_repository.save_message(message)
                if save_result.is_error:
                    self.log_performance_result("Chat Repository Performance", 0, False, "Message save failed")
                    return False
            save_duration = time.time() - save_start
            
            # Test bulk retrieval
            get_start = time.time()
            for message in test_messages:
                get_result = await chat_repository.get_message_by_id(message.message_id)
                if get_result.is_error:
                    self.log_performance_result("Chat Repository Performance", 0, False, "Message retrieval failed")
                    return False
            get_duration = time.time() - get_start
            
            # Test search performance
            search_start = time.time()
            search_result = await chat_repository.search_messages("performance test", limit=20)
            search_duration = time.time() - search_start
            
            if search_result.is_error:
                self.log_performance_result("Chat Repository Performance", 0, False, "Message search failed")
                return False
            
            total_duration = time.time() - start_time
            
            # Performance thresholds
            save_threshold = 5.0  # 5 seconds for 50 messages
            get_threshold = 3.0  # 3 seconds for 50 retrievals
            search_threshold = 1.0  # 1 second for search
            
            success = (save_duration < save_threshold and 
                      get_duration < get_threshold and 
                      search_duration < search_threshold)
            
            self.log_performance_result(
                "Chat Repository Performance", 
                total_duration, 
                success, 
                f"Save: {save_duration:.3f}s, Get: {get_duration:.3f}s, Search: {search_duration:.3f}s"
            )
            return success
            
        except Exception as e:
            self.log_performance_result("Chat Repository Performance", 0, False, str(e))
            return False
    
    async def test_cache_performance(self):
        """Test cache service performance"""
        try:
            start_time = time.time()
            
            # Get cache service
            cache_service = self.di_service.get_cache_service()
            
            # Test bulk cache operations
            cache_operations = 100
            cache_start = time.time()
            
            for i in range(cache_operations):
                key = f"perf_cache_key_{i}"
                value = {"test": True, "performance": True, "index": i}
                
                # Test set
                set_result = await cache_service.set(key, value, ttl=300)
                if set_result.is_error:
                    self.log_performance_result("Cache Performance", 0, False, "Cache set failed")
                    return False
                
                # Test get
                get_result = await cache_service.get(key)
                if get_result.is_error:
                    self.log_performance_result("Cache Performance", 0, False, "Cache get failed")
                    return False
                
                # Test delete
                delete_result = await cache_service.delete(key)
                if delete_result.is_error:
                    self.log_performance_result("Cache Performance", 0, False, "Cache delete failed")
                    return False
            
            cache_duration = time.time() - cache_start
            total_duration = time.time() - start_time
            
            # Performance thresholds
            cache_threshold = 10.0  # 10 seconds for 100 operations
            
            success = cache_duration < cache_threshold
            
            self.log_performance_result(
                "Cache Performance", 
                total_duration, 
                success, 
                f"{cache_operations} operations in {cache_duration:.3f}s"
            )
            return success
            
        except Exception as e:
            self.log_performance_result("Cache Performance", 0, False, str(e))
            return False
    
    async def test_search_performance(self):
        """Test search service performance"""
        try:
            start_time = time.time()
            
            # Get search service
            search_service = self.di_service.get_search_service()
            
            # Test bulk document indexing
            documents = [
                {"id": f"perf_doc_{i}", "content": f"Performance test document {i} with search content"}
                for i in range(50)  # Test with 50 documents
            ]
            
            index_start = time.time()
            for doc in documents:
                index_result = await search_service.index_document(doc["id"], doc)
                if index_result.is_error:
                    self.log_performance_result("Search Performance", 0, False, "Document indexing failed")
                    return False
            index_duration = time.time() - index_start
            
            # Test search performance
            search_start = time.time()
            search_result = await search_service.search("performance test", limit=20)
            search_duration = time.time() - search_start
            
            if search_result.is_error:
                self.log_performance_result("Search Performance", 0, False, "Search failed")
                return False
            
            total_duration = time.time() - start_time
            
            # Performance thresholds
            index_threshold = 5.0  # 5 seconds for 50 documents
            search_threshold = 1.0  # 1 second for search
            
            success = index_duration < index_threshold and search_duration < search_threshold
            
            self.log_performance_result(
                "Search Performance", 
                total_duration, 
                success, 
                f"Index: {index_duration:.3f}s, Search: {search_duration:.3f}s"
            )
            return success
            
        except Exception as e:
            self.log_performance_result("Search Performance", 0, False, str(e))
            return False
    
    async def test_memory_usage(self):
        """Test memory usage"""
        try:
            start_time = time.time()
            
            # Get initial memory usage
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Perform memory-intensive operations
            embedding_service = self.di_service.get_embedding_service()
            vector_db_service = self.di_service.get_vector_db_service()
            
            # Create many embeddings
            texts = [f"Memory test text {i}" for i in range(100)]
            embeddings_result = await embedding_service.create_embeddings_batch(texts)
            
            if embeddings_result.is_error:
                self.log_performance_result("Memory Usage", 0, False, "Embeddings creation failed")
                return False
            
            # Create many vector chunks
            chunks = [
                RAGChunk(
                    chunk_id=f"mem_chunk_{i}",
                    text_chunk=f"Memory test chunk {i}",
                    metadata={"test": True, "memory": True},
                    score=0.9,
                    quality_level=QualityLevel.EXCELLENT
                )
                for i in range(100)
            ]
            
            collection_name = "mem_test_collection"
            await vector_db_service.create_collection(collection_name)
            await vector_db_service.upsert_chunks(chunks)
            
            # Get final memory usage
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Clean up
            await vector_db_service.delete_collection(collection_name)
            
            total_duration = time.time() - start_time
            
            # Memory threshold: should not increase by more than 500MB
            memory_threshold = 500.0  # MB
            
            success = memory_increase < memory_threshold
            
            self.log_performance_result(
                "Memory Usage", 
                total_duration, 
                success, 
                f"Memory increase: {memory_increase:.1f}MB"
            )
            return success
            
        except Exception as e:
            self.log_performance_result("Memory Usage", 0, False, str(e))
            return False
    
    async def test_concurrent_operations(self):
        """Test concurrent operations performance"""
        try:
            start_time = time.time()
            
            # Get services
            embedding_service = self.di_service.get_embedding_service()
            cache_service = self.di_service.get_cache_service()
            
            # Test concurrent operations
            async def concurrent_embedding_task(task_id: int):
                text = f"Concurrent test text {task_id}"
                result = await embedding_service.create_embedding(text)
                return result.is_success
            
            async def concurrent_cache_task(task_id: int):
                key = f"concurrent_cache_{task_id}"
                value = {"task_id": task_id, "concurrent": True}
                set_result = await cache_service.set(key, value, ttl=300)
                get_result = await cache_service.get(key)
                delete_result = await cache_service.delete(key)
                return set_result.is_success and get_result.is_success and delete_result.is_success
            
            # Run concurrent tasks
            concurrent_tasks = 20
            tasks = []
            
            for i in range(concurrent_tasks):
                tasks.append(concurrent_embedding_task(i))
                tasks.append(concurrent_cache_task(i))
            
            concurrent_start = time.time()
            results = await asyncio.gather(*tasks)
            concurrent_duration = time.time() - concurrent_start
            
            total_duration = time.time() - start_time
            
            # Check all tasks succeeded
            success_count = sum(results)
            total_tasks = len(results)
            success_rate = success_count / total_tasks
            
            # Performance thresholds
            concurrent_threshold = 10.0  # 10 seconds for 40 concurrent operations
            success_rate_threshold = 0.95  # 95% success rate
            
            success = (concurrent_duration < concurrent_threshold and 
                      success_rate >= success_rate_threshold)
            
            self.log_performance_result(
                "Concurrent Operations", 
                total_duration, 
                success, 
                f"{success_count}/{total_tasks} tasks succeeded in {concurrent_duration:.3f}s"
            )
            return success
            
        except Exception as e:
            self.log_performance_result("Concurrent Operations", 0, False, str(e))
            return False
    
    async def run_all_tests(self):
        """Run all performance tests"""
        print("⚡ Starting Comprehensive Performance Tests...")
        print("=" * 60)
        
        # Run all tests
        tests = [
            self.test_embedding_performance,
            self.test_vector_db_performance,
            self.test_chat_repository_performance,
            self.test_cache_performance,
            self.test_search_performance,
            self.test_memory_usage,
            self.test_concurrent_operations
        ]
        
        passed_tests = 0
        failed_tests = 0
        
        for test in tests:
            try:
                success = await test()
                if success:
                    passed_tests += 1
                else:
                    failed_tests += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {e}")
                failed_tests += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests / (passed_tests + failed_tests)) * 100:.1f}%")
        
        # Print performance metrics
        print("\n📈 PERFORMANCE METRICS:")
        for test_name, duration in self.performance_metrics.items():
            print(f"  {test_name}: {duration:.3f}s")
        
        if failed_tests == 0:
            print("\n🎉 ALL PERFORMANCE TESTS PASSED! Project meets performance requirements!")
            return True
        else:
            print(f"\n⚠️ {failed_tests} performance tests failed. Please optimize before Git release.")
            return False

async def main():
    """Main performance test runner"""
    test_suite = PerformanceTestSuite()
    success = await test_suite.run_all_tests()
    
    if success:
        print("\n✅ Project meets performance requirements for Git release!")
        return 0
    else:
        print("\n❌ Project needs performance optimization before Git release!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
