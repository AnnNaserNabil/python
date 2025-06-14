"""
3. Partial Application with Objects

This module demonstrates how to use partial application with object-oriented
programming, including method binding, instance methods, and class methods.
"""
from functools import partial, partialmethod
from typing import Any, Callable, TypeVar, Optional, List, Dict

T = TypeVar('T')
U = TypeVar('U')

class DataProcessor:
    """A class that processes data with configurable steps."""
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.steps: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []
    
    def add_step(self, step: Callable[[Dict[str, Any]], Dict[str, Any]]) -> 'DataProcessor':
        """Add a processing step."""
        self.steps.append(step)
        return self
    
    def process(self) -> List[Dict[str, Any]]:
        """Process the data through all steps."""
        result = self.data.copy()
        for step in self.steps:
            result = [step(item) for item in result]
        return result
    
    @classmethod
    def create_processor(
        cls, 
        data: List[Dict[str, Any]],
        *steps: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> 'DataProcessor':
        """Create a processor with predefined steps."""
        processor = cls(data)
        for step in steps:
            processor.add_step(step)
        return processor

class StringTransformer:
    """A class that demonstrates method binding with partial."""
    
    def __init__(self, prefix: str = "", suffix: str = ""):
        self.prefix = prefix
        self.suffix = suffix
    
    def transform(self, text: str, *, upper: bool = False, reverse: bool = False) -> str:
        """Transform the text with prefix, suffix, and optional modifications."""
        result = f"{self.prefix}{text}{self.suffix}"
        if upper:
            result = result.upper()
        if reverse:
            result = result[::-1]
        return result
    
    def create_transformer(self, **kwargs) -> Callable[[str], str]:
        """Create a transformer function with some arguments pre-filled."""
        return partial(self.transform, **kwargs)

class MathOperations:
    """A class that demonstrates class methods with partial application."""
    
    @classmethod
    def power(cls, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        return base ** exponent
    
    @classmethod
    def create_power_function(cls, exponent: float) -> Callable[[float], float]:
        """Create a power function with a fixed exponent."""
        return partial(cls.power, exponent=exponent)
    
    @staticmethod
    def multiply(x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y
    
    @classmethod
    def create_multiplier(cls, factor: float) -> Callable[[float], float]:
        """Create a multiplier function with a fixed factor."""
        return partial(cls.multiply, y=factor)

def demonstrate() -> None:
    """Demonstrate partial application with objects."""
    print("=== Partial Application with Objects ===\n")
    
    # 1. Using partial with instance methods
    print("1. Partial with instance methods:")
    
    transformer = StringTransformer("**", "**")
    
    # Create specialized transformers
    make_bold = partial(transformer.transform, upper=True)
    make_reversed = partial(transformer.transform, reverse=True)
    
    print(f"make_bold('hello'): {make_bold('hello')}")
    print(f"make_reversed('hello'): {make_reversed('hello')}")
    
    # 2. Using partialmethod for class method binding
    print("\n2. Using partialmethod for class method binding:")
    
    class Greeter:
        def __init__(self, greeting: str = "Hello"):
            self.greeting = greeting
        
        def greet(self, name: str, punctuation: str = "!") -> str:
            return f"{self.greeting}, {name}{punctuation}"
        
        # Create a method with a fixed punctuation
        greet_excited = partialmethod(greet, punctuation="!!!")
    
    greeter = Greeter("Hi there")
    print(f"greeter.greet('Alice'): {greeter.greet('Alice')}")
    print(f"greeter.greet_excited('Bob'): {greeter.greet_excited('Bob')}")
    
    # 3. Class methods with partial application
    print("\n3. Class methods with partial application:")
    
    # Create specialized power functions
    square = MathOperations.create_power_function(2)
    cube = MathOperations.create_power_function(3)
    
    print(f"square(5): {square(5)}  # 5² = 25")
    print(f"cube(3): {cube(3)}  # 3³ = 27")
    
    # Create specialized multipliers
    double = MathOperations.create_multiplier(2)
    triple = MathOperations.create_multiplier(3)
    
    print(f"double(4): {double(4)}  # 2 * 4 = 8")
    print(f"triple(4): {triple(4)}  # 3 * 4 = 12")
    
    # 4. Data processing pipeline with objects
    print("\n4. Data processing pipeline with objects:")
    
    # Sample data
    data = [
        {"name": "Alice", "score": 85, "subject": "Math"},
        {"name": "Bob", "score": 90, "subject": "Math"},
        {"name": "Charlie", "score": 78, "subject": "Science"},
        {"name": "Diana", "score": 92, "subject": "Science"},
    ]
    
    # Define processing steps as methods
    def add_letter_grade(item: Dict[str, Any]) -> Dict[str, Any]:
        score = item["score"]
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        else:
            grade = "F"
        return {**item, "grade": grade}
    
    def add_passing_status(item: Dict[str, Any], passing_grade: str = "D") -> Dict[str, Any]:
        return {
            **item, 
            "passed": item.get("grade", "F") < passing_grade
        }
    
    # Create a processor with specific steps
    processor = DataProcessor(data)
    
    # Add steps with partial application
    processor.add_step(add_letter_grade)
    
    # Create a specialized passing function
    is_passing_math = partial(add_passing_status, passing_grade="C")
    is_passing_science = partial(add_passing_status, passing_grade="B")
    
    # Add conditional step based on subject
    def process_item(item: Dict[str, Any]) -> Dict[str, Any]:
        if item["subject"] == "Math":
            return is_passing_math(item)
        else:
            return is_passing_science(item)
    
    processor.add_step(process_item)
    
    # Process the data
    results = processor.process()
    
    print("\nProcessed data:")
    for item in results:
        print(f"- {item['name']} ({item['subject']}): {item['score']} {item['grade']} "
              f"{'PASS' if item['passed'] else 'FAIL'}")
    
    # 5. Method chaining with partial application
    print("\n5. Method chaining with partial application:")
    
    class QueryBuilder:
        def __init__(self):
            self.filters: List[Callable[[Dict[str, Any]], bool]] = []
            self.sorts: List[Callable[[Dict[str, Any]], Any]] = []
            self.limit_value: Optional[int] = None
        
        def filter_by(self, key: str, value: Any) -> 'QueryBuilder':
            """Add an equality filter."""
            self.filters.append(lambda item, k=key, v=value: item.get(k) == v)
            return self
        
        def sort_by(self, key: str, reverse: bool = False) -> 'QueryBuilder':
            """Add a sort key."""
            self.sorts.append(lambda item, k=key: item.get(k))
            self.sorts.reverse()  # To apply sorts in the correct order
            return self
        
        def limit(self, n: int) -> 'QueryBuilder':
            """Set a result limit."""
            self.limit_value = n
            return self
        
        def apply(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """Apply all filters and sorts to the data."""
            # Apply filters
            result = data.copy()
            
            for filter_func in self.filters:
                result = [item for item in result if filter_func(item)]
            
            # Apply sorts (in reverse order to get the correct priority)
            for sort_key in reversed(self.sorts):
                result.sort(key=sort_key)
            
            # Apply limit
            if self.limit_value is not None:
                result = result[:self.limit_value]
            
            return result
    
    # Create a query builder with some pre-configured filters
    def create_math_query(score_threshold: int = 0) -> QueryBuilder:
        """Create a query for math students with a minimum score."""
        return (
            QueryBuilder()
            .filter_by("subject", "Math")
            .filter_by("score", lambda x: x >= score_threshold)
            .sort_by("score", reverse=True)
        )
    
    # Create specialized query builders
    top_math_students = create_math_query(85)
    passing_math_students = create_math_query(70)
    
    # Execute queries
    print("\nTop math students (score >= 85):")
    for student in top_math_students.apply(data):
        print(f"- {student['name']}: {student['score']}")
    
    print("\nAll passing math students (score >= 70):")
    for student in passing_math_students.apply(data):
        print(f"- {student['name']}: {student['score']}")

if __name__ == "__main__":
    demonstrate()
