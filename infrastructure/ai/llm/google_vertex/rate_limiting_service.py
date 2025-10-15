# infrastructure/llm/google_vertex/rate_limiting_service.py
import time
from typing import Dict, Any
from domain.utils.result import Result

class RateLimitingService:
    """Service for managing rate limiting and quotas"""
    
    def __init__(self):
        self._requests_per_minute = 60
        self._tokens_per_minute = 10000
        self._daily_limit = 1000
        self._request_times = []
        self._token_usage = []
        self._daily_usage = 0
        self._last_reset = time.time()
    
    async def get_rate_limit_info(self) -> Result[Dict[str, Any], str]:
        """Get rate limit information"""
        try:
            current_time = time.time()
            # Clean old request times (older than 1 minute)
            self._request_times = [t for t in self._request_times if current_time - t < 60]
            
            rate_info = {
                "requests_per_minute": self._requests_per_minute,
                "tokens_per_minute": self._tokens_per_minute,
                "current_requests": len(self._request_times),
                "current_tokens": sum(self._token_usage[-60:]) if len(self._token_usage) > 60 else sum(self._token_usage),
                "remaining_requests": max(0, self._requests_per_minute - len(self._request_times)),
                "remaining_tokens": max(0, self._tokens_per_minute - (sum(self._token_usage[-60:]) if len(self._token_usage) > 60 else sum(self._token_usage)))
            }
            return Result.success(rate_info)
        except Exception as e:
            return Result.error(f"Failed to get rate limit info: {str(e)}")
    
    async def check_rate_limit(self) -> Result[bool, str]:
        """Check if rate limit allows request"""
        try:
            current_time = time.time()
            
            # Clean old request times
            self._request_times = [t for t in self._request_times if current_time - t < 60]
            
            # Check requests per minute
            if len(self._request_times) >= self._requests_per_minute:
                return Result.success(False)
            
            # Check tokens per minute
            recent_tokens = sum(self._token_usage[-60:]) if len(self._token_usage) > 60 else sum(self._token_usage)
            if recent_tokens >= self._tokens_per_minute:
                return Result.success(False)
            
            return Result.success(True)
        except Exception as e:
            return Result.error(f"Failed to check rate limit: {str(e)}")
    
    async def get_quota_info(self) -> Result[Dict[str, Any], str]:
        """Get quota information"""
        try:
            current_time = time.time()
            
            # Reset daily usage if it's a new day
            if current_time - self._last_reset > 86400:  # 24 hours
                self._daily_usage = 0
                self._last_reset = current_time
            
            quota_info = {
                "daily_limit": self._daily_limit,
                "used_today": self._daily_usage,
                "remaining": max(0, self._daily_limit - self._daily_usage),
                "reset_time": self._last_reset + 86400
            }
            return Result.success(quota_info)
        except Exception as e:
            return Result.error(f"Failed to get quota info: {str(e)}")
    
    def record_request(self, tokens: int = 0):
        """Record a request and token usage"""
        current_time = time.time()
        self._request_times.append(current_time)
        self._token_usage.append(tokens)
        self._daily_usage += 1
        
        # Clean old data
        self._request_times = [t for t in self._request_times if current_time - t < 60]
        self._token_usage = self._token_usage[-60:]  # Keep only last 60 entries
