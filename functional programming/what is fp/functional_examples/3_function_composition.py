"""
3. Function Composition

Function composition is the process of combining two or more functions to produce a new function.
In mathematics, f(g(x)) is the composition of f and g.
"""

def compose(*functions):
    """
    Compose functions from right to left.
    compose(f, g, h)(x) is equivalent to f(g(h(x)))
    """
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed

# Example functions
def add_one(x):
    return x + 1

def double(x):
    return x * 2

def square(x):
    return x ** 2

def format_result(x):
    return f"The result is: {x}"

def to_upper(s):
    return s.upper()

def add_exclamation(s):
    return s + "!"

# Testing the composition
if __name__ == "__main__":
    # Mathematical composition: square(double(add_one(3)))
    math_operation = compose(square, double, add_one)
    print(f"square(double(add_one(3))) = {math_operation(3)}")
    
    # String processing composition: to_upper(add_exclamation("hello"))
    string_operation = compose(to_upper, add_exclamation)
    print(f"to_upper(add_exclamation('hello')) = {string_operation('hello')}")
    
    # More complex composition
    complex_operation = compose(format_result, str, square, double, add_one)
    print(f"Complex operation on 3: {complex_operation(3)}")
    
    # Using lambda functions for quick composition
    add_then_double = compose(lambda x: x * 2, lambda x: x + 5)
    print(f"Add 5 then double (input 3): {add_then_double(3)}")
    
    # Composition with multiple arguments using lambda
    def add(a, b):
        return a + b
    
    # We can use lambda to make a multi-arg function work with compose
    add_5 = lambda x: add(x, 5)
    operation = compose(square, add_5)
    print(f"(x + 5)² where x=3: {operation(3)}")
