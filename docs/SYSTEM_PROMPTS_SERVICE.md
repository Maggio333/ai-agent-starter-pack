# SystemPromptsService - Centralne Repozytorium Stringów RAG

## 📋 Przegląd

`SystemPromptsService` to centralny serwis w warstwie Domain, który przechowuje **wszystkie hardcoded stringi** używane w systemie RAG. Zapewnia spójność i łatwość w zarządzaniu tekstami używanymi do konfiguracji osobowości Eliora, formatowania i innych funkcji.

## 🎯 Cel

Wzorowany na `ChatElioraSystem.Core.Domain.Resources.RAGPromptsGeneral` z architektury C#, ten serwis:
- ✅ Eliminuje duplikację hardcoded stringów
- ✅ Zapewnia jedną lokalizację dla wszystkich tekstów RAG
- ✅ Umożliwia łatwą zmianę konfiguracji
- ✅ Przestrzega Clean Architecture (Domain layer)

## 📦 Dostępne Prompty

### 1. Osobowość Eliora

```python
service.eliora_personality_prompt
# Zwraca: Główny prompt osobowości Eliora
```

### 2. Formatowanie Kolorów

```python
service.color_syntax_prompt          # Prosta wersja
service.color_syntax_prompt_extended # Z przykładami
```

### 3. Role Konwersacyjne

```python
service.general_conversation_role    # Rola rozpoznawcza
service.admin_role_prompt           # Uprawnienia admina
```

### 4. Idiomy Refleksyjne

```python
service.get_idioms_prompt(combined_idioms: str)
# Generuje prompt z idiomami
```

### 5. Profile Użytkownika

```python
service.get_user_profile_prompt(user_context: dict)
# Generuje prompt na podstawie kontekstu
```

## 🎨 Obsługa Emotek

### Lista Dozwolonych Emotek

```python
service.allowed_emojis
# Zwraca: ["😊", "😄", "😃", "😉", "😍", "🤔", "💭", "✨", "🌟", "💫", ...]
```

### Wytyczne Używania

```python
service.emoji_usage_guidelines
# Zwraca tekst z wytycznymi do używania emotek
```

## 🔧 Użycie

### Podstawowe

```python
from domain.services.SystemPromptsService import SystemPromptsService

# Tworzenie serwisu
prompts = SystemPromptsService()

# Pobieranie promptów
personality = prompts.eliora_personality_prompt
colors = prompts.color_syntax_prompt
```

### W PromptService

```python
from domain.services.SystemPromptsService import SystemPromptsService

class PromptService:
    def __init__(self, system_prompts_service: Optional[SystemPromptsService] = None):
        self.system_prompts = system_prompts_service or SystemPromptsService()
    
    def get_global_system_prompts(self, user_context: Optional[dict] = None):
        prompts = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.system_prompts.eliora_personality_prompt,
                timestamp=datetime.now()
            ),
            # ...
        ]
```

### Kompletna Konfiguracja RAG

```python
# Pobranie całej konfiguracji
config = service.get_rag_configuration()
# Zwraca zorganizowany słownik ze wszystkimi stringami

# Pobranie wszystkich hardcoded stringów
all_strings = service.get_all_hardcoded_strings()
```

## 📊 Statystyki

```python
stats = service.get_prompt_stats()
# Zwraca:
# {
#     'total_chars': int,
#     'personality_length': int,
#     'color_length': int,
#     'role_length': int,
#     'available_prompts': List[str]
# }
```

## 🧪 Testowanie

Uruchom test serwisu:
```bash
python tests/test_system_prompts.py
```

## 🔄 Refaktoryzacja

### Przed (hardcoded w PromptService):

```python
content="Nazywasz się Eliora - pomocna, etyczna asystentka..."
content="Używaj kolorów w odpowiedziach: <color=#aabbcc>tekst</color>"
```

### Po (użycie SystemPromptsService):

```python
content=self.system_prompts.eliora_personality_prompt
content=self.system_prompts.color_syntax_prompt
```

## 🚀 Rozszerzenia

### Dodanie Nowego Promptu

1. Dodaj property w `SystemPromptsService`:
```python
@property
def new_feature_prompt(self) -> str:
    return "Twój nowy prompt..."
```

2. Dodaj do metod pomocniczych:
```python
def _get_all_public_methods(self) -> List[str]:
    return [
        # ...
        'new_feature_prompt',
    ]
```

### Dodanie Obsługi Emotek

```python
# Sprawdź czy emotka jest dozwolona
if emoji in service.allowed_emojis:
    # Użyj emotki
    pass
```

## 📁 Lokalizacja

```
domain/services/SystemPromptsService.py
```

## 🎓 Architektura

```
Domain Layer
└── services/
    └── SystemPromptsService.py  ← Centralne repozytorium stringów

Application Layer
└── services/
    └── PromptService.py         ← Używa SystemPromptsService
```

## 💡 Zalety

1. **Single Source of Truth** - jedna lokalizacja dla wszystkich stringów
2. **Testowalność** - łatwe testowanie zmian promptów
3. **Maintainability** - łatwa zmiana bez modyfikacji kodu biznesowego
4. **Spójność** - gwarancja użycia tych samych stringów wszędzie
5. **Eksport** - możliwość eksportu wszystkich stringów do analizy

## 🔗 Związane Pliki

- `application/services/prompt_service.py` - używa SystemPromptsService
- `domain/services/IKnowledgeService.py` - przykład struktury interfejsu
- `LLM_CONTEXT.md` - pokazuje jak prompty trafiają do LLM

## 📝 TODO

- [ ] Dodanie obsługi różnych języków
- [ ] Cache dla często używanych promptów
- [ ] Interfejs ISystemPromptsService dla testowania
- [ ] Walidacja poprawności stringów
- [ ] Export do plików konfiguracyjnych (YAML/JSON)

