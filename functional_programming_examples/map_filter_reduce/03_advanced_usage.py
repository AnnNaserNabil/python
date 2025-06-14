"""
3. Advanced Usage of Map, Filter, and Reduce

Explores more advanced patterns and techniques using map, filter, and reduce,
including partial function application, function composition, and more.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Iterable, Any, List, Dict, Tuple, Optional
from functools import reduce, partial
import operator
import math
from collections import defaultdict

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# 1. Partial Function Application

def demonstrate_partial() -> None:
    """Show how to use partial to create specialized functions."""
    print("=== Partial Function Application ===\n")
    
    # Create a function that always adds 10
    add_ten = partial(operator.add, 10)
    print(f"add_ten(5) = {add_ten(5)}")
    
    # Create a function that multiplies by 3 and adds 1
    triple_plus_one = partial(operator.add, 1, 3)
    print(f"triple_plus_one(5) = {triple_plus_one(5)}")
    
    # Using partial with keyword arguments
    def power(base: float, exponent: float) -> float:
        return base ** exponent
    
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"square(5) = {square(5)}")
    print(f"cube(3) = {cube(3)}")
    
    # Using partial with map
    numbers = [1, 2, 3, 4, 5]
    squares = list(map(square, numbers))
    print(f"Squares of {numbers}: {squares}")

# 2. Function Composition

def compose(*funcs: Callable) -> Callable:
    """Compose functions from right to left."""
    def composed(x: Any) -> Any:
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed

def demonstrate_function_composition() -> None:
    """Show how to compose functions for data transformation."""
    print("\n=== Function Composition ===\n")
    
    # Define some simple functions
    def add_one(x: int) -> int:
        return x + 1
    
    def double(x: int) -> int:
        return x * 2
    
    def square(x: int) -> int:
        return x ** 2
    
    # Compose functions
    add_one_then_double = compose(double, add_one)
    print(f"add_one_then_double(5) = {add_one_then_double(5)}")
    
    # More complex composition
    transform = compose(str, square, add_one, double)
    print(f"double, add_one, square, then to string: {transform(3)}")
    
    # Using with map
    numbers = [1, 2, 3, 4, 5]
    transformed = list(map(compose(str, square, add_one), numbers))
    print(f"Transformed {numbers}: {transformed}")

# 3. Advanced Reduce Patterns

def demonstrate_advanced_reduce() -> None:
    """Show advanced patterns using reduce."""
    print("\n=== Advanced Reduce Patterns ===\n")
    
    # 3.1 Finding the maximum value with reduce
    numbers = [4, 2, 8, 1, 9, 5]
    max_num = reduce(lambda a, b: a if a > b else b, numbers)
    print(f"Max of {numbers}: {max_num}")
    
    # 3.2 Flatten a list of lists
    nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    flattened = reduce(lambda x, y: x + y, nested, [])
    print(f"Flattened {nested}: {flattened}")
    
    # 3.3 Counting occurrences with reduce
    words = ["apple", "banana", "apple", "orange", "banana", "apple"]
    word_counts = reduce(
        lambda counts, word: {**counts, word: counts.get(word, 0) + 1},
        words,
        {}
    )
    print(f"Word counts: {word_counts}")
    
    # 3.4 Composing functions with reduce
    def compose_with_reduce(*funcs: Callable) -> Callable:
        """Compose functions using reduce."""
        return lambda x: reduce(lambda acc, f: f(acc), reversed(funcs), x)
    
    # Example usage
    def add_five(x: int) -> int:
        return x + 5
    
    composed = compose_with_reduce(str, square, add_five, double)
    print(f"Composed function (double, add_five, square, str) of 3: {composed(3)}")

# 4. Advanced Map Patterns

def demonstrate_advanced_map() -> None:
    """Show advanced patterns using map."""
    print("\n=== Advanced Map Patterns ===\n")
    
    # 4.1 Mapping with multiple iterables
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    
    # Create a list of dictionaries
    people = list(map(
        lambda name, age: {"name": name, "age": age},
        names,
        ages
    ))
    print(f"People: {people}")
    
    # 4.2 Using map with functions that return None
    results = []
    def process_item(x: int) -> None:
        results.append(x ** 2)
    
    # map returns an iterator that needs to be consumed
    _ = list(map(process_item, [1, 2, 3, 4, 5]))
    print(f"Results from side effects: {results}")
    
    # 4.3 Mapping with index using enumerate
    items = ["apple", "banana", "cherry"]
    indexed = list(map(lambda x: (x[0], x[1].upper()), enumerate(items)))
    print(f"Indexed items: {indexed}")
    
    # 4.4 Using starmap for unpacking arguments
    from itertools import starmap
    
    points = [(1, 2), (3, 4), (5, 6)]
    distances = list(starmap(lambda x, y: (x**2 + y**2)**0.5, points))
    print(f"Distances from origin: {distances}")

# 5. Advanced Filter Patterns

def demonstrate_advanced_filter() -> None:
    """Show advanced patterns using filter."""
    print("\n=== Advanced Filter Patterns ===\n")
    
    # 5.1 Filtering with multiple conditions
    def is_even_positive(x: int) -> bool:
        return x > 0 and x % 2 == 0
    
    numbers = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
    filtered = list(filter(is_even_positive, numbers))
    print(f"Even positive numbers in {numbers}: {filtered}")
    
    # 5.2 Using filterfalse from itertools
    from itertools import filterfalse
    
    # Get all odd numbers
    odds = list(filterfalse(lambda x: x % 2 == 0, numbers))
    print(f"Odd numbers: {odds}")
    
    # 5.3 Filtering with index using enumerate
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    # Keep items with even indices
    filtered_items = [item for i, item in enumerate(items) if i % 2 == 0]
    print(f"Items at even indices: {filtered_items}")
    
    # 5.4 Using takewhile and dropwhile
    from itertools import takewhile, dropwhile
    
    data = [1, 4, 6, 8, 10, 2, 3, 4, 5]
    # Take elements while they are less than 10
    taken = list(takewhile(lambda x: x < 10, data))
    # Drop elements while they are less than 10
    dropped = list(dropwhile(lambda x: x < 10, data))
    
    print(f"Original: {data}")
    print(f"Taken while < 10: {taken}")
    print(f"Dropped while < 10: {dropped}")

# 6. Practical Example: Data Processing Pipeline

def advanced_data_processing() -> None:
    """Demonstrate an advanced data processing pipeline."""
    print("\n=== Advanced Data Processing Pipeline ===\n")
    
    # Sample data: List of product orders
    orders = [
        {"id": 1, "customer": "Alice", "items": [
            {"product": "Laptop", "price": 1200, "quantity": 1},
            {"product": "Mouse", "price": 30, "quantity": 2}
        ], "discount": 0.1},
        {"id": 2, "customer": "Bob", "items": [
            {"product": "Keyboard", "price": 80, "quantity": 1},
            {"product": "Monitor", "price": 250, "quantity": 2},
            {"product": "Mouse", "price": 30, "quantity": 1}
        ], "discount": 0.15},
        {"id": 3, "customer": "Charlie", "items": [
            {"product": "Laptop", "price": 1200, "quantity": 1},
            {"product": "Docking Station", "price": 150, "quantity": 1}
        ], "discount": 0.0}
    ]
    
    # 1. Calculate total for each order (including discount)
    def calculate_order_total(order: dict) -> dict:
        subtotal = sum(
            item["price"] * item["quantity"]
            for item in order["items"]
        )
        total = subtotal * (1 - order["discount"])
        return {
            "id": order["id"],
            "customer": order["customer"],
            "subtotal": subtotal,
            "discount": order["discount"] * subtotal,
            "total": total
        }
    
    order_totals = list(map(calculate_order_total, orders))
    
    # 2. Find top spending customers
    customer_spending = {}
    for order in order_totals:
        customer = order["customer"]
        customer_spending[customer] = customer_spending.get(customer, 0) + order["total"]
    
    top_customers = sorted(
        customer_spending.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # 3. Generate a product sales report
    product_sales = defaultdict(float)
    for order in orders:
        for item in order["items"]:
            product_sales[item["product"]] += item["price"] * item["quantity"]
    
    # Print results
    print("Order Totals:")
    for order in order_totals:
        print(f"  Order {order['id']} ({order['customer']}): "
              f"${order['subtotal']:.2f} - ${order['discount']:.2f} = ${order['total']:.2f}")
    
    print("\nTop Spending Customers:")
    for i, (customer, total) in enumerate(top_customers, 1):
        print(f"  {i}. {customer}: ${total:.2f}")
    
    print("\nProduct Sales:")
    for product, sales in product_sales.items():
        print(f"  {product}: ${sales:.2f}")

if __name__ == "__main__":
    print("=== Advanced Usage of Map, Filter, and Reduce ===\n")
    
    demonstrate_partial()
    demonstrate_function_composition()
    demonstrate_advanced_reduce()
    demonstrate_advanced_map()
    demonstrate_advanced_filter()
    advanced_data_processing()
    
    print("\n=== Key Takeaways ===")
    print("1. partial() creates specialized functions by fixing arguments")
    print("2. Function composition enables building complex transformations")
    print("3. reduce() can implement many common aggregation patterns")
    print("4. Advanced map() patterns handle multiple iterables and side effects")
    print("5. filter() can be combined with other tools for powerful data processing")
