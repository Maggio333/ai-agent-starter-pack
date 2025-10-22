# 🎤 Voice AI Assistant - Prosty Przewodnik

## 🎯 Co to jest?

**Voice AI Assistant** to aplikacja, która pozwala na rozmowę z AI używając głosu:

- 🎤 **Mówisz** do aplikacji
- 🤖 **AI odpowiada** tekstowo  
- 🔊 **AI mówi** odpowiedź

## ⚡ Szybki Start (5 minut)

### 1️⃣ Pobierz programy
- **Python 3.10+**: https://www.python.org/downloads/
- **Flutter SDK**: https://flutter.dev/docs/get-started/install/windows
- **LM Studio**: https://lmstudio.ai/

### 2️⃣ Pobierz kod
```bash
git clone https://github.com/Maggio333/ai-agent-starter-pack.git
cd ai-agent-starter-pack
pip install -r requirements.txt
```

### 3️⃣ Uruchom aplikację

**Terminal 1: LM Studio**
- Otwórz LM Studio → Local Server → Start Server

**Terminal 2: Python Backend**
```bash
python main_fastapi.py
```

**Terminal 3: Flutter Frontend**
```bash
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```

### 4️⃣ Otwórz aplikację
🌐 **http://localhost:3000**

## 🎤 Jak używać

1. **Kliknij mikrofon** 🎤
2. **Mów** do aplikacji
3. **Słuchaj** odpowiedzi AI

## 🔧 Problemy?

### Port zajęty?
```bash
netstat -ano | findstr :8080
taskkill /PID [numer] /F
```

### Python nie działa?
```bash
python --version
pip install -r requirements.txt
```

### Flutter nie działa?
```bash
flutter doctor
flutter clean
flutter pub get
```

### LM Studio nie odpowiada?
- Sprawdź czy serwer jest uruchomiony na porcie 8123
- Upewnij się że model jest załadowany

## 🎯 Różnice między serwerami

| Funkcja | Clean FastAPI | Google ADK |
|---------|---------------|------------|
| **Łatwość** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Funkcje** | Podstawowe | Zaawansowane |
| **Dokumentacja** | OpenAPI | ADK UI |
| **Zalecane dla** | Początkujących | Zaawansowanych |

## 📞 Pomoc

- 📖 **Pełny przewodnik**: `USER_GUIDE.md`
- 🆘 **Problemy**: Sprawdź logi w terminalu
- 💼 **Kontakt**: [LinkedIn](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/) | [GitHub](https://github.com/Maggio333)

**Miłego używania!** 🎉
