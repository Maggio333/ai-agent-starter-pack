#!/usr/bin/env python3
"""
Test dla SystemPromptsService - sprawdza czy wszystkie prompty są dostępne
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.services.SystemPromptsService import SystemPromptsService

def test_system_prompts():
    """Test czy SystemPromptsService działa poprawnie"""
    
    print("=" * 60)
    print("Test SystemPromptsService")
    print("=" * 60)
    
    # 1. Tworzenie instancji
    service = SystemPromptsService()
    print("\n[OK] Utworzono instancję SystemPromptsService")
    
    # 2. Sprawdzenie wszystkich dostępnych promptów
    print("\n" + "-" * 60)
    print("DOSTEPNE PROMPTY:")
    print("-" * 60)
    
    prompts = service.get_all_system_prompts()
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{i}. {prompt['name']}")
        print(f"   Dlugosc: {len(prompt['content'])} znakow")
        print(f"   Przewidyw: {prompt['content'][:80]}...")
    
    # 3. Test wszystkich właściwości
    print("\n" + "-" * 60)
    print("TEST WSZYSTKICH WLASCIWOSCI:")
    print("-" * 60)
    
    tests = [
        ("eliora_personality_prompt", service.eliora_personality_prompt),
        ("color_syntax_prompt", service.color_syntax_prompt),
        ("color_syntax_prompt_extended", service.color_syntax_prompt_extended),
        ("general_conversation_role", service.general_conversation_role),
        ("admin_role_prompt", service.admin_role_prompt),
    ]
    
    for name, value in tests:
        assert value is not None, f"{name} jest None"
        assert len(value) > 0, f"{name} jest pusty"
        print(f"[OK] {name}: {len(value)} znakow")
    
    # 4. Test metody get_idioms_prompt
    print("\n" + "-" * 60)
    print("TEST METODY get_idioms_prompt:")
    print("-" * 60)
    
    test_idioms = "Idiom 1\nIdiom 2\nIdiom 3"
    idioms_prompt = service.get_idioms_prompt(test_idioms)
    assert "refleksyjne myślenie" in idioms_prompt.lower()
    assert "Idiom 1" in idioms_prompt
    print(f"[OK] get_idioms_prompt: {len(idioms_prompt)} znakow")
    
    # 5. Test statystyk
    print("\n" + "-" * 60)
    print("STATYSTYKI:")
    print("-" * 60)
    
    stats = service.get_prompt_stats()
    print(f"Calkowita dlugosc: {stats['total_chars']} znakow")
    print(f"Dostepne prompty: {len(stats['available_prompts'])}")
    for prompt_name in stats['available_prompts']:
        print(f"  - {prompt_name}")
    
    # 6. Test z kontekstem użytkownika
    print("\n" + "-" * 60)
    print("TEST Z KONTEKSTEM UZYTKOWNIKA:")
    print("-" * 60)
    
    user_context = {'role': 'admin'}
    profile_prompt = service.get_user_profile_prompt(user_context)
    assert user_context['role'] in profile_prompt
    print(f"[OK] get_user_profile_prompt: {profile_prompt}")
    
    # Test z adminem
    all_prompts_with_admin = service.get_all_system_prompts(user_context=user_context, include_admin=True)
    assert len(all_prompts_with_admin) > len(prompts)
    print(f"[OK] Przy admin: {len(all_prompts_with_admin)} promptow (bez admin: {len(prompts)})")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Wszystkie testy przeszły pomyslnie!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        test_system_prompts()
    except Exception as e:
        print(f"\n[ERROR] Test nieudany: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

