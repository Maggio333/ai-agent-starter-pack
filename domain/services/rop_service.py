# domain/services/rop_service.py
from domain.utils.result import Result
from typing import Callable, TypeVar

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')

class ROPService:
    """Railway Oriented Programming Service"""
    
    @staticmethod
    def pipeline(*functions: Callable) -> Callable:
        """Chain multiple functions in ROP style"""
        def pipeline_func(input_value):
            result = Result.success(input_value)
            for func in functions:
                result = result.bind(func)
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