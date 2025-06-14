"""
9. Lazy Evaluation with Pure Functions

Implementing lazy evaluation patterns in a pure functional style.
- Generators for lazy sequences
- Memoization of function results
- Infinite sequences
"""
from typing import TypeVar, Callable, Iterator, List, Any
from functools import lru_cache
import itertools

T = TypeVar('T')
U = TypeVar('U')

def natural_numbers() -> Iterator[int]:
    """
    Generate an infinite sequence of natural numbers.
    
    Yields:
        Natural numbers starting from 1
    """
    n = 1
    while True:
        yield n
        n += 1

def take(n: int, iterable: Iterator[T]) -> List[T]:
    """
    Take the first n elements from an iterable.
    
    Args:
        n: Number of elements to take
        iterable: Source iterable
        
    Returns:
        List of the first n elements
    """
    return [x for _, x in zip(range(n), iterable)]

def map_lazy(func: Callable[[T], U], iterable: Iterator[T]) -> Iterator[U]:
    """
    Lazy version of map that works with iterators.
    
    Args:
        func: Function to apply
        iterable: Source iterable
        
    Yields:
        Transformed elements
    """
    for item in iterable:
        yield func(item)

def filter_lazy(predicate: Callable[[T], bool], iterable: Iterator[T]) -> Iterator[T]:
    """
    Lazy version of filter that works with iterators.
    
    Args:
        predicate: Function that returns True for elements to keep
        iterable: Source iterable
        
    Yields:
        Elements that satisfy the predicate
    """
    for item in iterable:
        if predicate(item):
            yield item

@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number with memoization.
    
    Args:
        n: Index of the Fibonacci number to calculate
        
    Returns:
        The nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def primes() -> Iterator[int]:
    """
    Generate an infinite sequence of prime numbers using the Sieve of Eratosthenes.
    
    Yields:
        Prime numbers starting from 2
    """
    D = {}  # Map composite numbers to primes that divide them
    q = 2   # Current number to test for primality
    
    while True:
        if q not in D:
            # q is a prime number
            D[q * q] = [q]
            yield q
        else:
            # q is composite, add next multiple to the sieve
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1

def memoize_generator(func: Callable[..., Iterator[T]]) -> Callable[..., Iterator[T]]:
    """
    Memoize a generator function by caching its results.
    
    Args:
        func: Generator function to memoize
        
    Returns:
        Memoized version of the generator function
    """
    cache = []
    
    @wraps(func)
    def wrapper(*args, **kwargs) -> Iterator[T]:
        # Return cached results first
        for item in cache:
            yield item
            
        # Then generate and cache new items
        gen = func(*args, **kwargs)
        for item in gen:
            cache.append(item)
            yield item
    
    return wrapper

# Example usage
if __name__ == "__main__":
    # Test natural_numbers and take
    print("First 10 natural numbers:")
    print(take(10, natural_numbers()))
    
    # Test map_lazy
    squares = map_lazy(lambda x: x * x, natural_numbers())
    print("\nFirst 5 squares:")
    print(take(5, squares))
    
    # Test filter_lazy
    evens = filter_lambda(lambda x: x % 2 == 0, natural_numbers())
    print("\nFirst 5 even numbers:")
    print(take(5, evens))
    
    # Test fibonacci with memoization
    print("\nFibonacci numbers:")
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
    
    # Test primes generator
    print("\nFirst 10 prime numbers:")
    print(take(10, primes()))
    
    # Test memoize_generator
    @memoize_generator
    def count_up_to(n: int) -> Iterator[int]:
        for i in range(1, n + 1):
            yield i
    
    print("\nTesting memoized generator:")
    gen1 = count_up_to(5)
    print("First run:", list(gen1))
    gen2 = count_up_to(7)  # Should return cached results first, then generate 6,7
    print("Second run:", list(gen2))
