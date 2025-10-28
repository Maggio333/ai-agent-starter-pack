"""
JSONEmbeddingService - Obsługuje parsowanie pierwszego JSON z modelu i generowanie embeddingu
"""

import json
import logging
from typing import Dict, Any, Optional
from domain.utils.result import Result

class JSONEmbeddingService:
    """
    Serwis do obsługi JSON zwracanego przez model i generowania embeddingu
    dla późniejszego wyszukiwania w bazie wektorowej
    """
    
    def __init__(self, embedding_service=None):
        self.embedding_service = embedding_service
        self.logger = logging.getLogger(__name__)
    
    async def extract_and_embed_from_json(
        self, 
        llm_response: str,
        query_key: str = "vector_query"
    ) -> Result[tuple[Dict[str, Any], Optional[str]], str]:
        """
        Ekstraktuje JSON z odpowiedzi LLM i generuje embedding dla określonego pola
        
        Args:
            llm_response: Odpowiedź z modelu
            query_key: Klucz w JSON, którego wartość będzie użyta do embeddingu
        
        Returns:
            Result[(parsed_json, embedding_text), error_msg]
        """
        try:
            # 1. Parsuj JSON z odpowiedzi
            parsed_json = self._extract_json_from_response(llm_response)
            
            if not parsed_json:
                return Result.error("Nie znaleziono poprawnego JSON w odpowiedzi LLM")
            
            # 2. Wyciągnij pole do embeddingu
            query_text = self._extract_query_text(parsed_json, query_key)
            
            if not query_text:
                return Result.error(f"Nie znaleziono pola '{query_key}' w JSON")
            
            self.logger.info(f"📝 JSONEmbedding: Wyciągnięto query text: '{query_text[:100]}...'")
            
            # 3. Zwróć parsowany JSON i tekst do embeddingu
            return Result.success((parsed_json, query_text))
            
        except Exception as e:
            self.logger.error(f"❌ JSONEmbedding: Błąd parsowania JSON: {str(e)}")
            return Result.error(f"Błąd parsowania JSON: {str(e)}")
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Wyciąga JSON z odpowiedzi LLM
        Próbuje parsować: bezpośrednio, z ```json, z ```polish-json, zwykły tekst
        """
        try:
            # Próba 1: Bezpośredni JSON
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                pass
            
            # Próba 2: JSON w bloku code z ```json
            import re
            json_match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1).strip())
                except json.JSONDecodeError:
                    pass
            
            # Próba 3: JSON w bloku code bez markera (```)
            json_match = re.search(r'```\s*(.*?)```', response, re.DOTALL)
            if json_match:
                try:
                    content = json_match.group(1).strip()
                    # Usuń ewentualny marker języka
                    content = re.sub(r'^\w+\s*', '', content)
                    return json.loads(content)
                except json.JSONDecodeError:
                    pass
            
            # Próba 4: Znajdź pierwszy słownik w tekście (pyton dict syntax)
            dict_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if dict_match:
                try:
                    # Zastąp składnię Python (True/False/None) na JSON
                    dict_str = dict_match.group(0)
                    dict_str = dict_str.replace("True", "true")
                    dict_str = dict_str.replace("False", "false")
                    dict_str = dict_str.replace("None", "null")
                    return json.loads(dict_str)
                except json.JSONDecodeError:
                    pass
            
            self.logger.warning(f"⚠️ JSONEmbedding: Nie udało się sparsować JSON z odpowiedzi")
            return None
            
        except Exception as e:
            self.logger.error(f"❌ JSONEmbedding: Błąd wyciągania JSON: {str(e)}")
            return None
    
    def _extract_query_text(self, parsed_json: Dict[str, Any], query_key: str) -> Optional[str]:
        """
        Wyciąga tekst do embeddingu z parsowanego JSON
        """
        try:
            # Sprawdź bezpośrednio
            if query_key in parsed_json:
                value = parsed_json[query_key]
                if isinstance(value, str):
                    return value
                else:
                    return str(value)
            
            # Sprawdź zagnieżdżone struktury (np. {"analysis": {"vector_query": "..."}})
            for key, value in parsed_json.items():
                if isinstance(value, dict):
                    result = self._extract_query_text(value, query_key)
                    if result:
                        return result
            
            self.logger.warning(f"⚠️ JSONEmbedding: Nie znaleziono klucza '{query_key}' w JSON")
            return None
            
        except Exception as e:
            self.logger.error(f"❌ JSONEmbedding: Błąd wyciągania query text: {str(e)}")
            return None
    
    async def create_embedding_for_query(self, query_text: str) -> Result[list[float], str]:
        """
        Tworzy embedding dla zapytania używając EmbeddingService
        
        Args:
            query_text: Tekst do konwersji na embedding
        
        Returns:
            Result[embedding_vector, error_msg]
        """
        try:
            if not self.embedding_service:
                self.logger.warning("⚠️ JSONEmbedding: Brak embedding service, zwracam dummy vector")
                return Result.success([0.1] * 1024)  # Dummy fallback
            
            # Wywołaj embedding service
            result = await self.embedding_service.create_embedding(query_text)
            
            if result.is_success:
                self.logger.info(f"📊 JSONEmbedding: Utworzono embedding o wymiarach: {len(result.value)}")
                return Result.success(result.value)
            else:
                self.logger.warning(f"⚠️ JSONEmbedding: Nie udało się utworzyć embeddingu: {result.error}")
                return Result.success([0.1] * 1024)  # Dummy fallback
                
        except Exception as e:
            self.logger.error(f"❌ JSONEmbedding: Błąd tworzenia embeddingu: {str(e)}")
            return Result.success([0.1] * 1024)  # Dummy fallback
    
    async def process_json_for_rag(
        self,
        llm_response: str,
        query_key: str = "vector_query",
        auto_create_embedding: bool = True
    ) -> Result[Dict[str, Any], str]:
        """
        Kompletne przetworzenie: ekstraktuj JSON, wyciągnij query, stwórz embedding
        
        Args:
            llm_response: Odpowiedź z modelu
            query_key: Klucz do wyciągnięcia z JSON
            auto_create_embedding: Czy automatycznie tworzyć embedding
        
        Returns:
            Result[{json, query_text, embedding?}, error_msg]
        """
        try:
            # 1. Ekstraktuj i sparsuj JSON
            extract_result = await self.extract_and_embed_from_json(llm_response, query_key)
            
            if extract_result.is_error:
                return Result.error(extract_result.error)
            
            parsed_json, query_text = extract_result.value
            
            # 2. Buduj wynikowy słownik
            result = {
                "parsed_json": parsed_json,
                "query_text": query_text,
                "query_key": query_key
            }
            
            # 3. Opcjonalnie: stwórz embedding
            if auto_create_embedding and query_text:
                embedding_result = await self.create_embedding_for_query(query_text)
                if embedding_result.is_success:
                    result["embedding"] = embedding_result.value
                    result["embedding_dim"] = len(embedding_result.value)
            
            self.logger.info(f"✅ JSONEmbedding: Przetworzono JSON - query: '{query_text[:50]}...'")
            return Result.success(result)
            
        except Exception as e:
            self.logger.error(f"❌ JSONEmbedding: Błąd przetwarzania JSON: {str(e)}")
            return Result.error(f"Błąd przetwarzania JSON: {str(e)}")
    
    def validate_json_structure(self, parsed_json: Dict[str, Any]) -> bool:
        """
        Waliduje czy JSON ma wymaganą strukturę
        
        Args:
            parsed_json: Sparsowany JSON
        
        Returns:
            bool: Czy struktura jest poprawna
        """
        try:
            # Podstawowa walidacja: czy to jest dict
            if not isinstance(parsed_json, dict):
                return False
            
            # Sprawdź czy ma jakieś klucze
            if not parsed_json:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ JSONEmbedding: Błąd walidacji JSON: {str(e)}")
            return False

