"""
Web Server Interface - Abstract interface for web servers
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from fastapi import FastAPI


class IWebServer(ABC):
    """Abstract interface for web server implementations"""
    
    @abstractmethod
    def create_app(self) -> FastAPI:
        """Create and configure FastAPI application"""
        pass
    
    @abstractmethod
    def get_app_info(self) -> Dict[str, Any]:
        """Get server information"""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if server is healthy"""
        pass
