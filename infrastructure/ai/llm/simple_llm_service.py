# infrastructure/ai/llm/simple_llm_service.py
import asyncio
import logging
from typing import List, AsyncIterator, Dict, Any, Optional
import httpx
import json
from domain.services.ILLMService import ILLMService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.utils.result import Result

class SimpleLLMService(ILLMService):
    """Simple LLM service implementation with only essential methods"""
    
    def __init__(self, proxy_url: str = "http://127.0.0.1:8123", model_name: str = "model:1"):
        self.proxy_url = proxy_url
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
        # LM Studio API endpoints
        self.chat_endpoint = f"{proxy_url}/v1/chat/completions"
        self.models_endpoint = f"{proxy_url}/v1/models"
        
        self.logger.info(f"Simple LLM Service initialized: {proxy_url} with model {model_name}")
    
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        """Get LLM completion from LM Studio"""
        try:
            # Convert ChatMessage to LM Studio format
            lm_messages = self._convert_messages_to_lm_format(messages)
            
            payload = {
                "model": self.model_name,
                "messages": lm_messages,
                "temperature": 0.7,
                "max_tokens": 2048,
                "stream": False
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.chat_endpoint, json=payload)
                response.raise_for_status()
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                self.logger.info(f"LM Studio completion successful: {len(content)} chars")
                return Result.success(content)
                
        except httpx.TimeoutException:
            error_msg = f"LM Studio request timeout for model {self.model_name}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except httpx.HTTPStatusError as e:
            error_msg = f"LM Studio HTTP error {e.response.status_code}: {e.response.text}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"LM Studio completion error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def get_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> Result[str, str]:
        """Get LLM completion with tool calling support"""
        try:
            # Convert ChatMessage to LM Studio format
            lm_messages = self._convert_messages_to_lm_format(messages)
            
            payload = {
                "model": self.model_name,
                "messages": lm_messages,
                "tools": tools,
                "tool_choice": "auto",
                "temperature": 0.7,
                "max_tokens": 2048,
                "stream": False
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.chat_endpoint, json=payload)
                response.raise_for_status()
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                self.logger.info(f"LM Studio completion with tools successful: {len(content)} chars")
                return Result.success(content)
                
        except Exception as e:
            error_msg = f"LM Studio completion with tools error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def stream_completion(self, messages: List[ChatMessage]) -> AsyncIterator[Result[str, str]]:
        """Stream LLM completion from LM Studio"""
        try:
            # Convert ChatMessage to LM Studio format
            lm_messages = self._convert_messages_to_lm_format(messages)
            
            payload = {
                "model": self.model_name,
                "messages": lm_messages,
                "temperature": 0.7,
                "max_tokens": 2048,
                "stream": True
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream("POST", self.chat_endpoint, json=payload) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]  # Remove "data: " prefix
                            if data.strip() == "[DONE]":
                                break
                            
                            try:
                                chunk = json.loads(data)
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield Result.success(content)
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            error_msg = f"LM Studio streaming error: {str(e)}"
            self.logger.error(error_msg)
            yield Result.error(error_msg)
    
    def _convert_messages_to_lm_format(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Convert ChatMessage list to LM Studio format"""
        lm_messages = []
        for msg in messages:
            lm_messages.append({
                "role": msg.role.value,
                "content": msg.content
            })
        return lm_messages
    
    # Placeholder implementations for abstract methods
    async def analyze_sentiment(self, text: str) -> Result[str, str]:
        return Result.success("neutral")
    
    async def batch_completion(self, messages_list: List[List[ChatMessage]]) -> Result[List[str], str]:
        results = []
        for messages in messages_list:
            result = await self.get_completion(messages)
            if result.is_success:
                results.append(result.value)
            else:
                return Result.error(f"Batch completion failed: {result.error}")
        return Result.success(results)
    
    async def batch_embeddings(self, texts: List[str]) -> Result[List[List[float]], str]:
        return Result.error("Embeddings not supported in SimpleLLMService")
    
    async def check_rate_limit(self) -> Result[bool, str]:
        return Result.success(True)
    
    async def classify_text(self, text: str, categories: List[str]) -> Result[str, str]:
        return Result.success("general")
    
    async def clear_cache(self) -> Result[None, str]:
        return Result.success(None)
    
    async def clear_conversation_history(self, session_id: str) -> Result[None, str]:
        return Result.success(None)
    
    async def clear_error_history(self) -> Result[None, str]:
        return Result.success(None)
    
    async def compare_responses(self, response1: str, response2: str) -> Result[Dict[str, Any], str]:
        return Result.success({"similarity": 0.5})
    
    async def count_tokens(self, text: str) -> Result[int, str]:
        return Result.success(len(text.split()))
    
    async def count_tokens_in_messages(self, messages: List[ChatMessage]) -> Result[int, str]:
        total = sum(len(msg.content.split()) for msg in messages)
        return Result.success(total)
    
    async def enable_caching(self, enabled: bool) -> Result[None, str]:
        return Result.success(None)
    
    async def end_conversation(self, session_id: str) -> Result[None, str]:
        return Result.success(None)
    
    async def estimate_cost(self, messages: List[ChatMessage]) -> Result[float, str]:
        return Result.success(0.0)
    
    async def evaluate_response(self, response: str, criteria: List[str]) -> Result[Dict[str, float], str]:
        return Result.success({"quality": 0.8})
    
    async def extract_entities(self, text: str) -> Result[List[Dict[str, Any]], str]:
        return Result.success([])
    
    async def extract_keywords(self, text: str, count: int = 10) -> Result[List[str], str]:
        return Result.success([])
    
    async def get_cache_stats(self) -> Result[Dict[str, Any], str]:
        return Result.success({"hits": 0, "misses": 0})
    
    async def get_configuration(self) -> Result[Dict[str, Any], str]:
        return Result.success({
            "model": self.model_name,
            "proxy_url": self.proxy_url,
            "temperature": 0.7,
            "max_tokens": 2048
        })
    
    async def get_conversation_history(self, session_id: str) -> Result[List[ChatMessage], str]:
        return Result.success([])
    
    async def get_current_model(self) -> Result[str, str]:
        return Result.success(self.model_name)
    
    async def get_embedding(self, text: str) -> Result[List[float], str]:
        return Result.error("Embeddings not supported in SimpleLLMService")
    
    async def get_embeddings(self, texts: List[str]) -> Result[List[List[float]], str]:
        return Result.error("Embeddings not supported in SimpleLLMService")
    
    async def get_error_history(self) -> Result[List[Dict[str, Any]], str]:
        return Result.success([])
    
    async def get_performance_metrics(self) -> Result[Dict[str, Any], str]:
        return Result.success({"avg_response_time": 1.0})
    
    async def get_prompt_suggestions(self, context: str) -> Result[List[str], str]:
        return Result.success([])
    
    async def get_quota_info(self) -> Result[Dict[str, Any], str]:
        return Result.success({"remaining": 1000})
    
    async def get_rate_limit_info(self) -> Result[Dict[str, Any], str]:
        return Result.success({"limit": 1000, "remaining": 1000})
    
    async def get_response_quality_score(self, response: str) -> Result[float, str]:
        return Result.success(0.8)
    
    async def get_usage_stats(self) -> Result[Dict[str, Any], str]:
        return Result.success({"total_requests": 0})
    
    async def list_custom_functions(self) -> Result[List[Dict[str, Any]], str]:
        return Result.success([])
    
    async def list_models(self) -> Result[List[str], str]:
        return Result.success([self.model_name])
    
    async def optimize_prompt(self, prompt: str) -> Result[str, str]:
        return Result.success(prompt)
    
    async def parallel_completion(self, messages_list: List[List[ChatMessage]]) -> Result[List[str], str]:
        return await self.batch_completion(messages_list)
    
    async def register_custom_function(self, function: Dict[str, Any]) -> Result[None, str]:
        return Result.success(None)
    
    async def reset_configuration(self) -> Result[None, str]:
        return Result.success(None)
    
    async def reset_usage_stats(self) -> Result[None, str]:
        return Result.success(None)
    
    async def set_cache_ttl(self, ttl: int) -> Result[None, str]:
        return Result.success(None)
    
    async def set_max_tokens(self, max_tokens: int) -> Result[None, str]:
        return Result.success(None)
    
    async def set_model(self, model: str) -> Result[None, str]:
        self.model_name = model
        return Result.success(None)
    
    async def set_temperature(self, temperature: float) -> Result[None, str]:
        return Result.success(None)
    
    async def set_top_p(self, top_p: float) -> Result[None, str]:
        return Result.success(None)
    
    async def start_conversation(self, session_id: str) -> Result[None, str]:
        return Result.success(None)
    
    async def stream_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> AsyncIterator[Result[str, str]]:
        # For now, just use regular streaming
        async for result in self.stream_completion(messages):
            yield result
    
    async def summarize_text(self, text: str, max_length: int = 100) -> Result[str, str]:
        return Result.success(text[:max_length])
    
    async def translate_text(self, text: str, target_language: str) -> Result[str, str]:
        return Result.success(text)
    
    async def unregister_custom_function(self, function_name: str) -> Result[None, str]:
        return Result.success(None)
    
    async def update_configuration(self, config: Dict[str, Any]) -> Result[None, str]:
        return Result.success(None)
    
    async def validate_prompt(self, prompt: str) -> Result[bool, str]:
        return Result.success(True)
