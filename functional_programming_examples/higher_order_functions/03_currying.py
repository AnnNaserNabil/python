"""
3. Currying and Partial Application in Python

This module explores function currying and partial application, two powerful
functional programming techniques that enable more flexible and reusable code.

Key Concepts:
- Currying: Transforming a function that takes multiple arguments into a 
  sequence of functions that each take a single argument.
- Partial Application: Fixing a number of arguments to a function, producing
  another function of smaller arity.

Why This Matters:
- Enables function specialization and reuse
- Facilitates function composition
- Makes it easier to create specialized functions from general ones
- Common in functional programming and used in libraries like functools and toolz

Related Concepts:
- Higher-Order Functions (see 01_basic_hofs.py)
- Function Composition (see function_composition/)
- Decorators (see 02_decorators.py)
"""
from typing import TypeVar, Callable, Any, Tuple, Dict, List, Optional
from functools import partial, wraps
import math
import operator
from collections import defaultdict

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# 1. Manual currying
def curry_explicit(func: Callable[..., T], arity: int) -> Callable[..., T]:
    """
    Explicitly curry a function to the specified arity.
    
    This function transforms a function that takes multiple arguments into a
    sequence of functions that each take a single argument. When all arguments
    are provided, the original function is called with those arguments.
    
    Args:
        func: The function to be curried
        arity: The number of arguments the function accepts
        
    Returns:
        A curried version of the input function
        
    Example:
        >>> def add_three(a, b, c):
        ...     return a + b + c
        >>> curried_add = curry_explicit(add_three, 3)
        >>> add_five = curried_add(2)(3)  # Partial application
        >>> add_five(5)  # 2 + 3 + 5 = 10
        10
        
    Note:
        This is a manual implementation for demonstration. In practice,
        consider using `functools.partial` or libraries like `toolz`.
    """
    def curried(*args: Any) -> Any:
        if len(args) >= arity:
            return func(*args[:arity])
        return lambda *more_args: curried(*(args + more_args))
    return curried

# 2. Using functools.partial
def demonstrate_partial() -> None:
    """
    Demonstrate the use of `functools.partial` for partial function application.
    
    Partial application allows you to fix a certain number of arguments
    of a function and generate a new function that takes the remaining
    arguments.
    
    Why Use Partial Application?
    - Create specialized functions from general ones
    - Improve code readability by reducing argument repetition
    - Enable function composition and pipelining
    
    Example Use Cases:
    - Creating specialized mathematical functions
    - Configuring callbacks with preset arguments
    - Building flexible APIs with sensible defaults
    """
    # Original function
    def power(base: float, exponent: float) -> float:
        return base ** exponent
    
    # Create specialized versions
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"Square of 5: {square(5)}")  # 25.0
    print(f"Cube of 3: {cube(3)}")      # 27.0
    
    # Partial with multiple arguments
    def greet(greeting: str, name: str, punctuation: str = "!") -> str:
        return f"{greeting}, {name}{punctuation}"
    
    say_hello = partial(greet, "Hello")
    say_hi = partial(greet, "Hi", punctuation=".")
    
    print(say_hello("Alice"))            # Hello, Alice!
    print(say_hi("Bob"))                 # Hi, Bob.
    print(say_hello("Charlie", "?"))      # Hello, Charlie?

# 3. Automatic currying decorator
def curry(func: Callable[..., T]) -> Callable[..., T]:
    """
    A decorator that automatically curries a function based on its signature.
    
    This decorator transforms a function into a curried version that can be
    called with arguments one at a time. The function will only execute when
    all required arguments are provided.
    
    Args:
        func: The function to be curried. Can be any callable with a defined
              `__code__.co_argcount` attribute.
              
    Returns:
        A curried version of the input function that can be called with
        arguments one at a time.
        
    Example:
        >>> @curry
        ... def add(a, b, c):
        ...     return a + b + c
        >>> add(1)(2)(3)  # Returns 6
        6
        >>> add(1, 2)(3)  # Also returns 6
        6
        
    Note:
        - The function determines its arity automatically using `inspect.signature`
        - Keyword arguments are supported but must be passed after all positional arguments
    """
    @wraps(func)
    def curried(*args: Any, **kwargs: Any) -> Any:
        # Try to bind the arguments to the function signature
        try:
            # If we have enough arguments, call the function
            return func(*args, **kwargs)
        except TypeError as e:
            # If we get a type error, it might be because we don't have enough arguments
            if 'missing' in str(e) or 'positional' in str(e):
                # Return a new curried function with the current arguments bound
                return lambda *more_args, **more_kwargs: curried(
                    *args, *more_args, **{**kwargs, **more_kwargs}
                )
            # If it's a different type error, raise it
            raise
    return cast(Callable[..., T], curried)

# 4. Practical use cases
def create_url(scheme: str, domain: str, path: str, query: Optional[Dict[str, str]] = None) -> str:
    """
    Create a URL from components.
    
    This function takes the scheme, domain, path, and optional query parameters
    to construct a URL string.
    
    Args:
        scheme: The URL scheme (e.g., http, https)
        domain: The domain name
        path: The URL path
        query: Optional query parameters as a dictionary
        
    Returns:
        A constructed URL string
    """
    query_str = ""
    if query:
        query_str = "?" + "&".join(f"{k}={v}" for k, v in query.items())
    return f"{scheme}://{domain}/{path.lstrip('/')}{query_str}"

