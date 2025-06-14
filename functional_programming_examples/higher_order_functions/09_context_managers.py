"""
9. Context Managers with Higher-Order Functions

Demonstrates how to create and use context managers with higher-order functions
for resource management, timing, and more.
"""
from __future__ import annotations
from typing import (
    TypeVar, Callable, Any, Dict, List, Tuple, Optional, Iterator, ContextManager,
    Type, Generic, cast
)
from contextlib import contextmanager
import time
import os
import tempfile
import sys
import logging
from functools import wraps

T = TypeVar('T')

# 1. Basic Context Manager with @contextmanager

@contextmanager
timed_operation(name: str) -> Iterator[None]:
    """A context manager that times the execution of a block of code."""
    start_time = time.perf_counter()
    print(f"Starting '{name}'...")
    
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"Finished '{name}' in {elapsed:.4f} seconds")

# 2. Context Manager for Temporary File

@contextmanager
def temp_file(prefix: str = 'tmp', suffix: str = '', mode: str = 'w+') -> Iterator[str]:
    """Create a temporary file that's automatically deleted when done."""
    fd, path = tempfile.mkstemp(prefix=prefix, suffix=suffix)
    file = None
    
    try:
        file = os.fdopen(fd, mode)
        yield path
    finally:
        if file is not None:
            file.close()
        try:
            os.unlink(path)
        except OSError:
            pass

# 3. Context Manager for Changing Directory

@contextmanager
def working_directory(path: str) -> Iterator[None]:
    """Change the working directory temporarily."""
    prev_dir = os.getcwd()
    os.chdir(path)
    
    try:
        yield
    finally:
        os.chdir(prev_dir)

# 4. Context Manager for Suppressing Exceptions

@contextmanager
def suppress(*exceptions: Type[BaseException]) -> Iterator[None]:
    """Suppress specified exceptions within the context."""
    try:
        yield
    except exceptions:
        pass

# 5. Context Manager for Logging

@contextmanager
def log_operation(operation: str, logger: Callable[[str], None] = print) -> Iterator[None]:
    """Log the start and end of an operation."""
    logger(f"Starting operation: {operation}")
    start_time = time.perf_counter()
    
    try:
        yield
    except Exception as e:
        logger(f"Operation '{operation}' failed with error: {e}")
        raise
    else:
        elapsed = time.perf_counter() - start_time
        logger(f"Completed operation '{operation}' in {elapsed:.4f} seconds")

# 6. Context Manager for Transaction-like Behavior

class TransactionError(Exception):
    pass

@contextmanager
def transaction() -> Iterator[list[str]]:
    """A simple transaction context manager that rolls back on errors."""
    operations: list[str] = []
    
    try:
        yield operations
    except Exception as e:
        # Rollback operations in reverse order
        print("Rolling back transaction due to error:", e)
        for op in reversed(operations):
            print(f"  Undoing: {op}")
        raise TransactionError("Transaction failed") from e
    else:
        print("Committing transaction")
        for op in operations:
            print(f"  Committed: {op}")

# 7. Context Manager for Resource Pooling

class Resource:
    """A simple resource that's expensive to create."""
    
    def __init__(self, name: str):
        self.name = name
        self.in_use = False
        print(f"Created resource: {self.name}")
    
    def use(self) -> None:
        """Use the resource."""
        if self.in_use:
            raise ValueError(f"Resource {self.name} is already in use")
        self.in_use = True
        print(f"Using resource: {self.name}")
    
    def release(self) -> None:
        """Release the resource."""
        self.in_use = False
        print(f"Released resource: {self.name}")

class ResourcePool:
    """A simple resource pool."""
    
    def __init__(self, size: int):
        self.resources = [Resource(f"Resource-{i}") for i in range(size)]
        self.available = self.resources.copy()
    
    def get_resource(self, timeout: float = 5.0) -> Resource:
        """Get a resource with a timeout."""
        start_time = time.perf_counter()
        
        while True:
            if self.available:
                resource = self.available.pop()
                resource.use()
                return resource
            
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError("Could not acquire resource: timeout")
            
            time.sleep(0.1)
    
    def release_resource(self, resource: Resource) -> None:
        """Release a resource back to the pool."""
        resource.release()
        self.available.append(resource)
    
    @contextmanager
    def resource_context(self, timeout: float = 5.0) -> Iterator[Resource]:
        """Context manager for resource acquisition and release."""
        resource = self.get_resource(timeout)
        try:
            yield resource
        finally:
            self.release_resource(resource)

# 8. Context Manager for Benchmarking

