"""
4. The Writer Monad

The Writer monad represents computations that produce a value along with
some "output" or "log" that is accumulated during the computation.
"""
from __future__ import annotations
from typing import Any, Callable, Generic, List, TypeVar, Tuple, Union, cast
from dataclasses import dataclass
from functools import reduce

W = TypeVar('W')  # Log type (must be a monoid)
A = TypeVar('A')  # Value type
B = TypeVar('B')

class Monoid(Generic[W]):
    """Type class for monoids."""
    
    @staticmethod
    def mempty() -> W:
        """The identity element of the monoid."""
        raise NotImplementedError
    
    @staticmethod
    def mappend(a: W, b: W) -> W:
        """The binary operation of the monoid."""
        raise NotImplementedError

class ListMonoid(Monoid[List[T]]):
    """List monoid (for logging)."""
    
    @staticmethod
    def mempty() -> List[T]:
        return []
    
    @staticmethod
    def mappend(a: List[T], b: List[T]) -> List[T]:
        return a + b

class StringMonoid(Monoid[str]):
    """String monoid (for string concatenation)."""
    
    @staticmethod
    def mempty() -> str:
        return ""
    
    @staticmethod
    def mappend(a: str, b: str) -> str:
        return a + b

class Writer(Generic[W, A]):
    """The Writer monad."""
    
    def __init__(self, value: A, log: W, monoid: Monoid[W]):
        self._value = value
        self._log = log
        self._monoid = monoid
    
    @classmethod
    def unit(cls, value: A, monoid: Monoid[W]) -> Writer[W, A]:
        """Create a writer with an empty log."""
        return cls(value, monoid.mempty(), monoid)
    
    @classmethod
    def tell(cls, log: W, monoid: Monoid[W]) -> Writer[W, None]:
        """Create a writer that just logs a value."""
        return cls(None, log, monoid)
    
    def bind(self, f: Callable[[A], Writer[W, B]]) -> Writer[W, B]:
        """Chain operations, combining their logs."""
        result = f(self._value)
        return Writer(
            result._value,
            self._monoid.mappend(self._log, result._log),
            self._monoid
        )
    
    def map(self, f: Callable[[A], B]) -> Writer[W, B]:
        """Map a function over the value."""
        return Writer(f(self._value), self._log, self._monoid)
    
    def run(self) -> Tuple[A, W]:
        """Run the computation, returning the value and log."""
        return (self._value, self._log)
    
    def exec(self) -> W:
        """Run the computation, returning just the log."""
        return self._log
    
    def __or__(self, f: Callable[[A], Writer[W, B]]) -> Writer[W, B]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[A], Writer[W, B]]) -> Writer[W, B]:
        """Override >> operator for chaining."""
        return self.bind(f)
    
    def __str__(self) -> str:
        return f"Writer(value={self._value}, log={self._log})"

