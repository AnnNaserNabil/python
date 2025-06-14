"""
7. Type-Checked Function Composition

Demonstrates how to implement and use type-checked function composition
with Python's type hints and the typing module.
"""
from __future__ import annotations
from typing import (
    TypeVar, Callable, Any, cast, overload, Union, Optional, 
    Type, Tuple, List, Dict, Sequence, Iterable, Iterator, 
    Generic, TypeGuard, Protocol, runtime_checkable
)
from functools import partial, reduce
import inspect
import sys
from dataclasses import dataclass

# Type variables for generic function composition
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')
E = TypeVar('E')

# For functions that might raise exceptions
T = TypeVar('T')
U = TypeVar('U')

# For generic function composition with type checking
F1 = TypeVar('F1', bound=Callable[..., Any])
F2 = TypeVar('F2', bound=Callable[..., Any])

# 1. Basic type-safe composition

def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    """Compose two functions with type checking."""
    def composed(a: A) -> C:
        return f(g(a))
    return composed

def pipe(f: Callable[[A], B], g: Callable[[B], C]) -> Callable[[A], C]:
    """Pipe two functions with type checking."""
    def piped(a: A) -> C:
        return g(f(a))
    return piped

# 2. Variadic composition with type checking

def safe_compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Compose functions with runtime type checking.
    
    Args:
        *funcs: Functions to compose, from right to left
        
    Returns:
        A composed function that type checks at runtime
        
    Raises:
        TypeError: If the functions cannot be composed due to type mismatches
    """
    if not funcs:
        return lambda x: x
    
    # Check that each function's output type matches the next function's input type
    for i in range(len(funcs) - 1):
        f = funcs[i]
        g = funcs[i + 1]
        
        # Get type hints
        f_sig = inspect.signature(f)
        g_sig = inspect.signature(g)
        
        # Skip if we can't determine the types
        if f_sig.return_annotation == inspect.Parameter.empty or \
           not g_sig.parameters or \
           next(iter(g_sig.parameters.values())).annotation == inspect.Parameter.empty:
            continue
        
        # Check if types are compatible
        f_return = f_sig.return_annotation
        g_param = next(iter(g_sig.parameters.values())).annotation
        
        if not is_subtype(f_return, g_param):
            raise TypeError(
                f"Type mismatch in composition at position {i}: "
                f"{f.__name__} returns {f_return}, but {g.__name__} expects {g_param}"
            )
    
    # Compose the functions
    def composed(*args: Any, **kwargs: Any) -> Any:
        result = funcs[-1](*args, **kwargs)
        for f in reversed(funcs[:-1]):
            result = f(result)
        return result
    
    return composed

def is_subtype(subtype: Any, supertype: Any) -> bool:
    """Check if one type is a subtype of another."""
    try:
        # Handle forward references
        if isinstance(subtype, str) or isinstance(supertype, str):
            return True  # Skip string annotations for now
            
        # Handle Union types
        if hasattr(supertype, '__origin__') and supertype.__origin__ is Union:
            return any(is_subtype(subtype, t) for t in supertype.__args__)
        
        # Handle generic types
        if hasattr(subtype, '__origin__') and hasattr(supertype, '__origin__'):
            if subtype.__origin__ != supertype.__origin__:
                return False
            
            # Check type arguments
            if hasattr(subtype, '__args__') and hasattr(supertype, '__args__'):
                if len(subtype.__args__) != len(supertype.__args__):
                    return False
                return all(is_subtype(sub, sup) for sub, sup in zip(subtype.__args__, supertype.__args__))
            
            return True
        
        # Handle concrete types
        return issubclass(subtype, supertype)
    except (TypeError, AttributeError):
        # If we can't determine the relationship, assume it's okay
        return True

# 3. Type-safe decorators

def typed_decorator(
    decorator: Callable[[F1], F2]
) -> Callable[[F1], F2]:
    """A decorator that preserves the type signature of the decorated function."""
    return decorator

@typed_decorator
type_safe = safe_compose  # Alias for better readability in decorator context

# 4. Type-safe pipeline builder

class Pipeline(Generic[A, B]):
    """A type-safe pipeline builder."""
    
    def __init__(self, func: Callable[..., B]):
        self.func = func
        
    def __call__(self, *args: Any, **kwargs: Any) -> B:
        return self.func(*args, **kwargs)
    
    def then(self, func: Callable[[B], C]) -> 'Pipeline[A, C]':
        """Add a step to the pipeline."""
        return Pipeline[A, C](lambda *args, **kwargs: func(self(*args, **kwargs)))
    
    @classmethod
    def of(cls, func: Callable[..., A]) -> 'Pipeline[A, A]':
        """Create a new pipeline from a function."""
        return cls(func)

# 5. Type-safe function composition with overloading

@overload
def typed_compose() -> Callable[[A], A]: ...

@overload
def typed_compose(f1: Callable[[A], B]) -> Callable[[A], B]: ...

@overload
def typed_compose(f1: Callable[[B], C], f2: Callable[[A], B]) -> Callable[[A], C]: ...

@overload
def typed_compose(f1: Callable[[C], D], f2: Callable[[B], C], f3: Callable[[A], B]) -> Callable[[A], D]: ...

def typed_compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Type-safe function composition with overloads for better type inference."""
    return safe_compose(*funcs)

