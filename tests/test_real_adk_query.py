#!/usr/bin/env python3
"""Test prawdziwego zapytania z ADK - Unicode + długie zapytania"""

import sys
import os
sys.path.append('.')

import asyncio
from application.services.di_service import DIService

async def test_real_adk_query():
    print('Testing Real ADK Query with Unicode and Long Text...')
    print('=' * 70)
    
    # Initialize DI Service
    di_service = DIService()
    knowledge_service = di_service.get_knowledge_service()
    
    # Test 1: Twoje operatory (które wcześniej nie działały)
    print('Test 1: Twoje operatory Unicode...')
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
    result1 = await knowledge_service.search_knowledge_base(operators_query)
    
    if result1.is_success:
        print(f'SUCCESS! Found {len(result1.value)} results')
        for i, result in enumerate(result1.value[:3]):
            print(f'  {i+1}. Score: {result["score"]:.4f}')
            print(f'     Facts: {result["facts"][0][:100]}...')
    else:
        print(f'ERROR: {result1.error}')
    
    # Test 2: Długie zapytanie (blisko limitu 2000)
    print('\nTest 2: Long query near 2000 char limit...')
    long_query = """
    Analiza semantyczna idiomów matematycznych w kontekście sztucznej inteligencji.
    Badanie wzorców językowych i ich reprezentacji wektorowych w przestrzeni Hilberta.
    Implementacja algorytmów machine learning dla rozpoznawania idiomów osobowościowych.
    Integracja z bazami danych wektorowych Qdrant dla efektywnego wyszukiwania semantycznego.
    Optymalizacja embeddingów dla lepszego zrozumienia kontekstu i intencji użytkownika.
    Rozwój systemów RAG (Retrieval-Augmented Generation) dla zaawansowanych chatbotów.
    Implementacja wzorców ROP (Railway Oriented Programming) dla niezawodności systemu.
    Architektura mikroserwisów z Dependency Injection dla skalowalności aplikacji.
    Testowanie wydajności i niezawodności systemów AI w środowisku produkcyjnym.
    Monitoring i observability dla systemów sztucznej inteligencji.
    Bezpieczeństwo danych i prywatność w systemach AI.
    Etyka sztucznej inteligencji i odpowiedzialne AI.
    """ * 3  # Powtórz 3 razy żeby zbliżyć się do limitu
    
    print(f'Query length: {len(long_query)} characters')
    result2 = await knowledge_service.search_knowledge_base(long_query)
    
    if result2.is_success:
        print(f'SUCCESS! Found {len(result2.value)} results')
        for i, result in enumerate(result2.value[:2]):
            print(f'  {i+1}. Score: {result["score"]:.4f}')
            print(f'     Facts: {result["facts"][0][:80]}...')
    else:
        print(f'ERROR: {result2.error}')
    
    # Test 3: Zapytanie przekraczające limit
    print('\nTest 3: Query exceeding 2000 char limit...')
    too_long_query = "A" * 2500
    print(f'Query length: {len(too_long_query)} characters')
    result3 = await knowledge_service.search_knowledge_base(too_long_query)
    
    if result3.is_error:
        print(f'CORRECTLY REJECTED: {result3.error}')
    else:
        print(f'UNEXPECTED: Should have been rejected!')
    
    # Test 4: Mieszane zapytanie (Unicode + długi tekst)
    print('\nTest 4: Mixed Unicode + Long Text...')
    mixed_query = """
    🔍 Analiza semantyczna idiomów matematycznych ⨁ Φ Ψ Ξ Σ Θ Ω
    Implementacja systemów AI z wykorzystaniem wzorców ROP
    Integracja z bazami wektorowymi Qdrant dla efektywnego wyszukiwania
    Optymalizacja embeddingów dla lepszego zrozumienia kontekstu
    Rozwój systemów RAG (Retrieval-Augmented Generation)
    Architektura mikroserwisów z Dependency Injection
    Testowanie wydajności i niezawodności systemów AI
    Monitoring i observability dla systemów sztucznej inteligencji
    Bezpieczeństwo danych i prywatność w systemach AI
    Etyka sztucznej inteligencji i odpowiedzialne AI
    """ * 2
    
    print(f'Query length: {len(mixed_query)} characters')
    result4 = await knowledge_service.search_knowledge_base(mixed_query)
    
    if result4.is_success:
        print(f'SUCCESS! Found {len(result4.value)} results')
        for i, result in enumerate(result4.value[:2]):
            print(f'  {i+1}. Score: {result["score"]:.4f}')
            print(f'     Facts: {result["facts"][0][:80]}...')
    else:
        print(f'ERROR: {result4.error}')
    
    print('\nReal ADK Query Test Completed!')
    print('=' * 70)

if __name__ == "__main__":
    asyncio.run(test_real_adk_query())
