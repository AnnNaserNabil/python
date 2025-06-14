"""
10. Advanced Recursion Techniques

Advanced recursion concepts and optimizations.
- Memoization and caching
- Tail call optimization (TCO) simulation
- Continuation-passing style (CPS)
- Recursive descent parsing
- Mutual recursion
"""
from __future__ import annotations
from typing import TypeVar, Generic, Callable, Any, Dict, List, Optional, Tuple, Set
from functools import lru_cache, wraps
import sys
import time

T = TypeVar('T')
U = TypeVar('U')

# 1. Memoization with Custom Cache
class Memoize:
    """Memoization decorator with custom cache."""
    def __init__(self, func: Callable[..., T]):
        self.func = func
        self.cache: Dict[Any, T] = {}
    
    def __call__(self, *args: Any, **kwargs: Any) -> T:
        key = (args, frozenset(kwargs.items()))
        if key not in self.cache:
            self.cache[key] = self.func(*args, **kwargs)
        return self.cache[key]
    
    def clear_cache(self) -> None:
        """Clear the memoization cache."""
        self.cache.clear()

# 2. Tail Call Optimization Simulation
class TailCall(Exception):
    """Exception to return a tail call."""
    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs

def tco_optimized(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that simulates tail call optimization."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        while isinstance(result, TailCall):
            result = result.func(*result.args, **result.kwargs)
        return result
    return wrapper

# 3. Continuation-Passing Style (CPS)
class Continuation:
    """Continuation for CPS style programming."""
    def __init__(self, func: Callable[..., Any]):
        self.func = func
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

def cps_factorial(n: int, cont: Continuation) -> Any:
    """Factorial in CPS style."""
    if n == 0:
        return cont(1)
    return cps_factorial(n - 1, Continuation(lambda x: cont(n * x)))

def trampoline_cps_factorial(n: int, cont: Continuation) -> Any:
    """Trampolined CPS factorial to avoid stack overflow."""
    result = cps_factorial(n, cont)
    while callable(result):
        result = result()
    return result

# 4. Recursive Descent Parser
class Parser:
    """Simple recursive descent parser for arithmetic expressions."""
    def __init__(self, text: str):
        self.tokens = self.tokenize(text)
        self.pos = 0
    
    def tokenize(self, text: str) -> List[str]:
        """Convert input text into tokens."""
        import re
        # Match numbers, operators, and parentheses
        token_pattern = r'\d+|[+\-*/()]|\S+'
        return re.findall(token_pattern, text)
    
    def current_token(self) -> Optional[str]:
        """Get the current token."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def eat(self, token: str) -> None:
        """Consume the current token if it matches the expected token."""
        if self.current_token() == token:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {token}, got {self.current_token()}")
    
    def parse(self) -> int:
        """Parse the expression and return the result."""
        result = self.expr()
        if self.pos < len(self.tokens):
            raise SyntaxError(f"Unexpected token: {self.current_token()}")
        return result
    
    def expr(self) -> int:
        """Parse addition and subtraction."""
        result = self.term()
        
        while self.current_token() in ('+', '-'):
            op = self.current_token()
            self.eat(op)
            right = self.term()
            if op == '+':
                result += right
            else:
                result -= right
        
        return result
    
    def term(self) -> int:
        """Parse multiplication and division."""
        result = self.factor()
        
        while self.current_token() in ('*', '/'):
            op = self.current_token()
            self.eat(op)
            right = self.factor()
            if op == '*':
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                result //= right
        
        return result
    
    def factor(self) -> int:
        """Parse numbers and parenthesized expressions."""
        token = self.current_token()
        
        if token == '(':
            self.eat('(')
            result = self.expr()
            self.eat(')')
            return result
        elif token and token.isdigit():
            self.eat(token)
            return int(token)
        else:
            raise SyntaxError(f"Unexpected token: {token}")

# 5. Mutual Recursion
def is_even(n: int) -> bool:
    """Check if a number is even using mutual recursion."""
    if n == 0:
        return True
    return is_odd(n - 1)

def is_odd(n: int) -> bool:
    """Check if a number is odd using mutual recursion."""
    if n == 0:
        return False
    return is_even(n - 1)

# 6. Memoization with Function Attributes
def memoize_attr(func: Callable[..., T]) -> Callable[..., T]:
    """Memoization using function attributes."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        if not hasattr(func, '_cache'):
            func._cache = {}  # type: ignore
        
        key = (args, frozenset(kwargs.items()))
        if key not in func._cache:  # type: ignore
            func._cache[key] = func(*args, **kwargs)  # type: ignore
        return func._cache[key]  # type: ignore
    
    return wrapper

# 7. Dynamic Programming: Longest Common Subsequence
@memoize_attr
def lcs(s1: str, s2: str, i: int = 0, j: int = 0) -> int:
    """Find the length of the longest common subsequence."""
    if i == len(s1) or j == len(s2):
        return 0
    
    if s1[i] == s2[j]:
        return 1 + lcs(s1, s2, i + 1, j + 1)
    else:
        return max(lcs(s1, s2, i + 1, j), lcs(s1, s2, i, j + 1))

# 8. Trampoline for Deep Recursion
def trampoline(func: Callable[..., Any]) -> Callable[..., Any]:
    """Trampoline decorator for deep recursion."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        while callable(result):
            result = result()
        return result
    return wrapper

# 9. Y-combinator for Anonymous Recursion
def y_combinator(f: Callable[..., Any]) -> Callable[..., Any]:
    """Y-combinator for anonymous recursion."""
    return (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))

# 10. Memoized Fibonacci with Y-combinator
@memoize_attr
def y_fib(n: int) -> int:
    """Fibonacci using Y-combinator and memoization."""
    if n <= 1:
        return n
    return y_fib(n - 1) + y_fib(n - 2)

def demonstrate_advanced_recursion() -> None:
    """Demonstrate advanced recursion techniques."""
    print("=== Memoization with Custom Cache ===")
    
    @Memoize
    def fib(n: int) -> int:
        """Fibonacci with custom memoization."""
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    
    print(f"fib(35) with custom memoization: {fib(35)}")
    
    print("\n=== Tail Call Optimization Simulation ===")
    
    @tco_optimized
    def factorial_tco(n: int, acc: int = 1) -> Any:
        """Tail-recursive factorial with TCO."""
        if n == 0:
            return acc
        return TailCall(factorial_tco, n - 1, n * acc)
    
    print(f"factorial_tco(10) = {factorial_tco(10)}")
    
    print("\n=== Continuation-Passing Style (CPS) ===")
    
    def identity(x: Any) -> Any:
        return x
    
    print(f"5! in CPS: {trampoline_cps_factorial(5, Continuation(identity))}")
    
    print("\n=== Recursive Descent Parser ===")
    
    expressions = [
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "10 / 2 - 3",
        "2 * (3 + 4) * 5"
    ]
    
    for expr in expressions:
        try:
            parser = Parser(expr)
            result = parser.parse()
            print(f"{expr} = {result}")
        except (SyntaxError, ZeroDivisionError) as e:
            print(f"Error parsing '{expr}': {e}")
    
    print("\n=== Mutual Recursion ===")
    for i in range(6):
        print(f"{i} is {'even' if is_even(i) else 'odd'}")
    
    print("\n=== Longest Common Subsequence ===")
    s1 = "ABCBDAB"
    s2 = "BDCABA"
    print(f"LCS of '{s1}' and '{s2}': {lcs(s1, s2)}")
    
    print("\n=== Y-combinator for Anonymous Recursion ===")
    print(f"Fibonacci(10) with Y-combinator: {y_fib(10)}")

if __name__ == "__main__":
    demonstrate_advanced_recursion()
    
    print("\n=== Key Takeaways ===")
    print("1. Memoization caches function results to avoid redundant calculations")
    print("2. Tail call optimization can prevent stack overflow in tail-recursive functions")
    print("3. Continuation-passing style (CPS) makes control flow explicit")
    print("4. Recursive descent parsers are easy to implement for simple grammars")
    print("5. Mutual recursion involves functions that call each other")
    print("6. The Y-combinator enables recursion in languages without native support")
