"""
4. Dictionary Operations with Pure Functions

This module demonstrates pure functions for common dictionary operations in Python.
These functions follow functional programming principles by:
1. Not modifying the input dictionaries (immutability)
2. Returning new dictionaries instead of mutating the original
3. Having no side effects
4. Being deterministic (same input always produces same output)

Key Concepts:
------------
- Immutability: Original dictionaries remain unchanged
- Function Purity: No side effects, only depends on inputs
- Dictionary Comprehensions: Pythonic way to create new dictionaries
- Type Safety: Uses Python's type hints for better code clarity

Why Use Pure Functions for Dictionary Operations?
-----------------------------------------------
- Predictable behavior and easier debugging
- Thread-safe by design
- Enable function composition and chaining
- Make code more maintainable and testable
- Prevent accidental modifications to input data

Real-world Applications:
----------------------
- Data transformation and processing
- Configuration management
- API response handling
- Data validation and cleaning
- Feature extraction in machine learning

Example:
-------
>>> data = {'a': 1, 'b': 2, 'c': 3}
>>> filter_dict(data, lambda k, v: v % 2 == 0)
{'b': 2}
>>> map_dict(data, lambda k, v: v * 2)
{'a': 2, 'b': 4, 'c': 6}
>>> merge_dicts({'a': 1}, {'b': 2}, {'c': 3})
{'a': 1, 'b': 2, 'c': 3}
"""
from typing import Dict, Any, TypeVar, Callable, List

K = TypeVar('K')
V = TypeVar('V')

def filter_dict(d: Dict[K, V], predicate: Callable[[K, V], bool]) -> Dict[K, V]:
    """
    Filter a dictionary based on a predicate function.
    
    This is a pure function that creates a new dictionary containing only the
    key-value pairs for which the predicate function returns True.
    The original dictionary remains unchanged.
    
    Args:
        d: The input dictionary to be filtered.
           Can contain any key-value pairs where keys are hashable.
        predicate: A function that takes a key and value as arguments
                 and returns a boolean. If True, the key-value pair is included
                 in the result.
                 
    Returns:
        Dict[K, V]: A new dictionary containing only the key-value pairs
                   that satisfy the predicate.
                   
    Examples:
        >>> data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        >>> filter_dict(data, lambda k, v: v % 2 == 0)
        {'b': 2, 'd': 4}
        >>> filter_dict(data, lambda k, v: k in ['a', 'c'])
        {'a': 1, 'c': 3}
        >>> filter_dict({}, lambda k, v: True)  # Empty dict returns empty dict
        {}
        
    Note:
        - Returns a new dictionary (original is not modified)
        - The order of items is preserved (Python 3.7+)
        - The predicate function should be pure for predictable results
        - If the input is empty, returns an empty dictionary
        
    Raises:
        TypeError: If the input is not a dictionary
    """
    if not isinstance(d, dict):
        raise TypeError(f"Expected a dictionary, got {type(d).__name__}")
    return {k: v for k, v in d.items() if predicate(k, v)}

def map_dict(d: Dict[K, V], func: Callable[[K, V], Any]) -> Dict[K, Any]:
    """
    Apply a transformation function to each value in a dictionary.
    
    This is a pure function that creates a new dictionary where each value is the
    result of applying the transformation function to the corresponding key-value
    pair in the original dictionary. The original dictionary remains unchanged.
    
    Args:
        d: The input dictionary to be transformed.
           Can contain any key-value pairs where keys are hashable.
        func: A function that takes a key and value as arguments
             and returns the new value for that key.
             
    Returns:
        Dict[K, Any]: A new dictionary with the same keys but transformed values.
                     The type of values may change based on the transformation function.
                     
    Examples:
        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> map_dict(data, lambda k, v: v * 2)
        {'a': 2, 'b': 4, 'c': 6}
        >>> map_dict(data, lambda k, v: f"{k.upper()}:{v}")
        {'a': 'A:1', 'b': 'B:2', 'c': 'C:3'}
        >>> map_dict({}, lambda k, v: v)  # Empty dict returns empty dict
        {}
        
    Note:
        - Returns a new dictionary (original is not modified)
        - The order of items is preserved (Python 3.7+)
        - The function should be pure for predictable results
        - Keys remain unchanged in the result
        - Type hints use Any for the return value since the transformation
          function can return any type
    """
    if not isinstance(d, dict):
        raise TypeError(f"Expected a dictionary, got {type(d).__name__}")
    return {k: func(k, v) for k, v in d.items()}

