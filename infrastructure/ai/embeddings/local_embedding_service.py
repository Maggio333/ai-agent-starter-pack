# infrastructure/ai/embeddings/local_embedding_service.py
import logging
import os
from typing import List, Dict, Any
from domain.utils.result import Result
from .IEmbeddingService import IEmbeddingService

try:
    import torch
    from transformers import AutoTokenizer, AutoModel
except ImportError:
    torch = None
    AutoTokenizer = None
    AutoModel = None
    logging.warning("PyTorch and Transformers not installed. LocalEmbeddingService will not be available.")

class LocalEmbeddingService(IEmbeddingService):
    """
    Local implementation of BaseEmbeddingService using custom models.
    This service uses local models and is free to use.
    Similar to ChatElioraSystem's local embedding approach.
    """
    
    def __init__(self, model_path: str, device: str = "auto"):
        if torch is None or AutoTokenizer is None or AutoModel is None:
            raise ImportError("PyTorch and Transformers libraries are not installed. Please install them with: pip install torch transformers")
        
        self.model_path = model_path
        self.device = self._get_device(device)
        self.logger = logging.getLogger(__name__)
        
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModel.from_pretrained(model_path)
            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            
            # Get model dimensions
            self.dimensions = self.model.config.hidden_size
            
            self.logger.info(f"LocalEmbeddingService initialized with model: {model_path} on device: {self.device}")
        except Exception as e:
            self.logger.error(f"Failed to load local model {model_path}: {e}")
            raise
    
    def _get_device(self, device: str) -> str:
        """Determine the best device to use"""
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"  # Apple Silicon
            else:
                return "cpu"
        return device
    
    async def create_embedding(self, text: str) -> Result[List[float], str]:
        """Generates an embedding for a given text using a local model."""
        try:
            # Tokenize input
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embedding
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use mean pooling of the last hidden state
                embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().tolist()
            
            return Result.success(embedding)
        except Exception as e:
            self.logger.error(f"Failed to create embedding for text: {e}")
            return Result.error(f"Embedding creation failed: {str(e)}")
    
    async def create_embeddings_batch(self, texts: List[str]) -> Result[List[List[float]], str]:
        """Generates embeddings for a batch of texts using a local model."""
        try:
            # Tokenize all texts
            inputs = self.tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use mean pooling of the last hidden state
                embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy().tolist()
            
            return Result.success(embeddings)
        except Exception as e:
            self.logger.error(f"Failed to create embeddings batch: {e}")
            return Result.error(f"Batch embedding creation failed: {str(e)}")
    
    async def get_model_info(self) -> Result[Dict[str, Any], str]:
        """Retrieves information about the local embedding model."""
        info = {
            "provider": "Local",
            "model_path": self.model_path,
            "model_name": os.path.basename(self.model_path),
            "dimensions": self.dimensions,
            "device": self.device,
            "type": "local",
            "config": {
                "vocab_size": self.model.config.vocab_size,
                "hidden_size": self.model.config.hidden_size,
                "num_layers": getattr(self.model.config, 'num_hidden_layers', 'unknown'),
                "model_type": self.model.config.model_type
            }
        }
        return Result.success(info)
    
    async def health_check(self) -> Result[dict, str]:
        """Performs a health check on the local embedding service."""
        try:
            # Try to encode a dummy text to check if the model is loaded and functional
            test_result = await self.create_embedding("health check")
            if test_result.is_error:
                return Result.error(f"Local embedding service health check failed: {test_result.error}")
            
            return Result.success({
                "status": "healthy", 
                "model_path": self.model_path,
                "device": self.device,
                "type": "local",
                "dimensions": self.dimensions
            })
        except Exception as e:
            return Result.error(f"Local embedding service health check failed: {e}")
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information"""
        if self.device == "cuda":
            return {
                "gpu_memory_allocated": torch.cuda.memory_allocated(),
                "gpu_memory_reserved": torch.cuda.memory_reserved(),
                "gpu_memory_max": torch.cuda.max_memory_allocated()
            }
        else:
            return {
                "device": self.device,
                "memory_info": "CPU/MPS memory usage not tracked"
            }
    
    def clear_cache(self):
        """Clear GPU memory cache if using CUDA"""
        if self.device == "cuda":
            torch.cuda.empty_cache()
            self.logger.info("GPU memory cache cleared")
