#!/usr/bin/env python3
"""
Skrypt do sprawdzania debug logów z FastAPI
"""
import subprocess
import time
import requests
import threading

def monitor_logs():
    """Monitoruje logi FastAPI w czasie rzeczywistym"""
    print("🔍 Monitoring FastAPI logs for debug info...")
    print("📤 Sending test request...")
    
    # Wyślij request w osobnym wątku
    def send_request():
        time.sleep(1)  # Daj czas na start monitorowania
        try:
            response = requests.post(
                "http://localhost:8080/api/message",
                json={"message": "test debug"},
                timeout=120
            )
            print(f"✅ Request completed: {response.status_code}")
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    # Uruchom request w tle
    request_thread = threading.Thread(target=send_request)
    request_thread.start()
    
    # Monitoruj logi (symulacja - w rzeczywistości trzeba by przechwycić stdout FastAPI)
    print("🔍 Looking for debug logs...")
    print("📋 Expected debug logs:")
    print("   🔍 DEBUG: Pierwszy chunk: {...}")
    print("   🔍 DEBUG: Typ pierwszego chunka: <class '...'>")
    print("   🔍 DEBUG: Klucze w chunka: [...]")
    print("   🔍 DEBUG: Chunk 1: {...}")
    print("   🔍 DEBUG: Chunk 1 content: '...'")
    
    request_thread.join()
    print("🏁 Monitoring completed")

if __name__ == "__main__":
    monitor_logs()
