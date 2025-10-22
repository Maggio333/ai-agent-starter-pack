# 🎤 Flutter Voice UI

**Flutter Voice UI** to frontend aplikacji Voice AI Assistant. Umożliwia nagrywanie głosu, wysyłanie do AI i odtwarzanie odpowiedzi.

## 🚀 Szybki Start

### Wymagania
- **Flutter SDK** 3.9.2+
- **Python Backend** uruchomiony na porcie 8080
- **LM Studio** z modelem AI

### Instalacja
```bash
# Zainstaluj zależności
flutter pub get

# Uruchom aplikację
flutter run -d web-server --web-port 3000
```

### Użytkowanie
1. **Otwórz aplikację** - http://localhost:3000
2. **Kliknij mikrofon** 🎤 i mów!
3. **AI przetworzy** Twój głos i odpowie
4. **Odtwórz odpowiedź** 🔊

## 🎯 Funkcje

### ✅ Zaimplementowane
- **🎤 Speech-to-Text** - nagrywanie głosu przez Web Audio API
- **🤖 AI Chat** - wysyłanie tekstu do Python backend
- **🔊 Text-to-Speech** - odtwarzanie odpowiedzi AI
- **📱 Material Design** - piękny interfejs
- **🌐 Web App** - działa w przeglądarce
- **🧪 Test Mode** - testowanie bez nagrywania

### 🚧 W planach
- **📱 Mobile App** - Flutter mobile
- **🎨 Custom Themes** - więcej motywów
- **🔊 Audio Visualization** - wizualizacja dźwięku
- **📊 Chat History** - historia rozmów

## 🛠️ Technologie

- **Flutter** - UI framework
- **Web Audio API** - nagrywanie audio
- **HTTP Client** - komunikacja z API
- **Material Design** - design system
- **Dart** - język programowania

## 📦 Zależności

```yaml
dependencies:
  flutter: sdk: flutter
  cupertino_icons: ^1.0.8
  
  # Voice features
  record: ^5.0.4          # Audio recording
  audioplayers: ^6.0.0    # Audio playback
  http: ^1.2.0            # API calls
  file_picker: ^8.0.0     # File upload
  html: ^0.15.4           # Web APIs
  
  # UI
  flutter_animate: ^4.5.0 # Animations
  lottie: ^3.1.2          # Lottie animations
```

## 🔧 Konfiguracja

### Backend URL
Aplikacja komunikuje się z Python backend na:
- **Transcription**: `http://localhost:8080/api/voice/transcribe`
- **AI Chat**: `http://localhost:8080/api/chat/send`
- **Text-to-Speech**: `http://localhost:8080/api/voice/speak`

### Porty
- **Flutter Web**: 3000
- **Python Backend**: 8080

## 🎮 Użytkowanie

### Nagrywanie głosu
1. **Kliknij mikrofon** 🎤
2. **Mów** - aplikacja nagrywa
3. **Kliknij stop** - zatrzymaj nagrywanie
4. **AI przetworzy** Twój głos

### Test mode
1. **Kliknij "Test STT → AI → TTS"** 🧪
2. **Aplikacja wyśle** testowy tekst
3. **AI odpowie** i odtworzy odpowiedź

## 🔧 Rozwiązywanie problemów

### Najczęstsze problemy
- **Backend nie odpowiada** → sprawdź czy Python backend jest uruchomiony
- **Nagrywanie nie działa** → sprawdź uprawnienia mikrofonu w przeglądarce
- **Audio nie odtwarza** → sprawdź czy backend generuje pliki audio

### Debug
- **Otwórz DevTools** - F12 w przeglądarce
- **Sprawdź Console** - błędy JavaScript
- **Sprawdź Network** - komunikacja z API

## 📚 Dokumentacja

- **Główny README**: [../README.md](../README.md)
- **Backend API**: [../python_agent/docs/API.md](../python_agent/docs/API.md)
- **Architektura**: [../python_agent/docs/ARCHITECTURE.md](../python_agent/docs/ARCHITECTURE.md)

## 🤝 Wsparcie

- **💼 LinkedIn**: [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **🐙 GitHub**: [Maggio333](https://github.com/Maggio333)

## 📄 Licencja

MIT License - zobacz [../python_agent/LICENSE](../python_agent/LICENSE)

---

**Miłego używania Flutter Voice UI!** 🎉🎤🤖
