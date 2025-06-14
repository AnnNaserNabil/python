"""
1. Map, Filter, and Reduce Basics

Introduces the fundamental concepts of map, filter, and reduce operations
with simple examples and explanations.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Iterable, Any, List, Dict, Tuple
from functools import reduce
import operator

T = TypeVar('T')
U = TypeVar('U')

# 1. Map Basics

def demonstrate_map() -> None:
    """Basic usage of the map function."""
    print("=== Map Basics ===\n")
    
    # Map applies a function to each item in an iterable
    numbers = [1, 2, 3, 4, 5]
    
    # Double each number
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"Doubled numbers: {doubled}")
    
    # Convert numbers to strings
    strings = list(map(str, numbers))
    print(f"As strings: {strings}")
    
    # Using map with a named function
    def square(x: int) -> int:
        return x ** 2
    
    squares = list(map(square, numbers))
    print(f"Squares: {squares}")
    
    # Map with multiple iterables
    a = [1, 2, 3]
    b = [4, 5, 6]
    sums = list(map(lambda x, y: x + y, a, b))
    print(f"Sums of {a} and {b}: {sums}")

# 2. Filter Basics

def demonstrate_filter() -> None:
    """Basic usage of the filter function."""
    print("\n=== Filter Basics ===\n")
    
    # Filter keeps elements where the function returns True
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Get even numbers
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Even numbers: {evens}")
    
    # Using filter with None to remove falsy values
    values = [0, 1, "", "hello", None, [], [1, 2], False, True]
    truthy = list(filter(None, values))
    print(f"Truthy values: {truthy}")
    
    # Using a named function
    def is_vowel(char: str) -> bool:
        return char.lower() in 'aeiou'
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    vowels = list(filter(is_vowel, letters))
    print(f"Vowels: {vowels}")

# 3. Reduce Basics

def demonstrate_reduce() -> None:
    """Basic usage of the reduce function."""
    print("\n=== Reduce Basics ===\n")
    
    # Reduce applies a function cumulatively to items of an iterable
    numbers = [1, 2, 3, 4, 5]
    
    # Sum of all numbers
    total = reduce(lambda x, y: x + y, numbers)
    print(f"Sum of {numbers}: {total}")
    
    # Product of all numbers
    product = reduce(lambda x, y: x * y, numbers)
    print(f"Product of {numbers}: {product}")
    
    # Using operator functions for common operations
    from operator import add, mul
    
    sum_operator = reduce(add, numbers)
    print(f"Sum using operator.add: {sum_operator}")
    
    product_operator = reduce(mul, numbers)
    print(f"Product using operator.mul: {product_operator}")
    
    # With an initial value
    sum_with_initial = reduce(add, numbers, 10)
    print(f"Sum with initial 10: {sum_with_initial}")

# 4. Combining Map, Filter, and Reduce

def demonstrate_combination() -> None:
    """Combining map, filter, and reduce."""
    print("\n=== Combining Map, Filter, and Reduce ===\n")
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Calculate the sum of squares of even numbers
    # Step 1: Filter even numbers
    evens = filter(lambda x: x % 2 == 0, numbers)
    
    # Step 2: Square each even number
    squares = map(lambda x: x ** 2, evens)
    
    # Step 3: Sum the squares
    result = reduce(lambda x, y: x + y, squares)
    
    print(f"Sum of squares of evens in {numbers}: {result}")
    
    # All in one line
    result = reduce(
        lambda x, y: x + y,
        map(
            lambda x: x ** 2,
            filter(lambda x: x % 2 == 0, numbers)
        )
    )
    print(f"Same result in one line: {result}")

# 5. Practical Example: Word Count

def word_count_example() -> None:
    """A practical example: counting word frequencies in a text."""
    print("\n=== Word Count Example ===\n")
    
    text = """
    Python is an interpreted high-level programming language.
    Python's design philosophy emphasizes code readability.
    Python is dynamically typed and garbage-collected.
    Python supports multiple programming paradigms.
    """
    
    # Convert to lowercase and split into words
    words = text.lower().split()
    
    # Remove punctuation from words
    import string
    words = [word.strip(string.punctuation) for word in words]
    
    # Count word frequencies using reduce
    def update_counts(counts: Dict[str, int], word: str) -> Dict[str, int]:
        counts[word] = counts.get(word, 0) + 1
        return counts
    
    word_counts = reduce(update_counts, words, {})
    
    # Sort by frequency (descending)
    sorted_counts = sorted(
        word_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )
    
    print("Word frequencies:")
    for word, count in sorted_counts:
        print(f"  {word}: {count}")

if __name__ == "__main__":
    print("=== Map, Filter, and Reduce Basics ===\n")
    
    demonstrate_map()
    demonstrate_filter()
    demonstrate_reduce()
    demonstrate_combination()
    word_count_example()
    
    print("\n=== Key Takeaways ===")
    print("1. map() applies a function to every item in an iterable")
    print("2. filter() selects items where a function returns True")
    print("3. reduce() cumulatively applies a function to reduce an iterable to a single value")
    print("4. These functions can be combined to create powerful data processing pipelines")
