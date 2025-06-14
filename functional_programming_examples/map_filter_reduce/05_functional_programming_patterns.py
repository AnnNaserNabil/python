"""
5. Functional Programming Patterns with Map, Filter, and Reduce

Explores common functional programming patterns implemented using map, filter, and reduce,
including function composition, currying, monads, and more.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Iterable, Any, List, Dict, Tuple, Optional, Generic
from functools import reduce, partial
from dataclasses import dataclass
import operator
import json
from pathlib import Path

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# 1. Function Composition

def compose(*funcs: Callable) -> Callable:
    """Compose functions from right to left."""
    def composed(x: Any) -> Any:
        result = x
        for f in reversed(funcs):
            result = f(result)
        return result
    return composed

def pipe(*funcs: Callable) -> Callable:
    """Pipe functions from left to right (reverse of compose)."""
    def piped(x: Any) -> Any:
        result = x
        for f in funcs:
            result = f(result)
        return result
    return piped

# 2. Currying and Partial Application

def curry(func: Callable[..., T], arity: Optional[int] = None) -> Callable:
    """Convert a function to a curried function."""
    if arity is None:
        arity = func.__code__.co_argcount
    
    def curried(*args: Any) -> Any:
        if len(args) >= arity:
            return func(*args[:arity])
        return lambda *more: curried(*(args + more))
    
    return curried

# 3. Functor Pattern

class Maybe(Generic[T]):
    """A simple Maybe monad implementation."""
    
    @classmethod
    def of(cls, value: Optional[T]) -> Maybe[T]:
        """Create a new Maybe with a value."""
        return Just(value) if value is not None else Nothing()
    
    def map(self, func: Callable[[T], U]) -> Maybe[U]:
        """Apply function to the value if it exists."""
        raise NotImplementedError
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Chain operations that return Maybes."""
        raise NotImplementedError
    
    def get_or_else(self, default: T) -> T:
        """Get the value or return a default."""
        raise NotImplementedError

class Just(Maybe[T]):
    """A Maybe that contains a value."""
    
    def __init__(self, value: T):
        self.value = value
    
    def map(self, func: Callable[[T], U]) -> Maybe[U]:
        return Just(func(self.value))
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return func(self.value)
    
    def get_or_else(self, default: T) -> T:
        return self.value
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Just) and self.value == other.value
    
    def __repr__(self) -> str:
        return f'Just({self.value})'

class Nothing(Maybe[Any]):
    """A Maybe that contains no value."""
    
    def map(self, func: Callable[[T], U]) -> Maybe[U]:
        return self
    
    def bind(self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return self
    
    def get_or_else(self, default: T) -> T:
        return default
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Nothing)
    
    def __repr__(self) -> str:
        return 'Nothing'

# 4. Either Monad for Error Handling

class Either(Generic[T]):
    """Base class for Either monad."""
    
    @classmethod
    def of(cls, value: T) -> Either[T]:
        """Create a Right value."""
        return Right(value)
    
    @classmethod
    def from_try(cls, func: Callable[[], T]) -> Either[T]:
        """Create from a function that might raise an exception."""
        try:
            return Right(func())
        except Exception as e:
            return Left(e)
    
    def map(self, func: Callable[[T], U]) -> Either[U]:
        """Map over the Right value."""
        raise NotImplementedError
    
    def bind(self, func: Callable[[T], Either[U]]) -> Either[U]:
        """Chain operations that return Either."""
        raise NotImplementedError
    
    def get_or_else(self, default: T) -> T:
        """Get the Right value or return a default."""
        raise NotImplementedError

class Right(Either[T]):
    """The happy path of Either, containing a value."""
    
    def __init__(self, value: T):
        self.value = value
    
    def map(self, func: Callable[[T], U]) -> Either[U]:
        return Right(func(self.value))
    
    def bind(self, func: Callable[[T], Either[U]]) -> Either[U]:
        return func(self.value)
    
    def get_or_else(self, default: T) -> T:
        return self.value
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Right) and self.value == other.value
    
    def __repr__(self) -> str:
        return f'Right({self.value})'

class Left(Either[Any]):
    """The error path of Either, containing an error."""
    
    def __init__(self, error: Exception):
        self.error = error
    
    def map(self, func: Callable[[T], U]) -> Either[U]:
        return self
    
    def bind(self, func: Callable[[T], Either[U]]) -> Either[U]:
        return self
    
    def get_or_else(self, default: T) -> T:
        return default
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Left) and self.error == other.error
    
    def __repr__(self) -> str:
        return f'Left({self.error})'

# 5. Reader Monad for Dependency Injection

