# infrastructure/ai/llm/base_llm_service.py
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import List, AsyncIterator, Dict, Any, Optional
from domain.services.ILLMService import ILLMService
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.utils.result import Result

class BaseLLMService(ILLMService):
    """Base implementation of LLMService with default implementations"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._cache_enabled = False
        self._cache = {}
        self._error_history = []
        self._performance_metrics = {
            "total_requests": 0,
            "total_tokens": 0,
            "avg_response_time": 0.0,
            "error_count": 0
        }
    
    # Core methods that should be implemented by subclasses
    # These have default implementations but can be overridden
    
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        """Get LLM completion - default implementation"""
        return Result.error("get_completion not implemented")
    
    async def stream_completion(self, messages: List[ChatMessage]) -> AsyncIterator[Result[str, str]]:
        """Stream LLM completion - default implementation"""
        # Fallback to regular completion
        result = await self.get_completion(messages)
        yield result
    
    async def get_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> Result[Dict[str, Any], str]:
        """Get completion with tool calling - default implementation"""
        # Fallback to regular completion
        result = await self.get_completion(messages)
        if result.is_success:
            return Result.success({
                "content": result.value,
                "tool_calls": [],
                "role": "assistant"
            })
        return Result.error(result.error)
    
    async def stream_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> AsyncIterator[Result[Dict[str, Any], str]]:
        """Stream completion with tool calling - default implementation"""
        # Fallback to regular streaming
        async for result in self.stream_completion(messages):
            if result.is_success:
                yield Result.success({
                    "content": result.value,
                    "tool_calls": [],
                    "role": "assistant"
                })
            else:
                yield result
    
    async def list_models(self) -> Result[List[Dict[str, Any]], str]:
        """List available models - default implementation"""
        return Result.success([{
            "id": "default",
            "name": "Default Model",
            "provider": "base",
            "capabilities": ["chat", "completion"]
        }])
    
    async def get_current_model(self) -> Result[str, str]:
        """Get current active model - default implementation"""
        return Result.success("default")
    
    async def set_model(self, model_name: str) -> Result[None, str]:
        """Set active model - default implementation"""
        return Result.success(None)
    
    async def get_configuration(self) -> Result[Dict[str, Any], str]:
        """Get current configuration - default implementation"""
        return Result.success({
            "model": "default",
            "provider": "base",
            "temperature": 0.7,
            "max_tokens": 2048
        })
    
    async def update_configuration(self, config: Dict[str, Any]) -> Result[None, str]:
        """Update configuration - default implementation"""
        return Result.success(None)
    
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health - default implementation"""
        return Result.success({
            "status": "healthy",
            "provider": "base",
            "model": "default"
        })
    
    # Default implementations for optional methods
    async def get_model_info(self, model_name: str) -> Result[Dict[str, Any], str]:
        """Get model information - default implementation"""
        try:
            models_result = await self.list_models()
            if models_result.is_error:
                return models_result
            
            models = models_result.value
            model = next((m for m in models if m.get("id") == model_name), None)
            
            if model:
                return Result.success(model)
            else:
                return Result.error(f"Model {model_name} not found")
        except Exception as e:
            return Result.error(f"Failed to get model info: {str(e)}")
    
    async def count_tokens(self, text: str) -> Result[int, str]:
        """Count tokens in text - default implementation"""
        # Simple word-based estimation
        word_count = len(text.split())
        estimated_tokens = int(word_count * 1.3)  # Rough estimation
        return Result.success(estimated_tokens)
    
    async def count_tokens_in_messages(self, messages: List[ChatMessage]) -> Result[int, str]:
        """Count tokens in messages - default implementation"""
        total_tokens = 0
        for message in messages:
            result = await self.count_tokens(message.content)
            if result.is_success:
                total_tokens += result.value
            else:
                return result
        return Result.success(total_tokens)
    
    async def estimate_cost(self, messages: List[ChatMessage]) -> Result[float, str]:
        """Estimate cost - default implementation (free for local models)"""
        return Result.success(0.0)
    
    async def get_usage_stats(self) -> Result[Dict[str, Any], str]:
        """Get usage statistics - default implementation"""
        return Result.success(self._performance_metrics.copy())
    
    async def reset_usage_stats(self) -> Result[None, str]:
        """Reset usage statistics - default implementation"""
        self._performance_metrics = {
            "total_requests": 0,
            "total_tokens": 0,
            "avg_response_time": 0.0,
            "error_count": 0
        }
        return Result.success(None)
    
    async def get_performance_metrics(self) -> Result[Dict[str, Any], str]:
        """Get performance metrics - default implementation"""
        return Result.success(self._performance_metrics.copy())
    
    async def get_error_history(self) -> Result[List[Dict[str, Any]], str]:
        """Get error history - default implementation"""
        return Result.success(self._error_history.copy())
    
    async def clear_error_history(self) -> Result[None, str]:
        """Clear error history - default implementation"""
        self._error_history.clear()
        return Result.success(None)
    
    async def enable_caching(self, enabled: bool = True) -> Result[None, str]:
        """Enable/disable caching - default implementation"""
        self._cache_enabled = enabled
        return Result.success(None)
    
    async def clear_cache(self) -> Result[None, str]:
        """Clear cache - default implementation"""
        self._cache.clear()
        return Result.success(None)
    
    async def get_cache_stats(self) -> Result[Dict[str, Any], str]:
        """Get cache statistics - default implementation"""
        return Result.success({
            "enabled": self._cache_enabled,
            "size": len(self._cache),
            "hits": 0,  # Would need to track this
            "misses": 0  # Would need to track this
        })
    
    async def set_cache_ttl(self, ttl_seconds: int) -> Result[None, str]:
        """Set cache TTL - default implementation"""
        return Result.success(None)
    
    # Conversation Management
    async def start_conversation(self, system_prompt: Optional[str] = None) -> Result[str, str]:
        """Start new conversation session - default implementation"""
        import uuid
        session_id = str(uuid.uuid4())
        return Result.success(session_id)
    
    async def end_conversation(self, session_id: str) -> Result[None, str]:
        """End conversation session - default implementation"""
        return Result.success(None)
    
    async def get_conversation_history(self, session_id: str) -> Result[List[ChatMessage], str]:
        """Get conversation history - default implementation"""
        return Result.success([])
    
    async def clear_conversation_history(self, session_id: str) -> Result[None, str]:
        """Clear conversation history - default implementation"""
        return Result.success(None)
    
    async def set_temperature(self, temperature: float) -> Result[None, str]:
        """Set temperature - default implementation"""
        return Result.success(None)
    
    async def set_top_p(self, top_p: float) -> Result[None, str]:
        """Set top_p - default implementation"""
        return Result.success(None)
    
    async def set_max_tokens(self, max_tokens: int) -> Result[None, str]:
        """Set max tokens - default implementation"""
        return Result.success(None)
    
    async def reset_configuration(self) -> Result[None, str]:
        """Reset configuration - default implementation"""
        return Result.success(None)
    
    # AI Features - default implementations (can be overridden)
    async def analyze_sentiment(self, text: str) -> Result[Dict[str, Any], str]:
        """Analyze sentiment - default implementation"""
        # Simple keyword-based sentiment analysis
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic"]
        negative_words = ["bad", "terrible", "awful", "horrible", "disgusting", "hate"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            score = 0.7
        elif negative_count > positive_count:
            sentiment = "negative"
            score = -0.7
        else:
            sentiment = "neutral"
            score = 0.0
        
        return Result.success({
            "sentiment": sentiment,
            "score": score,
            "confidence": 0.6
        })
    
    async def classify_text(self, text: str, categories: List[str]) -> Result[Dict[str, Any], str]:
        """Classify text - default implementation"""
        # Simple keyword-based classification
        text_lower = text.lower()
        scores = {}
        
        for category in categories:
            category_lower = category.lower()
            if category_lower in text_lower:
                scores[category] = 0.8
            else:
                scores[category] = 0.2
        
        best_category = max(scores, key=scores.get)
        
        return Result.success({
            "category": best_category,
            "scores": scores,
            "confidence": scores[best_category]
        })
    
    async def summarize_text(self, text: str, max_length: int = 100) -> Result[str, str]:
        """Summarize text - default implementation"""
        # Simple truncation-based summarization
        words = text.split()
        if len(words) <= max_length:
            return Result.success(text)
        
        summary = " ".join(words[:max_length]) + "..."
        return Result.success(summary)
    
    async def extract_keywords(self, text: str, count: int = 10) -> Result[List[str], str]:
        """Extract keywords - default implementation"""
        # Simple word frequency-based extraction
        words = text.lower().split()
        word_freq = {}
        
        for word in words:
            # Remove punctuation
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 3:  # Only words longer than 3 characters
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:count]]
        
        return Result.success(keywords)
    
    async def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> Result[str, str]:
        """Translate text - default implementation (returns original text)"""
        return Result.success(text)
    
    async def extract_entities(self, text: str) -> Result[List[Dict[str, Any]], str]:
        """Extract entities - default implementation"""
        # Simple regex-based entity extraction
        import re
        
        entities = []
        
        # Email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        for email in emails:
            entities.append({
                "text": email,
                "type": "email",
                "start": text.find(email),
                "end": text.find(email) + len(email)
            })
        
        # URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        for url in urls:
            entities.append({
                "text": url,
                "type": "url",
                "start": text.find(url),
                "end": text.find(url) + len(url)
            })
        
        return Result.success(entities)
    
    async def get_embedding(self, text: str) -> Result[List[float], str]:
        """Get embedding - default implementation (not supported)"""
        return Result.error("Embeddings not supported in base implementation")
    
    async def get_embeddings(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Get embeddings - default implementation (not supported)"""
        return Result.error("Embeddings not supported in base implementation")
    
    async def batch_completion(self, message_batches: List[List[ChatMessage]]) -> Result[List[str], str]:
        """Process multiple completions in batch - default implementation"""
        results = []
        for messages in message_batches:
            result = await self.get_completion(messages)
            if result.is_success:
                results.append(result.value)
            else:
                return Result.error(f"Batch completion failed: {result.error}")
        return Result.success(results)
    
    async def batch_embeddings(self, text_batches: List[List[str]]) -> Result[List[List[List[float]]], str]:
        """Process multiple embedding batches - default implementation (not supported)"""
        return Result.error("Embeddings not supported in base implementation")
    
    async def parallel_completion(self, messages_list: List[List[ChatMessage]]) -> Result[List[str], str]:
        """Process completions in parallel - default implementation"""
        # Run completions in parallel
        tasks = [self.get_completion(messages) for messages in messages_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        completion_results = []
        for result in results:
            if isinstance(result, Exception):
                return Result.error(f"Parallel completion failed: {str(result)}")
            elif result.is_success:
                completion_results.append(result.value)
            else:
                return Result.error(f"Parallel completion failed: {result.error}")
        
        return Result.success(completion_results)
    
    async def stream_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> AsyncIterator[Result[Dict[str, Any], str]]:
        """Stream completion with tools - default implementation"""
        # For now, just get completion and yield it
        result = await self.get_completion_with_tools(messages, tools)
        yield result
    
    async def check_rate_limit(self) -> Result[bool, str]:
        """Check rate limit - default implementation (no limits for local models)"""
        return Result.success(True)
    
    async def get_rate_limit_info(self) -> Result[Dict[str, Any], str]:
        """Get rate limit info - default implementation"""
        return Result.success({
            "limit": 1000,
            "remaining": 1000,
            "reset_time": None
        })
    
    async def get_quota_info(self) -> Result[Dict[str, Any], str]:
        """Get quota info - default implementation"""
        return Result.success({
            "total": 1000,
            "remaining": 1000,
            "reset_time": None
        })
    
    async def get_response_quality_score(self, response: str) -> Result[float, str]:
        """Get response quality score - default implementation"""
        # Simple quality scoring based on length and content
        score = 0.5  # Base score
        
        if len(response) > 50:
            score += 0.2
        if len(response) > 200:
            score += 0.2
        if any(word in response.lower() for word in ["thank", "please", "help"]):
            score += 0.1
        
        return Result.success(min(score, 1.0))
    
    async def evaluate_response(self, response: str, criteria: List[str]) -> Result[Dict[str, float], str]:
        """Evaluate response - default implementation"""
        scores = {}
        for criterion in criteria:
            if criterion == "length":
                scores[criterion] = min(len(response) / 200, 1.0)
            elif criterion == "clarity":
                scores[criterion] = 0.7  # Default clarity score
            elif criterion == "relevance":
                scores[criterion] = 0.8  # Default relevance score
            else:
                scores[criterion] = 0.5  # Default score for unknown criteria
        
        return Result.success(scores)
    
    async def compare_responses(self, response1: str, response2: str) -> Result[Dict[str, Any], str]:
        """Compare responses - default implementation"""
        return Result.success({
            "similarity": 0.5,
            "length_diff": abs(len(response1) - len(response2)),
            "word_overlap": 0.3
        })
    
    async def optimize_prompt(self, prompt: str) -> Result[str, str]:
        """Optimize prompt - default implementation"""
        return Result.success(prompt)
    
    async def validate_prompt(self, prompt: str) -> Result[Dict[str, Any], str]:
        """Validate prompt - default implementation"""
        return Result.success({
            "valid": len(prompt.strip()) > 0,
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "quality_score": 0.7
        })
    
    async def get_prompt_suggestions(self, context: str) -> Result[List[str], str]:
        """Get prompt suggestions - default implementation"""
        suggestions = [
            "Can you help me with...",
            "What do you think about...",
            "How can I...",
            "Tell me more about...",
            "What is the best way to..."
        ]
        return Result.success(suggestions)
    
    async def register_custom_function(self, function: Dict[str, Any]) -> Result[None, str]:
        """Register custom function - default implementation"""
        return Result.success(None)
    
    async def unregister_custom_function(self, function_name: str) -> Result[None, str]:
        """Unregister custom function - default implementation"""
        return Result.success(None)
    
    async def list_custom_functions(self) -> Result[List[Dict[str, Any]], str]:
        """List custom functions - default implementation"""
        return Result.success([])
    
    # Helper methods
    def _log_error(self, error_msg: str, exception: Exception = None):
        """Log error and add to history"""
        self.logger.error(error_msg)
        if exception:
            self.logger.exception("Exception details:")
        
        self._error_history.append({
            "timestamp": asyncio.get_event_loop().time(),
            "error": error_msg,
            "exception": str(exception) if exception else None
        })
        
        # Keep only last 100 errors
        if len(self._error_history) > 100:
            self._error_history = self._error_history[-100:]
    
    def _update_metrics(self, response_time: float, token_count: int = 0):
        """Update performance metrics"""
        self._performance_metrics["total_requests"] += 1
        self._performance_metrics["total_tokens"] += token_count
        
        # Update average response time
        total_requests = self._performance_metrics["total_requests"]
        current_avg = self._performance_metrics["avg_response_time"]
        self._performance_metrics["avg_response_time"] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )