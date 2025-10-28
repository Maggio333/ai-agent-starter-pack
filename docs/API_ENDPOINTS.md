# 🌐 API Endpoints - Dokumentacja API

## 📋 Przegląd

System Eliora AI Assistant udostępnia REST API przez FastAPI z następującymi endpointami:

## 🔗 Base URL
```
http://localhost:8080
```

## 📡 Dostępne Endpointy

### 1. **POST `/api/message`** - Wysłanie wiadomości

**Opis:** Główny endpoint do wysyłania wiadomości do asystentki Eliora

**Request Body:**
```json
{
  "message": "string",
  "session_id": "string (optional)"
}
```

**Response:**
```json
{
  "response": "string",
  "session_id": "string",
  "timestamp": "2024-01-01T12:00:00Z",
  "context_used": {
    "idioms_count": 5,
    "conversation_history": 2,
    "rag_results": 3
  }
}
```

**Przykład użycia:**
```bash
curl -X POST "http://localhost:8080/api/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "Cześć Eliora!"}'
```

### 2. **GET `/api/message/stream`** - Streaming odpowiedzi

**Opis:** Endpoint do otrzymywania odpowiedzi w czasie rzeczywistym (Server-Sent Events)

**Query Parameters:**
- `message` (string, required) - Treść wiadomości
- `session_id` (string, optional) - ID sesji

**Response:** Server-Sent Events stream
```
data: {"chunk": "Cześć", "is_complete": false}
data: {"chunk": "! Jak", "is_complete": false}
data: {"chunk": " się masz?", "is_complete": true}
```

**Przykład użycia:**
```bash
curl -N "http://localhost:8080/api/message/stream?message=Cześć%20Eliora!"
```

### 3. **POST `/api/chat/sessions`** - Utworzenie sesji

**Opis:** Tworzy nową sesję rozmowy

**Request Body:**
```json
{
  "user_id": "string (optional)"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "created_at": "2024-01-01T12:00:00Z",
  "status": "active"
}
```

### 4. **GET `/api/chat/sessions/{session_id}`** - Pobranie sesji

**Opis:** Pobiera informacje o sesji i historię rozmowy

**Path Parameters:**
- `session_id` (string, required) - ID sesji

**Response:**
```json
{
  "session_id": "uuid-string",
  "created_at": "2024-01-01T12:00:00Z",
  "status": "active",
  "messages": [
    {
      "role": "user",
      "content": "Cześć!",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "role": "assistant", 
      "content": "Cześć! Jak się masz?",
      "timestamp": "2024-01-01T12:00:01Z"
    }
  ]
}
```

### 5. **POST `/api/vector/search`** - Wyszukiwanie wektorowe

**Opis:** Wyszukuje podobne treści w bazie wektorowej

**Request Body:**
```json
{
  "query": "string",
  "limit": 10,
  "threshold": 0.7
}
```

**Response:**
```json
{
  "results": [
    {
      "content": "string",
      "score": 0.85,
      "metadata": {}
    }
  ],
  "total_found": 5,
  "query_time": "0.123s"
}
```

### 6. **GET `/api/knowledge/stats`** - Statystyki bazy wiedzy

**Opis:** Zwraca statystyki bazy wektorowej

**Response:**
```json
{
  "total_documents": 150,
  "total_vectors": 150,
  "collection_size": "2.5MB",
  "last_updated": "2024-01-01T12:00:00Z"
}
```

### 7. **POST `/api/audio/synthesize`** - Synteza mowy

**Opis:** Konwertuje tekst na mowę (TTS)

**Request Body:**
```json
{
  "text": "string",
  "voice": "female (optional)",
  "speed": 1.0
}
```

**Response:**
```json
{
  "audio_url": "http://localhost:8080/audio/generated_audio.wav",
  "duration": "3.5s",
  "file_size": "56KB"
}
```

## 🔐 Authentication

**Obecnie:** Brak uwierzytelniania (development mode)
**Planowane:** JWT tokens, user roles, permissions

## 📊 Status Codes

| Code | Description |
|------|-------------|
| 200  | OK - Request successful |
| 201  | Created - Resource created |
| 400  | Bad Request - Invalid input |
| 404  | Not Found - Resource not found |
| 422  | Unprocessable Entity - Validation error |
| 500  | Internal Server Error - Server error |

## 🚨 Error Responses

**Standardowy format błędu:**
```json
{
  "detail": "Error message",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Przykłady błędów:**
```json
// 400 Bad Request
{
  "detail": "Content cannot be empty",
  "error_code": "EMPTY_MESSAGE"
}

// 422 Validation Error  
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

// 500 Internal Server Error
{
  "detail": "LLM service unavailable",
  "error_code": "LLM_SERVICE_ERROR"
}
```

## 🔄 Rate Limiting

**Obecnie:** Brak limitów (development mode)
**Planowane:** 
- 100 requests/minute per IP
- 10 requests/minute per session

## 📝 Request/Response Examples

### Pełny przykład rozmowy:

**1. Utworzenie sesji:**
```bash
curl -X POST "http://localhost:8080/api/chat/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
```

**2. Wysłanie wiadomości:**
```bash
curl -X POST "http://localhost:8080/api/message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Opowiedz mi o matematyce",
    "session_id": "session-uuid"
  }'
```

**3. Pobranie historii:**
```bash
curl "http://localhost:8080/api/chat/sessions/session-uuid"
```

## 🧪 Testing

Użyj narzędzi debugowych do testowania API:

```bash
# Test podstawowego endpointu
python tests/test_endpoint.py

# Monitor logów w czasie rzeczywistym
python tests/check_debug_logs.py
```

## 🔮 Future Enhancements

### Planowane endpointy:
1. **`/api/users`** - Zarządzanie użytkownikami
2. **`/api/conversations/export`** - Eksport rozmów
3. **`/api/knowledge/upload`** - Upload dokumentów
4. **`/api/analytics/metrics`** - Metryki użycia
5. **`/api/settings/preferences`** - Preferencje użytkownika

### Planowane funkcje:
- WebSocket support dla real-time chat
- Batch processing dla wielu wiadomości
- File upload dla dokumentów
- Advanced search filters
- Conversation analytics

## 📚 Related Documentation

- **[Project Overview](PROJECT_OVERVIEW.md)** - Przegląd projektu
- **[Debug Tools](DEBUG_TOOLS.md)** - Narzędzia testowe
- **[Architecture](ARCHITECTURE.md)** - Architektura systemu
