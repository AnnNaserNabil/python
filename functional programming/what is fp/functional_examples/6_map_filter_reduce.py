"""
6. Map, Filter, and Reduce

These are three higher-order functions that operate on sequences (like lists).
They are fundamental tools in functional programming.
"""

from functools import reduce
from typing import Callable, TypeVar, List, Any, Iterable

T = TypeVar('T')
R = TypeVar('R')

def my_map(func: Callable[[T], R], iterable: Iterable[T]) -> List[R]:
    """
    Custom implementation of map.
    Applies func to each element in iterable and returns a new list.
    """
    return [func(x) for x in iterable]

def my_filter(func: Callable[[T], bool], iterable: Iterable[T]) -> List[T]:
    """
    Custom implementation of filter.
    Returns a list of elements for which func returns True.
    """
    return [x for x in iterable if func(x)]

def my_reduce(func: Callable[[R, T], R], iterable: Iterable[T], initial: R = None) -> R:
    """
    Custom implementation of reduce.
    Applies func cumulatively to the items of iterable, from left to right.
    """
    it = iter(iterable)
    if initial is None:
        try:
            initial = next(it)
        except StopIteration:
            raise TypeError("reduce() of empty sequence with no initial value") from None
    
    result = initial
    for x in it:
        result = func(result, x)
    return result

# Example functions to use with map, filter, reduce
def square(x: int) -> int:
    return x ** 2

def is_even(x: int) -> bool:
    return x % 2 == 0

def add(a: int, b: int) -> int:
    return a + b

def multiply(a: int, b: int) -> int:
    return a * b

def string_to_uppercase(s: str) -> str:
    return s.upper()

def is_vowel(c: str) -> bool:
    return c.lower() in 'aeiou'

def concatenate(a: str, b: str) -> str:
    return a + b

# Testing the functions
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    words = ["hello", "world", "python", "functional", "programming"]
    
    # Using built-in map, filter, reduce
    print("Using built-in functions:")
    
    # Map examples
    squares = list(map(square, numbers))
    print(f"Squares: {squares}")
    
    uppercase_words = list(map(string_to_uppercase, words))
    print(f"Uppercase words: {uppercase_words}")
    
    # Filter examples
    evens = list(filter(is_even, numbers))
    print(f"Even numbers: {evens}")
    
    vowels_in_words = [list(filter(is_vowel, word)) for word in words]
    print(f"Vowels in words: {vowels_in_words}")
    
    # Reduce examples
    sum_total = reduce(add, numbers)
    print(f"Sum of numbers: {sum_total}")
    
    product = reduce(multiply, numbers)
    print(f"Product of numbers: {product}")
    
    concatenated = reduce(concatenate, words)
    print(f"Concatenated words: {concatenated}")
    
    # Using our custom implementations
    print("\nUsing our custom implementations:")
    
    squares_custom = my_map(square, numbers)
    print(f"Squares (custom): {squares_custom}")
    
    evens_custom = my_filter(is_even, numbers)
    print(f"Even numbers (custom): {evens_custom}")
    
    sum_custom = my_reduce(add, numbers, 0)
    print(f"Sum of numbers (custom): {sum_custom}")
    
    # More complex examples
    print("\nMore complex examples:")
    
    # Sum of squares of even numbers
    result = reduce(
        add,
        filter(
            lambda x: x > 0,
            map(
                lambda x: x ** 2 if x % 2 == 0 else 0,
                numbers
            )
        ),
        0
    )
    print(f"Sum of squares of even numbers: {result}")
    
    # Count vowels in all words
    total_vowels = reduce(
        add,
        map(
            lambda word: len(list(filter(is_vowel, word))),
            words
        ),
        0
    )
    print(f"Total vowels in all words: {total_vowels}")
    
    # Using list comprehensions (more Pythonic alternative to map/filter)
    print("\nUsing list comprehensions (Pythonic alternative):")
    
    squares_comp = [x ** 2 for x in numbers]
    print(f"Squares (list comp): {squares_comp}")
    
    evens_comp = [x for x in numbers if x % 2 == 0]
    print(f"Even numbers (list comp): {evens_comp}")
    
    # Sum of squares of even numbers using generator expression
    sum_sq_evens = sum(x ** 2 for x in numbers if x % 2 == 0)
    print(f"Sum of squares of even numbers (gen expr): {sum_sq_evens}")
