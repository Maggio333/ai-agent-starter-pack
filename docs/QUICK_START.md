# QUICK START - ATS Reflectum Agent Chat UI

## 🚀 Szybkie Uruchomienie

### 1. Przygotowanie Środowiska

```bash
# Przejdź do katalogu projektu
cd moje/ATSReflectumAgentStarterPack/python_agent

# Skopiuj przykładową konfigurację
cp env.example .env

# Edytuj plik .env i ustaw swoje klucze API
# Najważniejsze:
# GOOGLE_API_KEY=your_google_api_key_here
# GOOGLE_PROJECT_ID=your_project_id_here
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
- **Web UI (Chat):** http://localhost:8080
- **API Documentation:** http://localhost:8080/docs
- **API Endpoints:** http://localhost:8080/api/

## 🎯 Co Masz Dostępne

### **1. Google ADK Web Interface**
- **URL:** http://localhost:8080
- **Funkcje:** 
  - Chat z agentem
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

## 📞 Wsparcie

Jeśli masz problemy:
1. Sprawdź logi aplikacji
2. Sprawdź konfigurację .env
3. Sprawdź czy wszystkie serwisy działają: `/api/health`

---

**Powodzenia z Twoim zaawansowanym agentem! 🎉**
