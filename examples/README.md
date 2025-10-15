# Examples

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

This directory contains practical examples demonstrating how to use the AI Agent Starter Pack.

## 🚀 Quick Start Examples

### **Basic Usage**
```python
# examples/basic_usage.py
import asyncio
from application.container import ContainerManager

async def main():
    """Basic usage example."""
    print("🚀 AI Agent Starter Pack - Basic Usage")
    print("=" * 50)
    
    # Initialize container
    container_manager = ContainerManager()
    container = container_manager.container
    
    # Get services
    embedding_service = container.embedding_service().value
    vector_db_service = container.vector_db_service()
    health_service = container.health_service()
    
    # Create embedding
    print("📝 Creating embedding...")
    result = await embedding_service.create_embedding("Hello, AI world!")
    if result.is_success:
        embedding = result.value
        print(f"✅ Embedding created: {len(embedding)} dimensions")
    else:
        print(f"❌ Embedding failed: {result.error}")
    
    # Check health
    print("\n🏥 Checking system health...")
    result = await health_service.get_overall_health()
    if result.is_success:
        health = result.value
        print(f"✅ System status: {health['status']}")
        print(f"📊 Services checked: {health['services_checked']}")
        print(f"⏱️ Response time: {health['response_time_ms']:.2f}ms")
    else:
        print(f"❌ Health check failed: {result.error}")
    
    print("\n🎉 Basic usage completed!")

if __name__ == "__main__":
    asyncio.run(main())
```

### **Embedding Service Examples**
```python
# examples/embedding_examples.py
import asyncio
from application.container import ContainerManager

async def test_embedding_providers():
    """Test different embedding providers."""
    print("🔤 Embedding Service Examples")
    print("=" * 50)
    
    container_manager = ContainerManager()
    container = container_manager.container
    
    # Get embedding service
    embedding_service = container.embedding_service().value
    
    # Test single embedding
    print("📝 Testing single embedding...")
    result = await embedding_service.create_embedding("Hello, world!")
    if result.is_success:
        embedding = result.value
        print(f"✅ Single embedding: {len(embedding)} dimensions")
        print(f"📊 First 5 values: {embedding[:5]}")
    else:
        print(f"❌ Single embedding failed: {result.error}")
    
    # Test batch embeddings
    print("\n📝 Testing batch embeddings...")
    texts = ["Hello", "World", "AI", "Agent", "Starter"]
    result = await embedding_service.create_embeddings_batch(texts)
    if result.is_success:
        embeddings = result.value
        print(f"✅ Batch embeddings: {len(embeddings)} texts")
        print(f"📊 Dimensions per text: {len(embeddings[0])}")
    else:
        print(f"❌ Batch embeddings failed: {result.error}")
    
    # Test model info
    print("\n📝 Testing model info...")
    result = await embedding_service.get_model_info()
    if result.is_success:
        info = result.value
        print(f"✅ Model info:")
        print(f"   Provider: {info['provider']}")
        print(f"   Model: {info['model_name']}")
        print(f"   Dimensions: {info['dimension']}")
        print(f"   Cost: {info['cost']}")
    else:
        print(f"❌ Model info failed: {result.error}")
    
    print("\n🎉 Embedding examples completed!")

if __name__ == "__main__":
    asyncio.run(test_embedding_providers())
```

