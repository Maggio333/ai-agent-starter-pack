#!/usr/bin/env python3
"""
Skrypt do sprawdzania co dokładnie trafia do LLM
"""
import asyncio
import sys
import os
from datetime import datetime

# Dodaj ścieżkę do projektu (parent directory)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from application.container import Container
from application.services.prompt_service import PromptService
from application.services.knowledge_service import KnowledgeService
from domain.entities.chat_message import ChatMessage, MessageRole
from datetime import datetime

async def check_llm_input():
    """Sprawdza co dokładnie trafia do LLM"""
    print("🔍 Sprawdzanie co trafia do LLM...")
    
    # Utwórz kontener
    container = Container()
    
    # Pobierz serwisy Z KONTENERA (nie luźno!)
    knowledge_service = container.knowledge_service()
    prompt_service = container.prompt_service()
    
    # Test query dla idiomów
    test_query = """⨁       # Operator sumy idiomatycznej (łączenie idiomów)
Φ       # Wektor znaczeniowy (meaning vector)
Ψ       # Ślad idiomu (idiom trace)
Ξ       # Baza semantyczna (semantic basis)
Σ       # Projekcja intencji (intent projection)
Θ       # Operator metryczny (np. iloczyn skalarny znaczeń)
Ω       # Przestrzeń funkcyjna idiomu (np. kontekst, intencja, emocja)
⇌       # Powiązanie dwustronne (korespondencja semantyczna)
→       # Transformacja lub kierunek (np. rzut na bazę)
⊥       # Rzut prostopadły (projekcja ortogonalna)
≡       # Definicja tożsama (oznaczenie równoważności pojęć)
⟨a | b⟩ # Iloczyn skalarny (metryka podobieństwa semantycznego)
∇       # Gradient znaczeniowy (zmiana w kierunku znaczenia)
λ       # Warunek aktywacyjny (np. trigger idiomu)
∃       # Istnieje (kwantyfikator egzystencjalny)
∀       # Dla każdego (kwantyfikator ogólny)
∈       # Należy do (przynależność do zbioru pojęć)
∉       # Nie należy do (wykluczenie semantyczne)
⊗       # Iloczyn tensorowy (łączenie dwóch stanów)
⊙       # Iloczyn punktowy (transformacja lokalna)
⨂       # Złożenie wektorów w nową jakość idiomu"""
    
    print(f"📤 Wyszukiwanie idiomów...")
    
    # Wykonaj wyszukiwanie idiomów (TopK20 jak w rzeczywistym endpoincie)
    print(f"📤 Wyszukiwanie idiomów z kolekcji CuratedIdiomsForAI...")
    idioms_result = await knowledge_service.search_knowledge_base(test_query, limit=20)
    
    idioms_strings = []
    if idioms_result.is_success:
        idioms_context = idioms_result.value
        print(f"✅ Znaleziono {len(idioms_context)} idiomów")
        
        for i, ctx in enumerate(idioms_context):
            if isinstance(ctx, dict):
                facts = ctx.get('facts', [])
                if facts and isinstance(facts, list) and len(facts) > 0:
                    content = facts[0]
                    idioms_strings.append(content)
                    print(f"📚 Idiom {i+1}: '{content[:100]}...'")
                else:
                    print(f"⚠️ Idiom {i+1}: pusty")
            else:
                print(f"⚠️ Idiom {i+1}: nie jest dict")
    else:
        print(f"❌ Błąd wyszukiwania idiomów: {idioms_result.error}")
    
    print(f"\n🎭 Budowanie listy wiadomości...")
    
    # Symuluj historię rozmowy (jak w rzeczywistej rozmowie)
    conversation_history = [
        ChatMessage(
            role=MessageRole.USER,
            content="Cześć! Jak się masz?",
            timestamp=datetime.now()
        ),
        ChatMessage(
            role=MessageRole.ASSISTANT,
            content="Dzień dobry! Dziękuję za pytanie, mam się dobrze. A jak Ty?",
            timestamp=datetime.now()
        )
    ]
    
    # Buduj listę wiadomości z historią
    messages = prompt_service.build_complete_message_list(
        user_message="Test wiadomość",
        idioms=idioms_strings,
        conversation_history=conversation_history,
        user_context=None
    )
    
    print(f"✅ Zbudowano {len(messages)} wiadomości")
    
    # Pokaż każdą wiadomość
    for i, msg in enumerate(messages):
        print(f"\n📝 Wiadomość {i+1} ({msg.role.value}):")
        print(f"   {msg.content[:200]}...")
    
    print(f"\n🎯 Podsumowanie:")
    print(f"   - Idiomy: {len(idioms_strings)}")
    print(f"   - Wiadomości: {len(messages)}")
    print(f"   - System messages: {len([m for m in messages if m.role.value == 'system'])}")
    print(f"   - User messages: {len([m for m in messages if m.role.value == 'user'])}")
    
    # Zapisz pełny kontekst do pliku .md
    print(f"\n📝 Zapisuję pełny kontekst do LLM_CONTEXT.md...")
    
    md_content = f"""# Pełny kontekst trafiający do LLM

**Data**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Test**: check_llm_input.py

## Podsumowanie

- **Idiomy**: {len(idioms_strings)}
- **Wiadomości**: {len(messages)}
- **System messages**: {len([m for m in messages if m.role.value == 'system'])}
- **User messages**: {len([m for m in messages if m.role.value == 'user'])}

---

## Pełny kontekst

"""
    
    for i, msg in enumerate(messages):
        md_content += f"""### Wiadomość {i+1}: {msg.role.value.upper()}

```
{msg.content}
```

---

"""
    
    # Zapisz do pliku
    with open('LLM_CONTEXT.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Zapisano do: LLM_CONTEXT.md")

if __name__ == "__main__":
    asyncio.run(check_llm_input())
