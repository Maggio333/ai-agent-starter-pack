"""
Google ADK Web Server Service - Implementation using Google ADK
"""
import logging
from typing import Dict, Any
from fastapi import FastAPI

from domain.services.IWebServer import IWebServer

logger = logging.getLogger(__name__)


class GoogleADKWebServerService(IWebServer):
    """Web server implementation using Google ADK"""
    
    def __init__(self, agents_dir: str = "", session_service_uri: str = "sqlite:///./sessions.db", 
                 allow_origins: list = None, web: bool = False):
        self.agents_dir = agents_dir
        self.session_service_uri = session_service_uri
        self.allow_origins = allow_origins or ["*"]
        self.web = web
        self._app = None
        
    def create_app(self) -> FastAPI:
        """Create FastAPI app using Google ADK"""
        try:
            from google.adk.cli.fast_api import get_fast_api_app
            
            logger.info("Creating FastAPI app with Google ADK...")
            
            # Create app with Google ADK
            app = get_fast_api_app(
                agents_dir=self.agents_dir,
                session_service_uri=self.session_service_uri,
                allow_origins=self.allow_origins,
                web=self.web,
            )
            
            # Enable OpenAPI schema for ADK Web UI
            # app.openapi = None  # Commented out to enable OpenAPI
            
            # Add our custom routers
            self._add_custom_routers(app)
            
            # Mount static files for audio
            self._mount_static_files(app)
            
            self._app = app
            logger.info("Google ADK FastAPI app created successfully")
            return app
            
        except Exception as e:
            logger.error(f"Failed to create Google ADK app: {e}")
            raise
    
    def _add_custom_routers(self, app: FastAPI):
        """Add custom routers to the app"""
        try:
            from presentation.api.chat_endpoints import router as chat_router
            from presentation.api.voice_endpoints import router as voice_router
            from presentation.api.notes_endpoints import router as notes_router
            
            # Include our custom routers
            app.include_router(chat_router, prefix="/api", tags=["chat"])
            app.include_router(voice_router, prefix="/api/voice", tags=["voice"])
            app.include_router(notes_router, prefix="/api", tags=["notes"])
            
            logger.info("Custom routers added to Google ADK app")
            
        except Exception as e:
            logger.error(f"Failed to add custom routers: {e}")
            raise
    
    def _mount_static_files(self, app: FastAPI):
        """Mount static files for audio"""
        import os
        from fastapi.staticfiles import StaticFiles
        
        # Get the project root directory (python_agent)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        static_dir = os.path.join(project_root, "static")
        
        if os.path.exists(static_dir):
            app.mount("/static", StaticFiles(directory=static_dir), name="static")
            logger.info(f"Static files mounted at /static from {static_dir}")
        else:
            logger.warning(f"Static directory '{static_dir}' does not exist. Skipping static files mount.")
    
    def get_app_info(self) -> Dict[str, Any]:
        """Get Google ADK server information"""
        return {
            "server_type": "Google ADK",
            "agents_dir": self.agents_dir,
            "session_service_uri": self.session_service_uri,
            "web_ui_enabled": self.web,
            "openapi_enabled": True,  # Enabled for ADK Web UI
            "features": [
                "Google ADK Integration",
                "ADK Web UI",
                "Custom API Endpoints",
                "Voice Processing",
                "Chat with LM Studio",
                "OpenAPI Documentation"
            ]
        }
    
    def is_healthy(self) -> bool:
        """Check if Google ADK server is healthy"""
        try:
            # Basic health check - if app was created successfully
            return self._app is not None
        except Exception as e:
            logger.error(f"Google ADK health check failed: {e}")
            return False
