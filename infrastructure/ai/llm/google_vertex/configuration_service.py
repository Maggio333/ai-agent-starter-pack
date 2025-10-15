# infrastructure/llm/google_vertex/configuration_service.py
from typing import Dict, Any
from domain.utils.result import Result

class ConfigurationService:
    """Service for managing LLM configuration"""
    
    def __init__(self):
        self._configuration = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9
        }
    
    async def get_configuration(self) -> Result[Dict[str, Any], str]:
        """Get current configuration"""
        try:
            return Result.success(self._configuration.copy())
        except Exception as e:
            return Result.error(f"Failed to get configuration: {str(e)}")
    
    async def update_configuration(self, config: Dict[str, Any]) -> Result[None, str]:
        """Update configuration"""
        try:
            self._configuration.update(config)
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to update configuration: {str(e)}")
    
    async def reset_configuration(self) -> Result[None, str]:
        """Reset to default configuration"""
        try:
            self._configuration = {
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 0.9
            }
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to reset configuration: {str(e)}")
    
    async def set_temperature(self, temperature: float) -> Result[None, str]:
        """Set temperature parameter"""
        try:
            self._configuration["temperature"] = temperature
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to set temperature: {str(e)}")
    
    async def set_max_tokens(self, max_tokens: int) -> Result[None, str]:
        """Set max tokens parameter"""
        try:
            self._configuration["max_tokens"] = max_tokens
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to set max tokens: {str(e)}")
    
    async def set_top_p(self, top_p: float) -> Result[None, str]:
        """Set top_p parameter"""
        try:
            self._configuration["top_p"] = top_p
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to set top_p: {str(e)}")
    
    def get_generation_config(self) -> Dict[str, Any]:
        """Get generation config for API calls"""
        return {
            "temperature": self._configuration["temperature"],
            "maxOutputTokens": self._configuration["max_tokens"],
            "topP": self._configuration["top_p"]
        }
