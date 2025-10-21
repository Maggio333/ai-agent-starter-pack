# QUICK START - AI Agent Starter Pack

## 📚 Dokumentacja

- **👥 Przewodnik dla użytkowników**: [USER_GUIDE.md](USER_GUIDE.md)
- **⚡ Szybki start dla użytkowników**: [QUICK_START_USER.md](QUICK_START_USER.md)
- **🔧 Rozwiązywanie problemów**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **🏗️ Architektura**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **🌐 API**: [API.md](API.md)

## 🚀 Szybkie Uruchomienie (Deweloperzy)

### 1. Przygotowanie Środowiska

```bash
# Przejdź do katalogu projektu
cd moje/ATSReflectumAgentStarterPack/python_agent

# Skopiuj przykładową konfigurację
cp env.example .env

# Edytuj plik .env i ustaw swoje ustawienia
# Najważniejsze:
# LMSTUDIO_LLM_PROXY_URL=http://127.0.0.1:8123
# EMBEDDING_PROVIDER=lmstudio
```

### 2. Instalacja Zależności

```bash
# Zainstaluj wymagane pakiety
pip install -r requirements.txt
```

### 3. Uruchomienie Aplikacji

```bash
# Uruchom aplikację
python main.py
```

**Aplikacja będzie dostępna na:**
- **FastAPI Backend:** http://localhost:8080
- **API Documentation:** http://localhost:8080/docs
- **API Endpoints:** http://localhost:8080/api/

### 4. Uruchomienie Flutter UI (Opcjonalnie)

```bash
# W nowym terminalu
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```

**Flutter UI będzie dostępne na:**
- **Voice Interface:** http://localhost:3000

### 5. Uruchomienie Google ADK Agent (Opcjonalnie)

```bash
# W nowym terminalu
python -m google_adk.agent --config agents/root_agent.yaml
```

## 🎯 Co Masz Dostępne

### **1. FastAPI Backend**
- **URL:** http://localhost:8080
- **Funkcje:** 
  - Chat z agentem
  - Voice processing (STT/TTS)
  - Session management
  - Health monitoring
  - Microservice tools
  - Tool calling visualization
  - Real-time responses
  - Session management

### **2. REST API Endpoints**

#### **Session Management**
```bash
# Utwórz nową sesję
POST /api/sessions
{
  "context": {"user_name": "Arek"},
  "system_prompt": "Jesteś pomocnym asystentem"
}

# Pobierz historię konwersacji
GET /api/sessions/{session_id}/history

# Lista aktywnych sesji
GET /api/sessions/active

# Zamknij sesję
DELETE /api/sessions/{session_id}
```

#### **Agent Services**
```bash
# Informacje o mieście
POST /api/agent/city-request?city=Warszawa

# Pogoda
GET /api/agent/weather/Warszawa

# Czas
GET /api/agent/time/Warszawa
```

#### **Monitoring**
```bash
# Health check
GET /api/health

# Statystyki
GET /api/stats

# Możliwości serwisów
GET /api/capabilities
```

## 🔧 Konfiguracja

### **Plik .env - Najważniejsze Ustawienia**

```bash
# Google Services (WYMAGANE)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_PROJECT_ID=your_project_id_here
GOOGLE_MODEL=gemini-2.0-flash

# Database
DATABASE_PATH=chat.db

# Embedding Service (opcjonalne)
EMBEDDING_PROVIDER=lmstudio
LMSTUDIO_PROXY_URL=http://127.0.0.1:8123

# Qdrant Vector DB (opcjonalne)
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=chat_collection
```

### **Minimalna Konfiguracja**
Jeśli chcesz tylko przetestować z lokalnym modelem:
```bash
# LM Studio (lokalny model)
LLM_PROVIDER=lmstudio
LMSTUDIO_LLM_PROXY_URL=http://127.0.0.1:1234
LMSTUDIO_LLM_MODEL_NAME=model:1

# Embeddings (już masz skonfigurowane)
EMBEDDING_PROVIDER=lmstudio
LMSTUDIO_PROXY_URL=http://127.0.0.1:8123
LMSTUDIO_MODEL_NAME=model:10
```

## 🎨 Jak Używać

### **1. Przez Web UI**
1. Otwórz http://localhost:8080
2. Zacznij chatować z agentem
3. Agent ma dostęp do 17+ narzędzi (weather, cities, knowledge base, etc.)

### **2. Przez API**
```python
import requests

# Utwórz sesję
response = requests.post("http://localhost:8080/api/sessions", 
                        json={"context": {"user": "test"}})
session_id = response.json()["session_id"]

# Wyślij wiadomość przez agenta
response = requests.post("http://localhost:8080/api/agent/city-request",
                        params={"city": "Kraków", "session_id": session_id})
print(response.json())
```

## 🛠️ Rozwiązywanie Problemów

### **Problem: "GOOGLE_API_KEY not set"**
```bash
# Sprawdź czy masz plik .env
ls -la .env

# Sprawdź zawartość
cat .env | grep GOOGLE_API_KEY
```

### **Problem: "Module not found"**
```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Sprawdź czy jesteś w odpowiednim katalogu
pwd
# Powinno być: .../python_agent
```

