"""
6. Recursive Pure Functions in Python

This module demonstrates how to implement pure recursive functions in Python.
Recursion is a programming technique where a function calls itself to solve
smaller instances of the same problem.

Key Concepts:
------------
- Base Case: The condition that stops the recursion (to prevent infinite loops)
- Recursive Case: The part where the function calls itself with a smaller input
- Call Stack: The data structure that tracks function calls (can grow deep)
- Tail Recursion: When the recursive call is the last operation (not optimized in Python)
- Memoization: Caching results to avoid redundant calculations

Why Use Recursion?
----------------
- Natural fit for problems with recursive structure (trees, graphs, etc.)
- Often leads to cleaner, more readable code
- Functional programming style (avoids mutable state)
- Makes some algorithms more intuitive to implement

Potential Pitfalls:
-----------------
- Can lead to stack overflow for deep recursion
- May be less efficient than iterative solutions
- Can be harder to debug
- Python has a default recursion limit (usually 1000)

Real-world Applications:
----------------------
- File system traversal
- Tree and graph algorithms
- Mathematical computations (factorial, Fibonacci, etc.)
- Parsing and syntax analysis
- Divide-and-conquer algorithms

Example:
-------
>>> sum_list([1, 2, 3, 4])  # 1 + 2 + 3 + 4 = 10
10
>>> find_max([3, 1, 4, 1, 5, 9])
9
>>> flatten([1, [2, [3, 4], 5]])
[1, 2, 3, 4, 5]
"""
from typing import List, TypeVar, Callable, Any
from functools import wraps

T = TypeVar('T')

def sum_list(numbers: List[int]) -> int:
    """
    Calculate the sum of a list of numbers using recursion.
    
    This is a pure function that recursively sums the elements of a list.
    It demonstrates the classic recursive pattern with a base case and a recursive case.
    
    Args:
        numbers: A list of integers to sum. Can be empty.
        
    Returns:
        int: The sum of all numbers in the list. Returns 0 for an empty list.
        
    Examples:
        >>> sum_list([1, 2, 3, 4])
        10
        >>> sum_list([])
        0
        >>> sum_list([-1, 0, 1])
        0
        
    Note:
        - Time complexity: O(n) where n is the length of the list
        - Space complexity: O(n) due to the call stack
        - Not tail-recursive (Python doesn't optimize tail recursion)
        - For large lists, consider using built-in sum() or an iterative approach
    """
    if not numbers:  # Base case: empty list
        return 0
    return numbers[0] + sum_list(numbers[1:])  # Recursive case

def find_max(numbers: List[int], current_max: int = None) -> int:
    """
    Find the maximum number in a list using recursion.
    
    This is a pure function that recursively finds the maximum value in a list.
    It demonstrates how to maintain state through recursive calls using parameters.
    
    Args:
        numbers: A list of integers to find the maximum from.
        current_max: The current maximum value found (used internally for recursion).
                   Users typically don't need to provide this.
                   
    Returns:
        int: The maximum number in the list.
        
    Raises:
        ValueError: If the input list is empty.
        
    Examples:
        >>> find_max([3, 1, 4, 1, 5, 9])
        9
        >>> find_max([-5, -1, -10])
        -1
        
    Note:
        - Time complexity: O(n) where n is the length of the list
        - Space complexity: O(n) due to the call stack
        - For empty lists, raises ValueError
        - For single-element lists, returns that element
    """
    if not numbers:
        if current_max is None:
            raise ValueError("Cannot find max of empty list")
        return current_max
    
    first = numbers[0]
    if current_max is None or first > current_max:
        return find_max(numbers[1:], first)
    return find_max(numbers[1:], current_max)

