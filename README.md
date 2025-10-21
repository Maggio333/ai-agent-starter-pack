# 🎤 Voice AI Assistant

**Voice AI Assistant** to aplikacja do rozmowy z sztuczną inteligencją używając głosu. Mówisz do aplikacji, AI odpowiada tekstowo, a następnie AI mówi odpowiedź.

## 🚀 Szybki Start

### Dla użytkowników (osoby nietechniczne)
📖 **[Przewodnik użytkownika](docs/USER_GUIDE.md)** - kompletna instrukcja instalacji i użytkowania

⚡ **[Szybki start](docs/QUICK_START_USER.md)** - instalacja w 5 minut

🔧 **[Rozwiązywanie problemów](docs/TROUBLESHOOTING.md)** - pomoc gdy coś nie działa

### Dla deweloperów
⚡ **[Quick Start](docs/QUICK_START.md)** - szybkie uruchomienie dla deweloperów

🏗️ **[Architektura](docs/ARCHITECTURE.md)** - opis architektury aplikacji

📚 **[API](docs/API.md)** - dokumentacja API

## 🎯 Co to jest?

**Voice AI Assistant** składa się z:

- **🎤 Speech-to-Text** - zamienia Twoją mowę na tekst
- **🤖 AI Chat** - odpowiada na pytania używając lokalnego modelu AI
- **🔊 Text-to-Speech** - zamienia odpowiedź AI na mowę

## 🏗️ Architektura

```
┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │
│  ┌─────────────────────────────────┐   │
│  │      Flutter Voice UI           │   │  ← Port 3000
│  │  - Speech-to-Text               │   │
│  │  - Text-to-Speech               │   │
│  │  - Voice Controls               │   │
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
│  │         DIService               │   │  ← DI Facade
│  │  - Service Access               │   │
│  │  - Lazy Loading                  │   │
│  │  - Error Handling               │   │
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
- **📱 Flutter UI** - aplikacja webowa
- **🔧 Dependency Injection** - 21 serwisów
- **📊 Health Monitoring** - status serwisów
- **🗄️ SQLite Database** - historia rozmów
- **📧 Email Service** - wysyłanie emaili

### 🚧 W planach
- **🌐 React Frontend** - piękny UI
- **🔐 Autentykacja** - JWT tokens
- **☁️ Cloud Deployment** - Railway/Heroku
- **📱 Mobile App** - Flutter mobile
- **🎨 Custom Voices** - więcej głosów TTS

## 🛠️ Technologie

### Backend
- **Python 3.10+** - główny język
- **FastAPI** - web framework
- **Dependency Injector** - DI container
- **SQLite** - baza danych
- **Whisper** - Speech-to-Text
- **Piper** - Text-to-Speech

### Frontend
- **Flutter** - UI framework
- **Web** - aplikacja webowa
- **Material Design** - design system

### AI
- **LM Studio** - lokalny model AI
- **Local Models** - wszystko działa offline

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
cd ATSReflectumAgentStarterPack/python_agent

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
python main.py
```

**📖 Pełna instrukcja**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)

## 📚 Documentation

- **👥 User Guide**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - Complete guide for non-technical users
- **⚡ Quick Start**: [docs/QUICK_START_USER.md](docs/QUICK_START_USER.md) - 5-minute setup guide
- **🔧 Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions
- **🏗️ Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture overview
- **🌐 API Reference**: [docs/API.md](docs/API.md) - Complete API documentation
- **🛠️ Developer Guide**: [docs/QUICK_START.md](docs/QUICK_START.md) - Developer quick start
- **🎯 Patterns**: [docs/ARCHITECTURAL_PATTERNS.md](docs/ARCHITECTURAL_PATTERNS.md) - Architectural patterns guide
- **🛣️ Roadmap**: [docs/ROADMAP.md](docs/ROADMAP.md) - Development roadmap and future plans

## 🎮 Użytkowanie

1. **Uruchom LM Studio** - załaduj model AI
2. **Uruchom Python Backend** - `python main.py`
3. **Uruchom Flutter Frontend** - `flutter run -d web-server --web-port 3000`
4. **Otwórz aplikację** - http://localhost:3000
5. **Kliknij mikrofon** 🎤 i mów!

## 🔧 Rozwiązywanie problemów

**Najczęstsze problemy:**
- Port zajęty → zabij proces używający portu
- Python nie działa → sprawdź instalację i PATH
- LM Studio nie odpowiada → sprawdź czy serwer jest uruchomiony
- Flutter nie działa → sprawdź `flutter doctor`

**📖 Pełny przewodnik**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## 📊 Status

**✅ Gotowe:**
- Backend API (31+ serwisów)
- Voice processing (STT + TTS)
- Flutter UI
- Dependency Injection
- Health monitoring

**🚧 W trakcie:**
- Dokumentacja
- Testy automatyczne
- Deployment

## 🤝 Wsparcie

- **📖 Dokumentacja**: [docs/](docs/)
- **🐛 Problemy**: GitHub Issues
- **💼 LinkedIn**: [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **🐙 GitHub**: [Maggio333](https://github.com/Maggio333)

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE)

---

**Miłego używania Voice AI Assistant!** 🎉🎤🤖