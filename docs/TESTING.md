# Testing Documentation

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 🧪 Testing Strategy

This project follows a comprehensive testing strategy with multiple levels of testing:

- **Unit Tests**: Individual service and component testing
- **Integration Tests**: Service interaction testing
- **End-to-End Tests**: Complete workflow testing
- **Performance Tests**: Load and stress testing

## 🏗️ Test Structure

```
tests/
├── services/                    # Service-specific tests
│   ├── test_all_services.py    # Comprehensive service testing
│   ├── test_city_service.py     # City service tests
│   ├── test_conversation_service.py # Conversation service tests
│   ├── test_knowledge_service.py    # Knowledge service tests
│   ├── test_orchestration_service.py # Orchestration service tests
│   ├── test_time_service.py     # Time service tests
│   └── test_weather_service.py # Weather service tests
├── test_chat_agent_improved.py # Chat agent tests
├── test_di_integration.py      # Dependency injection tests
├── test_embedding_comprehensive.py # Embedding service tests
├── test_health_service.py      # Health service tests
├── test_infrastructure.py     # Infrastructure tests
├── test_metadata_system.py    # Metadata system tests
├── test_property_based_metadata.py # Property-based metadata tests
├── test_qdrant_comprehensive.py # Qdrant service tests
├── test_quality_level_simple.py # Quality level tests
├── test_rop_agent_improved.py # ROP agent tests
├── test_rop.py                # ROP pattern tests
├── test_sqlite_microservices.py # SQLite microservices tests
├── check_collection.py        # Qdrant collection inspection
├── get_adaptive_trace.py      # Idiom pattern retrieval
├── search_mathematical_idioms.py # Mathematical idiom search
├── search_specific_terms.py   # Specific term search
└── universal_search.py        # Universal search testing
```

## 🚀 Running Tests

### **All Tests**
```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=.
```

### **Specific Test Categories**
```bash
# Service tests
python -m pytest tests/services/

# Integration tests
python -m pytest tests/test_di_integration.py

# Health service tests
python -m pytest tests/test_health_service.py

# Embedding service tests
python -m pytest tests/test_embedding_comprehensive.py
```

### **With Environment Variables**
```bash
# LM Studio provider
EMBEDDING_PROVIDER=lmstudio python tests/test_embedding_comprehensive.py

# HuggingFace provider
EMBEDDING_PROVIDER=huggingface python tests/test_embedding_comprehensive.py

# Local provider
EMBEDDING_PROVIDER=local python tests/test_embedding_comprehensive.py
```

## 🔧 Test Configuration

### **Environment Setup**
```bash
# Copy example environment
cp .env.example .env

# Edit environment variables
# EMBEDDING_PROVIDER=lmstudio
# LMSTUDIO_PROXY_URL=http://127.0.0.1:8123
# QDRANT_URL=http://localhost:6333
```

### **Test Dependencies**
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Install development dependencies
pip install -r requirements-dev.txt
```

## 📊 Test Examples

### **Unit Test Example**
```python
import pytest
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService

@pytest.mark.asyncio
async def test_lmstudio_embedding():
    """Test LM Studio embedding service."""
    service = LMStudioEmbeddingService(
        proxy_url="http://127.0.0.1:8123",
        model_name="model:10"
    )
    
    # Test single embedding
    result = await service.create_embedding("test")
    assert result.is_success
    assert len(result.value) > 0
    assert isinstance(result.value[0], float)
    
    # Test batch embeddings
    texts = ["hello", "world", "ai"]
    result = await service.create_embeddings_batch(texts)
    assert result.is_success
    assert len(result.value) == 3
    assert all(len(embedding) > 0 for embedding in result.value)
    
    # Test model info
    result = await service.get_model_info()
    assert result.is_success
    assert result.value["provider"] == "LM Studio"
    assert result.value["cost"] == "free"
```

### **Integration Test Example**
```python
import pytest
from application.container import ContainerManager

