"""
8. Monadic Composition

Demonstrates monadic composition patterns in Python, including Maybe, Either,
and IO monads, and how they can be used for function composition with effects.
"""
from __future__ import annotations
from typing import TypeVar, Generic, Callable, Any, Union, Optional, cast, overload
from functools import wraps, partial
import random
import time
from dataclasses import dataclass

T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E', bound=Exception)

# 1. Maybe Monad (Option type)

class Maybe(Generic[T]):
    """A Maybe monad representing optional values."""
    
    @staticmethod
    def of(value: T | None) -> Maybe[T]:
        """Create a Maybe from a value that might be None."""
        return Just(value) if value is not None else Nothing()
    
    def map(self, f: Callable[[T], U]) -> Maybe[U]:
        """Map a function over the Maybe."""
        raise NotImplementedError
    
    def bind(self, f: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Chain operations that return Maybes."""
        raise NotImplementedError
    
    def or_else(self, default: T) -> T:
        """Get the value or return a default."""
        raise NotImplementedError
    
    def __or__(self, f: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Override >> operator for bind."""
        return self.bind(f)

@dataclass
class Just(Maybe[T]):
    """Represents a value that exists."""
    value: T
    
    def map(self, f: Callable[[T], U]) -> Maybe[U]:
        return Just(f(self.value))
    
    def bind(self, f: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return f(self.value)
    
    def or_else(self, default: T) -> T:
        return self.value
    
    def __str__(self) -> str:
        return f"Just({self.value})"

class Nothing(Maybe[Any]):
    """Represents the absence of a value."""
    
    def map(self, f: Callable[[Any], Any]) -> Maybe[Any]:
        return self
    
    def bind(self, f: Callable[[Any], Maybe[Any]]) -> Maybe[Any]:
        return self
    
    def or_else(self, default: T) -> T:
        return default
    
    def __str__(self) -> str:
        return "Nothing"

# 2. Either Monad (Result type)
class Either(Generic[E, T]):
    """Base class for Either monad representing a result or an error."""
    
    @staticmethod
    def of(value: T) -> Either[E, T]:
        """Create a Right value."""
        return Right(value)
    
    @staticmethod
    def left(error: E) -> Either[E, T]:
        """Create a Left value."""
        return Left(error)
    
    def map(self, f: Callable[[T], U]) -> Either[E, U]:
        """Map over the right value."""
        raise NotImplementedError
    
    def map_error(self, f: Callable[[E], E]) -> Either[E, T]:
        """Map over the left (error) value."""
        raise NotImplementedError
    
    def bind(self, f: Callable[[T], Either[E, U]]) -> Either[E, U]:
        """Chain operations that return Either."""
        raise NotImplementedError
    
    def or_else(self, default: T) -> T:
        """Get the right value or return a default."""
        raise NotImplementedError
    
    def get_or_raise(self) -> T:
        """Get the right value or raise the left value as an exception."""
        raise NotImplementedError

@dataclass
class Left(Either[E, T]):
    """Represents an error case."""
    error: E
    
    def map(self, f: Callable[[T], U]) -> Either[E, U]:
        return Left(self.error)
    
    def map_error(self, f: Callable[[E], E]) -> Either[E, T]:
        return Left(f(self.error))
    
    def bind(self, f: Callable[[T], Either[E, U]]) -> Either[E, U]:
        return Left(self.error)
    
    def or_else(self, default: T) -> T:
        return default
    
    def get_or_raise(self) -> T:
        if isinstance(self.error, Exception):
            raise self.error
        raise ValueError(str(self.error))
    
    def __str__(self) -> str:
        return f"Left({self.error})"

@dataclass
class Right(Either[Any, T]):
    """Represents a success case."""
    value: T
    
    def map(self, f: Callable[[T], U]) -> Either[Any, U]:
        try:
            return Right(f(self.value))
        except Exception as e:
            return Left(e)
    
    def map_error(self, f: Callable[[E], E]) -> Either[E, T]:
        return self
    
    def bind(self, f: Callable[[T], Either[E, U]]) -> Either[E, U]:
        try:
            return f(self.value)
        except Exception as e:
            return Left(e)
    
    def or_else(self, default: T) -> T:
        return self.value
    
    def get_or_raise(self) -> T:
        return self.value
    
    def __str__(self) -> str:
        return f"Right({self.value})"

# 3. IO Monad
class IO(Generic[T]):
    """IO monad for handling side effects."""
    
    def __init__(self, effect: Callable[[], T]):
        self._effect = effect
    
    @staticmethod
    def of(value: T) -> IO[T]:
        """Lift a value into the IO monad."""
        return IO(lambda: value)
    
    def map(self, f: Callable[[T], U]) -> IO[U]:
        """Map a function over the result of the IO action."""
        return IO(lambda: f(self.run()))
    
    def bind(self, f: Callable[[T], IO[U]]) -> IO[U]:
        """Chain IO actions."""
        return IO(lambda: f(self.run()).run())
    
    def run(self) -> T:
        """Execute the IO action and return the result."""
        return self._effect()
    
    def __or__(self, f: Callable[[T], IO[U]]) -> IO[U]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[T], IO[U]]) -> IO[U]:
        """Override >> operator for bind."""
        return self.bind(f)
    
    def __str__(self) -> str:
        return f"IO({self._effect})"

