from typing import Union, TypeVar, Callable, Generic
from dataclasses import dataclass

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')
F = TypeVar('F')

@dataclass
class Result(Generic[T, E]):
    value: T | None
    error: E | None
    
    @property
    def is_success(self) -> bool:
        return self.error is None
    
    @property
    def is_error(self) -> bool:
        return self.error is not None
    
    @classmethod
    def success(cls, value: T) -> 'Result[T, E]':
        return cls(value=value, error=None)
    
    @classmethod
    def error(cls, error: E) -> 'Result[T, E]':
        return cls(value=None, error=error)
    
    def map(self, func: Callable[[T], U]) -> 'Result[U, E]':
        if self.is_success:
            return Result.success(func(self.value))
        return Result.error(self.error)
    
    def bind(self, func: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        if self.is_success:
            return func(self.value)
        return Result.error(self.error)
    
    def map_error(self, func: Callable[[E], F]) -> 'Result[T, F]':
        if self.is_error:
            return Result.error(func(self.error))
        return Result.success(self.value)