def flatten(nested_list: List[Any]) -> List[Any]:
    """
    Flatten an arbitrarily nested list structure into a single-level list.
    
    This is a pure function that recursively processes nested lists and returns
    a new list with all elements in a single level. It handles lists nested to any depth.
    
    Args:
        nested_list: A list that may contain other lists or non-list elements.
                   Can be empty or contain mixed types.
                   
    Returns:
        List[Any]: A new list with all elements from all nested lists in depth-first order.
                 The original nested_list is not modified.
                 
    Examples:
        >>> flatten([1, [2, [3, 4], 5]])
        [1, 2, 3, 4, 5]
        >>> flatten([1, 2, [3, [4, [5]]]])
        [1, 2, 3, 4, 5]
        >>> flatten([[[], []], []])
        []
        >>> flatten([1, 'a', [2, 'b']])
        [1, 'a', 2, 'b']
        
    Note:
        - Handles lists nested to any depth
        - Preserves the order of elements
        - Returns a new list (doesn't modify input)
        - Time complexity: O(n) where n is the total number of elements
        - Space complexity: O(d) where d is the maximum depth of nesting
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def memoize(func: Callable) -> Callable:
    """
    Memoization decorator for pure functions.
    
    This decorator caches the results of function calls based on their arguments,
    so that repeated calls with the same arguments return the cached result instead
    of recomputing. This is particularly useful for optimizing recursive functions
    with overlapping subproblems.
    
    Args:
        func: The pure function to memoize. Should be deterministic (same input
             always produces same output) and have no side effects.
             
    Returns:
        Callable: A new function with the same signature as the input function,
                but with results cached.
                
    Examples:
        >>> @memoize
        ... def fibonacci(n):
        ...     if n <= 1:
        ...         return n
        ...     return fibonacci(n-1) + fibonacci(n-2)
        
        # First call computes the result
        >>> fibonacci(10)
        55
        
        # Subsequent calls with same arguments return cached result
        >>> fibonacci(10)  # Returns immediately
        55
        
    Note:
        - Only works with hashable argument types
        - Consumes memory proportional to the number of unique function calls
        - Not suitable for functions with large or unhashable arguments
        - The cache is stored on the function object itself
    """
    cache = {}
    
    @wraps(func)  # Preserve original function's metadata
    def wrapper(*args, **kwargs):
        # Create a key from function arguments
        # frozenset is used for kwargs to handle unordered dict items
        key = (args, frozenset(kwargs.items()))
        
        # Check if result is already in cache
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            
        return cache[key]
        
    return wrapper

if __name__ == "__main__":
    print("=== Recursive Function Examples ===\n")
    
    # Example 1: Summing a list
    print("1. Summing a list recursively:")
    test_lists = [
        [1, 2, 3, 4, 5],
        [],
        [10],
        list(range(1, 11))  # 1+2+3+...+10 = 55
    ]
    
    for lst in test_lists:
        result = sum_list(lst)
        print(f"sum_list({lst}) = {result}")
    
    # Example 2: Finding maximum value
    print("\n2. Finding maximum value recursively:")
    test_cases = [
        [3, 1, 4, 1, 5, 9, 2, 6],
        [-5, -1, -10],
        [42],
        list(range(100, 0, -1))  # 100 is max
    ]
    
    for case in test_cases:
        result = find_max(case)
        print(f"find_max({case}) = {result}")
    
    # Example 3: Flattening nested lists
    print("\n3. Flattening nested lists:")
    nested_examples = [
        [1, [2, [3, 4], 5]],
        [[], [1], [2, [3]]],
        [1, 2, [3, [4, [5]]]],
        []
    ]
    
    for nested in nested_examples:
        result = flatten(nested)
        print(f"flatten({nested}) = {result}")
    
    # Example 4: Memoization with Fibonacci
    print("\n4. Memoization with Fibonacci sequence:")
    
    @memoize
    def fib(n: int) -> int:
        """Calculate nth Fibonacci number using recursion with memoization."""
        if n <= 1:
            return n
        return fib(n-1) + fib(n-2)
    
    # Print first 20 Fibonacci numbers
    print("First 20 Fibonacci numbers:")
    for i in range(20):
        print(f"fib({i:2d}) = {fib(i):5d}", end="\t")
        if (i + 1) % 4 == 0:  # New line every 4 numbers
            print()
    
    # Performance comparison with and without memoization
    print("\n5. Performance comparison with/without memoization:")
    
    def fib_slow(n: int) -> int:
        """Calculate nth Fibonacci number without memoization."""
        if n <= 1:
            return n
        return fib_slow(n-1) + fib_slow(n-2)
    
    import time
    
    def time_function(func, *args):
        """Time how long a function takes to execute."""
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        return result, end - start
    
    # Test with a moderately large n
    n = 30
    
    print(f"\nCalculating fib({n}) with memoization...")
    result, time_taken = time_function(fib, n)
    print(f"Result: {result}, Time: {time_taken:.6f} seconds")
    
    print(f"\nCalculating fib({n}) without memoization...")
    result, time_taken = time_function(fib_slow, n)
    print(f"Result: {result}, Time: {time_taken:.6f} seconds")
    
    print("\nNote the significant performance difference with memoization!")
    
    # Verify function purity with assertions
    print("\nVerifying function purity with assertions...")
    assert sum_list([]) == 0
    assert sum_list([1, 2, 3]) == 6
    assert find_max([5, 3, 8, 1]) == 8
    assert find_max([-1, -5, -2]) == -1
    assert flatten([1, [2, [3]]]) == [1, 2, 3]
    assert flatten([]) == []
    assert flatten([[[], []], []]) == []
    
    print("\nAll tests passed! All functions are pure and working as expected.")

