# 🚀 Przepływ Google ADK - Jak to lata po plikach

## 📁 **1. Uruchomienie (`main_adk.py`)**

```
main_adk.py
├── Import Container
├── container = Container()
├── web_server_manager = container.web_server_manager_service()
├── web_server = web_server_manager.create_server("google_adk")
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
├── create_server("google_adk")
├── return GoogleADKWebServerService()
└── web_server.create_app()
```

## 📁 **4. Google ADK Web Server (`application/services/google_adk_web_server_service.py`)**

```
GoogleADKWebServerService
├── app = get_fast_api_app()  # Google ADK
├── agents_dir="agents"      # Skanuje folder agents/
├── web=True                 # Włącza ADK Web UI
├── app.include_router(chat_router, prefix="/api/chat")
├── app.include_router(voice_router, prefix="/api/voice")
├── app.include_router(notes_router, prefix="/api/notes")
└── return app
```

## 📁 **5. Agent Discovery (`agents/microservices_agent/agent.py`)**

```
Agent Discovery
├── Google ADK skanuje folder "agents/"
├── Znajduje microservices_agent/agent.py
├── Importuje root_agent
├── root_agent = Agent() z narzędziami
└── Dodaje do ADK Web UI
```

## 📁 **6. ADK Agent (`agents/microservices_agent/agent.py`)**

```
ADK Agent
├── container = Container()
├── chat_agent_service = container.chat_agent_service()
├── lm_studio_model = LiteLlm(model="lm_studio/model:1")
├── root_agent = Agent(
│   ├── name="microservices_chat_agent"
│   ├── model=lm_studio_model
│   └── tools=[19 narzędzi z ChatAgentService]
└── )
```

## 📁 **7. ADK Web UI (`http://localhost:8080`)**

```
ADK Web UI
├── Wyświetla listę agentów
├── microservices_chat_agent
├── Użytkownik wybiera agenta
├── Rozpoczyna sesję
└── POST /run_sse (Server-Sent Events)
```

## 📁 **8. ADK Execution Flow**

```
ADK Execution
├── Użytkownik pisze wiadomość
├── ADK Web UI → POST /run_sse
├── Google ADK → root_agent.run()
├── root_agent → LiteLlm (LM Studio)
├── LM Studio → model:1 (port 8123)
├── Response ← LM Studio
├── ADK → function_tool.FunctionTool()
├── FunctionTool → ChatAgentService method
├── ChatAgentService → KnowledgeService
├── KnowledgeService → QdrantService
├── QdrantService → LMStudioEmbeddingService
├── LMStudioEmbeddingService → model:10 (port 8123)
├── Response ← Embedding Service
├── Response ← Vector Search
├── Response ← Knowledge Service
├── Response ← Chat Agent Service
├── Response ← Function Tool
├── Response ← ADK Agent
└── Response ← ADK Web UI
```

## 📁 **9. Narzędzia Agent (19 narzędzi)**

```
Agent Tools
├── Weather Service Tools
│   ├── get_weather()
│   ├── get_weather_forecast()
│   └── get_weather_alerts()
├── Time Service Tools
│   ├── get_current_time()
│   ├── get_timezone_info()
│   └── get_world_clock()
├── City Service Tools
│   ├── get_city_info()
│   ├── search_cities()
│   ├── get_city_attractions()
│   └── compare_cities()
├── Knowledge Service Tools
│   ├── search_knowledge_base()
│   ├── add_knowledge()
│   └── get_knowledge_stats()
├── Conversation Service Tools
│   ├── start_conversation()
│   ├── get_conversation_history()
│   ├── end_conversation()
│   └── get_conversation_stats()
└── Orchestration Tools
    ├── process_city_request()
    ├── get_service_health()
    └── get_service_capabilities()
```

## 📁 **10. Infrastructure Services**

```
Infrastructure
├── LMStudioLLMService (model:1) - Chat
├── LMStudioEmbeddingService (model:10) - Embeddings
├── QdrantService (vector search)
├── SqliteChatRepository (chat storage)
└── TextCleanerService (text processing)
```

## 🔄 **Pełny przepływ żądania ADK:**

```
1. Użytkownik → ADK Web UI
2. ADK Web UI → POST /run_sse
3. Google ADK → root_agent.run()
4. root_agent → LiteLlm (LM Studio model:1)
5. LM Studio → Response (port 8123)
6. ADK → Function Tool Call
7. Function Tool → ChatAgentService method
8. ChatAgentService → KnowledgeService
9. KnowledgeService → QdrantService
10. QdrantService → LMStudioEmbeddingService
11. LMStudioEmbeddingService → LM Studio (model:10)
12. LM Studio → Embedding (port 8123)
13. Embedding → Vector Search
14. Vector Search → Knowledge Results
15. Knowledge → Chat Agent Response
16. Chat Agent → Function Tool Response
17. Function Tool → ADK Agent Response
18. ADK Agent → ADK Web UI Response
19. ADK Web UI → Użytkownik
```

## ✅ **Korzyści Google ADK:**

- **ADK Web UI** - gotowy interfejs użytkownika
- **Agent Management** - zarządzanie agentami
- **Session Management** - sesje użytkowników
- **Debug Tracing** - śledzenie wykonania
- **Function Tools** - integracja z Python functions
- **Live Connection** - (ograniczone dla LM Studio)

## ⚠️ **Ograniczenia ADK:**

- **Live Connection** - nie działa z LM Studio
- **Warnings** - eksperymentalne funkcje
- **Complexity** - więcej warstw abstrakcji
- **Dependencies** - Google ADK + LiteLlm

## 🎯 **Endpointy dostępne:**

- `GET /` - ADK Web UI
- `GET /list-apps` - lista agentów
- `POST /run_sse` - wykonanie agenta
- `GET /debug/trace` - śledzenie debug
- `POST /api/chat/send` - nasze endpointy
- `POST /api/voice/transcribe` - transkrypcja
- `POST /api/voice/speak` - synteza
- `GET /api/health` - zdrowie serwisów
