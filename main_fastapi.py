"""
Main Application Entry Point - Clean FastAPI Version
Voice AI Assistant Backend using pure FastAPI
"""
import logging
import os
import uvicorn
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Container bezpośrednio - bez DIService
from application.container import Container

def main():
    """Main application entry point - Clean FastAPI version"""
    try:
        logger.info("🚀 Starting Voice AI Assistant with Clean FastAPI...")
        
        # Get Container
        container = Container()
        
        # Get web server manager
        web_server_manager = container.web_server_manager_service()
        
        # Force Clean FastAPI server type
        logger.info("🔧 Using Clean FastAPI web server")
        
        # Create Clean FastAPI web server
        web_server = web_server_manager.create_server(
            server_type="clean_fastapi",
            title="Voice AI Assistant - Clean FastAPI",
            description="Clean FastAPI backend for Voice AI Assistant - No Google ADK",
            version="1.0.0",
            allow_origins=["http://localhost", "http://localhost:8080", "*"]
        )
        
        # Create FastAPI app
        app = web_server.create_app()
        
        # Get server info
        server_info = web_server_manager.get_server_info()
        logger.info(f"📊 Server info: {server_info}")
        
        # Start server
        logger.info("🌐 Starting Clean FastAPI web server on http://0.0.0.0:8080")
        logger.info("✨ Clean startup - no Google ADK warnings!")
        uvicorn.run(app, host="0.0.0.0", port=8080)
        
    except Exception as e:
        logger.error(f"❌ Failed to start Clean FastAPI application: {e}")
        raise

if __name__ == "__main__":
    main()
