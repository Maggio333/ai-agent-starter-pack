## Update 2025-10-30

- Single SYSTEM prompt composed of sections: PERSONA, FORMAT, ROLE, optional USER PROFILE, and IDIOMS
- Conversation history filtered to ensure role alternation for LM Studio (…SYSTEM → USER → ASSISTANT…); trim trailing USER and drop leading ASSISTANT
- `create_app()` pattern with `uvicorn main_fastapi:app --reload` for dev autoreload
- Tests: global `conftest.py` (PYTHONPATH + async fallback), new `tests/test_prompt_service.py`

Diagram (high-level):

```
Presentation (Flutter, FastAPI Endpoints)
  └─ Chat/SSE → PromptService
Application
  ├─ PromptService (combine SYSTEM, filter history)
  ├─ DynamicRAGService (decide/search)
  ├─ ConversationService (sessions/history)
  └─ OrchestrationService
Infrastructure
  ├─ LMStudioLLMService (stream)
  ├─ Qdrant (Search/Embeddings)
  └─ SQLite ChatRepository (CRUD/Threads)
```

Last Updated: 2025-10-30  
Version: 1.1.0
# 🏗️ Architecture - Architektura Systemu

## 📋 Przegląd

System Eliora AI Assistant implementuje **Clean Architecture** z podziałem na warstwy, Dependency Injection i wzorce projektowe inspirowane przez `ChatElioraSystem`.

## 🎯 Zasady Architektury

### 1. **Clean Architecture**
- **Dependency Rule**: Zależności wskazują do wewnątrz
- **Separation of Concerns**: Każda warstwa ma określoną odpowiedzialność
- **Testability**: Łatwe testowanie dzięki DI i abstrakcjom

### 2. **Domain-Driven Design (DDD)**
- **Entities**: Podstawowe obiekty biznesowe
- **Services**: Logika biznesowa
- **Repositories**: Abstrakcje dostępu do danych

### 3. **SOLID Principles**
- **Single Responsibility**: Każda klasa ma jedną odpowiedzialność
- **Open/Closed**: Otwarte na rozszerzenia, zamknięte na modyfikacje
- **Dependency Inversion**: Zależność od abstrakcji, nie implementacji

## 🏛️ Struktura Warstw

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  Flutter UI (Voice + Chat)  │  FastAPI Endpoints           │
│  - Microphone recording     │  - /api/message               │
│  - Text input              │  - /api/message/stream         │
│  - Chat bubbles            │  - /api/chat/sessions          │
│  - Audio playback          │  - /api/vector/search         │
│  - Debug panel             │  - /api/knowledge/stats       │
│  - Color formatting        │  - /api/audio/synthesize      │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  PromptService              │  DynamicRAGService           │
│  - Builds message lists     │  - LLM-decided queries       │
│  - System prompts          │  - Context analysis          │
│  - Idiom consolidation      │  - Vector search             │
│  - Polish translations     │  - Threshold filtering       │
│                            │                               │
│  ChatAgentService          │  ConversationService          │
│  - High-level operations    │  - Session management         │
│  - Service coordination    │  - Message history           │
│  - Knowledge integration    │  - Context aggregation       │
│                            │                               │
│  OrchestrationService      │  UserSessionService            │
│  - Request routing          │  - User context              │
│  - Service coordination    │  - Session aggregation       │
│  - Error handling          │  - Permission flags           │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  Entities                   │  Services (Interfaces)       │
│  - ChatMessage              │  - IKnowledgeService          │
│  - Conversation             │  - ILLMService               │
│  - RAGResult                │  - IConversationService       │
│  - UserSession              │  - IOrchestrationService      │
│                            │                               │
│  Value Objects              │  Domain Services              │
│  - MessageRole              │  - ConversationAnalysisAgent │
│  - SessionStatus            │  - PromptTypeOrchestrator     │
│  - VectorScore              │  - ContextAggregator          │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  External Services          │  Data Access                  │
│  - LMStudioLLMService       │  - SqliteChatRepository       │
│  - QdrantVectorService      │  - VectorDbHelper             │
│  - GoogleTTSService         │  - FileSystemStorage          │
│  - WhisperSTTService        │  - CacheManager               │
│                            │                               │
│  Configuration              │  Monitoring                   │
│  - Settings                 │  - Logging                    │
│  - Environment Variables    │  - Metrics                    │
│  - Dependency Injection     │  - Health Checks              │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Dependency Injection Container

