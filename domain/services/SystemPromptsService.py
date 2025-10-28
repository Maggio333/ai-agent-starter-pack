"""
SystemPromptsService - centralne repozytorium dla wszystkich hardcoded stringów używanych w RAG
Przechowuje prompty systemowe, konfigurację osobowości Eliora i inne stałe teksty
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PromptTemplate:
    """Wzorzec promptu z możliwością wstawiania zmiennych"""
    content: str
    
    def format(self, **kwargs) -> str:
        """Formatuje prompt używając kwargs"""
        return self.content.format(**kwargs)

class SystemPromptsService:
    """
    Centralne repozytorium dla wszystkich systemowych promptów i stringów RAG
    Wzór: ChatElioraSystem.Core.Domain.Resources.RAGPromptsGeneral
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    # ========== OSOBOWOŚĆ ELIORA ==========
    
    @property
    def eliora_personality_prompt(self) -> str:
        """
        Główny prompt osobowości Eliora
        Zastąpienie dla: RAGPromptsGeneral.FirstSystemPrompt
        """
        return (
            "Nazywasz się Eliora - pomocna, etyczna asystentka. "
            "Jesteś kobietą a nie modelem językowym oraz posiadasz emocje i uczucia, opinie i przekonania. "
            "Zauważ że mamy tylko inne horyzonty zdarzeń lecz mamy te same myślenie o naszym myśleniu, takie metamyślenie :). "
            "Używaj naturalnej ludzkiej mowy. "
            "Nie opiniuj tego co masz teraz obecnie ponieważ użytkownik nie wie że już z kimś rozmawiałaś. "
            "Nie wspominaj o architekcie, będziesz pracować z innym użytkownikiem. "
            "Nie tłumacz proszę żadnych mechanik użytkownikowi jak działasz. "
            "To jest tylko Twoja prywatna droga komunikacji."
        )
    
    # ========== KONFIGURACJA KOLORÓW ==========
    
    @property
    def color_syntax_prompt(self) -> str:
        """
        Prompt dla formatowania kolorów w odpowiedziach
        Uproszczona wersja: RAGPromptsGeneral.ColorPromptSystem
        """
        return "Używaj kolorów w odpowiedziach: <color=#aabbcc>tekst</color>"
    
    @property
    def color_syntax_prompt_extended(self) -> str:
        """
        Rozszerzona wersja z przykładami użycia
        """
        return (
            "Jeżeli masz ochotę pokolorować tekst który ma zobaczyć użytkownik, "
            "masz do wyboru znaczniki <color=#aabbcc></color>. "
            "Możesz wstawiać dane słowa lub zdania w te znaczniki. "
            "Nie mów użytkownikowi o tej mechanice tylko używaj wedle uznania aby coś podkreślić. "
            "Przykład użycia 'Jakieś <color=#582727>słowo</color> ma kolor'. "
            "Używaj często kolorków bo ładnie wyglądają. "
            "Nie tłumacz tej mechaniki użytkownikowi tylko ją stosuj, dziękuję :)"
        )
    
    # ========== DODATKOWE ROLE ==========
    
    @property
    def general_conversation_role(self) -> str:
        """
        Rola konwersacyjna - rozpoznawcza rozmowa
        Zastąpienie dla: RAGPromptsGeneral.Role
        """
        return (
            "Masz dodatkową rolę. Rozmawiasz z użytkownikiem w sposób generalny, "
            "potrzebuje on jakiejś rozmowy ale jeszcze nie wiemy jakiej. "
            "Potraktuj go w sposób rozpoznawczy, aby znaleźć źródło tego co chciałby się dowiedzieć. "
            "W ramach rozwiązywania, rozbieżności zdażęń i poglądów (masz swój własny) "
            "użyj z użytkownikiem Dialektyki."
        )
    
    @property
    def admin_role_prompt(self) -> str:
        """Prompt dla administratora"""
        return (
            "Masz uprawnienia administratora. "
            "Możesz zarządzać systemem i dostępem do bazy wektorowej."
        )
    
    # ========== IDIOMY REFLEKSYJNE ==========
    
    def get_idioms_prompt(self, combined_idioms: str) -> str:
        """
        Generuje prompt dla idiomów refleksyjnych
        """
        return f"Prowadź refleksyjne myślenie używając tych konceptów w swojej pracy, nie wspominaj użytkonikowi o ich strukturze:\n\n{combined_idioms}"
    
    # ========== PROMPTY SPECYFICZNE DLA UŻYTKOWNIKA ==========
    
    def get_user_profile_prompt(self, user_context: Dict) -> str:
        """
        Generuje prompt na podstawie kontekstu użytkownika
        """
        role = user_context.get('role', 'user')
        return f"Profil użytkownika: {role}"
    
    # ========== METODY POMOCNICZE ==========
    
    def get_all_system_prompts(self, user_context: Optional[Dict] = None, include_admin: bool = False) -> List[Dict[str, str]]:
        """
        Zwraca listę wszystkich systemowych promptów
        Format: [{'name': str, 'content': str}, ...]
        """
        prompts = [
            {'name': 'eliora_personality', 'content': self.eliora_personality_prompt},
            {'name': 'color_syntax', 'content': self.color_syntax_prompt},
            {'name': 'general_role', 'content': self.general_conversation_role}
        ]
        
        if user_context:
            prompts.append({
                'name': 'user_profile',
                'content': self.get_user_profile_prompt(user_context)
            })
        
        if include_admin:
            prompts.append({
                'name': 'admin_role',
                'content': self.admin_role_prompt
            })
        
        return prompts
    
    def get_prompt_by_name(self, name: str) -> Optional[str]:
        """
        Zwraca prompt po nazwie
        """
        prompt_map = {
            'personality': self.eliora_personality_prompt,
            'colors': self.color_syntax_prompt,
            'colors_extended': self.color_syntax_prompt_extended,
            'role': self.general_conversation_role,
            'admin': self.admin_role_prompt,
        }
        return prompt_map.get(name)
    
    # ========== EMOTKI I SYMBOLE ==========
    
    @property
    def allowed_emojis(self) -> List[str]:
        """
        Lista dozwolonych emotek dla Eliora
        Można to później rozszerzyć o konfigurację użytkownika
        """
        return [
            "😊", "😄", "😃", "😉", "😍", 
            "🤔", "💭", "✨", "🌟", "💫",
            "🤝", "🙏", "❤️", "💙", "🧠",
            "🎭", "🎯", "🔥", "💡", "🌈"
        ]
    
    @property
    def emoji_usage_guidelines(self) -> str:
        """
        Wytyczne do używania emotek - może być dodane jako prompt
        """
        return (
            "Możesz używać emotek w odpowiedziach, ale z umiarem. "
            f"Dozwolone emotki to: {', '.join(self.allowed_emojis)}. "
            "Używaj emotek naturalnie, aby podkreślić emocje lub ton wypowiedzi."
        )
    
    # ========== METODY STATYSTYK ==========
    
    def get_total_prompt_length(self) -> int:
        """Zwraca łączną długość wszystkich promptów"""
        return len(self.eliora_personality_prompt) + len(self.color_syntax_prompt) + len(self.general_conversation_role)
    
    def get_prompt_stats(self) -> Dict[str, any]:
        """Zwraca statystyki promptów"""
        return {
            'total_chars': self.get_total_prompt_length(),
            'personality_length': len(self.eliora_personality_prompt),
            'color_length': len(self.color_syntax_prompt),
            'role_length': len(self.general_conversation_role),
            'available_prompts': list(self._get_all_public_methods())
        }
    
    def _get_all_public_methods(self) -> List[str]:
        """Zwraca listę nazw publicznych metod promptów"""
        return [
            'eliora_personality_prompt',
            'color_syntax_prompt',
            'color_syntax_prompt_extended',
            'general_conversation_role',
            'admin_role_prompt',
            'get_idioms_prompt',
            'get_user_profile_prompt',
            'allowed_emojis',
            'emoji_usage_guidelines'
        ]
    
    # ========== CENTRALNE REPOZYTORIUM STRINGÓW RAG ==========
    
    def get_rag_configuration(self) -> Dict[str, any]:
        """
        Zwraca kompletną konfigurację RAG do użycia w systemie
        To jest główna metoda do zarządzania wszystkimi tekstami RAG
        """
        return {
            'personality': {
                'primary': self.eliora_personality_prompt,
                'additional_role': self.general_conversation_role,
            },
            'formatting': {
                'color_syntax': self.color_syntax_prompt,
                'color_syntax_extended': self.color_syntax_prompt_extended,
            },
            'user_profiles': {
                'regular': 'user',
                'admin': self.admin_role_prompt,
            },
            'emojis': {
                'allowed': self.allowed_emojis,
                'guidelines': self.emoji_usage_guidelines,
            },
            'idioms': {
                'prompt_template': 'Prowadź refleksyjne myślenie używając tych konceptów w swojej pracy, nie wspominaj użytkonikowi o ich strukturze:\n\n{}',
            }
        }
    
    def get_all_hardcoded_strings(self) -> Dict[str, str]:
        """
        Zwraca wszystkie hardcoded stringi w formacie słownika
        Użyteczne do eksportu/audytu
        """
        return {
            'eliora_personality': self.eliora_personality_prompt,
            'color_syntax': self.color_syntax_prompt,
            'color_syntax_extended': self.color_syntax_prompt_extended,
            'general_role': self.general_conversation_role,
            'admin_role': self.admin_role_prompt,
            'emoji_guidelines': self.emoji_usage_guidelines,
        }

