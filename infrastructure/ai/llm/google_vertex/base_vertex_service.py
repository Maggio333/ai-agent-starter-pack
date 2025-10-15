# infrastructure/llm/google_vertex/base_vertex_service.py
import httpx
import json
from typing import List, AsyncIterator
from domain.entities.chat_message import ChatMessage
from domain.utils.result import Result

class BaseVertexService:
    """Base Google Vertex AI service for basic completion operations"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    async def get_completion(self, messages: List[ChatMessage], config: dict = None) -> Result[str, str]:
        """Get LLM completion"""
        try:
            async with httpx.AsyncClient() as client:
                # Convert messages to Google format
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
                        "generationConfig": generation_config
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    return Result.success(content)
                else:
                    return Result.error(f"API error: {response.status_code}")
                    
        except Exception as e:
            return Result.error(f"Failed to get completion: {str(e)}")
    
    async def stream_completion(self, messages: List[ChatMessage], config: dict = None) -> AsyncIterator[Result[str, str]]:
        """Stream LLM completion"""
        try:
            async with httpx.AsyncClient() as client:
                # Convert messages to Google format
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
                        "generationConfig": generation_config
                    }
                ) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                data = line[6:]  # Remove "data: " prefix
                                if data.strip() == "[DONE]":
                                    break
                                try:
                                    chunk_data = json.loads(data)
                                    if "candidates" in chunk_data and chunk_data["candidates"]:
                                        content = chunk_data["candidates"][0]["content"]["parts"][0]["text"]
                                        yield Result.success(content)
                                except json.JSONDecodeError:
                                    continue
                    else:
                        yield Result.error(f"API error: {response.status_code}")
                        
        except Exception as e:
            yield Result.error(f"Failed to stream completion: {str(e)}")
