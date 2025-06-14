"""
1. Basic Recursion

Introduction to recursive functions in Python.
- Factorial calculation
- Fibonacci sequence
- Sum of digits
- String reversal
- List sum
"""
from typing import List, Any, Optional
from functools import lru_cache

# 1. Factorial
def factorial(n: int) -> int:
    """Calculate factorial using recursion."""
    # Base case
    if n == 0 or n == 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)

# 2. Fibonacci sequence
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number using recursion."""
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1
    # Recursive case
    return fibonacci(n - 1) + fibonacci(n - 2)

# 3. Sum of digits
def sum_digits(n: int) -> int:
    """Calculate the sum of digits of a number using recursion."""
    # Base case: single digit
    if n < 10:
        return n
    # Recursive case: last digit + sum of other digits
    return n % 10 + sum_digits(n // 10)

# 4. String reversal
def reverse_string(s: str) -> str:
    """Reverse a string using recursion."""
    # Base case: empty string or single character
    if len(s) <= 1:
        return s
    # Recursive case: last character + reverse of the rest
    return s[-1] + reverse_string(s[:-1])

# 5. List sum
def list_sum(numbers: List[float]) -> float:
    """Calculate the sum of a list of numbers using recursion."""
    # Base case: empty list
    if not numbers:
        return 0
    # Recursive case: first element + sum of the rest
    return numbers[0] + list_sum(numbers[1:])

def demonstrate_basic_recursion() -> None:
    """Demonstrate basic recursive functions."""
    print("=== Factorial ===")
    for i in range(6):
        print(f"{i}! = {factorial(i)}")
    
    print("\n=== Fibonacci ===")
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
    
    print("\n=== Sum of Digits ===")
    numbers = [123, 456, 7890, 12345]
    for num in numbers:
        print(f"Sum of digits in {num} = {sum_digits(num)}")
    
    print("\n=== String Reversal ===")
    strings = ["hello", "recursion", "python", ""]
    for s in strings:
        print(f"Reverse of '{s}' is '{reverse_string(s)}'")
    
    print("\n=== List Sum ===")
    test_lists = [
        [1, 2, 3, 4, 5],
        [10.5, 20.5, 30.5],
        [],
        [7]
    ]
    for lst in test_lists:
        print(f"Sum of {lst} = {list_sum(lst)}")

if __name__ == "__main__":
    demonstrate_basic_recursion()
    
    print("\n=== Key Takeaways ===")
    print("1. Every recursive function needs a base case to stop the recursion")
    print("2. The recursive case should move toward the base case")
    print("3. Python has a default recursion limit (usually 1000)")
    print("4. Some problems are naturally recursive (trees, graphs, etc.)")
    print("5. Recursion can be less efficient than iteration due to function call overhead")
