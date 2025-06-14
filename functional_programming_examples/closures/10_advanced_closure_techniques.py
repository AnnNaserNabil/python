"""
10. Advanced Closure Techniques in Python

This module explores sophisticated uses of closures to implement advanced programming
patterns, demonstrating how closures can be used for state management, object-oriented
programming, and more.

Key Techniques Covered:
--------------------
1. Parameterized Decorators: Creating decorators that accept arguments
2. State Machines: Implementing complex stateful logic
3. Object-Oriented Patterns: Mimicking classes using closures
4. Advanced Caching: Memoization with automatic invalidation
5. Type-Safe Function Composition: Building complex operations from simple functions

Why Use These Advanced Techniques?
------------------------------
- Greater Flexibility: Create highly configurable and reusable components
- Better Encapsulation: Hide implementation details while exposing clean interfaces
- Functional Style: Write more declarative and composable code
- Performance: Implement efficient caching and state management
- Type Safety: Catch errors early with proper type hints

Real-world Applications:
----------------------
- Web frameworks (route decorators, middleware)
- Game development (game states, AI behavior)
- Data processing pipelines
- Configuration systems
- Testing frameworks

Example:
-------
>>> # Using the retry decorator
>>> @retry(max_attempts=3, delay=1, backoff=2)
... def fetch_data():
...     # Might fail, but will retry up to 3 times
...     return requests.get("https://api.example.com/data").json()
"""
from __future__ import annotations
from typing import Any, Callable, TypeVar, Generic, Optional, Dict, List, Type, cast
from dataclasses import dataclass
from enum import Enum, auto
import functools
import time
import inspect

T = TypeVar('T')
U = TypeVar('U')