@contextmanager
def benchmark(name: str = "block") -> Iterator[None]:
    """Benchmark the execution time of a block of code."""
    start_time = time.perf_counter()
    start_cpu = time.process_time()
    
    try:
        yield
    finally:
        wall_elapsed = time.perf_counter() - start_time
        cpu_elapsed = time.process_time() - start_cpu
        print(f"{name} took {wall_elapsed:.6f}s wall time, {cpu_elapsed:.6f}s CPU time")

# 9. Context Manager for Mocking/Testing

@contextmanager
def mock_stdout() -> Iterator[list[str]]:
    """Capture stdout within the context."""
    from io import StringIO
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    output: list[str] = []
    
    try:
        yield output
    finally:
        output.extend(sys.stdout.getvalue().splitlines())
        sys.stdout = old_stdout

# 10. Higher-Order Context Manager

def with_retries(max_retries: int = 3, delay: float = 1.0, 
                 exceptions: tuple[type[Exception], ...] = (Exception,)) -> Callable[[Callable[..., T]], Callable[..., T]]:
    ""
    A decorator that retries a function call if it raises an exception.
    Can be used as a decorator or a context manager.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
            
            raise last_exception  # type: ignore
        
        return wrapper
    
    return decorator

# Example Usage
def demonstrate_context_managers() -> None:
    print("=== Context Managers with Higher-Order Functions ===\n")
    
    # 1. Basic timing
    print("1. Timing a block of code:")
    with timed_operation("long calculation"):
        # Simulate work
        total = 0
        for i in range(1, 1_000_000):
            total += i
    
    # 2. Temporary file
    print("\n2. Working with temporary files:")
    with temp_file(prefix='example_', suffix='.txt') as temp_path:
        print(f"Created temporary file: {temp_path}")
        with open(temp_path, 'w') as f:
            f.write("Hello, world!\n")
        
        # File is automatically deleted when the block exits
    
    # 3. Working directory
    print("\n3. Changing working directory:")
    print(f"Current directory: {os.getcwd()}")
    
    with working_directory('/tmp'):
        print(f"In temporary directory: {os.getcwd()}")
    
    print(f"Back to original directory: {os.getcwd()}")
    
    # 4. Suppressing exceptions
    print("\n4. Suppressing exceptions:")
    with suppress(ZeroDivisionError):
        result = 1 / 0
        print("This won't be printed")
    print("Continuing after suppressed exception")
    
    # 5. Logging
    print("\n5. Logging operations:")
    with log_operation("data processing"):
        # Simulate work
        time.sleep(0.5)
    
    # 6. Transaction-like behavior
    print("\n6. Transaction processing:")
    try:
        with transaction() as ops:
            ops.append("Create user")
            ops.append("Update profile")
            ops.append("Send welcome email")
            # Uncomment to test rollback:
            # raise ValueError("Database connection failed")
    except TransactionError as e:
        print(f"Transaction failed: {e}")
    
    # 7. Resource pooling
    print("\n7. Resource pooling:")
    pool = ResourcePool(2)
    
    with pool.resource_context() as res1:
        print(f"Using resource: {res1.name}")
        
        # This will work because we have 2 resources
        with pool.resource_context() as res2:
            print(f"Using resource: {res2.name}")
            
            # This would block if uncommented (no more resources)
            # with pool.resource_context() as res3:
            #     print(f"Using resource: {res3.name}")
    
    # 8. Benchmarking
    print("\n8. Benchmarking code:")
    with benchmark("Fibonacci calculation"):
        def fib(n: int) -> int:
            return n if n <= 1 else fib(n-1) + fib(n-2)
        result = fib(30)  # This is slow
    print(f"Result: {result}")
    
    # 9. Mocking stdout
    print("\n9. Capturing stdout:")
    with mock_stdout() as output:
        print("This will be captured")
        print("So will this")
    
    print(f"Captured output: {output}")
    
    # 10. Retry context manager
    print("\n10. Retrying operations:")
    
    @with_retries(max_retries=3, delay=0.5)
    def unreliable_operation(should_fail: bool) -> str:
        """An operation that might fail."""
        if should_fail and random.random() < 0.7:  # 70% chance of failure
            raise ValueError("Temporary error occurred")
        return "Operation succeeded"
    
    try:
        # First call might fail and retry
        print("Calling unreliable operation (may retry):")
        result = unreliable_operation(should_fail=True)
        print(f"Result: {result}")
    except Exception as e:
        print(f"All retries failed: {e}")

if __name__ == "__main__":
    demonstrate_context_managers()
    
    print("\n=== Key Takeaways ===")
    print("1. Context managers ensure resources are properly managed")
    print("2. They can be created using @contextmanager or by implementing __enter__/__exit__")
    print("3. Useful for resource management, timing, mocking, and more")
    print("4. Can be composed and nested for complex scenarios")
