"""
Main Application Entry Point - Google ADK Version
Voice AI Assistant Backend using Google ADK
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
    """Main application entry point - Google ADK version"""
    try:
        logger.info("🚀 Starting Voice AI Assistant with Google ADK...")
        
        # Get Container
        container = Container()
        
        # Get web server manager
        web_server_manager = container.web_server_manager_service()
        
        # Force Google ADK server type
        logger.info("🔧 Using Google ADK web server")
        
        # Create Google ADK web server
        web_server = web_server_manager.create_server(
            server_type="google_adk",
            agents_dir="agents",  # Enable agents directory scanning - use our ADK agent!
            session_service_uri="sqlite:///./sessions.db",
            allow_origins=["http://localhost", "http://localhost:8080", "*"],
            web=True  # Enable ADK Web UI
        )
        
        # Create FastAPI app
        app = web_server.create_app()
        
        # Get server info
        server_info = web_server_manager.get_server_info()
        logger.info(f"📊 Server info: {server_info}")
        
        # Start server
        logger.info("🌐 Starting Google ADK web server on http://0.0.0.0:8080")
        logger.info("⚠️  Note: Google ADK warnings are expected and normal")
        uvicorn.run(app, host="0.0.0.0", port=8080)
        
    except Exception as e:
        logger.error(f"❌ Failed to start Google ADK application: {e}")
        raise

if __name__ == "__main__":
    main()
