"""
Main Application Entry Point - Clean FastAPI Version
Voice AI Assistant Backend using pure FastAPI
"""
import logging
import os
import sys
import uvicorn
from typing import Optional
from fastapi import FastAPI

# Configure logging to both console and file
log_file = "fastapi.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import Container bezpośrednio - bez DIService
from application.container import Container

def create_app() -> FastAPI:
    """Create FastAPI application - funkcja potrzebna dla reload"""
    try:
        logger.info("🚀 Creating Voice AI Assistant app with Clean FastAPI...")
        
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
        
        return app
    except Exception as e:
        logger.error(f"Pure FastAPI app initialization failed: {e}")
        raise

# Utwórz app na poziomie modułu - wymagane dla reload=True w uvicorn
app = create_app()

def main():
    """Main application entry point - Clean FastAPI version"""
    logger.info("🌐 Starting Clean FastAPI web server on http://0.0.0.0:8080")
    logger.info("✨ Clean startup - no Google ADK warnings!")
    
    # Sprawdź czy reload jest włączony
    reload_enabled = os.environ.get("RELOAD", "false").lower() == "true" or "--reload" in sys.argv
    
    if reload_enabled:
        logger.info("🔄 Auto-reload ENABLED - zmiany będą wykrywane automatycznie!")
        logger.info("📝 Monitorowane pliki: *.py w całym projekcie")
        # Używamy string modułu dla reload - to jest KLUCZOWE!
        uvicorn.run("main_fastapi:app", host="0.0.0.0", port=8080, reload=True, reload_includes=["*.py"])
    else:
        logger.info("💡 Dla auto-reload uruchom:")
        logger.info("   PowerShell: $env:RELOAD='true'; python main_fastapi.py")
        logger.info("   LUB bezpośrednio: uvicorn main_fastapi:app --reload --host 0.0.0.0 --port 8080")
        uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)

if __name__ == "__main__":
    main()
