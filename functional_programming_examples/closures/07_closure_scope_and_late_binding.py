"""
7. Understanding Closure Scope and Late Binding in Python

This module explores how variable scoping and late binding work with closures,
highlighting common pitfalls and demonstrating solutions. Understanding these
concepts is crucial for writing correct and maintainable code with closures.

Key Concepts:
------------
1. Variable Scope: Where variables are accessible in your code
2. Late Binding: How Python looks up variables at runtime, not when the function is defined
3. Common Pitfalls: Issues that can occur with closures in loops and comprehensions
4. Solutions: Patterns to avoid these issues

Why Understand Closure Scope?
--------------------------
- Avoid subtle bugs in your code
- Write more predictable and maintainable closures
- Understand Python's execution model better
- Debug closure-related issues effectively

Real-world Applications:
----------------------
- Event handlers in GUIs
- Callback functions
- Function factories
- Decorators

Example of the Issue:
-------------------
>>> funcs = []
>>> for i in range(3):
...     def func():
...         return i
...     funcs.append(func)
>>> [f() for f in funcs]  # Might expect [0, 1, 2], but gets [2, 2, 2]
[2, 2, 2]
"""
from __future__ import annotations
from typing import List, Callable, Any
import time

def demonstrate_scope_issue() -> List[Callable[[], int]]:
    """
    Demonstrate the late binding closure issue in Python.
    
    This function shows what happens when you create multiple closures
    in a loop without properly capturing the loop variable's value.
    
    Returns:
        List[Callable[[], int]]: A list of functions that all return the same value
        
    Example:
        >>> funcs = demonstrate_scope_issue()
        >>> [f() for f in funcs]  # All return 2, not 0, 1, 2
        [2, 2, 2]
        
    Note:
        This happens because Python's closures are late-binding - they remember
        the variable name, not the value when the function was created.
    """
    functions = []
    
    for i in range(3):
        def func() -> int:
            return i  # This will always refer to the final value of i
        
        functions.append(func)
    
    return functions

def fix_scope_issue_1() -> List[Callable[[], int]]:
    """
    Fix the scope issue using default arguments.
    
    This solution captures the current value of the loop variable by using
    it as a default argument, which is evaluated when the function is defined.
    
    Returns:
        List[Callable[[], int]]: A list of functions that return 0, 1, 2 respectively
        
    Example:
        >>> funcs = fix_scope_issue_1()
        >>> [f() for f in funcs]  # Returns [0, 1, 2] as expected
        [0, 1, 2]
        
    Note:
        Default arguments are evaluated at function definition time, not call time,
        which is why this works to capture the current value of i.
    """
    functions = []
    
    for i in range(3):
        def func(x: int = i) -> int:  # Capture current value of i
            return x
        
        functions.append(func)
    
    return functions

def fix_scope_issue_2() -> List[Callable[[], int]]:
    """
    Fix the scope issue using a factory function.
    
    This solution creates a new scope for each iteration by using a factory
    function, which captures the current value of the loop variable in a new
    closure each time it's called.
    
    Returns:
        List[Callable[[], int]]: A list of functions that return 0, 1, 2 respectively
        
    Example:
        >>> funcs = fix_scope_issue_2()
        >>> [f() for f in funcs]  # Returns [0, 1, 2] as expected
        [0, 1, 2]
        
    Note:
        This pattern is more explicit and works in more cases than the default
        argument approach, especially when you need to capture multiple variables.
    """
    def make_func(x: int) -> Callable[[], int]:
        def func() -> int:
            return x  # x is bound when make_func is called
        return func
    
    functions = []
    for i in range(3):
        functions.append(make_func(i))
    
    return functions

def demonstrate_late_binding() -> None:
    """
    Demonstrate how late binding affects closure behavior.
    
    This function shows how variables in closures are looked up at call time,
    not when the function is defined, which can lead to unexpected results
    if you're not careful with variable scoping.
    
    The example creates several functions in a loop and shows how they all
    end up referring to the same variable, which has its final value from
    the loop.
    """
    print("=== Late Binding Issue ===")
    funcs1 = demonstrate_scope_issue()
    print("All functions return the same value (last value of i):")
    for i, func in enumerate(funcs1):
        print(f"funcs1[{i}]() = {func()}")
    
    print("\n=== Fix 1: Using Default Arguments ===")
    funcs2 = fix_scope_issue_1()
    print("Each function captures its own value:")
    for i, func in enumerate(funcs2):
        print(f"funcs2[{i}]() = {func()}")
    
    print("\n=== Fix 2: Using a Factory Function ===")
    funcs3 = fix_scope_issue_2()
    print("Each function captures its own value:")
    for i, func in enumerate(funcs3):
        print(f"funcs3[{i}]() = {func()}")

def demonstrate_closure_with_loops() -> None:
    """Demonstrate closure behavior with loops."""
    print("\n=== Closures in Loops ===")
    
    # Problematic example
    callbacks = []
    for i in range(3):
        callbacks.append(lambda: f"Value: {i}")
    
    print("Problematic loop (all show last value):")
    for cb in callbacks:
        print(cb())  # All print "Value: 2"
    
    # Fixed with default argument
    callbacks = []
    for i in range(3):
        callbacks.append(lambda i=i: f"Value: {i}")
    
    print("\nFixed with default argument:")
    for cb in callbacks:
        print(cb())

def demonstrate_closure_with_comprehensions() -> None:
    """Demonstrate closure behavior with comprehensions."""
    print("\n=== Closures in List Comprehensions ===")
    
    # Problematic example
    funcs = [lambda: i for i in range(3)]
    print("Problematic list comprehension (all show last value):")
    for f in funcs:
        print(f())  # All print 2
    
    # Fixed with default argument
    funcs = [lambda i=i: i for i in range(3)]
    print("\nFixed with default argument:")
    for f in funcs:
        print(f())

def demonstrate_closure_with_timeouts() -> None:
    """Demonstrate closure issues with delayed execution."""
    print("\n=== Closures with Delayed Execution ===")
    
    def create_callbacks() -> List[Callable[[], int]]:
        callbacks = []
        for i in range(3):
            def callback() -> int:
                print(f"Callback called with i = {i}")
                return i
            callbacks.append(callback)
        return callbacks
    
    print("Callbacks with late binding (all show last value):")
    for cb in create_callbacks():
        print(f"Result: {cb()}")
    
    def create_fixed_callbacks() -> List[Callable[[], int]]:
        callbacks = []
        for i in range(3):
            def make_callback(x: int) -> Callable[[], int]:
                def callback() -> int:
                    print(f"Fixed callback called with x = {x}")
                    return x
                return callback
            callbacks.append(make_callback(i))
        return callbacks
    
    print("\nFixed callbacks (each captures its own value):")
    for cb in create_fixed_callbacks():
        print(f"Result: {cb()}")

if __name__ == "__main__":
    print("=== Closure Scope and Late Binding ===")
    demonstrate_late_binding()
    demonstrate_closure_with_loops()
    demonstrate_closure_with_comprehensions()
    demonstrate_closure_with_timeouts()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures in Python have late binding - they remember the variable name, not the value")
    print("2. In loops, all closures will see the final value of the loop variable")
    print("3. Common fixes include using default arguments or factory functions")
    print("4. List comprehensions have the same scoping rules as regular loops")
    print("5. Be careful with delayed execution (e.g., timeouts, event handlers)")
    print("6. Always test closures with the actual values they'll be called with")
