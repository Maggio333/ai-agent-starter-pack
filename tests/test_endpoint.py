#!/usr/bin/env python3
"""
Prosty skrypt do testowania endpointu /api/message
"""
import requests
import json

def test_message_endpoint():
    """Testuje endpoint wiadomości"""
    url = "http://localhost:8080/api/message"
    
    # Testowa wiadomość
    data = {
        "message": "Cześć! Jak się masz?"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 Wysyłanie wiadomości do FastAPI...")
        print(f"📤 Wiadomość: {data['message']}")
        print(f"🌐 URL: {url}")
        
        response = requests.post(url, json=data, headers=headers, timeout=120)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sukces!")
            print(f"📝 Odpowiedź: {result.get('response', 'Brak odpowiedzi')}")
            print(f"🆔 Session ID: {result.get('session_id', 'Brak')}")
            print(f"🔧 Service Used: {result.get('service_used', 'Brak')}")
            print(f"📚 Idioms Used: {result.get('idioms_used', False)}")
            print(f"🧠 Dynamic RAG: {result.get('dynamic_rag_performed', False)}")
            print(f"📊 Vector Results: {result.get('dynamic_vector_results_count', 0)}")
            print(f"💬 Conversation Length: {result.get('conversation_length', 0)}")
        else:
            print(f"❌ Błąd: {response.status_code}")
            print(f"📄 Treść błędu: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - FastAPI potrzebuje więcej czasu na przetwarzanie (120s)")
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd połączenia: {e}")
    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    test_message_endpoint()