### **Vector Database Examples**
```python
# examples/vector_db_examples.py
import asyncio
from application.container import ContainerManager
from domain.entities.rag_chunk import RAGChunk
from domain.entities.chat_message import ChatMessage
from datetime import datetime

async def test_vector_database():
    """Test vector database operations."""
    print("🗄️ Vector Database Examples")
    print("=" * 50)
    
    container_manager = ContainerManager()
    container = container_manager.container
    
    # Get services
    embedding_service = container.embedding_service().value
    vector_db_service = container.vector_db_service()
    
    # Create collection
    print("📝 Creating collection...")
    result = await vector_db_service.create_collection()
    if result.is_success:
        print("✅ Collection created successfully")
    else:
        print(f"❌ Collection creation failed: {result.error}")
    
    # Create test chunks
    print("\n📝 Creating test chunks...")
    chunks = [
        RAGChunk(
            chunk_id="1",
            text_chunk="Artificial intelligence is transforming the world",
            metadata={"source": "AI article", "page": 1},
            score=0.95,
            chat_messages=None
        ),
        RAGChunk(
            chunk_id="2",
            text_chunk="Machine learning algorithms are becoming more sophisticated",
            metadata={"source": "ML article", "page": 2},
            score=0.88,
            chat_messages=None
        ),
        RAGChunk(
            chunk_id="3",
            text_chunk="Natural language processing enables human-computer interaction",
            metadata={"source": "NLP article", "page": 3},
            score=0.92,
            chat_messages=None
        )
    ]
    
    # Upsert chunks
    print("📝 Upserting chunks...")
    result = await vector_db_service.upsert_chunks(chunks)
    if result.is_success:
        print(f"✅ Upserted {len(chunks)} chunks successfully")
    else:
        print(f"❌ Upsert failed: {result.error}")
    
    # Search
    print("\n📝 Searching for 'artificial intelligence'...")
    result = await vector_db_service.search("artificial intelligence", limit=3)
    if result.is_success:
        search_results = result.value
        print(f"✅ Found {len(search_results)} results:")
        for i, chunk in enumerate(search_results, 1):
            print(f"   {i}. Score: {chunk.score:.3f}")
            print(f"      Text: {chunk.text_chunk[:50]}...")
            print(f"      Source: {chunk.metadata.get('source', 'N/A')}")
    else:
        print(f"❌ Search failed: {result.error}")
    
    # Search with different query
    print("\n📝 Searching for 'machine learning'...")
    result = await vector_db_service.search("machine learning", limit=2)
    if result.is_success:
        search_results = result.value
        print(f"✅ Found {len(search_results)} results:")
        for i, chunk in enumerate(search_results, 1):
            print(f"   {i}. Score: {chunk.score:.3f}")
            print(f"      Text: {chunk.text_chunk[:50]}...")
    else:
        print(f"❌ Search failed: {result.error}")
    
    print("\n🎉 Vector database examples completed!")

if __name__ == "__main__":
    asyncio.run(test_vector_database())
```

### **Health Monitoring Examples**
```python
# examples/health_monitoring_examples.py
import asyncio
from application.container import ContainerManager
from infrastructure.monitoring.health.embedding_health_service import EmbeddingHealthService
from infrastructure.monitoring.health.qdrant_health_service import QdrantHealthService

async def test_health_monitoring():
    """Test health monitoring capabilities."""
    print("🏥 Health Monitoring Examples")
    print("=" * 50)
    
    container_manager = ContainerManager()
    container = container_manager.container
    
    # Get services
    embedding_service = container.embedding_service().value
    vector_db_service = container.vector_db_service()
    health_service = container.health_service()
    
    # Register individual health services
    print("📝 Registering health services...")
    embedding_health = EmbeddingHealthService(embedding_service)
    qdrant_health = QdrantHealthService(vector_db_service)
    
    health_service.register_service(embedding_health)
    health_service.register_service(qdrant_health)
    print(f"✅ Registered {len(health_service._health_services)} services")
    
    # Test individual service health
    print("\n📝 Testing individual service health...")
    detailed_result = await health_service.get_detailed_health()
    if detailed_result.is_success:
        health_checks = detailed_result.value
        for check in health_checks:
            print(f"🔍 {check.service_name}:")
            print(f"   Status: {check.status}")
            print(f"   Message: {check.message}")
            if check.response_time_ms is not None:
                print(f"   Response time: {check.response_time_ms:.2f}ms")
            if check.details:
                print(f"   Details: {check.details}")
            print()
    else:
        print(f"❌ Detailed health check failed: {detailed_result.error}")
    
    # Test overall system health
    print("📝 Testing overall system health...")
    overall_result = await health_service.get_overall_health()
    if overall_result.is_success:
        overall_health = overall_result.value
        print(f"✅ Overall Status: {overall_health['status']}")
        print(f"📝 Message: {overall_health['message']}")
        print(f"⏱️ Response time: {overall_health['response_time_ms']:.2f}ms")
        print(f"📊 Services checked: {overall_health['services_checked']}")
        print(f"✅ Healthy services: {overall_health['healthy_services']}")
        print(f"❌ Unhealthy services: {overall_health['unhealthy_services']}")
        print(f"⚠️ Degraded services: {overall_health['degraded_services']}")
    else:
        print(f"❌ Overall health check failed: {overall_result.error}")
    
    print("\n🎉 Health monitoring examples completed!")

if __name__ == "__main__":
    asyncio.run(test_health_monitoring())
```

## 🔧 Advanced Examples

