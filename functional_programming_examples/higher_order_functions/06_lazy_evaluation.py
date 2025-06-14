"""
6. Lazy Evaluation with Higher-Order Functions

Demonstrates how to implement and use lazy evaluation with generators
and higher-order functions for efficient data processing.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Iterable, Iterator, Any, Optional
from functools import partial
import time

T = TypeVar('T')
U = TypeVar('U')

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
    
    def to_list(self) -> list[T]:
        return list(self._iterable)
    
    def reduce(self, f: Callable[[U, T], U], initial: U) -> U:
        result = initial
        for item in self._iterable:
            result = f(result, item)
        return result

def lazy_range(start: int, stop: Optional[int] = None, step: int = 1) -> LazySequence[int]:
    """Create a lazy sequence of numbers."""
    def generate() -> Iterator[int]:
        if stop is None:
            # Single argument case: range(stop)
            current = 0
            while current < start:
                yield current
                current += step
        else:
            # Two or three arguments: range(start, stop[, step])
            current = start
            while current < stop:
                yield current
                current += step
    return LazySequence(generate())

def demonstrate_lazy_evaluation() -> None:
    """Demonstrate lazy evaluation with a large dataset."""
    print("=== Lazy Evaluation with Higher-Order Functions ===\n")
    
    # Create a large sequence (1 million numbers)
    print("Creating a lazy sequence of 1,000,000 numbers...")
    numbers = lazy_range(1, 1_000_001)
    
    # Chain operations (no computation happens yet)
    print("Chaining operations (map, filter, take)...")
    result = (
        numbers
        .map(lambda x: x * 2)          # Double each number
        .filter(lambda x: x % 3 == 0)   # Keep only multiples of 3
        .take(10)                       # Take first 10 results
    )
    
    # The computation happens only when we consume the sequence
    print("Computing results...")
    start_time = time.perf_counter()
    computed = result.to_list()
    end_time = time.perf_counter()
    
    print(f"First 10 even multiples of 3: {computed}")
    print(f"Computed in {end_time - start_time:.6f} seconds")
    
    # Compare with eager evaluation
    print("\n=== Eager vs Lazy Comparison ===\n")
    
    # Eager evaluation (creates full lists in memory)
    print("Eager evaluation (creates intermediate lists):")
    start_time = time.perf_counter()
    
    # This would create 3 full lists in memory
    eager_result = list(
        range(1, 1_000_001)
    )
    mapped = [x * 2 for x in eager_result]
    filtered = [x for x in mapped if x % 3 == 0]
    taken = filtered[:10]
    
    end_time = time.perf_counter()
    print(f"First 10 even multiples of 3 (eager): {taken}")
    print(f"Eager evaluation took: {end_time - start_time:.6f} seconds")
    
    # Lazy evaluation (generators)
    print("\nLazy evaluation (uses generators):")
    start_time = time.perf_counter()
    
    # This creates generator expressions (no intermediate lists)
    lazy_result = (
        x * 2 for x in range(1, 1_000_001)
    )
    lazy_filtered = (x for x in lazy_result if x % 3 == 0)
    lazy_taken = []
    
    # Only compute what we need
    for i, x in enumerate(lazy_filtered):
        if i >= 10:
            break
        lazy_taken.append(x)
    
    end_time = time.perf_counter()
    print(f"First 10 even multiples of 3 (lazy): {lazy_taken}")
    print(f"Lazy evaluation took: {end_time - start_time:.6f} seconds")

def demonstrate_infinite_sequences() -> None:
    """Demonstrate working with potentially infinite sequences."""
    print("\n=== Infinite Sequences ===\n")
    
    def fibonacci() -> Iterator[int]:
        """Generate an infinite sequence of Fibonacci numbers."""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    # Create a lazy sequence from the infinite generator
    fib = LazySequence(fibonacci())
    
    # Process the infinite sequence (but only take what we need)
    result = (
        fib
        .filter(lambda x: x % 2 == 0)  # Only even numbers
        .map(lambda x: x * 2)           # Double them
        .take(10)                       # Take first 10
        .to_list()                      # Materialize the result
    )
    
    print(f"First 10 doubled even Fibonacci numbers: {result}")

def demonstrate_chunked_processing() -> None:
    """Demonstrate processing data in chunks for memory efficiency."""
    print("\n=== Chunked Processing ===\n")
    
    def read_large_file(file_path: str, chunk_size: int = 1024) -> Iterator[bytes]:
        """Read a file in chunks."""
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    # Simulate processing a large file
    print("Simulating processing a large file in chunks...")
    
    # Create a large file in memory for demonstration
    large_data = b'Hello, world!\n' * 100000  # ~1.3MB of data
    
    # Process the data in chunks without loading it all into memory
    chunk_size = 1024  # 1KB chunks
    
    # Create a lazy sequence of chunks
    chunks = LazySequence(read_large_file_from_memory(large_data, chunk_size))
    
    # Process each chunk (e.g., count lines)
    total_lines = chunks.map(lambda chunk: chunk.count(b'\n'))\
                        .reduce(lambda x, y: x + y, 0)
    
    print(f"Total lines in the file: {total_lines}")

def read_large_file_from_memory(data: bytes, chunk_size: int) -> Iterator[bytes]:
    """Helper to simulate reading chunks from memory."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

if __name__ == "__main__":
    demonstrate_lazy_evaluation()
    demonstrate_infinite_sequences()
    demonstrate_chunked_processing()
    
    print("\n=== Key Takeaways ===")
    print("1. Lazy evaluation defers computation until results are needed")
    print("2. Generators allow processing large/infinite sequences with minimal memory")
    print("3. Chain operations without creating intermediate data structures")
    print("4. Process data in chunks to handle large files efficiently")
