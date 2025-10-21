# Architecture Documentation

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 📊 Layer Statistics

| Layer | Files | Services | Status |
|-------|-------|----------|--------|
| **Presentation** | 8+ | 3 | ✅ Complete (FastAPI + Flutter UI) |
| **Application** | 8 | 7 | ✅ Complete |
| **Domain** | 8 | 3 | ✅ Complete |
| **Infrastructure** | 35+ | 18+ | ✅ Complete |
| **Tests** | 20+ | - | ✅ Complete |

### **Total: 80+ files, 31+ services**

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Endpoints  │  Flutter Voice UI  │  Google ADK Agent   │
│  - Chat API         │  - Voice Recording │  - Tool Integration │
│  - Voice API        │  - STT/TTS         │  - Agent Orchestr. │
│  - Health API       │  - Real-time UI    │  - Microservices    │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  DI Container      │  DTOs            │  Application Services   │
│  - Container       │  - Request/Resp  │  - Orchestration       │
│  - DIService       │  - Validation    │  - ChatAgentService    │
│  - Service Registry│  - Error Handling│  - Business Logic      │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                          DOMAIN LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Entities          │  Interfaces (I*) │  Repositories          │
│  - ChatMessage     │  - ILLMService    │  - ChatRepository      │
│  - RAGChunk        │  - IVectorDbSvc   │  - VectorDbRepo        │
│  - QualityLevel    │  - ITextCleanerSvc│  - EmbeddingRepo       │
│  - Metadata        │  - IConfigService │  - CacheRepo           │
│                    │  - ICityService   │  - SearchRepo          │
│                    │  - IWeatherSvc   │  - HealthRepo           │
│                    │  - ITimeService   │                        │
│                    │  - IKnowledgeSvc  │                        │
│                    │  - IConversationSvc│                       │
│                    │  - IOrchestrationSvc│                      │
│                    │  - IDIService     │                        │
│                    │  - IEmailService  │                        │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│  AI Services       │  Data Services    │  External Services    │
│  - Embeddings      │  - SQLite         │  - LM Studio          │
│  - Vector DB        │  - Cache          │  - Google APIs        │
│  - LLM Services     │  - Search         │  - OpenAI             │
│  - Voice (STT/TTS)  │  - Storage         │  - HuggingFace        │
│  - Monitoring      │  - File System     │  - Qdrant             │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Key Architectural Patterns

### **1. Clean Architecture**
- **Domain Layer**: Core business logic, entities, and C#-style interfaces (I*)
- **Application Layer**: Use cases, orchestration, and DTOs
- **Infrastructure Layer**: External dependencies and implementations
- **Presentation Layer**: APIs, Flutter UI, and Google ADK integration

### **2. Multi-UI Architecture**
- **Flutter Voice UI**: Modern cross-platform voice interface
- **Google ADK Agent**: Enterprise-grade agent with tool integration
- **FastAPI Backend**: RESTful API for all frontend types
- **Future**: Custom tool system (replacing ADK dependency)

### **3. Dependency Injection**
- **Container**: Centralized service registration and resolution
- **Provider Choice**: Dynamic service selection based on configuration
- **Singleton Pattern**: Efficient resource management
- **Configuration**: Environment-based service configuration

### **4. Railway Oriented Programming (ROP)**
- **Result Pattern**: Consistent error handling across all services
- **Pipeline Operations**: Functional composition of operations
- **Error Propagation**: Clean error flow without exceptions
- **Validation**: Input validation and sanitization

### **5. Microservices Architecture**
- **Facade Pattern**: Unified interfaces for complex subsystems
- **Service Decomposition**: Specialized, focused services
- **Loose Coupling**: Independent service evolution
- **Scalability**: Horizontal scaling capabilities

### **6. Voice-First Design**
- **STT Integration**: Speech-to-Text with faster-whisper
- **TTS Integration**: Text-to-Speech with Piper
- **Real-time Processing**: WebSocket-like experience via HTTP
- **Cross-platform**: Flutter UI works on web, mobile, desktop

> **📚 Detailed patterns**: See [ARCHITECTURAL_PATTERNS.md](ARCHITECTURAL_PATTERNS.md) for comprehensive examples and implementation guidelines.

## 🚀 Agent Development Options

