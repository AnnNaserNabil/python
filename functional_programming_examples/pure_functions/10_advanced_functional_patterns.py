"""
10. Advanced Functional Patterns

Advanced functional programming patterns using pure functions.
- Monads (Maybe, Either)
- Function currying
- Immutable data structures with structural sharing
- Lenses for immutable updates
"""
from typing import TypeVar, Generic, Callable, Any, Optional, Union, Tuple, List
from dataclasses import dataclass
from functools import partial

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')

# 1. Maybe Monad (Option type)
class Maybe(Generic[T]):
    """Represents an optional value: Just(value) or Nothing."""
    
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

class Nothing(Maybe[Any]):
    """Represents the absence of a value."""
    
    def bind(self, func: Callable[[Any], Maybe[Any]]) -> 'Nothing':
        return self
    
    def get_or_else(self, default: T) -> T:
        return default
    
    def __str__(self) -> str:
        return "Nothing"

# 2. Either Monad for error handling
class Either(Generic[E, T]):
    """Represents a value that can be either a success (Right) or failure (Left)."""
    
    def bind(self, func: Callable[[T], 'Either[E, U]']) -> 'Either[E, U]':
        raise NotImplementedError
    
    def map(self, func: Callable[[T], U]) -> 'Either[E, U]':
        return self.bind(lambda x: Right(func(x)))
    
    def map_error(self, func: Callable[[E], E]) -> 'Either[E, T]':
        raise NotImplementedError
    
    def get_or_else(self, default: T) -> T:
        raise NotImplementedError

class Left(Either[E, Any]):
    """Represents a failure with an error value."""
    
    def __init__(self, error: E):
        self.error = error
    
    def bind(self, func: Callable[[Any], Either[E, U]]) -> 'Left[E, Any]':
        return self
    
    def map_error(self, func: Callable[[E], E]) -> 'Left[E, Any]':
        return Left(func(self.error))
    
    def get_or_else(self, default: T) -> T:
        return default
    
    def __str__(self) -> str:
        return f"Left({self.error})"

class Right(Either[Any, T]):
    """Represents a successful value."""
    
    def __init__(self, value: T):
        self.value = value
    
    def bind(self, func: Callable[[T], Either[E, U]]) -> Either[E, U]:
        return func(self.value)
    
    def map_error(self, func: Callable[[Any], E]) -> 'Right[E, T]':
        return self
    
    def get_or_else(self, default: T) -> T:
        return self.value
    
    def __str__(self) -> str:
        return f"Right({self.value})"

# 3. Function currying
def curry(func: Callable[..., T], arity: Optional[int] = None) -> Callable:
    """
    Convert a function to a curried function.
    
    Args:
        func: Function to curry
        arity: Number of arguments the function expects (None to auto-detect)
        
    Returns:
        Curried version of the function
    """
    if arity is None:
        arity = func.__code__.co_argcount
    
    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        return lambda *more: curried(*(args + more))
    
    return curried

# 4. Immutable data structure with structural sharing
@dataclass(frozen=True)
class ImList(Generic[T]):
    """Immutable list with structural sharing."""
    _items: Tuple[T, ...] = ()
    
    def cons(self, item: T) -> 'ImList[T]':
        """Add an item to the front of the list."""
        return ImList((item,) + self._items)
    
    def head(self) -> T:
        """Get the first item in the list."""
        if not self._items:
            raise IndexError("head of empty list")
        return self._items[0]
    
    def tail(self) -> 'ImList[T]':
        """Get the list without the first item."""
        if not self._items:
            raise IndexError("tail of empty list")
        return ImList(self._items[1:])
    
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return len(self._items) == 0
    
    def __iter__(self):
        return iter(self._items)
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __str__(self) -> str:
        return f"ImList({list(self._items)})"

# 5. Lenses for immutable updates
def lens(getter: Callable[[T], U], setter: Callable[[T, U], T]) -> Callable:
    """
    Create a lens for getting and setting values in nested data structures.
    
    Args:
        getter: Function to get a value from a structure
        setter: Function to set a value in a structure
        
    Returns:
        A lens function that can get, set, and update values
    """
    def _lens(func: Callable[[U], U]) -> Callable[[T], T]:
        def wrapper(structure: T) -> T:
            return setter(structure, func(getter(structure)))
        return wrapper
    return _lens

# Example usage
if __name__ == "__main__":
    print("=== Maybe Monad ===")
    def safe_divide(x: float, y: float) -> Maybe[float]:
        return Just(x / y) if y != 0 else Nothing()
    
    result = (
        safe_divide(10, 2)  # Just(5.0)
        .bind(lambda x: Just(x + 3))  # Just(8.0)
        .bind(lambda x: safe_divide(x, 2))  # Just(4.0)
    )
    print(f"Result: {result}")
    
    # Division by zero
    result = safe_divide(10, 0)  # Nothing
    print(f"Division by zero: {result}")
    
    print("\n=== Either Monad ===")
    def safe_divide_either(x: float, y: float) -> Either[str, float]:
        if y == 0:
            return Left("Division by zero")
        return Right(x / y)
    
    result = (
        safe_divide_either(10, 2)  # Right(5.0)
        .map(lambda x: x + 3)      # Right(8.0)
        .bind(lambda x: safe_divide_either(x, 2))  # Right(4.0)
    )
    print(f"Result: {result}")
    
    # Division by zero with Either
    result = safe_divide_either(10, 0)  # Left("Division by zero")
    print(f"Error case: {result}")
    
    print("\n=== Function Currying ===")
    @curry
    def add_three(a: int, b: int, c: int) -> int:
        return a + b + c
    
    add_five = add_three(2)(3)  # Partially applied
    print(f"add_five(10) = {add_five(10)}")  # 15
    
    print("\n=== Immutable List ===")
    lst = ImList[int]().cons(3).cons(2).cons(1)
    print(f"List: {lst}")
    print(f"Head: {lst.head()}")
    print(f"Tail: {lst.tail()}")
    
    print("\n=== Lenses ===")
    @dataclass(frozen=True)
    class Person:
        name: str
        age: int
    
    name_lens = lens(
        lambda p: p.name,
        lambda p, name: Person(name, p.age)
    )
    
    age_lens = lens(
        lambda p: p.age,
        lambda p, age: Person(p.name, age)
    )
    
    alice = Person("Alice", 30)
    
    # Get name
    get_name = name_lens(lambda x: x)
    print(f"Name: {get_name(alice)}")
    
    # Set name
    set_name = name_lens(lambda _: "Alice Smith")
    alice_updated = set_name(alice)
    print(f"Updated: {alice_updated}")
    
    # Increment age
    increment_age = age_lens(lambda age: age + 1)
    alice_older = increment_age(alice)
    print(f"Older: {alice_older}")
    
    # Original is unchanged (immutable)
    print(f"Original: {alice}")
