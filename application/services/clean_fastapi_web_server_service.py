"""
Clean FastAPI Web Server Service - Pure FastAPI implementation
"""
import logging
import os
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from domain.services.IWebServer import IWebServer

logger = logging.getLogger(__name__)


class CleanFastAPIWebServerService(IWebServer):
    """Web server implementation using pure FastAPI"""
    
    def __init__(self, title: str = "Voice AI Assistant", 
                 description: str = "Clean FastAPI backend for Voice AI Assistant",
                 version: str = "1.0.0",
                 allow_origins: list = None):
        self.title = title
        self.description = description
        self.version = version
        self.allow_origins = allow_origins or ["http://localhost", "http://localhost:8080", "*"]
        self._app = None
        
    def create_app(self) -> FastAPI:
        """Create pure FastAPI app"""
        try:
            logger.info("Creating clean FastAPI app...")
            
            # Create FastAPI app
            app = FastAPI(
                title=self.title,
                description=self.description,
                version=self.version,
                docs_url="/docs",
                redoc_url="/redoc"
            )
            
            # Add CORS middleware
            app.add_middleware(
                CORSMiddleware,
                allow_origins=self.allow_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            # Add custom routers
            self._add_custom_routers(app)
            
            # Mount static files
            self._mount_static_files(app)
            
            # Add middleware
            self._add_middleware(app)
            
            # Add root endpoints
            self._add_root_endpoints(app)
            
            self._app = app
            logger.info("Clean FastAPI app created successfully")
            return app
            
        except Exception as e:
            logger.error(f"Failed to create clean FastAPI app: {e}")
            raise
    
    def _add_custom_routers(self, app: FastAPI):
        """Add custom routers to the app"""
        try:
            from presentation.api.chat_endpoints import router as chat_router
            from presentation.api.voice_endpoints import router as voice_router
            from presentation.api.notes_endpoints import router as notes_router
            
            # Include routers
            app.include_router(chat_router, prefix="/api", tags=["chat"])
            app.include_router(voice_router, prefix="/api/voice", tags=["voice"])
            app.include_router(notes_router, prefix="/api", tags=["notes"])
            
            logger.info("Custom routers added to clean FastAPI app")
            
        except Exception as e:
            logger.error(f"Failed to add custom routers: {e}")
            raise
    
    def _mount_static_files(self, app: FastAPI):
        """Mount static files for audio"""
        # Get the project root directory (python_agent)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        static_dir = os.path.join(project_root, "static")
        
        if os.path.exists(static_dir):
            app.mount("/static", StaticFiles(directory=static_dir), name="static")
            logger.info(f"Static files mounted at /static from {static_dir}")
        else:
            logger.warning(f"Static directory '{static_dir}' does not exist. Skipping static files mount.")
    
    def _add_middleware(self, app: FastAPI):
        """Add request logging middleware"""
        @app.middleware("http")
        async def log_requests(request, call_next):
            start_time = datetime.now()
            response = await call_next(request)
            process_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
            return response
    
    def _add_root_endpoints(self, app: FastAPI):
        """Add root endpoints"""
        @app.get("/")
        async def root():
            return {
                "message": "Voice AI Assistant API",
                "version": self.version,
                "status": "running",
                "docs": "/docs"
            }
        
        @app.get("/health")
        async def health():
            return {
                "status": "healthy",
                "message": "Voice AI System is running",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_app_info(self) -> Dict[str, Any]:
        """Get clean FastAPI server information"""
        return {
            "server_type": "Clean FastAPI",
            "title": self.title,
            "version": self.version,
            "openapi_enabled": True,
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "features": [
                "Pure FastAPI",
                "Custom API Endpoints", 
                "Voice Processing",
                "Chat with LM Studio",
                "OpenAPI Documentation",
                "Request Logging"
            ]
        }
    
    def is_healthy(self) -> bool:
        """Check if clean FastAPI server is healthy"""
        try:
            return self._app is not None
        except Exception as e:
            logger.error(f"Clean FastAPI health check failed: {e}")
            return False
