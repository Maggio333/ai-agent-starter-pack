#!/usr/bin/env python3
"""Test nowego limitu znaków w search_knowledge_base"""

import sys
import os
sys.path.append('.')

import asyncio
from application.services.di_service import DIService

async def test_character_limit():
    print('Testing new character limit (2000 chars)...')
    print('=' * 60)
    
    # Initialize DI Service
    di_service = DIService()
    knowledge_service = di_service.get_knowledge_service()
    
    # Test 1: Query w granicach nowego limitu (1500 znaków)
    print('Test 1: Query within new limit (1500 chars)...')
    medium_query = "A" * 1500
    result1 = await knowledge_service.search_knowledge_base(medium_query)
    print(f'Result: {"SUCCESS" if result1.is_success else "ERROR"}')
    if result1.is_error:
        print(f'Error: {result1.error}')
    
    # Test 2: Query przekraczający nowy limit (2500 znaków)
    print('\nTest 2: Query exceeding new limit (2500 chars)...')
    long_query = "A" * 2500
    result2 = await knowledge_service.search_knowledge_base(long_query)
    print(f'Result: {"SUCCESS" if result2.is_success else "ERROR"}')
    if result2.is_error:
        print(f'Error: {result2.error}')
    
    # Test 3: Query z Twoimi operatorami (sprawdzimy długość)
    print('\nTest 3: Your operators query...')
    operators_query = """⨁       # Operator sumy idiomatycznej (łączenie idiomów)
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
    
    print(f'Query length: {len(operators_query)} characters')
    result3 = await knowledge_service.search_knowledge_base(operators_query)
    print(f'Result: {"SUCCESS" if result3.is_success else "ERROR"}')
    if result3.is_error:
        print(f'Error: {result3.error}')
    elif result3.is_success:
        print(f'Found {len(result3.value)} results')
        for i, result in enumerate(result3.value[:3]):  # Show first 3 results
            print(f'  {i+1}. Score: {result["score"]:.4f}, Facts: {len(result["facts"])}')
    
    print('\nCharacter limit test completed!')
    print('=' * 60)

if __name__ == "__main__":
    asyncio.run(test_character_limit())
