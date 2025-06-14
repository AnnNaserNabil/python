"""
4. Performance Considerations with Map, Filter, and Reduce

Explores the performance characteristics of map, filter, and reduce operations,
including comparisons with loops and comprehensions, memory usage, and optimization techniques.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Iterable, Any, List, Dict, Tuple, Optional
from functools import reduce
import timeit
import sys
import tracemalloc
import random
import math
from memory_profiler import profile

T = TypeVar('T')
U = TypeVar('U')

# 1. Performance Comparison: Map vs List Comprehension

def time_functions() -> None:
    """Compare execution time of map vs list comprehension."""
    print("=== Performance Comparison: Map vs List Comprehension ===\n")
    
    # Test with a large dataset
    data = list(range(1_000_000))
    
    # Function to test
    def square(x: int) -> int:
        return x ** 2
    
    # Time list comprehension
    list_comp_time = timeit.timeit(
        '[x ** 2 for x in data]',
        globals=globals(),
        number=10
    )
    
    # Time map with lambda
    map_lambda_time = timeit.timeit(
        'list(map(lambda x: x ** 2, data))',
        globals=globals(),
        number=10
    )
    
    # Time map with named function
    map_func_time = timeit.timeit(
        'list(map(square, data))',
        globals=globals(),
        number=10
    )
    
    # Time for loop
    for_loop_time = timeit.timeit(
        """
        result = []
        for x in data:
            result.append(x ** 2)
        """,
        globals=globals(),
        number=10
    )
    
    print(f"List comprehension: {list_comp_time:.4f} seconds")
    print(f"Map with lambda: {map_lambda_time:.4f} seconds")
    print(f"Map with named function: {map_func_time:.4f} seconds")
    print(f"For loop: {for_loop_time:.4f} seconds")
    
    # Winner
    times = {
        'list_comp': list_comp_time,
        'map_lambda': map_lambda_time,
        'map_func': map_func_time,
        'for_loop': for_loop_time
    }
    fastest = min(times, key=times.get)  # type: ignore
    print(f"\nFastest approach: {fastest} ({times[fastest]:.4f} seconds)")

# 2. Memory Usage Comparison

def compare_memory_usage() -> None:
    """Compare memory usage of different approaches."""
    print("\n=== Memory Usage Comparison ===\n")
    
    # Large dataset
    data = list(range(1_000_000))
    
    def square(x: int) -> int:
        return x ** 2
    
    # Memory profiling function
    def profile_memory(desc: str, func: Callable[[], Any]) -> None:
        print(f"{desc}:")
        
        # Get memory before
        tracemalloc.start()
        
        # Execute the function
        result = func()
        
        # Get memory after
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Clean up
        if hasattr(result, '__iter__') and not isinstance(result, (str, bytes)):
            _ = list(result)  # Consume generator if needed
        
        print(f"  Peak memory usage: {peak / 1024 / 1024:.2f} MB")
    
    # Test different approaches
    profile_memory(
        "List comprehension",
        lambda: [x ** 2 for x in data]
    )
    
    profile_memory(
        "Map with lambda (list)",
        lambda: list(map(lambda x: x ** 2, data))
    )
    
    profile_memory(
        "Map with lambda (generator)",
        lambda: map(lambda x: x ** 2, data)
    )
    
    profile_memory(
        "Generator expression",
        lambda: (x ** 2 for x in data)
    )

# 3. Lazy Evaluation with Generators

def demonstrate_lazy_evaluation() -> None:
    """Show the benefits of lazy evaluation with generators."""
    print("\n=== Lazy Evaluation with Generators ===\n")
    
    # A function that simulates a slow operation
    def slow_square(x: int) -> int:
        time.sleep(0.001)  # Simulate work
        return x ** 2
    
    # Eager evaluation (list comprehension)
    print("Eager evaluation (list comprehension):")
    start = time.time()
    
    # Process all items first, then take first 5
    result = [slow_square(x) for x in range(10)][:5]
    print(f"  Result: {result}")
    print(f"  Time taken: {time.time() - start:.4f} seconds")
    
    # Lazy evaluation (generator expression)
    print("\nLazy evaluation (generator expression):")
    start = time.time()
    
    # Only process first 5 items
    result = list(slow_square(x) for x in range(10))[:5]
    print(f"  Result: {result}")
    print(f"  Time taken: {time.time() - start:.4f} seconds")
    
    # Using islice for better lazy evaluation
    from itertools import islice
    
    print("\nUsing islice for lazy evaluation:")
    start = time.time()
    
    # Only process first 5 items
    result = list(islice((slow_square(x) for x in range(10)), 5))
    print(f"  Result: {result}")
    print(f"  Time taken: {time.time() - start:.4f} seconds")

# 4. Optimizing with Built-in Functions

def optimize_with_builtins() -> None:
    """Show how to optimize with built-in functions."""
    print("\n=== Optimizing with Built-in Functions ===\n")
    
    # Large dataset
    data = [random.random() * 100 for _ in range(1_000_000)]
    
    # 4.1 Using sum() vs reduce()
    print("Summing numbers:")
    
    # Using sum()
    start = time.time()
    total = sum(data)
    sum_time = time.time() - start
    print(f"  sum(): {sum_time:.6f} seconds")
    
    # Using reduce()
    start = time.time()
    total_reduce = reduce(lambda x, y: x + y, data, 0)
    reduce_time = time.time() - start
    print(f"  reduce(): {reduce_time:.6f} seconds")
    print(f"  Speedup: {reduce_time / sum_time:.2f}x")
    
    # 4.2 Using max() vs reduce()
    print("\nFinding maximum:")
    
    # Using max()
    start = time.time()
    max_val = max(data)
    max_time = time.time() - start
    print(f"  max(): {max_time:.6f} seconds")
    
    # Using reduce()
    start = time.time()
    max_reduce = reduce(lambda a, b: a if a > b else b, data)
    reduce_time = time.time() - start
    print(f"  reduce(): {reduce_time:.6f} seconds")
    print(f"  Speedup: {reduce_time / max_time:.2f}x")
    
    # 4.3 Using any() and all()
    print("\nChecking conditions:")
    
    # Check if any number is negative
    start = time.time()
    has_negative = any(x < 0 for x in data)
    any_time = time.time() - start
    print(f"  any(): {any_time:.6f} seconds")
    
    # Check if all numbers are positive
    start = time.time()
    all_positive = all(x >= 0 for x in data)
    all_time = time.time() - start
    print(f"  all(): {all_time:.6f} seconds")

# 5. Memory-Efficient Processing

def memory_efficient_processing() -> None:
    """Demonstrate memory-efficient processing techniques."""
    print("\n=== Memory-Efficient Processing ===\n")
    
    # 5.1 Processing large files line by line
    print("Processing large files:")
    
    # Create a large file for testing
    with open('large_data.txt', 'w') as f:
        for i in range(1_000_000):
            f.write(f"This is line {i}: {random.random()}\n")
    
    # Memory-inefficient approach (reading entire file into memory)
    print("\nMemory-inefficient approach (readlines):")
    start = time.time()
    with open('large_data.txt', 'r') as f:
        lines = f.readlines()  # Reads entire file into memory
        line_count = len(lines)
    print(f"  Lines processed: {line_count}")
    print(f"  Memory used: {sys.getsizeof(lines) / 1024 / 1024:.2f} MB")
    print(f"  Time taken: {time.time() - start:.4f} seconds")
    
    # Memory-efficient approach (process line by line)
    print("\nMemory-efficient approach (line by line):")
    start = time.time()
    line_count = 0
    with open('large_data.txt', 'r') as f:
        for line in f:  # Processes one line at a time
            line_count += 1
            # Process the line
            _ = line.strip()
    print(f"  Lines processed: {line_count}")
    print(f"  Memory used: Minimal (only one line in memory at a time)")
    print(f"  Time taken: {time.time() - start:.4f} seconds")
    
    # Clean up
    import os
    os.remove('large_data.txt')
    
    # 5.2 Using generator expressions for large datasets
    print("\nProcessing large datasets with generator expressions:")
    
    def process_data(data: Iterable[int]) -> float:
        """Process data in a memory-efficient way."""
        # Generator expression processes one item at a time
        squared = (x ** 2 for x in data)
        filtered = (x for x in squared if x % 2 == 0)
        return sum(filtered) / 1_000_000  # Some aggregation
    
    # Generate data on the fly without storing it all in memory
    data_generator = (random.randint(1, 100) for _ in range(10_000_000))
    
    start = time.time()
    result = process_data(data_generator)
    print(f"  Result: {result:.2f}")
    print(f"  Memory used: Minimal (generators process one item at a time)")
    print(f"  Time taken: {time.time() - start:.4f} seconds")

# 6. Practical Example: Optimizing Data Processing

def optimize_data_processing() -> None:
    """Demonstrate optimizing a data processing pipeline."""
    print("\n=== Optimizing a Data Processing Pipeline ===\n")
    
    # Generate sample data: 1 million records with random values
    data = [
        {
            'id': i,
            'value': random.random() * 100,
            'category': random.choice(['A', 'B', 'C', 'D']),
            'active': random.choice([True, False])
        }
        for i in range(1_000_000)
    ]
    
    # Task: Calculate average value for each category, but only for active items
    
    # 6.1 Naive approach (inefficient)
    print("Naive approach (multiple passes):")
    start = time.time()
    
    # Get unique categories
    categories = set(item['category'] for item in data)
    
    # Calculate averages
    result = {}
    for category in categories:
        # Filter active items
        active_items = [item for item in data if item['active'] and item['category'] == category]
        
        if active_items:
            # Calculate average
            total = sum(item['value'] for item in active_items)
            count = len(active_items)
            result[category] = total / count
    
    naive_time = time.time() - start
    print(f"  Result: {result}")
    print(f"  Time taken: {naive_time:.4f} seconds")
    
    # 6.2 Optimized approach (single pass)
    print("\nOptimized approach (single pass):")
    start = time.time()
    
    # Use a dictionary to store sums and counts
    category_stats: Dict[str, Tuple[float, int]] = {}
    
    for item in data:
        if item['active']:
            category = item['category']
            value = item['value']
            
            # Update category stats
            if category in category_stats:
                total, count = category_stats[category]
                category_stats[category] = (total + value, count + 1)
            else:
                category_stats[category] = (value, 1)
    
    # Calculate averages
    result_optimized = {
        category: total / count
        for category, (total, count) in category_stats.items()
    }
    
    optimized_time = time.time() - start
    print(f"  Result: {result_optimized}")
    print(f"  Time taken: {optimized_time:.4f} seconds")
    print(f"  Speedup: {naive_time / optimized_time:.2f}x")
    
    # 6.3 Using built-in functions for further optimization
    print("\nUsing built-in functions for optimization:")
    start = time.time()
    
    # Use filter and groupby
    from itertools import groupby
    from operator import itemgetter
    
    # Filter active items
    active_items = filter(lambda x: x['active'], data)
    
    # Sort by category (required for groupby)
    sorted_items = sorted(active_items, key=itemgetter('category'))
    
    # Group by category and calculate averages
    result_builtin = {}
    for category, group in groupby(sorted_items, key=itemgetter('category')):
        values = [item['value'] for item in group]
        result_builtin[category] = sum(values) / len(values)
    
    builtin_time = time.time() - start
    print(f"  Result: {result_builtin}")
    print(f"  Time taken: {builtin_time:.4f} seconds")
    print(f"  Speedup vs naive: {naive_time / builtin_time:.2f}x")

if __name__ == "__main__":
    print("=== Performance Considerations with Map, Filter, and Reduce ===\n")
    
    time_functions()
    compare_memory_usage()
    demonstrate_lazy_evaluation()
    optimize_with_builtins()
    memory_efficient_processing()
    optimize_data_processing()
    
    print("\n=== Key Takeaways ===")
    print("1. List comprehensions are often faster than map+lambda for simple operations")
    print("2. Generator expressions are memory-efficient for large datasets")
    print("3. Built-in functions (sum, max, any, all) are highly optimized")
    print("4. Processing data in a single pass is often more efficient")
    print("5. Consider memory usage when working with large datasets")
    print("6. Profile before optimizing - focus on bottlenecks")