# Example usage
def demonstrate() -> None:
    """Demonstrate the Writer monad."""
    print("=== Writer Monad ===\n")
    
    # 1. Basic usage with list monoid
    print("1. Basic usage with list monoid:")
    
    # Create a writer with a value and a log
    writer1 = Writer(42, ["Initial value: 42"], ListMonoid())
    print(f"Writer 1: {writer1}")
    
    # Chain operations
    def add(x: int) -> Writer[List[str], int]:
        return Writer(x + 1, [f"Added 1 to get {x + 1}"], ListMonoid())
    
    def double(x: int) -> Writer[List[str], int]:
        return Writer(x * 2, [f"Doubled to get {x * 2}"], ListMonoid())
    
    computation = (
        Writer.unit(5, ListMonoid())
        .bind(add)
        .bind(double)
        .bind(add)
    )
    
    value, log = computation.run()
    print(f"Final value: {value}")
    print("Log:")
    for entry in log:
        print(f"  - {entry}")
    
    # 2. Using string monoid
    print("\n2. Using string monoid:")
    
    def log_message(msg: str) -> Writer[str, None]:
        return Writer.tell(f"{msg}\n", StringMonoid())
    
    def greet(name: str) -> Writer[str, str]:
        return (
            log_message(f"Greeting {name}")
            .bind(lambda _: Writer.unit(f"Hello, {name}!", StringMonoid()))
        )
    
    def farewell(name: str) -> Writer[str, str]:
        return (
            log_message(f"Farewell to {name}")
            .bind(lambda _: Writer.unit(f"Goodbye, {name}!", StringMonoid()))
        )
    
    def conversation(name: str) -> Writer[str, str]:
        return (
            greet(name)
            .bind(lambda g: (
                log_message("Having a conversation...")
                .bind(lambda _: farewell(name))
                .map(lambda f: f"{g} {f}")
            ))
        )
    
    conv_result, conv_log = conversation("Alice").run()
    print(f"Result: {conv_result}")
    print("Conversation log:")
    print(conv_log)
    
    # 3. More complex example: Expression evaluator with logging
    print("\n3. Expression evaluator with logging:")
    
    class Expr:
        pass
    
    @dataclass
    class Const(Expr):
        value: int
    
    @dataclass
    class Add(Expr):
        left: Expr
        right: Expr
    
    @dataclass
    class Mul(Expr):
        left: Expr
        right: Expr
    
    def eval_expr(expr: Expr) -> Writer[List[str], int]:
        """Evaluate an expression with logging."""
        if isinstance(expr, Const):
            return Writer.unit(expr.value, ListMonoid())
        elif isinstance(expr, Add):
            return (
                eval_expr(expr.left)
                .bind(lambda l: (
                    eval_expr(expr.right)
                    .bind(lambda r: (
                        Writer(
                            l + r,
                            [f"Added {l} + {r} = {l + r}"],
                            ListMonoid()
                        )
                    ))
                ))
            )
        elif isinstance(expr, Mul):
            return (
                eval_expr(expr.left)
                .bind(lambda l: (
                    eval_expr(expr.right)
                    .bind(lambda r: (
                        Writer(
                            l * r,
                            [f"Multiplied {l} * {r} = {l * r}"],
                            ListMonoid()
                        )
                    ))
                ))
            )
        else:
            raise ValueError(f"Unknown expression type: {type(expr)}")
    
    # Expression: (2 + 3) * 4
    expr = Mul(Add(Const(2), Const(3)), Const(4))
    
    print("Evaluating expression: (2 + 3) * 4")
    result, log = eval_expr(expr).run()
    print(f"Result: {result}")
    print("Evaluation steps:")
    for step in log:
        print(f"  - {step}")
    
    # 4. Using Writer for performance measurement
    print("\n4. Performance measurement:")
    
    @dataclass
    class Timing:
        """Monoid for tracking time."""
        elapsed: float = 0.0
        
        @staticmethod
        def mempty() -> 'Timing':
            return Timing(0.0)
        
        @staticmethod
        def mappend(a: 'Timing', b: 'Timing') -> 'Timing':
            return Timing(a.elapsed + b.elapsed)
        
        def measure(self, name: str, func: Callable[[], A]) -> Tuple[A, 'Timing']:
            import time
            start = time.time()
            result = func()
            elapsed = time.time() - start
            print(f"{name}: {elapsed:.6f}s")
            return result, Timing(self.elapsed + elapsed)
    
    def timed[A](name: str, func: Callable[[], A]) -> Writer[Timing, A]:
        """Time a computation."""
        def run(timing: Timing) -> Tuple[A, Timing]:
            return timing.measure(name, func)
        
        return Writer(
            None,
            Timing(),
            type('TimingMonoid', (), {
                'mempty': Timing.mempty,
                'mappend': Timing.mappend
            })
        ).bind(lambda _: Writer(run, Timing(), Timing))  # type: ignore
    
    def slow_function() -> int:
        import time
        time.sleep(0.1)
        return 42
    
    def another_function(x: int) -> int:
        import time
        time.sleep(0.2)
        return x * 2
    
    computation = (
        timed("slow_function", slow_function)
        .bind(lambda x: timed("another_function", lambda: another_function(x)))
    )
    
    result, timing = computation.run()
    print(f"Final result: {result}")
    print(f"Total time: {timing.elapsed:.6f}s")

if __name__ == "__main__":
    demonstrate()
