# domain/services/llm_service.py
from abc import ABC, abstractmethod
from typing import List, AsyncIterator, Dict, Any, Optional
from domain.entities.chat_message import ChatMessage
from domain.utils.result import Result

class LLMService(ABC):
    """Enhanced LLM service interface with comprehensive AI capabilities"""
    
    # Basic Completion Operations
    @abstractmethod
    async def get_completion(self, messages: List[ChatMessage]) -> Result[str, str]:
        """Get LLM completion"""
        pass
    
    @abstractmethod
    async def stream_completion(self, messages: List[ChatMessage]) -> AsyncIterator[Result[str, str]]:
        """Stream LLM completion"""
        pass
    
    # Tool Calling Support
    @abstractmethod
    async def get_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> Result[Dict[str, Any], str]:
        """Get completion with tool calling support"""
        pass
    
    @abstractmethod
    async def stream_completion_with_tools(self, messages: List[ChatMessage], tools: List[Dict[str, Any]]) -> AsyncIterator[Result[Dict[str, Any], str]]:
        """Stream completion with tool calling support"""
        pass
    
    # Model Management
    @abstractmethod
    async def list_models(self) -> Result[List[Dict[str, Any]], str]:
        """List available models"""
        pass
    
    @abstractmethod
    async def get_model_info(self, model_name: str) -> Result[Dict[str, Any], str]:
        """Get model information"""
        pass
    
    @abstractmethod
    async def set_model(self, model_name: str) -> Result[None, str]:
        """Set active model"""
        pass
    
    @abstractmethod
    async def get_current_model(self) -> Result[str, str]:
        """Get current active model"""
        pass
    
    # Configuration & Settings
    @abstractmethod
    async def get_configuration(self) -> Result[Dict[str, Any], str]:
        """Get current configuration"""
        pass
    
    @abstractmethod
    async def update_configuration(self, config: Dict[str, Any]) -> Result[None, str]:
        """Update configuration"""
        pass
    
    @abstractmethod
    async def reset_configuration(self) -> Result[None, str]:
        """Reset to default configuration"""
        pass
    
    @abstractmethod
    async def set_temperature(self, temperature: float) -> Result[None, str]:
        """Set temperature parameter"""
        pass
    
    @abstractmethod
    async def set_max_tokens(self, max_tokens: int) -> Result[None, str]:
        """Set max tokens parameter"""
        pass
    
    @abstractmethod
    async def set_top_p(self, top_p: float) -> Result[None, str]:
        """Set top_p parameter"""
        pass
    
    # Token Management
    @abstractmethod
    async def count_tokens(self, text: str) -> Result[int, str]:
        """Count tokens in text"""
        pass
    
    @abstractmethod
    async def count_tokens_in_messages(self, messages: List[ChatMessage]) -> Result[int, str]:
        """Count tokens in messages"""
        pass
    
    @abstractmethod
    async def estimate_cost(self, messages: List[ChatMessage]) -> Result[Dict[str, Any], str]:
        """Estimate API cost for messages"""
        pass
    
    @abstractmethod
    async def get_usage_stats(self) -> Result[Dict[str, Any], str]:
        """Get usage statistics"""
        pass
    
    @abstractmethod
    async def reset_usage_stats(self) -> Result[None, str]:
        """Reset usage statistics"""
        pass
    
    # Advanced AI Features
    @abstractmethod
    async def get_embeddings(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Get text embeddings"""
        pass
    
    @abstractmethod
    async def get_embedding(self, text: str) -> Result[List[float], str]:
        """Get single text embedding"""
        pass
    
    @abstractmethod
    async def classify_text(self, text: str, categories: List[str]) -> Result[Dict[str, Any], str]:
        """Classify text into categories"""
        pass
    
    @abstractmethod
    async def summarize_text(self, text: str, max_length: int = 100) -> Result[str, str]:
        """Summarize text"""
        pass
    
    @abstractmethod
    async def extract_keywords(self, text: str, count: int = 10) -> Result[List[str], str]:
        """Extract keywords from text"""
        pass
    
    @abstractmethod
    async def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> Result[str, str]:
        """Translate text to target language"""
        pass
    
    @abstractmethod
    async def analyze_sentiment(self, text: str) -> Result[Dict[str, Any], str]:
        """Analyze text sentiment"""
        pass
    
    @abstractmethod
    async def extract_entities(self, text: str) -> Result[List[Dict[str, Any]], str]:
        """Extract named entities from text"""
        pass
    
    # Error Handling & Monitoring
    @abstractmethod
    async def health_check(self) -> Result[Dict[str, Any], str]:
        """Check service health"""
        pass
    
    @abstractmethod
    async def get_error_history(self) -> Result[List[Dict[str, Any]], str]:
        """Get error history"""
        pass
    
    @abstractmethod
    async def clear_error_history(self) -> Result[None, str]:
        """Clear error history"""
        pass
    
    @abstractmethod
    async def get_performance_metrics(self) -> Result[Dict[str, Any], str]:
        """Get performance metrics"""
        pass
    
    # Caching & Performance
    @abstractmethod
    async def enable_caching(self, enabled: bool = True) -> Result[None, str]:
        """Enable/disable response caching"""
        pass
    
    @abstractmethod
    async def clear_cache(self) -> Result[None, str]:
        """Clear response cache"""
        pass
    
    @abstractmethod
    async def get_cache_stats(self) -> Result[Dict[str, Any], str]:
        """Get cache statistics"""
        pass
    
    @abstractmethod
    async def set_cache_ttl(self, ttl_seconds: int) -> Result[None, str]:
        """Set cache time-to-live"""
        pass
    
    # Batch Processing
    @abstractmethod
    async def batch_completion(self, message_batches: List[List[ChatMessage]]) -> Result[List[str], str]:
        """Process multiple completions in batch"""
        pass
    
    @abstractmethod
    async def parallel_completion(self, messages_list: List[List[ChatMessage]]) -> Result[List[str], str]:
        """Process completions in parallel"""
        pass
    
    @abstractmethod
    async def batch_embeddings(self, text_batches: List[List[str]]) -> Result[List[List[List[float]]], str]:
        """Process multiple embedding batches"""
        pass
    
    # Prompt Engineering
    @abstractmethod
    async def optimize_prompt(self, prompt: str, context: Optional[str] = None) -> Result[str, str]:
        """Optimize prompt for better results"""
        pass
    
    @abstractmethod
    async def validate_prompt(self, prompt: str) -> Result[Dict[str, Any], str]:
        """Validate prompt quality"""
        pass
    
    @abstractmethod
    async def get_prompt_suggestions(self, task: str) -> Result[List[str], str]:
        """Get prompt suggestions for task"""
        pass
    
    # Conversation Management
    @abstractmethod
    async def start_conversation(self, system_prompt: Optional[str] = None) -> Result[str, str]:
        """Start new conversation session"""
        pass
    
    @abstractmethod
    async def end_conversation(self, session_id: str) -> Result[None, str]:
        """End conversation session"""
        pass
    
    @abstractmethod
    async def get_conversation_history(self, session_id: str) -> Result[List[ChatMessage], str]:
        """Get conversation history"""
        pass
    
    @abstractmethod
    async def clear_conversation_history(self, session_id: str) -> Result[None, str]:
        """Clear conversation history"""
        pass
    
    # Quality & Evaluation
    @abstractmethod
    async def evaluate_response(self, prompt: str, response: str, criteria: List[str]) -> Result[Dict[str, Any], str]:
        """Evaluate response quality"""
        pass
    
    @abstractmethod
    async def compare_responses(self, prompt: str, responses: List[str]) -> Result[Dict[str, Any], str]:
        """Compare multiple responses"""
        pass
    
    @abstractmethod
    async def get_response_quality_score(self, response: str) -> Result[float, str]:
        """Get response quality score"""
        pass
    
    # Custom Functions
    @abstractmethod
    async def register_custom_function(self, function_name: str, function_schema: Dict[str, Any]) -> Result[None, str]:
        """Register custom function for tool calling"""
        pass
    
    @abstractmethod
    async def unregister_custom_function(self, function_name: str) -> Result[None, str]:
        """Unregister custom function"""
        pass
    
    @abstractmethod
    async def list_custom_functions(self) -> Result[List[Dict[str, Any]], str]:
        """List registered custom functions"""
        pass
    
    # Rate Limiting & Quotas
    @abstractmethod
    async def get_rate_limit_info(self) -> Result[Dict[str, Any], str]:
        """Get rate limit information"""
        pass
    
    @abstractmethod
    async def check_rate_limit(self) -> Result[bool, str]:
        """Check if rate limit allows request"""
        pass
    
    @abstractmethod
    async def get_quota_info(self) -> Result[Dict[str, Any], str]:
        """Get quota information"""
        pass
