"""
6. The IO Monad

The IO monad represents computations that perform I/O operations.
It allows for pure functional handling of side effects.
"""
from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, cast
from dataclasses import dataclass
import sys
import os
import time

A = TypeVar('A')
B = TypeVar('B')

class IO(Generic[A]):
    """The IO monad for handling side effects."""
    
    def __init__(self, unsafe_run: Callable[[], A]):
        # Store the computation without running it
        self._unsafe_run = unsafe_run
    
    @classmethod
    def unit(cls, value: A) -> IO[A]:
        """Lift a pure value into the IO monad."""
        return IO(lambda: value)
    
    def bind(self, f: Callable[[A], IO[B]]) -> IO[B]:
        """Chain IO operations."""
        return IO(lambda: f(self.unsafe_run()).unsafe_run())
    
    def map(self, f: Callable[[A], B]) -> IO[B]:
        """Map a function over the result of the IO action."""
        return self.bind(lambda x: IO.unit(f(x)))
    
    def unsafe_run(self) -> A:
        """Run the IO action. This is the only impure function."""
        return self._unsafe_run()
    
    def __or__(self, f: Callable[[A], IO[B]]) -> IO[B]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[A], IO[B]]) -> IO[B]:
        """Override >> operator for chaining."""
        return self.bind(f)
    
    @classmethod
    def from_callable(cls, f: Callable[..., A], *args: Any, **kwargs: Any) -> IO[A]:
        """Lift a callable into the IO monad."""
        return IO(lambda: f(*args, **kwargs))
    
    @classmethod
    def print_line(cls, message: str) -> IO[None]:
        """Print a line to stdout."""
        return IO.from_callable(print, message)
    
    @classmethod
    def read_line(cls) -> IO[str]:
        """Read a line from stdin."""
        return IO(sys.stdin.readline)
    
    @classmethod
    def get_current_time(cls) -> IO[float]:
        """Get the current time."""
        return IO(time.time)
    
    @classmethod
    def sleep(cls, seconds: float) -> IO[None]:
        """Sleep for the given number of seconds."""
        return IO.from_callable(time.sleep, seconds)
    
    @classmethod
    def read_file(cls, path: str) -> IO[str]:
        """Read the entire contents of a file."""
        def read() -> str:
            with open(path, 'r') as f:
                return f.read()
        return IO(read)
    
    @classmethod
    def write_file(cls, path: str, content: str) -> IO[None]:
        """Write content to a file, overwriting if it exists."""
        def write() -> None:
            with open(path, 'w') as f:
                f.write(content)
        return IO(write)
    
    @classmethod
    def file_exists(cls, path: str) -> IO[bool]:
        """Check if a file exists."""
        return IO.from_callable(os.path.exists, path)
    
    @classmethod
    def get_environment_variable(cls, name: str) -> IO[Optional[str]]:
        """Get an environment variable."""
        return IO.from_callable(os.environ.get, name)
    
    @classmethod
    def sequence(cls, actions: list[IO[A]]) -> IO[list[A]]:
        """Run a list of IO actions in sequence and collect results."""
        def run() -> list[A]:
            return [action.unsafe_run() for action in actions]
        return IO(run)
    
    @classmethod
    def traverse(cls, values: list[A], f: Callable[[A], IO[B]]) -> IO[list[B]]:
        """Map each element to an IO action and collect the results."""
        return cls.sequence([f(v) for v in values])
    
    @classmethod
    def forever(cls, action: IO[A]) -> IO[None]:
        """Run an action repeatedly forever."""
        def loop() -> None:
            while True:
                action.unsafe_run()
        return IO(loop)
    
    @classmethod
    def when(cls, condition: bool, action: IO[None]) -> IO[None]:
        """Conditionally execute an action."""
        return action if condition else IO.unit(None)
    
    @classmethod
    def unless(cls, condition: bool, action: IO[None]) -> IO[None]:
        """Execute an action unless the condition is true."""
        return action if not condition else IO.unit(None)

