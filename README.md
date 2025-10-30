# 🎯 Voice AI Assistant

Zaawansowany system chatbot z architekturą Clean Architecture, integrujący Flutter frontend, FastAPI backend, bazę wektorową i inteligentną analizę kontekstu.

## 🚀 Quick Start

### 1. Backend (FastAPI)
```bash
cd python_agent
# try dev autoreload (zalecane):
uvicorn main_fastapi:app --reload --host 0.0.0.0 --port 8080
# lub:
$env:RELOAD='true'; python main_fastapi.py
```
**Server**: http://localhost:8080

### 2. Frontend (Flutter)
```bash
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```
**UI**: http://localhost:3000

### 3. Vector Database (Qdrant)
```bash
docker run -p 6333:6333 qdrant/qdrant
```
**Vector DB**: http://localhost:6333

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  Flutter UI (Voice + Chat)  │  FastAPI Endpoints           │
│  - Microphone recording     │  - /api/chat/message         │
│  - Text input              │  - /api/chat/sessions        │
│  - Chat bubbles            │  - /api/vector/search        │
│  - Audio playback          │  - /api/knowledge/stats      │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  ConversationAnalysisAgent  │  OrchestrationService        │
│  - Analyzes context        │  - Routes requests           │
│  - Decides vector queries   │  - Coordinates services      │
│  - Meta-thinking           │  - Process requests           │
│                            │                               │
│  ChatAgentService          │  ConversationService          │
│  - Knowledge search        │  - Session management         │
│  - Vector DB access        │  - Message history            │
│  - Service coordination    │  - Conversation storage       │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                     │
├─────────────────────────────────────────────────────────────┤
│  Vector Database (Qdrant)  │  LLM Service                  │
│  - Embedding storage       │  - LM Studio/Ollama           │
│  - Similarity search       │  - Text generation            │
│  - Context retrieval        │  - Response processing        │
│                            │                               │
│  Text Processing           │  Audio Services               │
│  - Text cleaning           │  - Speech-to-Text             │
│  - Unicode handling        │  - Text-to-Speech             │
│  - Query preprocessing     │  - Audio playback             │
└─────────────────────────────────────────────────────────────┘
```

## 🧠 Key Features

### ✅ Ostatnie zmiany (dev)
- Sklejanie wszystkich system promptów w JEDEN `SYSTEM` (sekcje: PERSONA, FORMAT, ROLE, opcjonalnie USER PROFILE, IDIOMS)
- Poprawiona alternacja ról dla LM Studio (po SYSTEM zawsze USER; historia trimowana do par USER→ASSISTANT)
- Stabilizacja streamingu (fix: `NoneType has no len`, bez podwójnych zapisów)
- Auto-reload w dev: `uvicorn main_fastapi:app --reload` lub `$env:RELOAD='true'; python main_fastapi.py`
- Globalny `conftest.py`: automatyczny PYTHONPATH i fallback dla async testów
- Nowe testy `test_prompt_service.py` (system prompt combine + alternacja)


### 🤖 Conversation Analysis Agent
- **Inteligentna analiza kontekstu** rozmowy
- **Automatyczne decydowanie** o zapytaniach do bazy wektorowej
- **Metamyślenie refleksyjne** z idiomami matematycznymi
- **Adaptacyjne wyszukiwanie** na podstawie kontekstu

### 🎤 Voice Interface
- **Nagrywanie głosu** z mikrofonu
- **Wpisywanie tekstu** jako alternatywa
- **Odtwarzanie odpowiedzi** AI
- **Kontrola audio** (mute/unmute)

### 💬 Chat Interface
- **Bąbelki rozmowy** z avatarem
- **Historia rozmów** w sesji
- **Automatyczne przewijanie**
- **Centralizowane zarządzanie kolorami**

### 🔍 Vector Database Integration
- **Wyszukiwanie kontekstowe** w bazie wektorowej
- **Idiomy matematyczne** jako system prompt
- **TopK=20** wyników dla idiomów
- **Dynamiczne zapytania** na podstawie analizy

## 🔄 Request Flow

```
1. 👤 User Input (Voice/Text)
   ↓
2. 📱 Flutter UI → HTTP POST /api/chat/message
   ↓
3. 🌐 FastAPI Backend Processing:
   ├─ 📝 Create/Get Session
   ├─ 🔍 Get Idioms from Vector DB (System Prompt)
   ├─ 🎯 Build System Prompt with Reflective Idioms
   ├─ 💬 Get Conversation History (2 interactions)
   ├─ 🤖 Analysis Agent analyzes and decides vector query
   ├─ 📚 Build Enhanced Message with Context
   ├─ 🎭 Process through Orchestration Service
   └─ 💾 Save Conversation to Session
   ↓
