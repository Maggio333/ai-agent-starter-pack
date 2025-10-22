# 🎤 Voice AI Assistant - Full Stack

**Voice AI Assistant** to kompletna aplikacja do rozmowy z sztuczną inteligencją używając głosu. Składa się z backendu Python (FastAPI + Google ADK) i frontendu Flutter Web.

## 🚀 Szybki Start

### Dla użytkowników (osoby nietechniczne)
📖 **[Przewodnik użytkownika](python_agent/docs/USER_GUIDE.md)** - kompletna instrukcja instalacji i użytkowania

⚡ **[Szybki start](python_agent/docs/QUICK_START_USER.md)** - instalacja w 5 minut

🔧 **[Rozwiązywanie problemów](python_agent/docs/TROUBLESHOOTING.md)** - pomoc gdy coś nie działa

### Dla deweloperów
⚡ **[Quick Start](python_agent/docs/QUICK_START.md)** - szybkie uruchomienie dla deweloperów

🏗️ **[Architektura](python_agent/docs/ARCHITECTURE.md)** - opis architektury aplikacji

📚 **[API](python_agent/docs/API.md)** - dokumentacja API

## 🎯 Co to jest?

**Voice AI Assistant** składa się z:

- **🎤 Speech-to-Text** - zamienia Twoją mowę na tekst (Whisper)
- **🤖 AI Chat** - odpowiada na pytania używając lokalnego modelu AI (LM Studio)
- **🔊 Text-to-Speech** - zamienia odpowiedź AI na mowę (Piper TTS)
- **📱 Flutter Web UI** - piękny interfejs użytkownika

## 🏗️ Architektura

```
┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │
│  ┌─────────────────────────────────┐   │
│  │      Flutter Voice UI           │   │  ← Port 3000
│  │  - Speech-to-Text               │   │
│  │  - Text-to-Speech               │   │
│  │  - Voice Controls               │   │
│  │  - Material Design              │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │      FastAPI Endpoints          │   │  ← Port 8080
│  │  - /api/send                    │   │
│  │  - /api/voice/transcribe       │   │
│  │  - /api/voice/speak            │   │
│  │  - Google ADK Integration      │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           APPLICATION LAYER             │
│  ┌─────────────────────────────────┐   │
│  │         Container               │   │  ← DI Container
│  │  - 21 Services Registered       │   │
│  │  - Dependency Injection         │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │      ChatAgentService           │   │  ← Google ADK Agent
│  │  - Microservices Integration    │   │
│  │  - Tool Calling                 │   │
│  │  - ROP Patterns                 │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│             DOMAIN LAYER               │
│  ┌─────────────────────────────────┐   │
│  │         Entities                │   │  ← Business Objects
│  │  - ChatMessage                  │   │
│  │  - RAGChunk                     │   │
│  │  - QualityLevel                 │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │         Services                │   │  ← Business Logic
│  │  - ROPService                   │   │
│  │  - Interfaces (I*)              │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │       Repositories              │   │  ← Data Access
│  │  - ChatRepository               │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           INFRASTRUCTURE LAYER         │
│  ┌─────────────────────────────────┐   │
│  │    Concrete Implementations     │   │
│  │  - VoiceService (STT/TTS)      │   │
│  │  - LMStudioLLMService          │   │
│  │  - SqliteChatRepository         │   │
│  │  - EmailService                 │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 🎯 Funkcje

### ✅ Zaimplementowane
- **🎤 Speech-to-Text** - Whisper (faster_whisper)
- **🔊 Text-to-Speech** - Piper TTS
- **🤖 AI Chat** - LM Studio (lokalny model)
- **📱 Flutter Web UI** - aplikacja webowa
- **🔧 Dependency Injection** - 21 serwisów
- **📊 Health Monitoring** - status serwisów
- **🗄️ SQLite Database** - historia rozmów
- **📧 Email Service** - wysyłanie emaili
- **🌐 Google ADK Integration** - zaawansowany agent
- **🔍 Vector Database** - Qdrant + embeddings
- **📚 Knowledge Base** - RAG functionality

### 🚧 W planach
- **🌐 React Frontend** - alternatywny UI
- **🔐 Autentykacja** - JWT tokens
- **☁️ Cloud Deployment** - Railway/Heroku
- **📱 Mobile App** - Flutter mobile
- **🎨 Custom Voices** - więcej głosów TTS
- **🔗 Multi-language** - obsługa wielu języków

## 🛠️ Technologie

### Backend
- **Python 3.10+** - główny język
- **FastAPI** - web framework
- **Google ADK** - agent framework
- **Dependency Injector** - DI container
- **SQLite** - baza danych
- **Whisper** - Speech-to-Text
- **Piper** - Text-to-Speech
- **Qdrant** - vector database
- **LM Studio** - lokalny model AI

### Frontend
- **Flutter** - UI framework
- **Web** - aplikacja webowa
- **Material Design** - design system
- **Web Audio API** - nagrywanie audio
- **HTTP Client** - komunikacja z API

### AI
- **LM Studio** - lokalny model AI
- **Local Models** - wszystko działa offline
- **Vector Embeddings** - LM Studio embeddings
- **RAG** - Retrieval Augmented Generation

## 📦 Instalacja

### Wymagania
- **Windows 10/11** (64-bit)
- **Python 3.10+**
- **Flutter SDK**
- **LM Studio**
- **8GB RAM** minimum

### Szybka instalacja
```bash
# Pobierz kod
git clone https://github.com/Maggio333/ai-agent-starter-pack.git
cd ai-agent-starter-pack

