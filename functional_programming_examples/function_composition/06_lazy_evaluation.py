"""
6. Lazy Evaluation with Generators

Demonstrates how to use Python generators and the itertools module
to create lazy evaluation pipelines with function composition.
"""
from __future__ import annotations
from typing import Callable, TypeVar, Any, Iterable, Iterator, Generator, Optional
from functools import partial, reduce
import itertools
import operator
import time

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Compose functions from right to left."""
    def _compose(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return reduce(_compose, funcs, lambda x: x)

def pipe(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Pipe functions from left to right."""
    def _pipe(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *args, **kwargs: g(f(*args, **kwargs))
    return reduce(_pipe, funcs, lambda x: x)

def lazy_map(func: Callable[[T], U]) -> Callable[[Iterable[T]], Iterator[U]]:
    """Create a lazy map function."""
    return lambda iterable: map(func, iterable)

def lazy_filter(predicate: Callable[[T], bool]) -> Callable[[Iterable[T]], Iterator[T]]:
    """Create a lazy filter function."""
    return lambda iterable: filter(predicate, iterable)

def take(n: int) -> Callable[[Iterable[T]], Iterator[T]]:
    """Take n items from an iterable."""
    return lambda iterable: itertools.islice(iterable, n)

def drop(n: int) -> Callable[[Iterable[T]], Iterator[T]]:
    """Drop n items from an iterable."""
    return lambda iterable: itertools.islice(iterable, n, None)

def demonstrate_basic_laziness() -> None:
    """Demonstrate basic lazy evaluation with generators."""
    def trace(iterable: Iterable[T]) -> Generator[T, None, None]:
        """Trace the items flowing through the pipeline."""
        for item in iterable:
            print(f"Processing: {item}")
            yield item
    
    # Create a pipeline of operations
    pipeline = pipe(
        lambda x: range(1, x + 1),  # Generate numbers 1..n
        trace,                      # Trace the numbers
        partial(map, lambda x: x * 2),  # Double each number
        trace,                          # Trace after doubling
        partial(filter, lambda x: x > 5),  # Filter numbers > 5
        trace,                            # Trace after filtering
        list                              # Materialize the result
    )
    
    print("=== Lazy Evaluation Pipeline ===")
    result = pipeline(5)
    print(f"Final result: {result}")

def demonstrate_infinite_sequences() -> None:
    """Demonstrate working with infinite sequences."""
    def natural_numbers(start: int = 0) -> Iterator[int]:
        """Generate natural numbers starting from start."""
        n = start
        while True:
            yield n
            n += 1
    
    # Create a pipeline for processing natural numbers
    pipeline = pipe(
        natural_numbers,                    # Infinite sequence
        partial(map, lambda x: x * 2),     # Double each number
        partial(filter, lambda x: x % 3 == 1),  # Filter numbers ≡ 1 mod 3
        partial(take, 5)                    # Take first 5 results
    )
    
    print("\n=== Processing Infinite Sequence ===")
    result = list(pipeline())
    print(f"First 5 numbers ≡ 1 mod 3 after doubling: {result}")

def demonstrate_chunked_processing() -> None:
    """Demonstrate processing data in chunks."""
    def read_large_file(filename: str, chunk_size: int = 1024) -> Generator[bytes, None, None]:
        """Read a file in chunks."""
        with open(filename, 'rb') as f:
            while chunk := f.read(chunk_size):
                yield chunk
    
    # Simulate processing chunks (e.g., counting lines)
    def process_chunk(chunk: bytes) -> int:
        """Process a chunk of data (count newlines)."""
        return chunk.count(b'\n')
    
    # Create a pipeline for chunked processing
    pipeline = pipe(
        read_large_file,                    # Read file in chunks
        partial(map, process_chunk),        # Process each chunk
        sum                                 # Sum the results
    )
    
    # Create a test file
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as f:
        for _ in range(1000):
            f.write(b"This is a test line.\n")
        test_file = f.name
    
    print("\n=== Chunked File Processing ===")
    try:
        line_count = pipeline(test_file)
        print(f"Total lines: {line_count}")
    finally:
        import os
        os.unlink(test_file)

def demonstrate_complex_pipeline() -> None:
    """Demonstrate a complex lazy evaluation pipeline."""
    from collections import namedtuple
    from itertools import groupby
    from operator import itemgetter
    
    # Define data structures
    Order = namedtuple('Order', ['order_id', 'customer_id', 'amount', 'date'])
    
    # Generate sample data
    def generate_orders(n: int = 100) -> Iterator[Order]:
        """Generate sample order data."""
        import random
        from datetime import datetime, timedelta
        
        for i in range(1, n + 1):
            customer_id = f"CUST{random.randint(1, 10):03d}"
            amount = round(random.uniform(10.0, 1000.0), 2)
            days_ago = random.randint(0, 30)
            date = datetime.now() - timedelta(days=days_ago)
            yield Order(f"ORDER{i:04d}", customer_id, amount, date)
    
    # Define processing functions
    def filter_recent_orders(days: int = 7) -> Callable[[Iterable[Order]], Iterator[Order]]:
        """Filter orders from the last N days."""
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        return lambda orders: (o for o in orders if o.date >= cutoff)
    
    def sum_by_customer(orders: Iterable[Order]) -> Iterator[tuple[str, float]]:
        """Calculate total amount by customer."""
        # Sort by customer_id (required for groupby)
        sorted_orders = sorted(orders, key=lambda o: o.customer_id)
        
        # Group by customer and sum amounts
        for customer_id, group in groupby(sorted_orders, key=lambda o: o.customer_id):
            total = sum(order.amount for order in group)
            yield (customer_id, total)
    
    # Create the pipeline
    pipeline = pipe(
        generate_orders,                    # Generate sample data
        filter_recent_orders(7),            # Last 7 days only
        sum_by_customer,                    # Sum by customer
        partial(sorted, key=itemgetter(1), reverse=True),  # Sort by total (desc)
        partial(take, 5),                    # Top 5 customers
        list                                # Materialize the result
    )
    
    print("\n=== Complex Data Processing Pipeline ===")
    top_customers = pipeline()
    print("Top 5 customers by spend in the last 7 days:")
    for customer_id, total in top_customers:
        print(f"  {customer_id}: ${total:.2f}")

def demonstrate_memory_efficiency() -> None:
    """Demonstrate memory efficiency of lazy evaluation."""
    import sys
    import random
    
    # Generate a large dataset
    def generate_data(n: int) -> Iterator[int]:
        """Generate n random numbers."""
        for _ in range(n):
            yield random.randint(1, 1000)
    
    # Eager processing (creates intermediate lists)
    def eager_processing(data: Iterable[int]) -> list[int]:
        """Process data eagerly with intermediate lists."""
        # Each operation creates a new list
        doubled = [x * 2 for x in data]
        filtered = [x for x in doubled if x % 3 == 0]
        return sorted(filtered, reverse=True)[:10]
    
    # Lazy processing (uses generators)
    def lazy_processing(data: Iterable[int]) -> list[int]:
        """Process data lazily with generators."""
        return list(pipe(
            data,
            partial(map, lambda x: x * 2),          # Double each number
            partial(filter, lambda x: x % 3 == 0),   # Filter multiples of 3
            partial(sorted, reverse=True),           # Sort in descending order
            partial(take, 10)                        # Take top 10
        )())
    
    # Test with a large dataset
    n = 1_000_000
    print(f"\n=== Memory Efficiency (n={n:,}) ===")
    
    # Measure memory usage with eager processing
    data = list(generate_data(n))  # Materialize the data
    
    import tracemalloc
    
    # Eager processing
    tracemalloc.start()
    result_eager = eager_processing(data)
    current, peak = tracemalloc.get_traced_memory()
    print(f"Eager processing - Peak memory usage: {peak / 1024:.2f} KB")
    tracemalloc.stop()
    
    # Lazy processing
    tracemalloc.start()
    result_lazy = lazy_processing(generate_data(n))  # Pass generator directly
    current, peak = tracemalloc.get_traced_memory()
    print(f"Lazy processing - Peak memory usage: {peak / 1024:.2f} KB")
    tracemalloc.stop()
    
    # Verify results are the same
    assert result_eager == result_lazy, "Results don't match!"
    print("Results match!")

if __name__ == "__main__":
    print("=== Lazy Evaluation with Generators ===")
    demonstrate_basic_laziness()
    demonstrate_infinite_sequences()
    demonstrate_chunked_processing()
    demonstrate_complex_pipeline()
    demonstrate_memory_efficiency()
    
    print("\n=== Key Takeaways ===")
    print("1. Generators enable lazy evaluation, processing items one at a time")
    print("2. Lazy evaluation is memory efficient, especially for large datasets")
    print("3. itertools provides powerful tools for working with iterators")
    print("4. Pipelines can process infinite or very large datasets")
    print("5. Chunking helps process large files without loading everything into memory")