# 4. Do notation simulation
def do_io(io: IO[T]) -> T:
    """Extract value from IO monad (used in do notation)."""
    return io.run()

def do_maybe(m: Maybe[T]) -> T:
    """Extract value from Maybe monad (used in do notation)."""
    if isinstance(m, Just):
        return m.value
    raise ValueError("Cannot extract value from Nothing")

def do_either(e: Either[E, T]) -> T:
    """Extract value from Either monad (used in do notation)."""
    if isinstance(e, Right):
        return e.value
    raise e.error if isinstance(e.error, Exception) else ValueError(str(e.error))

# 5. Examples
def demonstrate_maybe_monad() -> None:
    """Demonstrate the Maybe monad."""
    print("=== Maybe Monad ===")
    
    # Safe division that returns Maybe
    def safe_divide(x: float, y: float) -> Maybe[float]:
        return Maybe.of(x / y) if y != 0 else Nothing()
    
    # Function that might return None
    def find_user(id: int) -> Maybe[str]:
        users = {1: "Alice", 2: "Bob"}
        return Maybe.of(users.get(id))
    
    # Chaining operations with Maybe
    result = (
        safe_divide(10, 2)  # Just(5.0)
        .map(lambda x: x * 3)  # Just(15.0)
        .bind(lambda x: safe_divide(x, 5))  # Just(3.0)
    )
    print(f"Result: {result}")
    
    # Division by zero
    result = safe_divide(10, 0)  # Nothing
    print(f"Division by zero: {result}")
    
    # Find and process user
    user_processing = (
        find_user(1)  # Just("Alice")
        .map(str.upper)  # Just("ALICE")
        .map(lambda s: f"Hello, {s}!")  # Just("Hello, ALICE!")
    )
    print(f"User processing: {user_processing}")
    
    # User not found
    user_processing = find_user(99).map(str.upper)
    print(f"User not found: {user_processing}")

def demonstrate_either_monad() -> None:
    """Demonstrate the Either monad."""
    print("\n=== Either Monad ===")
    
    # Safe division that returns Either
    def safe_divide(x: float, y: float) -> Either[Exception, float]:
        try:
            return Right(x / y)
        except Exception as e:
            return Left(e)
    
    # Function that might fail
    def find_user(id: int) -> Either[str, str]:
        users = {1: "Alice", 2: "Bob"}
        if id in users:
            return Right(users[id])
        return Left(f"User with id {id} not found")
    
    # Chaining operations with Either
    result = (
        safe_divide(10, 2)  # Right(5.0)
        .map(lambda x: x * 3)  # Right(15.0)
        .bind(lambda x: safe_divide(x, 5))  # Right(3.0)
    )
    print(f"Result: {result}")
    
    # Error handling
    result = (
        safe_divide(10, 0)  # Left(ZeroDivisionError)
        .map(lambda x: x * 3)  # Still Left(ZeroDivisionError)
        .bind(lambda x: safe_divide(x, 5))  # Still Left(ZeroDivisionError)
        .map_error(lambda e: f"Error: {str(e)}")  # Left("Error: division by zero")
    )
    print(f"Error handling: {result}")
    
    # Find and process user
    user_processing = (
        find_user(1)  # Right("Alice")
        .map(str.upper)  # Right("ALICE")
        .map(lambda s: f"Hello, {s}!")  # Right("Hello, ALICE!")
    )
    print(f"User processing: {user_processing}")
    
    # User not found
    user_processing = find_user(99).map(str.upper)
    print(f"User not found: {user_processing}")