class Reader(Generic[T, U]):
    """Reader monad for dependency injection."""
    
    def __init__(self, func: Callable[[T], U]):
        self.func = func
    
    def run(self, env: T) -> U:
        """Run the reader with the given environment."""
        return self.func(env)
    
    def map(self, func: Callable[[U], V]) -> Reader[T, V]:
        """Map over the result of the reader."""
        return Reader(lambda env: func(self.run(env)))
    
    def bind(self, func: Callable[[U], Reader[T, V]]) -> Reader[T, V]:
        """Chain reader operations."""
        return Reader(lambda env: func(self.run(env)).run(env))
    
    @classmethod
    def ask(cls) -> Reader[T, T]:
        """Get the environment."""
        return Reader(lambda env: env)
    
    @classmethod
    def asks(cls, func: Callable[[T], U]) -> Reader[T, U]:
        """Get a function of the environment."""
        return Reader(func)

# 6. State Monad for Managing State

S = TypeVar('S')

class State(Generic[S, T]):
    """State monad for managing stateful computations."""
    
    def __init__(self, run_state: Callable[[S], Tuple[T, S]]):
        self.run_state = run_state
    
    def run(self, state: S) -> Tuple[T, S]:
        """Run the stateful computation."""
        return self.run_state(state)
    
    def map(self, func: Callable[[T], U]) -> State[S, U]:
        """Map over the result of the state computation."""
        def new_run(s: S) -> Tuple[U, S]:
            a, s1 = self.run(s)
            return func(a), s1
        return State(new_run)
    
    def bind(self, func: Callable[[T], State[S, U]]) -> State[S, U]:
        """Chain stateful computations."""
        def new_run(s: S) -> Tuple[U, S]:
            a, s1 = self.run(s)
            return func(a).run(s1)
        return State(new_run)
    
    @classmethod
    def of(cls, value: T) -> State[S, T]:
        """Create a state computation that returns a value without modifying the state."""
        return State(lambda s: (value, s))
    
    @classmethod
    def get(cls) -> State[S, S]:
        """Get the current state."""
        return State(lambda s: (s, s))
    
    @classmethod
    def put(cls, new_state: S) -> State[S, None]:
        """Set the state to a new value."""
        return State(lambda _: (None, new_state))
    
    @classmethod
    def modify(cls, func: Callable[[S], S]) -> State[S, None]:
        """Modify the state using a function."""
        return State(lambda s: (None, func(s)))

# 7. Practical Example: Data Validation Pipeline

def validate_user(data: Dict[str, Any]) -> Either[Dict[str, Any]]:
    """Validate user data using a pipeline of validations."""
    def validate_name(user: Dict[str, Any]) -> Either[Dict[str, Any]]:
        name = user.get('name', '').strip()
        if not name:
            return Left(ValueError("Name is required"))
        if len(name) < 3:
            return Left(ValueError("Name must be at least 3 characters"))
        return Right(user)
    
    def validate_email(user: Dict[str, Any]) -> Either[Dict[str, Any]]:
        email = user.get('email', '').strip()
        if not email:
            return Left(ValueError("Email is required"))
        if '@' not in email:
            return Left(ValueError("Invalid email format"))
        return Right(user)
    
    def validate_age(user: Dict[str, Any]) -> Either[Dict[str, Any]]:
        try:
            age = int(user.get('age', 0))
            if age < 18:
                return Left(ValueError("Must be at least 18 years old"))
            return Right(user)
        except (TypeError, ValueError):
            return Left(ValueError("Age must be a number"))
    
    # Chain validations using bind
    return (
        Right(data)
        .bind(validate_name)
        .bind(validate_email)
        .bind(validate_age)
    )

# 8. Practical Example: Configuration Reader

