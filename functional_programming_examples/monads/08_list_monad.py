"""
8. The List Monad

The List monad represents computations that can return multiple results.
It's useful for modeling non-deterministic computations, backtracking,
and combinatorial problems.
"""
from __future__ import annotations
from typing import Any, Callable, Generic, Iterable, List, TypeVar, cast, overload
from functools import reduce

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class ListMonad(Generic[A]):
    """The List monad."""
    
    def __init__(self, values: List[A]):
        self._values = values
    
    @classmethod
    def unit(cls, value: A) -> ListMonad[A]:
        """Lift a value into the List monad."""
        return cls([value])
    
    @classmethod
    def empty(cls) -> ListMonad[A]:
        """Create an empty list monad."""
        return cls([])
    
    def bind(self, f: Callable[[A], ListMonad[B]]) -> ListMonad[B]:
        """Chain list operations (also known as flatMap)."""
        return ListMonad([
            y
            for x in self._values
            for y in f(x)._values
        ])
    
    def map(self, f: Callable[[A], B]) -> ListMonad[B]:
        """Map a function over the list."""
        return ListMonad([f(x) for x in self._values])
    
    def filter(self, predicate: Callable[[A], bool]) -> ListMonad[A]:
        """Filter the list based on a predicate."""
        return ListMonad([x for x in self._values if predicate(x)])
    
    def concat(self, other: ListMonad[A]) -> ListMonad[A]:
        """Concatenate two lists."""
        return ListMonad(self._values + other._values)
    
    def __or__(self, f: Callable[[A], ListMonad[B]]) -> ListMonad[B]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[A], ListMonad[B]]) -> ListMonad[B]:
        """Override >> operator for chaining."""
        return self.bind(f)
    
    def run(self) -> List[A]:
        """Extract the underlying list."""
        return self._values
    
    def __iter__(self):
        return iter(self._values)
    
    def __repr__(self) -> str:
        return f"ListMonad({self._values})"
    
    @classmethod
    def sequence(cls, lists: List[ListMonad[A]]) -> ListMonad[List[A]]:
        """Convert a list of ListMonads into a ListMonad of lists."""
        def cons(x: A, xs: ListMonad[List[A]]) -> ListMonad[List[A]]:
            return xs.map(lambda tail: [x] + tail)
        
        if not lists:
            return cls.unit([])
        
        return lists[0].bind(
            lambda x: cls.sequence(lists[1:]).bind(
                lambda xs: cls.unit([x] + xs)
            )
        )
    
    @classmethod
    def guard(cls, condition: bool) -> ListMonad[None]:
        """Guard a computation based on a condition."""
        return cls.unit(None) if condition else cls.empty()
    
    def when(self, condition: bool) -> ListMonad[None]:
        """Conditionally execute based on a condition."""
        return self if condition else ListMonad.empty()

