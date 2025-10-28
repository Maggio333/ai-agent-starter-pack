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
        
        # 1. Globalne prompty systemowe
        messages.extend(self.get_global_system_prompts(user_context))
        
        # 2. Dodatkowe prompty systemowe
        messages.extend(self.get_additional_system_prompts(user_context))
        
        # 3. WSZYSTKIE IDIOMY RAZEM - jeden system prompt (jak SetBaseIdioms)
        if idioms and any(idiom.strip() for idiom in idioms if idiom):
            # Łączy wszystkie idiomy w jeden prompt
            combined_idioms = "\n\n".join([idiom.strip() for idiom in idioms if idiom and idiom.strip()])
            messages.append(ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.system_prompts.get_idioms_prompt(combined_idioms),
                timestamp=datetime.now()
            ))
            self.logger.info(f"🎭 PromptService: Dodano {len([i for i in idioms if i and i.strip()])} idiomów w jednym system prompt")
        else:
            self.logger.warning(f"⚠️ PromptService: Brak idiomów do dodania")
        
        # 4. Historia rozmowy (ostatnie 3 wiadomości)
        messages.extend(conversation_history[-3:])
        
        # 5. Aktualna wiadomość użytkownika
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
