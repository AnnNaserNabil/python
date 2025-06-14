"""
5. The State Monad

The State monad represents computations that carry a state that can be updated.
It allows for pure functional stateful computations.
"""
from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, Tuple, cast
from dataclasses import dataclass

S = TypeVar('S')  # State type
A = TypeVar('A')  # Result type
B = TypeVar('B')

class State(Generic[S, A]):
    """The State monad."""
    
    def __init__(self, run: Callable[[S], Tuple[A, S]]):
        self._run = run
    
    @classmethod
    def unit(cls, value: A) -> State[S, A]:
        """Create a state computation that returns the given value and leaves the state unchanged."""
        return State(lambda s: (value, s))
    
    def bind(self, f: Callable[[A], State[S, B]]) -> State[S, B]:
        """Chain state computations."""
        def run(s: S) -> Tuple[B, S]:
            a, new_s = self.run(s)
            return f(a).run(new_s)
        return State(run)
    
    def map(self, f: Callable[[A], B]) -> State[S, B]:
        """Map a function over the result of the state computation."""
        return self.bind(lambda a: State.unit(f(a)))
    
    def run(self, initial_state: S) -> Tuple[A, S]:
        """Run the state computation with the given initial state."""
        return self._run(initial_state)
    
    def exec(self, initial_state: S) -> S:
        """Run the computation and return the final state."""
        return self.run(initial_state)[1]
    
    def eval(self, initial_state: S) -> A:
        """Run the computation and return the final value."""
        return self.run(initial_state)[0]
    
    @classmethod
    def get(cls) -> State[S, S]:
        """Get the current state."""
        return State(lambda s: (s, s))
    
    @classmethod
    def put(cls, new_state: S) -> State[S, None]:
        """Set a new state."""
        return State(lambda _: (None, new_state))
    
    @classmethod
    def modify(cls, f: Callable[[S], S]) -> State[S, None]:
        """Modify the current state using a function."""
        return State.get().bind(lambda s: State.put(f(s)))
    
    def __or__(self, f: Callable[[A], State[S, B]]) -> State[S, B]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[A], State[S, B]]) -> State[S, B]:
        """Override >> operator for chaining."""
        return self.bind(f)