### **Option 1: Flutter Voice UI (Current)**
- **Best for**: Voice-first applications, mobile/web deployment
- **Features**: Real-time STT/TTS, modern UI, cross-platform
- **Tech Stack**: Flutter + FastAPI + LM Studio
- **Use Case**: Personal assistants, voice interfaces

### **Option 2: Google ADK Integration (Current)**
- **Best for**: Enterprise applications, complex tool integration
- **Features**: Advanced agent orchestration, microservice tools
- **Tech Stack**: Google ADK + FastAPI + LM Studio
- **Use Case**: Business automation, complex workflows

### **Option 3: Custom Tool System (Future)**
- **Best for**: Complete control, no external dependencies
- **Features**: Custom tool framework, full ownership
- **Tech Stack**: Custom implementation + FastAPI + LM Studio
- **Use Case**: Proprietary solutions, specialized domains

## 🛣️ Development Roadmap

### **Phase 1: Foundation (Current)**
- ✅ Clean Architecture implementation
- ✅ Dependency Injection container
- ✅ Railway Oriented Programming
- ✅ Voice services (STT/TTS)
- ✅ Flutter UI
- ✅ Google ADK integration

### **Phase 2: Enhancement (Next)**
- 🔄 Custom tool system development
- 🔄 Advanced agent orchestration
- 🔄 Multi-modal capabilities
- 🔄 Enhanced error handling

### **Phase 3: Scale (Future)**
- 📋 Distributed agent deployment
- 📋 Advanced monitoring
- 📋 Custom LLM integration
- 📋 Enterprise features

## 📦 Service Architecture

### **AI Services**
```
infrastructure/ai/
├── embeddings/
│   ├── base_embedding_service.py      # Abstract base class
│   ├── embedding_factory.py            # Factory pattern
│   ├── lmstudio_embedding_service.py  # LM Studio provider
│   ├── huggingface_embedding_service.py # HuggingFace provider
│   ├── google_embedding_service.py    # Google Vertex AI
│   ├── openai_embedding_service.py    # OpenAI provider
│   └── local_embedding_service.py     # Local Sentence Transformers
├── vector_db/
│   ├── qdrant_service.py              # Main Qdrant service
│   └── qdrant/                        # Microservices
│       ├── base_qdrant_service.py     # Base class
│       ├── collection_service.py      # Collection management
│       ├── embedding_service.py      # Embedding operations
│       ├── search_service.py          # Search operations
│       └── monitoring_service.py      # Health monitoring
└── llm/
    ├── google_vertex_service.py        # Main LLM service
    └── google_vertex/                  # Microservices
        ├── base_vertex_service.py     # Base class
        ├── tool_calling_service.py   # Function calling
        ├── model_management_service.py # Model operations
        └── configuration_service.py  # Configuration
```

### **Data Services**
```
infrastructure/data/
├── cache/
│   ├── base_cache_service.py          # Abstract base class
│   └── memory_cache_service.py        # Memory cache implementation
├── search/
│   ├── base_search_service.py         # Abstract base class
│   ├── search_factory.py              # Factory pattern
│   └── local_search_service.py         # Local search implementation
└── storage/
    ├── sqlite_chat_repository.py      # Main SQLite service
    └── sqlite/                        # Microservices
        ├── base_sqlite_service.py     # Base class
        ├── crud_service.py           # CRUD operations
        ├── bulk_operations_service.py # Bulk operations
        └── search_service.py         # Search operations
```

### **Monitoring Services**
```
infrastructure/monitoring/
├── health/
│   ├── base_health_service.py        # Abstract base class
│   ├── health_service.py             # Main health coordinator
│   ├── embedding_health_service.py   # Embedding health checks
│   └── qdrant_health_service.py      # Qdrant health checks
├── logging/
│   └── structured_logger.py          # Structured logging
└── metrics/                          # Prometheus metrics (planned)
```

## 🔧 Dependency Injection Container

### **Container Structure**
```python
class Container:
    # Configuration
    config_service = providers.Singleton(ConfigService)
    
    # AI Services
    embedding_service = providers.Singleton(EmbeddingFactory.create_service)
    vector_db_service = providers.Singleton(QdrantService)
    llm_service = providers.Singleton(GoogleVertexService)
    
    # Data Services
    cache_service = providers.Singleton(MemoryCacheService)
    search_service = providers.Singleton(SearchFactory.create_service)
    chat_repository = providers.Singleton(SqliteChatRepository)
    
    # Monitoring Services
    health_service = providers.Singleton(HealthService)
    logger = providers.Singleton(StructuredLogger)
```

