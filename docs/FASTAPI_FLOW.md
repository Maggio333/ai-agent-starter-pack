## Dev startup (autoreload)

```bash
cd python_agent
uvicorn main_fastapi:app --reload --host 0.0.0.0 --port 8080
# lub
$env:RELOAD='true'; python main_fastapi.py
```

## App creation
- Aplikacja jest budowana przez `create_app()` i eksportowana jako `app` w `main_fastapi.py`.
- Dzięki temu `uvicorn main_fastapi:app --reload` działa poprawnie.

Last Updated: 2025-10-30  
Version: 1.1.0
# 🚀 Przepływ Clean FastAPI - Jak to lata po plikach

## 📁 **1. Uruchomienie (`main_fastapi.py`)**

```
main_fastapi.py
├── Import Container
├── container = Container()
├── web_server_manager = container.web_server_manager_service()
├── web_server = web_server_manager.create_server("clean_fastapi")
├── app = web_server.create_app()
└── uvicorn.run(app, host="0.0.0.0", port=8080)
```

## 📁 **2. Container (`application/container.py`)**

```
Container
├── config_service = ConfigService()
├── embedding_service = LMStudioEmbeddingService()
├── vector_db_service = QdrantService()
├── chat_repository = SqliteChatRepository()
├── llm_service = LMStudioLLMService()
├── orchestration_service = OrchestrationService()
├── conversation_service = ConversationService()
├── chat_agent_service = ChatAgentService()
└── web_server_manager_service = WebServerManagerService()
```

## 📁 **3. Web Server Manager (`application/services/web_server_manager_service.py`)**

```
WebServerManagerService
├── create_server("clean_fastapi")
├── return CleanFastAPIWebServerService()
└── web_server.create_app()
```

## 📁 **4. Clean FastAPI Web Server (`application/services/clean_fastapi_web_server_service.py`)**

```
CleanFastAPIWebServerService
├── app = FastAPI()
├── app.include_router(chat_router, prefix="/api/chat")
├── app.include_router(voice_router, prefix="/api/voice")
├── app.include_router(notes_router, prefix="/api/notes")
├── app.mount("/static", StaticFiles(directory="static"))
└── return app
```

## 📁 **5. Chat Endpoints (`presentation/api/chat_endpoints.py`)**

```
Chat Endpoints
├── POST /api/chat/send
├── POST /api/chat/message
├── GET /api/chat/history
├── POST /api/chat/process
└── Depends(get_orchestration_service)
```

## 📁 **6. Orchestration Service (`application/services/orchestration_service.py`)**

```
OrchestrationService
├── process_message()
├── conversation_service.add_message()
├── llm_service.generate_response()
├── knowledge_service.search_knowledge_base()
└── return response
```

## 📁 **7. Chat Agent Service (`application/services/chat_agent_service.py`)**

```
ChatAgentService
├── get_weather()
├── get_city_info()
├── search_knowledge_base()
├── process_city_request()
└── orchestration_service.process_message()
```

## 📁 **8. Knowledge Service (`application/services/knowledge_service.py`)**

```
KnowledgeService
├── search_knowledge_base()
├── vector_db_service.search()
├── LMStudioEmbeddingService.create_embedding()
├── QdrantService.search()
└── return RAGChunk results
```

## 📁 **9. Infrastructure Services**

```
Infrastructure
├── LMStudioLLMService (model:1)
├── LMStudioEmbeddingService (model:10)
├── QdrantService (vector search)
├── SqliteChatRepository (chat storage)
└── TextCleanerService (text processing)
```

## 🔄 **Pełny przepływ żądania:**

```
1. HTTP Request → main_fastapi.py
2. Container → WebServerManagerService
3. CleanFastAPIWebServerService → FastAPI app
4. Chat Endpoints → OrchestrationService
5. OrchestrationService → ChatAgentService
6. ChatAgentService → KnowledgeService
7. KnowledgeService → QdrantService
8. QdrantService → LMStudioEmbeddingService
9. LMStudioEmbeddingService → LM Studio (port 8123)
10. Response ← LM Studio
11. Response ← Embedding Service
12. Response ← Vector Search
13. Response ← Knowledge Service
14. Response ← Chat Agent Service
15. Response ← Orchestration Service
16. Response ← Chat Endpoints
17. HTTP Response ← FastAPI
```

## ✅ **Korzyści Clean FastAPI:**

- **Brak Google ADK** - czysty FastAPI
- **Brak cykli** - liniowa architektura
- **Szybkie uruchamianie** - mniej zależności
- **Proste debugowanie** - jasny przepływ
- **Łatwe testowanie** - mockowanie przez Container
- **Clean Architecture** - separacja warstw

## 🎯 **Endpointy dostępne:**

- `POST /api/chat/send` - główny endpoint chat
- `POST /api/chat/message` - alternatywny endpoint
- `GET /api/chat/history` - historia rozmów
- `POST /api/voice/transcribe` - transkrypcja audio
- `POST /api/voice/speak` - synteza mowy
- `GET /api/health` - zdrowie serwisów
- `GET /docs` - dokumentacja OpenAPI
