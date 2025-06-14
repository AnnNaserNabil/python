"""
10. Advanced Composition Patterns and Performance

Explores advanced function composition patterns, optimization techniques,
and performance considerations when building functional pipelines in Python.
"""
from __future__ import annotations
from typing import (
    TypeVar, Callable, Any, Dict, List, Tuple, Iterator, Iterable, 
    Optional, Union, Generic, cast, Type, Sequence
)
from functools import partial, reduce, lru_cache, wraps
import time
import inspect
from dataclasses import dataclass
from collections import defaultdict, deque
import random
import sys
import math

# Type variables for generic functions
T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')
E = TypeVar('E', bound=Exception)

# 1. Memoization and Caching

def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """Memoize a function's return value based on its arguments."""
    cache = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper

class Memoized(Generic[T]):
    """A memoized computation that's only evaluated once."""
    
    def __init__(self, func: Callable[[], T]):
        self.func = func
        self._cached: Optional[T] = None
        self._computed = False
    
    def __call__(self) -> T:
        if not self._computed:
            self._cached = self.func()
            self._computed = True
        return cast(T, self._cached)

# 2. Lazy Evaluation

class Lazy(Generic[T]):
    """A lazy computation that's only evaluated when needed."""
    
    def __init__(self, func: Callable[[], T]):
        self.func = func
        self._cached: Optional[T] = None
        self._computed = False
    
    def __call__(self) -> T:
        if not self._computed:
            self._cached = self.func()
            self._computed = True
        return cast(T, self._cached)
    
    def map(self, f: Callable[[T], U]) -> 'Lazy[U]':
        return Lazy(lambda: f(self()))
    
    def bind(self, f: Callable[[T], 'Lazy[U]']) -> 'Lazy[U]':
        return Lazy(lambda: f(self())())

# 3. Function Composition with Caching

def cached_compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """
    Compose functions with cached intermediate results.
    
    This is useful when the same intermediate values are used multiple times.
    """
    if not funcs:
        return lambda x: x
    
    # Create a cache for each function
    caches = [{} for _ in funcs]
    
    def composed(*args: Any, **kwargs: Any) -> Any:
        # Start with the last function
        result = funcs[-1](*args, **kwargs)
        
        # Apply functions in reverse order (from right to left)
        for i in range(len(funcs)-2, -1, -1):
            # Create a key for the cache
            key = (result,)
            
            # Check cache
            if key in caches[i]:
                result = caches[i][key]
            else:
                # Compute and cache
                result = funcs[i](result)
                caches[i][key] = result
                
        return result
    
    return composed

# 4. Pipeline Optimization

class Pipeline(Generic[T, U]):
    """An optimized pipeline with support for fusion and other optimizations."""
    
    def __init__(self, func: Callable[[T], U]):
        self.func = func
    
    def __call__(self, x: T) -> U:
        return self.func(x)
    
    def then(self, other: Callable[[U], V]) -> 'Pipeline[T, V]':
        """Compose this pipeline with another function."""
        return Pipeline(lambda x: other(self.func(x)))
    
    def __or__(self, other: Callable[[U], V]) -> 'Pipeline[T, V]':
        """Operator version of then."""
        return self.then(other)
    
    def fuse(self) -> 'Pipeline[T, U]':
        """
        Optimize the pipeline by fusing adjacent operations when possible.
        This is a simplified version - in practice, you'd want to analyze
        the operations and apply specific optimizations.
        """
        return self  # In a real implementation, this would perform fusion
    
    def parallelize(self, num_workers: int = 4) -> 'Pipeline[T, U]':
        """
        Process items in parallel using multiple workers.
        This is a simplified version - in practice, you'd use concurrent.futures or similar.
        """
        def parallel_processor(items: Iterable[T]) -> Iterable[U]:
            # In a real implementation, this would use a thread/process pool
            return map(self.func, items)
        
        return Pipeline(parallel_processor)

# 5. Lazy Sequences

class LazySequence(Generic[T]):
    """A lazy sequence that supports functional operations with deferred execution."""
    
    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._iterable)
    
    def map(self, f: Callable[[T], U]) -> 'LazySequence[U]':
        return LazySequence(map(f, self._iterable))
    
    def filter(self, predicate: Callable[[T], bool]) -> 'LazySequence[T]':
        return LazySequence(filter(predicate, self._iterable))
    
    def take(self, n: int) -> 'LazySequence[T]':
        def take_n(iterable: Iterable[T]) -> Iterable[T]:
            it = iter(iterable)
            for _ in range(n):
                try:
                    yield next(it)
                except StopIteration:
                    break
        return LazySequence(take_n(self._iterable))
    
    def to_list(self) -> List[T]:
        return list(self._iterable)
    
    def reduce(self, f: Callable[[U, T], U], initial: U) -> U:
        return reduce(f, self._iterable, initial)

# 6. Performance Profiling

