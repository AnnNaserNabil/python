"""
6. Tail Recursion and Optimization

Understanding and optimizing tail-recursive functions in Python.
- Understanding tail recursion
- Converting regular recursion to tail recursion
- Python's recursion limit and optimization
- Trampoline pattern
- Practical examples and benchmarks
"""
import sys
import time
from typing import TypeVar, Any, Callable, List, Tuple, Optional, Dict
from functools import wraps

T = TypeVar('T')
U = TypeVar('U')

# 1. Regular vs Tail Recursion
def factorial_recursive(n: int) -> int:
    """Regular recursive factorial (not tail-recursive)."""
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)

def factorial_tail(n: int, accumulator: int = 1) -> int:
    """Tail-recursive factorial implementation."""
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)

# 2. Python's Recursion Limit
def test_recursion_limit() -> None:
    """Demonstrate Python's recursion limit."""
    print(f"Current recursion limit: {sys.getrecursionlimit()}")
    
    # This will hit the recursion limit
    try:
        def recursive_func(depth: int):
            print(f"Depth: {depth}", end='\r')
            recursive_func(depth + 1)
        
        recursive_func(1)
    except RecursionError as e:
        print(f"\nRecursionError: {e}")

# 3. Tail Recursion Optimization with Trampoline
class TailCall(Exception):
    """Exception to return a tail call."""
    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs

def tail_call_optimized(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that optimizes tail calls using a trampoline."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        while isinstance(result, TailCall):
            result = result.func(*result.args, **result.kwargs)
        return result
    return wrapper

@tail_call_optimized
def factorial_trampoline(n: int, accumulator: int = 1) -> int:
    """Tail-recursive factorial using trampoline."""
    if n <= 1:
        return accumulator
    return TailCall(factorial_trampoline, n - 1, n * accumulator)

# 4. Memoization for Recursive Functions
def memoize_recursive(func: Callable[..., T]) -> Callable[..., T]:
    """Memoization decorator for recursive functions."""
    cache: Dict[Tuple[Any, ...], T] = {}
    
    @wraps(func)
    def wrapper(*args: Any) -> T:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper

@memoize_recursive
def fib_memo(n: int) -> int:
    """Memoized recursive Fibonacci."""
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

# 5. Converting Iterative to Recursive
def iterative_sum(numbers: List[int]) -> int:
    """Iterative sum of a list."""
    total = 0
    for num in numbers:
        total += num
    return total

def recursive_sum(numbers: List[int], index: int = 0) -> int:
    """Recursive sum of a list."""
    if index >= len(numbers):
        return 0
    return numbers[index] + recursive_sum(numbers, index + 1)

def tail_recursive_sum(numbers: List[int], index: int = 0, accumulator: int = 0) -> int:
    """Tail-recursive sum of a list."""
    if index >= len(numbers):
        return accumulator
    return tail_recursive_sum(numbers, index + 1, accumulator + numbers[index])

# 6. Practical Example: Directory Size Calculation
import os

def get_directory_size(path: str) -> int:
    """Recursively calculate directory size in bytes."""
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_directory_size(entry.path)
    except (PermissionError, FileNotFoundError):
        pass
    return total

def get_directory_size_tail(path: str, total: int = 0) -> int:
    """Tail-recursive directory size calculation."""
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total = get_directory_size_tail(entry.path, total)
    except (PermissionError, FileNotFoundError):
        pass
    return total

def benchmark() -> None:
    """Benchmark different implementations."""
    import timeit
    
    # Test with a small value to avoid stack overflow
    n = 15
    
    print(f"Factorial of {n}:")
    print(f"Recursive: {timeit.timeit(lambda: factorial_recursive(n), number=1000):.6f}s")
    print(f"Tail Recursive: {timeit.timeit(lambda: factorial_tail(n), number=1000):.6f}s")
    print(f"Trampoline: {timeit.timeit(lambda: factorial_trampoline(n), number=1000):.6f}s")
    
    # Test with a larger list
    numbers = list(range(1000))
    print("\nSum of 1000 numbers:")
    print(f"Iterative: {timeit.timeit(lambda: iterative_sum(numbers), number=1000):.6f}s")
    print(f"Recursive: {timeit.timeit(lambda: recursive_sum(numbers), number=1000):.6f}s")
    print(f"Tail Recursive: {timeit.timeit(lambda: tail_recursive_sum(numbers), number=1000):.6f}s")

def demonstrate_tail_recursion() -> None:
    """Demonstrate tail recursion concepts."""
    print("=== Regular vs Tail Recursion ===")
    n = 5
    print(f"Factorial of {n}:")
    print(f"Recursive: {factorial_recursive(n)}")
    print(f"Tail Recursive: {factorial_tail(n)}")
    
    print("\n=== Python's Recursion Limit ===")
    test_recursion_limit()
    
    print("\n=== Trampoline Pattern ===")
    print(f"Factorial with trampoline (n=10): {factorial_trampoline(10)}")
    
    print("\n=== Memoization for Recursive Functions ===")
    print(f"Fibonacci(35) with memoization: {fib_memo(35)}")
    
    print("\n=== Converting Iterative to Recursive ===")
    numbers = [1, 2, 3, 4, 5]
    print(f"Numbers: {numbers}")
    print(f"Iterative sum: {iterative_sum(numbers)}")
    print(f"Recursive sum: {recursive_sum(numbers)}")
    print(f"Tail-recursive sum: {tail_recursive_sum(numbers)}")
    
    print("\n=== Directory Size Calculation ===")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Size of current directory (recursive): {get_directory_size(current_dir) / 1024:.2f} KB")
    print(f"Size of current directory (tail-recursive): {get_directory_size_tail(current_dir) / 1024:.2f} KB")
    
    print("\n=== Performance Benchmark ===")
    benchmark()

if __name__ == "__main__":
    demonstrate_tail_recursion()
    
    print("\n=== Key Takeaways ===")
    print("1. Tail recursion eliminates the need for stack frames, but Python doesn't optimize it")
    print("2. Use iteration or the trampoline pattern for deep recursion in Python")
    print("3. Memoization can optimize overlapping subproblems in recursive functions")
    print("4. Python has a default recursion limit (usually 1000) to prevent stack overflow")
    print("5. For performance-critical code, consider rewriting deep recursion as iteration")
