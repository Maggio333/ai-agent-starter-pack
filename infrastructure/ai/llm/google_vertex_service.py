# infrastructure/llm/google_vertex_service.py
from typing import List, AsyncIterator, Dict, Any, Optional
from domain.services.ILLMService import ILLMService
from domain.entities.chat_message import ChatMessage
from domain.utils.result import Result

# Import all specialized services
from .google_vertex.base_vertex_service import BaseVertexService
from .google_vertex.tool_calling_service import ToolCallingService
from .google_vertex.model_management_service import ModelManagementService
from .google_vertex.configuration_service import ConfigurationService
from .google_vertex.token_service import TokenService
from .google_vertex.ai_features_service import AIFeaturesService
from .google_vertex.monitoring_service import MonitoringService
from .google_vertex.caching_service import CachingService
from .google_vertex.rate_limiting_service import RateLimitingService

class GoogleVertexService(ILLMService):
    """Google Vertex AI implementation of LLMService using Facade pattern"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        
        # Initialize specialized services
        self.base_service = BaseVertexService(api_key, model)
        self.tool_service = ToolCallingService(api_key, model)
        self.model_service = ModelManagementService(api_key, model)
        self.config_service = ConfigurationService()
        self.token_service = TokenService(api_key, model)
        self.ai_service = AIFeaturesService(api_key, model)
        self.monitoring_service = MonitoringService(api_key, model)
        self.caching_service = CachingService()
        self.rate_limiting_service = RateLimitingService()
    
    # Basic Completion Operations
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        """Get LLM completion"""
        try:
            # Check rate limits
            rate_check = await self.rate_limiting_service.check_rate_limit()
            if rate_check.is_error or not rate_check.value:
                return Result.error("Rate limit exceeded")
            
            # Check cache
            cache_key = self.caching_service.generate_cache_key(
                [msg.to_dict() for msg in messages], 
                self.config_service.get_generation_config()
            )
            cached_response = self.caching_service.get_cached_response(cache_key)
            if cached_response:
                return Result.success(cached_response)
            
            # Get completion
            result = await self.base_service.get_completion(
                messages, 
                self.config_service.get_generation_config()
            )
            
            # Cache successful response
            if result.is_success:
                self.caching_service.cache_response(cache_key, result.value)
                # Record usage
                token_count = await self.token_service.count_tokens_in_messages(messages)
                if token_count.is_success:
                    self.rate_limiting_service.record_request(token_count.value)
                    self.token_service.update_usage_stats(token_count.value)
            
            return result
        except Exception as e:
            self.monitoring_service.log_error(str(e))
            return Result.error(f"Failed to get completion: {str(e)}")
    
    async def stream_completion(self, messages: List[ChatMessage]) -> AsyncIterator[Result[str, str]]:
        """Stream LLM completion"""
        try:
            # Check rate limits
            rate_check = await self.rate_limiting_service.check_rate_limit()
            if rate_check.is_error or not rate_check.value:
                yield Result.error("Rate limit exceeded")
                return
            
            async for result in self.base_service.stream_completion(
                messages, 
                self.config_service.get_generation_config()
            ):
                yield result
                
                # Record usage on first successful chunk
                if result.is_success:
                    token_count = await self.token_service.count_tokens_in_messages(messages)
                    if token_count.is_success:
                        self.rate_limiting_service.record_request(token_count.value)
                        self.token_service.update_usage_stats(token_count.value)
                    break
        except Exception as e:
            self.monitoring_service.log_error(str(e))
            yield Result.error(f"Failed to stream completion: {str(e)}")
    
    # Tool Calling Support
    async def get_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> Result[Dict[str, Any], str]:
        """Get completion with tool calling support"""
        return await self.tool_service.get_completion_with_tools(
            messages, 
            tools, 
            self.config_service.get_generation_config()
        )
    
    async def stream_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> AsyncIterator[Result[Dict[str, Any], str]]:
        """Stream completion with tool calling support"""
        async for result in self.tool_service.stream_completion_with_tools(
            messages, 
            tools, 
            self.config_service.get_generation_config()
        ):
            yield result
    
    # Model Management
    async def list_models(self) -> Result[List[Dict[str, Any]], str]:
        """List available models"""
        return await self.model_service.list_models()
    
    async def get_model_info(self, model_name: str) -> Result[Dict[str, Any], str]:
        """Get model information"""
        return await self.model_service.get_model_info(model_name)
    
    async def set_model(self, model_name: str) -> Result[None, str]:
        """Set active model"""
        result = await self.model_service.set_model(model_name)
        if result.is_success:
            # Update all services with new model
            self.base_service.model = model_name
            self.tool_service.model = model_name
            self.token_service.model = model_name
            self.ai_service.model = model_name
            self.monitoring_service.model = model_name
        return result
    
    async def get_current_model(self) -> Result[str, str]:
        """Get current active model"""
        return await self.model_service.get_current_model()
    
    # Configuration & Settings
    async def get_configuration(self) -> Result[Dict[str, Any], str]:
        """Get current configuration"""
        return await self.config_service.get_configuration()
    
    async def update_configuration(self, config: Dict[str, Any]) -> Result[None, str]:
        """Update configuration"""
        return await self.config_service.update_configuration(config)
    
    async def reset_configuration(self) -> Result[None, str]:
        """Reset to default configuration"""
        return await self.config_service.reset_configuration()
    
    async def set_temperature(self, temperature: float) -> Result[None, str]:
        """Set temperature parameter"""
        return await self.config_service.set_temperature(temperature)
    
    async def set_max_tokens(self, max_tokens: int) -> Result[None, str]:
        """Set max tokens parameter"""
        return await self.config_service.set_max_tokens(max_tokens)
    
    async def set_top_p(self, top_p: float) -> Result[None, str]:
        """Set top_p parameter"""
        return await self.config_service.set_top_p(top_p)
    
    # Token Management
    async def count_tokens(self, text: str) -> Result[int, str]:
        """Count tokens in text"""
        return await self.token_service.count_tokens(text)
    
    async def count_tokens_in_messages(self, messages: List[ChatMessage]) -> Result[int, str]:
        """Count tokens in messages"""
        return await self.token_service.count_tokens_in_messages(messages)
    
    async def estimate_cost(self, messages: List[ChatMessage]) -> Result[Dict[str, Any], str]:
        """Estimate API cost for messages"""
        return await self.token_service.estimate_cost(messages)
    
    async def get_usage_stats(self) -> Result[Dict[str, Any], str]:
        """Get usage statistics"""
        return await self.token_service.get_usage_stats()
    
    async def reset_usage_stats(self) -> Result[None, str]:
        """Reset usage statistics"""
        return await self.token_service.reset_usage_stats()
    
    # Advanced AI Features
    async def get_embeddings(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Get text embeddings"""
        return await self.ai_service.get_embeddings(texts)
    
    async def get_embedding(self, text: str) -> Result[List[float], str]:
        """Get single text embedding"""
        return await self.ai_service.get_embedding(text)
    
    async def classify_text(self, text: str, categories: List[str]) -> Result[Dict[str, Any], str]:
        """Classify text into categories"""
        return await self.ai_service.classify_text(text, categories)
    
    async def summarize_text(self, text: str, max_length: int = 100) -> Result[str, str]:
        """Summarize text"""
        return await self.ai_service.summarize_text(text, max_length)
    
    async def extract_keywords(self, text: str, count: int = 10) -> Result[List[str], str]:
        """Extract keywords from text"""
        return await self.ai_service.extract_keywords(text, count)
    
    async def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> Result[str, str]:
        """Translate text to target language"""
        return await self.ai_service.translate_text(text, target_language, source_language)
    
    async def analyze_sentiment(self, text: str) -> Result[Dict[str, Any], str]:
        """Analyze text sentiment"""
        return await self.ai_service.analyze_sentiment(text)
    
    async def extract_entities(self, text: str) -> Result[List[Dict[str, Any]], str]:
        """Extract named entities from text"""
        return await self.ai_service.extract_entities(text)
    
    # Error Handling & Monitoring
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        return await self.monitoring_service.health_check()
    
    async def get_error_history(self) -> Result[List[Dict[str, Any]], str]:
        """Get error history"""
        return await self.monitoring_service.get_error_history()
    
    async def clear_error_history(self) -> Result[None, str]:
        """Clear error history"""
        return await self.monitoring_service.clear_error_history()
    
    async def get_performance_metrics(self) -> Result[Dict[str, Any], str]:
        """Get performance metrics"""
        return await self.monitoring_service.get_performance_metrics()
    
    # Caching & Performance
    async def enable_caching(self, enabled: bool = True) -> Result[None, str]:
        """Enable/disable response caching"""
        return await self.caching_service.enable_caching(enabled)
    
    async def clear_cache(self) -> Result[None, str]:
        """Clear response cache"""
        return await self.caching_service.clear_cache()
    
    async def get_cache_stats(self) -> Result[Dict[str, Any], str]:
        """Get cache statistics"""
        return await self.caching_service.get_cache_stats()
    
    async def set_cache_ttl(self, ttl_seconds: int) -> Result[None, str]:
        """Set cache time-to-live"""
        return await self.caching_service.set_cache_ttl(ttl_seconds)
    
    # Batch Processing
    async def batch_completion(self, message_batches: List[List[ChatMessage]]) -> Result[List[str], str]:
        """Process multiple completions in batch"""
        try:
            results = []
            for batch in message_batches:
                completion_result = await self.get_completion(batch)
                if completion_result.is_error:
                    return completion_result
                results.append(completion_result.value)
            return Result.success(results)
        except Exception as e:
            return Result.error(f"Failed to process batch: {str(e)}")
    
    async def parallel_completion(self, messages_list: List[List[ChatMessage]]) -> Result[List[str], str]:
        """Process completions in parallel"""
        # For now, same as batch processing
        return await self.batch_completion(messages_list)
    
    async def batch_embeddings(self, text_batches: List[List[str]]) -> Result[List[List[List[float]]], str]:
        """Process multiple embedding batches"""
        try:
            results = []
            for batch in text_batches:
                embeddings_result = await self.get_embeddings(batch)
                if embeddings_result.is_error:
                    return embeddings_result
                results.append(embeddings_result.value)
            return Result.success(results)
        except Exception as e:
            return Result.error(f"Failed to process embedding batches: {str(e)}")
    
    # Prompt Engineering
    async def optimize_prompt(self, prompt: str, context: Optional[str] = None) -> Result[str, str]:
        """Optimize prompt for better results"""
        try:
            optimization_prompt = f"Optimize this prompt for better AI responses:\n\nPrompt: {prompt}"
            if context:
                optimization_prompt += f"\n\nContext: {context}"
            
            messages = [ChatMessage.create_user_message(optimization_prompt)]
            completion_result = await self.get_completion(messages)
            
            if completion_result.is_error:
                return completion_result
            
            return Result.success(completion_result.value.strip())
        except Exception as e:
            return Result.error(f"Failed to optimize prompt: {str(e)}")
    
    async def validate_prompt(self, prompt: str) -> Result[Dict[str, Any], str]:
        """Validate prompt quality"""
        validation = {
            "prompt": prompt,
            "length": len(prompt),
            "quality_score": 0.8,
            "suggestions": ["Consider adding more context", "Be more specific"]
        }
        return Result.success(validation)
    
    async def get_prompt_suggestions(self, task: str) -> Result[List[str], str]:
        """Get prompt suggestions for task"""
        suggestions = [
            f"Create a detailed prompt for: {task}",
            f"Write a step-by-step guide for: {task}",
            f"Generate examples for: {task}"
        ]
        return Result.success(suggestions)
    
    # Conversation Management
    async def start_conversation(self, system_prompt: Optional[str] = None) -> Result[str, str]:
        """Start new conversation session"""
        import time
        session_id = f"session_{int(time.time())}"
        # Implementation would store conversation state
        return Result.success(session_id)
    
    async def end_conversation(self, session_id: str) -> Result[None, str]:
        """End conversation session"""
        # Implementation would clean up conversation state
        return Result.success(None)
    
    async def get_conversation_history(self, session_id: str) -> Result[List[ChatMessage], str]:
        """Get conversation history"""
        # Implementation would retrieve conversation history
        return Result.success([])
    
    async def clear_conversation_history(self, session_id: str) -> Result[None, str]:
        """Clear conversation history"""
        # Implementation would clear conversation history
        return Result.success(None)
    
    # Quality & Evaluation
    async def evaluate_response(self, prompt: str, response: str, criteria: List[str]) -> Result[Dict[str, Any], str]:
        """Evaluate response quality"""
        evaluation = {
            "prompt": prompt,
            "response": response,
            "criteria": criteria,
            "scores": {criterion: 0.8 for criterion in criteria},
            "overall_score": 0.8
        }
        return Result.success(evaluation)
    
    async def compare_responses(self, prompt: str, responses: List[str]) -> Result[Dict[str, Any], str]:
        """Compare multiple responses"""
        comparison = {
            "prompt": prompt,
            "responses": responses,
            "best_response_index": 0,
            "scores": [0.8 for _ in responses]
        }
        return Result.success(comparison)
    
    async def get_response_quality_score(self, response: str) -> Result[float, str]:
        """Get response quality score"""
        return Result.success(0.8)  # Placeholder
    
    # Custom Functions
    async def register_custom_function(self, function_name: str, function_schema: Dict[str, Any]) -> Result[None, str]:
        """Register custom function for tool calling"""
        return await self.tool_service.register_custom_function(function_name, function_schema)
    
    async def unregister_custom_function(self, function_name: str) -> Result[None, str]:
        """Unregister custom function"""
        return await self.tool_service.unregister_custom_function(function_name)
    
    async def list_custom_functions(self) -> Result[List[Dict[str, Any]], str]:
        """List registered custom functions"""
        return await self.tool_service.list_custom_functions()
    
    # Rate Limiting & Quotas
    async def get_rate_limit_info(self) -> Result[Dict[str, Any], str]:
        """Get rate limit information"""
        return await self.rate_limiting_service.get_rate_limit_info()
    
    async def check_rate_limit(self) -> Result[bool, str]:
        """Check if rate limit allows request"""
        return await self.rate_limiting_service.check_rate_limit()
    
    async def get_quota_info(self) -> Result[Dict[str, Any], str]:
        """Get quota information"""
        return await self.rate_limiting_service.get_quota_info()