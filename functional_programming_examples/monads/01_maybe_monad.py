"""
1. The Maybe Monad

This module implements the Maybe monad, which represents optional values and
handles computations that might fail or return None.
"""
from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, Union, Optional
from dataclasses import dataclass

T = TypeVar('T')
U = TypeVar('U')

class Maybe(Generic[T]):
    """Base class for the Maybe monad."""
    
    @classmethod
    def unit(cls, value: U) -> Maybe[U]:
        """Wrap a value in a Maybe monad (Just)."""
        return Just(value)
    
    @classmethod
    def nothing(cls) -> Maybe[Any]:
        """Create a Nothing value."""
        return Nothing()
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Bind operation for the Maybe monad."""
        raise NotImplementedError
    
    def map(self, func: Callable[[T], U]) -> Maybe[U]:
        """Map a function over the Maybe value."""
        return self.bind(lambda x: Maybe.unit(func(x)))
    
    def get_or_else(self, default: U) -> Union[T, U]:
        """Get the value or return a default if Nothing."""
        raise NotImplementedError
    
    def is_just(self) -> bool:
        """Check if this is a Just value."""
        return isinstance(self, Just)
    
    def is_nothing(self) -> bool:
        """Check if this is Nothing."""
        return isinstance(self, Nothing)
    
    def __or__(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Override | operator for bind."""
        return self.bind(func)
    
    def __rshift__(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Override >> operator for chaining."""
        return self.bind(func)

@dataclass
class Just(Maybe[T]):
    """Represents a value that exists."""
    value: T
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Apply function to the value and return the result."""
        return func(self.value)
    
    def get_or_else(self, default: U) -> Union[T, U]:
        """Return the value since this is Just."""
        return self.value
    
    def __repr__(self) -> str:
        return f"Just({self.value})"

class Nothing(Maybe[Any]):
    """Represents the absence of a value."""
    
    def bind(self, func: Callable[[Any], Maybe[U]]) -> Maybe[U]:
        """Return Nothing, ignoring the function."""
        return self
    
    def get_or_else(self, default: U) -> U:
        """Return the default value since this is Nothing."""
        return default
    
    def __repr__(self) -> str:
        return "Nothing"

# Example usage
def safe_divide(x: float, y: float) -> Maybe[float]:
    """Safely divide two numbers, returning Nothing if division by zero."""
    if y == 0:
        return Nothing()
    return Just(x / y)

def safe_sqrt(x: float) -> Maybe[float]:
    """Safely compute square root, returning Nothing for negative numbers."""
    if x < 0:
        return Nothing()
    return Just(x ** 0.5)

def demonstrate() -> None:
    """Demonstrate the Maybe monad."""
    print("=== Maybe Monad ===\n")
    
    # Basic usage
    print("1. Basic usage:")
    result1 = Just(4).bind(lambda x: Just(x * 2))
    print(f"Just(4).bind(lambda x: Just(x * 2)) = {result1}")
    
    result2 = Nothing().bind(lambda x: Just(x * 2))
    print(f"Nothing().bind(lambda x: Just(x * 2)) = {result2}")
    
    # Using map
    print("\n2. Using map:")
    result3 = Just(3).map(lambda x: x * 2)
    print(f"Just(3).map(lambda x: x * 2) = {result3}")
    
    result4 = Nothing().map(lambda x: x * 2)
    print(f"Nothing().map(lambda x: x * 2) = {result4}")
    
    # Chaining operations
    print("\n3. Chaining operations:")
    # Using bind
    result5 = (
        Just(16)
        .bind(lambda x: safe_sqrt(x))
        .bind(lambda y: safe_divide(1, y))
    )
    print(f"sqrt(16) then 1/result = {result5}")
    
    # Using operator overloading
    result6 = Just(16) >> safe_sqrt >> (lambda y: safe_divide(1, y))
    print(f"Using >> operator: {result6}")
    
    # Division by zero
    print("\n4. Handling errors:")
    result7 = (
        Just(4)
        .bind(lambda x: safe_divide(x, 0))  # Division by zero
        .bind(lambda y: Just(y * 2))        # Skipped
    )
    print(f"4 / 0 * 2 = {result7} (handled safely)")
    
    # Complex computation with multiple steps
    print("\n5. Complex computation:")
    def complex_computation(x: float) -> Maybe[float]:
        return (
            Just(x)
            .bind(lambda a: safe_divide(a, 2))    # x / 2
            .bind(lambda b: safe_sqrt(b))          # sqrt(x/2)
            .bind(lambda c: safe_divide(1, c))     # 1 / sqrt(x/2)
        )
    
    print(f"Complex(8) = {complex_computation(8)}")
    print(f"Complex(-1) = {complex_computation(-1)} (handled)")
    
    # get_or_else
    print("\n6. Using get_or_else:")
    value1 = Just(42).get_or_else("default")
    value2 = Nothing().get_or_else("default")
    print(f"Just(42).get_or_else('default') = {value1}")
    print(f"Nothing().get_or_else('default') = {value2}")

if __name__ == "__main__":
    demonstrate()
