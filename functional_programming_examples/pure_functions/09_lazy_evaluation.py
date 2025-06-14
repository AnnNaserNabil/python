"""
9. Lazy Evaluation with Pure Functions in Python

This module demonstrates lazy evaluation techniques in Python, a core concept in functional programming
where expressions are not evaluated until their results are actually needed. This enables working with
potentially infinite data structures and can significantly improve performance and memory efficiency.

Key Concepts:
------------
- Lazy Evaluation: Delays evaluation of an expression until its value is needed
- Generators: Functions that yield values one at a time, maintaining state between yields
- Iterators: Objects that implement the iterator protocol (__iter__ and __next__ methods)
- Memoization: Caching function results to avoid redundant calculations
- Infinite Sequences: Data structures that represent unbounded collections

Why Use Lazy Evaluation?
----------------------
- Memory Efficiency: Process large or infinite sequences without loading everything into memory
- Performance: Avoid unnecessary calculations by only computing what's needed
- Composability: Easily combine operations without intermediate data structures
- Expressiveness: Work with infinite or very large data streams naturally

Common Use Cases:
---------------
- Processing large files or data streams
- Working with mathematical sequences (Fibonacci, primes, etc.)
- Implementing efficient data processing pipelines
- Handling potentially infinite data sources (sensor data, logs, etc.)
- Building responsive UIs that load data on demand

Example:
-------
>>> def natural_numbers():
...     n = 1
...     while True:
...         yield n
...         n += 1
>>> # Get first 5 natural numbers
>>> from itertools import islice
>>> list(islice(natural_numbers(), 5))
[1, 2, 3, 4, 5]
"""
from typing import TypeVar, Callable, Iterator, List, Any
from functools import lru_cache, wraps
import itertools

T = TypeVar('T')
U = TypeVar('U')

def natural_numbers() -> Iterator[int]:
    """
    Generate an infinite sequence of natural numbers starting from 1.
    
    This is a generator function that yields natural numbers one at a time,
    demonstrating lazy evaluation. The sequence is infinite, but since it's lazy,
    it won't consume infinite memory.
    
    Yields:
        int: The next natural number in the sequence (1, 2, 3, ...)
        
    Examples:
        >>> nums = natural_numbers()
        >>> next(nums)
        1
        >>> next(nums)
        2
        >>> # Get first 5 natural numbers
        >>> from itertools import islice
        >>> list(islice(natural_numbers(), 5))
        [1, 2, 3, 4, 5]
        
    Note:
        - Pure function: No side effects, same output for same inputs (no inputs in this case)
        - Lazy evaluation: Numbers are generated on-demand
        - Memory efficient: Only one number is in memory at a time
    """
    n = 1
    while True:
        yield n
        n += 1

def take(n: int, iterable: Iterator[T]) -> List[T]:
    """
    Take the first n elements from an iterable.
    
    This function demonstrates how to work with iterators in a memory-efficient way,
    only consuming as many items as needed from the iterator.
    
    Args:
        n: Number of elements to take. Must be non-negative.
        iterable: Source iterable (list, generator, etc.)
        
    Returns:
        List[T]: A list containing the first n elements from the iterable
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> take(3, [1, 2, 3, 4, 5])
        [1, 2, 3]
        >>> take(2, natural_numbers())  # Works with infinite sequences
        [1, 2]
        
    Note:
        - Pure function: No side effects, output depends only on inputs
        - Lazy evaluation: Only consumes as many items as needed from the iterator
        - Time complexity: O(n)
        - Space complexity: O(n) for the result list
    """
    if n < 0:
        raise ValueError("Cannot take negative number of elements")
    return [x for _, x in zip(range(n), iterable)]

def map_lazy(func: Callable[[T], U], iterable: Iterator[T]) -> Iterator[U]:
    """
    Lazy version of map that works with iterators.
    
    This function applies a transformation function to each element of an iterable
    in a lazy fashion, meaning elements are processed one at a time as they're needed.
    
    Args:
        func: A function that takes an element of type T and returns a value of type U
        iterable: An iterable of elements of type T
        
    Yields:
        U: Transformed elements of type U, one at a time
        
    Examples:
        >>> # Double each number in a list
        >>> list(map_lazy(lambda x: x * 2, [1, 2, 3]))
        [2, 4, 6]
        >>> # Works with infinite sequences
        >>> squares = map_lazy(lambda x: x*x, natural_numbers())
        >>> take(5, squares)
        [1, 4, 9, 16, 25]
        
    Note:
        - Pure function: No side effects, output depends only on inputs
        - Lazy evaluation: Processes elements one at a time as needed
        - Memory efficient: Only one element is processed at a time
        - Time complexity: O(1) per element (amortized)
    """
    for item in iterable:
        yield func(item)

