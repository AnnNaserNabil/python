"""
5. Composing Decorators

Demonstrates how to create and compose decorators using function composition,
and how to build decorators that can be composed in a flexible way.
"""
from __future__ import annotations
from typing import Callable, TypeVar, Any, cast, Type, Optional
from functools import wraps, partial, update_wrapper
import time
import logging
from datetime import datetime

T = TypeVar('T', bound=Callable[..., Any])

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Basic Decorator Composition
def log_call(logger: logging.Logger) -> Callable[[T], T]:
    """Decorator to log function calls."""
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned {result}")
            return result
        return cast(T, wrapper)
    return decorator

def time_execution(logger: logging.Logger) -> Callable[[T], T]:
    """Decorator to time function execution."""
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            logger.info(f"{func.__name__} executed in {elapsed:.6f} seconds")
            return result
        return cast(T, wrapper)
    return decorator

def validate_input(validator: Callable[..., bool]) -> Callable[[T], T]:
    """Decorator to validate function input."""
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not validator(*args, **kwargs):
                raise ValueError("Input validation failed")
            return func(*args, **kwargs)
        return cast(T, wrapper)
    return decorator

# 2. Composable Decorator Class
class Composable:
    """A decorator that can be composed with other decorators."""
    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func
        update_wrapper(self, func)
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)
    
    def __matmul__(self, other: Callable[..., Any]) -> 'Composable':
        ""
        Overload the @ operator for decorator composition.
        (f @ g)(x) = f(g(x))
        """
        @wraps(self.func)
        def composed(*args: Any, **kwargs: Any) -> Any:
            return self.func(other(*args, **kwargs))
        return Composable(composed)
    
    def __rrshift__(self, other: Callable[..., Any]) -> 'Composable':
        """
        Overload the >> operator for reverse composition.
        (f >> g)(x) = g(f(x))
        """
        @wraps(other)
        def composed(*args: Any, **kwargs: Any) -> Any:
            return self.func(other(*args, **kwargs))
        return Composable(composed)
    
    def __lshift__(self, other: Callable[..., Any]) -> 'Composable':
        """
        Overload the << operator for forward composition.
        (f << g)(x) = f(g(x))
        """
        @wraps(self.func)
        def composed(*args: Any, **kwargs: Any) -> Any:
            return self.func(other(*args, **kwargs))
        return Composable(composed)

# 3. Decorator Factories with Composition
def retry(max_attempts: int = 3, 
         exceptions: tuple[Type[Exception], ...] = (Exception,),
         delay: float = 1.0) -> Callable[[T], T]:
    """Decorator factory for retrying a function on failure."""
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        break
                    
                    logger.warning(
                        f"Attempt {attempt} failed: {e}. "
                        f"Retrying in {current_delay:.1f} seconds..."
                    )
                    time.sleep(current_delay)
                    current_delay *= 2  # Exponential backoff
            
            raise RuntimeError(
                f"Failed after {max_attempts} attempts"
            ) from last_exception
        return cast(T, wrapper)
    return decorator

def memoize(cache: Optional[dict] = None) -> Callable[[T], T]:
    """Decorator to memoize function results."""
    if cache is None:
        cache = {}
    
    def decorator(func: T) -> T:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, frozenset(kwargs.items()))
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return cast(T, wrapper)
    return decorator

# 4. Composable Decorator Pipeline
def compose_decorators(*decorators: Callable[[T], T]) -> Callable[[T], T]:
    """Compose multiple decorators into a single decorator."""
    def decorator(func: T) -> T:
        for d in reversed(decorators):
            func = d(func)
        return func
    return decorator

def demonstrate_decorator_composition() -> None:
    """Demonstrate various ways to compose decorators."""
    # Basic decorator application
    @log_call(logger)
    @time_execution(logger)
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        time.sleep(0.1)  # Simulate work
        return a + b
    
    print("=== Basic Decorator Composition ===")
    result = add(3, 5)
    print(f"Result: {result}")
    
    # Using compose_decorators
    @compose_decorators(
        log_call(logger),
        time_execution(logger),
        retry(max_attempts=3, exceptions=(ValueError,)),
    )
    def divide(a: float, b: float) -> float:
        """Divide two numbers with retry on division by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    print("\n=== Composed Decorators ===")
    try:
        result = divide(10, 2)
        print(f"10 / 2 = {result}")
        
        # This will trigger retries
        result = divide(10, 0)
        print(f"10 / 0 = {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Using the Composable class
    @Composable
    def double(x: int) -> int:
        return x * 2
    
    @Composable
    def increment(x: int) -> int:
        return x + 1
    
    # Compose using @ operator (right to left)
    double_then_increment = increment @ double
    print(f"\n=== Composable Decorators ===")
    print(f"(increment @ double)(5) = {double_then_increment(5)}")
    
    # Compose using >> operator (left to right)
    increment_then_double = increment >> double
    print(f"(increment >> double)(5) = {increment_then_double(5)}")
    
    # More complex composition
    square = Composable(lambda x: x * x)
    pipeline = square @ increment @ double
    print(f"(square @ increment @ double)(3) = {pipeline(3)}")

def demonstrate_real_world_example() -> None:
    """Demonstrate a real-world example of decorator composition."""
    # Cache for memoization
    cache: dict = {}
    
    # Define validators
    def is_positive(x: int) -> bool:
        return x > 0
    
    # Create decorators
    validate = validate_input(lambda x: is_positive(x))
    
    # Apply multiple decorators
    @compose_decorators(
        log_call(logger),
        time_execution(logger),
        memoize(cache),
        validate,
        retry(max_attempts=3, exceptions=(ValueError,))
    )
    def fibonacci(n: int) -> int:
        """Calculate the nth Fibonacci number."""
        if n <= 0:
            raise ValueError("n must be positive")
        if n in (1, 2):
            return 1
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    print("\n=== Real-World Example: Memoized Fibonacci ===")
    
    # First call (computes and caches)
    print("fibonacci(10) =", fibonacci(10))
    
    # Second call (uses cache)
    print("fibonacci(10) =", fibonacci(10))
    
    # This will trigger validation and retry
    try:
        print("fibonacci(-5) =", fibonacci(-5))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Composing Decorators ===")
    demonstrate_decorator_composition()
    demonstrate_real_world_example()
    
    print("\n=== Key Takeaways ===")
    print("1. Decorators can be composed to combine multiple behaviors")
    print("2. The order of decorators matters - they're applied from bottom to top")
    print("3. Composable decorators enable reusable and modular code")
    print("4. Decorator factories allow for parameterized decorators")
    print("5. The @functools.wraps decorator preserves function metadata")
