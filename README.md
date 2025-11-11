# 🎯 Voice AI Assistant

Zaawansowany system chatbot z architekturą Clean Architecture, integrujący Flutter frontend, FastAPI backend, bazę wektorową i inteligentną analizę kontekstu.

## 🚀 Quick Start

### Opcja 1: Docker (Zalecane) 🐳

Najprostszy sposób uruchomienia całego systemu:

```bash
cd python_agent

# 1. Skopiuj plik konfiguracyjny
cp env.example .env

# 2. Uruchom LM Studio na hoście (port 8123)
#    - Zainstaluj z https://lmstudio.ai/
#    - Załaduj model
#    - Uruchom Local Server (Settings → Local Server)

# 3. Uruchom wszystkie serwisy
docker-compose up --build

# 4. Dostęp:
#    - Frontend: http://localhost:3000
#    - Backend API: http://localhost:8080
#    - Qdrant UI: http://localhost:6333/dashboard
```

**Więcej informacji**: [DOCKER.md](DOCKER.md)

### Opcja 2: Lokalne uruchomienie

#### 1. Backend (FastAPI)
```bash
cd python_agent
# try dev autoreload (zalecane):
uvicorn main_fastapi:app --reload --host 0.0.0.0 --port 8080
# lub:
$env:RELOAD='true'; python main_fastapi.py
```
**Server**: http://localhost:8080

#### 2. Frontend (Flutter)
```bash
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```
**UI**: http://localhost:3000