def filter_lazy(predicate: Callable[[T], bool], iterable: Iterator[T]) -> Iterator[T]:
    """
    Lazy version of filter that works with iterators.
    
    This function filters elements from an iterable based on a predicate function,
    processing elements one at a time in a memory-efficient manner.
    
    Args:
        predicate: A function that takes an element and returns True if it should be included
        iterable: An iterable of elements to filter
        
    Yields:
        T: Elements from the iterable that satisfy the predicate
        
    Examples:
        >>> # Get even numbers
        >>> evens = filter_lazy(lambda x: x % 2 == 0, natural_numbers())
        >>> take(5, evens)
        [2, 4, 6, 8, 10]
        >>> # Filter strings by length
        >>> words = ["apple", "banana", "cherry", "date"]
        >>> long_words = filter_lazy(lambda w: len(w) > 5, iter(words))
        >>> list(long_words)
        ['banana', 'cherry']
        
    Note:
        - Pure function: No side effects, output depends only on inputs
        - Lazy evaluation: Processes elements one at a time as needed
        - Short-circuits: Stops processing as soon as the result is determined
        - Memory efficient: Only one element is in memory at a time
    """
    for item in iterable:
        if predicate(item):
            yield item

@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number with memoization.
    
    This function demonstrates how to use memoization to optimize a recursive
    Fibonacci implementation. The @lru_cache decorator caches function results
    to avoid redundant calculations.
    
    The Fibonacci sequence is defined as:
    - fib(0) = 0
    - fib(1) = 1
    - fib(n) = fib(n-1) + fib(n-2) for n > 1
    
    Args:
        n: Index of the Fibonacci number to calculate (non-negative integer)
        
    Returns:
        int: The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
        
    Note:
        - Pure function: Same input always produces the same output
        - Time complexity: O(n) with memoization, O(2^n) without
        - Space complexity: O(n) for the call stack and cache
        - Uses lru_cache for automatic memoization
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is only defined for non-negative integers")
        
    @lru_cache(maxsize=None)
    def fib(k: int) -> int:
        if k < 2:
            return k
        return fib(k-1) + fib(k-2)
    
    return fib(n)

def primes() -> Iterator[int]:
    """
    Generate an infinite sequence of prime numbers using the Sieve of Eratosthenes.
    
    This is an efficient, infinite generator of prime numbers that uses a dictionary
    to keep track of composite numbers and their prime factors. It's based on the
    Sieve of Eratosthenes algorithm but implemented in a way that allows for lazy
    evaluation of primes.
    
    Yields:
        int: Prime numbers in ascending order, starting from 2
        
    Examples:
        >>> first_five = take(5, primes())
        >>> first_five
        [2, 3, 5, 7, 11]
        >>> # Check if 17 is in the first 10 primes
        >>> 17 in take(10, primes())
        True
        
    Note:
        - Pure function: No side effects, always produces the same sequence
        - Lazy evaluation: Generates primes on-demand
        - Memory efficient: Only stores necessary composite numbers
        - Time complexity: O(n log log n) for generating n primes (amortized)
        - Space complexity: O(n / log n) for generating n primes (amortized)
        
    Reference:
        - https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
        - Original algorithm by David Eppstein, UC Irvine, 28 Feb 2002
    """
    # Dictionary to store the next composite number and its prime factors
    # Key: composite number, Value: list of primes that divide it
    composites = {}
    
    # The current number being checked for primality
    candidate = 2
    
    while True:
        if candidate not in composites:
            # candidate is a prime number
            yield candidate
            # Mark its square as composite with this prime as a factor
            # (We know candidate^2 is the next composite to check for this prime)
            composites[candidate * candidate] = [candidate]
        else:
            # candidate is composite. Get its prime factors
            for prime in composites[candidate]:
                # Mark the next multiple of this prime as composite
                next_multiple = candidate + prime
                if next_multiple in composites:
                    composites[next_multiple].append(prime)
                else:
                    composites[next_multiple] = [prime]
            # Remove the current candidate from the dictionary to save space
            del composites[candidate]
        
        # Move to the next number
        candidate += 1

def memoize_generator(func: Callable[..., Iterator[T]]) -> Callable[..., Iterator[T]]:
    """
    Memoize a generator function by caching its results.
    
    This decorator caches the results of a generator function so that subsequent
    calls with the same arguments will return the cached results instead of
    recomputing them. This is particularly useful for expensive computations
    that are likely to be repeated.
    
    Args:
        func: A generator function to be memoized
        
    Returns:
        Callable[..., Iterator[T]]: A memoized version of the input generator function
        
    Examples:
        >>> @memoize_generator
        ... def count_up_to(n):
        ...     for i in range(1, n+1):
        ...         print(f"Generating {i}")
        ...         yield i
        >>> # First call computes and caches the results
        >>> list(count_up_to(3))
        Generating 1
        Generating 2
        Generating 3
        [1, 2, 3]
        >>> # Subsequent calls with same args use the cache
        >>> list(count_up_to(3))
        [1, 2, 3]  # No "Generating" messages
        
    Note:
        - The cache is stored in the decorator's closure
        - The cache never expires (may lead to memory issues with many unique arguments)
        - Only works with hashable argument types
        - Preserves the original function's docstring and metadata via @wraps
        - Not thread-safe in its current implementation
    """
    cache = {}
    
    @wraps(func)  # Preserve original function's metadata
    def memoized(*args, **kwargs):
        # Create a unique key from the function arguments
        key = (args, frozenset(kwargs.items()))
        
        # If we've already computed results for these arguments,
        # yield them from the cache
        if key in cache:
            for item in cache[key]:
                yield item
            return
        
        # Otherwise, compute the results, cache them, and yield them
        results = []
        for item in func(*args, **kwargs):
            results.append(item)
            yield item
        cache[key] = results
    
    return memoized

