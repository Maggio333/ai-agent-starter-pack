# 🔧 Przewodnik Rozwiązywania Problemów

## 🚨 Najczęstsze Problemy

### ❌ "Python nie jest rozpoznawany jako polecenie"

**Przyczyna:** Python nie jest zainstalowany lub nie jest w PATH.

**Rozwiązanie:**
1. Pobierz Python z https://www.python.org/downloads/
2. Podczas instalacji zaznacz "Add Python to PATH"
3. Restartuj Command Prompt
4. Sprawdź: `python --version`

### ❌ "Port 8080 jest już w użyciu"

**Przyczyna:** Inna aplikacja używa portu 8080.

**Rozwiązanie:**
```cmd
# Znajdź proces
netstat -ano | findstr :8080

# Zabij proces (zastąp XXXX numerem PID)
taskkill /PID XXXX /F
```

### ❌ "Port 3000 jest już w użyciu"

**Przyczyna:** Inna aplikacja używa portu 3000.

**Rozwiązanie:**
```cmd
# Znajdź proces
netstat -ano | findstr :3000

# Zabij proces
taskkill /PID XXXX /F
```

### ❌ "LM Studio nie odpowiada"

**Przyczyna:** LM Studio nie jest uruchomiony lub model nie jest załadowany.

**Rozwiązanie:**
1. Otwórz LM Studio
2. Przejdź do "Local Server"
3. Wybierz model i kliknij "Start Server"
4. Sprawdź: http://localhost:1234

### ❌ "Flutter doctor pokazuje błędy"

**Przyczyna:** Flutter nie jest poprawnie zainstalowany.

**Rozwiązanie:**
1. Pobierz Flutter SDK
2. Rozpakuj do `C:\flutter`
3. Dodaj `C:\flutter\bin` do PATH
4. Restartuj Command Prompt
5. Uruchom: `flutter doctor`

### ❌ "Nie słyszę odpowiedzi AI"

**Przyczyna:** Problem z audio lub TTS.

**Rozwiązanie:**
1. Sprawdź głośniki/mikrofon
2. Sprawdź ustawienia przeglądarki
3. Sprawdź czy port 8080 działa
4. Sprawdź logi w terminalu Python

### ❌ "Mikrofon nie działa"

**Przyczyna:** Brak uprawnień do mikrofonu.

**Rozwiązanie:**
1. Sprawdź ustawienia przeglądarki
2. Zezwól na dostęp do mikrofonu
3. Sprawdź czy mikrofon działa w innych aplikacjach

### ❌ "Aplikacja nie ładuje się"

**Przyczyna:** Błąd w kodzie lub konfiguracji.

**Rozwiązanie:**
1. Sprawdź logi w terminalu
2. Sprawdź czy wszystkie serwisy są uruchomione
3. Restartuj wszystkie terminale
4. Sprawdź czy plik `.env` istnieje

---

## 🔍 Diagnostyka

### Sprawdź status serwisów

```cmd
# Sprawdź czy porty są otwarte
netstat -ano | findstr :8080
netstat -ano | findstr :3000
netstat -ano | findstr :1234
```

### Sprawdź logi

**Python Backend:**
```cmd
python main.py
# Szukaj błędów w terminalu
```

**Flutter Frontend:**
```cmd
flutter run -d web-server --web-port 3000
# Szukaj błędów w terminalu
```

### Sprawdź konfigurację

**Plik `.env`:**
```
LMSTUDIO_LLM_PROXY_URL=http://127.0.0.1:8123
LMSTUDIO_PROXY_URL=http://127.0.0.1:8123
```

---

## 🆘 Gdy nic nie pomaga

### 1. Restart wszystkiego
```cmd
# Zamknij wszystkie terminale
# Restartuj komputer
# Uruchom ponownie wszystkie serwisy
```

### 2. Sprawdź logi błędów
- Skopiuj błędy z terminala
- Prześlij deweloperowi

### 3. Sprawdź wersje
```cmd
python --version
flutter --version
```

### 4. Wyczyść cache
```cmd
# Flutter
flutter clean
flutter pub get

# Python
pip cache purge
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Kontakt

Gdy potrzebujesz pomocy:

1. **Sprawdź** ten przewodnik
2. **Sprawdź** logi błędów
3. **Skontaktuj się** z deweloperem
4. **Prześlij**:
   - Opis problemu
   - Logi błędów
   - Wersje programów
   - System operacyjny

- **LinkedIn:** [Arkadiusz Słota](https://www.linkedin.com/in/arkadiusz-s%C5%82ota-229551172/)
- **GitHub:** [Maggio333](https://github.com/Maggio333)