#### 3. Vector Database (Qdrant)
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
│  - Microphone recording     │  - /api/message/stream (SSE) │
│  - Text input               │  - /api/message              │
│  - Chat bubbles             │  - /api/sessions             │
│  - Audio playback           │  - /api/vector/search        │
│  - TTS Queue                │  - /api/knowledge/stats      │
│                              │  - /api/voice/*              │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                     │
├─────────────────────────────────────────────────────────────┤
│  ConversationAnalysisAgent  │  OrchestrationService        │
│  ChatAgentService           │  ConversationService         │
│  DynamicRAGService          │  PromptService               │
└─────────────────────────────────────────────────────────────┘
                                │ uses
┌─────────────────────────────────────────────────────────────┐
│                          DOMAIN LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  Entities: ChatMessage, RAGChunk, Result                    │
│  Interfaces: ILLMService, IKnowledgeService, Repositories   │
│  Policies: validation, invariants                           │
└─────────────────────────────────────────────────────────────┘
                                │ implemented by
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                     │
├─────────────────────────────────────────────────────────────┤
│  Vector Database (Qdrant)  │  LLM Service                  │
│  - Embedding storage       │  - LM Studio/Ollama           │
│  - Similarity search       │  - Text generation            │
│  - Context retrieval       │  - Response processing        │
│                            │                               │
│  SQLite ChatRepository     │  Text / Audio Services        │
│  - CRUD/Threads/Stats      │  - Cleaning / STT / TTS       │
└─────────────────────────────────────────────────────────────┘
```

## 🧠 Key Features

### ✅ Ostatnie zmiany (2025-11-11)
- **Docker Support**: Pełna konteneryzacja backendu i frontendu z Docker Compose
- **Dynamic RAG**: Inteligentne zapytania do bazy wektorowej generowane przez LLM
- **Streaming Responses**: Server-Sent Events (SSE) dla czasu rzeczywistego
- **Voice Chat**: Nagrywanie głosu, transkrypcja i synteza mowy
- **TTS Queue**: Kolejkowanie zdań dla płynnego odtwarzania audio
- **Debug Panel**: Panel debugowy w Flutterze z 200 ostatnimi logami
- **Szczegółowe logi**: Kompleksowe logowanie procesu RAG i wyszukiwania
- **Polskie tłumaczenia**: Wszystkie system prompty i komunikaty po polsku
- **Auto-reload w dev**: `uvicorn main_fastapi:app --reload` lub `$env:RELOAD='true'; python main_fastapi.py`


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

### 🔍 Vector Database Integration (RAG)
- **Dynamic RAG**: LLM generuje zapytania do bazy wektorowej na podstawie kontekstu rozmowy
- **Inteligentne filtrowanie**: Score threshold (0.50) dla jakości wyników
- **Idiomy matematyczne**: Automatyczne pobieranie idiomów jako system prompt
- **Kontekst w czasie rzeczywistym**: Wyniki RAG dodawane do promptu przed odpowiedzią LLM
- **Szczegółowe logi**: Pełne śledzenie procesu wyszukiwania i filtrowania

## 🔄 Request Flow

```
1. 👤 User Input (Voice/Text)
   ↓
2. 📱 Flutter UI → HTTP POST /api/message/stream (SSE)
   ↓
3. 🌐 FastAPI Backend Processing (Streaming):
   ├─ 📝 Create/Get Session
   ├─ 🔍 Get Idioms from Vector DB (System Prompt)
   ├─ 💬 Get Conversation History
   ├─ 🤖 Dynamic RAG: LLM generuje zapytanie do bazy wektorowej
   ├─ 📚 Wyszukiwanie w bazie wektorowej (score threshold: 0.50)
   ├─ 🎯 Build System Prompt z kontekstem RAG
   ├─ 🎭 Process through LLM Service (Streaming)
   └─ 💾 Save Conversation to Session
   ↓
4. 📱 Flutter UI ← SSE Stream (chunks + status)
   ├─ 📨 Chunk: Fragment odpowiedzi
   ├─ 📚 Status: Informacje o RAG
   └─ ✅ Done: Zakończenie streamingu
   ↓
5. 🔊 TTS Queue: Automatyczne odtwarzanie zdań
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
- `POST /api/message/stream` - **Streaming endpoint (SSE)** - główne przetwarzanie wiadomości z RAG
- `POST /api/message` - Synchroniczne przetwarzanie wiadomości
- `POST /api/sessions` - Tworzenie nowej sesji
- `GET /api/sessions/{session_id}` - Pobieranie sesji
- `GET /api/sessions/{session_id}/history` - Historia rozmowy w sesji
- `GET /api/sessions/active` - Lista aktywnych sesji
- `DELETE /api/sessions/{session_id}` - Usuwanie sesji
- `POST /api/vector/search` - Wyszukiwanie w bazie wektorowej
- `GET /api/knowledge/stats` - Statystyki bazy wiedzy
- `GET /api/capabilities` - Możliwości serwisów
- `POST /api/voice/transcribe` - Transkrypcja audio (Speech-to-Text)
- `POST /api/voice/speak` - Synteza mowy (Text-to-Speech)

### Dependency Injection
```python
# Container setup
chat_agent_service = providers.Singleton(ChatAgentService, ...)
conversation_analysis_agent = providers.Singleton(ConversationAnalysisAgent, ...)
orchestration_service = providers.Singleton(OrchestrationService, ...)
```

## 🔍 Vector Database Integration (RAG)

### Configuration
- **Provider**: Qdrant
- **URL**: http://localhost:6333 (lub `http://host.docker.internal:6333` w Docker)
- **Collections**:
  - `CuratedIdiomsForAI` - **Kolekcja idiomów** (refleksyjne idiomy matematyczne)
  - `PierwszaKolekcjaOnline` - **Standardowa kolekcja** (ogólne dane, dynamic RAG)
  - `chat_collection` - Kolekcja czatu (opcjonalna)
- **Embedding Provider**: LM Studio (lub inny z `EMBEDDING_PROVIDER`)
- **Score Threshold**: 0.50 (dla dynamic RAG), 0.75 (dla idiomów)

### Dynamic RAG Process
1. **LLM Analysis**: LLM analizuje kontekst rozmowy i generuje zapytanie do bazy wektorowej
2. **Vector Search**: Wyszukiwanie w Qdrant z embedding service
3. **Filtering**: Filtrowanie wyników według score threshold (0.50)
4. **Context Formatting**: Konwersja wyników do formatu RAGResult
5. **System Message**: Dodanie kontekstu RAG jako wiadomość systemowa przed odpowiedzią LLM

### Idioms Search
- **Collection**: `CuratedIdiomsForAI` - dedykowana kolekcja dla idiomów
- **Hardcoded Query**: "IDIOM_REFLECT REFLECTIVE THINKING CONCEPTS" dla refleksyjnych idiomów matematycznych
- **TopK**: 20 wyników
- **Usage**: Automatyczne dodawanie do system prompt przed każdą odpowiedzią LLM

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
# Dla lokalnego uruchomienia: http://127.0.0.1:8123
# Dla Docker: http://host.docker.internal:8123
LMSTUDIO_LLM_PROXY_URL=http://host.docker.internal:8123
LMSTUDIO_LLM_MODEL_NAME=model:1

# Embedding Configuration
EMBEDDING_PROVIDER=lmstudio
# Dla lokalnego uruchomienia: http://127.0.0.1:8123
# Dla Docker: http://host.docker.internal:8123
LMSTUDIO_PROXY_URL=http://host.docker.internal:8123

# Vector Database
VECTOR_DB_PROVIDER=qdrant
# Dla lokalnego uruchomienia: http://localhost:6333
# Dla Docker: http://qdrant:6333
QDRANT_URL=http://qdrant:6333
LOCAL_SEARCH_INDEX=PierwszaKolekcjaOnline

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8080
FRONTEND_PORT=3000
```

**Więcej opcji**: Zobacz [env.example](env.example) dla pełnej listy zmiennych konfiguracyjnych.

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
1. **Caching**: Cache dla vector search ✅ (częściowo - memory cache)
2. **Streaming**: Streaming odpowiedzi ✅ (SSE zaimplementowane)
3. **Batch Processing**: Przetwarzanie wsadowe
4. **Monitoring**: Zaawansowane monitorowanie ✅ (szczegółowe logi RAG)
5. **Testing**: Kompleksowe testy ✅ (testy jednostkowe i integracyjne)

## 📝 Changelog

### v1.2.0 (2025-11-11)
- ✅ **Docker Support**: Pełna konteneryzacja backendu i frontendu z Docker Compose
- ✅ **Dynamic RAG**: LLM generuje zapytania do bazy wektorowej na podstawie kontekstu
- ✅ **Streaming Responses**: Server-Sent Events (SSE) dla czasu rzeczywistego
- ✅ **Voice Chat**: Nagrywanie głosu, transkrypcja i synteza mowy
- ✅ **TTS Queue**: Kolejkowanie zdań dla płynnego odtwarzania audio
- ✅ **Polskie tłumaczenia**: Wszystkie system prompty i komunikaty po polsku
- ✅ **Szczegółowe logi**: Kompleksowe logowanie procesu RAG i wyszukiwania
- ✅ **Debug Panel**: Panel debugowy w Flutterze z 200 ostatnimi logami
- ✅ **Nginx Configuration**: Proxy dla frontendu i backendu z timeoutami
- ✅ **Code Cleanup**: Usunięcie niepotrzebnych print() i DEBUG logów

### v1.1.0 (2024-10-30)
- ✅ Sklejanie wszystkich system promptów w JEDEN `SYSTEM`
- ✅ Poprawiona alternacja ról dla LM Studio
- ✅ Stabilizacja streamingu
- ✅ Auto-reload w dev
- ✅ Globalny `conftest.py` dla testów

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

**Last Updated**: 2025-11-11  
**Version**: 1.2.0  
**Status**: Production Ready