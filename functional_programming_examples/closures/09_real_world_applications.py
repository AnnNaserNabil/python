"""
9. Real-World Applications of Closures in Python

This module demonstrates practical, real-world applications of closures in Python,
showing how they can solve common programming challenges in an elegant way.

Key Patterns Demonstrated:
-------------------------
1. Configuration Management: Manage application settings with controlled access
2. Logging Decorators: Add logging behavior to functions non-invasively
3. Rate Limiting: Control how often a function can be called
4. Caching: Store and retrieve computed results efficiently
5. Middleware: Create flexible processing pipelines
6. Retry Mechanisms: Automatically retry failed operations

Why Use Closures in These Scenarios?
---------------------------------
- Encapsulation: Keep implementation details private
- State Management: Maintain state between function calls
- Code Reusability: Write generic solutions that can be applied to many functions
- Readability: Keep related functionality together
- Flexibility: Customize behavior at runtime

Real-world Use Cases:
-------------------
- Web frameworks (Django, Flask middleware)
- API rate limiting
- Configuration management systems
- Caching layers
- Logging and monitoring systems
- Error handling and recovery systems

Example:
-------
>>> # Using the configuration manager
>>> set_config, get_config, get_all = create_config_manager({"theme": "light"})
>>> set_config("theme", "dark")
>>> get_config("theme")
'dark'

>>> # Using the rate limiter
>>> @rate_limiter(max_calls=3, period=10.0)
... def fetch_data():
...     return "Data from expensive operation"
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, TypeVar, Protocol
from dataclasses import dataclass
from datetime import datetime
import time
import json
import logging
from functools import wraps

T = TypeVar('T')

# 1. Configuration Management
def create_config_manager(initial_config: Dict[str, Any]) -> tuple[Callable[[str, Any], None], Callable[[str, Any], Any], Callable[[], Dict[str, Any]]]:
    """
    Create a configuration manager with getter and setter functions.
    
    This function demonstrates how closures can be used to create a simple
    configuration system where the configuration data is private and can only
    be accessed or modified through the returned functions.
    
    Args:
        initial_config: A dictionary containing the initial configuration values
        
    Returns:
        A tuple containing three functions:
        - set_config(key, value): Set a configuration value
        - get_config(key, default=None): Get a configuration value
        - get_all(): Get a copy of all configuration values
        
    Example:
        >>> set_config, get_config, get_all = create_config_manager({"theme": "light"})
        >>> set_config("theme", "dark")
        >>> get_config("theme")
        'dark'
        >>> get_all()
        {'theme': 'dark'}
        
    Note:
        The configuration is stored in the closure's scope, making it private
        and only accessible through the returned functions.
    """
    config = initial_config.copy()
    
    def set_config(key: str, value: Any) -> None:
        """Set a configuration value."""
        nonlocal config
        config[key] = value
    
    def get_config(key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return config.get(key, default)
    
    def get_all() -> Dict[str, Any]:
        """Get all configuration values."""
        return config.copy()
    
    return set_config, get_config, get_all

# 2. Logging Decorator with Context
def log_execution(logger_name: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Create a decorator that logs function execution details.
    
    This decorator logs when a function starts and finishes executing,
    along with its execution time and return value or any exceptions.
    
    Args:
        logger_name: Name of the logger to use for logging messages
        
    Returns:
        A decorator function that can be applied to other functions
        
    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> 
        >>> @log_execution('app')
        ... def process_data(data):
        ...     return [x * 2 for x in data]
        >>> 
        >>> process_data([1, 2, 3])
        INFO:app:Executing process_data with args: ([1, 2, 3],), kwargs: {}
        INFO:app:process_data returned: [2, 4, 6] (execution time: 0.0001s)
        
    Note:
        The decorated function's docstring and metadata are preserved using
        the @wraps decorator from functools.
    """
    logger = logging.getLogger(logger_name)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            start_time = time.perf_counter()
            logger.info(f"Starting {func.__name__} with args={args}, kwargs={kwargs}")
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start_time
                logger.info(f"Completed {func.__name__} in {elapsed:.4f}s")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise
        
        return wrapper
    return decorator

# 3. Rate Limiter
def rate_limiter(max_calls: int, period: float):
    """
    Create a decorator that limits how often a function can be called.
    
    This implements a sliding window rate limiter that allows up to
    max_calls function calls within any period-second window.
    
    Args:
        max_calls: Maximum number of allowed calls within the period
        period: Time period in seconds for rate limiting
        
    Returns:
        A decorator that can be applied to limit function call rates
        
    Example:
        >>> @rate_limiter(max_calls=3, period=10.0)
        ... def fetch_data():
        ...     return "Data from API"
        >>> 
        >>> # First 3 calls within 10 seconds work
        >>> fetch_data()
        'Data from API'
        >>> # Subsequent calls within 10 seconds raise RateLimitExceeded
        
    Note:
        This implementation uses a closure to maintain the call history
        for each decorated function independently.
    """
    from collections import deque
    import time
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        calls: deque[float] = deque()
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            now = time.time()
            
            # Remove calls older than the period
            while calls and calls[0] <= now - period:
                calls.popleft()
            
            if len(calls) >= max_calls:
                time_until_next = period - (now - calls[0])
                raise RuntimeError(f"Rate limit exceeded. Try again in {time_until_next:.2f} seconds")
            
            calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# 4. Cache with Expiration
