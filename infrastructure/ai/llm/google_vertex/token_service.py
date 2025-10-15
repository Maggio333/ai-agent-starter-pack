# infrastructure/llm/google_vertex/token_service.py
import httpx
import time
from typing import List, Dict, Any
from domain.entities.chat_message import ChatMessage
from domain.utils.result import Result
from .base_vertex_service import BaseVertexService

class TokenService(BaseVertexService):
    """Google Vertex AI service for token management operations"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        super().__init__(api_key, model)
        self._usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }
    
    async def count_tokens(self, text: str) -> Result[int, str]:
        """Count tokens in text"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:countTokens",
                    headers={"X-Goog-Api-Key": self.api_key},
                    json={"contents": [{"parts": [{"text": text}]}]}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return Result.success(data.get("totalTokens", 0))
                else:
                    return Result.error(f"API error: {response.status_code}")
        except Exception as e:
            return Result.error(f"Failed to count tokens: {str(e)}")
    
    async def count_tokens_in_messages(self, messages: List[ChatMessage]) -> Result[int, str]:
        """Count tokens in messages"""
        try:
            google_messages = []
            for msg in messages:
                google_messages.append({
                    "role": msg.role.value,
                    "parts": [{"text": msg.content}]
                })
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:countTokens",
                    headers={"X-Goog-Api-Key": self.api_key},
                    json={"contents": google_messages}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return Result.success(data.get("totalTokens", 0))
                else:
                    return Result.error(f"API error: {response.status_code}")
        except Exception as e:
            return Result.error(f"Failed to count tokens in messages: {str(e)}")
    
    async def estimate_cost(self, messages: List[ChatMessage]) -> Result[Dict[str, Any], str]:
        """Estimate API cost for messages"""
        try:
            token_count_result = await self.count_tokens_in_messages(messages)
            if token_count_result.is_error:
                return token_count_result
            
            # Rough cost estimation (this would need actual pricing data)
            estimated_cost = token_count_result.value * 0.00001  # $0.00001 per token
            
            cost_info = {
                "estimated_tokens": token_count_result.value,
                "estimated_cost_usd": estimated_cost,
                "model": self.model,
                "timestamp": time.time()
            }
            
            return Result.success(cost_info)
        except Exception as e:
            return Result.error(f"Failed to estimate cost: {str(e)}")
    
    async def get_usage_stats(self) -> Result[Dict[str, Any], str]:
        """Get usage statistics"""
        try:
            return Result.success(self._usage_stats.copy())
        except Exception as e:
            return Result.error(f"Failed to get usage stats: {str(e)}")
    
    async def reset_usage_stats(self) -> Result[None, str]:
        """Reset usage statistics"""
        try:
            self._usage_stats = {
                "total_requests": 0,
                "total_tokens": 0,
                "total_cost": 0.0
            }
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to reset usage stats: {str(e)}")
    
    def update_usage_stats(self, tokens: int, cost: float = 0.0):
        """Update usage statistics"""
        self._usage_stats["total_requests"] += 1
        self._usage_stats["total_tokens"] += tokens
        self._usage_stats["total_cost"] += cost
