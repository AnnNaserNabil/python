"""
10. Monads and Functional Error Handling

This module demonstrates how to use monads for functional error handling in Python.
We'll implement Maybe and Either monads, which are common in functional programming.
"""

from typing import TypeVar, Generic, Callable, Any, Optional, Union
from functools import wraps

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')

# ============================================
# 1. Maybe Monad (Option type)
# Represents an optional value: Some(value) or Nothing
# ============================================
class Maybe(Generic[T]):
    """Base class for Maybe monad."""
    
    def bind(self, func: Callable[[T], 'Maybe[U]']) -> 'Maybe[U]':
        raise NotImplementedError
    
    def map(self, func: Callable[[T], U]) -> 'Maybe[U]':
        return self.bind(lambda x: Just(func(x)))
    
    def get_or_else(self, default: T) -> T:
        raise NotImplementedError
    
    def is_just(self) -> bool:
        return isinstance(self, Just)
    
    def is_nothing(self) -> bool:
        return isinstance(self, Nothing)
    
    def __or__(self, func):
        """Override | operator for chaining operations."""
        return self.bind(func)
    
    @staticmethod
    def from_value(value: Optional[T]) -> 'Maybe[T]':
        """Convert a value that might be None to a Maybe."""
        return Just(value) if value is not None else Nothing()

class Just(Maybe[T]):
    """Represents a value that exists."""
    
    def __init__(self, value: T):
        self.value = value
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return func(self.value)
    
    def get_or_else(self, default: T) -> T:
        return self.value
    
    def __str__(self) -> str:
        return f"Just({self.value})"
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Just) and self.value == other.value

class Nothing(Maybe[Any]):
    """Represents the absence of a value."""
    
    def bind(self, func: Callable[[Any], Maybe[Any]]) -> 'Nothing':
        return self
    
    def get_or_else(self, default: T) -> T:
        return default
    
    def __str__(self) -> str:
        return "Nothing"
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Nothing)

# ============================================
# 2. Either Monad
# Represents a value that can be one of two types: Left(error) or Right(value)
# ============================================
class Either(Generic[E, T]):
    """Base class for Either monad."""
    
    def bind(self, func: Callable[[T], 'Either[E, U]']) -> 'Either[E, U]':
        raise NotImplementedError
    
    def map(self, func: Callable[[T], U]) -> 'Either[E, U]':
        return self.bind(lambda x: Right(func(x)))
    
    def map_error(self, func: Callable[[E], E]) -> 'Either[E, T]':
        raise NotImplementedError
    
    def is_right(self) -> bool:
        return isinstance(self, Right)
    
    def is_left(self) -> bool:
        return isinstance(self, Left)
    
    def get_or_else(self, default: T) -> T:
        raise NotImplementedError
    
    def get_or_raise(self) -> T:
        raise NotImplementedError
    
    @staticmethod
    def from_value(value: Union[E, T], is_error: bool = False) -> 'Either[E, T]':
        """Convert a value to Either."""
        return Left(value) if is_error else Right(value)
    
    @staticmethod
    def try_except(func: Callable[[], T]) -> 'Either[Exception, T]':
        """Execute a function that might raise an exception and return an Either."""
        try:
            return Right(func())
        except Exception as e:
            return Left(e)

class Right(Either[Any, T]):
    """Represents the successful case (contains a value)."""
    
    def __init__(self, value: T):
        self.value = value
    
    def bind(self, func: Callable[[T], Either[E, U]]) -> Either[E, U]:
        return func(self.value)
    
    def map_error(self, func: Callable[[Any], E]) -> 'Right[E, T]':
        return self
    
    def get_or_else(self, default: T) -> T:
        return self.value
    
    def get_or_raise(self) -> T:
        return self.value
    
    def __str__(self) -> str:
        return f"Right({self.value})"
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Right) and self.value == other.value

class Left(Either[E, Any]):
    """Represents the error case (contains an error)."""
    
    def __init__(self, error: E):
        self.error = error
    
    def bind(self, func: Callable[[Any], Either[E, U]]) -> 'Left[E, Any]':
        return self
    
    def map_error(self, func: Callable[[E], E]) -> 'Left[E, Any]':
        return Left(func(self.error))
    
    def get_or_else(self, default: T) -> T:
        return default
    
    def get_or_raise(self) -> T:
        if isinstance(self.error, Exception):
            raise self.error
        raise ValueError(f"Error: {self.error}")
    
    def __str__(self) -> str:
        return f"Left({self.error})"
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Left) and self.error == other.error

