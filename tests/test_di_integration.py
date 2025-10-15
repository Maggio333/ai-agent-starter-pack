#!/usr/bin/env python3
"""Test DI + LM Studio + Qdrant integration"""

import sys
import os
sys.path.append('.')

import asyncio
from datetime import datetime
from application.container import ContainerManager
from domain.entities.rag_chunk import RAGChunk
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.models.metadata import RAGChunkMetadata, MetadataType

async def test_di_integration():
    print('🎯 Testing DI + LM Studio + Qdrant Integration...')
    print('=' * 60)
    
    # Initialize DI Container
    print('📦 Initializing DI Container...')
    container_manager = ContainerManager()
    container = container_manager.container
    
    # Get services from DI
    print('🔧 Getting services from DI...')
    embedding_service_result = container.embedding_service()
    vector_db_service = container.vector_db_service()
    
    if embedding_service_result.is_error:
        print(f'❌ Failed to get embedding service: {embedding_service_result.error}')
        return
    
    embedding_service = embedding_service_result.value
    print(f'✅ Embedding Service: {type(embedding_service).__name__}')
    print(f'✅ Vector DB Service: {type(vector_db_service).__name__}')
    
    # Test embedding service
    print('\n🧠 Testing Embedding Service...')
    embedding_result = await embedding_service.create_embedding("Test text for DI integration")
    if embedding_result.is_success:
        print(f'✅ Embedding created: {len(embedding_result.value)} dimensions')
        print(f'   First 5 values: {embedding_result.value[:5]}')
    else:
        print(f'❌ Embedding failed: {embedding_result.error}')
        return
    
    # Test model info
    info_result = await embedding_service.get_model_info()
    if info_result.is_success:
        print(f'✅ Model info: {info_result.value["provider"]} - {info_result.value["type"]}')
    
    # Test health check
    health_result = await embedding_service.health_check()
    if health_result.is_success:
        print(f'✅ Health check: {health_result.value["status"]}')
    
    # Test vector DB service
    print('\n🗄️ Testing Vector DB Service...')
    
    # Create collection first
    print('🏗️ Creating collection...')
    create_result = await vector_db_service.create_collection()
    if create_result.is_success:
        print('✅ Collection created successfully!')
    else:
        print(f'⚠️ Collection creation: {create_result.error}')
    
    # Create test chunks with real embeddings
    test_chunks = [
        RAGChunk(
            text_chunk="Matematyczne idiomy są fascynujące",
            chat_messages=[
                ChatMessage(
                    content="Czy możesz opowiedzieć o matematycznych idiomach?",
                    role=MessageRole.USER,
                    timestamp=datetime.now()
                ),
                ChatMessage(
                    content="Matematyczne idiomy są fascynujące! To są wyrażenia, które mają ukryte znaczenie matematyczne.",
                    role=MessageRole.ASSISTANT,
                    timestamp=datetime.now()
                )
            ],
            chunk_id="test_1",
            score=0.95,
            metadata=RAGChunkMetadata(
                entity_type=MetadataType.RAG_CHUNK,
                entity_id="test_1",
                source="test",
                quality_level="high"
            )
        ),
        RAGChunk(
            text_chunk="Symbole matematyczne mają głębokie znaczenie",
            chat_messages=[
                ChatMessage(
                    content="Co oznaczają symbole matematyczne?",
                    role=MessageRole.USER,
                    timestamp=datetime.now()
                ),
                ChatMessage(
                    content="Symbole matematyczne mają głębokie znaczenie i reprezentują abstrakcyjne koncepty.",
                    role=MessageRole.ASSISTANT,
                    timestamp=datetime.now()
                )
            ],
            chunk_id="test_2", 
            score=0.88,
            metadata=RAGChunkMetadata(
                entity_type=MetadataType.RAG_CHUNK,
                entity_id="test_2",
                source="test",
                quality_level="medium"
            )
        )
    ]
    
    print(f'📝 Created {len(test_chunks)} test chunks')
    
    # Test upsert with real embeddings
    print('💾 Testing upsert with real embeddings...')
    upsert_result = await vector_db_service.upsert_chunks(test_chunks)
    if upsert_result.is_success:
        print('✅ Chunks upserted successfully with real embeddings!')
    else:
        print(f'❌ Upsert failed: {upsert_result.error}')
    
    # Test search with real embeddings
    print('\n🔍 Testing search with real embeddings...')
    search_result = await vector_db_service.search("matematyczne idiomy", limit=2)
    if search_result.is_success:
        print(f'✅ Search successful: {len(search_result.value)} results')
        for i, chunk in enumerate(search_result.value):
            print(f'   {i+1}. Score: {chunk.score:.3f} - "{chunk.text_chunk[:50]}..."')
    else:
        print(f'❌ Search failed: {search_result.error}')
    
    # Test streaming search
    print('\n🌊 Testing streaming search...')
    async for result in vector_db_service.stream_search("symbole matematyczne", limit=1):
        if result.is_success:
            chunk = result.value
            print(f'✅ Stream result: Score {chunk.score:.3f} - "{chunk.text_chunk[:50]}..."')
        else:
            print(f'❌ Stream error: {result.error}')
        break  # Just test first result
    
    # Test stats
    print('\n📊 Testing collection stats...')
    stats_result = await vector_db_service.get_stats()
    if stats_result.is_success:
        print(f'✅ Collection stats: {stats_result.value}')
    else:
        print(f'❌ Stats failed: {stats_result.error}')
    
    print('\n🎉 DI + LM Studio + Qdrant integration test completed!')
    print('=' * 60)

if __name__ == "__main__":
    asyncio.run(test_di_integration())