# Example usage
def demonstrate() -> None:
    """Demonstrate the IO monad."""
    print("=== IO Monad ===\n")
    
    # 1. Basic usage
    print("1. Basic usage:")
    
    # Create an IO action that prints a message
    greet = IO.print_line("Hello, IO monad!")
    
    # Create an IO action that gets the current time
    get_time = IO.get_current_time()
    
    # Chain operations
    program = (
        greet
        .bind(lambda _: get_time)
        .bind(lambda t: IO.print_line(f"Current time: {t}"))
    )
    
    # Run the program
    print("Running IO program:")
    program.unsafe_run()
    
    # 2. File operations
    print("\n2. File operations:")
    
    # Create a file with some content
    file_path = "test_io_monad.txt"
    
    file_program = (
        IO.print_line(f"Creating file: {file_path}")
        .bind(lambda _: IO.write_file(file_path, "Hello, IO monad!\n"))
        .bind(lambda _: IO.print_line("File written successfully"))
        .bind(lambda _: IO.file_exists(file_path))
        .bind(lambda exists: (
            IO.print_line(f"File exists: {exists}")
            .bind(lambda _: IO.read_file(file_path) if exists else IO.unit(""))
        ))
        .bind(lambda content: IO.print_line(f"File content: {content!r}"))
    )
    
    print("Running file operations:")
    file_program.unsafe_run()
    
    # 3. Interactive program
    print("\n3. Interactive program:")
    
    def ask_question(question: str) -> IO[str]:
        """Ask a question and return the user's response."""
        return (
            IO.print_line(question)
            .bind(lambda _: IO.read_line())
            .map(lambda s: s.strip())
        )
    
    interactive = (
        ask_question("What is your name? ")
        .bind(lambda name: (
            ask_question(f"Hello, {name}! How old are you? ")
            .bind(lambda age_str: (
                IO.unit(int(age_str)) if age_str.isdigit() 
                else IO.print_line("Invalid age. Using 0.").bind(lambda _: IO.unit(0))
            ))
            .bind(lambda age: (
                IO.get_current_time()
                .bind(lambda current_time: (
                    IO.print_line(
                        f"Hello {name}, you are {age} years old. "
                        f"Current Unix time: {current_time}"
                    )
                ))
            ))
        ))
    )
    
    # Uncomment to run the interactive program
    # print("Running interactive program:")
    # interactive.unsafe_run()
    
    # 4. Error handling
    print("\n4. Error handling:")
    
    def safe_divide(x: float, y: float) -> IO[float]:
        """Safely divide two numbers, handling division by zero."""
        if y == 0:
            return IO.print_line("Error: Division by zero").bind(
                lambda _: IO.unit(float('inf'))
            )
        return IO.unit(x / y)
    
    division = (
        safe_divide(10, 2)
        .bind(lambda result: IO.print_line(f"10 / 2 = {result}"))
        .bind(lambda _: safe_divide(5, 0))
        .bind(lambda result: IO.print_line(f"5 / 0 = {result}"))
    )
    
    division.unsafe_run()
    
    # 5. Looping and control flow
    print("\n5. Looping and control flow:")
    
    def countdown(n: int) -> IO[None]:
        """Count down from n to 1 with a delay."""
        if n <= 0:
            return IO.unit(None)
        return (
            IO.print_line(f"{n}...")
            .bind(lambda _: IO.sleep(0.5))
            .bind(lambda _: countdown(n - 1))
        )
    
    print("Starting countdown:")
    countdown(3).unsafe_run()
    
    # 6. Environment variables
    print("\n6. Environment variables:")
    
    env_program = (
        IO.get_environment_variable("USER")
        .bind(lambda user: (
            IO.print_line(f"Current user: {user}")
            if user is not None
            else IO.print_line("USER environment variable not set")
        ))
    )
    
    env_program.unsafe_run()
    
    # 7. Sequence and traverse
    print("\n7. Sequence and traverse:")
    
    # Sequence a list of IO actions
    actions = [
        IO.print_line("Action 1"),
        IO.print_line("Action 2"),
        IO.print_line("Action 3")
    ]
    
    sequence_program = IO.sequence(actions).bind(
        lambda _: IO.print_line("All actions completed")
    )
    
    print("Running sequence of actions:")
    sequence_program.unsafe_run()
    
    # Traverse a list with a function that returns IO
    numbers = [1, 2, 3, 4, 5]
    
    def process_number(n: int) -> IO[None]:
        return IO.print_line(f"Processing number: {n}")
    
    traverse_program = IO.traverse(numbers, process_number)
    
    print("\nTraversing list:")
    traverse_program.unsafe_run()

if __name__ == "__main__":
    demonstrate()
