# infrastructure/ai/llm/lmstudio_llm_service.py
import asyncio
import logging
from typing import List, AsyncIterator, Dict, Any, Optional
import httpx
import json
from .base_llm_service import BaseLLMService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.utils.result import Result

class LMStudioLLMService(BaseLLMService):
    """LM Studio implementation of LLMService for local LLM models"""
    
    def __init__(self, proxy_url: str = "http://127.0.0.1:8123", model_name: str = "model:1"):
        super().__init__()
        self.proxy_url = proxy_url
        self.model_name = model_name
        
        # LM Studio API endpoints
        self.chat_endpoint = f"{proxy_url}/v1/chat/completions"
        self.models_endpoint = f"{proxy_url}/v1/models"
        
        self.logger.info(f"LM Studio LLM Service initialized: {proxy_url} with model {model_name}")
    
    # Override core methods for LM Studio implementation
    
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
            error_msg = f"LM Studio HTTP error: {e.response.status_code} - {e.response.text}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"LM Studio completion error: {str(e)}"
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
            
            async with httpx.AsyncClient(timeout=60.0) as client:
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
    
    async def get_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> Result[Dict[str, Any], str]:
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
                message = result["choices"][0]["message"]
                
                # Return structured response with tool calls if present
                response_data = {
                    "content": message.get("content", ""),
                    "tool_calls": message.get("tool_calls", []),
                    "role": message.get("role", "assistant")
                }
                
                self.logger.info(f"LM Studio completion with tools successful: {len(response_data['content'])} chars")
                return Result.success(response_data)
                
        except Exception as e:
            error_msg = f"LM Studio completion with tools error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def stream_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> AsyncIterator[Result[Dict[str, Any], str]]:
        """Stream completion with tool calling support"""
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
                "stream": True
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
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
                                    tool_calls = delta.get("tool_calls", [])
                                    
                                    if content or tool_calls:
                                        response_data = {
                                            "content": content,
                                            "tool_calls": tool_calls,
                                            "role": "assistant"
                                        }
                                        yield Result.success(response_data)
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            error_msg = f"LM Studio streaming with tools error: {str(e)}"
            self.logger.error(error_msg)
            yield Result.error(error_msg)
    
    async def list_models(self) -> Result[List[Dict[str, Any]], str]:
        """List available models from LM Studio"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.models_endpoint)
                response.raise_for_status()
                
                result = response.json()
                models = result.get("data", [])
                
                # Format models for consistency
                formatted_models = []
                for model in models:
                    formatted_models.append({
                        "id": model.get("id"),
                        "name": model.get("name", model.get("id")),
                        "provider": "lmstudio",
                        "capabilities": ["chat", "completion"]
                    })
                
                self.logger.info(f"Found {len(formatted_models)} models in LM Studio")
                return Result.success(formatted_models)
                
        except Exception as e:
            error_msg = f"Failed to list LM Studio models: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def get_current_model(self) -> Result[str, str]:
        """Get current active model"""
        return Result.success(self.model_name)
    
    async def set_model(self, model_name: str) -> Result[None, str]:
        """Set active model"""
        try:
            # Verify model exists
            models_result = await self.list_models()
            if models_result.is_error:
                return models_result
            
            models = models_result.value
            model_exists = any(model.get("id") == model_name for model in models)
            
            if model_exists:
                self.model_name = model_name
                self.logger.info(f"Switched to model: {model_name}")
                return Result.success(None)
            else:
                return Result.error(f"Model {model_name} not found")
                
        except Exception as e:
            error_msg = f"Failed to set model: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def get_configuration(self) -> Result[Dict[str, Any], str]:
        """Get current configuration"""
        return Result.success({
            "model": self.model_name,
            "proxy_url": self.proxy_url,
            "temperature": 0.7,
            "max_tokens": 2048,
            "provider": "lmstudio"
        })
    
    async def update_configuration(self, config: Dict[str, Any]) -> Result[None, str]:
        """Update configuration"""
        try:
            if "model" in config:
                self.model_name = config["model"]
            if "proxy_url" in config:
                self.proxy_url = config["proxy_url"]
                self.chat_endpoint = f"{self.proxy_url}/v1/chat/completions"
                self.models_endpoint = f"{self.proxy_url}/v1/models"
            
            self.logger.info("Configuration updated successfully")
            return Result.success(None)
            
        except Exception as e:
            error_msg = f"Failed to update configuration: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        try:
            # Try to list models as a health check
            models_result = await self.list_models()
            
            if models_result.is_success:
                return Result.success({
                    "status": "healthy",
                    "provider": "lmstudio",
                    "proxy_url": self.proxy_url,
                    "model": self.model_name,
                    "models_available": len(models_result.value)
                })
            else:
                return Result.success({
                    "status": "unhealthy",
                    "provider": "lmstudio",
                    "proxy_url": self.proxy_url,
                    "model": self.model_name,
                    "error": models_result.error
                })
                
        except Exception as e:
            error_msg = f"Health check failed: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    # Helper methods
    def _convert_messages_to_lm_format(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Convert ChatMessage list to LM Studio format"""
        lm_messages = []
        
        for msg in messages:
            role_mapping = {
                MessageRole.USER: "user",
                MessageRole.ASSISTANT: "assistant", 
                MessageRole.SYSTEM: "system",
                MessageRole.TOOL: "tool"
            }
            
            lm_role = role_mapping.get(msg.role, "user")
            
            lm_messages.append({
                "role": lm_role,
                "content": msg.content
            })
        
        return lm_messages