### Container Structure
```python
class Container:
    # Infrastructure
    llm_service = providers.Singleton(LMStudioLLMService)
    knowledge_service = providers.Singleton(KnowledgeService)
    conversation_service = providers.Singleton(ConversationService)
    
    # Application Services
    prompt_service = providers.Singleton(PromptService, knowledge_service=knowledge_service)
    dynamic_rag_service = providers.Singleton(DynamicRAGService, ...)
    chat_agent_service = providers.Singleton(ChatAgentService, ...)
    orchestration_service = providers.Singleton(OrchestrationService, ...)
```

### Dependency Flow
```
FastAPI Endpoints
    ↓ (depends on)
Container
    ↓ (injects)
Application Services
    ↓ (depends on)
Domain Services
    ↓ (depends on)
Infrastructure Services
```

## 🎭 Wzorce Projektowe

### 1. **Service Layer Pattern**
```python
class PromptService:
    def build_complete_message_list(self, idioms, conversation_history, user_message):
        # Centralized prompt building logic
```

### 2. **Repository Pattern**
```python
class IKnowledgeService(ABC):
    @abstractmethod
    async def search_knowledge_base(self, query: str, limit: int) -> List[Dict]:
        pass
```

### 3. **Factory Pattern**
```python
class LLMFactory:
    @staticmethod
    def create_llm_service() -> ILLMService:
        return LMStudioLLMService()
```

### 4. **Strategy Pattern**
```python
class OrchestrationService:
    async def process_request(self, request_type: str, **kwargs):
        if request_type == "conversation_start":
            return await self._handle_conversation_start(**kwargs)
        elif request_type == "message_processing":
            return await self._handle_message_processing(**kwargs)
```

## 🔄 Data Flow

### 1. **Message Processing Flow**
```
User Input (Flutter)
    ↓
FastAPI Endpoint (/api/message)
    ↓
Container.get_container()
    ↓
OrchestrationService.process_request()
    ↓
PromptService.build_complete_message_list()
    ↓
DynamicRAGService.search_with_filtering()
    ↓
LLMService.get_completion()
    ↓
Response to User
```

### 2. **RAG Processing Flow**
```
User Message
    ↓
ConversationAnalysisAgent.analyze_conversation()
    ↓
LLM generates vector query
    ↓
KnowledgeService.search_knowledge_base()
    ↓
Filter by threshold (≥0.85)
    ↓
PromptService consolidates idioms
    ↓
Send to LLM with context
```

### 3. **Streaming Flow**
```
User Message
    ↓
FastAPI SSE Endpoint (/api/message/stream)
    ↓
LLMService.stream_completion()
    ↓
Yield chunks to client
    ↓
Flutter processes chunks
    ↓
Sentence-by-sentence TTS
```

## 🗄️ Data Models

### Core Entities
```python
@dataclass
class ChatMessage:
    role: MessageRole
    content: str
    timestamp: datetime
    
@dataclass  
class RAGResult:
    typ: str
    temat: str
    payload: str
    score: float
    
@dataclass
class Conversation:
    session_id: str
    messages: List[ChatMessage]
    created_at: datetime
    status: SessionStatus
```

### Service Interfaces
```python
class IKnowledgeService(ABC):
    @abstractmethod
    async def search_knowledge_base(self, query: str, limit: int) -> List[Dict]:
        pass
        
class ILLMService(ABC):
    @abstractmethod
    async def get_completion(self, messages: List[ChatMessage]) -> str:
        pass
        
    @abstractmethod
    async def stream_completion(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        pass
```

## 🔌 External Integrations

