# 🪟 Instalacja na Windows - Krok po Kroku

## 📋 Wymagania

- **Windows 10/11** (64-bit)
- **8GB RAM** minimum (16GB zalecane)
- **10GB wolnego miejsca** na dysku
- **Połączenie internetowe**

## 🚀 Instalacja Programów

### 1️⃣ Python 3.10+

1. **Pobierz Python** z https://www.python.org/downloads/
2. **Uruchom installer** i zaznacz:
   - ✅ "Add Python to PATH"
   - ✅ "Install for all users"
3. **Sprawdź instalację:**
   ```cmd
   python --version
   ```
   Powinno pokazać: `Python 3.10.x` lub nowszy

### 2️⃣ Git

1. **Pobierz Git** z https://git-scm.com/download/win
2. **Zainstaluj** z domyślnymi ustawieniami
3. **Sprawdź instalację:**
   ```cmd
   git --version
   ```

### 3️⃣ Flutter SDK

1. **Pobierz Flutter** z https://flutter.dev/docs/get-started/install/windows
2. **Rozpakuj** do `C:\flutter`
3. **Dodaj do PATH:**
   - Otwórz "Zmienne środowiskowe"
   - Kliknij "Zmienne środowiskowe..."
   - W sekcji "Zmienne systemu" znajdź "Path"
   - Kliknij "Edytuj..." → "Nowy"
   - Dodaj: `C:\flutter\bin`
   - Kliknij "OK"
4. **Sprawdź instalację:**
   ```cmd
   flutter doctor
   ```

### 4️⃣ LM Studio

1. **Pobierz LM Studio** z https://lmstudio.ai/
2. **Zainstaluj** aplikację
3. **Pobierz model AI:**
   - Otwórz LM Studio
   - Przejdź do "Models"
   - Wyszukaj "Llama" lub "Mistral"
   - Pobierz model (około 4-7GB)

## 📥 Pobieranie Kodu

1. **Otwórz Command Prompt** (cmd)
2. **Przejdź do folderu Desktop:**
   ```cmd
   cd C:\Users\%USERNAME%\Desktop
   ```
3. **Pobierz kod:**
   ```cmd
   git clone https://github.com/Maggio333/ai-agent-starter-pack.git
   ```
4. **Przejdź do folderu aplikacji:**
   ```cmd
   cd ai-agent-starter-pack
   ```

## 🔧 Instalacja Zależności

1. **Zainstaluj Python zależności:**
   ```cmd
   pip install -r requirements.txt
   ```

2. **Sprawdź czy wszystko działa:**
   ```cmd
   python --version
   flutter doctor
   ```

## 🎬 Uruchamianie Aplikacji

### Krok 1: Uruchom LM Studio

1. **Otwórz LM Studio**
2. **Załaduj model:**
   - Przejdź do "Local Server"
   - Wybierz pobrany model
   - Kliknij "Start Server"
3. **Sprawdź czy działa:**
   - Otwórz przeglądarkę
   - Idź na `http://localhost:1234`
   - Powinieneś zobaczyć interfejs LM Studio

### Krok 2: Uruchom Python Backend

**Opcja A: Clean FastAPI (Zalecane)**
```cmd
python main_fastapi.py
```

**Opcja B: Google ADK (Zaawansowane)**
```cmd
python main_adk.py
```

**Sprawdź czy działa:**
- Otwórz przeglądarkę
- Idź na `http://localhost:8080`
- Powinieneś zobaczyć stronę API

### Krok 3: Uruchom Flutter Frontend

1. **Otwórz nowy Command Prompt**
2. **Przejdź do folderu Flutter:**
   ```cmd
   cd C:\Users\%USERNAME%\Desktop\ai-agent-starter-pack\presentation\ui\flutter_voice_ui
   ```
3. **Uruchom aplikację:**
   ```cmd
   flutter run -d web-server --web-port 3000
   ```
4. **Sprawdź czy działa:**
   - Otwórz przeglądarkę
   - Idź na `http://localhost:3000`
   - Powinieneś zobaczyć aplikację głosową

## 🎤 Używanie Aplikacji

1. **Otwórz aplikację** w przeglądarce: `http://localhost:3000`
2. **Kliknij przycisk mikrofonu** 🎤
3. **Mów** do mikrofonu
4. **Poczekaj** na odpowiedź AI
5. **Słuchaj** odpowiedzi AI

## 🔧 Rozwiązywanie Problemów

### Port zajęty?
```cmd
netstat -ano | findstr :8080
taskkill /PID [numer] /F
```

### Python nie działa?
```cmd
python --version
pip install -r requirements.txt
```

### Flutter nie działa?
```cmd
flutter doctor
flutter clean
flutter pub get
```

### LM Studio nie odpowiada?
- Sprawdź czy serwer jest uruchomiony na porcie 8123
- Upewnij się że model jest załadowany
- Sprawdź logi w LM Studio

### Aplikacja nie odpowiada?
- Sprawdź czy wszystkie 3 serwery są uruchomione
- Sprawdź logi w terminalach
- Upewnij się że porty są wolne

## 📞 Pomoc

- 📖 **Pełny przewodnik**: `USER_GUIDE.md`
- 🆘 **Problemy**: Sprawdź logi w terminalu
- 💼 **Kontakt**: [LinkedIn](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/) | [GitHub](https://github.com/Maggio333)

**Miłego używania!** 🎉
