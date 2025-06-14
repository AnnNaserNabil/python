"""
3. Composing Higher-Order Functions in Python

This module demonstrates how to combine higher-order functions (HOFs) like map, 
filter, and reduce with function composition to create expressive and powerful
data processing pipelines. Higher-order functions are functions that take other
functions as arguments or return them as results.

Key Concepts:
------------
1. Higher-Order Functions: Functions that operate on other functions
2. Function Composition: Combining simple functions to build complex operations
3. Data Pipelines: Creating reusable processing chains
4. Lazy Evaluation: Processing data on-demand with generators

Why Compose Higher-Order Functions?
---------------------------------
- Expressiveness: Write complex transformations clearly and concisely
- Modularity: Build complex operations from simple, reusable components
- Readability: Make data transformations more declarative
- Maintainability: Easier to modify and extend processing pipelines

Real-world Applications:
----------------------
- Data analysis and transformation
- ETL (Extract, Transform, Load) pipelines
- API response processing
- Data validation and cleaning
- Stream processing

Example:
-------
>>> from functools import reduce
>>> data = [1, 2, 3, 4, 5]
>>> # Compose map and filter operations
>>> pipeline = map_compose(lambda x: x**2, lambda x: x + 1)
>>> filtered = filter_compose(lambda x: x > 5)
>>> list(filtered(pipeline(data)))
[10, 17, 26]
"""
from __future__ import annotations
from typing import Callable, TypeVar, Iterable, Any, List, Dict, Tuple
from functools import reduce, partial
import operator
import json

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Compose functions from right to left.
    
    Creates a function that applies a series of functions to its input,
    with each function receiving the output of the previous function.
    
    Args:
        *funcs: Variable number of functions to compose
        
    Returns:
        Callable[..., Any]: A new function that applies all input functions
                          from right to left
                          
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> composed = compose(square, add_one)
        >>> composed(2)  # square(add_one(2)) = (2 + 1)² = 9
        9
    """
    def _compose(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return reduce(_compose, funcs, lambda x: x)

def pipe(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Pipe functions from left to right.
    
    Creates a function that applies a series of functions to its input,
    with each function receiving the output of the previous function.
    
    Args:
        *funcs: Variable number of functions to pipe
        
    Returns:
        Callable[..., Any]: A new function that applies all input functions
                          from left to right
                          
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> piped = pipe(add_one, square)
        >>> piped(2)  # square(add_one(2)) = (2 + 1)² = 9
        9
    """
    def _pipe(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: g(f(*args, **kwargs))
    return reduce(_pipe, funcs, lambda x: x)

def map_compose(*funcs: Callable[..., Any]) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """
    Create a function that applies a composition of functions to each element of an iterable.
    
    This higher-order function returns a new function that, when called with an iterable,
    applies the composed functions to each element. The composition is done from right to left,
    similar to mathematical function composition.
    
    Args:
        *funcs: Variable number of functions to compose and map
        
    Returns:
        Callable[[Iterable[Any]], Iterable[Any]]: A function that maps the composed
                                              functions over an iterable
                                              
    Example:
        >>> def add_one(x): return x + 1
        >>> def square(x): return x * x
        >>> process = map_compose(square, add_one)
        >>> list(process([1, 2, 3]))  # [(1+1)², (2+1)², (3+1)²] = [4, 9, 16]
        [4, 9, 16]
        
    Note:
        - Returns a generator for lazy evaluation
        - If no functions are provided, returns the iterable unchanged
    """
    def mapper(iterable: Iterable[Any]) -> Iterable[Any]:
        for item in iterable:
            result = item
            for func in reversed(funcs):
                result = func(result)
            yield result
    return mapper

def filter_compose(*predicates: Callable[[Any], bool]) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """
    Create a function that filters an iterable based on multiple predicates.
    
    This higher-order function returns a new function that filters an iterable,
    keeping only elements that satisfy all provided predicates. The predicates
    are combined using logical AND.
    
    Args:
        *predicates: Variable number of predicate functions
        
    Returns:
        Callable[[Iterable[Any]], Iterable[Any]]: A function that filters an iterable
                                              based on the predicates
                                              
    Example:
        >>> is_even = lambda x: x % 2 == 0
        >>> is_positive = lambda x: x > 0
        >>> filter_func = filter_compose(is_even, is_positive)
        >>> list(filter_func([-2, -1, 0, 1, 2, 3, 4]))
        [2, 4]
        
    Note:
        - Returns a generator for lazy evaluation
        - If no predicates are provided, all elements are included
    """
    def filterer(iterable: Iterable[Any]) -> Iterable[Any]:
        for item in iterable:
            if all(pred(item) for pred in predicates):
                yield item
    return filterer

def demonstrate_map_composition() -> None:
    """Demonstrate composition with mapping functions."""
    # Basic data
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Simple transformations
    square = lambda x: x ** 2
    double = lambda x: x * 2
    increment = lambda x: x + 1
    
    # Compose transformations
    transform = compose(
        partial(map, square),
        partial(map, double),
        partial(map, increment)
    )
    
    # Apply transformations
    result = list(transform(numbers))
    print(f"Transform result: {result}")
    
    # More readable with a single map
    transform_single = partial(map, compose(square, double, increment))
    result_single = list(transform_single(numbers))
    print(f"Single map result: {result_single}")
    
    # Using map_compose helper
    transform_mapped = map_compose(square, double, increment)
    result_mapped = list(transform_mapped(numbers))
    print(f"map_compose result: {result_mapped}")

def demonstrate_filter_composition() -> None:
    """Demonstrate composition with filtering functions."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Predicates
    is_even = lambda x: x % 2 == 0
    is_greater_than_5 = lambda x: x > 5
    is_less_than_10 = lambda x: x < 10
    
    # Compose filters
    filter_nums = compose(
        partial(filter, is_less_than_10),
        partial(filter, is_greater_than_5),
        partial(filter, is_even)
    )
    
    # Apply filters
    result = list(filter_nums(numbers))
    print(f"Filtered numbers: {result}")
    
    # Using filter_compose helper
    filter_combined = filter_compose(is_even, is_greater_than_5, is_less_than_10)
    result_combined = list(filter_combined(numbers))
    print(f"Combined filter: {result_combined}")

def demonstrate_reduce_composition() -> None:
    """Demonstrate composition with reduction functions."""
    # Sample data
    items = [
        {"name": "item1", "price": 10.0, "quantity": 2},
        {"name": "item2", "price": 20.0, "quantity": 1},
        {"name": "item3", "price": 15.0, "quantity": 3},
    ]
    
    # Processing steps
    get_prices = partial(map, lambda item: item["price"] * item["quantity"])
    sum_prices = partial(reduce, lambda acc, x: acc + x)
    
    # Compose processing pipeline
    calculate_total = compose(sum_prices, get_prices)
    
    # Calculate total
    total = calculate_total(items)
    print(f"Total price: {total}")
    
    # More complex example with multiple steps
    def calculate_discounted_total(discount: float) -> Callable[[Iterable[Dict[str, Any]]], float]:
        """Create a function that calculates total with discount."""
        return compose(
            sum,  # Sum all values
            partial(map, lambda x: x * (1 - discount)),  # Apply discount
            partial(map, lambda item: item["price"] * item["quantity"])  # Calculate line total
        )
    
    # Create a 10% discount calculator
    calculate_with_discount = calculate_discounted_total(0.1)
    discounted_total = calculate_with_discount(items)
    print(f"Discounted total (10% off): {discounted_total:.2f}")

def demonstrate_complex_pipeline() -> None:
    """Demonstrate a complex data processing pipeline."""
    # Sample data: list of orders
    orders = [
        {"id": 1, "customer": "Alice", "items": [
            {"name": "Widget", "price": 10.0, "quantity": 2},
            {"name": "Gadget", "price": 25.0, "quantity": 1}
        ]},
        {"id": 2, "customer": "Bob", "items": [
            {"name": "Widget", "price": 10.0, "quantity": 1},
            {"name": "Thingy", "price": 5.0, "quantity": 4}
        ]},
        {"id": 3, "customer": "Alice", "items": [
            {"name": "Gadget", "price": 25.0, "quantity": 2},
            {"name": "Thingy", "price": 5.0, "quantity": 2}
        ]}
    ]
    
    # Processing functions
    def get_order_total(order: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate total for an order."""
        total = sum(item["price"] * item["quantity"] for item in order["items"])
        return {**order, "total": total}
    
    def filter_high_value(min_total: float) -> Callable[[Dict[str, Any]], bool]:
        """Create a filter for high-value orders."""
        return lambda order: order["total"] >= min_total
    
    def group_by_customer(orders: Iterable[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group orders by customer."""
        groups: Dict[str, List[Dict[str, Any]]] = {}
        for order in orders:
            customer = order["customer"]
            if customer not in groups:
                groups[customer] = []
            groups[customer].append(order)
        return groups
    
    # Create the processing pipeline
    process_orders = compose(
        group_by_customer,
        partial(sorted, key=lambda x: x["total"], reverse=True),  # Sort by total
        partial(filter, filter_high_value(30.0)),  # Only orders over $30
        partial(map, get_order_total)  # Add total to each order
    )
    
    # Process the orders
    result = process_orders(orders)
    
    # Print results
    print("\nProcessed Orders by Customer:")
    print(json.dumps(result, indent=2))
    
    # Calculate customer totals
    customer_totals = {
        customer: sum(order["total"] for order in customer_orders)
        for customer, customer_orders in result.items()
    }
    
    print("\nCustomer Totals:")
    for customer, total in customer_totals.items():
        print(f"{customer}: ${total:.2f}")

if __name__ == "__main__":
    print("=== Composing Higher-Order Functions ===")
    
    print("\n--- Map Composition ---")
    demonstrate_map_composition()
    
    print("\n--- Filter Composition ---")
    demonstrate_filter_composition()
    
    print("\n--- Reduce Composition ---")
    demonstrate_reduce_composition()
    
    print("\n--- Complex Pipeline ---")
    demonstrate_complex_pipeline()
    
    print("\n=== Key Takeaways ===")
    print("1. Higher-order functions can be composed to create powerful data pipelines")
    print("2. map, filter, and reduce can be combined for complex transformations")
    print("3. Function composition makes the data flow clear and declarative")
    print("4. Each function in the pipeline should have a single responsibility")
    print("5. Composition enables code reuse and modularity")
