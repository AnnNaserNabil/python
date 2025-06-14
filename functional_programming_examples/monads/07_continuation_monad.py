"""
7. The Continuation Monad

The Continuation monad represents computations in continuation-passing style (CPS).
It's a powerful abstraction that can be used to implement control flow operators,
coroutines, and more.
"""
from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, cast
from functools import partial

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
R = TypeVar('R')

# A continuation is a function that takes a value and returns a result
Continuation = Callable[[A], R]

class Cont(Generic[R, A]):
    """The Continuation monad."""
    
    def __init__(self, run_cont: Callable[[Continuation[A, R]], R]):
        self._run_cont = run_cont
    
    def run_cont(self, k: Continuation[A, R]) -> R:
        """Run the continuation with the given continuation function."""
        return self._run_cont(k)
    
    @classmethod
    def unit(cls, value: A) -> Cont[R, A]:
        """Lift a value into the continuation monad."""
        return cls(lambda k: k(value))
    
    def bind(self, f: Callable[[A], Cont[R, B]]) -> Cont[R, B]:
        """Chain continuation operations."""
        return Cont[R, B](lambda k: self.run_cont(lambda a: f(a).run_cont(k)))
    
    def map(self, f: Callable[[A], B]) -> Cont[R, B]:
        """Map a function over the continuation's result."""
        return self.bind(lambda x: Cont.unit(f(x)))
    
    @classmethod
    def call_cc(cls, f: Callable[[Callable[[A], Cont[R, B]]], Cont[R, A]]) -> Cont[R, A]:
        """Call with current continuation."""
        return Cont[R, A](lambda k: f(lambda a: Cont[R, B](lambda _: k(a))).run_cont(k))
    
    def __or__(self, f: Callable[[A], Cont[R, B]]) -> Cont[R, B]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[A], Cont[R, B]]) -> Cont[R, B]:
        """Override >> operator for chaining."""
        return self.bind(f)
    
    @classmethod
    def reset(cls, m: Cont[A, A]) -> Cont[R, A]:
        """Reset the continuation."""
        return cls.unit(m.run_cont(lambda x: x))
    
    @classmethod
    def shift(cls, f: Callable[[Callable[[A], Cont[R, R]]], Cont[R, R]]) -> Cont[R, A]:
        """Capture the current continuation."""
        return Cont[R, A](lambda k: f(lambda a: Cont.unit(k(a))).run_cont(lambda x: x))

