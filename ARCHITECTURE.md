# Architecture Documentation

## 🏗️ **C#-Style Interface Architecture**

This project implements a **C#-style interface architecture** in Python, providing consistency and clarity across the entire codebase.

## 🎯 **Design Principles**

### **1. Interface Naming Convention**
All interfaces follow the C# naming convention with the `I` prefix:

```python
# ✅ Correct (C# style)
class ILLMService(ABC):
    @abstractmethod
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        pass

# ❌ Incorrect (Python style)
class LLMService(ABC):
    @abstractmethod
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        pass
```

### **2. Implementation Pattern**
All service implementations inherit from their respective interfaces:

```python
# ✅ Correct implementation
class GoogleVertexService(ILLMService):
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        # Implementation here
        pass

# ❌ Incorrect (no interface)
class GoogleVertexService:
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        # Implementation here
        pass
```

## 📋 **Complete Interface Inventory**

### **Core AI Services**
- `ILLMService` - Language Model operations
- `IVectorDbService` - Vector database operations
- `IEmbeddingService` - Text embedding operations

### **Application Services**
- `ICityService` - City information management
- `IWeatherService` - Weather data operations
- `ITimeService` - Time and timezone operations
- `IKnowledgeService` - Knowledge base management
- `IConversationService` - Chat conversation management
- `IOrchestrationService` - Service coordination

### **Infrastructure Services**
- `IDIService` - Dependency Injection service
- `IConfigService` - Configuration management
- `IEmailService` - Email operations
- `ITextCleanerService` - Text cleaning utilities
- `IHealthService` - Health monitoring

## 🔄 **Dependency Injection Architecture**

### **Container Pattern**
```python
class Container(containers.DeclarativeContainer):
    """Dependency Injection Container"""
    
    # Core Services
    config_service = providers.Singleton(ConfigService)
    llm_service = providers.Singleton(_create_llm_service)
    vector_db_service = providers.Singleton(QdrantService)
    
    # Application Services
    city_service = providers.Singleton(CityService)
    weather_service = providers.Singleton(WeatherService)
    time_service = providers.Singleton(TimeService)
    knowledge_service = providers.Singleton(KnowledgeService)
    conversation_service = providers.Singleton(ConversationService)
    orchestration_service = providers.Singleton(OrchestrationService)
```

### **Auto-Discovery Pattern**
```python
class DIService(IDIService):
    """Unified Dependency Injection Service"""
    
    def _auto_discover_services(self):
        """Automatically discovers all services from Container"""
        container_providers = [attr for attr in dir(self.container) 
                              if not attr.startswith('_') and 
                              hasattr(getattr(self.container, attr), '__call__')]
        
        for service_name in container_providers:
            method_name = f"get_{service_name}"
            if not hasattr(self, method_name):
                # Create getter method dynamically
                def create_getter(name):
                    def getter():
                        if not hasattr(self, f"_{name}") or getattr(self, f"_{name}") is None:
                            setattr(self, f"_{name}", getattr(self.container, name)())
                        return getattr(self, f"_{name}")
                    return getter
                
                setattr(self, method_name, create_getter(service_name))
```

## 🎨 **Layer Architecture**

### **Domain Layer (Interfaces)**
```
domain/services/
├── ILLMService.py
├── IVectorDbService.py
├── IEmbeddingService.py
├── IHealthService.py
├── ITextCleanerService.py
├── IEmailService.py
├── ICityService.py
├── IWeatherService.py
├── ITimeService.py
├── IKnowledgeService.py
├── IConversationService.py
├── IOrchestrationService.py
├── IDIService.py
└── IConfigService.py
```

### **Application Layer (Implementations)**
```
application/services/
├── city_service.py          # Implements ICityService
├── weather_service.py       # Implements IWeatherService
├── time_service.py          # Implements ITimeService
├── knowledge_service.py     # Implements IKnowledgeService
├── conversation_service.py  # Implements IConversationService
├── orchestration_service.py # Implements IOrchestrationService
└── di_service.py           # Implements IDIService
```

### **Infrastructure Layer (Implementations)**
```
infrastructure/
├── ai/
│   ├── llm/
│   │   ├── google_vertex_service.py    # Implements ILLMService
│   │   ├── simple_llm_service.py       # Implements ILLMService
│   │   └── lmstudio_llm_service.py     # Implements ILLMService
│   ├── vector_db/
│   │   └── qdrant_service.py           # Implements IVectorDbService
│   └── embeddings/
│       ├── google_embedding_service.py # Implements IEmbeddingService
│       ├── openai_embedding_service.py # Implements IEmbeddingService
│       └── lmstudio_embedding_service.py # Implements IEmbeddingService
├── services/
│   ├── email_service.py                # Implements IEmailService
│   └── text_cleaner_service.py         # Implements ITextCleanerService
├── config/
│   └── services/
│       └── config_service.py           # Implements IConfigService
└── monitoring/
    └── health/
        └── health_service.py           # Implements IHealthService
```

## 🔧 **Usage Patterns**

### **Service Retrieval**
```python
# ✅ Correct usage
di_service = DIService()
city_service = di_service.get_city_service()  # Returns ICityService
weather_service = di_service.get_weather_service()  # Returns IWeatherService

# ❌ Incorrect usage (direct container access)
container = Container()
city_service = container.city_service()  # Avoid this
```

### **Interface Implementation**
```python
# ✅ Correct implementation
class MyCustomService(ICityService):
    async def get_city_info(self, city_name: str) -> Result[Dict[str, Any], str]:
        # Implementation here
        pass
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        # Implementation here
        pass

# ❌ Incorrect (missing interface)
class MyCustomService:
    async def get_city_info(self, city_name: str) -> Result[Dict[str, Any], str]:
        # Implementation here
        pass
```

## 🎯 **Benefits of C#-Style Architecture**

### **1. Consistency**
- **Uniform naming** across all interfaces
- **Clear distinction** between interfaces and implementations
- **Predictable patterns** for developers

### **2. Maintainability**
- **Easy to identify** interfaces vs implementations
- **Simple refactoring** with clear dependencies
- **Better IDE support** with consistent naming

### **3. Scalability**
- **Easy to add new services** following the same pattern
- **Clear extension points** for new functionality
- **Consistent testing** patterns

### **4. Team Collaboration**
- **Reduced cognitive load** with consistent patterns
- **Easier code reviews** with clear interface contracts
- **Better documentation** with standardized naming

## 🚀 **Future Enhancements**

### **Planned Improvements**
- **Interface versioning** for backward compatibility
- **Interface composition** for complex service hierarchies
- **Interface mocking** for enhanced testing
- **Interface documentation** generation

### **Advanced Patterns**
- **Interface segregation** for focused contracts
- **Dependency inversion** with interface-based DI
- **Interface adapters** for external service integration
- **Interface decorators** for cross-cutting concerns