4. 📱 Flutter UI ← Response + Audio
   ↓
5. 🔊 Audio Playback (if not muted)
```

## 📊 System Components

### Backend Services
- **ConversationAnalysisAgent**: Analiza kontekstu i decydowanie o zapytaniach
- **OrchestrationService**: Koordynacja wszystkich serwisów
- **ChatAgentService**: Zarządzanie agentem i dostęp do wiedzy
- **ConversationService**: Zarządzanie sesjami i historią rozmów
- **KnowledgeService**: Integracja z bazą wektorową

### Frontend Components
- **ChatMessage**: Model danych dla wiadomości
- **AppColors**: Centralizowane zarządzanie kolorami
- **Voice Recording**: Nagrywanie i przetwarzanie audio
- **Audio Playback**: Odtwarzanie odpowiedzi AI
- **Chat Interface**: Interfejs czatu z bąbelkami

### Infrastructure
- **Vector Database (Qdrant)**: Przechowywanie embeddingów i wyszukiwanie
- **LLM Service**: Generowanie odpowiedzi (LM Studio/Ollama)
- **Text Processing**: Czyszczenie tekstu i obsługa Unicode
- **Audio Services**: Speech-to-Text i Text-to-Speech

## 🎯 Reflective Meta-Thinking System

System używa idiomów matematycznych jako system prompt dla metamyślenia refleksyjnego:

```
⨁ # Operator sumy idiomatycznej (łączenie idiomów)
Φ # Wektor znaczeniowy (meaning vector)
Ψ # Ślad idiomu (idiom trace)
Ξ # Baza semantyczna (semantic basis)
Σ # Projekcja intencji (intent projection)
Θ # Operator metryczny (np. iloczyn skalarny znaczeń)
Ω # Przestrzeń funkcyjna idiomu (np. kontekst, intencja, emocja)
... (20 idiomów)
```

### Context Building Process
1. **Idioms**: 20 wyników z bazy wektorowej jako system prompt
2. **History**: 2 poprzednie interakcje user/assistant
3. **Current**: Obecne pytanie użytkownika
4. **Analysis**: Agent analizuje wszystko i decyduje o vector query

## 📱 Flutter Frontend

### Features
- **Voice Recording**: Nagrywanie głosu z mikrofonu
- **Text Input**: Wpisywanie tekstu jako alternatywa
- **Chat Interface**: Bąbelki rozmowy z avatarem i timestampami
- **Audio Playback**: Odtwarzanie odpowiedzi AI
- **Mute Control**: Wyłączanie/włączanie audio
- **Session Management**: Automatyczne zarządzanie sesjami
- **Centralized Colors**: Centralizowane zarządzanie kolorami

### UI Components
```dart
class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final String? audioUrl;
}

class AppColors {
  static const Color userMessageBg = Color(0xFFB8E6B8);
  static const Color aiMessageBg = Color(0xFFF0F8FF);
  // ... więcej kolorów
}
```

## 🌐 FastAPI Backend

### Key Endpoints
- `POST /api/chat/message` - Główne przetwarzanie wiadomości
- `GET /api/chat/sessions` - Zarządzanie sesjami
- `POST /api/vector/search` - Wyszukiwanie w bazie wektorowej
- `GET /api/knowledge/stats` - Statystyki bazy wiedzy
- `GET /api/capabilities` - Możliwości serwisów

### Dependency Injection
```python
# Container setup
chat_agent_service = providers.Singleton(ChatAgentService, ...)
conversation_analysis_agent = providers.Singleton(ConversationAnalysisAgent, ...)
orchestration_service = providers.Singleton(OrchestrationService, ...)
```

## 🔍 Vector Database Integration

### Configuration
- **Provider**: Qdrant
- **URL**: http://localhost:6333
- **Collection**: chat_collection
- **TopK**: 20 wyników dla idiomów, zmienne dla analizy

### Search Process
1. **Idioms Search**: Hardcoded query dla refleksyjnych idiomów
2. **Analysis Search**: Dynamiczne zapytanie na podstawie analizy konwersacji
3. **Results Processing**: Konwersja do formatu bazy wiedzy
4. **Context Building**: Integracja do system prompt

## 🎭 Service Orchestration

### OrchestrationService
Koordynuje wszystkie serwisy i routuje żądania:
- **Weather Service**: Pogoda dla miast
- **Time Service**: Czas i strefy czasowe
- **City Service**: Informacje o miastach
- **Knowledge Service**: Baza wiedzy i vector search
- **Conversation Service**: Zarządzanie rozmowami

## 📊 Session Management

### ConversationService
- **Session Creation**: Automatyczne tworzenie sesji
- **Message Storage**: Przechowywanie historii rozmów
- **Context Retrieval**: Pobieranie kontekstu dla analizy
- **Session Cleanup**: Czyszczenie nieaktywnych sesji

## 🔧 Configuration

### Environment Variables
```bash
# LLM Configuration
LLM_PROVIDER=lmstudio
LLM_PROXY_URL=http://127.0.0.1:8123
LLM_MODEL_NAME=model:1