def get_database_config() -> Reader[Dict[str, Any], Dict[str, str]]:
    """Get database configuration using the Reader monad."""
    def get_config(key: str) -> Reader[Dict[str, Any], str]:
        return Reader(lambda env: env.get(key, ""))
    
    return (
        get_config("database")
        .bind(lambda db: (
            get_config("username")
            .bind(lambda user: (
                get_config("password")
                .bind(lambda pwd: (
                    get_config("host")
                    .bind(lambda host: (
                        get_config("port")
                        .bind(lambda port: (
                            Reader.asks(lambda _: {
                                'db': db,
                                'user': user,
                                'password': pwd,
                                'host': host,
                                'port': port
                            })
                        ))
                    ))
                ))
            ))
        )
    )

# 9. Practical Example: Stateful Counter

def counter_example() -> Tuple[int, int]:
    """Example of using the State monad for a counter."""
    # Define stateful operations
    def increment() -> State[int, int]:
        return State.get().bind(
            lambda n: State.put(n + 1).bind(
                lambda _: State.of(n + 1)
            )
        )
    
    def decrement() -> State[int, int]:
        return State.get().bind(
            lambda n: State.put(n - 1).bind(
                lambda _: State.of(n - 1)
            )
        )
    
    # Compose stateful operations
    computation = (
        increment()
        .bind(lambda _: increment())
        .bind(lambda _: increment())
        .bind(lambda _: decrement())
        .bind(lambda _: State.get())
    )
    
    # Run the computation with initial state 0
    return computation.run(0)

# 10. Practical Example: Maybe for Safe Navigation

def safe_navigation_example() -> None:
    """Example of using Maybe for safe navigation through nested data."""
    # Sample nested data structure
    data = {
        'user': {
            'profile': {
                'name': 'Alice',
                'address': {
                    'street': '123 Main St',
                    'city': 'Wonderland'
                }
            }
        }
    }
    
    # Safe navigation function
    def safe_get(d: Any, *keys: str) -> Maybe[Any]:
        result = d
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return Nothing()
        return Just(result)
    
    # Safe access examples
    name = safe_get(data, 'user', 'profile', 'name')
    print(f"Name: {name.get_or_else('Unknown')}")
    
    zip_code = safe_get(data, 'user', 'profile', 'address', 'zip')
    print(f"ZIP Code: {zip_code.get_or_else('Not provided')}")
    
    # Chaining operations
    formatted_address = (
        safe_get(data, 'user', 'profile', 'address')
        .map(lambda addr: f"{addr.get('street', '')}, {addr.get('city', '')}")
        .get_or_else('Address not available')
    )
    print(f"Formatted Address: {formatted_address}")

def demonstrate_functional_patterns() -> None:
    """Demonstrate all functional programming patterns."""
    print("=== Functional Programming Patterns ===\n")
    
    # 1. Function Composition
    print("1. Function Composition:")
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x ** 2
    
    # Compose functions: square(double(add_one(x)))
    composed = compose(square, double, add_one)
    print(f"compose(square, double, add_one)(3) = {composed(3)}")
    
    # Pipe functions: add_one(double(square(x)))
    piped = pipe(add_one, double, square)
    print(f"pipe(add_one, double, square)(3) = {piped(3)}")
    
    # 2. Currying
    print("\n2. Currying:")
    
    @curry
    def add_three(a: int, b: int, c: int) -> int:
        return a + b + c
    
    add_five = add_three(2)(3)  # Partially applied
    print(f"add_five(10) = {add_five(10)}")
    
    # 3. Maybe Monad
    print("\n3. Maybe Monad:")
    def safe_divide(x: float, y: float) -> Maybe[float]:
        return Maybe.of(x / y if y != 0 else None)
    
    result = (
        Maybe.of(10)
        .bind(lambda x: safe_divide(x, 2))
        .bind(lambda x: safe_divide(x, 0))  # This will return Nothing
        .get_or_else(float('inf'))
    )
    print(f"Safe division result: {result}")
    
    # 4. Either Monad
    print("\n4. Either Monad (Validation):")
    
    # Test validation
    valid_user = {
        'name': 'Alice',
        'email': 'alice@example.com',
        'age': '25'
    }
    
    invalid_user = {
        'name': 'Bo',  # Too short
        'email': 'invalid-email',
        'age': 'seventeen'  # Not a number
    }
    
    print("\nValid user validation:")
    valid_result = validate_user(valid_user)
    if isinstance(valid_result, Right):
        print("  Valid user:", valid_result.value)
    else:
        print("  Error:", valid_result.error)
    
    print("\nInvalid user validation:")
    invalid_result = validate_user(invalid_user)
    if isinstance(invalid_result, Right):
        print("  Valid user:", invalid_result.value)
    else:
        print("  Error:", invalid_result.error)
    
    # 5. Reader Monad
    print("\n5. Reader Monad (Dependency Injection):")
    
    config = {
        'database': 'myapp_db',
        'username': 'admin',
        'password': 'secret',
        'host': 'localhost',
        'port': '5432'
    }
    
    db_config = get_database_config().run(config)
    print("Database config:", db_config)
    
    # 6. State Monad
    print("\n6. State Monad (Counter):")
    final_count, final_state = counter_example()
    print(f"Final count: {final_count}, Final state: {final_state}")
    
    # 7. Safe Navigation with Maybe
    print("\n7. Safe Navigation with Maybe:")
    safe_navigation_example()

if __name__ == "__main__":
    demonstrate_functional_patterns()
    
    print("\n=== Key Takeaways ===")
    print("1. Function composition enables building complex transformations from simple functions")
    print("2. Currying allows partial application of functions")
    print("3. Maybe handles null/None values in a type-safe way")
    print("4. Either represents success/failure with values")
    print("5. Reader manages dependencies and configuration")
    print("6. State manages stateful computations in a pure way")
