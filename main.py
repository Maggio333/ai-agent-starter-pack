# main.py
import os
import logging
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# Import our custom API endpoints
from presentation.api.chat_endpoints import router as chat_router

# Configure logging with UTF-8 encoding
import sys
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Example session service URI (e.g., SQLite)
SESSION_SERVICE_URI = "sqlite:///./sessions.db"
# Example allowed origins for CORS
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]
# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True

# Call the function to get the FastAPI app instance
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_SERVICE_URI,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# Add our custom API endpoints
app.include_router(chat_router, prefix="/api", tags=["chat"])

# Add custom middleware for logging
@app.middleware("http")
async def log_requests(request, call_next):
    """Log all API requests"""
    logger.info(f"API Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"API Response: {response.status_code}")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))