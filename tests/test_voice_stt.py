#!/usr/bin/env python3
"""
Test STT with real audio file
"""
import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:8080"

def test_stt_with_file():
    """Test STT with a real audio file"""
    print("Testing STT with audio file...")
    
    # Check if we have any audio files in static/audio
    audio_dir = Path("static/audio")
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.wav"))
        if audio_files:
            audio_file = audio_files[0]  # Use first available audio file
            print(f"Using audio file: {audio_file}")
        else:
            print("No audio files found in static/audio")
            return
    else:
        print("No static/audio directory found")
        return
    
    url = f"{BASE_URL}/api/voice/transcribe"
    
    try:
        with open(audio_file, 'rb') as f:
            files = {'audio': (audio_file.name, f, 'audio/wav')}
            data = {'language': 'pl'}
            
            response = requests.post(url, files=files, data=data)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "ok":
                    print("STT working!")
                    print(f"Transcript: {result.get('transcript')}")
                    print(f"Confidence: {result.get('confidence')}")
                    print(f"Language: {result.get('language')}")
                else:
                    print(f"STT warning: {result.get('message')}")
            
    except Exception as e:
        print(f"STT error: {e}")

def test_stt_with_simple_audio():
    """Test STT by creating a simple test audio file"""
    print("\nCreating simple test audio...")
    
    # Create a simple sine wave audio file for testing
    import numpy as np
    import soundfile as sf
    
    # Generate a simple tone
    sample_rate = 16000
    duration = 2  # seconds
    frequency = 440  # Hz (A note)
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.sin(2 * np.pi * frequency * t) * 0.3  # 30% volume
    
    # Save test audio
    test_audio_path = "test_audio.wav"
    sf.write(test_audio_path, audio, sample_rate)
    print(f"Created test audio: {test_audio_path}")
    
    # Test STT with this file
    url = f"{BASE_URL}/api/voice/transcribe"
    
    try:
        with open(test_audio_path, 'rb') as f:
            files = {'audio': (test_audio_path, f, 'audio/wav')}
            data = {'language': 'pl'}
            
            response = requests.post(url, files=files, data=data)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "ok":
                    print("STT working!")
                    print(f"Transcript: {result.get('transcript')}")
                else:
                    print(f"STT warning: {result.get('message')}")
            
    except Exception as e:
        print(f"STT error: {e}")
    finally:
        # Cleanup
        if os.path.exists(test_audio_path):
            os.remove(test_audio_path)
            print(f"Cleaned up: {test_audio_path}")

if __name__ == "__main__":
    print("Testing STT with Audio Files")
    print("=" * 50)
    
    # First try with existing audio files
    test_stt_with_file()
    
    # Then try with generated test audio
    test_stt_with_simple_audio()
    
    print("\n" + "=" * 50)
    print("STT test completed!")
