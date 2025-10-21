#!/usr/bin/env python3
"""
Test script for voice endpoints
"""
import requests
import json
import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8080"

def test_tts():
    """Test Text-to-Speech endpoint"""
    print("Testing TTS endpoint...")
    
    url = f"{BASE_URL}/api/voice/speak"
    data = {
        "text": "Cześć! To jest test polskiego głosu. Jak się masz?",
        "voice": "pl-PL-default"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "ok":
                print("TTS working!")
                print(f"Audio URL: {result.get('audio_url')}")
            else:
                print(f"TTS warning: {result.get('message')}")
        
    except Exception as e:
        print(f"TTS error: {e}")

def test_notes():
    """Test Notes endpoint"""
    print("\nTesting Notes endpoint...")
    
    url = f"{BASE_URL}/api/notes/save"
    data = {
        "title": "Test notatki",
        "content": "To jest testowa notatka z głosu",
        "location": "Warszawa",
        "tags": "test, głos, AI"
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("Notes working!")
        
    except Exception as e:
        print(f"Notes error: {e}")

def test_health():
    """Test if server is running"""
    print("Testing server health...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 307]:
            print("Server is running!")
            return True
        else:
            print("Server not responding")
            return False
    except Exception as e:
        print(f"Server error: {e}")
        return False

async def main():
    """Main test function"""
    print("Testing Voice Features")
    print("=" * 50)
    
    if test_health():
        test_tts()
        test_notes()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(main())