### **Custom Service Implementation**
```python
# examples/custom_service_example.py
import asyncio
from typing import List, Dict, Any
from domain.utils.result import Result
from infrastructure.ai.embeddings.base_embedding_service import BaseEmbeddingService

class CustomEmbeddingService(BaseEmbeddingService):
    """Custom embedding service implementation."""
    
    def __init__(self, custom_param: str):
        self.custom_param = custom_param
        self.embedding_dimension = 512  # Custom dimension
    
    async def create_embedding(self, text: str) -> Result[List[float], str]:
        """Create a custom embedding."""
        try:
            # Custom embedding logic here
            # For demo purposes, return dummy embedding
            embedding = [0.1] * self.embedding_dimension
            return Result.success(embedding)
        except Exception as e:
            return Result.error(f"Custom embedding failed: {str(e)}")
    
    async def create_embeddings_batch(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Create batch embeddings."""
        try:
            embeddings = []
            for text in texts:
                result = await self.create_embedding(text)
                if result.is_success:
                    embeddings.append(result.value)
                else:
                    return Result.error(f"Batch embedding failed: {result.error}")
            return Result.success(embeddings)
        except Exception as e:
            return Result.error(f"Batch embedding failed: {str(e)}")
    
    async def get_model_info(self) -> Result[Dict[str, Any], str]:
        """Get custom model info."""
        return Result.success({
            "provider": "Custom",
            "model_name": "custom-model",
            "dimension": self.embedding_dimension,
            "custom_param": self.custom_param,
            "cost": "free"
        })
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Custom health check."""
        return Result.success({
            "status": "healthy",
            "provider": "Custom",
            "custom_param": self.custom_param,
            "dimension": self.embedding_dimension
        })

async def test_custom_service():
    """Test custom service implementation."""
    print("🔧 Custom Service Example")
    print("=" * 50)
    
    # Create custom service
    custom_service = CustomEmbeddingService("test-param")
    
    # Test embedding
    result = await custom_service.create_embedding("Hello, custom service!")
    if result.is_success:
        embedding = result.value
        print(f"✅ Custom embedding: {len(embedding)} dimensions")
    else:
        print(f"❌ Custom embedding failed: {result.error}")
    
    # Test model info
    result = await custom_service.get_model_info()
    if result.is_success:
        info = result.value
        print(f"✅ Custom model info: {info}")
    else:
        print(f"❌ Custom model info failed: {result.error}")
    
    # Test health check
    result = await custom_service.health_check()
    if result.is_success:
        health = result.value
        print(f"✅ Custom health check: {health}")
    else:
        print(f"❌ Custom health check failed: {result.error}")
    
    print("\n🎉 Custom service example completed!")

if __name__ == "__main__":
    asyncio.run(test_custom_service())
```

### **ROP Pattern Examples**
```python
# examples/rop_pattern_examples.py
import asyncio
from domain.utils.result import Result
from domain.services.rop_service import ROPService

async def validate_input(data: str) -> Result[str, str]:
    """Validate input data."""
    if not data or len(data.strip()) == 0:
        return Result.error("Input cannot be empty")
    
    if len(data) > 1000:
        return Result.error("Input too long")
    
    return Result.success(data.strip())

async def process_data(data: str) -> Result[str, str]:
    """Process the data."""
    try:
        # Simulate processing
        processed = data.upper()
        return Result.success(processed)
    except Exception as e:
        return Result.error(f"Processing failed: {str(e)}")

async def save_result(data: str) -> Result[str, str]:
    """Save the result."""
    try:
        # Simulate saving
        saved = f"Saved: {data}"
        return Result.success(saved)
    except Exception as e:
        return Result.error(f"Saving failed: {str(e)}")

async def test_rop_pattern():
    """Test Railway Oriented Programming pattern."""
    print("🔄 ROP Pattern Examples")
    print("=" * 50)
    
    # Create pipeline
    pipeline = ROPService.pipeline(
        validate_input,
        process_data,
        save_result
    )
    
    # Test successful pipeline
    print("📝 Testing successful pipeline...")
    result = await pipeline("hello world")
    if result.is_success:
        print(f"✅ Pipeline success: {result.value}")
    else:
        print(f"❌ Pipeline failed: {result.error}")
    
    # Test validation error
    print("\n📝 Testing validation error...")
    result = await pipeline("")
    if result.is_error:
        print(f"✅ Validation error caught: {result.error}")
    else:
        print(f"❌ Validation error not caught: {result.value}")
    
    # Test processing error
    print("\n📝 Testing processing error...")
    result = await pipeline("a" * 2000)  # Too long
    if result.is_error:
        print(f"✅ Processing error caught: {result.error}")
    else:
        print(f"❌ Processing error not caught: {result.value}")
    
    # Test individual operations
    print("\n📝 Testing individual operations...")
    
    # Test validation
    result = await validate_input("test")
    if result.is_success:
        print(f"✅ Validation success: {result.value}")
    else:
        print(f"❌ Validation failed: {result.error}")
    
    # Test processing
    result = await process_data("test")
    if result.is_success:
        print(f"✅ Processing success: {result.value}")
    else:
        print(f"❌ Processing failed: {result.error}")
    
    # Test saving
    result = await save_result("TEST")
    if result.is_success:
        print(f"✅ Saving success: {result.value}")
    else:
        print(f"❌ Saving failed: {result.error}")
    
    print("\n🎉 ROP pattern examples completed!")

if __name__ == "__main__":
    asyncio.run(test_rop_pattern())
```