# Backend Python
pip install -r requirements.txt

# Uruchom aplikację
# Terminal 1: Backend (wybierz jeden)
python main_fastapi.py    # Clean FastAPI (zalecane)
# LUB
python main_adk.py        # Google ADK (zaawansowane)

# Terminal 2: Frontend
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```

**📖 Pełna instrukcja**: [python_agent/docs/USER_GUIDE.md](python_agent/docs/USER_GUIDE.md)

## 📚 Documentation

- **👥 User Guide**: [python_agent/docs/USER_GUIDE.md](python_agent/docs/USER_GUIDE.md) - Complete guide for non-technical users
- **⚡ Quick Start**: [python_agent/docs/QUICK_START_USER.md](python_agent/docs/QUICK_START_USER.md) - 5-minute setup guide
- **🆕 Simple Guide**: [python_agent/docs/README_SIMPLE.md](python_agent/docs/README_SIMPLE.md) - Ultra-simple guide for beginners
- **🪟 Windows Setup**: [python_agent/docs/SETUP_WINDOWS.md](python_agent/docs/SETUP_WINDOWS.md) - Detailed Windows installation
- **🔧 Troubleshooting**: [python_agent/docs/TROUBLESHOOTING.md](python_agent/docs/TROUBLESHOOTING.md) - Common issues and solutions
- **🏗️ Architecture**: [python_agent/docs/ARCHITECTURE.md](python_agent/docs/ARCHITECTURE.md) - System architecture overview
- **🌐 API Reference**: [python_agent/docs/API.md](python_agent/docs/API.md) - Complete API documentation
- **🛠️ Developer Guide**: [python_agent/docs/QUICK_START.md](python_agent/docs/QUICK_START.md) - Developer quick start
- **🎯 Patterns**: [python_agent/docs/ARCHITECTURAL_PATTERNS.md](python_agent/docs/ARCHITECTURAL_PATTERNS.md) - Architectural patterns guide
- **🛣️ Roadmap**: [python_agent/docs/ROADMAP.md](python_agent/docs/ROADMAP.md) - Development roadmap and future plans

## 🎮 Użytkowanie

1. **Uruchom LM Studio** - załaduj model AI
2. **Uruchom Python Backend** - `python main_fastapi.py` (zalecane) lub `python main_adk.py`
3. **Uruchom Flutter Frontend** - `cd presentation/ui/flutter_voice_ui && flutter run -d web-server --web-port 3000`
4. **Otwórz aplikację** - http://localhost:3000
5. **Kliknij mikrofon** 🎤 i mów!

## 🔧 Rozwiązywanie problemów

**Najczęstsze problemy:**
- Port zajęty → zabij proces używający portu
- Python nie działa → sprawdź instalację i PATH
- LM Studio nie odpowiada → sprawdź czy serwer jest uruchomiony
- Flutter nie działa → sprawdź `flutter doctor`

**📖 Pełny przewodnik**: [python_agent/docs/TROUBLESHOOTING.md](python_agent/docs/TROUBLESHOOTING.md)

## 📊 Status

**✅ Gotowe:**
- Backend API (31+ serwisów)
- Voice processing (STT + TTS)
- Flutter Web UI
- Dependency Injection
- Health monitoring
- Google ADK Integration
- Vector Database
- Knowledge Base

**🚧 W trakcie:**
- Dokumentacja
- Testy automatyczne
- Deployment

## 🤝 Wsparcie

- **📖 Dokumentacja**: [python_agent/docs/](python_agent/docs/)
- **🐛 Problemy**: GitHub Issues
- **💼 LinkedIn**: [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **🐙 GitHub**: [Maggio333](https://github.com/Maggio333)

## 📄 Licencja

MIT License - zobacz [python_agent/LICENSE](python_agent/LICENSE)

---

**Miłego używania Voice AI Assistant!** 🎉🎤🤖
