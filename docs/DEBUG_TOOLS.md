## New helpers (2025-10-30)

- `check_syntax.py` – szybkie sprawdzenie składni wszystkich plików Pythona:
  ```bash
  cd python_agent
  python check_syntax.py
  ```

- Globalny `tests/conftest.py` –
  - dodaje PYTHONPATH (projekt root) dla testów
  - zapewnia fallback do uruchamiania `async def` testów bez dodatkowych pluginów

## Notes
- Przy LM Studio logi mogą wymagać pełnych treści promptu; ograniczyliśmy nadmiar, ale w razie potrzeby włącz sekcje w PromptService.

Last Updated: 2025-10-30  
Version: 1.1.0
# 🔧 Debug Tools - Narzędzia Debugowania

## 📋 Przegląd

Projekt zawiera zestaw narzędzi debugowych do analizy działania systemu w czasie rzeczywistym.

## 🛠️ Dostępne Narzędzia

### 1. **`check_debug_logs.py`** - Monitor Logów

**Cel:** Monitoruje logi FastAPI w czasie rzeczywistym

**Użycie:**
```bash
python tests/check_debug_logs.py
```

**Co robi:**
- Wysyła test request do `/api/message`
- Monitoruje logi FastAPI
- Pokazuje oczekiwane debug logi
- Pomaga w diagnozowaniu problemów

**Przykład outputu:**
```
🔍 Monitoring FastAPI logs for debug info...
📤 Sending test request...
✅ Request completed: 200
🔍 Looking for debug logs...
📋 Expected debug logs:
   🔍 DEBUG: Pierwszy chunk: {...}
   🔍 DEBUG: Typ pierwszego chunka: <class '...'>
```

### 3. **`check_llm_input.py`** - Analiza Promptów

**Cel:** Sprawdza co dokładnie trafia do LLM

**Użycie:**
```bash
python tests/check_llm_input.py
```

**Co robi:**
- Testuje wyszukiwanie idiomów
- Buduje listę wiadomości przez `PromptService`
- Pokazuje strukturę promptów
- Analizuje skład wiadomości systemowych

**Przykład outputu:**
```
🔍 Sprawdzanie co trafia do LLM...
📤 Wyszukiwanie idiomów...
✅ Znaleziono 5 idiomów
📚 Idiom 1: 'IDIO_VECTOR_SEED _MEANING_VECTOR _IDIOM_TRACE...'

🎭 Budowanie listy wiadomości...
✅ Zbudowano 6 wiadomości

📝 Wiadomość 1 (system):
   Nazywasz się Eliora - pomocna, etyczna asystentka...

📝 Wiadomość 2 (system):
   Używaj kolorów w odpowiedziach: <color=#aabbcc>tekst</color>...
```

## 🎯 **Kiedy używać:**

### **`check_debug_logs.py`**
- ❌ Problemy z logowaniem
- ❌ Brak debug informacji
- ❌ Monitorowanie requestów

### **`check_llm_input.py`**
- ❌ Problemy z promptami
- ❌ Niepoprawne odpowiedzi LLM
- ❌ Debugowanie `PromptService`

### **`test_endpoint.py`**
- ❌ Problemy z API
- ❌ Testy endpointów FastAPI
- ❌ Weryfikacja odpowiedzi serwera

## 🔧 **Konfiguracja**

### Wymagania:
- FastAPI server uruchomiony na `localhost:8080`
- Qdrant database dostępna
- LM Studio uruchomiony

### Przed uruchomieniem:
```bash
# Uruchom FastAPI
python main_fastapi.py

# W osobnym terminalu uruchom narzędzie
python tests/check_debug_logs.py
```

## 📊 **Interpretacja Wyników**

### **Prawidłowe chunk:**
```python
{
    'facts': ['IDIO_VECTOR_SEED _MEANING_VECTOR...'],
    'metadata': {...},
    'score': 0.85
}
```

### **Prawidłowe wiadomości:**
- **System 1:** Osobowość Eliora
- **System 2:** Instrukcje kolorów
- **System 3:** Idiomy (konsolidowane)
- **System 4:** Kontekst z pamięci
- **User:** Wiadomość użytkownika

## 🚨 **Typowe Problemy**

### **Puste idiomy:**
```
⚠️ Idiom 1: pusty
```
**Rozwiązanie:** Sprawdź połączenie z Qdrant

### **Błąd request:**
```
❌ Request failed: Connection refused
```
**Rozwiązanie:** Uruchom FastAPI server

### **Niepoprawna struktura:**
```
⚠️ Idiom 1: nie jest dict
```
**Rozwiązanie:** Sprawdź `KnowledgeService`

## 📝 **Rozszerzanie**

Możesz dodać własne narzędzia debugowe:

```python
#!/usr/bin/env python3
"""
Custom debug tool
"""
import asyncio
from application.container import Container

async def custom_debug():
    container = Container()
    # Twój kod debugowy
    
if __name__ == "__main__":
    asyncio.run(custom_debug())
```

## 🎯 **Podsumowanie**

Te narzędzia są nieocenione dla:
- **Debugowania** problemów w czasie rzeczywistym
- **Analizy** struktury danych
- **Monitorowania** działania systemu
- **Optymalizacji** promptów i RAG

**Używaj ich regularnie podczas developmentu!** 🚀
