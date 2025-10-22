"""
Web Server Manager Service - Manages different web server implementations
"""
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI

from domain.services.IWebServer import IWebServer
from application.services.google_adk_web_server_service import GoogleADKWebServerService
from application.services.clean_fastapi_web_server_service import CleanFastAPIWebServerService

logger = logging.getLogger(__name__)


class WebServerManagerService:
    """Service for managing web server implementations"""
    
    def __init__(self):
        self._current_server: Optional[IWebServer] = None
        self._server_type: Optional[str] = None
        
    def create_server(self, server_type: str, **kwargs) -> IWebServer:
        """Create web server based on type"""
        try:
            if server_type.lower() == "google_adk":
                logger.info("Creating Google ADK web server...")
                server = GoogleADKWebServerService(**kwargs)
                
            elif server_type.lower() == "clean_fastapi":
                logger.info("Creating clean FastAPI web server...")
                server = CleanFastAPIWebServerService(**kwargs)
                
            else:
                raise ValueError(f"Unknown server type: {server_type}")
            
            self._current_server = server
            self._server_type = server_type
            logger.info(f"Web server '{server_type}' created successfully")
            return server
            
        except Exception as e:
            logger.error(f"Failed to create web server '{server_type}': {e}")
            raise
    
    def get_current_server(self) -> Optional[IWebServer]:
        """Get current web server instance"""
        return self._current_server
    
    def get_current_server_type(self) -> Optional[str]:
        """Get current server type"""
        return self._server_type
    
    def switch_server(self, server_type: str, **kwargs) -> IWebServer:
        """Switch to different server type"""
        logger.info(f"Switching from '{self._server_type}' to '{server_type}'")
        return self.create_server(server_type, **kwargs)
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about current server"""
        if self._current_server is None:
            return {
                "status": "no_server",
                "message": "No web server is currently active"
            }
        
        info = self._current_server.get_app_info()
        info["manager_status"] = "active"
        info["health"] = self._current_server.is_healthy()
        return info
    
    def is_healthy(self) -> bool:
        """Check if current server is healthy"""
        if self._current_server is None:
            return False
        return self._current_server.is_healthy()
