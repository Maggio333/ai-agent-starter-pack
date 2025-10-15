# API Documentation

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 🚀 Getting Started

### **Installation**
```bash
# Clone repository
git clone <repository-url>
cd python_agent

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration
```

### **Quick Start**
```python
from application.container import ContainerManager

# Initialize container
container_manager = ContainerManager()
container = container_manager.container

# Get services
embedding_service = container.embedding_service().value
vector_db_service = container.vector_db_service()
health_service = container.health_service()

# Use services
embedding_result = await embedding_service.create_embedding("Hello world")
search_result = await vector_db_service.search("Hello world", limit=5)
health_result = await health_service.check_health()
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Embedding Service
EMBEDDING_PROVIDER=lmstudio  # lmstudio, huggingface, google, openai, local
LMSTUDIO_PROXY_URL=http://127.0.0.1:8123
LMSTUDIO_MODEL_NAME=model:10

# Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=chat_collection

# Cache Service
CACHE_PROVIDER=memory  # memory, redis
REDIS_URL=redis://localhost:6379

# Search Service
SEARCH_PROVIDER=local  # local, elasticsearch, solr, algolia
```

## 🏗️ Core Services API

### **Embedding Service**

#### **BaseEmbeddingService**
```python
class BaseEmbeddingService(ABC):
    @abstractmethod
    async def create_embedding(self, text: str) -> Result[List[float], str]:
        """Create a single embedding for the given text."""
        pass
    
    @abstractmethod
    async def create_embeddings_batch(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Create embeddings for a list of texts."""
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Result[Dict[str, Any], str]:
        """Get information about the embedding model."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Perform a health check on the embedding service."""
        pass
```

#### **LM Studio Embedding Service**
```python
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService

# Initialize service
service = LMStudioEmbeddingService(
    proxy_url="http://127.0.0.1:8123",
    model_name="model:10"
)

# Create embedding
result = await service.create_embedding("Hello world")
if result.is_success:
    embedding = result.value  # List[float]
else:
    error = result.error  # str

# Batch embeddings
texts = ["Hello", "World", "AI"]
result = await service.create_embeddings_batch(texts)
if result.is_success:
    embeddings = result.value  # List[List[float]]
```

#### **HuggingFace Embedding Service**
```python
from infrastructure.ai.embeddings.huggingface_embedding_service import HuggingFaceEmbeddingService

# Initialize service
service = HuggingFaceEmbeddingService(
    api_token="your_token",
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Use same API as LM Studio
result = await service.create_embedding("Hello world")
```

### **Vector Database Service**

#### **QdrantService**
```python
from infrastructure.ai.vector_db.qdrant_service import QdrantService

# Initialize service
service = QdrantService(
    url="http://localhost:6333",
    collection_name="chat_collection",
    embedding_service=embedding_service
)

# Create collection
result = await service.create_collection()
if result.is_success:
    print("Collection created successfully")

# Upsert chunks
chunks = [
    RAGChunk(
        chunk_id="1",
        text_chunk="Hello world",
        metadata={"source": "test"},
        score=0.9
    )
]
result = await service.upsert_chunks(chunks)

# Search
result = await service.search("Hello world", limit=5)
if result.is_success:
    chunks = result.value  # List[RAGChunk]
    for chunk in chunks:
        print(f"Score: {chunk.score}, Text: {chunk.text_chunk}")
```

### **Health Service**

#### **HealthService**
```python
from infrastructure.monitoring.health import HealthService

# Initialize service
health_service = HealthService()

# Register services
health_service.register_service(embedding_health_service)
health_service.register_service(qdrant_health_service)

# Check overall health
result = await health_service.get_overall_health()
if result.is_success:
    health = result.value
    print(f"Status: {health['status']}")
    print(f"Message: {health['message']}")
    print(f"Response time: {health['response_time_ms']:.2f}ms")

# Get detailed health
result = await health_service.get_detailed_health()
if result.is_success:
    checks = result.value  # List[HealthCheck]
    for check in checks:
        print(f"Service: {check.service_name}")
        print(f"Status: {check.status}")
        print(f"Message: {check.message}")
```

## 🎯 Domain Entities

### **RAGChunk**
```python
from domain.entities.rag_chunk import RAGChunk

chunk = RAGChunk(
    chunk_id="unique_id",
    text_chunk="Your text content",
    metadata={"source": "document", "page": 1},
    score=0.95,
    chat_messages=None
)

# Access properties
print(chunk.chunk_id)      # str
print(chunk.text_chunk)    # str
print(chunk.metadata)      # Dict[str, Any]
print(chunk.score)         # float
```

### **ChatMessage**
```python
from domain.entities.chat_message import ChatMessage
from datetime import datetime

message = ChatMessage(
    content="Hello, how can I help you?",
    role="assistant",
    timestamp=datetime.now()
)

# Access properties
print(message.content)     # str
print(message.role)        # str
print(message.timestamp)   # datetime
```

