"""
3. Power Function Generator using Closures

This module demonstrates how to use closures to create specialized mathematical
functions, specifically power functions with fixed exponents. This is a classic
example of a function factory pattern in functional programming.

Key Concepts:
------------
1. Function Factories: Functions that create and return other functions
2. Closures: Functions that remember values in their enclosing scope
3. Mathematical Function Composition: Creating specialized functions from general ones

Why Use Function Factories?
-------------------------
- Code Reuse: Avoid duplicating similar function definitions
- Customization: Create specialized functions with specific behaviors
- Encapsulation: Keep the implementation details hidden
- Readability: Make the intention of specialized functions clear

Real-world Applications:
-----------------------
- Mathematical and scientific computing
- Configuration of callback functions
- Creating specialized validators or transformers
- Implementing strategy patterns

Example:
-------
>>> square = make_power_function(2)
>>> square(5)  # Returns 25
>>> cube = make_power_function(3)
>>> cube(3)    # Returns 27
>>> sqrt = make_power_function(0.5)
>>> sqrt(16)   # Returns 4.0
"""
from __future__ import annotations
from typing import Callable

def make_power_function(exponent: float) -> Callable[[float], float]:
    """
    Create a power function that raises any number to a fixed exponent.
    
    This is a classic example of a function factory that uses closures to
    create specialized mathematical functions. The returned function 'remembers'
    the exponent value from its enclosing scope.
    
    Args:
        exponent (float): The exponent to use in the power function.
                        Can be any real number (positive, negative, or fractional).
        
    Returns:
        Callable[[float], float]: A function that takes a number and returns
                                that number raised to the stored exponent.
                                
    Example:
        >>> square = make_power_function(2)
        >>> square(4)  # Returns 16.0
        >>> cube = make_power_function(3)
        >>> cube(3)    # Returns 27.0
        
    Implementation Notes:
    - Uses a closure to maintain the exponent value
    - The inner function has access to the exponent from the outer scope
    - Each call to make_power_function creates a new, independent function
    - The exponent is fixed at function creation time
    """
    def power(base: float) -> float:
        """Raise base to the power of the stored exponent."""
        return base ** exponent
    
    return power

def demonstrate_power_functions() -> None:
    """
    Demonstrate the creation and use of specialized power functions.
    
    This function shows how to use the make_power_function factory to create
    various mathematical functions like square, cube, square root, and reciprocal.
    It also demonstrates how these functions maintain their state (the exponent)
    between calls.
    
    The examples include:
    - Creating common power functions (square, cube, etc.)
    - Using list comprehensions to apply power functions to sequences
    - Creating dynamic power functions based on runtime values
    
    Note how each generated function maintains its own exponent value
    independently, even though they were created by the same factory function.
    """
    # Create some specialized power functions
    square = make_power_function(2)
    cube = make_power_function(3)
    square_root = make_power_function(0.5)
    reciprocal = make_power_function(-1)
    
    # Use the generated functions
    print(f"Square of 5: {square(5)}")
    print(f"Cube of 3: {cube(3)}")
    print(f"Square root of 16: {square_root(16):.1f}")
    print(f"Reciprocal of 4: {reciprocal(4):.2f}")
    
    # Create and use a dynamic power function
    exponent = 2.5
    power_func = make_power_function(exponent)
    value = 10
    print(f"\n{value} to the power of {exponent}: {power_func(value):.2f}")
    
    # Show that the functions maintain their state
    print("\nUsing the same functions with different inputs:")
    numbers = [1, 2, 3, 4, 5]
    print(f"Squares: {[square(n) for n in numbers]}")
    print(f"Cubes: {[cube(n) for n in numbers]}")
    
    # Create a list of power functions with different exponents
    exponents = [0.5, 1, 2, 3]
    power_functions = [make_power_function(exp) for exp in exponents]
    
    print("\nApplying multiple power functions to the same number (4):")
    for exp, func in zip(exponents, power_functions):
        print(f"4^{exp} = {func(4):.2f}")

if __name__ == "__main__":
    print("=== Power Function Generator ===")
    demonstrate_power_functions()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures can be used to create specialized functions")
    print("2. The outer function's parameters become part of the closure's state")
    print("3. Each generated function maintains its own state independently")
    print("4. This pattern is useful for function factories")
    print("5. The same function can be specialized in different ways")
