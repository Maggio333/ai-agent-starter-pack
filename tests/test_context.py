#!/usr/bin/env python3
"""
Test kontekstu - sprawdza jak SystemPromptsService integruje się z PromptService
i jak kontekst trafia do LLM
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.services.SystemPromptsService import SystemPromptsService
from application.services.prompt_service import PromptService
from domain.entities.chat_message import ChatMessage, MessageRole
from datetime import datetime

def test_context():
    """Test czy kontekst budowany przez PromptService jest prawidłowy"""
    
    print("=" * 60)
    print("Test Kontekstu - SystemPromptsService + PromptService")
    print("=" * 60)
    
    # 1. Utworz serwisy
    system_prompts = SystemPromptsService()
    prompt_service = PromptService(system_prompts_service=system_prompts)
    
    print("\n[OK] Utworzono serwisy")
    
    # 2. Sprawdź globalne prompty
    print("\n" + "-" * 60)
    print("1. TEST GLOBALNYCH PROMPTÓW:")
    print("-" * 60)
    
    global_prompts = prompt_service.get_global_system_prompts()
    print(f"\nLiczba globalnych promptów: {len(global_prompts)}")
    
    for i, msg in enumerate(global_prompts, 1):
        print(f"\n  Prompt {i}:")
        print(f"    Role: {msg.role.value}")
        print(f"    Długość: {len(msg.content)} znaków")
        print(f"    Preview: {msg.content[:80]}...")
    
    # 3. Sprawdź dodatkowe prompty
    print("\n" + "-" * 60)
    print("2. TEST DODATKOWYCH PROMPTÓW:")
    print("-" * 60)
    
    additional_prompts = prompt_service.get_additional_system_prompts()
    print(f"\nLiczba dodatkowych promptów: {len(additional_prompts)}")
    
    for i, msg in enumerate(additional_prompts, 1):
        print(f"\n  Prompt {i}:")
        print(f"    Role: {msg.role.value}")
        print(f"    Długość: {len(msg.content)} znaków")
        print(f"    Preview: {msg.content[:80]}...")
    
    # 4. Test budowania kompletnej listy wiadomości
    print("\n" + "-" * 60)
    print("3. TEST KOMPLETNEJ LISTY WIADOMOŚCI:")
    print("-" * 60)
    
    # Mock idiomy
    idioms = [
        "Test idiom 1: myślenie refleksyjne",
        "Test idiom 2: analiza kontekstu"
    ]
    
    # Mock historia rozmowy
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
    
    # Buduj kompletną listę
    messages = prompt_service.build_complete_message_list(
        user_message="Test wiadomość",
        idioms=idioms,
        conversation_history=conversation_history
    )
    
    print(f"\nCałkowita liczba wiadomości: {len(messages)}")
    print(f"\nStruktura kontekstu:")
    
    system_msgs = [m for m in messages if m.role == MessageRole.SYSTEM]
    user_msgs = [m for m in messages if m.role == MessageRole.USER]
    assistant_msgs = [m for m in messages if m.role == MessageRole.ASSISTANT]
    
    print(f"  - System messages: {len(system_msgs)}")
    print(f"  - User messages: {len(user_msgs)}")
    print(f"  - Assistant messages: {len(assistant_msgs)}")
    
    # 5. Szczegółowy przegląd kontekstu
    print("\n" + "-" * 60)
    print("4. SZCZEGÓŁOWY KONTEKST:")
    print("-" * 60)
    
    for i, msg in enumerate(messages, 1):
        print(f"\nWiadomość {i}:")
        print(f"  Role: {msg.role.value}")
        print(f"  Długość: {len(msg.content)} znaków")
        
        if msg.role == MessageRole.SYSTEM:
            # Sprawdź czy to jeden z naszych promptów
            content_preview = msg.content[:100]
            if "Eliora" in content_preview:
                print(f"  Typ: Osobowość Eliora")
            elif "<color=" in content_preview:
                print(f"  Typ: Formatowanie kolorów")
            elif "dodatkową rolę" in content_preview or "rozpoznawczy" in content_preview:
                print(f"  Typ: Rola konwersacyjna")
            elif "refleksyjne myślenie" in content_preview:
                print(f"  Typ: Idiomy refleksyjne")
                print(f"  Idiomy: {msg.content.count('idiom')} wystąpień")
            else:
                print(f"  Typ: Inny prompt")
                print(f"  Preview: {content_preview}...")
        else:
            print(f"  Preview: {msg.content[:80]}...")
    
    # 6. Statystyki kontekstu
    print("\n" + "-" * 60)
    print("5. STATYSTYKI KONTEKSTU:")
    print("-" * 60)
    
    total_chars = sum(len(m.content) for m in messages)
    total_tokens_approx = total_chars // 4  # Średnio 1 token = 4 znaki
    
    print(f"\nCałkowita długość: {total_chars:,} znaków")
    print(f"Przybliżona liczba tokenów: {total_tokens_approx:,}")
    
    breakdown = {
        "System (Eliora personality)": 0,
        "System (Colors)": 0,
        "System (Role)": 0,
        "System (Idioms)": 0,
        "User": 0,
        "Assistant": 0
    }
    
    for msg in messages:
        if msg.role == MessageRole.SYSTEM:
            if "Eliora" in msg.content:
                breakdown["System (Eliora personality)"] += len(msg.content)
            elif "<color=" in msg.content:
                breakdown["System (Colors)"] += len(msg.content)
            elif "dodatkową rolę" in msg.content or "rozpoznawczy" in msg.content:
                breakdown["System (Role)"] += len(msg.content)
            elif "refleksyjne myślenie" in msg.content:
                breakdown["System (Idioms)"] += len(msg.content)
        elif msg.role == MessageRole.USER:
            breakdown["User"] += len(msg.content)
        elif msg.role == MessageRole.ASSISTANT:
            breakdown["Assistant"] += len(msg.content)
    
    print(f"\nPodział kontekstu:")
    for category, length in breakdown.items():
        percentage = (length / total_chars * 100) if total_chars > 0 else 0
        print(f"  {category}: {length:,} znaków ({percentage:.1f}%)")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Test kontekstu zakończony pomyślnie!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        test_context()
    except Exception as e:
        print(f"\n[ERROR] Test nieudany: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

