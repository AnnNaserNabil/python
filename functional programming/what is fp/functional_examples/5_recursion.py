"""
5. Recursion

Recursion is a technique where a function calls itself in order to solve a problem.
It's a fundamental concept in functional programming.

Key components of recursion:
1. Base case(s): The simplest possible case that can be solved directly
2. Recursive case: Breaking down the problem into smaller subproblems
"""

def factorial(n):
    """
    Calculate factorial using recursion.
    - Base case: factorial(0) = 1
    - Recursive case: n * factorial(n-1)
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return 1 if n == 0 else n * factorial(n - 1)

def fibonacci(n):
    """
    Calculate nth Fibonacci number using recursion.
    - Base cases: fib(0) = 0, fib(1) = 1
    - Recursive case: fib(n) = fib(n-1) + fib(n-2)
    """
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)

def sum_list(numbers):
    """
    Calculate the sum of a list of numbers using recursion.
    - Base case: sum([]) = 0
    - Recursive case: first + sum(rest)
    """
    return 0 if not numbers else numbers[0] + sum_list(numbers[1:])

def reverse_string(s):
    """
    Reverse a string using recursion.
    - Base case: reverse("") = ""
    - Recursive case: reverse(rest) + first_char
    """
    return s if len(s) <= 1 else reverse_string(s[1:]) + s[0]

def count_down(n):
    """
    Count down from n to 1 using recursion.
    - Base case: n == 0 (stop)
    - Recursive case: print n, then count_down(n-1)
    """
    if n > 0:
        print(n)
        count_down(n - 1)
    else:
        print("Blast off!")

# Tail recursion optimized version of factorial
def factorial_tail(n, accumulator=1):
    """
    Tail-recursive factorial function.
    - Uses an accumulator to avoid stack growth
    - Some languages can optimize this to use constant stack space
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return accumulator if n == 0 else factorial_tail(n - 1, n * accumulator)

# Testing the recursive functions
if __name__ == "__main__":
    print("Factorial:")
    for i in range(6):
        print(f"{i}! = {factorial(i)}")
    
    print("\nFibonacci:")
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
    
    print("\nSum of list:")
    numbers = [1, 2, 3, 4, 5]
    print(f"sum({numbers}) = {sum_list(numbers)}")
    
    print("\nReverse string:")
    s = "hello"
    print(f"reverse('{s}') = '{reverse_string(s)}'")
    
    print("\nCount down:")
    count_down(5)
    
    print("\nTail-recursive factorial:")
    print(f"5! = {factorial_tail(5)}")
    
    # Note: Python doesn't optimize tail recursion by default, so this will still
    # hit the recursion limit for large n. This is just to demonstrate the concept.
