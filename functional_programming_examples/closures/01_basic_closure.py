"""
1. Basic Closure in Python

This module introduces the fundamental concept of closures in Python.

What is a Closure?
-----------------
A closure is a function object that remembers values in enclosing scopes even 
if they are not present in memory. It's like a "function factory" that 
remembers the environment in which it was created.

Key Concepts:
------------
1. Nested Functions: Functions defined inside other functions
2. Non-local Variables: Variables from the outer function that the inner function can access
3. Function Factories: Functions that create and return other functions

Why Use Closures?
---------------
- Data Hiding: Keep variables private to specific functions
- Function Factories: Create specialized functions from more general ones
- Decorators: Implement Python decorators
- Callbacks: Create callback functions with access to their environment

Real-world Applications:
-----------------------
- Decorators (@decorator syntax in Python)
- Callback functions in GUIs and event-driven programming
- Creating function factories
- Implementing private variables in classes

Example:
-------
>>> def make_multiplier(factor):
...     def multiplier(x):
...         return x * factor
...     return multiplier
>>> double = make_multiplier(2)
>>> double(5)  # Returns 10
"""
from __future__ import annotations
from typing import Callable

def outer_function(msg: str) -> Callable[[], None]:
    """
    Create a closure that remembers the message passed to the outer function.
    
    This is a classic example of a closure where the inner function 'remembers'
    the environment in which it was created, including the 'msg' variable.
    
    Args:
        msg (str): A message that will be remembered by the inner function
        
    Returns:
        Callable[[], None]: A function that when called will print the remembered message
        
    Example:
        >>> greet = outer_function("Hello, World!")
        >>> greet()  # Prints: Message from outer function: Hello, World!
        
    How It Works:
    1. When outer_function is called with a message, it defines inner_function
    2. inner_function has access to 'msg' from the outer scope
    3. outer_function returns inner_function
    4. The returned function still has access to 'msg' even after outer_function has finished executing
    """
    def inner_function() -> None:
        """Inner function that has access to 'msg' from the enclosing scope."""
        print(f"Message from outer function: {msg}")
    
    return inner_function

def demonstrate_basic_closure() -> None:
    """Demonstrate the basic closure functionality."""
    # Create a closure by calling the outer function
    my_closure = outer_function("Hello, Closure!")
    
    # The inner function still has access to 'msg' even though outer_function has finished executing
    my_closure()
    
    # Another closure with a different message
    another_closure = outer_function("This is another message")
    another_closure()
    
    # Show that each closure maintains its own state
    print("\nCalling both closures again:")
    my_closure()
    another_closure()

if __name__ == "__main__":
    print("=== Basic Closure Example ===")
    demonstrate_basic_closure()
    
    print("\n=== Key Takeaways ===")
    print("1. A closure is a function that remembers values from its enclosing lexical scope")
    print("2. The inner function has access to variables from the outer function's scope")
    print("3. Each closure maintains its own state independently")
    print("4. The outer function's variables are 'remembered' even after it has finished executing")
