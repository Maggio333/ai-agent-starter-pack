# Architectural Patterns - AI Agent Starter Pack

**Author**: Arkadiusz Słota  
**Project**: AI Agent Starter Pack  
**Year**: 2025

## 🎯 Overview

This document describes the key architectural patterns used in the AI Agent Starter Pack. These patterns provide a solid foundation for building scalable, maintainable, and extensible AI agents.

## 🏗️ Core Architectural Patterns

### **1. Clean Architecture**

Clean Architecture separates concerns into distinct layers, ensuring that business logic remains independent of external dependencies.

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                      │
│  FastAPI Endpoints  │  Flutter Voice UI  │  Google ADK Agent   │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                       │
│  DI Container      │  DTOs            │  Application Services   │
│  - Container       │  - Request/Resp  │  - Orchestration       │
│  - DIService       │  - Validation    │  - ChatAgentService    │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                          DOMAIN LAYER                           │
│  Entities          │  Interfaces (I*) │  Repositories          │
│  - ChatMessage     │  - ILLMService    │  - ChatRepository      │
│  - RAGChunk        │  - IVectorDbSvc   │  - VectorDbRepo        │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                      │
│  AI Services       │  Data Services    │  External Services    │
│  - Embeddings      │  - SQLite         │  - LM Studio          │
│  - Vector DB        │  - Cache          │  - Google APIs        │
│  - LLM Services     │  - Search         │  - OpenAI             │
│  - Voice (STT/TTS)  │  - Storage         │  - HuggingFace        │
└─────────────────────────────────────────────────────────────────┘
```

#### **Benefits**
- **Testability**: Easy to unit test business logic
- **Maintainability**: Clear separation of concerns
- **Flexibility**: Easy to swap implementations
- **Independence**: Business logic doesn't depend on external frameworks

#### **Implementation Example**
```python
# Domain Layer - Pure business logic
class ChatMessage:
    def __init__(self, content: str, sender: str):
        self.content = content
        self.sender = sender
        self.timestamp = datetime.now()

# Application Layer - Use cases
class ConversationService:
    def __init__(self, chat_repository: IChatRepository):
        self.chat_repository = chat_repository
    
    async def save_message(self, message: ChatMessage) -> Result[bool, str]:
        return await self.chat_repository.save(message)

