# domain/services/rop_service.py
from domain.utils.result import Result
from typing import Callable, TypeVar, Awaitable, Coroutine

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')

class ROPService:
    """Railway Oriented Programming Service"""
    
    @staticmethod
    def pipeline(*functions: Callable) -> Callable:
        """Chain multiple functions in ROP style (synchronous)"""
        def pipeline_func(input_value):
            result = Result.success(input_value)
            for func in functions:
                result = result.bind(func)
            return result
        return pipeline_func
    
    @staticmethod
    def async_pipeline(*functions: Callable) -> Callable:
        """Chain multiple async functions in ROP style (asynchronous)
        
        Returns an async function that processes input through the pipeline.
        Functions should be async and return Result[T, E] or Awaitable[Result[T, E]]
        """
        async def pipeline_func(input_value):
            result = Result.success(input_value)
            for func in functions:
                # If result is error, return early (Railway pattern)
                if result.is_error:
                    return result
                
                # Execute async function
                func_result = func(result.value)
                
                # Handle both async and sync results
                if isinstance(func_result, Coroutine):
                    func_result = await func_result
                
                # func should return Result[U, E]
                if isinstance(func_result, Result):
                    result = func_result
                else:
                    # If function doesn't return Result, wrap it
                    result = Result.success(func_result)
            
            return result
        return pipeline_func
    
    @staticmethod
    def try_catch(func: Callable[[T], U]) -> Callable[[T], Result[U, Exception]]:
        """Wrap function to return Result instead of raising exceptions"""
        def wrapper(value: T) -> Result[U, Exception]:
            try:
                return Result.success(func(value))
            except Exception as e:
                return Result.error(e)
        return wrapper
    
    @staticmethod
    def validate(validator: Callable[[T], bool], error_msg: str) -> Callable[[T], Result[T, str]]:
        """Create validation function"""
        def validator_func(value: T) -> Result[T, str]:
            if validator(value):
                return Result.success(value)
            return Result.error(error_msg)
        return validator_func