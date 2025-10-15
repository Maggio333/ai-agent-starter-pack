# infrastructure/ai/vector_db/qdrant/collection_service.py
from typing import List, Dict, Any, Optional
from domain.utils.result import Result
from .base_qdrant_service import BaseQdrantService

class CollectionService(BaseQdrantService):
    """Service for managing Qdrant collections"""
    
    async def create_collection(self, collection_name: str, vector_size: int = 384, distance: str = "Cosine") -> Result[None, str]:
        """Create a new collection"""
        self.logger.info(f"Creating collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        # Ensure vector_size is an integer
        try:
            vector_size = int(vector_size)
        except (ValueError, TypeError):
            return Result.error(f"Invalid vector size: {vector_size}")
        
        if vector_size <= 0:
            return Result.error(f"Invalid vector size: {vector_size}")
        
        data = {
            "vectors": {
                "size": vector_size,
                "distance": distance
            }
        }
        
        result = await self._make_request("PUT", f"/collections/{collection_name}", data)
        
        if result.is_success:
            self.logger.info(f"Collection created successfully: {collection_name}")
            return Result.success(None)
        else:
            self.logger.error(f"Failed to create collection: {result.error}")
            return result
    
    async def delete_collection(self, collection_name: str) -> Result[None, str]:
        """Delete a collection"""
        self.logger.info(f"Deleting collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        result = await self._make_request("DELETE", f"/collections/{collection_name}")
        
        if result.is_success:
            self.logger.info(f"Collection deleted successfully: {collection_name}")
            return Result.success(None)
        else:
            self.logger.error(f"Failed to delete collection: {result.error}")
            return result
    
    async def get_collection_info(self, collection_name: str) -> Result[Dict[str, Any], str]:
        """Get collection information"""
        self.logger.info(f"Getting collection info: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        result = await self._make_request("GET", f"/collections/{collection_name}")
        
        if result.is_success:
            self.logger.info(f"Collection info retrieved: {collection_name}")
            return result
        else:
            self.logger.error(f"Failed to get collection info: {result.error}")
            return result
    
    async def list_collections(self) -> Result[List[str], str]:
        """List all collections"""
        self.logger.info("Listing collections")
        
        result = await self._make_request("GET", "/collections")
        
        if result.is_success:
            collections = [col["name"] for col in result.value.get("result", {}).get("collections", [])]
            self.logger.info(f"Found {len(collections)} collections")
            return Result.success(collections)
        else:
            self.logger.error(f"Failed to list collections: {result.error}")
            return result
    
    async def collection_exists(self, collection_name: str) -> Result[bool, str]:
        """Check if collection exists"""
        self.logger.info(f"Checking if collection exists: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        result = await self.get_collection_info(collection_name)
        
        if result.is_success:
            return Result.success(True)
        elif "not found" in result.error.lower():
            return Result.success(False)
        else:
            return result
    
    async def get_collection_stats(self, collection_name: str) -> Result[Dict[str, Any], str]:
        """Get collection statistics"""
        self.logger.info(f"Getting collection stats: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        result = await self._make_request("GET", f"/collections/{collection_name}/stats")
        
        if result.is_success:
            stats = result.value.get("result", {})
            self.logger.info(f"Collection stats retrieved: {collection_name}")
            return Result.success(stats)
        else:
            self.logger.error(f"Failed to get collection stats: {result.error}")
            return result
