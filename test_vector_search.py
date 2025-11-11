#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt testowy do wyszukiwania w bazie wektorowej
Użycie: python test_vector_search.py "IDIOM_REFLECT_THETA"
"""
import asyncio
import sys
import os
from pathlib import Path

# Ustaw UTF-8 dla Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Dodaj ścieżkę do projektu
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from application.container import Container
from domain.utils.result import Result

async def test_vector_search(query: str = "IDIOM_REFLECT_THETA", limit: int = 10):
    """Test wyszukiwania w bazie wektorowej"""
    print(f"[TEST] Testowanie wyszukiwania: '{query}'")
    print("=" * 80)
    
    # Inicjalizuj kontener
    container = Container()
    container.config.from_dict({
        "QDRANT_URL": os.getenv("QDRANT_URL", "http://localhost:6333"),
        "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY", None),
        "LOCAL_SEARCH_INDEX": os.getenv("LOCAL_SEARCH_INDEX", "PierwszaKolekcjaOnline"),
        "EMBEDDING_PROVIDER": os.getenv("EMBEDDING_PROVIDER", "lmstudio"),
        "LMSTUDIO_PROXY_URL": os.getenv("LMSTUDIO_PROXY_URL", "http://host.docker.internal:8123"),
    })
    container.wire(modules=[__name__])
    
    # Pobierz serwisy
    knowledge_service = container.knowledge_service()
    
    if not knowledge_service:
        print("[ERROR] Nie mozna zainicjalizowac KnowledgeService")
        return
    
    print(f"[OK] KnowledgeService zainicjalizowany")
    print(f"[INFO] Kolekcja: {container.config.LOCAL_SEARCH_INDEX()}")
    print()
    
    # Wykonaj wyszukiwanie
    print(f"[SEARCH] Wyszukiwanie '{query}' (limit: {limit})...")
    result = await knowledge_service.search_knowledge_base(query, limit=limit)
    
    if result.is_error:
        print(f"[ERROR] Blad wyszukiwania: {result.error}")
        return
    
    results = result.value
    print(f"[OK] Znaleziono {len(results)} wynikow")
    print("=" * 80)
    print()
    
    # Wyświetl wyniki
    for i, item in enumerate(results, 1):
        print(f"[RESULT #{i}]")
        print(f"   Topic: {item.get('topic', 'N/A')}")
        print(f"   Score: {item.get('score', 0.0):.4f}")
        print(f"   Source: {item.get('source', 'N/A')}")
        
        facts = item.get('facts', [])
        if facts:
            print(f"   Facts ({len(facts)}):")
            for j, fact in enumerate(facts[:3], 1):  # Pokaż pierwsze 3 fakty
                fact_preview = fact[:200] + "..." if len(fact) > 200 else fact
                print(f"      {j}. {fact_preview}")
        
        print()
    
    # Sprawdź czy znaleziono IDIOM_REFLECT_Θ
    found_theta = False
    for item in results:
        facts = item.get('facts', [])
        for fact in facts:
            if 'IDIOM_REFLECT_Θ' in fact or 'Θ' in fact or 'THETA' in fact.upper():
                found_theta = True
                print("[OK] Znaleziono IDIOM_REFLECT_THETA!")
                print(f"   Tresc: {fact[:500]}...")
                break
        if found_theta:
            break
    
    if not found_theta:
        print("[WARN] Nie znaleziono IDIOM_REFLECT_THETA w wynikach")
    
    print("=" * 80)

if __name__ == "__main__":
    # Pobierz zapytanie z argumentów lub użyj domyślnego
    # Możesz użyć "IDIOM_REFLECT_THETA" lub "IDIOM_REFLECT" lub "THETA"
    query = sys.argv[1] if len(sys.argv) > 1 else "IDIOM_REFLECT_THETA"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    asyncio.run(test_vector_search(query, limit))