# Example usage
def demonstrate() -> None:
    """Demonstrate the State monad."""
    print("=== State Monad ===\n")
    
    # 1. Basic usage
    print("1. Basic usage:")
    
    # A simple state computation that increments a counter
    def increment() -> State[int, int]:
        return (
            State.get()
            .bind(lambda s: (
                State.put(s + 1)
                .bind(lambda _: State.unit(s + 1))
            ))
        )
    
    # Run the computation with an initial state
    result, new_state = increment().run(0)
    print(f"Increment from 0: result={result}, new_state={new_state}")
    
    # 2. Chaining stateful operations
    print("\n2. Chaining operations:")
    
    computation = (
        State.unit(0)  # Start with value 0
        .bind(lambda _: increment())  # 0 -> 1
        .bind(lambda x: increment().map(lambda y: x + y))  # 1 -> 2, then 1 + 2
    )
    
    result, state = computation.run(0)
    print(f"Result: {result}, Final state: {state}")
    
    # 3. Using modify
    print("\n3. Using modify:")
    
    def add_to_state(n: int) -> State[int, None]:
        return State.modify(lambda s: s + n)
    
    computation = (
        add_to_state(5)
        .bind(lambda _: add_to_state(3))
        .bind(lambda _: State.get())
    )
    
    result, state = computation.run(0)
    print(f"Final state: {state}")
    
    # 4. Stack example
    print("\n4. Stack operations:")
    
    def push(x: int) -> State[list[int], None]:
        return State.modify(lambda s: [x] + s)
    
    def pop() -> State[list[int], int]:
        return (
            State.get()
            .bind(lambda s: (
                State.put(s[1:])  # Update state to remove the top element
                .bind(lambda _: State.unit(s[0]))  # Return the popped element
            ) if s else State.unit(0)  # Default to 0 if stack is empty
        ))
    
    # A computation that manipulates a stack
    stack_computation = (
        push(1)
        .bind(lambda _: push(2))
        .bind(lambda _: push(3))
        .bind(lambda _: pop())  # Pop 3
        .bind(lambda x: (
            push(x * 2)  # Push 6
            .bind(lambda _: pop())  # Pop 6
            .bind(lambda y: (
                push(x + y)  # Push 9 (3 + 6)
                .bind(lambda _: State.get())  # Get the final state
            ))
        ))
    )
    
    result, final_stack = stack_computation.run([])
    print(f"Final stack: {final_stack}")
    
    # 5. Complex example: Bank account
    print("\n5. Bank account simulation:")
    
    @dataclass
    class Account:
        balance: float
        transactions: list[str]
    
    def deposit(amount: float) -> State[Account, float]:
        """Deposit money into the account."""
        return (
            State.get()
            .bind(lambda acc: (
                State.put(Account(
                    acc.balance + amount,
                    acc.transactions + [f"Deposit: +{amount}"]
                ))
                .bind(lambda _: State.unit(acc.balance + amount))
            ))
        )
    
    def withdraw(amount: float) -> State[Account, float]:
        """Withdraw money from the account."""
        return (
            State.get()
            .bind(lambda acc: (
                State.put(Account(
                    acc.balance - amount,
                    acc.transactions + [f"Withdrawal: -{amount}"]
                ))
                .bind(lambda _: State.unit(acc.balance - amount))
                if acc.balance >= amount
                else State.unit(acc.balance)  # Not enough funds
            ))
        )
    
    def get_balance() -> State[Account, float]:
        """Get the current balance."""
        return State.get().map(lambda acc: acc.balance)
    
    def get_transactions() -> State[Account, list[str]]:
        """Get the transaction history."""
        return State.get().map(lambda acc: acc.transactions)
    
    # A sequence of banking operations
    banking = (
        deposit(100.0)
        .bind(lambda _: withdraw(30.0))
        .bind(lambda _: deposit(50.0))
        .bind(lambda _: withdraw(20.0))
        .bind(lambda _: get_balance())
        .bind(lambda bal: (
            get_transactions()
            .map(lambda txns: (bal, txns))
        ))
    )
    
    # Run the banking operations with an initial account
    initial_account = Account(0.0, ["Account opened"])
    (final_balance, transactions), _ = banking.run(initial_account)
    
    print(f"Final balance: ${final_balance:.2f}")
    print("Transaction history:")
    for txn in transactions:
        print(f"  - {txn}")
    
    # 6. Parser combinator example
    print("\n6. Parser combinator example:")
    
    # A parser takes an input string and returns a result and remaining input
    Parser = State[str, A]
    
    def char(c: str) -> Parser[str]:
        """Parse a specific character."""
        def parse(s: str) -> Tuple[str, str]:
            if s and s[0] == c:
                return (c, s[1:])
            raise ValueError(f"Expected '{c}', got '{s[:10]}...'")
        return State(parse)
    
    def any_char() -> Parser[str]:
        """Parse any single character."""
        def parse(s: str) -> Tuple[str, str]:
            if s:
                return (s[0], s[1:])
            raise ValueError("Unexpected end of input")
        return State(parse)
    
    def many(p: Parser[A]) -> Parser[list[A]]:
        """Parse zero or more occurrences of p."""
        def parse(s: str) -> Tuple[list[A], str]:
            result = []
            remaining = s
            while True:
                try:
                    value, remaining = p.run(remaining)
                    result.append(value)
                except ValueError:
                    break
            return (result, remaining)
        return State(parse)
    
    def choice(*parsers: Parser[A]) -> Parser[A]:
        """Try each parser in order until one succeeds."""
        if not parsers:
            raise ValueError("No parsers provided")
        
        def parse(s: str) -> Tuple[A, str]:
            for parser in parsers:
                try:
                    return parser.run(s)
                except ValueError:
                    continue
            raise ValueError("No matching parser found")
        
        return State(parse)
    
    # Example: Parse a simple arithmetic expression
    def number() -> Parser[int]:
        """Parse a sequence of digits as an integer."""
        def parse_digit() -> Parser[int]:
            return any_char().bind(
                lambda c: State.unit(int(c)) if c.isdigit() 
                else State(lambda _: (0, ""))  # This will be caught by many()
            )
        
        return many(parse_digit()).bind(
            lambda ds: State.unit(int(''.join(map(str, ds)))) if ds 
            else State(lambda _: (0, ""))  # Shouldn't happen due to many()
        )
    
    def add_expr() -> Parser[int]:
        """Parse addition expressions."""
        return (
            number()
            .bind(lambda x: (
                many(
                    char('+').bind(
                        lambda _: number().map(lambda y: ('+', y))
                    )
                )
                .bind(lambda ops: State.unit(
                    x + sum(y for op, y in ops if op == '+')
                ))
            ))
        )
    
    # Test the parser
    expr = "1+2+3"
    try:
        result, remaining = add_expr().run(expr)
        if remaining:
            print(f"Parsed '{expr}' as {result} (remaining: '{remaining}')")
        else:
            print(f"Successfully parsed '{expr}' as {result}")
    except ValueError as e:
        print(f"Failed to parse '{expr}': {e}")

if __name__ == "__main__":
    demonstrate()