def process_data(processor: Callable[[List[float]], float], data: List[float]) -> Dict[str, Any]:
    """
    Process data using the provided processor function.
    
    This function applies the given processor function to the input data and
    returns the result along with metadata.
    
    Args:
        processor: A function that takes a list of floats and returns a float
        data: The input data as a list of floats
        
    Returns:
        A dictionary containing the result and metadata
    """
    result = processor(data)
    return {
        "result": result,
        "timestamp": "2023-01-01T12:00:00",
        "data_length": len(data)
    }

def demonstrate_currying() -> None:
    """
    Demonstrate practical examples of function currying.
    
    This function shows how currying can be used to create specialized
    functions from more general ones, improving code reuse and readability.
    
    Real-world Applications:
    1. Creating specialized utility functions
    2. Building configuration-driven systems
    3. Implementing domain-specific languages (DSLs)
    4. Creating fluent APIs
    
    The examples below illustrate both manual currying and the use of
    the `@curry` decorator for more concise code.
    """
    # Create specialized URL creators
    create_http_url = partial(create_url, "http")
    create_https_url = partial(create_url, "https")
    
    create_api_url = partial(create_http_url, "api.example.com")
    
    users_url = create_api_url("users")
    products_url = create_api_url("products")
    
    print(f"Users URL: {users_url}")
    print(f"Products URL: {products_url}")
    
    # Create a URL with query parameters
    search_url = partial(create_api_url, "search")
    user_search = search_url(query={"q": "alice", "page": "1"})
    print(f"User search URL: {user_search}")
    
    # Data processing pipeline
    data = [1.2, 3.4, 5.6, 7.8, 9.0]
    
    # Create specialized processors
    calculate_mean = partial(process_data, lambda x: sum(x) / len(x))
    calculate_max = partial(process_data, max)
    calculate_min = partial(process_data, min)
    
    print("\nData Processing:")
    print(f"Mean: {calculate_mean(data)}")
    print(f"Max: {calculate_max(data)}")
    print(f"Min: {calculate_min(data)}")

# 5. Currying with multiple arguments
def curry_by_args(func: Callable[..., T], arg_count: Optional[int] = None) -> Callable[..., T]:
    """
    Curry a function based on argument count.
    
    Args:
        func: The function to curry
        arg_count: Number of arguments to curry (defaults to func.__code__.co_argcount)
    """
    if arg_count is None:
        arg_count = func.__code__.co_argcount
    
    @wraps(func)
    def curried(*args: Any) -> Any:
        if len(args) >= arg_count:
            return func(*args[:arg_count])
        return lambda *more_args: curried(*(args + more_args))
    return cast(Callable[..., T], curried)

# 6. Practical example: Configuration
def create_logger(level: str, format_str: str, output: str):
    """Create a logger with the specified configuration."""
    print(f"Creating logger - Level: {level}, Format: {format_str}, Output: {output}")
    # In a real implementation, this would create and return a logger
    return {"level": level, "format": format_str, "output": output}

def demonstrate_configuration() -> None:
    """Show how currying can be used for configuration."""
    # Create a default logger creator with some defaults
    create_dev_logger = partial(
        create_logger,
        level="DEBUG",
        format_str="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        output="console"
    )
    
    # Create a file logger with custom format
    create_file_logger = partial(
        create_dev_logger,
        output="app.log"
    )
    
    # Create a production logger
    create_prod_logger = partial(
        create_logger,
        level="WARNING",
        format_str="%(levelname)s: %(message)s",
        output="syslog"
    )
    
    print("\nLogger Configurations:")
    print("Development Logger:", create_dev_logger())
    print("File Logger:", create_file_logger())
    print("Production Logger:", create_prod_logger())

def main() -> None:
    """
    Main demonstration function for currying and partial application.
    
    This function ties together all the concepts in this module, showing:
    1. Manual currying with explicit arity
    2. Using `functools.partial` for partial application
    3. Automatic currying with the `@curry` decorator
    
    The examples progress from basic to more advanced usage patterns,
    demonstrating how these functional programming techniques can make
    your code more expressive and maintainable.
    
    See Also:
        - `functools.partial` in the Python standard library
        - The `toolz.curry` function for more advanced currying
        - The `fn` library for additional functional programming tools
    """
    print("=== Manual Currying ===")
    # Manual currying example
    @curry_explicit
    def add_three(a: int, b: int, c: int) -> int:
        return a + b + c
    
    add_five = add_three(2)(3)  # Partial application
    print(f"add_five(10) = {add_five(10)}")  # 15
    
    print("\n=== Using functools.partial ===")
    demonstrate_partial()
    
    print("\n=== Automatic Currying ===")
    @curry
    def multiply(a: int, b: int, c: int) -> int:
        return a * b * c
    
    double = multiply(2)  # Partial application
    triple = multiply(3)
    
    print(f"double(5)(3) = {double(5)(3)}")  # 30
    print(f"triple(4)(2) = {triple(4)(2)}")  # 24
    
    print("\n=== Practical Use Cases ===")
    demonstrate_currying()
    
    print("\n=== Configuration Example ===")
    demonstrate_configuration()
    
    print("\n=== Key Takeaways ===")
    print("1. Currying transforms a multi-argument function into a chain of single-argument functions")
    print("2. functools.partial is great for fixing specific arguments")
    print("3. Currying enables function specialization and composition")
    print("4. Useful for configuration, API clients, and data processing pipelines")
    print("5. Consider using libraries like toolz.curry for more advanced use cases")

if __name__ == "__main__":
    main()
