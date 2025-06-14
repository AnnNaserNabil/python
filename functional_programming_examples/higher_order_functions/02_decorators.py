"""
2. Function Decorators

Advanced usage of decorators in Python.
- Basic decorators
- Decorators with arguments
- Class decorators
- Decorator factories
- Preserving function metadata
- Stacking decorators
"""
from typing import TypeVar, Callable, Any, Type, Optional, cast
from functools import wraps
import time
import logging
from datetime import datetime

T = TypeVar('T', bound=Callable[..., Any])
F = TypeVar('F', bound=Callable[..., Any])

# 1. Basic decorator
def log_calls(func: F) -> F:
    """Log function calls and return values."""
    @wraps(func)  # Preserves function metadata
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return cast(F, wrapper)

# 2. Decorator with arguments
def repeat(times: int) -> Callable[[F], F]:
    """Decorator that repeats the function call a specified number of times."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            results = []
            for i in range(times):
                print(f"Call {i + 1}/{times}")
                result = func(*args, **kwargs)
                results.append(result)
            return results[-1]  # Return the last result
        return cast(F, wrapper)
    return decorator

# 3. Class-based decorator
class Timer:
    """Decorator that measures function execution time."""
    
    def __init__(self, func: F):
        self.func = func
        self.execution_times: list[float] = []
        wraps(func)(self)
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = self.func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        self.execution_times.append(execution_time)
        print(f"{self.func.__name__} executed in {execution_time:.6f} seconds")
        return result
    
    def average_time(self) -> float:
        """Return the average execution time."""
        return sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0

# 4. Decorator with optional arguments
def log_to_file(filename: Optional[str] = None) -> Callable[[F], F]:
    """Log function calls to a file or stdout if no filename is provided."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log_message = (
                f"[{datetime.now().isoformat()}] "
                f"Calling {func.__name__} with args={args}, kwargs={kwargs}\n"
            )
            
            if filename:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(log_message)
            else:
                print(log_message, end='')
            
            return func(*args, **kwargs)
        return cast(F, wrapper)
    return decorator

# 5. Method decorator for class methods
def class_log_calls(method: F) -> F:
    """Decorator that logs method calls, including the class name."""
    @wraps(method)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        class_name = self.__class__.__name__
        print(f"Calling {class_name}.{method.__name__}")
        return method(self, *args, **kwargs)
    return cast(F, wrapper)

# 6. Decorator with state
class CountCalls:
    """Decorator that counts how many times a function is called."""
    
    def __init__(self, func: F):
        self.func = func
        self.call_count = 0
        wraps(func)(self)
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.call_count += 1
        print(f"Call {self.call_count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

# 7. Stacking decorators
def debug(func: F) -> F:
    """Print debug information about function calls."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        arg_str = ', '.join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        print(f"DEBUG: Calling {func.__name__}({arg_str})")
        result = func(*args, **kwargs)
        print(f"DEBUG: {func.__name__} returned {result!r}")
        return result
    return cast(F, wrapper)

def validate_input(validator: Callable[..., bool]) -> Callable[[F], F]:
    """Decorator to validate function arguments."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not validator(*args, **kwargs):
                raise ValueError("Validation failed for function arguments")
            return func(*args, **kwargs)
        return cast(F, wrapper)
    return decorator

def is_positive(x: int) -> bool:
    """Check if a number is positive."""
    return x > 0

# Example usage of decorators
@log_calls
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@repeat(3)
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"n
@Timer
def slow_function() -> None:
    """A function that takes some time to execute."""
    time.sleep(0.5)

@log_to_file("function_calls.log")
def save_data(data: str) -> None:
    """Save data (simulated)."""
    print(f"Saving data: {data}")

class Calculator:
    """A simple calculator class with decorated methods."""
    
    @class_log_calls
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    
    @CountCalls
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

@debug
@validate_input(is_positive)
def square_root(x: int) -> float:
    """Calculate the square root of a positive number."""
    return x ** 0.5

def demonstrate_decorators() -> None:
    """Show examples of decorators in action."""
    print("=== Basic Decorator ===")
    result = add(3, 5)
    print(f"Result: {result}")
    
    print("\n=== Decorator with Arguments ===")
    greeting = greet("Alice")
    print(f"Final greeting: {greeting}")
    
    print("\n=== Class-based Decorator ===")
    slow_function()
    slow_function()
    print(f"Average execution time: {slow_function.average_time():.6f} seconds")
    
    print("\n=== Method Decorator ===")
    calc = Calculator()
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"5 * 4 = {calc.multiply(5, 4)}")
    print(f"5 * 6 = {calc.multiply(5, 6)}")
    print(f"Method was called {calc.multiply.call_count} times")  # type: ignore
    
    print("\n=== Stacked Decorators ===")
    try:
        print(f"Square root of 9: {square_root(9)}")
        print(f"Square root of -4: {square_root(-4)}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n=== File Logging Decorator ===")
    save_data("Important information")
    print("Check function_calls.log for the log entry")

if __name__ == "__main__":
    demonstrate_decorators()
    
    print("\n=== Key Takeaways ===")
    print("1. Decorators modify or extend the behavior of functions/methods")
    print("2. Use @wraps to preserve function metadata")
    print("3. Decorators can accept arguments by adding another level of nesting")
    print("4. Class-based decorators can maintain state between calls")
    print("5. Decorators can be stacked to combine multiple behaviors")
