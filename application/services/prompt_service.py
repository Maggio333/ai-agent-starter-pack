import logging
from typing import List, Optional, AsyncGenerator
from datetime import datetime
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.utils.result import Result
from domain.services.SystemPromptsService import SystemPromptsService

class PromptService:
    """Serwis do budowania kompletnych list wiadomości z promptami systemowymi (inspirowany ChatElioraReflect)"""
    
    def __init__(self, knowledge_service=None, system_prompts_service: Optional[SystemPromptsService] = None):
        self.knowledge_service = knowledge_service
        self.system_prompts = system_prompts_service or SystemPromptsService()
        self.logger = logging.getLogger(__name__)
    
    def get_global_system_prompts(self, user_context: Optional[dict] = None) -> List[ChatMessage]:
        """Pobiera globalne prompty systemowe (jak GetGlobalChatMessages w ChatElioraReflect)"""
        prompts = [
            # 1. OSOBOWOŚĆ ELIORA - jeden prompt
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.system_prompts.eliora_personality_prompt,
                timestamp=datetime.now()
            ),
            # 2. KOLORY - jeden prompt
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.system_prompts.color_syntax_prompt,
                timestamp=datetime.now()
            )
        ]
        
        # TODO: Dodać prompty specyficzne dla użytkownika gdy system logowania zostanie zaimplementowany
        if user_context:
            prompts.append(ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.system_prompts.get_user_profile_prompt(user_context),
                timestamp=datetime.now()
            ))
        
        return prompts
    
    def get_additional_system_prompts(self, user_context: Optional[dict] = None) -> List[ChatMessage]:
        """Pobiera dodatkowe prompty systemowe (jak GetAdditionalChatMessage w ChatElioraReflect)"""
        prompts = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.system_prompts.general_conversation_role,
                timestamp=datetime.now()
            )
        ]
        
        # TODO: Dodać prompty specyficzne dla roli gdy system logowania zostanie zaimplementowany
        if user_context and user_context.get('role') == 'admin':
            prompts.append(ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.system_prompts.admin_role_prompt,
                timestamp=datetime.now()
            ))
        
        return prompts
    
    def build_complete_message_list(
        self, 
        user_message: str, 
        idioms: List[str], 
        conversation_history: List[ChatMessage],
        user_context: Optional[dict] = None
    ) -> List[ChatMessage]:
        """Buduje kompletną listę wiadomości (jak GetPromptWindowList w ChatElioraReflect)"""
        self.logger.info(f"🎭 PromptService: Budowanie listy wiadomości - user_message: '{user_message}', idioms: {len(idioms)}, history: {len(conversation_history)}")
        messages = []
        
        # 1-3. SKLEJ WSZYSTKIE SYSTEM PROMPTY W JEDEN
        persona = self.system_prompts.eliora_personality_prompt
        color = self.system_prompts.color_syntax_prompt
        general_role = self.system_prompts.general_conversation_role
        user_profile = self.system_prompts.get_user_profile_prompt(user_context) if user_context else None

        # Zbierz idiomy do jednego bloku (opcjonalnie)
        idioms_block = None
        if idioms and any(idm and idm.strip() for idm in idioms):
            combined_idioms = "\n\n".join([idm.strip() for idm in idioms if idm and idm.strip()])
            idioms_block = self.system_prompts.get_idioms_prompt(combined_idioms)
            self.logger.info(f"🎭 PromptService: Połączono {len([i for i in idioms if i and i.strip()])} idiomów w jeden blok")

        # Złóż sekcje w jeden system ChatMessage
        system_sections: List[str] = [
            f"### PERSONA\n{persona}",
            f"### FORMAT\n{color}",
            f"### ROLE\n{general_role}"
        ]
        if user_profile and user_profile.strip():
            system_sections.append(f"### USER PROFILE\n{user_profile}")
        if idioms_block and idioms_block.strip():
            system_sections.append(f"### IDIOMS\n{idioms_block}")

        combined_system_prompt = "\n\n".join(system_sections)
        messages.append(ChatMessage(
            role=MessageRole.SYSTEM,
            content=combined_system_prompt,
            timestamp=datetime.now()
        ))
        
        # 4. Historia rozmowy z filtrowaniem dla poprawnej alternacji ról
        # WAŻNE: LM Studio wymaga: SYSTEM → USER → ASSISTANT → USER → ASSISTANT...
        # Po SYSTEM messages MUSI być USER (nie ASSISTANT!)
        
        filtered_history = []
        if conversation_history:
            # Pobierz tylko USER i ASSISTANT z historii (bez SYSTEM)
            chat_messages = [msg for msg in conversation_history if msg.role in [MessageRole.USER, MessageRole.ASSISTANT]]
            
            # KROK 1: Usuń ostatnią USER (bo dodamy nową w kroku 5)
            if chat_messages and chat_messages[-1].role == MessageRole.USER:
                chat_messages.pop()
                self.logger.info(f"🎭 PromptService: Usunięto ostatnią wiadomość USER")
            
            # KROK 2: Jeśli pierwsza wiadomość to ASSISTANT - usuń ją (po SYSTEM musi być USER!)
            while chat_messages and chat_messages[0].role == MessageRole.ASSISTANT:
                removed = chat_messages.pop(0)
                self.logger.info(f"🎭 PromptService: Usunięto wiadomość ASSISTANT z początku (po SYSTEM musi być USER)")
            
            # KROK 3: Zbuduj pary USER→ASSISTANT
            pairs = []
            i = 0
            while i < len(chat_messages):
                if i < len(chat_messages) and chat_messages[i].role == MessageRole.USER:
                    user_msg = chat_messages[i]
                    # Sprawdź czy następna to ASSISTANT
                    if i + 1 < len(chat_messages) and chat_messages[i + 1].role == MessageRole.ASSISTANT:
                        assistant_msg = chat_messages[i + 1]
                        pairs.append((user_msg, assistant_msg))
                        i += 2
                    else:
                        # USER bez ASSISTANT - pomiń
                        i += 1
                else:
                    # ASSISTANT bez poprzedzającego USER - pomiń
                    i += 1
            
            # KROK 4: Weź ostatnie pary (max 2 pary = 4 wiadomości)
            if pairs:
                last_pairs = pairs[-2:] if len(pairs) > 2 else pairs
                for user_msg, assistant_msg in last_pairs:
                    filtered_history.append(user_msg)
                    filtered_history.append(assistant_msg)
                self.logger.info(f"🎭 PromptService: Dodano {len(last_pairs)} par (user→assistant)")
        
        self.logger.info(f"🎭 PromptService: Historia rozmowy - całkowita: {len(conversation_history)}, po filtrowaniu: {len(filtered_history)}")
        if filtered_history:
            for i, hist_msg in enumerate(filtered_history, 1):
                self.logger.info(f"🎭   Historia {i}: {hist_msg.role.value} - {hist_msg.content[:100]}...")
        
        messages.extend(filtered_history)
        
        # 5. Aktualna wiadomość użytkownika (zawsze dodajemy na końcu)
        if user_message and user_message.strip():
            messages.append(ChatMessage(
                role=MessageRole.USER,
                content=user_message,
                timestamp=datetime.now()
            ))
            self.logger.info(f"🎭 PromptService: Dodano wiadomość użytkownika: '{user_message}'")
        else:
            self.logger.error(f"❌ PromptService: Pusta wiadomość użytkownika!")
            raise ValueError("User message cannot be empty")
        
        # AREK TESTY: Sprawdź czy content nie jest obcięty w żadnej wiadomości
        #self.logger.info("=" * 80)
        #self.logger.info("AREK TESTY: SPRAWDZENIE CONTENT W WSZYSTKICH WIADOMOŚCIACH PRZED ZWRÓCENIEM")
        #self.logger.info("=" * 80)
        #for i, msg in enumerate(messages, 1):
            #self.logger.info(f"\nWIADOMOŚĆ #{i} W LISTACH:")
            #self.logger.info(f"  ROLE: {msg.role.value}")
            #self.logger.info(f"  CONTENT DŁUGOŚĆ: {len(msg.content)} znaków")
            #self.logger.info(f"  CONTENT (PEŁNY - linia po linii):")
            #for line_num, line in enumerate(msg.content.split('\n'), 1):
            #    self.logger.info(f"    [{line_num:03d}] {line}")
        #self.logger.info("=" * 80)
        
        self.logger.info(f"🎭 PromptService: Zbudowano {len(messages)} wiadomości")
        return messages
    
    async def send_to_llm_streaming(
        self, 
        messages: List[ChatMessage], 
        llm_service
    ) -> AsyncGenerator[str, None]:
        """Wysyła do LLM z streamingiem (jak SendStreamToLLM w ChatElioraReflect)"""
        self.logger.info(f"🎭 PromptService: Wysyłanie {len(messages)} wiadomości do LLM")
        
        # Debug: sprawdź czy messages nie są puste
        for i, msg in enumerate(messages):
            self.logger.info(f"🎭 Wiadomość {i+1}: {msg.role.value} - {msg.content[:100]}...")     

        async for chunk in llm_service.stream_completion(messages):
            if chunk.is_success:
                if chunk.value:  # Sprawdź czy chunk nie jest pusty
                    yield chunk.value
                else:
                    self.logger.warning("⚠️ PromptService: Otrzymano pusty chunk od LLM")
            else:
                self.logger.error(f"❌ Błąd streamingu LLM: {chunk.error}")
                break
