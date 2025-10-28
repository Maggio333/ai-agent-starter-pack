# application/services/conversation_analysis_agent.py
from typing import Dict, List, Optional, Any
from datetime import datetime
from domain.utils.result import Result
from domain.services.rop_service import ROPService
from domain.entities.chat_message import ChatMessage, MessageRole
from application.services.chat_agent_service import ChatAgentService

class ConversationAnalysisAgent:
    """Agent that analyzes conversation context and decides what to query from vector database"""
    
    def __init__(self, chat_agent_service: ChatAgentService):
        self.rop_service = ROPService()
        self.chat_agent_service = chat_agent_service
        
    async def analyze_and_decide_vector_query(
        self, 
        system_prompt: str,
        conversation_context: List[ChatMessage],
        current_user_message: str
    ) -> Result[Dict[str, Any], str]:
        """Analyze conversation context and decide what to query from vector database"""
        try:
            # STEP 1: Build analysis prompt
            analysis_prompt = self._build_analysis_prompt(
                system_prompt, 
                conversation_context, 
                current_user_message
            )
            
            # STEP 2: Analyze conversation using LLM
            analysis_result = await self._analyze_conversation(analysis_prompt)
            
            if analysis_result.is_error:
                return Result.error(f"Analysis failed: {analysis_result.error}")
            
            analysis = analysis_result.value
            
            # STEP 3: Decide vector query based on analysis
            vector_query_result = await self._decide_vector_query(analysis)
            
            if vector_query_result.is_error:
                return Result.error(f"Vector query decision failed: {vector_query_result.error}")
            
            vector_query = vector_query_result.value
            
            # STEP 4: Execute vector search
            vector_search_result = await self.chat_agent_service.search_knowledge_base(
                vector_query, 
                limit=20
            )
            
            # Safely handle vector results
            vector_results = []
            if vector_search_result.is_success and isinstance(vector_search_result.value, list):
                vector_results = vector_search_result.value
            elif vector_search_result.is_success and isinstance(vector_search_result.value, str):
                # If it's a string (error message), treat as empty results
                self.logger.warning(f"Vector search returned string instead of list: {vector_search_result.value}")
                vector_results = []
            else:
                self.logger.warning(f"Vector search failed: {vector_search_result.error if vector_search_result.is_error else 'Unknown error'}")
                vector_results = []
            
            return Result.success({
                "analysis": analysis,
                "vector_query": vector_query,
                "vector_results": vector_results,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            return Result.error(f"Conversation analysis failed: {str(e)}")
    
    def _build_analysis_prompt(
        self, 
        system_prompt: str, 
        conversation_context: List[ChatMessage], 
        current_user_message: str
    ) -> str:
        """Build analysis prompt for LLM"""
        
        # Build conversation history
        conversation_text = ""
        for msg in conversation_context[-4:]:  # Last 4 messages (2 interactions)
            role = "User" if msg.role == MessageRole.USER else "Assistant"
            conversation_text += f"{role}: {msg.content}\n"
        
        analysis_prompt = f"""Jesteś agentem analizy rozmów z refleksyjnymi zdolnościami meta-myślenia.

SYSTEM PROMPT (Reflective Idioms):
{system_prompt}

KONTEKST ROZMOWY:
{conversation_text}

OBECNA WIADOMOŚĆ UŻYTKOWNIKA:
{current_user_message}

ZADANIE ANALIZY:
Przeanalizuj ten kontekst rozmowy i określ:
1. Jaki jest główny temat/przedmiot dyskusji?
2. Jakie konkretne informacje mogą być potrzebne z bazy wiedzy?
3. Jakie byłoby najbardziej efektywne zapytanie do wyszukania odpowiednich informacji?

Odpowiedz w formacie JSON:
{{
    "main_topic": "string",
    "information_needed": "string", 
    "suggested_vector_query": "string",
    "reasoning": "string"
}}"""
        
        return analysis_prompt
    
    async def _analyze_conversation(self, analysis_prompt: str) -> Result[Dict[str, Any], str]:
        """Analyze conversation using LLM"""
        try:
            # Use orchestration service to process analysis
            result = await self.chat_agent_service.orchestration_service.process_request(analysis_prompt)
            
            if result.is_success:
                # Safely handle different return types
                response_value = result.value
                
                # If it's a string, treat it as response text
                if isinstance(response_value, str):
                    response = response_value
                # If it's a dict, try to get response field
                elif isinstance(response_value, dict):
                    response = response_value.get("response", str(response_value))
                # If it's a list, join it as text
                elif isinstance(response_value, list):
                    response = " ".join([str(item) for item in response_value])
                else:
                    response = str(response_value)
                
                # Try to parse JSON response
                try:
                    import json
                    analysis = json.loads(response)
                    return Result.success(analysis)
                except json.JSONDecodeError:
                    # Fallback: extract information from text response
                    analysis = self._extract_analysis_from_text(response)
                    return Result.success(analysis)
            else:
                return Result.error(f"LLM analysis failed: {result.error}")
                
        except Exception as e:
            return Result.error(f"Analysis error: {str(e)}")
    
    def _extract_analysis_from_text(self, text: str) -> Dict[str, Any]:
        """Extract analysis from text response when JSON parsing fails"""
        return {
            "main_topic": "conversation_analysis",
            "information_needed": "contextual_information",
            "suggested_vector_query": text[:100] + "...",  # Use first 100 chars
            "reasoning": "Extracted from text response",
            "raw_response": text
        }
    
    async def _decide_vector_query(self, analysis: Dict[str, Any]) -> Result[str, str]:
        """Decide what to query from vector database based on analysis"""
        try:
            suggested_query = analysis.get("suggested_vector_query", "")
            main_topic = analysis.get("main_topic", "")
            information_needed = analysis.get("information_needed", "")
            
            # Build final vector query
            if suggested_query and len(suggested_query.strip()) > 0:
                vector_query = suggested_query.strip()
            elif main_topic and len(main_topic.strip()) > 0:
                vector_query = main_topic.strip()
            elif information_needed and len(information_needed.strip()) > 0:
                vector_query = information_needed.strip()
            else:
                vector_query = "general knowledge information"
            
            return Result.success(vector_query)
            
        except Exception as e:
            return Result.error(f"Vector query decision error: {str(e)}")
    
    async def get_analysis_stats(self) -> Result[Dict[str, Any], str]:
        """Get analysis agent statistics"""
        try:
            stats = {
                "agent_name": "ConversationAnalysisAgent",
                "capabilities": [
                    "conversation_analysis",
                    "vector_query_decision", 
                    "context_understanding",
                    "meta_thinking"
                ],
                "dependencies": {
                    "chat_agent_service": self.chat_agent_service is not None,
                    "rop_service": self.rop_service is not None
                },
                "timestamp": datetime.now().isoformat()
            }
            return Result.success(stats)
        except Exception as e:
            return Result.error(f"Stats error: {str(e)}")
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Health check for analysis agent"""
        try:
            health_data = {
                "status": "healthy",
                "service": "ConversationAnalysisAgent",
                "dependencies": {
                    "chat_agent_service": self.chat_agent_service is not None,
                    "rop_service": self.rop_service is not None
                },
                "timestamp": datetime.now().isoformat()
            }
            return Result.success(health_data)
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
