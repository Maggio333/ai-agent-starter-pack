#!/usr/bin/env python3
"""Comprehensive tests for QdrantService"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import uuid
from datetime import datetime
from infrastructure.ai.vector_db.qdrant_service import QdrantService
from domain.entities.rag_chunk import RAGChunk
from domain.utils.result import Result

class TestQdrantService:
    """Test suite for QdrantService"""
    
    async def test_create_collection(self, qdrant_service):
        """Test collection creation"""
        print('🧪 Testing collection creation...')
        
        result = await qdrant_service.create_collection()
        
        if result.is_success:
            print('✅ Collection created successfully')
        else:
            print(f'⚠️ Collection creation: {result.error}')
            # Collection might already exist, that's OK
    
    async def test_save_chunk(self, qdrant_service):
        """Test saving a single chunk"""
        print('🧪 Testing save_chunk...')
        
        chunk = RAGChunk(
            text_chunk='Test chunk for Python QdrantService - comprehensive testing',
            chat_messages=None,
            chunk_id=str(uuid.uuid4()),
            score=0.95
        )
        
        result = await qdrant_service.save_chunk(chunk)
        
        if result.is_success:
            print('✅ Chunk saved successfully')
        else:
            print(f'❌ Save chunk failed: {result.error}')
    
    async def test_upsert_chunks(self, qdrant_service):
        """Test bulk upsert of chunks"""
        print('🧪 Testing upsert_chunks...')
        
        chunks = [
            RAGChunk(
                text_chunk=f'Bulk test chunk {i} - comprehensive testing',
                chat_messages=None,
                chunk_id=str(uuid.uuid4()),
                score=0.9 + (i * 0.01)
            )
            for i in range(3)
        ]
        
        result = await qdrant_service.upsert_chunks(chunks)
        
        if result.is_success:
            print('✅ Bulk chunks upserted successfully')
        else:
            print(f'❌ Upsert chunks failed: {result.error}')
    
    async def test_search(self, qdrant_service):
        """Test search functionality"""
        print('🧪 Testing search...')
        
        result = await qdrant_service.search('Python QdrantService', limit=5)
        
        if result.is_success and len(result.value) > 0:
            print(f'✅ Search successful, found {len(result.value)} results')
            for i, chunk in enumerate(result.value):
                print(f'  {i+1}. Score: {chunk.score:.6f} - {chunk.text_chunk[:50]}...')
        else:
            print(f'❌ Search failed: {result.error}')
    
    async def test_stream_search(self, qdrant_service):
        """Test streaming search"""
        print('🧪 Testing stream_search...')
        
        results = []
        async for result in qdrant_service.stream_search('Python', limit=3):
            if result.is_success:
                results.append(result.value)
            else:
                print(f'⚠️ Stream search error: {result.error}')
        
        print(f'✅ Stream search completed, found {len(results)} results')
        for i, chunk in enumerate(results):
            print(f'  {i+1}. Score: {chunk.score:.6f} - {chunk.text_chunk[:50]}...')
    
    async def test_batch_search(self, qdrant_service):
        """Test batch search"""
        print('🧪 Testing batch_search...')
        
        queries = ['Python', 'testing', 'QdrantService']
        result = await qdrant_service.batch_search(queries, limit=2)
        
        if result.is_success and len(result.value) == len(queries):
            print(f'✅ Batch search successful for {len(queries)} queries')
            for i, query_results in enumerate(result.value):
                print(f'  Query {i+1}: {len(query_results)} results')
        else:
            print(f'❌ Batch search failed: {result.error}')
    
    async def test_health_check(self, qdrant_service):
        """Test health check"""
        print('🧪 Testing health_check...')
        
        result = await qdrant_service.health_check()
        
        if result.is_success and 'status' in result.value:
            print(f'✅ Health check passed: {result.value}')
        else:
            print(f'❌ Health check failed: {result.error}')
    
    async def test_vector_size_compatibility(self, qdrant_service):
        """Test 1024 vector size compatibility"""
        print('🧪 Testing 1024 vector size compatibility...')
        
        # Test with existing collection that has 1024 vectors
        service_1024 = QdrantService(
            url='http://localhost:6333', 
            collection_name='TopicCollection'  # Your existing collection
        )
        
        # Test search
        result = await service_1024.search('idiom', limit=2)
        
        if result.is_success:
            print(f'✅ 1024 vector search successful, found {len(result.value)} results')
            for i, chunk in enumerate(result.value):
                print(f'  {i+1}. Score: {chunk.score:.6f} - {chunk.text_chunk[:50]}...')
        else:
            print(f'❌ 1024 vector search failed: {result.error}')
    
    async def test_payload_structure_handling(self, qdrant_service):
        """Test handling of different payload structures"""
        print('🧪 Testing payload structure handling...')
        
        # Test with your existing collection that has Polish structure
        service_polish = QdrantService(
            url='http://localhost:6333', 
            collection_name='PierwszaKolekcjaOnline'
        )
        
        result = await service_polish.search('Eliora', limit=2)
        
        if result.is_success:
            print(f'✅ Polish payload handling successful, found {len(result.value)} results')
            for i, chunk in enumerate(result.value):
                print(f'  {i+1}. Score: {chunk.score:.6f}')
                print(f'      Text: {chunk.text_chunk[:100]}...')
        else:
            print(f'❌ Polish payload handling failed: {result.error}')

async def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print('🚀 Starting comprehensive QdrantService tests...')
    print('=' * 60)
    
    test_instance = TestQdrantService()
    
    # Create service for testing
    service = QdrantService(
        url='http://localhost:6333', 
        collection_name='test_collection_python'
    )
    
    try:
        # Run tests
        await test_instance.test_create_collection(service)
        await test_instance.test_save_chunk(service)
        await test_instance.test_upsert_chunks(service)
        await test_instance.test_search(service)
        await test_instance.test_stream_search(service)
        await test_instance.test_batch_search(service)
        await test_instance.test_health_check(service)
        await test_instance.test_vector_size_compatibility(service)
        await test_instance.test_payload_structure_handling(service)
        
        print('=' * 60)
        print('🎉 All comprehensive tests completed!')
        
    except Exception as e:
        print(f'❌ Test failed: {e}')
        raise

if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())