# Example usage
def demonstrate() -> None:
    """Demonstrate the List monad."""
    print("=== List Monad ===\n")
    
    # 1. Basic usage
    print("1. Basic usage:")
    
    # Create list monads
    numbers = ListMonad([1, 2, 3])
    letters = ListMonad(['a', 'b'])
    
    print(f"Numbers: {numbers}")
    print(f"Letters: {letters}")
    
    # Map over a list
    doubled = numbers.map(lambda x: x * 2)
    print(f"Doubled: {doubled}")
    
    # 2. List comprehensions with bind
    print("\n2. List comprehensions:")
    
    # Equivalent to [x * y | x <- [1, 2, 3], y <- [10, 20]]
    products = numbers.bind(
        lambda x: ListMonad([10, 20]).map(
            lambda y: x * y
        )
    )
    print(f"Products: {products}")
    
    # Using operator overloading
    products_op = numbers >> (lambda x: 
        ListMonad([10, 20]) >> (lambda y: 
            ListMonad.unit(x * y)
        )
    )
    print(f"Products (with >>): {products_op}")
    
    # 3. Filtering with guard
    print("\n3. Filtering with guard:")
    
    # Generate all pairs where x + y is even
    even_sums = (
        numbers
        .bind(lambda x: 
            numbers
            .bind(lambda y: 
                ListMonad.guard((x + y) % 2 == 0)
                .bind(lambda _: ListMonad.unit((x, y)))
            )
        )
    )
    print(f"Pairs with even sum: {even_sums}")
    
    # 4. Pythagorean triples
    print("\n4. Pythagorean triples:")
    
    def pythagorean_triples(n: int) -> ListMonad[tuple[int, int, int]]:
        """Generate all pythagorean triples with a, b, c <= n."""
        return (
            ListMonad(range(1, n + 1))
            .bind(lambda a: 
                ListMonad(range(a + 1, n + 1))
                .bind(lambda b: 
                    ListMonad(range(b + 1, n + 1))
                    .bind(lambda c: 
                        ListMonad.guard(a*a + b*b == c*c)
                        .bind(lambda _: ListMonad.unit((a, b, c)))
                    )
                )
            )
        )
    
    triples = pythagorean_triples(20)
    print(f"Pythagorean triples up to 20: {triples.run()}")
    
    # 5. Permutations
    print("\n5. Permutations:")
    
    def permutations(xs: List[A]) -> ListMonad[List[A]]:
        """Generate all permutations of a list."""
        if not xs:
            return ListMonad.unit([])
            
        return (
            ListMonad(xs)
            .bind(lambda x: 
                permutations([y for y in xs if y != x])
                .map(lambda rest: [x] + rest)
            )
        )
    
    perms = permutations([1, 2, 3])
    print(f"Permutations of [1, 2, 3]: {perms.run()}")
    
    # 6. N-Queens problem
    print("\n6. N-Queens problem:")
    
    def nqueens(n: int) -> ListMonad[List[int]]:
        """Solve the N-Queens problem."""
        def place_queens(k: int) -> ListMonad[List[int]]:
            if k == 0:
                return ListMonad.unit([])
            else:
                return (
                    place_queens(k - 1)
                    .bind(lambda queens: 
                        ListMonad(range(1, n + 1))
                        .bind(lambda col: 
                            ListMonad.guard(
                                all(col != q and abs(col - q) != k - i - 1 
                                    for i, q in enumerate(queens))
                            )
                            .bind(lambda _: ListMonad.unit([col] + queens))
                        )
                    )
                )
        return place_queens(n)
    
    queens = nqueens(4)
    print(f"Solutions to 4-queens: {queens.run()}")
    
    # 7. Monadic parsing
    print("\n7. Monadic parsing:")
    
    class Parser(Generic[A]):
        def __init__(self, parse: Callable[[str], ListMonad[tuple[A, str]]]):
            self._parse = parse
        
        def parse(self, s: str) -> ListMonad[tuple[A, str]]:
            return self._parse(s)
        
        def __or__(self, other: Parser[A]) -> Parser[A]:
            """Choice combinator."""
            return Parser(lambda s: self.parse(s).concat(other.parse(s)))
        
        def bind(self, f: Callable[[A], Parser[B]]) -> Parser[B]:
            """Monadic bind for parsers."""
            def parse(s: str) -> ListMonad[tuple[B, str]]:
                return self.parse(s).bind(
                    lambda pair: f(pair[0]).parse(pair[1])
                )
            return Parser(parse)
        
        def map(self, f: Callable[[A], B]) -> Parser[B]:
            """Map over the result of a parser."""
            return self.bind(lambda x: Parser.unit(f(x)))
        
        @classmethod
        def unit(cls, value: A) -> Parser[A]:
            """A parser that always succeeds with the given value."""
            return cls(lambda s: ListMonad([(value, s)]))
        
        @classmethod
        def empty(cls) -> Parser[A]:
            """A parser that always fails."""
            return cls(lambda _: ListMonad([]))
        
        @classmethod
        def item(cls) -> Parser[str]:
            """Parse a single character."""
            def parse(s: str) -> ListMonad[tuple[str, str]]:
                return (
                    ListMonad([(s[0], s[1:])]) if s 
                    else ListMonad([])
                )
            return cls(parse)
        
        def many(self) -> Parser[List[A]]:
            """Parse zero or more occurrences."""
            return self.many1() | Parser.unit([])
        
        def many1(self) -> Parser[List[A]]:
            """Parse one or more occurrences."""
            return self.bind(
                lambda x: self.many().bind(
                    lambda xs: Parser.unit([x] + xs)
                )
            )
        
        def sep_by(self, sep: Parser[B]) -> Parser[List[A]]:
            """Parse zero or more occurrences separated by sep."""
            return self.sep_by1(sep) | Parser.unit([])
        
        def sep_by1(self, sep: Parser[B]) -> Parser[List[A]]:
            """Parse one or more occurrences separated by sep."""
            return self.bind(
                lambda x: (sep >> self).many().bind(
                    lambda xs: Parser.unit([x] + xs)
                )
            )
        
        def __rshift__(self, f: Callable[[A], Parser[B]]) -> Parser[B]:
            """Override >> operator for chaining."""
            return self.bind(f)
    
    # Basic parsers
    def char(c: str) -> Parser[str]:
        """Parse a specific character."""
        return Parser.item().bind(
            lambda x: Parser.unit(x) if x == c 
            else Parser.empty()
        )
    
    def digit() -> Parser[str]:
        """Parse a single digit."""
        return Parser.item().bind(
            lambda x: Parser.unit(x) if x.isdigit() 
            else Parser.empty()
        )
    
    # Example: Parse a simple arithmetic expression
    def expr() -> Parser[int]:
        """Parse addition and multiplication expressions."""
        return term().bind(
            lambda t: (char('+') >> expr() | Parser.unit(0)).bind(
                lambda e: Parser.unit(t + e)
            )
        )
    
    def term() -> Parser[int]:
        """Parse multiplication terms."""
        return factor().bind(
            lambda f: (char('*') >> term() | Parser.unit(1)).bind(
                lambda t: Parser.unit(f * t)
            )
        )
    
    def factor() -> Parser[int]:
        """Parse factors (numbers or parenthesized expressions)."""
        return number() | (char('(') >> expr() << char(')'))
    
    def number() -> Parser[int]:
        """Parse a non-negative integer."""
        return digit().many1().bind(
            lambda ds: Parser.unit(int(''.join(ds)))
        )
    
    # Test the parser
    test_expr = "2*(3+4)"
    result = expr().parse(test_expr)
    print(f"Parse result for '{test_expr}': {result.run()}")

if __name__ == "__main__":
    demonstrate()