### **Provider Choice System**
```python
# Environment-based provider selection
EMBEDDING_PROVIDER=lmstudio  # lmstudio, huggingface, google, openai, local
CACHE_PROVIDER=memory        # memory, redis
SEARCH_PROVIDER=local        # local, elasticsearch, solr, algolia
```

## 🚀 Service Lifecycle

### **1. Initialization**
1. **Container** loads configuration from environment
2. **Factory** creates services based on provider choice
3. **Services** initialize with configuration
4. **Health Service** registers all services

### **2. Runtime**
1. **Request** comes through presentation layer
2. **Application** orchestrates domain services
3. **Domain** executes business logic
4. **Infrastructure** handles external dependencies
5. **Response** flows back through layers

### **3. Monitoring**
1. **Health Service** continuously monitors all services
2. **Logger** records structured logs
3. **Metrics** collect performance data (planned)
4. **Alerts** notify of issues (planned)

## 🔍 Error Handling Strategy

### **Railway Oriented Programming**
```python
# Success case
result = await service.operation()
if result.is_success:
    data = result.value
    # Process data
else:
    error = result.error
    # Handle error

# Pipeline operations
result = await pipeline(
    validate_input,
    process_data,
    save_result
)
```

### **Error Types**
- **Validation Errors**: Input validation failures
- **Service Errors**: External service failures
- **Infrastructure Errors**: Database, network issues
- **Business Logic Errors**: Domain rule violations

## 📊 Performance Considerations

### **Singleton Pattern**
- **Memory Efficiency**: Single instance per service
- **Resource Sharing**: Shared connections and caches
- **Thread Safety**: Proper synchronization

### **Async/Await**
- **Non-blocking**: Concurrent operations
- **Scalability**: Handle multiple requests
- **Resource Efficiency**: Better resource utilization

### **Caching Strategy**
- **Memory Cache**: Fast access to frequently used data
- **Redis Cache**: Distributed caching (planned)
- **TTL Management**: Automatic expiration

## 🔒 Security Architecture

### **Authentication** (Planned)
- **JWT Tokens**: Stateless authentication
- **OAuth Integration**: Third-party authentication
- **Role-based Access**: Permission management

### **Encryption** (Planned)
- **Data Encryption**: Sensitive data protection
- **Transport Security**: HTTPS/TLS
- **Key Management**: Secure key storage

### **Validation** (Planned)
- **Input Sanitization**: Prevent injection attacks
- **Rate Limiting**: Prevent abuse
- **Audit Logging**: Security event tracking

## 🧪 Testing Strategy

### **Unit Tests**
- **Domain Logic**: Business rule validation
- **Service Logic**: Individual service testing
- **Error Handling**: ROP pattern testing

### **Integration Tests**
- **DI Container**: Service resolution testing
- **External Services**: API integration testing
- **Database Operations**: Data persistence testing

### **End-to-End Tests**
- **Complete Workflows**: Full user journey testing
- **Performance Testing**: Load and stress testing
- **Health Monitoring**: System health validation

## 📈 Scalability Considerations

### **Horizontal Scaling**
- **Stateless Services**: No shared state
- **Load Balancing**: Multiple service instances
- **Database Sharding**: Data distribution

### **Vertical Scaling**
- **Resource Optimization**: CPU and memory usage
- **Connection Pooling**: Database connections
- **Caching**: Reduce external calls

### **Microservices Benefits**
- **Independent Deployment**: Service-specific releases
- **Technology Diversity**: Different tech stacks
- **Fault Isolation**: Service-specific failures

## 🔄 Future Enhancements

### **Planned Features**
- **Metrics Service**: Prometheus integration
- **Security Services**: JWT, OAuth, encryption
- **External Services**: Google, Qdrant, APIs
- **Web UI**: React-based frontend
- **Docker Support**: Containerization
- **Kubernetes**: Orchestration

### **Architecture Evolution**
- **Event Sourcing**: Event-driven architecture
- **CQRS**: Command Query Responsibility Segregation
- **Saga Pattern**: Distributed transaction management
- **Circuit Breaker**: Fault tolerance patterns

---

**This architecture provides a solid foundation for building scalable, maintainable, and testable AI agent systems.**
