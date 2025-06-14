"""
2. Counter with Closure in Python

This module demonstrates how to create a stateful counter using closures, 
showcasing how functions can maintain state between calls without using classes.

Key Concepts:
------------
1. State Management: Using closures to maintain state between function calls
2. Data Encapsulation: Hiding the counter variable in the closure's scope
3. Multiple Inner Functions: Different functions sharing the same non-local variable

Why Use Closures for State?
-------------------------
- Encapsulation: The counter variable is private to the closure
- No Global State: Avoids polluting the global namespace
- Multiple Instances: Each closure maintains its own independent state
- Clean Interface: Exposes only the desired functionality

Real-world Applications:
-----------------------
- Stateful function factories
- Implementing private variables in modules
- Creating lightweight objects with behavior but no formal class
- Managing configuration in a controlled way

Example:
-------
>>> get_count, increment, reset = create_counter()
>>> increment()
1
>>> increment()
2
>>> get_count()
2
>>> reset()
>>> get_count()
0
"""
from __future__ import annotations
from typing import Callable, Tuple

def create_counter() -> Tuple[Callable[[], int], Callable[[], int], Callable[[], None]]:
    """
    Create a counter with get, increment, and reset functionality using closures.
    
    This function demonstrates how to maintain state between function calls without
    using classes or global variables. The state (count) is stored in the closure's
    scope and can only be modified through the returned functions.
    
    Returns:
        A tuple containing three functions:
        - get_count: Function that returns the current count
        - increment: Function that increments and returns the new count
        - reset: Function that resets the counter to zero
        
    Example:
        >>> get_count, increment, reset = create_counter()
        >>> increment()
        1
        >>> increment()
        2
        >>> get_count()
        2
        >>> reset()
        >>> get_count()
        0
        
    Implementation Notes:
    - Uses nonlocal to modify the count variable from inner functions
    - Each call to create_counter() creates a new, independent counter
    - The count variable is private to the closure and cannot be accessed directly
    """
    count = 0  # This variable is in the enclosing scope
    
    def get_count() -> int:
        """Return the current count."""
        nonlocal count
        return count
    
    def increment() -> int:
        """Increment the counter and return the new count."""
        nonlocal count
        count += 1
        return count
    
    def reset() -> None:
        """Reset the counter to zero."""
        nonlocal count
        count = 0
    
    return get_count, increment, reset

def demonstrate_counter() -> None:
    """Demonstrate the counter closure."""
    # Create a counter
    get_count, increment, reset = create_counter()
    
    # Initial state
    print(f"Initial count: {get_count()}")
    
    # Increment and check
    print(f"After increment: {increment()}")
    print(f"After increment: {increment()}")
    print(f"Current count: {get_count()}")
    
    # Reset and check
    reset()
    print(f"After reset: {get_count()}")
    
    # Create another independent counter
    print("\nCreating a second counter...")
    get_count2, increment2, reset2 = create_counter()
    print(f"Second counter initial: {get_count2()}")
    print(f"Increment second counter: {increment2()}")
    print(f"First counter still at: {get_count()}")
    
    # Show that the first counter is still accessible
    print(f"\nFirst counter after operations: {get_count()}")
    print(f"Increment first counter: {increment()}")
    print(f"First counter now: {get_count()}")

if __name__ == "__main__":
    print("=== Counter with Closure ===")
    demonstrate_counter()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures can maintain state between function calls")
    print("2. Each closure has its own independent state")
    print("3. The 'nonlocal' keyword allows modifying variables in the enclosing scope")
    print("4. Multiple functions can close over the same variables")
    print("5. Closures provide data encapsulation similar to objects")
