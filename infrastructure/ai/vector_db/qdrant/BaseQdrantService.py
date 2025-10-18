# infrastructure/ai/vector_db/qdrant/BaseQdrantService.py
import httpx
import logging
from typing import List, Dict, Any, Optional
from domain.utils.result import Result

class BaseQdrantService:  # Klasa bazowa z wspólną funkcjonalnością
    """Klasa bazowa dla serwisów Qdrant z wspólną funkcjonalnością"""
    
    def __init__(self, url: str = "http://localhost:6333", api_key: Optional[str] = None):
        self.url = url.rstrip('/')
        self.api_key = api_key
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _get_headers(self) -> Dict[str, str]:
        """Zwraca nagłówki HTTP dla żądań do Qdrant"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Result[Dict[str, Any], str]:
        """Wykonuje żądanie HTTP do API Qdrant"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.url}{endpoint}"
                headers = self._get_headers()
                
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(url, headers=headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    return Result.error(f"Unsupported HTTP method: {method}")
                
                if response.status_code in [200, 201]:
                    return Result.success(response.json())
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"Qdrant API error: {error_msg}")
                    return Result.error(error_msg)
                    
        except httpx.TimeoutException:
            error_msg = "Qdrant request timeout"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except httpx.ConnectError:
            error_msg = f"Failed to connect to Qdrant at {self.url}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(error_msg)
            return Result.error(error_msg)
    
    async def health_check(self) -> Result[dict, str]:
        """Sprawdza stan zdrowia serwisu Qdrant"""
        try:
            result = await self._make_request("GET", "/health")
            if result.is_success:
                health_data = {
                    'status': 'healthy',
                    'service': self.__class__.__name__,
                    'url': self.url,
                    'qdrant_response': result.value
                }
                return Result.success(health_data)
            else:
                return Result.error(f"Health check failed: {result.error}")
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return Result.error(f"Health check failed: {str(e)}")
    
    def _validate_collection_name(self, collection_name: str) -> bool:
        """Waliduje format nazwy kolekcji"""
        if not collection_name or not isinstance(collection_name, str):
            return False
        # Nazwy kolekcji Qdrant powinny być alfanumeryczne z podkreśleniami
        return collection_name.replace('_', '').replace('-', '').isalnum()
    
    def _validate_vector_dimension(self, vector: List[float]) -> bool:
        """Waliduje wymiar wektora"""
        if not vector or not isinstance(vector, list):
            return False
        return all(isinstance(x, (int, float)) for x in vector)
