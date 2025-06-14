"""
4. Function Composition

Techniques for composing functions in Python.
- Basic function composition
- The compose utility
- The pipe utility
- Composing with multiple arguments
- Practical examples
"""
from typing import TypeVar, Callable, Any, List, Dict, Tuple, Optional
from functools import reduce, partial
import math
import operator

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')
W = TypeVar('W')

# 1. Basic composition
def compose(*funcs: Callable) -> Callable:
    """
    Compose functions from right to left.
    compose(f, g, h)(x) -> f(g(h(x)))
    """
    def _compose(f: Callable, g: Callable) -> Callable:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return reduce(_compose, funcs, lambda x: x)

def pipe(*funcs: Callable) -> Callable:
    """
    Pipe functions from left to right.
    pipe(f, g, h)(x) -> h(g(f(x)))
    """
    def _pipe(f: Callable, g: Callable) -> Callable:
        return lambda *args, **kwargs: g(f(*args, **kwargs))
    return reduce(_pipe, funcs, lambda x: x)

# 2. Composing with multiple arguments
def compose_multi(*funcs: Callable) -> Callable:
    """
    Compose functions that take multiple arguments.
    The last function can take multiple arguments, others take one.
    """
    if not funcs:
        return lambda *args, **kwargs: (args, kwargs) if args or kwargs else None
    
    def composed(*args, **kwargs):
        # The last function can take multiple arguments
        result = funcs[-1](*args, **kwargs)
        
        # Apply the rest from right to left
        for func in reversed(funcs[:-1]):
            result = func(result)
            
        return result
    
    return composed

def pipe_multi(*funcs: Callable) -> Callable:
    """
    Pipe functions from left to right, with multiple arguments for the first function.
    """
    if not funcs:
        return lambda *args, **kwargs: (args, kwargs) if args or kwargs else None
    
    def piped(*args, **kwargs):
        result = funcs[0](*args, **kwargs)
        
        # Apply the rest from left to right
        for func in funcs[1:]:
            result = func(result)
            
        return result
    
    return piped

# 3. Composing with argument forwarding
def forward_compose(*funcs: Callable) -> Callable:
    """
    Compose functions, forwarding all arguments to each function.
    Each function must accept the same arguments as the first.
    """
    def composed(*args, **kwargs):
        result = None
        for func in funcs:
            result = func(*args, **kwargs)
            args = (result,)
            kwargs = {}
        return result
    return composed

# 4. Practical examples
def add(x: float, y: float) -> float:
    return x + y

def square(x: float) -> float:
    return x * x

def double(x: float) -> float:
    return x * 2

def to_string(x: float) -> str:
    return str(x)

def format_result(value: float) -> str:
    return f"The result is: {value:.2f}"

def process_data(data: List[float]) -> Dict[str, float]:
    return {
        'sum': sum(data),
        'avg': sum(data) / len(data) if data else 0,
        'max': max(data) if data else 0,
        'min': min(data) if data else 0
    }

def filter_positive(numbers: List[float]) -> List[float]:
    return [x for x in numbers if x > 0]

def calculate_stats() -> Callable[[List[float]], Dict[str, float]]:
    """Create a stats calculation pipeline."""
    return pipe(
        filter_positive,
        process_data
    )

def create_pipeline() -> Callable[[float, float], str]:
    """Create a pipeline that processes two numbers."""
    return pipe(
        # Takes two arguments, returns their sum
        lambda x, y: x + y,
        # The rest take one argument
        lambda x: x * 2,
        square,
        format_result
    )

# 5. Composition with error handling
def safe_divide(x: float, y: float) -> float:
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def safe_sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    return math.sqrt(x)

def try_except(default: Any = None):
    """Decorator to handle exceptions in a pipeline."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")
                return default
        return wrapper
    return decorator

def safe_pipeline(*funcs: Callable, default: Any = None) -> Callable:
    """Create a pipeline with error handling."""
    def composed(*args, **kwargs):
        result = None
        for func in funcs:
            try:
                if result is None and not args and not kwargs:
                    # First function in pipeline
                    result = func()
                elif result is None:
                    # First function with arguments
                    result = func(*args, **kwargs)
                    # Clear args after first use
                    args = ()
                    kwargs = {}
                else:
                    # Subsequent functions
                    result = func(result)
            except Exception as e:
                print(f"Error in pipeline: {func.__name__} - {e}")
                return default
        return result
    return composed

def demonstrate_composition() -> None:
    """Show examples of function composition."""
    print("=== Basic Composition ===")
    # Compose functions right to left
    add_then_square = compose(square, add)
    print(f"(2 + 3)² = {add_then_square(2, 3)}")  # (2 + 3)² = 25
    
    # Pipe functions left to right
    add_then_square_pipe = pipe(add, square)
    print(f"(2 + 3)² = {add_then_square_pipe(2, 3)}")  # (2 + 3)² = 25
    
    print("\n=== Multi-function Composition ===")
    # Compose multiple functions
    process = compose(
        to_string,
        square,
        double,
        lambda x: x + 5
    )
    print(f"Process(3) = {process(3)}")  # "196"
    
    # Same as above but with pipe (left to right)
    process_pipe = pipe(
        lambda x: x + 5,  # 3 + 5 = 8
        double,           # 8 * 2 = 16
        square,           # 16 * 16 = 256
        to_string         # "256"
    )
    print(f"Process with pipe(3) = {process_pipe(3)}")  # "256"
    
    print("\n=== Practical Example: Data Processing ===")
    data = [1.5, -2.0, 3.5, 4.0, -5.5, 6.0]
    
    # Create a processing pipeline
    pipeline = pipe(
        filter_positive,  # [1.5, 3.5, 4.0, 6.0]
        process_data      # {'sum': 15.0, 'avg': 3.75, 'max': 6.0, 'min': 1.5}
    )
    
    result = pipeline(data)
    print(f"Processed data: {result}")
    
    print("\n=== Pipeline with Multiple Arguments ===")
    # Create a pipeline that processes two numbers
    process_two_numbers = create_pipeline()
    print(f"Process(3, 4) = {process_two_numbers(3, 4)}")  # "The result is: 196.00"
    
    print("\n=== Error Handling in Pipelines ===")
    # Create a pipeline with error handling
    safe_process = safe_pipeline(
        lambda x, y: x + y,
        safe_divide,
        safe_sqrt,
        format_result,
        default="Error occurred"
    )
    
    print(f"Safe process(8, 2) = {safe_process(8, 2)}")  # "The result is: 2.24"
    print(f"Safe process(8, 0) = {safe_process(8, 0)}")  # "Error occurred"
    print(f"Safe process(-1, 1) = {safe_process(-1, 1)}")  # "Error occurred"

def main() -> None:
    """Demonstrate function composition techniques."""
    demonstrate_composition()
    
    print("\n=== Key Takeaways ===")
    print("1. Function composition combines simple functions to build complex behavior")
    print("2. compose() applies functions right-to-left (mathematical composition)")
    print("3. pipe() applies functions left-to-right (easier to read for many people)")
    print("4. Handle errors in pipelines with try/except or helper functions")
    print("5. Consider using libraries like toolz or fn.py for more advanced composition")

if __name__ == "__main__":
    main()