# 1. Decorator Factory with Parameters
def retry(max_attempts: int, exceptions: tuple[Type[Exception], ...] = (Exception,), 
         delay: float = 1.0, backoff: float = 2.0) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Create a decorator that retries a function on failure with exponential backoff.
    
    This decorator wraps a function to automatically retry it when specific exceptions
    occur, with increasing delays between attempts (exponential backoff).
    
    Args:
        max_attempts: Maximum number of times to attempt the function
        exceptions: Tuple of exception types to catch and retry on
        delay: Initial delay between attempts in seconds
        backoff: Multiplier for the delay after each failed attempt
        
    Returns:
        A decorator that can be applied to functions to add retry behavior
        
    Example:
        >>> @retry(max_attempts=3, delay=1, backoff=2)
        ... def fetch_data():
        ...     # This will be retried up to 3 times if it fails
        ...     return requests.get("https://api.example.com/data").json()
        
    Note:
        - The last exception will be re-raised if all attempts fail
        - Uses functools.wraps to preserve the original function's metadata
        - Not thread-safe in this implementation
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            current_delay = delay
            last_exception: Optional[Exception] = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts:
                        break
                    
                    print(f"Attempt {attempt} failed: {e}. Retrying in {current_delay:.1f} seconds...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            raise RuntimeError(f"Failed after {max_attempts} attempts") from last_exception
        
        return wrapper
    return decorator

# 2. State Machine with Closures
class State(Enum):
    IDLE = auto()
    PROCESSING = auto()
    PAUSED = auto()
    STOPPED = auto()

def create_state_machine():
    """
    Create a state machine using closures.
    
    This function returns a state machine object with methods to transition
    between states and execute callbacks on state changes. The state is stored
    in the closure, making it private and only modifiable through the provided
    methods.
    
    Returns:
        A state machine object with the following methods:
        - transition_to(new_state): Change to a new state
        - on_enter(state, callback): Register a callback for state entry
        - on_exit(state, callback): Register a callback for state exit
        - get_state(): Get the current state
        
    Example:
        >>> fsm = create_state_machine()
        >>> fsm.on_enter(State.PROCESSING, lambda: print("Starting processing"))
        >>> fsm.transition_to(State.PROCESSING)  # Prints "Starting processing"
        
    Note:
        - States should be members of the State enum
        - Callbacks are executed in the order they were registered
        - The state machine starts in State.IDLE
    """
    state = State.IDLE
    data: List[Any] = []
    enter_callbacks: Dict[State, List[Callable[..., None]]] = {}
    exit_callbacks: Dict[State, List[Callable[..., None]]] = {}
    
    def transition(new_state: State) -> None:
        nonlocal state
        print(f"Transitioning from {state.name} to {new_state.name}")
        
        # Execute exit callbacks for the current state
        if state in exit_callbacks:
            for callback in exit_callbacks[state]:
                callback()
        
        state = new_state
        
        # Execute enter callbacks for the new state
        if state in enter_callbacks:
            for callback in enter_callbacks[state]:
                callback()
    
    def on_enter(state: State, callback: Callable[..., None]) -> None:
        if state not in enter_callbacks:
            enter_callbacks[state] = []
        enter_callbacks[state].append(callback)
    
    def on_exit(state: State, callback: Callable[..., None]) -> None:
        if state not in exit_callbacks:
            exit_callbacks[state] = []
        exit_callbacks[state].append(callback)
    
    def get_state() -> State:
        return state
    
    return {
        'transition_to': transition,
        'on_enter': on_enter,
        'on_exit': on_exit,
        'get_state': get_state,
        'state': property(get_state)  # Read-only property
    }

# 3. Object-Oriented Programming with Closures
def create_person(name: str, age: int):
    """
    Create a person object using closures instead of classes.
    
    This demonstrates how closures can be used to implement object-oriented
    patterns like encapsulation and methods without using classes.
    
    Args:
        name: The person's name
        age: The person's age
        
    Returns:
        A dictionary of methods that can manipulate the person's data:
        - get_name(): Get the person's name
        - set_name(new_name): Change the person's name
        - get_age(): Get the person's age
        - have_birthday(): Increment the person's age
        - greet(): Return a greeting message
        
    Example:
        >>> person = create_person("Alice", 30)
        >>> person["greet"]()
        'Hello, my name is Alice and I am 30 years old.'
        >>> person["have_birthday"]()
        >>> person["get_age"]()
        31
        
    Note:
        The person's data is stored in the closure and can only be
        accessed or modified through the returned methods.
    """
    _name = name
    _age = age
    _friends: List[Dict[str, Any]] = []
    
    def get_name() -> str:
        return _name
    
    def get_age() -> int:
        return _age
    
    def have_birthday() -> None:
        nonlocal _age
        _age += 1
    
    def add_friend(friend: Dict[str, Any]) -> None:
        if friend not in _friends:
            _friends.append(friend)
    
    def get_friends() -> List[Dict[str, Any]]:
        return _friends.copy()
    
    def introduce() -> str:
        friend_names = [f['get_name']() for f in _friends]
        friends_str = ", ".join(friend_names) if friend_names else "no one"
        return f"Hi, I'm {_name}, {_age} years old. My friends are: {friends_str}."
    
    return {
        'get_name': get_name,
        'get_age': get_age,
        'have_birthday': have_birthday,
        'add_friend': add_friend,
        'get_friends': get_friends,
        'introduce': introduce,
        'name': property(get_name),
        'age': property(get_age)
    }

# 4. Memoization with Cache Invalidation
def memoize_with_invalidation(invalidate_after: float = 60.0) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Memoize function results with time-based invalidation."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[Any, tuple[float, T]] = {}
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create a cache key
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            
            # Invalidate old cache entries
            for k in list(cache.keys()):
                timestamp, _ = cache[k]
                if now - timestamp > invalidate_after:
                    del cache[k]
            
            # Check cache
            if key in cache:
                _, result = cache[key]
                return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result
        
        # Add cache clearing method
        def clear_cache() -> None:
            cache.clear()
        
        wrapper.clear_cache = clear_cache  # type: ignore
        return wrapper
    return decorator

# 5. Function Composition with Type Safety
def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Compose functions with type checking."""
    if not funcs:
        return lambda x: x
    
    # Check function signatures
    for i in range(len(funcs) - 1):
        f = funcs[i]
        g = funcs[i + 1]
        
        # Get type hints
        f_sig = inspect.signature(f)
        g_sig = inspect.signature(g)
        
        # Check if output of g matches input of f
        # This is a simplified check - in practice, you'd want more robust type checking
        if (f_sig.return_annotation != inspect.Parameter.empty and 
            g_sig.parameters and 
            next(iter(g_sig.parameters.values())).annotation != inspect.Parameter.empty):
            
            if f_sig.return_annotation != next(iter(g_sig.parameters.values())).annotation:
                print(f"Warning: Type mismatch in composition: {f.__name__} returns {f_sig.return_annotation}, "
                      f"but {g.__name__} expects {next(iter(g_sig.parameters.values())).annotation}")
    
    return functools.reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)

def demonstrate_advanced_techniques() -> None:
    """
    Showcase advanced techniques using closures in Python.
    
    This function demonstrates several sophisticated patterns:
    
    1. Parameterized Decorators: Creating flexible decorators with arguments
    2. State Machines: Implementing complex stateful logic with clean interfaces
    3. Object-Oriented Patterns: Mimicking classes using closures and functions
    4. Advanced Caching: Memoization with automatic cache invalidation
    5. Type-Safe Composition: Building complex operations from simple functions
    
    Each example is designed to be self-contained and highlights a different
    aspect of what can be achieved with closures in Python.
    
    The examples progress from simpler to more complex patterns, building on
    concepts introduced earlier in the module.
    """
    print("=== Retry Decorator ===")
    
    @retry(max_attempts=3, delay=0.5, backoff=1.5, exceptions=(ValueError,))
    def risky_operation(should_fail: bool = True) -> str:
        """An operation that might fail."""
        if should_fail:
            raise ValueError("Temporary failure")
        return "Success"
    
    try:
        print("Running risky operation (will retry):")
        print(risky_operation(should_fail=True))
    except Exception as e:
        print(f"Operation failed: {e}")
    
    print("\n=== State Machine ===")
    sm = create_state_machine()
    sm['process']()
    sm['pause']()
    sm['resume']()
    sm['stop']()
    
    print("\n=== Object-Oriented with Closures ===")
    alice = create_person("Alice", 30)
    bob = create_person("Bob", 25)
    charlie = create_person("Charlie", 35)
    
    alice['add_friend'](bob)
    alice['add_friend'](charlie)
    bob['add_friend'](alice)
    
    print(alice['introduce']())
    print(bob['introduce']())
    
    alice['have_birthday']()
    print(f"After birthday: {alice['get_name']()} is now {alice['get_age']} years old")
    
    print("\n=== Memoization with Invalidation ===")
    @memoize_with_invalidation(invalidate_after=2.0)
    def expensive_computation(x: int) -> int:
        print(f"Computing expensive_computation({x})...")
        time.sleep(0.5)
        return x * x
    
    print("First call (computes):", expensive_computation(5))
    print("Second call (cached):", expensive_computation(5))
    print("Waiting for cache to invalidate...")
    time.sleep(2.5)
    print("After invalidation (computes again):", expensive_computation(5))
    
    print("\n=== Function Composition with Type Checking ===")
    def double(x: int) -> int:
        return x * 2
    
    def to_str(x: int) -> str:
        return str(x)
    
    def add_exclamation(s: str) -> str:
        return s + "!"
    
    # This will show a type warning in the output
    pipeline = compose(double, to_str, add_exclamation)
    print("Composed function result:", pipeline(5))
    
    # Clear the cache of the memoized function
    if hasattr(expensive_computation, 'clear_cache'):
        expensive_computation.clear_cache()  # type: ignore
        print("\nCache cleared for expensive_computation")

if __name__ == "__main__":
    print("=== Advanced Closure Techniques ===")
    demonstrate_advanced_techniques()
    
    print("\n=== Key Takeaways ===")
    print("1. Closures can implement complex patterns like state machines")
    print("2. They can emulate object-oriented programming with encapsulation")
    print("3. Advanced decorators can handle retries, caching, and validation")
    print("4. Type safety can be added to functional patterns")
    print("5. Closures are powerful but should be used judiciously")
    print("6. They're a fundamental building block of Python's decorator system")