### **Problem: Port zajęty**
```bash
# Zmień port w .env
echo "PORT=8081" >> .env

# Lub uruchom z innym portem
python main.py --port 8081
```

## 🎯 Co Działa Out-of-the-Box

✅ **Chat z agentem** - pełna funkcjonalność  
✅ **Session management** - zarządzanie sesjami  
✅ **Health monitoring** - status wszystkich serwisów  
✅ **API documentation** - automatyczna dokumentacja  
✅ **Tool calling** - agent używa narzędzi  
✅ **Conversation history** - historia rozmów  
✅ **Statistics** - statystyki użycia  

## 🚀 Następne Kroki

Po testach prostego UI możesz:
1. **Dodać React frontend** - piękny UI jak w ChatElioraSystem
2. **Rozszerzyć API** - więcej endpointów
3. **Dodać autentykację** - JWT tokens
4. **Deploy na Cloud Run** - production deployment

## 🏗️ Wzorce Architektoniczne

### **1. Clean Architecture**
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

### **2. Dependency Injection**
```python
from application.services.di_service import DIService

# Automatyczne wstrzykiwanie zależności
di_service = DIService()

# Pobieranie serwisów
llm_service = di_service.get_llm_service()
voice_service = di_service.get_voice_service()
chat_agent_service = di_service.get_chat_agent_service()
```

### **3. Railway Oriented Programming (ROP)**
```python
from domain.common.result import Result

# Spójne obsługiwanie błędów
result = await service.process_data(input_data)
if result.is_success:
    # Sukces
    data = result.value
else:
    # Błąd
    error_message = result.error
```

### **4. Multi-UI Architecture**
- **Flutter Voice UI**: Nowoczesny interfejs głosowy
- **Google ADK Agent**: Zaawansowany agent z narzędziami
- **FastAPI Backend**: RESTful API dla wszystkich frontendów
- **Future**: Własny system narzędzi (zastąpi ADK)

> **📚 Szczegółowe wzorce**: Zobacz [ARCHITECTURAL_PATTERNS.md](ARCHITECTURAL_PATTERNS.md) dla kompletnych przykładów i implementacji.

## 🛠️ Rozwój Własnego Agenta

### **Krok 1: Wybór Interfejsu**
```bash
# Opcja A: Flutter Voice UI (zalecane dla voice-first)
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000

# Opcja B: Google ADK (zalecane dla enterprise)
python -m google_adk.agent --config agents/root_agent.yaml

# Opcja C: Własny frontend (dowolny framework)
# Użyj API endpoints z http://localhost:8080/api/
```

### **Krok 2: Dodanie Własnych Narzędzi**
```python
# 1. Stwórz nowy serwis w infrastructure/services/
class MyCustomService:
    async def process_data(self, data: str) -> Result[str, str]:
        # Twoja logika biznesowa
        pass

# 2. Zarejestruj w application/container.py
my_service = providers.Singleton(MyCustomService)

# 3. Dodaj do ChatAgentService
class ChatAgentService:
    def __init__(self, ..., my_service: MyCustomService):
        self.my_service = my_service
        # Zarejestruj jako narzędzie
        self._services["my_tool"] = self.my_service
```

### **Krok 3: Konfiguracja Środowiska**
```bash
# .env
LMSTUDIO_LLM_PROXY_URL=http://127.0.0.1:8123
EMBEDDING_PROVIDER=lmstudio
CACHE_PROVIDER=memory
SEARCH_PROVIDER=local

# Dodaj własne zmienne
MY_SERVICE_API_KEY=your_key_here
MY_SERVICE_URL=https://api.example.com
```

## 🔧 Narzędzia Deweloperskie

### **Testowanie**
```bash
# Uruchom wszystkie testy
python -m pytest tests/

# Test konkretnego serwisu
python -m pytest tests/test_voice_service.py

# Test z coverage
python -m pytest --cov=application tests/
```

### **Debugging**
```bash
# Uruchom z debugowaniem
python -m debugpy --listen 5678 main.py

# Sprawdź logi
tail -f logs/app.log

# Health check
curl http://localhost:8080/api/health
```

### **Monitoring**
```bash
# Sprawdź status serwisów
curl http://localhost:8080/api/capabilities

# Statystyki konwersacji
curl http://localhost:8080/api/stats

# Health wszystkich komponentów
curl http://localhost:8080/api/health
```

## 📚 Dalsze Kroki

1. **Przeczytaj dokumentację**: [ARCHITECTURE.md](ARCHITECTURE.md), [API.md](API.md)
2. **Eksperymentuj z kodem**: Zmodyfikuj serwisy, dodaj nowe narzędzia
3. **Stwórz własny agent**: Użyj wzorców jako podstawy
4. **Współtwórz**: Dodaj nowe funkcjonalności, popraw błędy

## 🆘 Wsparcie

- **Dokumentacja**: [docs/](docs/)
- **Problemy**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Przykłady**: [tests/examples/](../tests/examples/)
- **Kontakt**: Arkadiusz Słota - [LinkedIn](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/) | [GitHub](https://github.com/Maggio333)

---

**Powodzenia z Twoim zaawansowanym agentem! 🎉**
