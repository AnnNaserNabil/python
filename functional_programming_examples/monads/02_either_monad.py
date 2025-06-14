"""
2. The Either Monad

This module implements the Either monad, which represents a value that can be
one of two possible types (typically used for error handling where the value is
either a successful result or an error).
"""
from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, Union, Type, cast
from dataclasses import dataclass

L = TypeVar('L')  # Left type (typically used for errors)
R = TypeVar('R')  # Right type (typically used for success values)
T = TypeVar('T')
U = TypeVar('U')

class Either(Generic[L, R]):
    """Base class for the Either monad."""
    
    @classmethod
    def right(cls, value: R) -> Either[Any, R]:
        """Create a Right value."""
        return Right(value)
    
    @classmethod
    def left(cls, value: L) -> Either[L, Any]:
        """Create a Left value."""
        return Left(value)
    
    def bind(self, func: Callable[[R], Either[L, U]]) -> Either[L, U]:
        """Bind operation for the Either monad."""
        raise NotImplementedError
    
    def map(self, func: Callable[[R], U]) -> Either[L, U]:
        """Map a function over the Right value."""
        return self.bind(lambda x: Either.right(func(x)))
    
    def map_left(self, func: Callable[[L], T]) -> Either[T, R]:
        """Map a function over the Left value."""
        raise NotImplementedError
    
    def get_or_else(self, default: U) -> Union[R, U]:
        """Get the Right value or return a default."""
        raise NotImplementedError
    
    def is_right(self) -> bool:
        """Check if this is a Right value."""
        return isinstance(self, Right)
    
    def is_left(self) -> bool:
        """Check if this is a Left value."""
        return isinstance(self, Left)
    
    def __or__(self, func: Callable[[R], Either[L, U]]) -> Either[L, U]:
        """Override | operator for bind."""
        return self.bind(func)
    
    def __rshift__(self, func: Callable[[R], Either[L, U]]) -> Either[L, U]:
        """Override >> operator for chaining."""
        return self.bind(func)
    
    @staticmethod
    def sequence(iterable: list[Either[L, R]]) -> Either[L, list[R]]:
        """Convert a list of Eithers to an Either of a list."""
        result = []
        for item in iterable:
            if item.is_left():
                return cast(Left[L, list[R]], item)
            result.append(cast(Right[L, R], item).value)
        return Either.right(result)

@dataclass
class Right(Either[Any, R]):
    """Represents the successful case (right side)."""
    value: R
    
    def bind(self, func: Callable[[R], Either[L, U]]) -> Either[L, U]:
        """Apply function to the Right value."""
        return func(self.value)
    
    def map_left(self, func: Callable[[Any], T]) -> Either[T, R]:
        """Map over Left does nothing for Right."""
        return cast(Either[T, R], self)
    
    def get_or_else(self, default: U) -> Union[R, U]:
        """Return the Right value."""
        return self.value
    
    def __repr__(self) -> str:
        return f"Right({self.value})"

@dataclass
class Left(Either[L, Any]):
    """Represents the error case (left side)."""
    value: L
    
    def bind(self, func: Callable[[Any], Either[L, U]]) -> Either[L, U]:
        """Return self, ignoring the function."""
        return cast(Either[L, U], self)
    
    def map(self, func: Callable[[Any], U]) -> Either[L, U]:
        """Map over Right does nothing for Left."""
        return cast(Either[L, U], self)
    
    def map_left(self, func: Callable[[L], T]) -> Either[T, Any]:
        """Apply function to the Left value."""
        return Left(func(self.value))
    
    def get_or_else(self, default: U) -> U:
        """Return the default value."""
        return default
    
    def __repr__(self) -> str:
        return f"Left({self.value})"

# Example usage
def parse_int(s: str) -> Either[str, int]:
    """Parse a string to an integer, returning Left on failure."""
    try:
        return Right(int(s))
    except ValueError as e:
        return Left(f"Could not parse '{s}' as integer: {e}")

def safe_divide(x: float, y: float) -> Either[str, float]:
    """Safely divide two numbers, returning Left on division by zero."""
    if y == 0:
        return Left("Division by zero")
    return Right(x / y)

def demonstrate() -> None:
    """Demonstrate the Either monad."""
    print("=== Either Monad ===\n")
    
    # Basic usage
    print("1. Basic usage:")
    result1 = Right(4).bind(lambda x: Right(x * 2))
    print(f"Right(4).bind(lambda x: Right(x * 2)) = {result1}")
    
    result2 = Left("error").bind(lambda x: Right(x * 2))
    print(f"Left('error').bind(lambda x: Right(x * 2)) = {result2}")
    
    # Using map
    print("\n2. Using map:")
    result3 = Right(3).map(lambda x: x * 2)
    print(f"Right(3).map(lambda x: x * 2) = {result3}")
    
    result4 = Left("error").map(lambda x: x * 2)
    print(f"Left('error').map(lambda x: x * 2) = {result4}")
    
    # Chaining operations
    print("\n3. Chaining operations:")
    # Using bind
    result5 = (
        parse_int("4")
        .bind(lambda x: safe_divide(10, x))
        .bind(lambda y: Right(y * 2))
    )
    print(f"10 / parse('4') * 2 = {result5}")
    
    # Using operator overloading
    result6 = parse_int("4") >> (lambda x: safe_divide(10, x)) >> (lambda y: Right(y * 2))
    print(f"Using >> operator: {result6}")
    
    # Error handling
    print("\n4. Error handling:")
    result7 = (
        parse_int("abc")  # This will fail
        .bind(lambda x: safe_divide(10, x))
        .bind(lambda y: Right(y * 2))
    )
    print(f"Error case: {result7}")
    
    # get_or_else
    print("\n5. Using get_or_else:")
    value1 = Right(42).get_or_else("default")
    value2 = Left("error").get_or_else("default")
    print(f"Right(42).get_or_else('default') = {value1}")
    print(f"Left('error').get_or_else('default') = {value2}")
    
    # sequence
    print("\n6. Using sequence:")
    numbers = ["1", "2", "3"]
    parsed = [parse_int(n) for n in numbers]
    result8 = Either.sequence(parsed)
    print(f"Sequence of valid numbers: {result8}")
    
    invalid = ["1", "two", "3"]
    parsed_invalid = [parse_int(n) for n in invalid]
    result9 = Either.sequence(parsed_invalid)
    print(f"Sequence with invalid number: {result9}")
    
    # Complex computation with error handling
    print("\n7. Complex computation with error handling:")
    def process_numbers(a: str, b: str, c: str) -> Either[str, float]:
        """Process three numbers with error handling."""
        return (
            parse_int(a)
            .bind(lambda x: parse_int(b).bind(
                lambda y: parse_int(c).bind(
                    lambda z: safe_divide(x + y, z)
                )
            ))
        )
    
    print(f"(1 + 2) / 3 = {process_numbers('1', '2', '3')}")
    print(f"(1 + x) / 3 = {process_numbers('1', 'x', '3')}")
    print(f"(1 + 2) / 0 = {process_numbers('1', '2', '0')}")

if __name__ == "__main__":
    demonstrate()
