# Architecture Documentation

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 📊 Layer Statistics

| Layer | Files | Services | Status |
|-------|-------|----------|--------|
| **Presentation** | 3 | 0 | 🟡 Empty (Ready for implementation) |
| **Application** | 8 | 7 | ✅ Complete |
| **Domain** | 8 | 3 | ✅ Complete |
| **Infrastructure** | 35 | 15+ | ✅ Complete |
| **Tests** | 20+ | - | ✅ Complete |

### **Total: 70+ files, 25+ services**

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
│  - Embeddings      │  - SQLite         │  - Google APIs        │
│  - Vector DB       │  - Cache          │  - Qdrant             │
│  - LLM             │  - Search         │  - OpenAI             │
│  - Monitoring      │  - Storage         │  - HuggingFace        │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Key Architectural Patterns

### **1. Clean Architecture**
- **Domain Layer**: Core business logic, entities, and C#-style interfaces (I*)
- **Application Layer**: Use cases, orchestration, and DTOs
- **Infrastructure Layer**: External dependencies and implementations
- **Presentation Layer**: APIs, CLI, and user interfaces

### **2. Dependency Injection**
- **Container**: Centralized service registration and resolution
- **Provider Choice**: Dynamic service selection based on configuration
- **Singleton Pattern**: Efficient resource management
- **Configuration**: Environment-based service configuration

### **3. Railway Oriented Programming (ROP)**
- **Result Pattern**: Consistent error handling across all services
- **Pipeline Operations**: Functional composition of operations
- **Error Propagation**: Clean error flow without exceptions
- **Validation**: Input validation and sanitization

### **4. Microservices Architecture**
- **Facade Pattern**: Unified interfaces for complex subsystems
- **Service Decomposition**: Specialized, focused services
- **Loose Coupling**: Independent service evolution
- **Scalability**: Horizontal scaling capabilities

### **5. C#-Style Interface Architecture**
- **Interface Naming**: All interfaces use `I` prefix (ICityService, IWeatherService, etc.)
- **Abstract Methods**: Clear separation of interface from implementation
- **Enterprise Patterns**: Professional patterns from C#/.NET ecosystem
- **Consistency**: Every service has its corresponding interface

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
