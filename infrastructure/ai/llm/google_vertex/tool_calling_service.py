# infrastructure/llm/google_vertex/tool_calling_service.py
import httpx
import json
from typing import List, AsyncIterator, Dict, Any
from domain.entities.chat_message import ChatMessage
from domain.utils.result import Result
from .base_vertex_service import BaseVertexService

class ToolCallingService(BaseVertexService):
    """Google Vertex AI service for tool calling operations"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        super().__init__(api_key, model)
        self._custom_functions = {}
    
    async def get_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]], config: dict = None) -> Result[Dict[str, Any], str]:
        """Get completion with tool calling support"""
        try:
            async with httpx.AsyncClient() as client:
                google_messages = []
                for msg in messages:
                    google_messages.append({
                        "role": msg.role.value,
                        "parts": [{"text": msg.content}]
                    })
                
                generation_config = config or {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000
                }
                
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:generateContent",
                    headers={"X-Goog-Api-Key": self.api_key},
                    json={
                        "contents": google_messages,
                        "tools": tools,
                        "generationConfig": generation_config
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return Result.success(data)
                else:
                    return Result.error(f"API error: {response.status_code}")
        except Exception as e:
            return Result.error(f"Failed to get completion with tools: {str(e)}")
    
    async def stream_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]], config: dict = None) -> AsyncIterator[Result[Dict[str, Any], str]]:
        """Stream completion with tool calling support"""
        try:
            async with httpx.AsyncClient() as client:
                google_messages = []
                for msg in messages:
                    google_messages.append({
                        "role": msg.role.value,
                        "parts": [{"text": msg.content}]
                    })
                
                generation_config = config or {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000
                }
                
                async with client.stream(
                    "POST",
                    f"{self.base_url}/models/{self.model}:streamGenerateContent",
                    headers={"X-Goog-Api-Key": self.api_key},
                    json={
                        "contents": google_messages,
                        "tools": tools,
                        "generationConfig": generation_config
                    }
                ) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                data = line[6:]
                                if data.strip() == "[DONE]":
                                    break
                                try:
                                    chunk_data = json.loads(data)
                                    yield Result.success(chunk_data)
                                except json.JSONDecodeError:
                                    continue
                    else:
                        yield Result.error(f"API error: {response.status_code}")
        except Exception as e:
            yield Result.error(f"Failed to stream completion with tools: {str(e)}")
    
    async def register_custom_function(self, function_name: str, function_schema: Dict[str, Any]) -> Result[None, str]:
        """Register custom function for tool calling"""
        try:
            self._custom_functions[function_name] = function_schema
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to register custom function: {str(e)}")
    
    async def unregister_custom_function(self, function_name: str) -> Result[None, str]:
        """Unregister custom function"""
        try:
            if function_name in self._custom_functions:
                del self._custom_functions[function_name]
            return Result.success(None)
        except Exception as e:
            return Result.error(f"Failed to unregister custom function: {str(e)}")
    
    async def list_custom_functions(self) -> Result[List[Dict[str, Any]], str]:
        """List registered custom functions"""
        try:
            functions = [{"name": name, "schema": schema} for name, schema in self._custom_functions.items()]
            return Result.success(functions)
        except Exception as e:
            return Result.error(f"Failed to list custom functions: {str(e)}")