# Example usage
def demonstrate() -> None:
    """Demonstrate the Continuation monad."""
    print("=== Continuation Monad ===\n")
    
    # 1. Basic usage
    print("1. Basic usage:")
    
    # A simple continuation
    cont1 = Cont.unit(5).map(lambda x: x * 2)
    result1 = cont1.run_cont(lambda x: x)
    print(f"Cont.unit(5).map(x => x * 2) = {result1}")
    
    # Chaining operations
    cont2 = (
        Cont.unit(5)
        .bind(lambda x: Cont.unit(x + 3))
        .bind(lambda y: Cont.unit(y * 2))
    )
    result2 = cont2.run_cont(lambda x: x)
    print(f"5 + 3 * 2 = {result2}")
    
    # 2. Using call/cc (call with current continuation)
    print("\n2. Using call/cc:")
    
    def example_call_cc() -> Cont[int, int]:
        """Example using call/cc to implement early return."""
        return Cont.call_cc(lambda exit: (
            Cont.unit(1)
            .bind(lambda x: Cont.unit(x + 1))
            .bind(lambda x: exit(x * 10))  # Early return with x*10
            .bind(lambda _: Cont.unit(100))  # This is skipped
        ))
    
    result3 = example_call_cc().run_cont(lambda x: x)
    print(f"Example with call/cc: {result3}")
    
    # 3. Nested call/cc
    print("\n3. Nested call/cc:")
    
    def nested_call_cc() -> Cont[int, int]:
        """Example with nested call/cc."""
        return Cont.call_cc(lambda outer_exit: (
            Cont.call_cc(lambda inner_exit: (
                Cont.unit(1)
                .bind(lambda x: inner_exit(x * 10))  # Return from inner call/cc
                .bind(lambda _: Cont.unit(100))  # Skipped
            ))
            .bind(lambda x: Cont.unit(x + 1))  # This runs
            .bind(lambda x: outer_exit(x * 10))  # Return from outer call/cc
            .bind(lambda _: Cont.unit(1000))  # Skipped
        ))
    
    result4 = nested_call_cc().run_cont(lambda x: x)
    print(f"Nested call/cc: {result4}")
    
    # 4. Implementing a simple calculator with error handling
    print("\n4. Calculator with error handling:")
    
    def safe_divide(n: int, d: int) -> Cont[str, int]:
        """Safely divide two numbers with error handling."""
        return Cont.call_cc(lambda exit: (
            Cont.unit((n, d))
            .bind(lambda nd: (
                exit("Division by zero") if nd[1] == 0
                else Cont.unit(nd[0] // nd[1])
            ))
        ))
    
    def calculator(a: int, b: int, op: str) -> Cont[str, int]:
        """A simple calculator with error handling."""
        if op == "+":
            return Cont.unit(a + b)
        elif op == "-":
            return Cont.unit(a - b)
        elif op == "*":
            return Cont.unit(a * b)
        elif op == "/":
            return safe_divide(a, b)
        else:
            return Cont.unit(f"Unknown operator: {op}")
    
    def run_calculator(a: int, b: int, op: str) -> None:
        """Run the calculator and print the result."""
        result = calculator(a, b, op).run_cont(lambda x: x)
        if isinstance(result, str):
            print(f"{a} {op} {b} = Error: {result}")
        else:
            print(f"{a} {op} {b} = {result}")
    
    run_calculator(10, 2, "+")
    run_calculator(10, 2, "-")
    run_calculator(10, 2, "*")
    run_calculator(10, 2, "/")
    run_calculator(10, 0, "/")  # Division by zero
    run_calculator(10, 2, "%")  # Unknown operator
    
    # 5. Implementing a simple coroutine system
    print("\n5. Simple coroutine system:")
    
    class Coroutine(Generic[A, B]):
        """A simple coroutine using continuations."""
        
        def __init__(self, cont: Cont[Any, tuple[A, Coroutine[A, B]]]):
            self._cont = cont
        
        @classmethod
        def unit(cls, value: B) -> Coroutine[A, B]:
            """Create a coroutine that immediately returns a value."""
            return cls(Cont.unit((value, cls(Cont.unit((None, None))))))
        
        def bind(self, f: Callable[[B], Coroutine[A, C]]) -> Coroutine[A, C]:
            """Chain coroutines."""
            def next_cont(yb: tuple[B, Coroutine[A, B]]) -> Cont[Any, tuple[A, Coroutine[A, C]]]:
                y, next_coro = yb
                return f(y)._cont
            
            return Coroutine(self._cont.bind(next_cont))
        
        def send(self, value: A = None) -> tuple[B, Coroutine[A, B]]:
            """Send a value to the coroutine and get the next value and coroutine."""
            return self._cont.run_cont(lambda x: x)
        
        @classmethod
        def yield_value(cls, value: A) -> Coroutine[A, B]:
            """Yield a value from the coroutine."""
            return cls(Cont.call_cc(
                lambda k: Cont.unit((value, cls(k))))
            )
    
    # Example coroutine that yields values
    def counter(max_count: int) -> Coroutine[None, int]:
        """A coroutine that counts up to max_count."""
        def loop(n: int) -> Coroutine[None, int]:
            if n >= max_count:
                return Coroutine.unit(n)
            return (
                Coroutine.yield_value(n)
                .bind(lambda _: loop(n + 1))
            )
        return loop(0)
    
    # Run the counter coroutine
    print("Running counter coroutine:")
    coro = counter(5)
    
    while True:
        value, next_coro = coro.send()
        print(f"Got value: {value}")
        if next_coro._cont is None:
            break
        coro = next_coro
    
    # 6. Implementing generators with continuations
    print("\n6. Generators with continuations:")
    
    class Generator(Generic[A]):
        """A simple generator using continuations."""
        
        def __init__(self, cont: Cont[list[A], None]):
            self._cont = cont
        
        @classmethod
        def from_iterable(cls, iterable: list[A]) -> Generator[A]:
            """Create a generator from an iterable."""
            def loop(xs: list[A]) -> Cont[list[A], None]:
                if not xs:
                    return Cont.unit(None)
                return (
                    Cont.shift(lambda k: k(None))
                    .bind(lambda _: Cont.unit(xs[0]))
                    .bind(lambda x: (
                        Cont.shift(lambda k: k(None))
                        .bind(lambda _: loop(xs[1:]))
                    ))
                )
            return cls(loop(iterable))
        
        def to_list(self) -> list[A]:
            """Convert the generator to a list."""
            result: list[A] = []
            
            def collect(x: A) -> Cont[list[A], None]:
                result.append(x)
                return Cont.unit(None)
            
            self._cont.run_cont(lambda _: result)
            return result
    
    # Example generator
    gen = Generator.from_iterable([1, 2, 3, 4, 5])
    print(f"Generator to list: {gen.to_list()}")

if __name__ == "__main__":
    demonstrate()
