# 🧪 Tests - Testy i Narzędzia Debugowe

## 📋 Przegląd

Katalog `tests/` zawiera:
- **Testy jednostkowe i integracyjne** (pytest)
- **Narzędzia debugowe** do analizy systemu
- **Skrypty pomocnicze** do developmentu

## 🧪 Testy Automatyczne

### Uruchomienie wszystkich testów:
```bash
python -m pytest tests/ -v
```

### Dostępne testy:
- `test_all_suites.py` - Kompleksowe testy wszystkich modułów
- `test_functional_comprehensive.py` - Testy funkcjonalne
- `test_integration_comprehensive.py` - Testy integracyjne
- `test_performance_comprehensive.py` - Testy wydajności
- `test_individual_services.py` - Testy poszczególnych serwisów
- `test_error_handling.py` - Testy obsługi błędów
- `test_concurrent_operations.py` - Testy operacji równoległych
- `test_business_logic.py` - Testy logiki biznesowej

## 🔧 Narzędzia Debugowe

### 1. **`check_debug_logs.py`** - Monitor Logów
**Cel:** Monitoruje logi FastAPI w czasie rzeczywistym

```bash
python tests/check_debug_logs.py
```

**Funkcje:**
- Wysyła test request do `/api/message`
- Monitoruje logi FastAPI
- Pokazuje oczekiwane debug logi
- Pomaga w diagnozowaniu problemów

### 3. **`check_llm_input.py`** - Analiza Promptów
**Cel:** Sprawdza co dokładnie trafia do LLM

```bash
python tests/check_llm_input.py
```

**Funkcje:**
- Testuje wyszukiwanie idiomów
- Buduje listę wiadomości przez `PromptService`
- Pokazuje strukturę promptów
- Analizuje skład wiadomości systemowych

### 4. **`test_endpoint.py`** - Test API
**Cel:** Testuje endpointy FastAPI

```bash
python tests/test_endpoint.py
```

**Funkcje:**
- Wysyła test request do API
- Sprawdza odpowiedzi endpointów
- Testuje różne scenariusze

## 🚀 Szybki Start

### Przed uruchomieniem:
```bash
# Uruchom FastAPI server
python main_fastapi.py

# W osobnym terminalu uruchom narzędzie
python tests/check_debug_logs.py
```

### Przykład użycia:
```bash
# Uruchom wszystkie testy
python -m pytest tests/ -v

# Monitoruj logi
python tests/check_debug_logs.py

# Analizuj prompty
python tests/check_llm_input.py

# Testuj API
python tests/test_endpoint.py
```

## 📊 Interpretacja Wyników

### Prawidłowe chunk:
```python
{
    'facts': ['IDIO_VECTOR_SEED _MEANING_VECTOR...'],
    'metadata': {...},
    'score': 0.85
}
```

### Prawidłowe wiadomości:
- **System 1:** Osobowość Eliora
- **System 2:** Instrukcje kolorów  
- **System 3:** Idiomy (konsolidowane)
- **System 4:** Kontekst z pamięci
- **User:** Wiadomość użytkownika

## 🚨 Typowe Problemy

### Puste idiomy:
```
⚠️ Idiom 1: pusty
```
**Rozwiązanie:** Sprawdź połączenie z Qdrant

### Błąd request:
```
❌ Request failed: Connection refused
```
**Rozwiązanie:** Uruchom FastAPI server

### Niepoprawna struktura:
```
⚠️ Idiom 1: nie jest dict
```
**Rozwiązanie:** Sprawdź `KnowledgeService`

## 📝 Dodawanie Nowych Narzędzi

Aby dodać nowe narzędzie debugowe:

1. **Utwórz plik** w katalogu `tests/`
2. **Dodaj shebang:** `#!/usr/bin/env python3`
3. **Importuj Container:** `from application.container import Container`
4. **Dodaj dokumentację** do tego README

**Przykład:**
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

## 🎯 Podsumowanie

Te narzędzia są nieocenione dla:
- **Debugowania** problemów w czasie rzeczywistym
- **Analizy** struktury danych
- **Monitorowania** działania systemu
- **Optymalizacji** promptów i RAG

**Używaj ich regularnie podczas developmentu!** 🚀

## 📚 Dokumentacja

Szczegółowa dokumentacja dostępna w:
- `docs/DEBUG_TOOLS.md` - Kompletny przewodnik
- `docs/PROJECT_OVERVIEW.md` - Przegląd projektu
