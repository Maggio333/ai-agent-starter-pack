# application/services/dynamic_rag_service.py
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.utils.result import Result
from application.services.chat_agent_service import ChatAgentService
from application.services.json_embedding_service import JSONEmbeddingService

class DynamicRAGService:
    """Serwis do dynamicznych zapytań RAG decydowanych przez LLM (inspirowany ChatElioraReflect)"""
    
    def __init__(self, llm_service=None, knowledge_service=None, conversation_service=None, json_embedding_service=None):
        """Initialize DynamicRAGService with injected dependencies"""
        self.llm_service = llm_service
        self.knowledge_service = knowledge_service
        self.conversation_service = conversation_service
        self.json_embedding_service = json_embedding_service
        self.logger = logging.getLogger(__name__)
    
    async def decide_vector_query(
        self, 
        conversation_context: List[ChatMessage], 
        current_message: str,
        user_context: Optional[dict] = None
    ) -> Result[str, str]:
        """Decyduje jakie zapytanie zadać do bazy wektorowej (jak GetStreamHistoryFromDb w ChatElioraReflect)"""
        try:
            # Buduje prompt analizy (jak w ChatElioraReflect)
            analysis_prompt = self._build_rag_analysis_prompt(
                conversation_context, 
                current_message, 
                user_context
            )
            
            # Wysyła do LLM do analizy
            analysis_result = await self._analyze_for_rag_query(analysis_prompt)
            
            if analysis_result.is_error:
                return Result.error(f"Analiza RAG nie powiodła się: {analysis_result.error}")
            
            analysis = analysis_result.value
            vector_query = analysis.get("vector_query", "")
            
            if not vector_query:
                return Result.error("Nie wygenerowano zapytania wektorowego")
            
            self.logger.info(f"🧠 LLM zdecydował o zapytaniu wektorowym: {vector_query}")
            return Result.success(vector_query)
            
        except Exception as e:
            return Result.error(f"Decyzja o dynamicznym zapytaniu RAG nie powiodła się: {str(e)}")
    
    def _build_rag_analysis_prompt(
        self, 
        conversation_context: List[ChatMessage], 
        current_message: str,
        user_context: Optional[dict] = None
    ) -> str:
        """Buduje prompt analizy dla decyzji o zapytaniu RAG"""
        
        # Buduje historię rozmowy
        conversation_text = ""
        for msg in conversation_context[-4:]:  # Ostatnie 4 wiadomości
            role = "User" if msg.role == MessageRole.USER else "Assistant"
            conversation_text += f"{role}: {msg.content}\n"
        
        # TODO: Dodać kontekst użytkownika gdy system logowania zostanie zaimplementowany
        user_context_info = ""
        if user_context:
            user_context_info = f"\nKONTEKST UŻYTKOWNIKA:\nRola: {user_context.get('role', 'user')}\nUprawnienia: {user_context.get('permissions', [])}"
        
        analysis_prompt = f"""Jesteś agentem analizy rozmów z refleksyjnymi zdolnościami meta-myślenia.

KONTEKST ROZMOWY:
{conversation_text}

OBECNA WIADOMOŚĆ UŻYTKOWNIKA:
{current_message}
{user_context_info}

ZADANIE ANALIZY:
Przeanalizuj ten kontekst rozmowy i zdecyduj jakie zapytanie zadać do bazy wektorowej.
1. Jaki jest główny temat/przedmiot dyskusji?
2. Jakie konkretne informacje mogą być potrzebne z bazy wiedzy?
3. Jakie byłoby najbardziej efektywne zapytanie do wyszukania odpowiednich informacji?

WAŻNE: Wszystkie odpowiedzi w JSON muszą być po POLSKU, szczególnie pole "vector_query" - to zapytanie będzie użyte do wyszukania w bazie wektorowej i musi być w języku polskim.

Pola w odpowiedzi JSON:
- main_topic - główny temat/przedmiot dyskusji (po polsku)
- information_needed - konkretne informacje potrzebne z bazy wiedzy (po polsku)
- vector_query - krótkie zapytanie do bazy wektorowej które zamienię na embedding i będzie użyte do wyszukania w bazie wektorowej.
- reasoning - rozumowanie, które zostało wykonane przez LLM do wygenerowania zapytania wektorowego (po polsku)

Odpowiedz w formacie JSON (wszystkie wartości stringów po polsku):
{{
    "main_topic": "string",
    "information_needed": "string", 
    "vector_query": "string",
    "reasoning": "string"
}}"""
        
        return analysis_prompt
    
    async def _analyze_for_rag_query(self, analysis_prompt: str) -> Result[Dict[str, Any], str]:
        """Analizuje rozmowę używając LLM do decyzji o zapytaniu RAG"""
        try:
            import time
            start_time = time.time()
            
            # Używa LLM Service z ChatAgentService (z Container)
            self.logger.info("=" * 80)
            self.logger.info(f"🔍 DYNAMIC RAG: Rozpoczynam analizę dla zapytania RAG")
            self.logger.info(f"   Prompt length: {len(analysis_prompt)} znaków")
            self.logger.info("=" * 80)
            
            # Buduje wiadomości dla LLM
            from datetime import datetime
            analysis_messages = [
                ChatMessage(role=MessageRole.SYSTEM, content="Jesteś ekspertem w analizie rozmów i generowaniu zapytań do bazy wektorowej.", timestamp=datetime.now()),
                ChatMessage(role=MessageRole.USER, content=analysis_prompt, timestamp=datetime.now())
            ]
            
            self.logger.info(f"📤 Wywołuję llm_service.get_completion...")
            llm_start = time.time()
            
            # Wywołuje LLM Service bezpośrednio (z Container)
            result = await self.llm_service.get_completion(analysis_messages)
            
            llm_time = time.time() - llm_start
            self.logger.info(f"⏱️ LLM odpowiedział w {llm_time:.2f}s")
            
            if result.is_success:
                response_value = result.value
                self.logger.info(f"✅ Otrzymano odpowiedź od LLM: {type(response_value)} - {len(str(response_value))} znaków")
                self.logger.info(f"   Preview: {str(response_value)[:200]}...")
                
                # LLM Service zwraca bezpośrednio string
                response = str(response_value)
                
                # NOWA METODA: Użyj JSONEmbeddingService do parsowania
                self.logger.info(f"📝 Używanie JSONEmbeddingService do parsowania...")
                parse_start = time.time()
                
                processing_result = await self.json_embedding_service.process_json_for_rag(
                    response,
                    query_key="vector_query",
                    auto_create_embedding=True
                )
                
                parse_time = time.time() - parse_start
                self.logger.info(f"⏱️ Parsowanie JSON zajęło {parse_time:.2f}s")
                
                if processing_result.is_success:
                    processed_data = processing_result.value
                    parsed_json = processed_data["parsed_json"]
                    self.logger.info(f"✅ Successfully parsed JSON with {len(parsed_json)} keys")
                    
                    # Sprawdź czy mamy embedding
                    if "embedding" in processed_data:
                        self.logger.info(f"📊 Utworzono embedding o wymiarach: {processed_data['embedding_dim']}")
                    
                    total_time = time.time() - start_time
                    self.logger.info(f"✅ DYNAMIC RAG: Analiza zakończona sukcesem w {total_time:.2f}s")
                    self.logger.info("=" * 80)
                    
                    return Result.success(parsed_json)
                else:
                    self.logger.warning(f"⚠️ JSON parsing failed, fallback to text extraction: {processing_result.error}")
                    # Fallback: wyciąga informacje z odpowiedzi tekstowej
                    analysis = self._extract_rag_analysis_from_text(response)
                    total_time = time.time() - start_time
                    self.logger.info(f"⚠️ DYNAMIC RAG: Użyto fallback w {total_time:.2f}s")
                    self.logger.info("=" * 80)
                    return Result.success(analysis)
            else:
                total_time = time.time() - start_time
                self.logger.error(f"❌ DYNAMIC RAG: Analiza LLM nie powiodła się w {total_time:.2f}s: {result.error}")
                self.logger.info("=" * 80)
                return Result.error(f"Analiza LLM nie powiodła się: {result.error}")
                
        except Exception as e:
            import traceback
            total_time = time.time() - start_time if 'start_time' in locals() else 0
            self.logger.error(f"❌ DYNAMIC RAG: Błąd analizy RAG w {total_time:.2f}s: {str(e)}")
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            self.logger.info("=" * 80)
            return Result.error(f"Błąd analizy RAG: {str(e)}")
    
    def _extract_rag_analysis_from_text(self, text: str) -> Dict[str, Any]:
        """Wyciąga analizę RAG z odpowiedzi tekstowej gdy parsowanie JSON nie powiedzie się"""
        return {
            "main_topic": "analiza_rozmowy",
            "information_needed": "informacje_kontekstowe",
            "vector_query": text[:100] + "...",  # Używa pierwszych 100 znaków
            "reasoning": "Wyciągnięte z odpowiedzi tekstowej",
            "raw_response": text
        }
    
    async def search_with_filtering(
        self, 
        query: str, 
        score_threshold: float = 0.85,
        limit: int = 20,
        user_context: Optional[dict] = None
    ) -> Result[List[Dict[str, Any]], str]:
        """Wyszukuje w bazie wektorowej z filtrowaniem (jak GetValueFromVDB w ChatElioraReflect)"""
        try:
            self.logger.info("=" * 80)
            self.logger.info(f"🔍 DYNAMIC RAG: search_with_filtering")
            self.logger.info(f"   Query: '{query}'")
            self.logger.info(f"   Score threshold: {score_threshold}")
            self.logger.info(f"   Limit: {limit}")
            self.logger.info("=" * 80)
            
            # Wykonuje wyszukiwanie wektorowe przez KnowledgeService
            self.logger.info(f"📤 Wywołuję knowledge_service.search_knowledge_base...")
            search_result = await self.knowledge_service.search_knowledge_base(query, limit=limit)
            
            if search_result.is_error:
                self.logger.error(f"❌ Błąd wyszukiwania: {search_result.error}")
                return Result.error(f"Wyszukiwanie wektorowe nie powiodło się: {search_result.error}")
            
            vector_results = search_result.value
            self.logger.info(f"📥 Otrzymano {len(vector_results)} wyników z knowledge_service")
            
            if not vector_results:
                self.logger.warning("⚠️ Knowledge service zwrócił pustą listę wyników!")
                return Result.success([])
            
            # Loguj wszystkie wyniki przed filtrowaniem
            self.logger.info("=" * 80)
            self.logger.info(f"📋 WYNIKI PRZED FILTROWANIEM (score_threshold={score_threshold}):")
            self.logger.info("=" * 80)
            for i, result in enumerate(vector_results[:5], 1):  # Loguj pierwsze 5
                if isinstance(result, dict):
                    score = result.get('score', 0.0)
                    topic = result.get('topic', 'N/A')
                    self.logger.info(f"   {i}. Score={score:.4f}, Topic='{topic}', Pass={score >= score_threshold}")
                else:
                    self.logger.info(f"   {i}. Result type: {type(result)}, Value: {str(result)[:100]}")
            
            # Filtruje wyniki według score (jak w ChatElioraReflect)
            filtered_results = []
            for result in vector_results:
                if isinstance(result, dict):
                    score = result.get('score', 0.0)
                    if score >= score_threshold:
                        filtered_results.append(result)
                        self.logger.info(f"   ✅ Dodano wynik: Score={score:.4f} >= {score_threshold}")
                    else:
                        self.logger.debug(f"   ❌ Odrzucono wynik: Score={score:.4f} < {score_threshold}")
                else:
                    # Jeśli brak informacji o score, uwzględnia wszystkie wyniki
                    self.logger.warning(f"   ⚠️ Wynik bez score, dodaję bez filtrowania: {type(result)}")
                    filtered_results.append(result)
            
            self.logger.info("=" * 80)
            self.logger.info(f"✅ PO FILTROWANIU: {len(filtered_results)} wyników (z {len(vector_results)} przed filtrowaniem)")
            self.logger.info("=" * 80)
            
            if not filtered_results:
                self.logger.warning(f"⚠️ Wszystkie wyniki zostały odrzucone przez score_threshold={score_threshold}!")
                self.logger.warning(f"   Rozważ obniżenie score_threshold lub sprawdzenie czy baza wektorowa ma odpowiednie dane")
            
            # TODO: Dodać filtrowanie specyficzne dla użytkownika gdy system logowania zostanie zaimplementowany
            if user_context and user_context.get('role') != 'admin':
                # Użytkownicy nie-admin otrzymują ograniczone wyniki
                filtered_results = filtered_results[:10]
            
            return Result.success(filtered_results)
            
        except Exception as e:
            self.logger.error(f"❌ Błąd w search_with_filtering: {str(e)}")
            import traceback
            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return Result.error(f"Przefiltrowane wyszukiwanie wektorowe nie powiodło się: {str(e)}")
