# infrastructure/llm/google_vertex/caching_service.py
import time
from typing import Dict, Any
from domain.utils.result import Result

class CachingService:
    """Service for managing response caching"""
    
    def __init__(self):
        self._cache_enabled = False
        self._cache = {}
        self._cache_ttl = 3600  # 1 hour default
    
    async def enable_caching(self, enabled: bool = True) -> Result[None, str]:
        """Enable/disable response caching"""
        try:
            self._cache_enabled = enabled
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to enable caching: {str(e)}")
    
    async def clear_cache(self) -> Result[None, str]:
        """Clear response cache"""
        try:
            self._cache.clear()
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to clear cache: {str(e)}")
    
    async def get_cache_stats(self) -> Result[Dict[str, Any], str]:
        """Get cache statistics"""
        try:
            stats = {
                "enabled": self._cache_enabled,
                "size": len(self._cache),
                "hit_rate": 0.0,  # Would need to track hits/misses
                "ttl_seconds": self._cache_ttl
            }
            return Result.success(stats)
        except Exception as e:
            return Result.error(f"Failed to get cache stats: {str(e)}")
    
    async def set_cache_ttl(self, ttl_seconds: int) -> Result[None, str]:
        """Set cache time-to-live"""
        try:
            self._cache_ttl = ttl_seconds
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to set cache TTL: {str(e)}")
    
    def get_cached_response(self, cache_key: str) -> Any:
        """Get cached response if available and not expired"""
        if not self._cache_enabled:
            return None
        
        if cache_key in self._cache:
            cached_item = self._cache[cache_key]
            if time.time() - cached_item["timestamp"] < self._cache_ttl:
                return cached_item["response"]
            else:
                # Expired, remove from cache
                del self._cache[cache_key]
        
        return None
    
    def cache_response(self, cache_key: str, response: Any):
        """Cache response with timestamp"""
        if self._cache_enabled:
            self._cache[cache_key] = {
                "response": response,
                "timestamp": time.time()
            }
    
    def generate_cache_key(self, messages: list, config: dict = None) -> str:
        """Generate cache key from messages and config"""
        import hashlib
        import json
        
        key_data = {
            "messages": messages,
            "config": config or {}
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