# ============================================
# 3. Decorators for working with monads
# ============================================
def maybe_returns(func):
    """Decorator to convert return value to Maybe."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return Just(result) if result is not None else Nothing()
    return wrapper

def either_returns(error_type=Exception):
    """Decorator to convert return value to Either."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return Right(result)
            except error_type as e:
                return Left(e)
        return wrapper
    return decorator

# ============================================
# 4. Example usage
# ============================================
if __name__ == "__main__":
    print("=== Maybe Monad Examples ===")
    
    # Safe division that returns Maybe
    def safe_divide(x: float, y: float) -> Maybe[float]:
        return Just(x / y) if y != 0 else Nothing()
    
    # Chaining operations with Maybe
    result = (
        safe_divide(10, 2)  # Just(5.0)
        .bind(lambda x: Just(x + 3))  # Just(8.0)
        .bind(lambda x: safe_divide(x, 2))  # Just(4.0)
    )
    print(f"Result of safe operations: {result}")
    
    # Division by zero
    result = (
        safe_divide(10, 0)  # Nothing
        .bind(lambda x: Just(x + 3))  # Still Nothing
        .bind(lambda x: safe_divide(x, 2))  # Still Nothing
    )
    print(f"Result with division by zero: {result}")
    print(f"Default value: {result.get_or_else('Error')}")
    
    # Using the decorator
    @maybe_returns
    def find_user(user_id: int) -> Optional[dict]:
        users = {1: {"id": 1, "name": "Alice"}, 2: {"id": 2, "name": "Bob"}}
        return users.get(user_id)
    
    user = find_user(1).map(lambda u: u["name"]).get_or_else("Unknown")
    print(f"User 1: {user}")
    
    user = find_user(99).map(lambda u: u["name"]).get_or_else("Unknown")
    print(f"User 99: {user}")
    
    print("\n=== Either Monad Examples ===")
    
    # Safe division that returns Either
    def safe_divide_either(x: float, y: float) -> Either[str, float]:
        if y == 0:
            return Left("Division by zero")
        return Right(x / y)
    
    # Chaining operations with Either
    result = (
        safe_divide_either(10, 2)  # Right(5.0)
        .map(lambda x: x + 3)      # Right(8.0)
        .bind(lambda x: safe_divide_either(x, 2))  # Right(4.0)
    )
    print(f"Result of safe operations: {result}")
    
    # Division by zero with Either
    result = (
        safe_divide_either(10, 0)  # Left("Division by zero")
        .map(lambda x: x + 3)      # Still Left
        .bind(lambda x: safe_divide_either(x, 2))  # Still Left
    )
    print(f"Result with division by zero: {result}")
    print(f"Default value: {result.get_or_else('Error')}")
    
    # Using the decorator with Either
    @either_returns(KeyError)
    def get_user_email(user_id: int) -> str:
        users = {
            1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
            2: {"id": 2, "name": "Bob"}  # Missing email
        }
        return users[user_id]["email"]
    
    # Process user email
    def process_user_email(user_id: int) -> Either[str, str]:
        return (
            Either.try_except(lambda: get_user_email(user_id))
            .map_error(lambda e: f"User {user_id} not found" if isinstance(e, KeyError) else str(e))
            .map(lambda email: f"Sending email to {email}")
        )
    
    print("\nProcessing user emails:")
    print(f"User 1: {process_user_email(1).get_or_else('Error')}")
    print(f"User 2: {process_user_email(2).get_or_else('Error')}")
    print(f"User 99: {process_user_email(99).get_or_else('Error')}")
    
    # Using Either for validation
    def validate_age(age: int) -> Either[str, int]:
        if age < 0:
            return Left("Age cannot be negative")
        if age > 120:
            return Left("Age seems unrealistic")
        return Right(age)
    
    def create_user(name: str, age: int) -> Either[str, dict]:
        if not name.strip():
            return Left("Name cannot be empty")
        return validate_age(age).map(lambda a: {"name": name, "age": a})
    
    print("\nUser validation:")
    print(f"Create Alice: {create_user('Alice', 30)}")
    print(f"Create empty name: {create_user('', 30)}")
    print(f"Create invalid age: {create_user('Bob', 150)}")