## 🧪 Testing Examples

### **Unit Test Example**
```python
# examples/unit_test_example.py
import pytest
import asyncio
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService

class TestLMStudioEmbeddingService:
    """Test class for LM Studio embedding service."""
    
    @pytest.fixture
    def service(self):
        """Create service instance."""
        return LMStudioEmbeddingService(
            proxy_url="http://127.0.0.1:8123",
            model_name="model:10"
        )
    
    @pytest.mark.asyncio
    async def test_create_embedding(self, service):
        """Test single embedding creation."""
        result = await service.create_embedding("test")
        assert result.is_success
        assert len(result.value) > 0
        assert isinstance(result.value[0], float)
    
    @pytest.mark.asyncio
    async def test_create_embeddings_batch(self, service):
        """Test batch embedding creation."""
        texts = ["hello", "world", "ai"]
        result = await service.create_embeddings_batch(texts)
        assert result.is_success
        assert len(result.value) == 3
        assert all(len(embedding) > 0 for embedding in result.value)
    
    @pytest.mark.asyncio
    async def test_get_model_info(self, service):
        """Test model info retrieval."""
        result = await service.get_model_info()
        assert result.is_success
        assert result.value["provider"] == "LM Studio"
        assert result.value["cost"] == "free"
    
    @pytest.mark.asyncio
    async def test_health_check(self, service):
        """Test health check."""
        result = await service.health_check()
        assert result.is_success
        assert result.value["status"] in ["healthy", "unhealthy"]

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

## 📊 Performance Examples

### **Performance Testing**
```python
# examples/performance_example.py
import asyncio
import time
from application.container import ContainerManager

async def test_performance():
    """Test service performance."""
    print("📊 Performance Testing")
    print("=" * 50)
    
    container_manager = ContainerManager()
    container = container_manager.container
    
    embedding_service = container.embedding_service().value
    
    # Test single embedding performance
    print("📝 Testing single embedding performance...")
    start_time = time.time()
    result = await embedding_service.create_embedding("Performance test")
    end_time = time.time()
    
    if result.is_success:
        response_time = (end_time - start_time) * 1000
        print(f"✅ Single embedding: {response_time:.2f}ms")
        print(f"📊 Embedding dimension: {len(result.value)}")
    else:
        print(f"❌ Single embedding failed: {result.error}")
    
    # Test batch embedding performance
    print("\n📝 Testing batch embedding performance...")
    texts = ["Performance test"] * 10  # 10 texts
    
    start_time = time.time()
    result = await embedding_service.create_embeddings_batch(texts)
    end_time = time.time()
    
    if result.is_success:
        response_time = (end_time - start_time) * 1000
        print(f"✅ Batch embedding (10 texts): {response_time:.2f}ms")
        print(f"📊 Average per text: {response_time/10:.2f}ms")
    else:
        print(f"❌ Batch embedding failed: {result.error}")
    
    # Test concurrent requests
    print("\n📝 Testing concurrent requests...")
    async def concurrent_embedding(text):
        return await embedding_service.create_embedding(text)
    
    texts = [f"Concurrent test {i}" for i in range(5)]
    
    start_time = time.time()
    results = await asyncio.gather(*[concurrent_embedding(text) for text in texts])
    end_time = time.time()
    
    successful_results = [r for r in results if r.is_success]
    response_time = (end_time - start_time) * 1000
    
    print(f"✅ Concurrent requests (5): {response_time:.2f}ms")
    print(f"📊 Successful: {len(successful_results)}/5")
    print(f"📊 Average per request: {response_time/5:.2f}ms")
    
    print("\n🎉 Performance testing completed!")

if __name__ == "__main__":
    asyncio.run(test_performance())
```

## 🚀 Running Examples

### **Run All Examples**
```bash
# Basic usage
python examples/basic_usage.py

# Embedding examples
python examples/embedding_examples.py

# Vector database examples
python examples/vector_db_examples.py

# Health monitoring examples
python examples/health_monitoring_examples.py

# Custom service example
python examples/custom_service_example.py

# ROP pattern examples
python examples/rop_pattern_examples.py

# Performance testing
python examples/performance_example.py
```

### **Run with Environment Variables**
```bash
# LM Studio provider
EMBEDDING_PROVIDER=lmstudio python examples/embedding_examples.py

# HuggingFace provider
EMBEDDING_PROVIDER=huggingface python examples/embedding_examples.py

# Local provider
EMBEDDING_PROVIDER=local python examples/embedding_examples.py
```

---

**These examples demonstrate the key features and capabilities of the AI Agent Starter Pack. Use them as a starting point for your own implementations.**
