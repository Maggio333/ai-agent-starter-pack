# infrastructure/services/email_service.py
import smtplib
import re
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from domain.services.IEmailService import IEmailService
from domain.utils.result import Result

class EmailService(IEmailService):
    """Implementacja serwisu wysyłania emaili przez SMTP"""
    
    def __init__(self, smtp_host: str = "localhost", smtp_port: int = 587, 
                 username: Optional[str] = None, password: Optional[str] = None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
        
        # Proste szablony emaili
        self.templates = {
            "welcome": {
                "subject": "Witamy w {app_name}!",
                "body": "Cześć {name}!\n\nWitamy w {app_name}!\n\nDziękujemy za rejestrację."
            },
            "notification": {
                "subject": "Powiadomienie: {title}",
                "body": "Cześć {name}!\n\n{message}\n\nPozdrawiamy,\nZespół {app_name}"
            },
            "error": {
                "subject": "Błąd w systemie",
                "body": "Wystąpił błąd: {error_message}\n\nCzas: {timestamp}"
            }
        }
    
    async def send_email(self, to: str, subject: str, body: str, 
                        from_email: Optional[str] = None) -> Result[bool, str]:
        """Wysyła pojedynczy email"""
        try:
            # Walidacja email
            validation_result = await self.validate_email(to)
            if not validation_result.is_success:
                return Result.error(f"Invalid email address: {validation_result.error}")
            
            # Tworzenie wiadomości
            msg = MIMEMultipart()
            msg['From'] = from_email or self.username or "noreply@example.com"
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Wysyłanie (symulacja - w rzeczywistości użyłbyś prawdziwego SMTP)
            self.logger.info(f"📧 Email sent to {to}: {subject}")
            self.logger.debug(f"Email body: {body[:100]}...")
            
            # Symulacja wysyłania
            await self._simulate_smtp_send(msg)
            
            return Result.success(True)
            
        except Exception as e:
            self.logger.error(f"Failed to send email to {to}: {e}")
            return Result.error(f"Failed to send email: {str(e)}")
    
    async def send_bulk_email(self, emails: List[Dict[str, str]]) -> Result[List[bool], str]:
        """Wysyła wiele emaili jednocześnie"""
        try:
            results = []
            
            for email_data in emails:
                to = email_data.get('to')
                subject = email_data.get('subject')
                body = email_data.get('body')
                from_email = email_data.get('from')
                
                if not all([to, subject, body]):
                    results.append(False)
                    continue
                
                result = await self.send_email(to, subject, body, from_email)
                results.append(result.is_success)
            
            success_count = sum(results)
            self.logger.info(f"📧 Bulk email sent: {success_count}/{len(emails)} successful")
            
            return Result.success(results)
            
        except Exception as e:
            self.logger.error(f"Failed to send bulk emails: {e}")
            return Result.error(f"Failed to send bulk emails: {str(e)}")
    
    async def send_template_email(self, to: str, template_name: str, 
                                 template_data: Dict[str, Any]) -> Result[bool, str]:
        """Wysyła email z szablonu"""
        try:
            if template_name not in self.templates:
                return Result.error(f"Template '{template_name}' not found")
            
            template = self.templates[template_name]
            
            # Zastąpienie zmiennych w szablonie
            subject = template['subject'].format(**template_data)
            body = template['body'].format(**template_data)
            
            return await self.send_email(to, subject, body)
            
        except Exception as e:
            self.logger.error(f"Failed to send template email: {e}")
            return Result.error(f"Failed to send template email: {str(e)}")
    
    async def validate_email(self, email: str) -> Result[bool, str]:
        """Waliduje adres email"""
        try:
            if not email or not isinstance(email, str):
                return Result.error("Email address is required")
            
            # Prosty regex dla walidacji email
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if re.match(pattern, email):
                return Result.success(True)
            else:
                return Result.error(f"Invalid email format: {email}")
                
        except Exception as e:
            return Result.error(f"Email validation failed: {str(e)}")
    
    async def _simulate_smtp_send(self, msg: MIMEMultipart):
        """Symuluje wysyłanie przez SMTP (dla demo)"""
        import asyncio
        await asyncio.sleep(0.1)  # Symulacja opóźnienia sieci
        self.logger.debug(f"SMTP simulation: Message sent to {msg['To']}")
    
    def add_template(self, name: str, subject: str, body: str):
        """Dodaje nowy szablon email"""
        self.templates[name] = {
            "subject": subject,
            "body": body
        }
        self.logger.info(f"Added email template: {name}")
    
    def get_available_templates(self) -> List[str]:
        """Zwraca listę dostępnych szablonów"""
        return list(self.templates.keys())
