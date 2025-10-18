#!/usr/bin/env python3
"""Simple LM Studio Integration Test"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService
from infrastructure.ai.vector_db.qdrant_service import QdrantService

class TestLMStudioSimple:
    """Simple test suite for LM Studio integration"""
    
    async def test_lmstudio_embedding(self):
        """Test LM Studio embedding service"""
        print("Testing LM Studio Embedding Service...")
        
        try:
            # Create LM Studio service
            service = LMStudioEmbeddingService(
                proxy_url="http://127.0.0.1:8123",
                model_name="model:10"
            )
            print("OK: LM Studio service created")
            
            # Test embedding
            result = await service.create_embedding("Test text for LM Studio")
            
            if result.is_success:
                embedding = result.value
                print(f"OK: Embedding created, dimension: {len(embedding)}")
                print(f"First 3 values: {embedding[:3]}")
                return True
            else:
                print(f"ERROR: Embedding failed: {result.error}")
                return False
                
        except Exception as e:
            print(f"ERROR: LM Studio test failed: {e}")
            return False

    async def test_qdrant_connection(self):
        """Test Qdrant vector database connection"""
        print("\nTesting Qdrant Vector Database...")
        
        try:
            # Test with existing collections
            collections = ['TopicCollection']
            
            for collection_name in collections:
                print(f"\nTesting collection: {collection_name}")
                
                service = QdrantService(
                    url='http://localhost:6333', 
                    collection_name=collection_name
                )
                
                # Test search
                result = await service.search('test', limit=2)
                
                if result.is_success:
                    print(f"OK: Found {len(result.value)} results")
                    for i, chunk in enumerate(result.value):
                        print(f"  {i+1}. Score: {chunk.score:.6f}")
                        try:
                            # Safe text display
                            text_preview = chunk.text_chunk[:50].encode('ascii', 'ignore').decode('ascii')
                            print(f"      Text: {text_preview}...")
                        except:
                            print(f"      Text: [Polish text]")
                else:
                    print(f"ERROR: Search failed: {result.error}")
                    
            return True
                    
        except Exception as e:
            print(f"ERROR: Qdrant test failed: {e}")
            return False

async def run_simple_lmstudio_tests():
    """Run simple LM Studio tests"""
    print("Starting Simple LM Studio Integration Tests")
    print("=" * 50)
    
    test_instance = TestLMStudioSimple()
    
    try:
        # Test LM Studio
        lmstudio_ok = await test_instance.test_lmstudio_embedding()
        
        # Test Qdrant
        qdrant_ok = await test_instance.test_qdrant_connection()
        
        print("\n" + "=" * 50)
        if lmstudio_ok and qdrant_ok:
            print("SUCCESS: LM Studio and Vector DB are working!")
        else:
            print("ERROR: Some components are not working properly")
        
    except Exception as e:
        print(f"ERROR: Test suite failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_simple_lmstudio_tests())
