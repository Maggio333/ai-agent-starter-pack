# CHANGELOG

All notable changes to the AI Agent Starter Pack project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-18

### 🎯 **Major Refactoring: C#-Style Interface Architecture**

#### ✅ **Added**
- **Complete C#-style interface architecture** with `I` prefix for all services
- **14 new interfaces** following C# naming conventions:
  - `ICityService` - City information management
  - `IWeatherService` - Weather data operations
  - `ITimeService` - Time and timezone operations
  - `IKnowledgeService` - Knowledge base management
  - `IConversationService` - Chat conversation management
  - `IOrchestrationService` - Service coordination
  - `IDIService` - Dependency Injection service
  - `IConfigService` - Configuration management
  - `IEmailService` - Email operations
  - `ITextCleanerService` - Text cleaning utilities
  - `IHealthService` - Health monitoring
  - `IEmbeddingService` - Text embedding operations
  - `IVectorDbService` - Vector database operations
  - `ILLMService` - Language Model operations

#### 🔄 **Changed**
- **All service implementations** now inherit from their respective interfaces
- **Dependency Injection** enhanced with auto-discovery mechanism
- **Character limit** increased from 500 to 2000 characters for knowledge base queries
- **Unicode support** improved with comprehensive text cleaning
- **Architecture consistency** across all layers

#### 🐛 **Fixed**
- **Unicode encoding issues** (`charmap` codec errors) resolved
- **Text cleaning** for problematic characters (emojis, mathematical symbols)
- **Interface inheritance** properly implemented across all services
- **Health check methods** added to all services

#### 🗑️ **Removed**
- **Old Python-style** interface naming (without `I` prefix)
- **ContainerManager** class (replaced with unified DIService)
- **Direct container access** patterns

#### 🔧 **Technical Details**
- **Interface Pattern**: All interfaces inherit from `ABC` with `@abstractmethod`
- **Implementation Pattern**: All services inherit from their respective `I*` interfaces
- **DI Pattern**: Unified `DIService` with auto-discovery of all container providers
- **Error Handling**: Consistent `Result<T, E>` pattern across all services

#### 📚 **Documentation**
- **README.md** updated with new architecture overview
- **Interface documentation** added for all services
- **Architecture diagrams** updated to reflect C#-style interfaces

---

## [1.0.0] - 2025-01-15

### 🎉 **Initial Release**

#### ✅ **Added**
- **Clean Architecture** implementation
- **Dependency Injection** with `dependency_injector`
- **Railway Oriented Programming** patterns
- **FastAPI** web interface
- **SQLite** database integration
- **Vector database** support (Qdrant)
- **Multiple LLM providers** (Google, OpenAI, LM Studio)
- **Embedding services** (HuggingFace, Google, OpenAI, Local)
- **Comprehensive testing** suite
- **Health monitoring** system
- **Configuration management**

#### 🏗️ **Architecture**
- **Domain Layer**: Entities, services, repositories
- **Application Layer**: Use cases, DTOs, orchestration
- **Infrastructure Layer**: External services, data access
- **Presentation Layer**: API endpoints, CLI interface

#### 🔧 **Services**
- **CityService**: City information and data
- **WeatherService**: Weather data operations
- **TimeService**: Time and timezone operations
- **KnowledgeService**: Knowledge base with RAG
- **ConversationService**: Chat management
- **OrchestrationService**: Service coordination

#### 📦 **Dependencies**
- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM
- **Qdrant**: Vector database
- **Pydantic**: Data validation
- **Pytest**: Testing framework
- **Dependency Injector**: DI container

---

## [2.1.0] - 2025-01-18

### ✅ **Added**
- **SystemPromptsService** - Centralized service for all hardcoded RAG strings and system prompts
- **JSONEmbeddingService** - Service to parse LLM JSON responses and generate embeddings for specific fields
- **Dynamic RAG** - Intelligent context analysis that generates vector queries based on conversation
- **Audio cleanup** - Automatic deletion of all audio files when creating new ones (prevents disk space issues)
- **Enhanced logging** - Detailed logging for RAG context being added to LLM
- **RAG context preview** - Full logging of what content from vector database is being added to LLM context

### 🔄 **Changed**
- **Refactored PromptService** to use SystemPromptsService for all hardcoded strings
- **Reduced score_threshold** from 0.85 to 0.75 for better result quantity in vector search
- **Fixed RAGResult.from_vector_result** to properly extract content from 'facts' list
- **Idioms prompt** updated from descriptive to action-oriented (AI uses idioms directly instead of mentioning them)

### 🐛 **Fixed**
- **RAG content extraction** - Fixed issue where RAGResult.from_vector_result was not extracting content from 'facts' field
- **Audio cleanup** - All audio files are now deleted before creating new ones to prevent disk space issues
- **Unicode errors** in logging - Changed query strings to use safe ASCII characters for logging
- **RAG context logging** - Added detailed logging showing exactly what content is being added to LLM context

### 📚 **Documentation**
- **SYSTEM_PROMPTS_SERVICE.md** - Documentation for centralized system prompts service
- **JSON_EMBEDDING_SERVICE.md** - Documentation for JSON parsing and embedding service
- **Updated CHANGELOG.md** with latest changes

### 🔧 **Technical Details**
- **SystemPromptsService**: Centralizes all hardcoded RAG strings in `domain/services/SystemPromptsService.py`
- **JSONEmbeddingService**: Parses LLM JSON responses and generates embeddings in `application/services/json_embedding_service.py`
- **DynamicRAGService**: Enhanced with JSONEmbeddingService for intelligent query generation
- **VoiceService**: Automatic cleanup of all audio files before creating new ones

---

## [Unreleased]

### 🔮 **Planned Features**
- **Fix conversation saving** - 'coroutine' object has no attribute 'bind' error
- **Hot reload** for development
- **Web UI** interface
- **Docker** containerization
- **Kubernetes** deployment
- **Monitoring** dashboard
- **Performance** optimization
- **Security** enhancements