# Infrastructure Layer - External dependencies
class SQLiteChatRepository(IChatRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def save(self, message: ChatMessage) -> Result[bool, str]:
        # SQLite implementation
        pass
```

### **2. Dependency Injection (DI)**

Dependency Injection manages object creation and dependencies, promoting loose coupling and testability.

#### **Container Pattern**
```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    # Configuration
    config = providers.Configuration()
    
    # Core services
    rop_service = providers.Singleton(ROPService)
    config_service = providers.Singleton(ConfigService)
    
    # AI services
    llm_service = providers.Singleton(_create_llm_service)
    embedding_service = providers.Singleton(_create_embedding_service)
    
    # Application services
    conversation_service = providers.Singleton(
        ConversationService, 
        chat_repository
    )
    
    # Voice services
    voice_service = providers.Singleton(VoiceService)
    
    # Agent services
    chat_agent_service = providers.Singleton(
        ChatAgentService,
        rop_service,
        chat_repository,
        llm_service,
        vector_db_service,
        orchestration_service,
        conversation_service
    )
```

#### **Service Facade Pattern**
```python
class DIService:
    """Facade over the DI container for simplified service access."""
    
    def __init__(self):
        self._container = Container()
        self._container.config.from_env()
        self._container.wire(modules=[__name__])
    
    def get_llm_service(self) -> ILLMService:
        """Get LLM service with lazy loading."""
        if not hasattr(self, '_llm_service'):
            self._llm_service = self._container.llm_service()
        return self._llm_service
    
    def get_voice_service(self) -> VoiceService:
        """Get voice service with lazy loading."""
        if not hasattr(self, '_voice_service'):
            self._voice_service = self._container.voice_service()
        return self._voice_service
```

#### **Benefits**
- **Loose Coupling**: Services don't create their dependencies
- **Testability**: Easy to mock dependencies
- **Configuration**: Centralized service configuration
- **Lazy Loading**: Services created only when needed

### **3. Railway Oriented Programming (ROP)**

ROP provides consistent error handling using Result types instead of exceptions.

#### **Result Pattern**
```python
from domain.common.result import Result

class Result(Generic[T, E]):
    def __init__(self, value: T = None, error: E = None):
        self._value = value
        self._error = error
    
    @property
    def is_success(self) -> bool:
        return self._error is None
    
    @property
    def is_failure(self) -> bool:
        return self._error is not None
    
    @property
    def value(self) -> T:
        if self.is_failure:
            raise ValueError("Cannot get value from failed result")
        return self._value
    
    @property
    def error(self) -> E:
        if self.is_success:
            raise ValueError("Cannot get error from successful result")
        return self._error
```

#### **Service Implementation**
```python
class VoiceService:
    async def transcribe_audio(self, audio_file: bytes) -> Result[str, str]:
        try:
            # Process audio
            text = await self._process_audio(audio_file)
            return Result(value=text)
        except Exception as e:
            logger.error(f"Speech transcription error: {e}")
            return Result(error=str(e))
    
    async def synthesize_speech(self, text: str) -> Result[str, str]:
        try:
            # Generate audio
            audio_file = await self._generate_audio(text)
            return Result(value=audio_file)
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
            return Result(error=str(e))
```

#### **Pipeline Operations**
```python
async def process_voice_message(audio_file: bytes) -> Result[str, str]:
    # Step 1: Transcribe audio
    transcribe_result = await voice_service.transcribe_audio(audio_file)
    if transcribe_result.is_failure:
        return transcribe_result
    
    # Step 2: Process text with AI
    text = transcribe_result.value
    ai_result = await llm_service.generate_response(text)
    if ai_result.is_failure:
        return ai_result
    
    # Step 3: Synthesize response
    response_text = ai_result.value
    synthesize_result = await voice_service.synthesize_speech(response_text)
    return synthesize_result
```

#### **Benefits**
- **Consistent Error Handling**: No unexpected exceptions
- **Composable Operations**: Easy to chain operations
- **Explicit Error States**: Clear success/failure states
- **Functional Style**: Immutable result objects

### **4. Multi-UI Architecture**

The system supports multiple user interfaces, each optimized for different use cases.

#### **Flutter Voice UI**
```dart
// Flutter implementation for voice-first applications
class VoiceChatPage extends StatefulWidget {
  @override
  _VoiceChatPageState createState() => _VoiceChatPageState();
}

class _VoiceChatPageState extends State<VoiceChatPage> {
  bool _isRecording = false;
  String _transcribedText = '';
  String _aiResponse = '';
  
  Future<void> _startRecording() async {
    // Start voice recording
    setState(() => _isRecording = true);
  }
  
  Future<void> _processVoice() async {
    // Send to backend for processing
    final response = await http.post(
      Uri.parse('http://localhost:8080/api/voice/transcribe'),
      body: audioData,
    );
    
    // Handle response
    setState(() => _transcribedText = response.body);
  }
}
```

#### **Google ADK Integration**
```yaml
# agents/root_agent.yaml
agent:
  name: "AI Assistant"
  description: "Intelligent voice assistant"
  
tools:
  - name: "weather_service"
    description: "Get weather information"
    parameters:
      city: string
      
  - name: "time_service"
    description: "Get current time"
    parameters:
      city: string
      
  - name: "city_service"
    description: "Get city information"
    parameters:
      city: string
```

#### **FastAPI Backend**
```python
# presentation/api/voice_endpoints.py
@router.post("/voice/transcribe")
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    voice_service: VoiceService = Depends(get_voice_service)
):
    audio_data = await audio_file.read()
    result = await voice_service.transcribe_audio(audio_data)
    
    if result.is_success:
        return {"text": result.value}
    else:
        raise HTTPException(status_code=500, detail=result.error)
```

#### **Benefits**
- **Flexibility**: Choose the best UI for your use case
- **Reusability**: Same backend serves multiple frontends
- **Scalability**: Each UI can be deployed independently
- **Future-proof**: Easy to add new UI types

### **5. Microservices Architecture**

The system is built using microservices, each handling a specific domain.

#### **Service Decomposition**
```python
# Weather Service
class WeatherService:
    async def get_weather(self, city: str) -> Result[WeatherData, str]:
        # Weather-specific logic
        pass

# Time Service  
class TimeService:
    async def get_current_time(self, city: str) -> Result[TimeData, str]:
        # Time-specific logic
        pass

# City Service
class CityService:
    async def get_city_info(self, city: str) -> Result[CityData, str]:
        # City-specific logic
        pass
```

#### **Agent Orchestration**
```python
class ChatAgentService:
    def __init__(self, weather_service: WeatherService, 
                 time_service: TimeService, 
                 city_service: CityService):
        self._services = {
            "weather": weather_service,
            "time": time_service,
            "city": city_service
        }
    
    async def process_request(self, request: str) -> Result[str, str]:
        # Determine which service to use
        service_name = self._determine_service(request)
        service = self._services.get(service_name)
        
        if service:
            return await service.process(request)
        else:
            return Result(error=f"Unknown service: {service_name}")
