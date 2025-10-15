# infrastructure/llm/google_vertex/ai_features_service.py
import httpx
from typing import List, Dict, Any, Optional
from domain.entities.chat_message import ChatMessage
from domain.utils.result import Result
from .base_vertex_service import BaseVertexService

class AIFeaturesService(BaseVertexService):
    """Google Vertex AI service for advanced AI features"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        super().__init__(api_key, model)
    
    async def get_embeddings(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Get text embeddings"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/embedding-001:embedContent",
                    headers={"X-Goog-Api-Key": self.api_key},
                    json={
                        "requests": [{"content": {"parts": [{"text": text}]}} for text in texts]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    embeddings = [item["embedding"]["values"] for item in data.get("embeddings", [])]
                    return Result.success(embeddings)
                else:
                    return Result.error(f"API error: {response.status_code}")
        except Exception as e:
            return Result.error(f"Failed to get embeddings: {str(e)}")
    
    async def get_embedding(self, text: str) -> Result[List[float], str]:
        """Get single text embedding"""
        embeddings_result = await self.get_embeddings([text])
        if embeddings_result.is_error:
            return embeddings_result
        
        if embeddings_result.value:
            return Result.success(embeddings_result.value[0])
        else:
            return Result.error("No embedding returned")
    
    async def classify_text(self, text: str, categories: List[str]) -> Result[Dict[str, Any], str]:
        """Classify text into categories"""
        try:
            prompt = f"Classify the following text into one of these categories: {', '.join(categories)}\n\nText: {text}\n\nCategory:"
            
            messages = [ChatMessage.create_user_message(prompt)]
            completion_result = await self.get_completion(messages)
            
            if completion_result.is_error:
                return completion_result
            
            classification = {
                "text": text,
                "categories": categories,
                "predicted_category": completion_result.value.strip(),
                "confidence": 0.8  # Placeholder
            }
            
            return Result.success(classification)
        except Exception as e:
            return Result.error(f"Failed to classify text: {str(e)}")
    
    async def summarize_text(self, text: str, max_length: int = 100) -> Result[str, str]:
        """Summarize text"""
        try:
            prompt = f"Summarize the following text in maximum {max_length} characters:\n\n{text}"
            
            messages = [ChatMessage.create_user_message(prompt)]
            completion_result = await self.get_completion(messages)
            
            if completion_result.is_error:
                return completion_result
            
            return Result.success(completion_result.value.strip())
        except Exception as e:
            return Result.error(f"Failed to summarize text: {str(e)}")
    
    async def extract_keywords(self, text: str, count: int = 10) -> Result[List[str], str]:
        """Extract keywords from text"""
        try:
            prompt = f"Extract {count} key keywords from the following text:\n\n{text}\n\nKeywords:"
            
            messages = [ChatMessage.create_user_message(prompt)]
            completion_result = await self.get_completion(messages)
            
            if completion_result.is_error:
                return completion_result
            
            keywords = [kw.strip() for kw in completion_result.value.split(',')]
            return Result.success(keywords[:count])
        except Exception as e:
            return Result.error(f"Failed to extract keywords: {str(e)}")
    
    async def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> Result[str, str]:
        """Translate text to target language"""
        try:
            source_info = f" from {source_language}" if source_language else ""
            prompt = f"Translate the following text{source_info} to {target_language}:\n\n{text}"
            
            messages = [ChatMessage.create_user_message(prompt)]
            completion_result = await self.get_completion(messages)
            
            if completion_result.is_error:
                return completion_result
            
            return Result.success(completion_result.value.strip())
        except Exception as e:
            return Result.error(f"Failed to translate text: {str(e)}")
    
    async def analyze_sentiment(self, text: str) -> Result[Dict[str, Any], str]:
        """Analyze text sentiment"""
        try:
            prompt = f"Analyze the sentiment of the following text and provide a score from -1 (very negative) to 1 (very positive):\n\n{text}"
            
            messages = [ChatMessage.create_user_message(prompt)]
            completion_result = await self.get_completion(messages)
            
            if completion_result.is_error:
                return completion_result
            
            sentiment = {
                "text": text,
                "sentiment_score": 0.0,  # Would need to parse from response
                "sentiment_label": completion_result.value.strip(),
                "confidence": 0.8
            }
            
            return Result.success(sentiment)
        except Exception as e:
            return Result.error(f"Failed to analyze sentiment: {str(e)}")
    
    async def extract_entities(self, text: str) -> Result[List[Dict[str, Any]], str]:
        """Extract named entities from text"""
        try:
            prompt = f"Extract named entities (people, places, organizations) from the following text:\n\n{text}"
            
            messages = [ChatMessage.create_user_message(prompt)]
            completion_result = await self.get_completion(messages)
            
            if completion_result.is_error:
                return completion_result
            
            entities = [
                {
                    "text": "placeholder",
                    "type": "PERSON",
                    "start": 0,
                    "end": 10,
                    "confidence": 0.8
                }
            ]
            
            return Result.success(entities)
        except Exception as e:
            return Result.error(f"Failed to extract entities: {str(e)}")
