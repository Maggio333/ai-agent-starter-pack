# infrastructure/ai/vector_db/qdrant/embedding_service.py
from typing import List, Dict, Any, Optional
from domain.utils.result import Result
from .base_qdrant_service import BaseQdrantService

class EmbeddingService(BaseQdrantService):
    """Service for managing embeddings in Qdrant"""
    
    async def upsert_points(self, collection_name: str, points: List[Dict[str, Any]]) -> Result[None, str]:
        """Upsert points (vectors with payload) to collection"""
        self.logger.info(f"Upserting {len(points)} points to collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        if not points:
            return Result.error("No points provided")
        
        # Validate points structure
        for i, point in enumerate(points):
            if not isinstance(point, dict):
                return Result.error(f"Point {i} is not a dictionary")
            
            if "id" not in point:
                return Result.error(f"Point {i} missing 'id' field")
            
            if "vector" not in point:
                return Result.error(f"Point {i} missing 'vector' field")
            
            if not self._validate_vector_dimension(point["vector"]):
                return Result.error(f"Point {i} has invalid vector")
        
        data = {
            "points": points
        }
        
        result = await self._make_request("PUT", f"/collections/{collection_name}/points", data)
        
        if result.is_success:
            self.logger.info(f"Successfully upserted {len(points)} points to {collection_name}")
            return Result.success(None)
        else:
            self.logger.error(f"Failed to upsert points: {result.error}")
            return result
    
    async def delete_points(self, collection_name: str, point_ids: List[str]) -> Result[None, str]:
        """Delete points by IDs"""
        self.logger.info(f"Deleting {len(point_ids)} points from collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        if not point_ids:
            return Result.error("No point IDs provided")
        
        data = {
            "points": point_ids
        }
        
        result = await self._make_request("POST", f"/collections/{collection_name}/points/delete", data)
        
        if result.is_success:
            self.logger.info(f"Successfully deleted {len(point_ids)} points from {collection_name}")
            return Result.success(None)
        else:
            self.logger.error(f"Failed to delete points: {result.error}")
            return result
    
    async def get_points(self, collection_name: str, point_ids: List[str]) -> Result[List[Dict[str, Any]], str]:
        """Get points by IDs"""
        self.logger.info(f"Getting {len(point_ids)} points from collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        if not point_ids:
            return Result.error("No point IDs provided")
        
        data = {
            "ids": point_ids,
            "with_payload": True,
            "with_vector": True
        }
        
        result = await self._make_request("POST", f"/collections/{collection_name}/points", data)
        
        if result.is_success:
            points = result.value.get("result", [])
            self.logger.info(f"Retrieved {len(points)} points from {collection_name}")
            return Result.success(points)
        else:
            self.logger.error(f"Failed to get points: {result.error}")
            return result
    
    async def update_points(self, collection_name: str, points: List[Dict[str, Any]]) -> Result[None, str]:
        """Update points payload"""
        self.logger.info(f"Updating {len(points)} points in collection: {collection_name}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        if not points:
            return Result.error("No points provided")
        
        # Validate points structure for updates
        for i, point in enumerate(points):
            if not isinstance(point, dict):
                return Result.error(f"Point {i} is not a dictionary")
            
            if "id" not in point:
                return Result.error(f"Point {i} missing 'id' field")
            
            if "payload" not in point:
                return Result.error(f"Point {i} missing 'payload' field")
        
        data = {
            "points": points
        }
        
        result = await self._make_request("POST", f"/collections/{collection_name}/points/payload", data)
        
        if result.is_success:
            self.logger.info(f"Successfully updated {len(points)} points in {collection_name}")
            return Result.success(None)
        else:
            self.logger.error(f"Failed to update points: {result.error}")
            return result
    
    async def scroll_points(self, collection_name: str, limit: int = 10, offset: Optional[str] = None) -> Result[Dict[str, Any], str]:
        """Scroll through points in collection"""
        self.logger.info(f"Scrolling points in collection: {collection_name}, limit: {limit}")
        
        if not self._validate_collection_name(collection_name):
            return Result.error(f"Invalid collection name: {collection_name}")
        
        data = {
            "limit": limit,
            "with_payload": True,
            "with_vector": False
        }
        
        if offset:
            data["offset"] = offset
        
        result = await self._make_request("POST", f"/collections/{collection_name}/points/scroll", data)
        
        if result.is_success:
            scroll_result = result.value.get("result", {})
            points_count = len(scroll_result.get("points", []))
            self.logger.info(f"Scrolled {points_count} points from {collection_name}")
            return Result.success(scroll_result)
        else:
            self.logger.error(f"Failed to scroll points: {result.error}")
            return result