```

#### **Benefits**
- **Single Responsibility**: Each service has one job
- **Independent Deployment**: Deploy services separately
- **Technology Diversity**: Use different tech stacks per service
- **Scalability**: Scale services independently

### **6. Voice-First Design**

The system is designed with voice interaction as a first-class citizen.

#### **STT Integration**
```python
class VoiceService:
    def __init__(self):
        self.whisper_model = WhisperModel("base")
    
    async def transcribe_audio(self, audio_file: bytes) -> Result[str, str]:
        try:
            # Convert audio to text
            segments, info = self.whisper_model.transcribe(audio_file)
            text = " ".join([segment.text for segment in segments])
            return Result(value=text.strip())
        except Exception as e:
            return Result(error=str(e))
```

#### **TTS Integration**
```python
class VoiceService:
    def __init__(self):
        self.piper_model = PiperVoice.from_config("voice_model")
    
    async def synthesize_speech(self, text: str) -> Result[str, str]:
        try:
            # Convert text to speech
            audio_file = f"temp_audio_{uuid.uuid4()}.wav"
            self.piper_model.synthesize_wav(text, audio_file)
            return Result(value=audio_file)
        except Exception as e:
            return Result(error=str(e))
```

#### **Real-time Processing**
```python
# Flutter UI sends audio chunks
class VoiceRecorder {
  Stream<Uint8List> startRecording() {
    return _recorder.startStream(
      const RecordConfig(
        encoder: AudioEncoder.pcm16bits,
        sampleRate: 16000,
      ),
    );
  }
}

# Backend processes in real-time
@router.post("/voice/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    # Process audio immediately
    result = await voice_service.transcribe_audio(await audio_file.read())
    return {"text": result.value}
```

#### **Benefits**
- **Natural Interaction**: Voice is more natural than typing
- **Accessibility**: Better for users with disabilities
- **Hands-free**: Use while doing other tasks
- **Cross-platform**: Works on any device with microphone

## 🛠️ Implementation Guidelines

### **1. Service Creation**
```python
# 1. Define interface in domain layer
class IMyService(ABC):
    @abstractmethod
    async def process_data(self, data: str) -> Result[str, str]:
        pass

# 2. Implement in infrastructure layer
class MyService(IMyService):
    async def process_data(self, data: str) -> Result[str, str]:
        # Implementation
        pass

# 3. Register in container
my_service = providers.Singleton(MyService)

# 4. Use in application layer
class MyUseCase:
    def __init__(self, my_service: IMyService):
        self.my_service = my_service
```

### **2. Error Handling**
```python
# Always use Result pattern
async def my_service_method(self, input_data: str) -> Result[str, str]:
    try:
        # Process data
        result = await self._process(input_data)
        return Result(value=result)
    except ValidationError as e:
        return Result(error=f"Validation error: {e}")
    except ExternalServiceError as e:
        return Result(error=f"External service error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return Result(error="Internal server error")
```

### **3. Testing**
```python
# Mock dependencies for testing
class TestMyService:
    def test_process_data_success(self):
        # Arrange
        mock_service = Mock(spec=IMyService)
        mock_service.process_data.return_value = Result(value="success")
        
        # Act
        result = await mock_service.process_data("test")
        
        # Assert
        assert result.is_success
        assert result.value == "success"
```

## 🚀 Best Practices

### **1. Interface Segregation**
- Create small, focused interfaces
- Don't force classes to implement unused methods
- Use composition over inheritance

### **2. Dependency Inversion**
- Depend on abstractions, not concretions
- Use interfaces for all external dependencies
- Inject dependencies through constructor

### **3. Single Responsibility**
- Each class should have one reason to change
- Keep services focused on one domain
- Separate concerns into different layers

### **4. Open/Closed Principle**
- Open for extension, closed for modification
- Use interfaces to allow new implementations
- Add new features without changing existing code

## 📚 Further Reading

- **Clean Architecture**: Robert C. Martin
- **Dependency Injection**: Mark Seemann
- **Railway Oriented Programming**: Scott Wlaschin
- **Microservices Patterns**: Chris Richardson
- **Voice User Interface Design**: Cathy Pearl

---

**These patterns provide a solid foundation for building scalable, maintainable AI agents. Use them as guidelines, not rigid rules, and adapt them to your specific needs.**