def merge_dicts(*dicts: Dict[K, V]) -> Dict[K, V]:
    """
    Merge multiple dictionaries into a single dictionary.
    
    This is a pure function that creates a new dictionary containing all key-value
    pairs from the input dictionaries. If the same key appears in multiple
    dictionaries, the value from the last dictionary containing that key is used.
    The original dictionaries remain unchanged.
    
    Args:
        *dicts: Any number of dictionaries to merge. Can be zero or more.
              All dictionaries must have the same key and value types.
              
    Returns:
        Dict[K, V]: A new dictionary containing all key-value pairs from all
                   input dictionaries, with later values taking precedence.
                   
    Examples:
        >>> dict1 = {'a': 1, 'b': 2}
        >>> dict2 = {'b': 3, 'c': 4}
        >>> merge_dicts(dict1, dict2)
        {'a': 1, 'b': 3, 'c': 4}
        >>> merge_dicts(dict1, {}, {'a': 5})  # Empty dicts are handled
        {'a': 5, 'b': 2}
        >>> merge_dicts()  # No arguments returns empty dict
        {}
        
    Note:
        - Returns a new dictionary (originals are not modified)
        - The order of items is preserved (Python 3.7+), with later
          dictionaries' items appearing after earlier ones
        - If no dictionaries are provided, returns an empty dictionary
        - All dictionaries should have the same key and value types for type safety
          (though Python won't enforce this at runtime)
    """
    result: Dict[K, V] = {}
    for d in dicts:
        if not isinstance(d, dict):
            raise TypeError(f"All arguments must be dictionaries, got {type(d).__name__}")
        result.update(d)
    return result

if __name__ == "__main__":
    print("=== Dictionary Operations with Pure Functions ===\n")
    
    # Example 1: Filtering dictionary items
    print("1. Filtering a dictionary:")
    student_scores = {
        'Alice': 85,
        'Bob': 90,
        'Charlie': 78,
        'David': 92,
        'Eve': 88
    }
    print(f"Original scores: {student_scores}")
    
    # Get only students who scored 90 or above
    high_achievers = filter_dict(student_scores, lambda name, score: score >= 90)
    print(f"High achievers (>=90): {high_achievers}")
    
    # Get only students whose names start with 'A' or 'B'
    ab_students = filter_dict(student_scores, lambda name, _: name[0] in 'AB')
    print(f"Students with names starting with A or B: {ab_students}")
    
    # Example 2: Transforming dictionary values
    print("\n2. Transforming dictionary values:")
    
    # Add 5 points to each score (capped at 100)
    adjusted_scores = map_dict(student_scores, lambda name, score: min(score + 5, 100))
    print(f"Adjusted scores (+5 points, max 100): {adjusted_scores}")
    
    # Create a summary string for each student
    student_summaries = map_dict(
        student_scores,
        lambda name, score: f"{name}: {'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'F'}"
    )
    print(f"Student summaries: {student_summaries}")
    
    # Example 3: Merging dictionaries
    print("\n3. Merging multiple dictionaries:")
    
    # Default configuration
    default_config = {
        'theme': 'light',
        'notifications': True,
        'items_per_page': 10
    }
    
    # User preferences
    user_prefs = {
        'theme': 'dark',  # Override default
        'language': 'en', # New setting
        'items_per_page': 25  # Override default
    }
    
    # Environment-specific settings
    env_settings = {
        'api_url': 'https://api.example.com',
        'debug': False
    }
    
    # Merge all configurations (later dictionaries take precedence)
    config = merge_dicts(default_config, user_prefs, env_settings)
    print(f"Merged configuration: {config}")
    
    # Verify immutability of inputs
    assert len(default_config) == 3, "Original dictionary should not be modified"
    assert len(user_prefs) == 3, "Original dictionary should not be modified"
    
    # Test with empty dictionaries
    empty_merge = merge_dicts({}, {}, {})
    assert empty_merge == {}, "Merging empty dictionaries should return an empty dictionary"
    
    print("\nAll tests passed! All dictionary operations are pure and working as expected.")