@pytest.mark.asyncio
async def test_di_integration():
    """Test dependency injection integration."""
    container_manager = ContainerManager()
    container = container_manager.container
    
    # Test embedding service
    embedding_result = container.embedding_service()
    assert embedding_result.is_success
    embedding_service = embedding_result.value
    
    # Test vector db service
    vector_db_service = container.vector_db_service()
    assert vector_db_service is not None
    
    # Test health service
    health_service = container.health_service()
    assert health_service is not None
    
    # Test service interaction
    result = await embedding_service.create_embedding("test")
    assert result.is_success
    assert len(result.value) > 0
```

### **Health Service Test Example**
```python
import pytest
from infrastructure.monitoring.health import HealthService
from infrastructure.monitoring.health.embedding_health_service import EmbeddingHealthService
from infrastructure.monitoring.health.qdrant_health_service import QdrantHealthService

@pytest.mark.asyncio
async def test_health_service():
    """Test health service functionality."""
    # Initialize services
    health_service = HealthService()
    embedding_service = LMStudioEmbeddingService()
    vector_db_service = QdrantService()
    
    # Register health services
    embedding_health = EmbeddingHealthService(embedding_service)
    qdrant_health = QdrantHealthService(vector_db_service)
    
    health_service.register_service(embedding_health)
    health_service.register_service(qdrant_health)
    
    # Test overall health
    result = await health_service.get_overall_health()
    assert result.is_success
    assert result.value["status"] in ["healthy", "unhealthy", "degraded"]
    assert "services_checked" in result.value
    
    # Test detailed health
    result = await health_service.get_detailed_health()
    assert result.is_success
    assert len(result.value) >= 2  # At least 2 services registered
```

## 🔍 Test Categories

### **1. Service Tests**
Test individual services in isolation:

```python
# Embedding service tests
python tests/test_embedding_comprehensive.py

# Vector database tests
python tests/test_qdrant_comprehensive.py

# Health service tests
python tests/test_health_service.py
```

### **2. Integration Tests**
Test service interactions:

```python
# DI container integration
python tests/test_di_integration.py

# SQLite microservices
python tests/test_sqlite_microservices.py

# ROP pattern integration
python tests/test_rop.py
```

### **3. End-to-End Tests**
Test complete workflows:

```python
# Chat agent workflow
python tests/test_chat_agent_improved.py

# ROP agent workflow
python tests/test_rop_agent_improved.py

# Universal search workflow
python tests/universal_search.py
```

### **4. Performance Tests**
Test system performance:

```python
# Comprehensive service testing
python tests/services/test_all_services.py

# Infrastructure performance
python tests/test_infrastructure.py
```

## 🏥 Health Check Tests

### **Individual Service Health**
```python
@pytest.mark.asyncio
async def test_embedding_health():
    """Test embedding service health check."""
    service = LMStudioEmbeddingService()
    health_service = EmbeddingHealthService(service)
    
    result = await health_service.check_health()
    assert result.is_success
    
    health_check = result.value
    assert health_check.service_name == "EmbeddingService"
    assert health_check.status in ["healthy", "unhealthy"]
    assert health_check.response_time_ms is not None
```

### **System Health**
```python
@pytest.mark.asyncio
async def test_system_health():
    """Test overall system health."""
    health_service = HealthService()
    
    # Register all services
    health_service.register_service(embedding_health)
    health_service.register_service(qdrant_health)
    
    # Test overall health
    result = await health_service.get_overall_health()
    assert result.is_success
    
    overall_health = result.value
    assert overall_health["status"] in ["healthy", "unhealthy", "degraded"]
    assert overall_health["services_checked"] >= 2
    assert overall_health["response_time_ms"] > 0
```

## 🔄 ROP Pattern Tests

### **Result Pattern Tests**
```python
@pytest.mark.asyncio
async def test_result_pattern():
    """Test Result pattern functionality."""
    # Success result
    result = Result.success("test")
    assert result.is_success
    assert result.value == "test"
    assert result.error is None
    
    # Error result
    result = Result.error("error")
    assert result.is_error
    assert result.error == "error"
    assert result.value is None
