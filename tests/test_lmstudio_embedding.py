#!/usr/bin/env python3
"""LM Studio Embedding Service Tests"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import uuid
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService
from domain.utils.result import Result

class TestLMStudioEmbeddingService:
    """Test suite for LM Studio Embedding Service"""
    
    async def test_lmstudio_embedding_service(self):
        """Test LM Studio embedding service"""
        print('Testing LMStudioEmbeddingService...')
        
        try:
            # Test LM Studio service
            service = LMStudioEmbeddingService(
                proxy_url="http://127.0.0.1:8123",
                model_name="model:10"
            )
            print('OK: LMStudioEmbeddingService created')
            
            # Test single embedding
            print('Testing single embedding...')
            result = await service.create_embedding("Test text for LM Studio embedding")
            
            if result.is_success:
                embedding = result.value
                print(f'OK: Single embedding created, dimension: {len(embedding)}')
                print(f'   First 5 values: {embedding[:5]}')
            else:
                print(f'ERROR: Single embedding failed: {result.error}')
            
            # Test batch embeddings
            print('Testing batch embeddings...')
            texts = [
                "First text for LM Studio batch",
                "Second text for LM Studio batch", 
                "Third text for LM Studio batch"
            ]
            
            batch_result = await service.create_embeddings_batch(texts)
            
            if batch_result.is_success:
                embeddings = batch_result.value
                print(f'OK: Batch embeddings created, count: {len(embeddings)}')
                for i, emb in enumerate(embeddings):
                    print(f'   Text {i+1}: dimension {len(emb)}, first 3 values: {emb[:3]}')
            else:
                print(f'ERROR: Batch embeddings failed: {batch_result.error}')
            
            # Test model info
            print('Testing model info...')
            info_result = await service.get_model_info()
            
            if info_result.is_success:
                info = info_result.value
                print(f'OK: Model info: {info}')
            else:
                print(f'ERROR: Model info failed: {info_result.error}')
            
            # Test health check
            print('Testing health check...')
            health_result = await service.health_check()
            
            if health_result.is_success:
                health = health_result.value
                print(f'OK: Health check passed: {health}')
            else:
                print(f'ERROR: Health check failed: {health_result.error}')
                
        except Exception as e:
            print(f'ERROR: LMStudioEmbeddingService test failed: {e}')
    
    async def test_lmstudio_polish_text(self):
        """Test LM Studio with Polish text"""
        print('Testing LM Studio with Polish text...')
        
        try:
            service = LMStudioEmbeddingService(
                proxy_url="http://127.0.0.1:8123",
                model_name="model:10"
            )
            
            # Test Polish text
            polish_texts = [
                "test polskiego tekstu",
                "matematyka jest piękna",
                "testowanie systemów AI",
                "baza wektorowa Qdrant"
            ]
            
            for text in polish_texts:
                print(f'Testing Polish text: "{text}"')
                result = await service.create_embedding(text)
                
                if result.is_success:
                    embedding = result.value
                    print(f'OK: Polish embedding created, dimension: {len(embedding)}')
                else:
                    print(f'ERROR: Polish embedding failed: {result.error}')
                    
        except Exception as e:
            print(f'ERROR: Polish text test failed: {e}')

async def run_lmstudio_embedding_tests():
    """Run all LM Studio embedding tests"""
    print('Starting LM Studio Embedding Service tests...')
    print('=' * 60)
    
    test_instance = TestLMStudioEmbeddingService()
    
    try:
        await test_instance.test_lmstudio_embedding_service()
        print('-' * 60)
        await test_instance.test_lmstudio_polish_text()
        
        print('=' * 60)
        print('SUCCESS: All LM Studio embedding tests completed!')
        
    except Exception as e:
        print(f'ERROR: Test suite failed: {e}')
        raise

if __name__ == "__main__":
    asyncio.run(run_lmstudio_embedding_tests())
