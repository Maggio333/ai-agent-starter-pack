# Voice AI Assistant - Server Comparison

## 🎯 **Dwa różne serwery - jedna aplikacja!**

Mamy teraz **dwa osobne serwery** pokazujące różnice między Google ADK a czystym FastAPI.

## 📁 **Pliki:**

- **`main_adk.py`** - Google ADK wersja
- **`main_fastapi.py`** - Czysty FastAPI wersja  
- **`main_service.py`** - Uniwersalny serwer (domyślnie FastAPI)

## 🚀 **Jak uruchomić:**

### **Google ADK wersja:**
```bash
python main_adk.py
```

### **Czysty FastAPI wersja:**
```bash
python main_fastapi.py
```

### **Uniwersalny serwer:**
```bash
# Domyślnie FastAPI
python main_service.py

# Lub z zmienną środowiskową
WEB_SERVER_TYPE=google_adk python main_service.py
WEB_SERVER_TYPE=clean_fastapi python main_service.py
```

## 📊 **Porównanie:**

| Funkcja | Google ADK | Clean FastAPI |
|---------|------------|---------------|
| **Startup** | Wolny, dużo ostrzeżeń | Szybki, czyste logi |
| **Ostrzeżenia** | `[EXPERIMENTAL]` warnings | Brak ostrzeżeń |
| **OpenAPI** | Wyłączony (błędy PIL) | Włączony (`/docs`) |
| **Zależności** | Google ADK + FastAPI | Tylko FastAPI |
| **Kontrola** | Ograniczona | Pełna |
| **Performance** | Wolniejszy | Szybszy |
| **Debugging** | Trudniejszy | Łatwiejszy |

## 🔍 **Różnice w logach:**

### **Google ADK (`main_adk.py`):**
```
WARNING:root:Whoosh not available...
WARNING:root:Elasticsearch not available...
UserWarning: [EXPERIMENTAL] InMemoryCredentialService...
UserWarning: [EXPERIMENTAL] BaseCredentialService...
INFO:google_adk.google.adk.models.registry:Updating LLM class...
```

### **Clean FastAPI (`main_fastapi.py`):**
```
INFO:__main__:🚀 Starting Voice AI Assistant with Clean FastAPI...
INFO:__main__:🔧 Using Clean FastAPI web server
INFO:__main__:✨ Clean startup - no Google ADK warnings!
```

## 🎯 **Który wybrać?**

- **Google ADK** - jeśli potrzebujesz funkcji Google ADK
- **Clean FastAPI** - dla większości przypadków (zalecane)
- **Uniwersalny** - dla łatwego przełączania

## 🌐 **Endpointy:**

Wszystkie serwery mają te same endpointy:
- `POST /api/voice/transcribe` - transkrypcja mowy
- `POST /api/voice/speak` - synteza mowy  
- `POST /api/chat/send` - chat z AI
- `GET /api/voice/health` - health check
- `GET /docs` - dokumentacja API (tylko FastAPI)

## 🎉 **Wynik:**

**Masz teraz pełną kontrolę nad architekturą serwera!**