def profile(func: Callable[..., T]) -> Callable[..., T]:
    """A simple profiling decorator."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds")
        return result
    return wrapper

# 7. Example: Optimized Data Processing Pipeline

def process_data_pipeline() -> None:
    """Demonstrate an optimized data processing pipeline."""
    print("=== Optimized Data Processing Pipeline ===")
    
    # Generate a large dataset
    def generate_data(n: int) -> Iterable[Dict[str, Any]]:
        """Generate random e-commerce transaction data."""
        products = [
            ("Laptop", 999.99),
            ("Phone", 699.99),
            ("Tablet", 349.99),
            ("Headphones", 199.99),
            ("Monitor", 249.99),
        ]
        
        for i in range(n):
            product_name, price = random.choice(products)
            yield {
                'transaction_id': f"TXN{10000 + i}",
                'customer_id': f"CUST{random.randint(1, 1000):04d}",
                'product': product_name,
                'quantity': random.randint(1, 5),
                'unit_price': price,
                'date': f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                'discount': random.choice([0, 0, 0, 0.1, 0.15, 0.2])
            }
    
    # Define processing steps with optimizations
    
    @memoize
    def calculate_total(record: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate the total price with discount."""
        subtotal = record['quantity'] * record['unit_price']
        discount = subtotal * record['discount']
        return {**record, 'total': subtotal - discount}
    
    def filter_high_value(record: Dict[str, Any]) -> bool:
        """Filter high-value transactions."""
        return record.get('total', 0) > 500
    
    def aggregate_by_month(records: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Aggregate sales by month."""
        monthly_sales: Dict[str, Dict[str, float]] = defaultdict(lambda: {
            'total_sales': 0.0,
            'transaction_count': 0,
            'avg_order_value': 0.0
        })
        
        for record in records:
            month = record['date'][:7]  # YYYY-MM
            monthly_sales[month]['total_sales'] += record['total']
            monthly_sales[month]['transaction_count'] += 1
        
        # Calculate averages
        for month in monthly_sales:
            monthly_sales[month]['avg_order_value'] = (
                monthly_sales[month]['total_sales'] / 
                monthly_sales[month]['transaction_count']
            )
        
        return dict(monthly_sales)
    
    # Build and run the pipeline
    print("Generating data...")
    data = list(generate_data(1_000_000))  # 1M records
    
    print("Processing...")
    
    # Time the pipeline
    start_time = time.perf_counter()
    
    # Process using lazy evaluation and composition
    result = (
        LazySequence(data)
        .map(calculate_total)  # Calculate totals (memoized)
        .filter(filter_high_value)  # Filter high-value transactions
        .to_list()  # Materialize for aggregation
    )
    
    # Aggregate results
    monthly_report = aggregate_by_month(result)
    
    end_time = time.perf_counter()
    
    # Print results
    print(f"Processed {len(data):,} records in {end_time - start_time:.2f} seconds")
    print(f"Found {len(result):,} high-value transactions")
    
    print("\nMonthly Sales Report:")
    for month, stats in sorted(monthly_report.items()):
        print(f"{month}: ${stats['total_sales']:,.2f} "
              f"({stats['transaction_count']} transactions, "
              f"avg: ${stats['avg_order_value']:,.2f})")

# 8. Advanced: Function Composition with Type Checking

def typed_compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Compose functions with runtime type checking."""
    # This is a simplified version - in practice, you'd want to use
    # a library like typeguard or implement more sophisticated type checking
    
    def composed(*args: Any, **kwargs: Any) -> Any:
        # Start with the last function
        result = funcs[-1](*args, **kwargs)
        
        # Apply functions in reverse order (from right to left)
        for f in reversed(funcs[:-1]):
            result = f(result)
            
        return result
    
    return composed

# 9. Example: Parallel Processing

def parallel_map(
    func: Callable[[T], U], 
    items: Iterable[T], 
    num_workers: int = 4
) -> Iterable[U]:
    """
    A simple parallel map implementation.
    In production, consider using concurrent.futures.ProcessPoolExecutor.
    """
    from multiprocessing import Pool
    
    with Pool(num_workers) as pool:
        yield from pool.map(func, items)

# 10. Example: Caching with LRU

@lru_cache(maxsize=128)
def expensive_computation(x: int, y: int) -> int:
    """A computation that's expensive to perform."""
    print(f"Computing {x} + {y}...")
    time.sleep(0.1)  # Simulate work
    return x + y

def demonstrate_caching() -> None:
    """Demonstrate the benefits of caching."""
    print("\n=== Caching Demonstration ===")
    
    # First call - will compute
    start_time = time.perf_counter()
    result1 = expensive_computation(3, 4)
    end_time = time.perf_counter()
    print(f"Result: {result1}, took {end_time - start_time:.4f}s")
    
    # Same call again - will use cache
    start_time = time.perf_counter()
    result2 = expensive_computation(3, 4)
    end_time = time.perf_counter()
    print(f"Result: {result2}, took {end_time - start_time:.4f}s (cached)")
    
    # Different call - will compute again
    start_time = time.perf_counter()
    result3 = expensive_computation(5, 6)
    end_time = time.perf_counter()
    print(f"Result: {result3}, took {end_time - start_time:.4f}s")

if __name__ == "__main__":
    print("=== Advanced Function Composition Patterns ===\n")
    
    # Run the examples
    demonstrate_caching()
    
    # Uncomment to run the data processing pipeline (may take a while)
    # process_data_pipeline()
    
    print("\n=== Key Takeaways ===")
    print("1. Use memoization and caching to avoid redundant computations")
    print("2. Leverage lazy evaluation for efficient processing of large datasets")
    print("3. Consider parallel processing for CPU-bound operations")
    print("4. Use type hints and runtime checking for safer function composition")
    print("5. Profile your code to identify and optimize bottlenecks")
    print("6. Consider using specialized libraries like Dask or PySpark for big data")
    print("7. Always measure performance before and after optimizations")
