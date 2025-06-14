"""
2. List and Dictionary Comprehensions

Shows how list and dictionary comprehensions can often replace
map and filter operations with more readable syntax.
"""
from __future__ import annotations
from typing import List, Dict, Tuple, Set, Any, Callable, TypeVar
from functools import reduce
import operator
import math

T = TypeVar('T')
U = TypeVar('U')

# 1. List Comprehensions vs Map/Filter

def demonstrate_list_comprehensions() -> None:
    """Show equivalent operations with list comprehensions and map/filter."""
    print("=== List Comprehensions vs Map/Filter ===\n")
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Map equivalent: Squaring numbers
    squares_map = list(map(lambda x: x ** 2, numbers))
    squares_comp = [x ** 2 for x in numbers]
    print(f"Squares (map): {squares_map}")
    print(f"Squares (comprehension): {squares_comp}")
    
    # Filter equivalent: Even numbers
    evens_filter = list(filter(lambda x: x % 2 == 0, numbers))
    evens_comp = [x for x in numbers if x % 2 == 0]
    print(f"\nEvens (filter): {evens_filter}")
    print(f"Evens (comprehension): {evens_comp}")
    
    # Map and filter combined
    result_map_filter = list(map(
        lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers)
    ))
    result_comp = [x ** 2 for x in numbers if x % 2 == 0]
    print(f"\nSquares of evens (map+filter): {result_map_filter}")
    print(f"Squares of evens (comprehension): {result_comp}")
    
    # With condition in the expression (ternary operator)
    result_conditional = [x ** 2 if x % 2 == 0 else x for x in numbers]
    print(f"\nSquares of evens, others unchanged: {result_conditional}")

# 2. Nested List Comprehensions

def demonstrate_nested_comprehensions() -> None:
    """Show examples of nested list comprehensions."""
    print("\n=== Nested List Comprehensions ===\n")
    
    # Flattening a 2D list
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    # Using nested loops
    flattened = []
    for row in matrix:
        for num in row:
            flattened.append(num)
    
    # Using list comprehension
    flattened_comp = [num for row in matrix for num in row]
    
    print(f"Flattened (loops): {flattened}")
    print(f"Flattened (comprehension): {flattened_comp}")
    
    # Transposing a matrix
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print(f"\nOriginal matrix: {matrix}")
    print(f"Transposed: {transposed}")

# 3. Dictionary Comprehensions

def demonstrate_dict_comprehensions() -> None:
    """Show examples of dictionary comprehensions."""
    print("\n=== Dictionary Comprehensions ===\n")
    
    # Create a dictionary of squares
    numbers = [1, 2, 3, 4, 5]
    squares_dict = {x: x ** 2 for x in numbers}
    print(f"Squares dict: {squares_dict}")
    
    # Filter items in a dictionary
    student_scores = {"Alice": 85, "Bob": 72, "Charlie": 90, "David": 68}
    passed = {name: score for name, score in student_scores.items() if score >= 70}
    print(f"\nStudents who passed: {passed}")
    
    # Create a dictionary from two lists
    keys = ['a', 'b', 'c']
    values = [1, 2, 3]
    combined = {k: v for k, v in zip(keys, values)}
    print(f"\nCombined dict: {combined}")
    
    # Swap keys and values
    swapped = {v: k for k, v in combined.items()}
    print(f"Swapped dict: {swapped}")

# 4. Set Comprehensions

def demonstrate_set_comprehensions() -> None:
    """Show examples of set comprehensions."""
    print("\n=== Set Comprehensions ===\n")
    
    # Create a set of unique characters in a string
    text = "hello world"
    unique_chars = {char for char in text if char != ' '}
    print(f"Unique characters in '{text}': {unique_chars}")
    
    # Set of squares
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    unique_squares = {x ** 2 for x in numbers}
    print(f"Unique squares: {unique_squares}")

# 5. Generator Expressions