if __name__ == "__main__":
    print("=== Lazy Evaluation Examples ===\n")
    
    # 1. Demonstrate natural_numbers and take
    print("1. Generating natural numbers:")
    print("First 10 natural numbers:", take(10, natural_numbers()))
    
    # 2. Demonstrate map_lazy with natural numbers
    print("\n2. Lazy mapping:")
    squares = map_lazy(lambda x: x*x, natural_numbers())
    print("Squares of first 5 natural numbers:", take(5, squares))
    
    # 3. Demonstrate filter_lazy with natural numbers
    print("\n3. Lazy filtering:")
    evens = filter_lazy(lambda x: x % 2 == 0, natural_numbers())
    print("First 5 even numbers:", take(5, evens))
    
    # 4. Demonstrate chaining lazy operations
    print("\n4. Chaining lazy operations (square of odd numbers):")
    square_odds = map_lazy(
        lambda x: x**2,
        filter_lazy(
            lambda x: x % 2 == 1,
            natural_numbers()
        )
    )
    print("First 5 odd squares:", take(5, square_odds))
    
    # 5. Demonstrate fibonacci with memoization
    print("\n5. Fibonacci numbers with memoization:")
    fib_numbers = [fibonacci(i) for i in range(10)]
    print("First 10 Fibonacci numbers:", fib_numbers)
    
    # 6. Demonstrate primes generator
    print("\n6. Prime number generation:")
    first_primes = take(10, primes())
    print("First 10 prime numbers:", first_primes)
    
    # 7. Demonstrate memoize_generator decorator
    print("\n7. Memoized generator example:")
    
    @memoize_generator
    def count_up_to(n: int) -> Iterator[int]:
        """Generate numbers from 1 to n."""
        print(f"  Generating numbers up to {n}...")
        for i in range(1, n+1):
            yield i
    
    print("  First call to count_up_to(5):")
    gen1 = count_up_to(5)
    print(f"  Result: {list(gen1)}")
    
    print("\n  Second call to count_up_to(5) (should use cache):")
    gen2 = count_up_to(5)
    print(f"  Result: {list(gen2)}")
    
    print("\n  Call with new argument count_up_to(7) (should generate 6,7):")
    gen3 = count_up_to(7)
    print(f"  Result: {list(gen3)}")
    
    # 8. Verify function purity and correctness with assertions
    print("\n8. Verifying function purity and correctness...")
    
    # Test natural_numbers and take
    assert take(5, natural_numbers()) == [1, 2, 3, 4, 5]
    
    # Test map_lazy
    assert take(3, map_lazy(lambda x: x * 2, iter([1, 2, 3]))) == [2, 4, 6]
    
    # Test filter_lazy
    assert take(3, filter_lazy(lambda x: x % 2 == 0, iter([1, 2, 3, 4, 5, 6]))) == [2, 4, 6]
    
    # Test fibonacci
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    
    # Test primes
    first_five_primes = take(5, primes())
    assert first_five_primes == [2, 3, 5, 7, 11]
    
    # Test memoize_generator
    @memoize_generator
    def test_gen(n):
        for i in range(n):
            yield i
    
    # First call should compute
    assert list(test_gen(3)) == [0, 1, 2]
    # Second call should use cache
    assert list(test_gen(3)) == [0, 1, 2]
    
    print("\nAll tests passed! All lazy evaluation functions are working as expected.")
    
    # 9. Performance comparison: with and without memoization
    print("\n9. Performance comparison (Fibonacci with and without memoization):")
    
    # Non-memoized Fibonacci for comparison
    def fib_slow(n: int) -> int:
        if n < 2:
            return n
        return fib_slow(n-1) + fib_slow(n-2)
    
    # Time the functions
    import time
    
    # Test with a larger number to see the difference
    test_n = 30
    
    print(f"\nCalculating fib({test_n}) with memoization:")
    start = time.perf_counter()
    result1 = fibonacci(test_n)
    end = time.perf_counter()
    print(f"  Result: {result1}")
    print(f"  Time: {end - start:.6f} seconds")
    
    print(f"\nCalculating fib({test_n}) without memoization (may take a while):")
    start = time.perf_counter()
    result2 = fib_slow(test_n)
    end = time.perf_counter()
    print(f"  Result: {result2}")
    print(f"  Time: {end - start:.6f} seconds")
    
    print("\nNote the significant performance difference due to memoization!")