def cache_with_expiration(expire_seconds: float) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that caches function results with expiration."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[str, tuple[float, T]] = {}
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create a cache key
            key = json.dumps((args, sorted(kwargs.items())))
            now = time.time()
            
            # Check cache
            if key in cache:
                timestamp, result = cache[key]
                if now - timestamp < expire_seconds:
                    return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result
        
        return wrapper
    return decorator

# 5. Middleware Pattern
def create_middleware_chain(*middlewares: Callable[[Callable[[], T]], Callable[[], T]]) -> Callable[[Callable[[], T]], Callable[[], T]]:
    """Create a middleware chain for processing requests."""
    def apply_middleware(handler: Callable[[], T]) -> Callable[[], T]:
        # Apply middlewares in reverse order
        for middleware in reversed(middlewares):
            handler = middleware(handler)
        return handler
    return apply_middleware

# 6. Retry Mechanism
def retry(max_attempts: int, delay: float = 1.0, exceptions: tuple[type[Exception], ...] = (Exception,)) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that retries a function on failure."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(delay * attempt)  # Exponential backoff
            raise RuntimeError(f"Failed after {max_attempts} attempts") from last_exception
        return wrapper
    return decorator

def demonstrate_real_world_applications() -> None:
    """
    Showcase practical applications of closures in real-world scenarios.
    
    This function demonstrates several common patterns where closures provide
    elegant solutions to programming challenges:
    
    1. Configuration Management: Manage application settings with controlled access
    2. Logging: Add execution logging to functions
    3. Rate Limiting: Control how often functions can be called
    4. Caching: Store and retrieve computed results
    5. Middleware: Create processing pipelines
    6. Retry Mechanisms: Automatically retry failed operations
    
    Each example is self-contained and shows how closures help solve
    real programming problems in a clean, maintainable way.
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("app")
    
    print("=== Configuration Management ===")
    set_config, get_config, get_all = create_config_manager({"debug": False, "timeout": 30})
    
    set_config("debug", True)
    print(f"Debug mode: {get_config('debug')}")
    print(f"All config: {get_all()}")
    
    print("\n=== Logging Decorator ===")
    @log_execution("app")
    def process_data(data: str) -> str:
        """Process some data."""
        logger.info(f"Processing data: {data}")
        time.sleep(0.1)  # Simulate work
        return f"Processed: {data.upper()}"
    
    result = process_data("test data")
    print(f"Result: {result}")
    
    print("\n=== Rate Limiter ===")
    @rate_limiter(max_calls=3, period=5.0)
    def api_call() -> str:
        """Simulate an API call."""
        return "API response"
    
    print("Making API calls (limited to 3 per 5 seconds):")
    for i in range(5):
        try:
            print(f"Call {i+1}: {api_call()}")
        except Exception as e:
            print(f"Call {i+1} failed: {e}")
        time.sleep(1)  # Space out the calls
    
    print("\n=== Cache with Expiration ===")
    @cache_with_expiration(expire_seconds=2)
    def expensive_operation(x: int) -> int:
        print(f"Computing expensive_operation({x})...")
        time.sleep(0.5)
        return x * x
    
    print("First call (computes):", expensive_operation(5))
    print("Second call (cached):", expensive_operation(5))
    print("Waiting for cache to expire...")
    time.sleep(2.5)
    print("After expiration (computes again):", expensive_operation(5))
    
    print("\n=== Middleware Pattern ===")
    def logging_middleware(next_handler: Callable[[], T]) -> Callable[[], T]:
        def wrapper() -> T:
            print("Logging: Before handler")
            result = next_handler()
            print("Logging: After handler")
            return result
        return wrapper
    
    def timing_middleware(next_handler: Callable[[], T]) -> Callable[[], T]:
        def wrapper() -> T:
            start_time = time.time()
            result = next_handler()
            elapsed = time.time() - start_time
            print(f"Timing: Handler took {elapsed:.4f} seconds")
            return result
        return wrapper
    
    def handler() -> str:
        print("Handler: Processing request")
        time.sleep(0.5)
        return "Response from handler"
    
    # Apply middlewares
    apply_middleware = create_middleware_chain(logging_middleware, timing_middleware)
    wrapped_handler = apply_middleware(handler)
    
    print("Running handler with middlewares:")
    response = wrapped_handler()
    print(f"Final response: {response}")
    
    print("\n=== Retry Mechanism ===")
    attempt = 0
    
    @retry(max_attempts=3, delay=0.5, exceptions=(ValueError,))
    def unreliable_operation() -> str:
        """An operation that might fail."""
        nonlocal attempt
        attempt += 1
        if attempt < 3:
            raise ValueError(f"Temporary failure (attempt {attempt})")
        return "Operation succeeded"
    
    print("Running unreliable operation with retry:")
    try:
        result = unreliable_operation()
        print(f"Success: {result}")
    except Exception as e:
        print(f"Failed after retries: {e}")

if __name__ == "__main__":
    print("=== Real-World Applications of Closures ===")
    demonstrate_real_world_applications()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures are powerful for managing state in a controlled way")
    print("2. They enable patterns like configuration management and middleware")
    print("3. Decorators (which use closures) can add cross-cutting concerns")
    print("4. Closures help implement retry, caching, and rate limiting")
    print("5. They're widely used in web frameworks and libraries")
    print("6. Understanding closures is key to writing Pythonic, functional code")
