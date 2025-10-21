# 🎤 Voice AI Assistant - Przewodnik Użytkownika

## 📋 Spis Treści
1. [Co to jest?](#co-to-jest)
2. [Wymagania](#wymagania)
3. [Instalacja krok po kroku](#instalacja-krok-po-kroku)
4. [Uruchamianie aplikacji](#uruchamianie-aplikacji)
5. [Jak używać](#jak-używać)
6. [Rozwiązywanie problemów](#rozwiązywanie-problemów)
7. [FAQ](#faq)

---

## 🤖 Co to jest?

**Voice AI Assistant** to aplikacja, która pozwala na rozmowę z sztuczną inteligencją używając głosu:

- 🎤 **Mówisz** do aplikacji (Speech-to-Text)
- 🤖 **AI odpowiada** tekstowo
- 🔊 **AI mówi** odpowiedź (Text-to-Speech)

**Aplikacja składa się z:**
- **Python Backend** - serwer AI (port 8080)
- **Flutter Frontend** - aplikacja głosowa (port 3000)
- **LM Studio** - lokalny model AI

---

## 💻 Wymagania

### 🖥️ System Operacyjny
- **Windows 10/11** (64-bit)
- **8GB RAM** minimum (16GB zalecane)
- **10GB wolnego miejsca** na dysku

### 📦 Wymagane Programy
1. **Python 3.10+** - [Pobierz tutaj](https://www.python.org/downloads/)
2. **Flutter SDK** - [Pobierz tutaj](https://flutter.dev/docs/get-started/install/windows)
3. **LM Studio** - [Pobierz tutaj](https://lmstudio.ai/)
4. **Git** - [Pobierz tutaj](https://git-scm.com/download/win)

### 🌐 Porty
Upewnij się, że porty są wolne:
- **8080** - Python Backend
- **3000** - Flutter Frontend
- **8123** - LM Studio Proxy

---

## 🚀 Instalacja krok po kroku

### Krok 1: Pobierz kod aplikacji

1. Otwórz **Command Prompt** (cmd)
2. Przejdź do folderu gdzie chcesz mieć aplikację:
   ```cmd
   cd C:\Users\%USERNAME%\Desktop
   ```
3. Pobierz kod:
   ```cmd
   git clone https://github.com/twoj-repo/ATSReflectumAgentStarterPack.git
   ```
4. Przejdź do folderu aplikacji:
   ```cmd
   cd ATSReflectumAgentStarterPack\python_agent
   ```

### Krok 2: Zainstaluj Python i zależności

1. **Sprawdź czy Python jest zainstalowany:**
   ```cmd
   python --version
   ```
   Powinno pokazać: `Python 3.10.x` lub nowszy

2. **Zainstaluj zależności Python:**
   ```cmd
   pip install -r requirements.txt
   ```

### Krok 3: Zainstaluj Flutter

1. **Pobierz Flutter SDK** z [flutter.dev](https://flutter.dev/docs/get-started/install/windows)
2. **Rozpakuj** do `C:\flutter`
3. **Dodaj do PATH:**
   - Otwórz "Zmienne środowiskowe"
   - Dodaj `C:\flutter\bin` do PATH
4. **Sprawdź instalację:**
   ```cmd
   flutter doctor
   ```

### Krok 4: Zainstaluj LM Studio

1. **Pobierz LM Studio** z [lmstudio.ai](https://lmstudio.ai/)
2. **Zainstaluj** aplikację
3. **Pobierz model AI:**
   - Otwórz LM Studio
   - Przejdź do "Models"
   - Wyszukaj "Llama" lub "Mistral"
   - Pobierz model (około 4-7GB)

### Krok 5: Skonfiguruj aplikację

1. **Skopiuj plik konfiguracyjny:**
   ```cmd
   copy env.example .env
   ```

2. **Otwórz plik `.env`** w notatniku i sprawdź ustawienia:
   ```
   LMSTUDIO_LLM_PROXY_URL=http://127.0.0.1:8123
   LMSTUDIO_PROXY_URL=http://127.0.0.1:8123
   ```

---

## 🎬 Uruchamianie aplikacji

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

1. **Otwórz Command Prompt**
2. **Przejdź do folderu aplikacji:**
   ```cmd
   cd C:\Users\%USERNAME%\Desktop\ATSReflectumAgentStarterPack\python_agent
   ```
3. **Uruchom serwer:**
   ```cmd
   python main.py
   ```
4. **Sprawdź czy działa:**
   - Otwórz przeglądarkę
   - Idź na `http://localhost:8080`
   - Powinieneś zobaczyć stronę API

### Krok 3: Uruchom Flutter Frontend

1. **Otwórz nowy Command Prompt**
2. **Przejdź do folderu Flutter:**
   ```cmd
   cd C:\Users\%USERNAME%\Desktop\ATSReflectumAgentStarterPack\python_agent\presentation\ui\flutter_voice_ui
   ```
3. **Uruchom aplikację:**
   ```cmd
   flutter run -d web-server --web-port 3000
   ```
4. **Sprawdź czy działa:**
   - Otwórz przeglądarkę
   - Idź na `http://localhost:3000`
   - Powinieneś zobaczyć aplikację głosową

---

## 🎤 Jak używać

### 🎯 Podstawowe użycie

1. **Otwórz aplikację** w przeglądarce: `http://localhost:3000`
2. **Kliknij przycisk mikrofonu** 🎤
3. **Mów** do mikrofonu
4. **Poczekaj** na odpowiedź AI
5. **Słuchaj** odpowiedzi AI

### 🎛️ Kontrolki

- **🎤 Przycisk mikrofonu** - rozpocznij/zakończ nagrywanie
- **🔊 Głośność** - reguluj głośność odpowiedzi
- **⚙️ Ustawienia** - konfiguruj aplikację

### 💡 Wskazówki

- **Mów wyraźnie** - lepsze rozpoznawanie mowy
- **Nie mów za szybko** - AI lepiej zrozumie
- **Używaj krótkich zdań** - lepsze odpowiedzi
- **Sprawdź mikrofon** - upewnij się że działa

---

## 🔧 Rozwiązywanie problemów

### ❌ Problem: "Python nie jest rozpoznawany"

**Rozwiązanie:**
1. Sprawdź czy Python jest zainstalowany: `python --version`
2. Dodaj Python do PATH w zmiennych środowiskowych
3. Restartuj Command Prompt

### ❌ Problem: "Port 8080 jest zajęty"

**Rozwiązanie:**
1. Znajdź proces używający portu:
   ```cmd
   netstat -ano | findstr :8080
   ```
2. Zabij proces:
   ```cmd
   taskkill /PID [numer_procesu] /F
   ```

### ❌ Problem: "LM Studio nie odpowiada"

**Rozwiązanie:**
1. Sprawdź czy LM Studio jest uruchomiony
2. Sprawdź czy model jest załadowany
3. Sprawdź port: `http://localhost:1234`
4. Restartuj LM Studio

### ❌ Problem: "Flutter nie działa"

**Rozwiązanie:**
1. Sprawdź instalację: `flutter doctor`
2. Uruchom: `flutter clean`
3. Uruchom: `flutter pub get`

### ❌ Problem: "Nie słyszę odpowiedzi AI"

**Rozwiązanie:**
1. Sprawdź głośniki/mikrofon
2. Sprawdź ustawienia przeglądarki
3. Sprawdź czy port 8080 działa
4. Sprawdź logi w Command Prompt

---

## ❓ FAQ

### 🤔 Czy potrzebuję internetu?

**TAK** - tylko do pobrania modeli AI. Po pobraniu wszystko działa lokalnie.

### 🤔 Ile miejsca na dysku potrzebuję?

**Minimum 10GB:**
- Python: ~1GB
- Flutter: ~2GB
- LM Studio: ~1GB
- Model AI: ~4-7GB

### 🤔 Czy mogę używać innych modeli AI?

**TAK** - możesz używać różnych modeli w LM Studio. Sprawdź dokumentację LM Studio.

### 🤔 Czy aplikacja działa na innych systemach?

**TAK** - ale ten przewodnik jest dla Windows. Dla Linux/Mac potrzebujesz innych instrukcji.

### 🤔 Czy mogę zmienić porty?

**TAK** - ale musisz zmienić konfigurację w kilku miejscach. Skontaktuj się z deweloperem.

---

## 📞 Wsparcie

### 🆘 Gdy potrzebujesz pomocy

1. **Sprawdź logi** w Command Prompt
2. **Sprawdź** sekcję "Rozwiązywanie problemów"
3. **Skontaktuj się** z deweloperem
4. **Prześlij** logi błędów

### 📧 Kontakt

- **LinkedIn:** [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **GitHub:** [Maggio333](https://github.com/Maggio333)

---

## 🎉 Gratulacje!

Jeśli dotarłeś do tego miejsca, powinieneś mieć działającą aplikację Voice AI Assistant!

**Miłego używania!** 🚀🎤🤖