### **QualityLevel**
```python
from domain.entities.quality_level import QualityLevel

# Enum values
QualityLevel.EXCELLENT    # "excellent"
QualityLevel.GOOD         # "good"
QualityLevel.FAIR         # "fair"
QualityLevel.POOR         # "poor"

# Usage
quality = QualityLevel.EXCELLENT
print(quality.value)  # "excellent"
```

## 🔄 Result Pattern (ROP)

### **Result Class**
```python
from domain.utils.result import Result

# Success result
result = Result.success("Hello world")
if result.is_success:
    value = result.value  # "Hello world"
    error = result.error  # None

# Error result
result = Result.error("Something went wrong")
if result.is_error:
    error = result.error  # "Something went wrong"
    value = result.value  # None
```

### **Pipeline Operations**
```python
from domain.services.rop_service import ROPService

# Create pipeline
pipeline = ROPService.pipeline(
    validate_input,
    process_data,
    save_result
)

# Execute pipeline
result = await pipeline("input_data")
if result.is_success:
    final_result = result.value
else:
    error = result.error
```

## 🏥 Health Monitoring

### **Health Check Implementation**
```python
from infrastructure.monitoring.health.base_health_service import BaseHealthService

class CustomHealthService(BaseHealthService):
    def __init__(self, service_name: str):
        super().__init__(service_name)
    
    async def check_health(self) -> Result[HealthCheck, str]:
        try:
            # Perform health check logic
            start_time = time.time()
            # ... your health check code ...
            response_time = (time.time() - start_time) * 1000
            
            return Result.success(HealthCheck(
                service_name=self.service_name,
                status=HealthStatus.HEALTHY,
                message="Service is healthy",
                response_time_ms=response_time,
                details={"custom": "data"}
            ))
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
```

### **Health Status Values**
```python
from infrastructure.monitoring.health.base_health_service import HealthStatus

HealthStatus.HEALTHY    # "healthy"
HealthStatus.UNHEALTHY  # "unhealthy"
HealthStatus.DEGRADED   # "degraded"
HealthStatus.UNKNOWN    # "unknown"
```

## 🧪 Testing Examples

### **Unit Test Example**
```python
import pytest
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService

@pytest.mark.asyncio
async def test_lmstudio_embedding():
    service = LMStudioEmbeddingService(
        proxy_url="http://127.0.0.1:8123",
        model_name="model:10"
    )
    
    result = await service.create_embedding("test")
    assert result.is_success
    assert len(result.value) > 0
    assert isinstance(result.value[0], float)
```

### **Integration Test Example**
```python
import pytest
from application.container import ContainerManager

@pytest.mark.asyncio
async def test_di_integration():
    container_manager = ContainerManager()
    container = container_manager.container
    
    # Test embedding service
    embedding_result = container.embedding_service()
    assert embedding_result.is_success
    
    # Test vector db service
    vector_db_service = container.vector_db_service()
    assert vector_db_service is not None
    
    # Test health service
    health_service = container.health_service()
    assert health_service is not None
```

## 🔍 Error Handling

### **Common Error Patterns**
```python
# Service unavailable
result = await service.operation()
if result.is_error:
    if "connection" in result.error.lower():
        # Handle connection error
        pass
    elif "timeout" in result.error.lower():
        # Handle timeout error
        pass
    else:
        # Handle other errors
        pass

# Validation errors
result = await validate_input(data)
if result.is_error:
    # Log validation error
    logger.error(f"Validation failed: {result.error}")
    return Result.error("Invalid input")
```

### **Error Recovery**
```python
# Retry pattern
max_retries = 3
for attempt in range(max_retries):
    result = await service.operation()
    if result.is_success:
        break
    elif attempt == max_retries - 1:
        return Result.error(f"Operation failed after {max_retries} attempts")
    else:
        await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## 📊 Performance Tips

### **Batch Operations**
```python
# Instead of individual calls
for text in texts:
    result = await embedding_service.create_embedding(text)

# Use batch operations
result = await embedding_service.create_embeddings_batch(texts)
```

### **Caching**
```python
# Check cache first
cached_result = await cache_service.get(key)
if cached_result.is_success:
    return cached_result.value

# Perform operation
result = await service.operation()
if result.is_success:
    # Cache the result
    await cache_service.set(key, result.value, ttl=3600)
```

### **Async Operations**
```python
# Concurrent operations
tasks = [
    service1.operation(),
    service2.operation(),
    service3.operation()
]
results = await asyncio.gather(*tasks)
```

## 🔒 Security Considerations

### **Input Validation**
```python
def validate_input(text: str) -> Result[str, str]:
    if not text or len(text.strip()) == 0:
        return Result.error("Text cannot be empty")
    
    if len(text) > 10000:
        return Result.error("Text too long")
    
    # Sanitize input
    sanitized = text.strip()
    return Result.success(sanitized)
```

### **API Key Management**
```python
# Use environment variables
api_key = os.getenv("API_KEY")
if not api_key:
    return Result.error("API key not configured")

# Don't log sensitive data
logger.info("API request made")  # Good
logger.info(f"API key: {api_key}")  # Bad
```

---

**For more examples and advanced usage, see the test files in the `tests/` directory.**