### 1. **LM Studio**
- **Purpose**: Local LLM inference
- **Protocol**: HTTP REST API
- **Models**: Custom fine-tuned models
- **Features**: Completion, streaming, embeddings

### 2. **Qdrant Vector Database**
- **Purpose**: Semantic search, knowledge base
- **Protocol**: HTTP REST API
- **Collections**: Idioms, documents, embeddings
- **Features**: Similarity search, filtering, scoring

### 3. **Google Cloud TTS**
- **Purpose**: Text-to-Speech synthesis
- **Protocol**: HTTP REST API
- **Features**: Multiple voices, SSML support
- **Languages**: Polish, English

### 4. **Whisper (Local)**
- **Purpose**: Speech-to-Text transcription
- **Protocol**: Local API
- **Features**: Real-time transcription, multiple languages

## 🚀 Performance Considerations

### 1. **Caching Strategy**
- **Vector Search**: Cache frequent queries
- **LLM Responses**: Cache similar prompts
- **TTS Audio**: Cache generated audio files

### 2. **Async Processing**
- **Non-blocking I/O**: All external API calls
- **Concurrent Operations**: Parallel service calls
- **Streaming**: Real-time response delivery

### 3. **Resource Management**
- **Connection Pooling**: HTTP clients
- **Memory Management**: Large model handling
- **CPU Optimization**: Batch processing

## 🔒 Security Architecture

### 1. **Current State (Development)**
- No authentication
- No authorization
- Local services only

### 2. **Planned Security**
- **JWT Authentication**: User sessions
- **Role-based Access**: User permissions
- **API Rate Limiting**: Request throttling
- **Input Validation**: Pydantic models
- **HTTPS**: Encrypted communication

### 3. **Data Protection**
- **No PII Storage**: Minimal user data
- **Local Processing**: No cloud dependencies
- **Encrypted Storage**: Sensitive data encryption

## 🧪 Testing Architecture

### 1. **Test Structure**
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── functional/     # Functional tests
├── performance/    # Performance tests
└── debug tools/    # Debug utilities
```

### 2. **Testing Strategy**
- **Unit Tests**: Individual service testing
- **Integration Tests**: Service interaction testing
- **Functional Tests**: End-to-end workflow testing
- **Performance Tests**: Load and stress testing

### 3. **Test Data**
- **Mock Services**: External API mocking
- **Test Fixtures**: Sample data
- **Test Database**: Isolated test environment

## 📊 Monitoring & Observability

### 1. **Logging**
- **Structured Logging**: JSON format
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Context Information**: Request IDs, timestamps
- **Debug Tools**: Real-time log monitoring

### 2. **Metrics**
- **Performance Metrics**: Response times, throughput
- **Business Metrics**: Message counts, user sessions
- **Error Metrics**: Error rates, failure patterns

### 3. **Health Checks**
- **Service Health**: External service availability
- **Database Health**: Connection status
- **Resource Health**: Memory, CPU usage

## 🔮 Future Architecture

### 1. **Microservices Migration**
- **Service Decomposition**: Split into microservices
- **API Gateway**: Centralized routing
- **Service Mesh**: Inter-service communication
- **Container Orchestration**: Kubernetes deployment

### 2. **Scalability Improvements**
- **Horizontal Scaling**: Multiple service instances
- **Load Balancing**: Request distribution
- **Caching Layer**: Redis/Memcached
- **Database Sharding**: Data partitioning

### 3. **Advanced Features**
- **Event Sourcing**: Event-driven architecture
- **CQRS**: Command Query Responsibility Segregation
- **Saga Pattern**: Distributed transaction management
- **Circuit Breaker**: Fault tolerance

## 📚 Related Documentation

- **[Project Overview](PROJECT_OVERVIEW.md)** - Przegląd projektu
- **[API Endpoints](API_ENDPOINTS.md)** - Dokumentacja API
- **[Debug Tools](DEBUG_TOOLS.md)** - Narzędzia debugowe
- **[Flutter UI](FLUTTER_VOICE_UI.md)** - Dokumentacja frontend