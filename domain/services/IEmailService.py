# domain/services/IEmailService.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from domain.utils.result import Result

class IEmailService(ABC):  # Interfejs zgodny z konwencją C# dla czytelności
    """Interfejs serwisu wysyłania emaili"""
    
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str, 
                        from_email: Optional[str] = None) -> Result[bool, str]:
        """Wysyła pojedynczy email"""
        pass
    
    @abstractmethod
    async def send_bulk_email(self, emails: List[Dict[str, str]]) -> Result[List[bool], str]:
        """Wysyła wiele emaili jednocześnie"""
        pass
    
    @abstractmethod
    async def send_template_email(self, to: str, template_name: str, 
                                 template_data: Dict[str, Any]) -> Result[bool, str]:
        """Wysyła email z szablonu"""
        pass
    
    @abstractmethod
    async def validate_email(self, email: str) -> Result[bool, str]:
        """Waliduje adres email"""
        pass
    
    async def health_check(self) -> Result[dict, str]:
        """Sprawdza stan serwisu email"""
        try:
            # Test walidacji email
            test_result = await self.validate_email("test@example.com")
            if test_result.is_success:
                health_data = {
                    'status': 'healthy',
                    'service': self.__class__.__name__,
                    'type': 'email_service'
                }
                return Result.success(health_data)
            else:
                return Result.error(f"Health check failed: {test_result.error}")
        except Exception as e:
            return Result.error(f"Health check failed: {str(e)}")