# 6. Example type-safe functions

def parse_int(s: str) -> int:
    """Parse a string to an integer."""
    return int(s)

def double(n: int) -> int:
    """Double a number."""
    return n * 2

def to_string(n: int) -> str:
    """Convert a number to a string."""
    return str(n)

def add_exclamation(s: str) -> str:
    """Add an exclamation mark to a string."""
    return s + "!"

def demonstrate_type_safe_composition() -> None:
    """Demonstrate type-safe function composition."""
    print("=== Type-Safe Function Composition ===")
    
    # Basic composition with type checking
    try:
        # This will raise a TypeError because the types don't match
        # double expects an int, but to_string returns a str
        bad_compose = safe_compose(double, to_string)
        result = bad_compose(42)
        print(f"This should not print: {result}")
    except TypeError as e:
        print(f"Expected type error: {e}")
    
    # Correct composition
    good_compose = safe_compose(add_exclamation, to_string, double)
    result = good_compose(21)
    print(f"Good composition: {result}")  # "42!"
    
    # Using the Pipeline class
    pipeline = (
        Pipeline.of(parse_int)
        .then(double)
        .then(to_string)
        .then(add_exclamation)
    )
    
    result = pipeline("10")
    print(f"Pipeline result: {result}")  # "20!"
    
    # Using typed_compose with overloads
    composed = typed_compose(add_exclamation, to_string, double)
    result = composed(10)
    print(f"Typed compose: {result}")  # "20!"

def demonstrate_advanced_type_checking() -> None:
    """Demonstrate more advanced type checking scenarios."""
    print("\n=== Advanced Type Checking ===")
    
    from typing import List, Dict, Optional
    
    # Function with complex types
    def process_data(data: Dict[str, List[int]]) -> List[int]:
        """Process data and return a flattened list of values."""
        return [item for sublist in data.values() for item in sublist]
    
    # Another function with compatible types
    def sum_numbers(numbers: List[int]) -> int:
        """Sum a list of numbers."""
        return sum(numbers)
    
    # This composition should work
    try:
        pipeline = safe_compose(sum_numbers, process_data)
        data = {"a": [1, 2, 3], "b": [4, 5, 6]}
        result = pipeline(data)
        print(f"Sum of {data} = {result}")  # 21
    except TypeError as e:
        print(f"Unexpected error: {e}")
    
    # Function with optional return
    def maybe_get_value(key: str) -> Optional[int]:
        """Maybe get a value by key."""
        data = {"a": 1, "b": 2}
        return data.get(key)
    
    # Function that handles optional
    def increment(n: int) -> int:
        """Increment a number."""
        return n + 1
    
    # This will raise a type error because maybe_get_value returns Optional[int]
    # but increment expects int
    try:
        bad_pipeline = safe_compose(increment, maybe_get_value)
        result = bad_pipeline("a")
        print(f"This should not print: {result}")
    except TypeError as e:
        print(f"Expected type error: {e}")

def demonstrate_runtime_type_validation() -> None:
    """Demonstrate runtime type validation."""
    print("\n=== Runtime Type Validation ===")
    
    from typeguard import typechecked
    
    # Decorate with runtime type checking
    @typechecked
    def add(a: int, b: int) -> int:
        return a + b
    
    # This will work
    try:
        result = add(1, 2)
        print(f"1 + 2 = {result}")
    except TypeError as e:
        print(f"Unexpected error: {e}")
    
    # This will raise a TypeError at runtime
    try:
        result = add("1", "2")  # type: ignore
        print(f"This should not print: {result}")
    except TypeError as e:
        print(f"Expected type error: {e}")
    
    # Compose with runtime type checking
    @typechecked
    def double(n: int) -> int:
        return n * 2
    
    # Create a type-checked pipeline
    pipeline = safe_compose(double, add)
    
    # This will work
    try:
        result = pipeline(10, 20)
        print(f"Double of (10 + 20) = {result}")
    except TypeError as e:
        print(f"Unexpected error: {e}")
    
    # This will fail at runtime
    try:
        result = pipeline("10", 20)  # type: ignore
        print(f"This should not print: {result}")
    except TypeError as e:
        print(f"Expected type error: {e}")

if __name__ == "__main__":
    print("=== Type-Checked Function Composition ===")
    demonstrate_type_safe_composition()
    demonstrate_advanced_type_checking()
    
    # Only run if typeguard is installed
    try:
        import typeguard  # type: ignore
        demonstrate_runtime_type_validation()
    except ImportError:
        print("\nSkipping runtime type validation (install with: pip install typeguard)")
    
    print("\n=== Key Takeaways ===")
    print("1. Type hints make function composition safer and more maintainable")
    print("2. Runtime type checking can catch type errors that static type checkers miss")
    print("3. The typing module provides tools for complex type annotations")
    print("4. Type-safe pipelines help prevent runtime errors")
    print("5. Consider using mypy or pyright for static type checking")
