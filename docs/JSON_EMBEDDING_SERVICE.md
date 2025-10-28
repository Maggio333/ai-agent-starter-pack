# JSONEmbeddingService - Obsługa JSON i Embeddingów

## 📋 Przegląd

`JSONEmbeddingService` obsługuje parsowanie pierwszego JSON zwróconego przez model oraz automatyczne generowanie embeddingu dla wyszukiwania w bazie wektorowej.

## 🎯 Problem, który rozwiązuje

### Przed
```python
# Hardcoded parsowanie JSON
response = str(result.value)
try:
    analysis = json.loads(response)
except json.JSONDecodeError:
    # Fallback...
```

### Po
```python
# Centralny serwis z inteligentnym parsowaniem
result = await json_embedding_service.process_json_for_rag(
    llm_response,
    query_key="vector_query",
    auto_create_embedding=True
)
```

## 🔧 Funkcjonalność

### 1. Inteligentne parsowanie JSON

Obsługuje wiele formatów odpowiedzi z modelu:

```python
# Format 1: Bezpośredni JSON
{"vector_query": "..."}

# Format 2: JSON w bloku code
```json
{"vector_query": "..."}
```

# Format 3: Python dict syntax
{"vector_query": True, "reasoning": None}

# Format 4: Text z ukrytym dict
Some text before {dict} more text
```

### 2. Ekstrakcja zapytania wektorowego

```python
# Automatycznie znajdzie pole "vector_query" w JSON
result = await json_embedding_service.extract_and_embed_from_json(
    llm_response,
    query_key="vector_query"
)

# parsed_json: {"vector_query": "...", "reasoning": "..."}
# query_text: "..."
```

### 3. Automatyczne generowanie embeddingu

```python
# Jednym wywołaniem: parse + extract + embed
result = await json_embedding_service.process_json_for_rag(
    llm_response,
    auto_create_embedding=True
)

# Zwraca:
# {
#   "parsed_json": {...},
#   "query_text": "...",
#   "embedding": [0.1, 0.2, ...],
#   "embedding_dim": 1024
# }
```

## 📊 Integracja z DynamicRAG

```python
class DynamicRAGService:
    def __init__(self, ..., embedding_service=None):
        self.json_embedding_service = JSONEmbeddingService(
            embedding_service=embedding_service
        )
    
    async def _analyze_for_rag_query(self, analysis_prompt: str):
        # Wywołaj LLM
        result = await self.llm_service.get_completion(analysis_messages)
        response = str(result.value)
        
        # Użyj JSONEmbeddingService
        processing = await self.json_embedding_service.process_json_for_rag(
            response,
            query_key="vector_query",
            auto_create_embedding=True
        )
        
        if processing.is_success:
            # Masz JSON i embedding gotowy do użycia!
            parsed_json = processing.value["parsed_json"]
            embedding = processing.value.get("embedding")
            
            # Teraz możesz wyszukać w bazie wektorowej używając embedding
            search_results = await self.knowledge_service.search_by_embedding(
                embedding
            )
```

## 🔍 Metody API

### `extract_and_embed_from_json(llm_response, query_key)`

Ekstraktuje JSON i wyciąga określone pole.

```python
result = await service.extract_and_embed_from_json(
    '{"vector_query": "AI ethics", "reasoning": "..."}',
    query_key="vector_query"
)

# Returns: ({"vector_query": "...", "reasoning": "..."}, "AI ethics")
```

### `create_embedding_for_query(query_text)`

Tworzy embedding dla tekstu.

```python
result = await service.create_embedding_for_query("AI ethics")
# Returns: [0.1, 0.2, 0.3, ...]  # embedding vector
```

### `process_json_for_rag(llm_response, query_key, auto_create_embedding)`

Kompletne przetworzenie: parse + extract + embed.

```python
result = await service.process_json_for_rag(
    llm_response="<JSON response>",
    query_key="vector_query",
    auto_create_embedding=True
)

# Returns: {
#   "parsed_json": {...},
#   "query_text": "...",
#   "embedding": [...],
#   "embedding_dim": 1024
# }
```

## 🎓 Przykład użycia

### Scenariusz: Dynamiczne zapytania RAG

```python
# 1. Model zwraca JSON z analizą
llm_response = """
{
    "main_topic": "AI ethics",
    "information_needed": "Philosophical frameworks",
    "vector_query": "What are philosophical frameworks for AI ethics?",
    "reasoning": "User is asking about ethical frameworks"
}
```

# 2. JSONEmbeddingService parsuje i wyciąga pole "vector_query"
result = await json_embedding_service.process_json_for_rag(
    llm_response,
    query_key="vector_query"
)

# 3. Otrzymujesz embedding gotowy do użycia
if result.is_success:
    embedding = result.value["embedding"]
    query_text = result.value["query_text"]
    
    # 4. Wyszukaj w bazie wektorowej używając embedding
    search_results = await vector_db.search_by_embedding(
        embedding,
        limit=5
    )
```

## 🔄 Przepływ danych

```
LLM Response (JSON string)
  ↓
extract_json_from_response()
  ↓
Parsed JSON dict
  ↓
extract_query_text(query_key)
  ↓
Query Text
  ↓
create_embedding_for_query()
  ↓
Embedding Vector [0.1, 0.2, ...]
  ↓
Vector Database Search
```

## 📝 Walidacja

```python
# Sprawdź czy JSON ma poprawną strukturę
is_valid = service.validate_json_structure(parsed_json)

# Walidacja sprawdza:
# - Czy to jest dict
# - Czy ma klucze
# - Czy struktura jest ok
```

## 🛠️ Konfiguracja

### Embedding Service

Serwis wymaga przekazania `embedding_service`:

```python
from infrastructure.ai.embedding.lmstudio_embedding_service import LMStudioEmbeddingService

embedding_service = LMStudioEmbeddingService(...)
json_embedding_service = JSONEmbeddingService(
    embedding_service=embedding_service
)
```

### Auto-fallback

Jeśli embedding service nie jest dostępny, zwraca dummy vector:

```python
# Bez embedding service
result = await service.create_embedding_for_query("test")
# Returns: [0.1] * 1024  # Dummy vector
```

## 📍 Lokalizacja

```
application/services/json_embedding_service.py
```

## 🔗 Powiązane serwisy

- `DynamicRAGService` - używa JSONEmbeddingService
- `KnowledgeService` - wyszukiwanie w bazie wektorowej
- `EmbeddingService` - generowanie embeddingów

## 💡 Zalety

1. **Inteligentne parsowanie** - obsługuje wiele formatów JSON
2. **Automatyczne embeddingi** - tworzy embedding używając właściwego query
3. **Fallback handling** - graceful degradation gdy coś się nie udaje
4. **Centralizacja** - jedna lokalizacja dla parsowania JSON
5. **Logging** - szczegółowe logi dla debugowania

## 🚀 Przyszłe rozszerzenia

- [ ] Cache dla embeddingów
- [ ] Validacja schematu JSON (JSON Schema)
- [ ] Obsługa wielu zapytań (batch embeddings)
- [ ] Metryki jakości embeddings
- [ ] Konfigurowalne strategie parsowania

