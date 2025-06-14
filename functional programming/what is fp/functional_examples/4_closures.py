"""
4. Closures

A closure is a function that remembers values in the enclosing scope even if they are not present in memory.
It's a record that stores a function together with an environment.
"""

def make_counter():
    """
    Returns a counter function that remembers the count between calls.
    Each call to the returned function increments and returns the count.
    """
    count = 0  # This variable is in the enclosing scope
    
    def counter():
        nonlocal count  # Allows us to modify the count variable from the outer scope
        count += 1
        return count
    
    return counter

def make_power(n):
    """
    Returns a function that raises its argument to the power of n.
    The returned function remembers the value of n from the outer scope.
    """
    def power(x):
        return x ** n
    return power

def make_tag(tag):
    """
    Returns a function that wraps text in HTML tags.
    The returned function remembers the tag from the outer scope.
    """
    def wrapper(text):
        return f"<{tag}>{text}</{tag}>"
    return wrapper

def make_adder(x):
    """
    Returns a function that adds x to its argument.
    The returned function remembers the value of x from the outer scope.
    """
    def add(y):
        return x + y
    return add

def make_multiplier(factor):
    """
    Returns a function that multiplies its argument by factor.
    The returned function remembers the factor from the outer scope.
    """
    def multiplier(x):
        return x * factor
    return multiplier

# Testing the closures
if __name__ == "__main__":
    # Test counter
    print("Testing counter:")
    counter1 = make_counter()
    print(f"counter1: {counter1()}")  # 1
    print(f"counter1: {counter1()}")  # 2
    
    counter2 = make_counter()
    print(f"counter2: {counter2()}")  # 1 (independent of counter1)
    
    # Test power functions
    print("\nTesting power functions:")
    square = make_power(2)
    cube = make_power(3)
    print(f"square(4) = {square(4)}")  # 16
    print(f"cube(3) = {cube(3)}")      # 27
    
    # Test HTML tag wrapper
    print("\nTesting HTML tag wrapper:")
    make_bold = make_tag("b")
    make_italic = make_tag("i")
    print(make_bold("Hello"))     # <b>Hello</b>
    print(make_italic("World"))   # <i>World</i>
    
    # Test adder
    print("\nTesting adder:")
    add5 = make_adder(5)
    print(f"add5(3) = {add5(3)}")  # 8
    
    # Test multiplier
    print("\nTesting multiplier:")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5) = {double(5)}")  # 10
    print(f"triple(5) = {triple(5)}")  # 15
    
    # Closures remember values even if they go out of scope
    def make_greeter(greeting):
        def greet(name):
            return f"{greeting}, {name}!"
        return greet
    
    say_hello = make_greeter("Hello")
    say_hi = make_greeter("Hi")
    
    # The greeting variable is remembered by each closure
    print(f"\n{say_hello('Alice')}")  # Hello, Alice!
    print(f"{say_hi('Bob')}")         # Hi, Bob!
