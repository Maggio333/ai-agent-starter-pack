# AI Agent Starter Pack - Python

A comprehensive, production-ready AI agent framework built with Clean Architecture, Dependency Injection, and Railway Oriented Programming patterns.

**Author**: Arkadiusz Słota  
**License**: MIT with Attribution Requirement  
**Year**: 2025

## 🆕 **Latest Updates (v2.0)**

### ✅ **C#-Style Interface Architecture**
- **All services now use C#-style interfaces with `I` prefix**
- **Full interface consistency across the entire codebase**
- **Enhanced Dependency Injection with auto-discovery**
- **Unicode support and extended character limits (2000 chars)**

### 🎯 **Interface Naming Convention**
```python
# Before (Python style)
class LLMService(ABC):
    pass

# After (C# style) 
class ILLMService(ABC):
    pass
```

### 📋 **Complete Interface List**
- `ILLMService` - Language Model operations
- `IVectorDbService` - Vector database operations  
- `IEmbeddingService` - Text embedding operations
- `IHealthService` - Health monitoring
- `ITextCleanerService` - Text cleaning utilities
- `IEmailService` - Email operations
- `ICityService` - City information
- `IWeatherService` - Weather data
- `ITimeService` - Time operations
- `IKnowledgeService` - Knowledge base
- `IConversationService` - Chat management
- `IOrchestrationService` - Service coordination
- `IDIService` - Dependency Injection
- `IConfigService` - Configuration management

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│  API (FastAPI)     │  CLI Interface    │  Web UI (Future)     │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  DI Container      │  DTOs            │  Application Services   │
│  - Container       │  - Request/Resp  │  - Orchestration       │
│  - DIService       │  - Validation    │  - Business Logic      │
│  - Auto-Discovery  │  - Mapping       │  - Use Cases          │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                          DOMAIN LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Entities          │  Interfaces (I*) │  Repositories          │
│  - ChatMessage     │  - ILLMService    │  - ChatRepository      │
│  - RAGChunk        │  - IVectorDbSvc   │  - VectorDbRepo        │
│  - QualityLevel    │  - IEmbeddingSvc  │  - EmbeddingRepo       │
│  - Metadata        │  - IHealthService │  - CacheRepo           │
│  - Result<T,E>     │  - I*Service      │  - SearchRepo          │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│  AI Services       │  Data Services    │  External Services    │
│  - Embeddings      │  - SQLite         │  - Google APIs        │
│  - Vector DB       │  - Cache          │  - Qdrant             │
│  - LLM             │  - Search         │  - OpenAI             │
│  - Monitoring      │  - Storage         │  - HuggingFace        │
│  - Text Cleaning   │  - Email          │  - LM Studio          │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Key Features

### ✅ **Clean Architecture**
- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and orchestration
- **Infrastructure Layer**: External dependencies and implementations
- **Presentation Layer**: APIs and user interfaces

### ✅ **Dependency Injection**
- **Container**: Centralized service registration
- **Provider Choice**: Dynamic service selection based on configuration
- **Singleton Pattern**: Efficient resource management
- **Configuration**: Environment-based service configuration

### ✅ **Railway Oriented Programming**
- **Result Pattern**: Consistent error handling
- **Pipeline Operations**: Functional composition
- **Error Propagation**: Clean error flow
- **Validation**: Input validation and sanitization

### ✅ **Microservices Architecture**
- **Facade Pattern**: Unified interfaces for complex subsystems
- **Service Decomposition**: Specialized, focused services
- **Loose Coupling**: Independent service evolution
- **Scalability**: Horizontal scaling capabilities

## 🚀 Core Services

### **AI Services**
- **EmbeddingService**: Multiple providers (LM Studio, HuggingFace, Google, OpenAI)
- **VectorDbService**: Qdrant integration with semantic search
- **LLMService**: Google Vertex AI integration
- **SearchService**: Elasticsearch, Solr, local search options

### **Data Services**
- **CacheService**: Memory and Redis caching
- **StorageService**: SQLite with microservices architecture
- **ConfigService**: Environment-based configuration management

### **Monitoring Services**
- **HealthService**: Comprehensive health checks for all services
- **StructuredLogger**: Advanced logging with context
- **MetricsService**: Prometheus metrics (planned)

### **Security Services**
- **AuthService**: JWT and OAuth integration (planned)
- **EncryptionService**: Data encryption and security (planned)
- **ValidationService**: Input validation and sanitization (planned)

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd python_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration
```

## ⚙️ Configuration

### **Environment Variables**
```bash
# Embedding Service
EMBEDDING_PROVIDER=lmstudio  # lmstudio, huggingface, google, openai, local
LMSTUDIO_PROXY_URL=http://127.0.0.1:8123
LMSTUDIO_MODEL_NAME=model:10

# Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=chat_collection

# Google Services
GOOGLE_API_KEY=your_api_key
GOOGLE_PROJECT_ID=your_project_id
GOOGLE_LOCATION=us-central1

# Cache Service
CACHE_PROVIDER=memory  # memory, redis
REDIS_URL=redis://localhost:6379

# Search Service
SEARCH_PROVIDER=local  # local, elasticsearch, solr, algolia
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python tests/test_health_service.py
python tests/test_di_integration.py
python tests/test_qdrant_comprehensive.py

