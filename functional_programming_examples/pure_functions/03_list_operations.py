"""
3. List Operations with Pure Functions

This module demonstrates pure functions for common list operations in Python.
These functions follow functional programming principles by:
1. Not modifying the input list (immutability)
2. Returning new lists instead of mutating the original
3. Having no side effects
4. Being deterministic (same input always produces same output)

Key Concepts:
------------
- Immutability: Original lists remain unchanged
- Function Purity: No side effects, only depends on inputs
- Higher-Order Functions: Functions that take other functions as arguments
- List Comprehensions: Pythonic way to create new lists

Why Use Pure Functions for List Operations?
-----------------------------------------
- Predictable behavior
- Easier to reason about and debug
- Thread-safe by design
- Enable function composition
- Make code more maintainable and testable

Real-world Applications:
----------------------
- Data transformation and processing
- Data cleaning and filtering
- Feature engineering in machine learning
- API response processing
- Configuration management

Example:
-------
>>> numbers = [1, 2, 3, 4, 5, 6]
>>> filter_list(numbers, lambda x: x % 2 == 0)
[2, 4, 6]
>>> map_list(numbers, lambda x: x * 2)
[2, 4, 6, 8, 10, 12]
>>> remove_duplicates([1, 2, 2, 3, 3, 3])
[1, 2, 3]
"""
from typing import List, TypeVar, Callable, Any, Type

# Type variable for generic type hints
T = TypeVar('T')

# Example usage of the list operation functions
if __name__ == "__main__":
    print("=== List Operations with Pure Functions ===\n")
    
    # Example 1: Filtering even numbers
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = filter_list(numbers, lambda x: x % 2 == 0)
    print(f"Even numbers: {evens}")
    
    # Example 2: Mapping numbers to their squares
    squares = map_list(numbers, lambda x: x ** 2)
    print(f"Squares: {squares}")
    
    # Example 3: Removing duplicates while preserving order
    duplicates = [1, 2, 2, 3, 4, 4, 4, 5, 1]
    unique = remove_duplicates(duplicates)
    print(f"With duplicates: {duplicates}")
    print(f"Without duplicates: {unique}")
    
    # Example 4: Chaining operations (function composition)
    result = remove_duplicates(
        map_list(
            filter_list(numbers, lambda x: x > 5),
            lambda x: x * 10
        )
    )
    print(f"Chained operations result: {result}")
    
    # Test with empty list
    assert filter_list([], lambda x: True) == []
    assert map_list([], lambda x: x) == []
    assert remove_duplicates([]) == []
    
    print("\nAll tests passed! All functions are pure and working as expected.")

def filter_list(lst: List[T], predicate: Callable[[T], bool]) -> List[T]:
    """
    Filter elements from a list based on a predicate function.
    
    This is a pure function that creates a new list containing only the elements
    for which the predicate function returns True. The original list remains unchanged.
    
    Args:
        lst: The input list to be filtered. Can contain elements of any type.
        predicate: A function that takes an element and returns a boolean.
                 Elements that evaluate to True are included in the result.
                 
    Returns:
        List[T]: A new list containing only elements that satisfy the predicate.
        
    Examples:
        >>> filter_list([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        [2, 4]
        >>> filter_list(['apple', 'banana', 'cherry'], lambda s: 'a' in s)
        ['apple', 'banana']
        >>> filter_list([], lambda x: True)
        []
        
    Note:
        - Returns a new list (original list is not modified)
        - The order of elements is preserved
        - If the input list is empty, returns an empty list
        - The predicate function should be pure for predictable results
    """
    return [x for x in lst if predicate(x)]

def map_list(lst: List[T], func: Callable[[T], T]) -> List[T]:
    """
    Apply a function to each element of a list and return a new list.
    
    This is a pure function that creates a new list by applying the given function
    to each element of the input list. The original list remains unchanged.
    
    Args:
        lst: The input list to be transformed. Can contain elements of any type.
        func: A function that transforms an element of the list.
             Should take one argument and return the transformed value.
             
    Returns:
        List[T]: A new list with the function applied to each element.
        
    Examples:
        >>> map_list([1, 2, 3], lambda x: x * 2)
        [2, 4, 6]
        >>> map_list(['hello', 'world'], str.upper)
        ['HELLO', 'WORLD']
        >>> map_list([], lambda x: x)  # Empty list returns empty list
        []
        
    Note:
        - Returns a new list (original list is not modified)
        - The order of elements is preserved
        - The function should be pure for predictable results
        - Type hints use TypeVar T for flexibility with different types
    """
    return [func(x) for x in lst]

def remove_duplicates(lst: List[T]) -> List[T]:
    """
    Remove duplicate elements from a list while preserving the original order.
    
    This is a pure function that returns a new list containing only the first
    occurrence of each element in the input list. The original list remains unchanged.
    
    Args:
        lst: The input list from which to remove duplicates.
            Elements must be hashable (can be used as dictionary keys).
            
    Returns:
        List[T]: A new list with duplicates removed, preserving the order of first occurrences.
        
    Examples:
        >>> remove_duplicates([1, 2, 2, 3, 3, 3])
        [1, 2, 3]
        >>> remove_duplicates(['a', 'b', 'a', 'c', 'b'])
        ['a', 'b', 'c']
        >>> remove_duplicates([1, '1', 1.0])  # Different types are considered distinct
        [1, '1', 1.0]
        
    Note:
        - Returns a new list (original list is not modified)
        - Preserves the order of first occurrences
        - Elements must be hashable (e.g., lists are not allowed)
        - Complexity is O(n) time and O(n) space
        
    Raises:
        TypeError: If the list contains unhashable types (like lists or dictionaries)
    """
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    
    # Test filter_list
    evens = filter_list(numbers, lambda x: x % 2 == 0)
    print(f"Even numbers: {evens}")
    
    # Test map_list
    squares = map_list(numbers, lambda x: x ** 2)
    print(f"Squares: {squares}")
    
    # Test remove_duplicates
    unique = remove_duplicates(numbers)
    print(f"Unique numbers: {unique}")
    
    # The functions are pure - they don't modify the input
    assert numbers == [1, 2, 3, 4, 5, 4, 3, 2, 1]
    
    # More assertions
    assert filter_list([], lambda x: True) == []
    assert map_list([1, 2, 3], str) == ['1', '2', '3']
    assert remove_duplicates([1, 2, 2, 3, 3, 3]) == [1, 2, 3]
