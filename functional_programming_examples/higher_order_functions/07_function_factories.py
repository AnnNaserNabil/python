"""
7. Function Factories with Higher-Order Functions

Demonstrates how to create functions dynamically using higher-order functions
and closures to generate specialized functions at runtime.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Any, Dict, List, Tuple, Optional, Type
from functools import partial, wraps
import math
import time
import random

T = TypeVar('T')
U = TypeVar('U')

# 1. Basic Function Factory

def create_multiplier(factor: float) -> Callable[[float], float]:
    """Create a function that multiplies its input by a fixed factor."""
    def multiplier(x: float) -> float:
        return x * factor
    return multiplier

# 2. Function Factory with Configuration

def create_power_function(exponent: float) -> Callable[[float], float]:
    """Create a function that raises its input to a given power."""
    def power(x: float) -> float:
        return x ** exponent
    return power

# 3. Function Factory with Validation

def create_validator(
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    allowed_values: Optional[List[Any]] = None
) -> Callable[[Any], bool]:
    """
    Create a validation function that checks if a value meets certain criteria.
    
    Args:
        min_value: If provided, value must be >= min_value
        max_value: If provided, value must be <= max_value
        allowed_values: If provided, value must be in this list
    
    Returns:
        A function that takes a value and returns a boolean indicating validity
    """
    def validate(value: Any) -> bool:
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        if allowed_values is not None and value not in allowed_values:
            return False
        return True
    
    return validate

# 4. Function Factory for Caching

def create_cached_function(
    func: Callable[..., T],
    max_size: int = 128
) -> Callable[..., T]:
    """
    Create a cached version of a function with LRU (Least Recently Used) eviction.
    
    Args:
        func: The function to cache
        max_size: Maximum number of entries to keep in the cache
    
    Returns:
        A new function with caching behavior
    """
    cache: Dict[Tuple[Any, ...], T] = {}
    cache_order: List[Tuple[Any, ...]] = []
    
    def cached_func(*args: Any, **kwargs: Any) -> T:
        # Create a cache key from the function arguments
        key = (args, frozenset(kwargs.items()))
        
        # Check cache
        if key in cache:
            # Move to end of LRU list
            cache_order.remove(key)
            cache_order.append(key)
            return cache[key]
        
        # Call the original function
        result = func(*args, **kwargs)
        
        # Add to cache
        if len(cache) >= max_size:
            # Remove least recently used item
            oldest_key = cache_order.pop(0)
            del cache[oldest_key]
        
        cache[key] = result
        cache_order.append(key)
        return result
    
    return cached_func

# 5. Function Factory for Retry Logic

def create_retryable_function(
    func: Callable[..., T],
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable[..., T]:
    """
    Create a function that retries on failure with exponential backoff.
    
    Args:
        func: The function to make retryable
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each failure
        exceptions: Tuple of exceptions to catch and retry on
    
    Returns:
        A new function with retry behavior
    """
    def retryable_func(*args: Any, **kwargs: Any) -> T:
        current_delay = delay
        last_exception = None
        
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                if attempt == max_attempts - 1:
                    break  # Don't sleep on the last attempt
                    
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {current_delay:.1f}s...")
                time.sleep(current_delay)
                current_delay *= backoff
        
        raise last_exception  # type: ignore
    
    return retryable_func

# 6. Function Factory for Logging

def create_logged_function(
    func: Callable[..., T],
    logger: Callable[[str], None] = print,
    log_args: bool = True,
    log_result: bool = True,
    log_time: bool = True
) -> Callable[..., T]:
    """
    Create a function that logs its arguments, result, and execution time.
    
    Args:
        func: The function to add logging to
        logger: Function to handle log messages (defaults to print)
        log_args: Whether to log function arguments
        log_result: Whether to log the return value
        log_time: Whether to log execution time
    
    Returns:
        A new function with logging behavior
    """
    def logged_func(*args: Any, **kwargs: Any) -> T:
        # Log function call with arguments
        if log_args:
            args_str = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
            logger(f"Calling {func.__name__}({args_str})")
        
        # Time the function execution
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            
            # Log result and time
            if log_result:
                logger(f"{func.__name__} returned: {result!r}")
            
            if log_time:
                elapsed = time.perf_counter() - start_time
                logger(f"{func.__name__} took {elapsed:.6f} seconds")
            
            return result
            
        except Exception as e:
            logger(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise
    
    return logged_func

# 7. Function Factory for Rate Limiting

def create_rate_limited_function(
    func: Callable[..., T],
    calls: int,
    period: float
) -> Callable[..., T]:
    """
    Create a rate-limited version of a function.
    
    Args:
        func: The function to rate-limit
        calls: Maximum number of calls allowed in the period
        period: Time period in seconds
    
    Returns:
        A new function with rate limiting
    """
    from collections import deque
    import time
    
    call_times: deque[float] = deque(maxlen=calls)
    
    def rate_limited_func(*args: Any, **kwargs: Any) -> T:
        now = time.time()
        
        # Remove timestamps older than the period
        while call_times and call_times[0] <= now - period:
            call_times.popleft()
        
        # Check if we've reached the rate limit
        if len(call_times) >= calls:
            # Calculate how long to wait
            time_to_wait = call_times[0] + period - now
            if time_to_wait > 0:
                time.sleep(time_to_wait)
        
        # Record the call time
        call_time = time.time()
        call_times.append(call_time)
        
        # Call the original function
        return func(*args, **kwargs)
    
    return rate_limited_func

# Example Usage
def demonstrate_function_factories() -> None:
    print("=== Function Factories with Higher-Order Functions ===\n")
    
    # 1. Basic multiplier
    print("1. Basic Multiplier:")
    double = create_multiplier(2.0)
    triple = create_multiplier(3.0)
    print(f"Double of 5: {double(5)}")
    print(f"Triple of 5: {triple(5)}")
    
    # 2. Power functions
    print("\n2. Power Functions:")
    square = create_power_function(2)
    cube = create_power_function(3)
    print(f"Square of 4: {square(4)}")
    print(f"Cube of 4: {cube(4)}")
    
    # 3. Validation
    print("\n3. Validation:")
    is_positive = create_validator(min_value=0)
    is_digit = create_validator(allowed_values=list('0123456789'))
    print(f"Is 5 positive? {is_positive(5)}")
    print(f"Is -1 positive? {is_positive(-1)}")
    print(f"Is '7' a digit? {is_digit('7')}")
    print(f"Is 'a' a digit? {is_digit('a')}")
    
    # 4. Caching
    print("\n4. Caching:")
    
    def expensive_calculation(x: int) -> int:
        print(f"  Calculating square of {x}...")
        return x * x
    
    cached_calc = create_cached_function(expensive_calculation, max_size=2)
    print("First call (should calculate):")
    print(f"  Result: {cached_calc(3)}")
    print("Second call (should use cache):")
    print(f"  Result: {cached_calc(3)}")
    print("Third call with different arg (should calculate):")
    print(f"  Result: {cached_calc(4)}")
    
    # 5. Retry logic
    print("\n5. Retry Logic:")
    
    def unreliable_operation() -> int:
        if random.random() < 0.7:  # 70% chance of failure
            raise ValueError("Temporary failure")
        return 42
    
    reliable_op = create_retryable_function(
        unreliable_operation,
        max_attempts=3,
        delay=0.5,
        backoff=2.0,
        exceptions=(ValueError,)
    )
    
    print("Running unreliable operation with retries:")
    try:
        result = reliable_op()
        print(f"  Success! Result: {result}")
    except Exception as e:
        print(f"  Failed after retries: {e}")
    
    # 6. Logging
    print("\n6. Logging:")
    
    def add(a: int, b: int) -> int:
        return a + b
    
    logged_add = create_logged_function(add)
    print("Calling logged function:")
    print(f"  Result: {logged_add(3, 4)}")
    
    # 7. Rate limiting
    print("\n7. Rate Limiting:")
    
    def api_call(x: int) -> str:
        return f"API result for {x}"
    
    # Limit to 2 calls per second
    limited_api = create_rate_limited_function(api_call, calls=2, period=1.0)
    
    print("Making rapid API calls (limited to 2 per second):")
    start_time = time.time()
    
    for i in range(5):
        result = limited_api(i)
        elapsed = time.time() - start_time
        print(f"  Call {i}: {result} (took {elapsed:.2f}s)")

if __name__ == "__main__":
    demonstrate_function_factories()
    
    print("\n=== Key Takeaways ===")
    print("1. Function factories create and return new functions dynamically")
    print("2. They enable behavior customization through closures")
    print("3. Common patterns include validation, caching, retries, and logging")
    print("4. Function composition allows building complex behavior from simple parts")