```

### **Pipeline Tests**
```python
@pytest.mark.asyncio
async def test_pipeline():
    """Test ROP pipeline functionality."""
    async def step1(data):
        return Result.success(data.upper())
    
    async def step2(data):
        return Result.success(f"Processed: {data}")
    
    pipeline = ROPService.pipeline(step1, step2)
    result = await pipeline("hello")
    
    assert result.is_success
    assert result.value == "Processed: HELLO"
```

## 📊 Test Data

### **Test Collections**
```python
# Qdrant test collection
COLLECTION_NAME = "test_collection"

# Test chunks
test_chunks = [
    RAGChunk(
        chunk_id="1",
        text_chunk="Hello world",
        metadata={"source": "test"},
        score=0.9
    ),
    RAGChunk(
        chunk_id="2",
        text_chunk="AI is amazing",
        metadata={"source": "test"},
        score=0.8
    )
]
```

### **Mock Data**
```python
# Mock embedding response
mock_embedding = [0.1] * 1024

# Mock health check response
mock_health = {
    "status": "healthy",
    "message": "Service is healthy",
    "response_time_ms": 50.0
}
```

## 🚨 Error Testing

### **Service Errors**
```python
@pytest.mark.asyncio
async def test_service_errors():
    """Test service error handling."""
    # Test with invalid URL
    service = LMStudioEmbeddingService(proxy_url="http://invalid:9999")
    
    result = await service.create_embedding("test")
    assert result.is_error
    assert "connection" in result.error.lower()
```

### **Validation Errors**
```python
@pytest.mark.asyncio
async def test_validation_errors():
    """Test input validation."""
    service = LMStudioEmbeddingService()
    
    # Test empty text
    result = await service.create_embedding("")
    assert result.is_error
    
    # Test None input
    result = await service.create_embedding(None)
    assert result.is_error
```

## 📈 Performance Testing

### **Response Time Tests**
```python
@pytest.mark.asyncio
async def test_response_times():
    """Test service response times."""
    service = LMStudioEmbeddingService()
    
    start_time = time.time()
    result = await service.create_embedding("test")
    response_time = (time.time() - start_time) * 1000
    
    assert result.is_success
    assert response_time < 5000  # Less than 5 seconds
```

### **Batch Performance**
```python
@pytest.mark.asyncio
async def test_batch_performance():
    """Test batch operation performance."""
    service = LMStudioEmbeddingService()
    
    texts = ["test"] * 100  # 100 texts
    
    start_time = time.time()
    result = await service.create_embeddings_batch(texts)
    response_time = (time.time() - start_time) * 1000
    
    assert result.is_success
    assert len(result.value) == 100
    assert response_time < 10000  # Less than 10 seconds
```

## 🔧 Test Utilities

### **Test Helpers**
```python
def create_test_chunk(chunk_id: str, text: str) -> RAGChunk:
    """Create a test RAG chunk."""
    return RAGChunk(
        chunk_id=chunk_id,
        text_chunk=text,
        metadata={"source": "test"},
        score=0.9
    )

def create_test_message(content: str, role: str) -> ChatMessage:
    """Create a test chat message."""
    return ChatMessage(
        content=content,
        role=role,
        timestamp=datetime.now()
    )
```

### **Async Test Helpers**
```python
async def wait_for_service(service, timeout: int = 30):
    """Wait for service to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = await service.health_check()
        if result.is_success and result.value["status"] == "healthy":
            return True
        await asyncio.sleep(1)
    return False
```

## 📋 Test Checklist

### **Before Running Tests**
- [ ] Environment variables configured
- [ ] External services running (LM Studio, Qdrant)
- [ ] Dependencies installed
- [ ] Test data prepared

### **Test Coverage**
- [ ] Unit tests for all services
- [ ] Integration tests for DI container
- [ ] Health check tests
- [ ] Error handling tests
- [ ] Performance tests

### **After Tests**
- [ ] Clean up test data
- [ ] Check test coverage
- [ ] Review failed tests
- [ ] Update documentation

---

**For more test examples and patterns, see the individual test files in the `tests/` directory.**