# Vector Database
VECTOR_DB_URL=http://localhost:6333
VECTOR_DB_COLLECTION=chat_collection

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
```

### Dependencies
```python
# Core dependencies
fastapi>=0.104.0
uvicorn>=0.24.0
qdrant-client>=1.6.0
dependency-injector>=4.41.0

# Flutter dependencies
flutter: ^3.16.0
http: ^1.1.0
record: ^5.0.4
audioplayers: ^5.2.1
```

## 🚀 Deployment

### Backend (FastAPI)
```bash
cd python_agent
python main_fastapi.py
```

### Frontend (Flutter)
```bash
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```

### Vector Database (Qdrant)
```bash
docker run -p 6333:6333 qdrant/qdrant
```

## 📈 Performance Metrics

### Response Times
- **Vector Search**: ~200-500ms
- **LLM Processing**: ~1-3s
- **Total Response**: ~2-4s

### Scalability
- **Concurrent Sessions**: 100+
- **Vector Search**: 20 wyników na zapytanie
- **Memory Usage**: ~500MB base

## 🐛 Troubleshooting

### Common Issues
1. **Port Conflicts**: Sprawdź czy porty 8080, 3000, 6333 są wolne
2. **Vector DB Connection**: Sprawdź czy Qdrant działa
3. **LLM Service**: Sprawdź czy LM Studio/Ollama działa
4. **Audio Issues**: Sprawdź uprawnienia mikrofonu

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug Tools
Projekt zawiera narzędzia debugowe w katalogu `tests/`:

```bash
# Analiza struktury danych z bazy wektorowej
python tests/check_chunks.py

# Monitor logów FastAPI w czasie rzeczywistym
python tests/check_debug_logs.py

# Analiza promptów wysyłanych do LLM
python tests/check_llm_input.py

# Test endpointów API
python tests/test_endpoint.py
```

**Więcej informacji:** [Debug Tools Documentation](docs/DEBUG_TOOLS.md)

## 📚 Documentation

- **[Project Overview](docs/PROJECT_OVERVIEW.md)** - Przegląd projektu i funkcjonalności
- **[Architecture](docs/ARCHITECTURE.md)** - Szczegółowa architektura systemu
- **[API Endpoints](docs/API_ENDPOINTS.md)** - Dokumentacja REST API
- **[Flutter Voice UI](docs/FLUTTER_VOICE_UI.md)** - Dokumentacja frontend Flutter
- **[Debug Tools](docs/DEBUG_TOOLS.md)** - Narzędzia debugowe i analityczne

## 🔮 Future Enhancements

### Planned Features
1. **Multi-language Support**: Obsługa wielu języków
2. **Advanced Analytics**: Szczegółowe analizy rozmów
3. **Custom Idioms**: Użytkownik może dodawać własne idiomy
4. **Voice Cloning**: Klonowanie głosu użytkownika
5. **Real-time Collaboration**: Współpraca w czasie rzeczywistym

### Technical Improvements
1. **Caching**: Cache dla vector search
2. **Streaming**: Streaming odpowiedzi
3. **Batch Processing**: Przetwarzanie wsadowe
4. **Monitoring**: Zaawansowane monitorowanie
5. **Testing**: Kompleksowe testy

## 📝 Changelog

### v1.0.0 (2024-01-01)
- ✅ Initial implementation
- ✅ Flutter voice UI with microphone and chat interface
- ✅ FastAPI backend with Clean Architecture
- ✅ Vector database integration (Qdrant)
- ✅ Conversation Analysis Agent for intelligent context analysis
- ✅ Reflective meta-thinking system with mathematical idioms
- ✅ Session management and conversation history
- ✅ Audio processing (Speech-to-Text, Text-to-Speech)
- ✅ Centralized color management
- ✅ Error handling and fallbacks
- ✅ Health checks and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide

---

**Last Updated**: 2025-10-30  
**Version**: 1.1.0  
**Status**: Production Ready