def demonstrate_io_monad() -> None:
    """Demonstrate the IO monad."""
    print("\n=== IO Monad ===")
    
    # IO actions
    def get_name() -> IO[str]:
        return IO(lambda: input("What's your name? "))
    
    def greet(name: str) -> IO[None]:
        return IO(lambda: print(f"Hello, {name}!"))
    
    def get_random_number() -> IO[int]:
        return IO(lambda: random.randint(1, 100))
    
    # Compose IO actions
    program = (
        get_name()
        .bind(lambda name: 
            get_random_number()
            .bind(lambda num: 
                greet(f"{name} (lucky number: {num})")
            )
        )
    )
    
    print("Running IO program...")
    program.run()
    
    # With do notation (simulated with nested lambdas)
    def program_do() -> IO[None]:
        name = yield get_name()
        num = yield get_random_number()
        return greet(f"{name} (lucky number: {num})")
    
    # We need a helper to run the generator-based do notation
    def run_io(generator):
        """Run a generator-based do notation for IO."""
        def send(val=None):
            try:
                io = generator.send(val)
                return io.bind(send)
            except StopIteration as e:
                return IO.of(e.value) if e.value is not None else IO.of(None)
        return send()
    
    print("\nRunning IO program with do notation...")
    run_io(program_do()).run()

def demonstrate_monadic_composition() -> None:
    """Demonstrate composing different monads."""
    print("\n=== Monadic Composition ===")
    
    # A function that returns Maybe
    def parse_int(s: str) -> Maybe[int]:
        try:
            return Just(int(s))
        except ValueError:
            return Nothing()
    
    # A function that returns Either
    def safe_divide(x: float, y: float) -> Either[str, float]:
        if y == 0:
            return Left("Division by zero")
        return Right(x / y)
    
    # A function that returns IO
    def get_input(prompt: str) -> IO[str]:
        return IO(lambda: input(prompt))
    
    # A program that composes all three monads
    def program() -> IO[None]:
        # Get input (IO)
        input_str = yield get_input("Enter two numbers separated by a slash (e.g., 10/2): ")
        
        # Parse input (Maybe)
        parts = input_str.split('/')
        if len(parts) != 2:
            return IO(lambda: print("Invalid input format. Please use format: number/number"))
        
        a_maybe = parse_int(parts[0].strip())
        b_maybe = parse_int(parts[1].strip())
        
        # Extract from Maybe (could use do notation here)
        try:
            a = do_maybe(a_maybe)
            b = do_maybe(b_maybe)
            
            # Perform division (Either)
            result = safe_divide(a, b)
            
            # Handle result
            if isinstance(result, Right):
                return IO(lambda: print(f"Result: {result.value}"))
            else:
                return IO(lambda: print(f"Error: {result.error}"))
        except ValueError:
            return IO(lambda: print("Error: Invalid number(s)"))
    
    # Run the program
    print("Running monadic composition example...")
    run_io(program()).run()

if __name__ == "__main__":
    print("=== Monadic Composition in Python ===")
    demonstrate_maybe_monad()
    demonstrate_either_monad()
    demonstrate_io_monad()
    demonstrate_monadic_composition()
    
    print("\n=== Key Takeaways ===")
    print("1. Monads help manage side effects and handle errors in a functional way")
    print("2. Maybe/Option types handle null/None values safely")
    print("3. Either/Result types handle errors explicitly")
    print("4. IO monad manages side effects and separates pure/impure code")
    print("5. Monadic composition allows chaining operations that produce effects")
