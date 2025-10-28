#!/usr/bin/env python3
"""
Test Dynamic RAG - sprawdza czy DynamicRAGService działa i generuje zapytania
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.container import Container
from application.services.dynamic_rag_service import DynamicRAGService
from domain.entities.chat_message import ChatMessage, MessageRole
from datetime import datetime

async def test_dynamic_rag():
    """Test czy DynamicRAGService generuje zapytania"""
    
    print("=" * 60)
    print("Test Dynamic RAG")
    print("=" * 60)
    
    # Utwórz kontener
    container = Container()
    dynamic_rag_service = container.dynamic_rag_service()
    
    print("\n[OK] Utworzono DynamicRAGService z kontenera")
    
    # Test query
    conversation_history = [
        ChatMessage(
            role=MessageRole.USER,
            content="Cześć! Co to jest sztuczna inteligencja?",
            timestamp=datetime.now()
        ),
        ChatMessage(
            role=MessageRole.ASSISTANT,
            content="Sztuczna inteligencja to dziedzina informatyki zajmująca się tworzeniem systemów, które mogą wykonywać zadania wymagające ludzkiej inteligencji.",
            timestamp=datetime.now()
        )
    ]
    
    current_message = "Opowiedz mi więcej o machine learning"
    
    print("\n" + "-" * 60)
    print("ROZMOWA:")
    print("-" * 60)
    print(f"Historia: {len(conversation_history)} wiadomości")
    print(f"Obecna wiadomość: {current_message}")
    
    # Wywołaj Dynamic RAG
    print("\n" + "-" * 60)
    print("WYZWOLANIE DYNAMIC RAG:")
    print("-" * 60)
    
    result = await dynamic_rag_service.decide_vector_query(
        conversation_context=conversation_history,
        current_message=current_message,
        user_context=None
    )
    
    if result.is_success:
        print(f"\n✅ Dynamic RAG zwrócił query:")
        print(f"   {result.value}")
        
        # Pokazuj strukturę
        if isinstance(result.value, dict):
            print(f"\n📊 Struktura JSON:")
            for key, value in result.value.items():
                print(f"   {key}: {str(value)[:100]}...")
        
        # TEST: Wyszukaj w bazie wektorowej używając query
        print(f"\n" + "-" * 60)
        print("WYSZUKIWANIE W BAZIE WEKTOROWEJ:")
        print("-" * 60)
        
        query = result.value if isinstance(result.value, str) else str(result.value)
        
        search_result = await dynamic_rag_service.search_with_filtering(
            query=query,
            score_threshold=0.85,
            limit=5
        )
        
        if search_result.is_success:
            print(f"\n✅ Znaleziono {len(search_result.value)} wyników")
            
            for i, rag_item in enumerate(search_result.value, 1):
                print(f"\n📄 Wynik {i}:")
                if isinstance(rag_item, dict):
                    print(f"   Score: {rag_item.get('score', 'N/A')}")
                    print(f"   Topic: {rag_item.get('topic', 'N/A')}")
                    facts = rag_item.get('facts', [])
                    if facts:
                        print(f"   Treść: {facts[0][:100]}...")
                else:
                    print(f"   {str(rag_item)[:100]}...")
        else:
            print(f"\n❌ Wyszukiwanie nie powiodło się: {search_result.error}")
    else:
        print(f"\n❌ Dynamic RAG błąd: {result.error}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Test Dynamic RAG zakończony!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        asyncio.run(test_dynamic_rag())
    except Exception as e:
        print(f"\n[ERROR] Test nieudany: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

