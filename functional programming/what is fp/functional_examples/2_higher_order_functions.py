"""
2. Higher-Order Functions

A higher-order function is a function that:
1. Takes one or more functions as arguments, or
2. Returns a function as its result
"""

# Example 1: Function as argument
def apply_operation(x, y, operation):
    """
    Applies the given operation to x and y.
    - Takes a function as an argument
    - Returns the result of applying the operation
    """
    return operation(x, y)

# Example 2: Function that returns a function
def make_multiplier(factor):
    """
    Returns a function that multiplies by the given factor.
    - Returns a new function
    - The returned function remembers the 'factor' value (closure)
    """
    def multiplier(x):
        return x * factor
    return multiplier

# Example 3: Using built-in higher-order functions
def process_numbers(numbers, filter_func, map_func):
    """
    Processes numbers using filter and map functions.
    - filter_func: A function that returns True/False
    - map_func: A function to apply to each element
    """
    filtered = filter(filter_func, numbers)
    return list(map(map_func, filtered))

# Testing the functions
if __name__ == "__main__":
    # Test apply_operation with different operations
    print("apply_operation examples:")
    print(f"Addition: {apply_operation(5, 3, lambda x, y: x + y)}")
    print(f"Multiplication: {apply_operation(5, 3, lambda x, y: x * y)}")
    
    # Test make_multiplier
    print("\nmake_multiplier examples:")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"Double of 5: {double(5)}")
    print(f"Triple of 5: {triple(5)}")
    
    # Test process_numbers
    print("\nprocess_numbers example:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Get squares of even numbers
    result = process_numbers(
        numbers,
        filter_func=lambda x: x % 2 == 0,  # Keep even numbers
        map_func=lambda x: x ** 2           # Square each number
    )
    print(f"Squares of even numbers: {result}")
    
    # Get cubes of numbers greater than 5
    result = process_numbers(
        numbers,
        filter_func=lambda x: x > 5,         # Keep numbers > 5
        map_func=lambda x: x ** 3            # Cube each number
    )
    print(f"Cubes of numbers > 5: {result}")