def demonstrate_generator_expressions() -> None:
    """Show examples of generator expressions."""
    print("\n=== Generator Expressions ===\n")
    
    # Generator expression (lazy evaluation)
    numbers = [1, 2, 3, 4, 5]
    squares_gen = (x ** 2 for x in numbers)
    
    print("Generator object:", squares_gen)
    print("Consuming generator:", list(squares_gen))
    
    # Memory efficient processing
    large_range = range(1_000_000)
    sum_squares = sum(x ** 2 for x in large_range)
    print(f"Sum of squares (memory efficient): {sum_squares}")
    
    # Using with any() and all()
    has_negative = any(x < 0 for x in [1, 2, 3, -4, 5])
    all_positive = all(x > 0 for x in [1, 2, 3, 4, 5])
    print(f"Has negative: {has_negative}")
    print(f"All positive: {all_positive}")

# 6. Practical Example: Data Processing Pipeline

def data_processing_pipeline() -> None:
    """Demonstrate a data processing pipeline using comprehensions."""
    print("\n=== Data Processing Pipeline ===\n")
    
    # Sample data: List of transactions (customer_id, amount, country)
    transactions = [
        (101, 150.0, 'US'),
        (102, 200.0, 'UK'),
        (101, 75.0, 'US'),
        (103, 300.0, 'CA'),
        (102, 50.0, 'UK'),
        (104, 100.0, 'US'),
        (101, 225.0, 'US'),
        (103, 80.0, 'CA'),
    ]
    
    # 1. Filter transactions above $100
    large_transactions = [t for t in transactions if t[1] > 100]
    
    # 2. Convert to a list of dictionaries for better readability
    transaction_dicts = [
        {'customer_id': t[0], 'amount': t[1], 'country': t[2]}
        for t in large_transactions
    ]
    
    # 3. Group transactions by country
    from collections import defaultdict
    transactions_by_country = defaultdict(list)
    for t in transaction_dicts:
        transactions_by_country[t['country']].append(t)
    
    # 4. Calculate total and average by country
    country_stats = {
        country: {
            'total': sum(t['amount'] for t in ts),
            'count': len(ts),
            'average': sum(t['amount'] for t in ts) / len(ts)
        }
        for country, ts in transactions_by_country.items()
    }
    
    # 5. Find top customers by total spent
    customer_totals = defaultdict(float)
    for t in transaction_dicts:
        customer_totals[t['customer_id']] += t['amount']
    
    top_customers = [
        {'customer_id': cid, 'total': total}
        for cid, total in sorted(
            customer_totals.items(),
            key=lambda x: x[1],
            reverse=True
        )
    ][:3]  # Top 3 customers
    
    # Print results
    print("Large transactions:")
    for t in transaction_dicts:
        print(f"  Customer {t['customer_id']}: ${t['amount']:.2f} ({t['country']})")
    
    print("\nStatistics by country:")
    for country, stats in country_stats.items():
        print(f"  {country}: ${stats['total']:.2f} total, "
              f"{stats['count']} transactions, "
              f"avg ${stats['average']:.2f}")
    
    print("\nTop customers:")
    for i, cust in enumerate(top_customers, 1):
        print(f"  {i}. Customer {cust['customer_id']}: ${cust['total']:.2f}")

if __name__ == "__main__":
    print("=== List and Dictionary Comprehensions ===\n")
    
    demonstrate_list_comprehensions()
    demonstrate_nested_comprehensions()
    demonstrate_dict_comprehensions()
    demonstrate_set_comprehensions()
    demonstrate_generator_expressions()
    data_processing_pipeline()
    
    print("\n=== Key Takeaways ===")
    print("1. List comprehensions provide a more readable alternative to map/filter")
    print("2. Dictionary and set comprehensions create dictionaries and sets concisely")
    print("3. Generator expressions are memory-efficient for large datasets")
    print("4. Comprehensions can be nested for complex transformations")
    print("5. They're generally preferred in Python for their readability and performance")
