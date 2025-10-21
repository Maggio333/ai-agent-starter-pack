# 🚀 Szybki Start - Voice AI Assistant

## ⚡ Instalacja w 5 minut

### 1️⃣ Pobierz i zainstaluj

```bash
# Pobierz kod
git clone https://github.com/twoj-repo/ATSReflectumAgentStarterPack.git
cd ATSReflectumAgentStarterPack/python_agent

# Zainstaluj Python zależności
pip install -r requirements.txt
```

### 2️⃣ Pobierz programy

- **Python 3.10+**: https://www.python.org/downloads/
- **Flutter SDK**: https://flutter.dev/docs/get-started/install/windows
- **LM Studio**: https://lmstudio.ai/

### 3️⃣ Uruchom aplikację

```bash
# Terminal 1: LM Studio
# Otwórz LM Studio → Local Server → Start Server

# Terminal 2: Python Backend
python main.py

# Terminal 3: Flutter Frontend
cd presentation/ui/flutter_voice_ui
flutter run -d web-server --web-port 3000
```

### 4️⃣ Otwórz aplikację

🌐 **http://localhost:3000**

---

## 🎤 Jak używać

1. **Kliknij mikrofon** 🎤
2. **Mów** do aplikacji
3. **Słuchaj** odpowiedzi AI

---

## 🔧 Problemy?

### Port zajęty?
```bash
# Znajdź proces
netstat -ano | findstr :8080

# Zabij proces
taskkill /PID [numer] /F
```

### Python nie działa?
```bash
# Sprawdź wersję
python --version

# Zainstaluj zależności
pip install -r requirements.txt
```

### Flutter nie działa?
```bash
# Sprawdź instalację
flutter doctor

# Wyczyść cache
flutter clean
flutter pub get
```

---

## 📞 Pomoc

- 📖 **Pełny przewodnik**: `README_USER_GUIDE.md`
- 🆘 **Problemy**: Sprawdź logi w terminalu
- 💼 **Kontakt**: [LinkedIn](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/) | [GitHub](https://github.com/Maggio333)

**Miłego używania!** 🎉
