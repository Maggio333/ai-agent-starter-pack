#!/usr/bin/env python3
"""Comprehensive tests for EmbeddingService with HuggingFace"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import uuid
from infrastructure.ai.embeddings.huggingface_embedding_service import HuggingFaceEmbeddingService
from infrastructure.ai.embeddings.local_embedding_service import LocalEmbeddingService
from infrastructure.ai.embeddings.embedding_factory import EmbeddingFactory, EmbeddingProvider
from domain.utils.result import Result

class TestEmbeddingService:
    """Test suite for EmbeddingService"""
    
    async def test_huggingface_embedding_service(self):
        """Test HuggingFace embedding service"""
        print('🧪 Testing HuggingFaceEmbeddingService...')
        
        try:
            # Test HuggingFace service
            service = HuggingFaceEmbeddingService(model_name="all-MiniLM-L6-v2")
            print('✅ HuggingFaceEmbeddingService created')
            
            # Test single embedding
            print('🔍 Testing single embedding...')
            result = await service.create_embedding("Test text for embedding")
            
            if result.is_success:
                embedding = result.value
                print(f'✅ Single embedding created, dimension: {len(embedding)}')
                print(f'   First 5 values: {embedding[:5]}')
            else:
                print(f'❌ Single embedding failed: {result.error}')
            
            # Test batch embeddings
            print('🔍 Testing batch embeddings...')
            texts = [
                "First text for batch embedding",
                "Second text for batch embedding", 
                "Third text for batch embedding"
            ]
            
            batch_result = await service.create_embeddings_batch(texts)
            
            if batch_result.is_success:
                embeddings = batch_result.value
                print(f'✅ Batch embeddings created, count: {len(embeddings)}')
                for i, emb in enumerate(embeddings):
                    print(f'   Text {i+1}: dimension {len(emb)}, first 3 values: {emb[:3]}')
            else:
                print(f'❌ Batch embeddings failed: {batch_result.error}')
            
            # Test model info
            print('🔍 Testing model info...')
            info_result = await service.get_model_info()
            
            if info_result.is_success:
                info = info_result.value
                print(f'✅ Model info: {info}')
            else:
                print(f'❌ Model info failed: {info_result.error}')
            
            # Test health check
            print('🔍 Testing health check...')
            health_result = await service.health_check()
            
            if health_result.is_success:
                health = health_result.value
                print(f'✅ Health check passed: {health}')
            else:
                print(f'❌ Health check failed: {health_result.error}')
                
        except Exception as e:
            print(f'❌ HuggingFaceEmbeddingService test failed: {e}')
    
    async def test_local_embedding_service(self):
        """Test Local embedding service"""
        print('🧪 Testing LocalEmbeddingService...')
        
        try:
            # Test Local service
            service = LocalEmbeddingService(model_path="sentence-transformers/all-MiniLM-L6-v2")
            print('✅ LocalEmbeddingService created')
            
            # Test single embedding
            print('🔍 Testing single embedding...')
            result = await service.create_embedding("Test text for local embedding")
            
            if result.is_success:
                embedding = result.value
                print(f'✅ Single embedding created, dimension: {len(embedding)}')
                print(f'   First 5 values: {embedding[:5]}')
            else:
                print(f'❌ Single embedding failed: {result.error}')
            
            # Test batch embeddings
            print('🔍 Testing batch embeddings...')
            texts = [
                "First text for local batch",
                "Second text for local batch"
            ]
            
            batch_result = await service.create_embeddings_batch(texts)
            
            if batch_result.is_success:
                embeddings = batch_result.value
                print(f'✅ Batch embeddings created, count: {len(embeddings)}')
                for i, emb in enumerate(embeddings):
                    print(f'   Text {i+1}: dimension {len(emb)}, first 3 values: {emb[:3]}')
            else:
                print(f'❌ Batch embeddings failed: {batch_result.error}')
            
            # Test model info
            print('🔍 Testing model info...')
            info_result = await service.get_model_info()
            
            if info_result.is_success:
                info = info_result.value
                print(f'✅ Model info: {info}')
            else:
                print(f'❌ Model info failed: {info_result.error}')
                
        except Exception as e:
            print(f'❌ LocalEmbeddingService test failed: {e}')
    
    async def test_embedding_factory(self):
        """Test EmbeddingFactory"""
        print('🧪 Testing EmbeddingFactory...')
        
        try:
            factory = EmbeddingFactory()
            print('✅ EmbeddingFactory created')
            
            # Test available providers
            print('🔍 Testing available providers...')
            providers = factory.get_available_providers()
            print(f'✅ Available providers: {list(providers.keys())}')
            for provider, info in providers.items():
                print(f'   {provider}: {info["name"]} ({info["type"]})')
            
            # Test recommended provider
            print('🔍 Testing recommended provider...')
            free_provider = factory.get_recommended_provider("free")
            paid_provider = factory.get_recommended_provider("paid")
            
            print(f'✅ Recommended free provider: {free_provider}')
            print(f'✅ Recommended paid provider: {paid_provider}')
            
            # Test creating HuggingFace service
            print('🔍 Testing HuggingFace service creation...')
            hf_result = factory.create_service(EmbeddingProvider.HUGGINGFACE, model_name="all-MiniLM-L6-v2")
            
            if hf_result.is_success:
                hf_service = hf_result.value
                print('✅ HuggingFace service created via factory')
                
                # Test the service
                test_result = await hf_service.create_embedding("Factory test embedding")
                if test_result.is_success:
                    print(f'✅ Factory-created service works, dimension: {len(test_result.value)}')
                else:
                    print(f'❌ Factory-created service failed: {test_result.error}')
            else:
                print(f'❌ HuggingFace service creation failed: {hf_result.error}')
                
        except Exception as e:
            print(f'❌ EmbeddingFactory test failed: {e}')
    
    async def test_embedding_comparison(self):
        """Test comparison between different embedding services"""
        print('🧪 Testing embedding comparison...')
        
        try:
            test_text = "This is a test text for embedding comparison"
            
            # Create services
            hf_service = HuggingFaceEmbeddingService(model_name="all-MiniLM-L6-v2")
            local_service = LocalEmbeddingService(model_path="sentence-transformers/all-MiniLM-L6-v2")
            
            print('✅ Both services created')
            
            # Get embeddings
            hf_result = await hf_service.create_embedding(test_text)
            local_result = await local_service.create_embedding(test_text)
            
            if hf_result.is_success and local_result.is_success:
                hf_embedding = hf_result.value
                local_embedding = local_result.value
                
                print(f'✅ Both embeddings created')
                print(f'   HuggingFace dimension: {len(hf_embedding)}')
                print(f'   Local dimension: {len(local_embedding)}')
                
                # Compare dimensions
                if len(hf_embedding) == len(local_embedding):
                    print('✅ Dimensions match!')
                    
                    # Calculate similarity (cosine similarity)
                    import math
                    
                    dot_product = sum(a * b for a, b in zip(hf_embedding, local_embedding))
                    norm_hf = math.sqrt(sum(a * a for a in hf_embedding))
                    norm_local = math.sqrt(sum(b * b for b in local_embedding))
                    
                    similarity = dot_product / (norm_hf * norm_local)
                    print(f'✅ Cosine similarity: {similarity:.6f}')
                    
                    if similarity > 0.95:
                        print('🎉 Very high similarity - services produce similar embeddings!')
                    elif similarity > 0.8:
                        print('✅ Good similarity - services produce reasonably similar embeddings')
                    else:
                        print('⚠️ Low similarity - services produce different embeddings')
                else:
                    print('❌ Dimensions don\'t match!')
            else:
                print(f'❌ Embedding comparison failed')
                if not hf_result.is_success:
                    print(f'   HuggingFace error: {hf_result.error}')
                if not local_result.is_success:
                    print(f'   Local error: {local_result.error}')
                    
        except Exception as e:
            print(f'❌ Embedding comparison test failed: {e}')

async def run_embedding_tests():
    """Run all embedding tests"""
    print('🚀 Starting comprehensive EmbeddingService tests...')
    print('=' * 60)
    
    test_instance = TestEmbeddingService()
    
    try:
        await test_instance.test_huggingface_embedding_service()
        print('-' * 60)
        await test_instance.test_local_embedding_service()
        print('-' * 60)
        await test_instance.test_embedding_factory()
        print('-' * 60)
        await test_instance.test_embedding_comparison()
        
        print('=' * 60)
        print('🎉 All embedding tests completed!')
        
    except Exception as e:
        print(f'❌ Test suite failed: {e}')
        raise

if __name__ == "__main__":
    asyncio.run(run_embedding_tests())