# Run with specific environment
EMBEDDING_PROVIDER=lmstudio python tests/test_embedding_comprehensive.py
```

## 📊 Health Monitoring

```python
from application.container import ContainerManager

# Initialize container
container_manager = ContainerManager()
container = container_manager.container

# Get health service
health_service = container.health_service()

# Register services
health_service.register_embedding_service(embedding_service)
health_service.register_qdrant_service(qdrant_service)

# Check overall health
result = await health_service.check_health()
if result.is_success:
    health = result.value
    print(f"Status: {health.status.value}")
    print(f"Message: {health.message}")
    print(f"Response time: {health.response_time_ms:.2f}ms")
```

## 🔍 Usage Examples

### **Basic Agent Usage**
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

### **Custom Service Registration**
```python
from infrastructure.ai.embeddings.lmstudio_embedding_service import LMStudioEmbeddingService

# Create custom service
custom_embedding = LMStudioEmbeddingService(
    proxy_url="http://localhost:8123",
    model_name="model:10"
)

# Register with health service
health_service.register_embedding_service(custom_embedding)
```

## 🏗️ Project Structure

```
python_agent/
├── agents/                 # Agent implementations
│   └── ChatAgent.py       # Main chat agent
├── application/           # Application layer
│   ├── container.py      # DI Container (17 services)
│   ├── dto/             # Data Transfer Objects (empty)
│   └── services/        # Application services (Use Cases)
│       ├── city_service.py           # City information service
│       ├── conversation_service.py   # Conversation management
│       ├── di_service.py             # DI utility service
│       ├── knowledge_service.py      # Knowledge base service
│       ├── orchestration_service.py  # Service orchestrator
│       ├── time_service.py           # Time operations service
│       └── weather_service.py        # Weather information service
├── domain/              # Domain layer
│   ├── entities/        # Core entities
│   │   ├── chat_message.py      # Chat message entity
│   │   ├── quality_level.py     # Quality level enum
│   │   └── rag_chunk.py         # RAG chunk entity
│   ├── models/          # Domain models
│   │   ├── metadata_fields.py   # Metadata field definitions
│   │   └── metadata.py          # Metadata models
│   ├── repositories/    # Repository interfaces
│   │   └── chat_repository.py   # Chat repository interface
│   ├── services/        # Domain services
│   │   ├── llm_service.py       # LLM service interface
│   │   ├── rop_service.py       # Railway Oriented Programming
│   │   └── vector_db_service.py # Vector DB service interface
│   └── utils/           # Domain utilities
│       └── result.py            # Result pattern implementation
├── infrastructure/      # Infrastructure layer
│   ├── ai/             # AI services
│   │   ├── embeddings/         # Embedding services (5 providers)
│   │   ├── llm/               # LLM services (Google Vertex AI)
│   │   └── vector_db/         # Vector database services (Qdrant)
│   ├── config/         # Configuration services
│   │   ├── environment/       # Environment configuration
│   │   ├── services/          # Configuration service
│   │   └── validation/        # Validation (empty)
│   ├── data/           # Data services
│   │   ├── cache/             # Cache services (2 providers)
│   │   ├── search/            # Search services (4 providers)
│   │   └── storage/           # Storage services (SQLite)
│   └── monitoring/     # Monitoring services
│       ├── health/            # Health monitoring
│       └── logging/          # Structured logging
├── presentation/       # Presentation layer (empty - ready for implementation)
│   ├── api/           # API endpoints (empty)
│   └── cli/           # CLI interface (empty)
├── tests/            # Test suite (25+ test files)
├── docs/             # Documentation
├── examples/         # Usage examples
├── main.py          # Application entry point
├── requirements.txt # Dependencies
└── README.md        # This file
```

## 🔧 Development

### **Adding New Services**
1. Create service in appropriate infrastructure directory
2. Implement base interface/abstract class
3. Register in DI Container
4. Add health check implementation
5. Write comprehensive tests

### **Adding New Providers**
1. Implement provider interface
2. Add to factory pattern
3. Update configuration service
4. Add environment variables
5. Update documentation

## 📈 Performance

- **Embedding Service**: ~87ms response time (LM Studio)
- **Vector Search**: ~42ms response time (Qdrant)
- **Health Checks**: ~84ms overall system check
- **Memory Usage**: Optimized with singleton pattern
- **Scalability**: Horizontal scaling ready

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the **MIT License with Attribution Requirement** - see the [LICENSE](LICENSE) file for details.

### **Commercial Use Requirements**
When using this Software in any commercial or public project, you **MUST** include a clear attribution to the original author:
- "Based on AI Agent Starter Pack by Arkadiusz Słota" 
- Or similar acknowledgment in documentation, about pages, and public acknowledgments

### **Attribution Examples**
```markdown
## Acknowledgments
- Based on AI Agent Starter Pack by Arkadiusz Słota
- Framework: AI Agent Starter Pack (https://github.com/Maggio333/ai-agent-starter-pack)
- Author: Arkadiusz Słota
```

**For commercial licensing or custom agreements, please contact the author.**

## 🙏 Acknowledgments

- **Clean Architecture** principles by Robert C. Martin
- **Railway Oriented Programming** patterns
- **Dependency Injection** best practices
- **Microservices** architecture patterns

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the test examples

---

**Built with ❤️ for the AI community**