# infrastructure/config/environment/env_loader.py
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
except ImportError:
    pass  # python-dotenv not available

class Environment(Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class EnvironmentConfig:
    """Environment configuration"""
    environment: Environment
    debug: bool
    log_level: str
    database_url: str
    redis_url: str
    api_keys: Dict[str, str]
    feature_flags: Dict[str, bool]

class EnvironmentLoader:
    """Service for loading environment configuration"""
    
    def __init__(self):
        self.config: Optional[EnvironmentConfig] = None
    
    def load_from_env(self) -> EnvironmentConfig:
        """Load configuration from environment variables"""
        environment = Environment(os.getenv("ENVIRONMENT", "development"))
        debug = os.getenv("DEBUG", "false").lower() == "true"
        log_level = os.getenv("LOG_LEVEL", "INFO")
        
        database_url = os.getenv("DATABASE_URL", "sqlite:///chat.db")
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Load API keys
        api_keys = {
            "google_api_key": os.getenv("GOOGLE_API_KEY", ""),
            "qdrant_api_key": os.getenv("QDRANT_API_KEY", ""),
            "openai_api_key": os.getenv("OPENAI_API_KEY", "")
        }
        
        # Load feature flags
        feature_flags = {
            "enable_caching": os.getenv("ENABLE_CACHING", "true").lower() == "true",
            "enable_monitoring": os.getenv("ENABLE_MONITORING", "true").lower() == "true",
            "enable_rate_limiting": os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
        }
        
        self.config = EnvironmentConfig(
            environment=environment,
            debug=debug,
            log_level=log_level,
            database_url=database_url,
            redis_url=redis_url,
            api_keys=api_keys,
            feature_flags=feature_flags
        )
        
        return self.config
    
    def load_from_file(self, file_path: str) -> EnvironmentConfig:
        """Load configuration from file"""
        # This would implement loading from JSON/YAML file
        # For now, fallback to environment variables
        return self.load_from_env()
    
    def get_config(self) -> EnvironmentConfig:
        """Get current configuration"""
        if self.config is None:
            return self.load_from_env()
        return self.config
    
    def get(self, key: str, default: str = None) -> str:
        """Get environment variable as string"""
        return os.getenv(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer"""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def is_production(self) -> bool:
        """Check if running in production"""
        config = self.get_config()
        return config.environment == Environment.PRODUCTION
    
    def is_development(self) -> bool:
        """Check if running in development"""
        config = self.get_config()
        return config.environment == Environment.DEVELOPMENT
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for service"""
        config = self.get_config()
        return config.api_keys.get(f"{service}_api_key")
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if feature is enabled"""
        config = self.get_config()
        return config.feature_flags.get(feature, False)
