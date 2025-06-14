"""
7. Concurrent Processing with Map, Filter, and Reduce

This module demonstrates how to use map, filter, and reduce with concurrent execution
for improved performance, including thread pools, process pools, and asyncio.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Iterable, Any, List, Dict, Tuple, Optional, AsyncIterable, Iterator
from functools import reduce, partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import asyncio
import time
import math
import random
import os
import multiprocessing as mp
from pathlib import Path
import csv
import json
import urllib.request
from urllib.parse import urlparse
import aiohttp
import aiofiles

T = TypeVar('T')
U = TypeVar('U')

# 1. Thread Pool Executor

def process_with_threads(
    func: Callable[[T], U],
    items: Iterable[T],
    max_workers: Optional[int] = None
) -> List[U]:
    """
    Process items in parallel using a thread pool.
    Best for I/O-bound tasks.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(func, items))

# 2. Process Pool Executor

def process_with_processes(
    func: Callable[[T], U],
    items: Iterable[T],
    max_workers: Optional[int] = None,
    chunksize: int = 1
) -> List[U]:
    """
    Process items in parallel using a process pool.
    Best for CPU-bound tasks.
    """
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(func, items, chunksize=chunksize))

# 3. Asynchronous Processing

async def process_async(
    func: Callable[[T], Awaitable[U]],
    items: Iterable[T],
    max_concurrent: int = 10
) -> List[U]:
    """
    Process items asynchronously with a semaphore to limit concurrency.
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_item(item: T) -> U:
        async with semaphore:
            return await func(item)
    
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

# 4. Parallel Map Implementation

def parallel_map(
    func: Callable[[T], U],
    iterable: Iterable[T],
    executor_type: str = 'thread',
    max_workers: Optional[int] = None,
    chunksize: int = 1
) -> Iterator[U]:
    """
    A parallel version of map that can use threads or processes.
    
    Args:
        func: Function to apply to each item
        iterable: Items to process
        executor_type: 'thread' or 'process'
        max_workers: Maximum number of workers
        chunksize: Number of items to process in each worker (for ProcessPool)
    """
    executor_class = ThreadPoolExecutor if executor_type == 'thread' else ProcessPoolExecutor
    
    with executor_class(max_workers=max_workers) as executor:
        yield from executor.map(func, iterable, chunksize=chunksize)

# 5. Parallel Filter Implementation

def parallel_filter(
    predicate: Callable[[T], bool],
    iterable: Iterable[T],
    executor_type: str = 'thread',
    max_workers: Optional[int] = None
) -> Iterator[T]:
    """
    A parallel version of filter.
    """
    # First, evaluate the predicate in parallel
    with ThreadPoolExecutor(max_workers=max_workers) if executor_type == 'thread' else ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Create a list of (item, future) pairs
        future_item_pairs = [
            (item, executor.submit(predicate, item))
            for item in iterable
        ]
        
        # Yield items where predicate is True
        for item, future in future_item_pairs:
            if future.result():
                yield item

# 6. Parallel Reduce Implementation

def parallel_reduce(
    func: Callable[[T, T], T],
    iterable: Iterable[T],
    executor_type: str = 'thread',
    max_workers: Optional[int] = None,
    chunksize: int = 1000
) -> T:
    """
    A parallel version of reduce using a tree reduction pattern.
    The function must be associative for correct results.
    """
    items = list(iterable)
    
    if not items:
        raise TypeError("reduce() of empty sequence with no initial value")
    
    if len(items) == 1:
        return items[0]
    
    # If the chunk is small, do a sequential reduce
    if len(items) <= chunksize:
        return reduce(func, items)
    
    # Split the work into chunks and process in parallel
    executor_class = ThreadPoolExecutor if executor_type == 'thread' else ProcessPoolExecutor
    
    with executor_class(max_workers=max_workers) as executor:
        # Process chunks in parallel
        chunk_results = list(executor.map(
            lambda chunk: reduce(func, chunk),
            (items[i:i + chunksize] for i in range(0, len(items), chunksize))
        ))
        
        # Recursively reduce the results
        return parallel_reduce(func, chunk_results, executor_type, max_workers, chunksize)

# 7. Real-world Example: Parallel Web Scraping

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Tuple[str, str]:
    """Fetch a URL and return its content."""
    try:
        async with session.get(url, timeout=10) as response:
            return url, await response.text()
    except Exception as e:
        return url, f"Error: {str(e)}"

async def scrape_websites(urls: List[str], max_concurrent: int = 10) -> Dict[str, str]:
    """Scrape multiple websites concurrently."""
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(results)

# 8. Real-world Example: Parallel File Processing

def process_file(file_path: Path) -> Dict[str, Any]:
    """Process a single file and return statistics."""
    try:
        # Simulate processing time
        time.sleep(0.1)
        
        # Get file stats
        stat = file_path.stat()
        
        # Count lines (for text files)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
        except (UnicodeDecodeError, PermissionError):
            line_count = 0
        
        return {
            'path': str(file_path),
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': stat.st_mtime,
            'line_count': line_count,
            'status': 'success'
        }
    except Exception as e:
        return {
            'path': str(file_path),
            'error': str(e),
            'status': 'error'
        }

async def process_files_parallel(directory: str, pattern: str = '*.py', 
                               max_workers: int = None) -> List[Dict[str, Any]]:
    """Process multiple files in parallel."""
    path = Path(directory)
    files = list(path.glob('**/' + pattern))
    
    # Use process pool for CPU-bound tasks
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_file, file)
            for file in files
        ]
        
        return await asyncio.gather(*tasks)

# 9. Real-world Example: Data Processing Pipeline

@dataclass
class DataRecord:
    """Represents a data record in our processing pipeline."""
    id: int
    value: float
    category: str
    timestamp: float
    processed: bool = False
    error: Optional[str] = None

def process_data_pipeline(
    records: List[DataRecord],
    max_workers: Optional[int] = None
) -> Tuple[List[DataRecord], Dict[str, Any]]:
    """
    Process data records through a parallel pipeline:
    1. Validate records
    2. Transform values
    3. Categorize
    4. Aggregate results
    """
    def validate_record(record: DataRecord) -> DataRecord:
        """Validate the record (I/O bound)."""
        time.sleep(0.01)  # Simulate I/O
        if record.value < 0:
            record.error = "Negative value not allowed"
        return record
    
    def transform_value(record: DataRecord) -> DataRecord:
        """Transform the value (CPU bound)."""
        if record.error:
            return record
        
        # Simulate CPU-intensive transformation
        for _ in range(1000):
            record.value = math.sqrt(record.value ** 2)
        
        record.value = round(record.value, 2)
        return record
    
    def categorize(record: DataRecord) -> DataRecord:
        """Categorize the record."""
        if record.error:
            return record
            
        if record.value > 1000:
            record.category = "high"
        elif record.value > 100:
            record.category = "medium"
        else:
            record.category = "low"
        
        record.processed = True
        return record
    
    # Process records in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Stage 1: Validate (I/O bound)
        validated = list(executor.map(validate_record, records))
        
        # Stage 2: Transform (CPU bound)
        with ProcessPoolExecutor(max_workers=max_workers) as process_executor:
            transformed = list(process_executor.map(transform_value, validated))
        
        # Stage 3: Categorize
        categorized = list(executor.map(categorize, transformed))
        
        # Calculate statistics
        valid_records = [r for r in categorized if r.processed]
        errors = [r for r in categorized if r.error]
        
        stats = {
            'total': len(categorized),
            'processed': len(valid_records),
            'errors': len(errors),
            'categories': Counter(r.category for r in valid_records),
            'avg_value': statistics.mean(r.value for r in valid_records) if valid_records else 0,
        }
        
        return categorized, stats

# 10. Benchmarking and Comparison

def benchmark_operations() -> None:
    """Benchmark different processing approaches."""
    print("=== Benchmarking Different Processing Approaches ===\n")
    
    # Generate test data
    data = [i for i in range(1, 1001)]
    
    # Function to test (CPU-bound)
    def process_item(x: int) -> float:
        return math.sqrt(x ** 2 + 1) * math.sin(x) / math.cos(x) if x % 2 == 0 else math.log(x + 1)
    
    # 1. Sequential processing
    print("1. Sequential Processing")
    start = time.time()
    results_seq = list(map(process_item, data))
    seq_time = time.time() - start
    print(f"  Time: {seq_time:.4f} seconds")
    
    # 2. Thread pool (not ideal for CPU-bound tasks due to GIL)
    print("\n2. Thread Pool (not optimal for CPU-bound)")
    start = time.time()
    with ThreadPoolExecutor() as executor:
        results_thread = list(executor.map(process_item, data))
    thread_time = time.time() - start
    print(f"  Time: {thread_time:.4f} seconds")
    print(f"  Speedup: {seq_time / thread_time:.2f}x")
    
    # 3. Process pool (better for CPU-bound tasks)
    print("\n3. Process Pool (better for CPU-bound)")
    start = time.time()
    with ProcessPoolExecutor() as executor:
        results_process = list(executor.map(process_item, data, chunksize=100))
    process_time = time.time() - start
    print(f"  Time: {process_time:.4f} seconds")
    print(f"  Speedup: {seq_time / process_time:.2f}x")
    
    # 4. Asynchronous (not shown here as it's more complex for CPU-bound tasks)
    
    # Verify results
    assert all(math.isclose(a, b) for a, b in zip(results_seq, results_thread))
    assert all(math.isclose(a, b) for a, b in zip(results_seq, results_process))

def main() -> None:
    """Run all demonstrations."""
    # Benchmark different approaches
    benchmark_operations()
    
    # Example: Process files in a directory
    print("\n=== Example: Processing Files in Parallel ===\n")
    
    # Use the current directory for demonstration
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Process Python files in the current directory
    loop = asyncio.get_event_loop()
    try:
        results = loop.run_until_complete(
            process_files_parallel(current_dir, '*.py', max_workers=4)
        )
        
        # Print summary
        success = [r for r in results if r['status'] == 'success']
        print(f"Processed {len(success)}/{len(results)} files successfully")
        
        if success:
            total_size = sum(r['size_mb'] for r in success)
            avg_size = total_size / len(success)
            print(f"Total size: {total_size:.2f} MB")
            print(f"Average size: {avg_size:.2f} MB")
            print(f"Total lines: {sum(r['line_count'] for r in success):,}")
    except Exception as e:
        print(f"Error processing files: {e}")
    finally:
        loop.close()
    
    # Example: Data processing pipeline
    print("\n=== Example: Data Processing Pipeline ===\n")
    
    # Generate test data
    random.seed(42)
    test_data = [
        DataRecord(
            id=i,
            value=random.uniform(0, 2000),
            category='',
            timestamp=time.time() - random.uniform(0, 86400)
        )
        for i in range(1000)
    ]
    
    # Add some invalid records
    for i in range(10):
        test_data[i * 100].value = -1  # Invalid value
    
    print(f"Processing {len(test_data)} records...")
    start = time.time()
    processed, stats = process_data_pipeline(test_data, max_workers=4)
    elapsed = time.time() - start
    
    print(f"\nProcessing completed in {elapsed:.2f} seconds")
    print(f"Records processed: {stats['processed']}/{stats['total']}")
    print(f"Errors: {stats['errors']}")
    print("\nCategories:")
    for category, count in stats['categories'].items():
        print(f"  {category}: {count}")
    print(f"\nAverage value: {stats['avg_value']:.2f}")

if __name__ == "__main__":
    main()
