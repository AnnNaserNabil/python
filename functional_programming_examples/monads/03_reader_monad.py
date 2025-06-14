"""
3. The Reader Monad

The Reader monad represents a computation that can read values from a shared
environment, pass values from function to function, and execute within a context.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, Generic, TypeVar, cast, overload
from dataclasses import dataclass

E = TypeVar('E')  # Environment type
A = TypeVar('A')  # Result type
B = TypeVar('B')

class Reader(Generic[E, A]):
    """The Reader monad."""
    
    def __init__(self, run: Callable[[E], A]):
        self._run = run
    
    def run(self, env: E) -> A:
        """Run the reader with the given environment."""
        return self._run(env)
    
    def map(self, f: Callable[[A], B]) -> Reader[E, B]:
        """Map a function over the result of the reader."""
        return Reader(lambda e: f(self.run(e)))
    
    def bind(self, f: Callable[[A], Reader[E, B]]) -> Reader[E, B]:
        """Chain operations that can read from the environment."""
        return Reader(lambda e: f(self.run(e)).run(e))
    
    @classmethod
    def ask(cls) -> Reader[E, E]:
        """Get the environment."""
        return Reader(lambda e: e)
    
    @classmethod
    def asks(cls, f: Callable[[E], A]) -> Reader[E, A]:
        """Get a value from the environment using the given function."""
        return Reader(f)
    
    def local(self, f: Callable[[E], E]) -> Reader[E, A]:
        """Run the reader with a modified environment."""
        return Reader(lambda e: self.run(f(e)))
    
    def __or__(self, f: Callable[[A], Reader[E, B]]) -> Reader[E, B]:
        """Override | operator for bind."""
        return self.bind(f)
    
    def __rshift__(self, f: Callable[[A], Reader[E, B]]) -> Reader[E, B]:
        """Override >> operator for chaining."""
        return self.bind(f)
    
    def __call__(self, env: E) -> A:
        """Make the reader callable with the environment."""
        return self.run(env)

# Example usage
def demonstrate() -> None:
    """Demonstrate the Reader monad."""
    print("=== Reader Monad ===\n")
    
    # 1. Basic usage
    print("1. Basic usage:")
    
    # A reader that gets a value from the environment and adds 1
    add_one = Reader(lambda env: env['value'] + 1)
    
    # Run the reader with an environment
    result = add_one.run({'value': 41})
    print(f"add_one with value=41: {result}")
    
    # 2. Chaining operations
    print("\n2. Chaining operations:")
    
    # Multiple operations that depend on the environment
    computation = (
        Reader.ask()
        .bind(lambda env: Reader(lambda _: env['x'] + env['y']))
        .bind(lambda s: Reader(lambda _: s * 2))
    )
    
    env = {'x': 10, 'y': 20}
    print(f"(x + y) * 2 where x=10, y=20: {computation.run(env)}")
    
    # 3. Using map
    print("\n3. Using map:")
    
    # Map over the result
    computation = Reader(lambda env: env['name']).map(str.upper)
    print(f"Uppercase name: {computation.run({'name': 'alice'})}")
    
    # 4. Using asks
    print("\n4. Using asks:")
    
    # Get a specific value from the environment
    get_age = Reader.asks(lambda env: env['age'])
    print(f"Age: {get_age.run({'age': 30, 'name': 'Bob'})}")
    
    # 5. Local modifications
    print("\n5. Local modifications:")
    
    # Original reader
    get_name = Reader.asks(lambda env: env['user']['name'])
    
    # Modify the environment for a sub-computation
    nested_env = {
        'user': {
            'name': 'Alice',
            'email': 'alice@example.com'
        },
        'settings': {}
    }
    
    # Get the name from a modified environment
    get_modified = get_name.local(lambda env: {
        **env,
        'user': {**env['user'], 'name': 'Modified ' + env['user']['name']}
    })
    
    print(f"Original name: {get_name.run(nested_env)}")
    print(f"Modified name: {get_modified.run(nested_env)}")
    
    # 6. Complex example: Configuration
    print("\n6. Complex example: Configuration:")
    
    # Define our configuration
    config = {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'myapp_db',
            'user': 'admin'
        },
        'server': {
            'port': 3000,
            'environment': 'development',
            'debug': True
        },
        'features': {
            'caching': True,
            'analytics': False
        }
    }
    
    # Helper functions to access nested config
    def get_database_config() -> Reader[dict, dict]:
        return Reader.asks(lambda cfg: cfg['database'])
    
    def get_server_config() -> Reader[dict, dict]:
        return Reader.asks(lambda cfg: cfg['server'])
    
    def get_feature_flag(name: str) -> Reader[dict, bool]:
        return Reader.asks(lambda cfg: cfg['features'].get(name, False))
    
    # A more complex computation using the config
    def get_database_connection_string() -> Reader[dict, str]:
        return (
            get_database_config()
            .bind(lambda db: Reader.unit(
                f"postgresql://{db['user']}@{db['host']}:{db['port']}/{db['name']}"
            ))
        )
    
    def get_server_info() -> Reader[dict, str]:
        return (
            get_server_config()
            .bind(lambda srv: get_database_connection_string()
                .bind(lambda conn: get_feature_flag('caching')
                    .map(lambda use_cache: (
                        f"Server running on port {srv['port']} in {srv['environment']} mode\n"
                        f"Database: {conn}\n"
                        f"Caching: {'enabled' if use_cache else 'disabled'}"
                    ))
                )
            )
        )
    
    # Run the computation
    server_info = get_server_info().run(config)
    print("Server information:")
    print(server_info)
    
    # 7. Composition of readers
    print("\n7. Composition of readers:")
    
    def add(x: int, y: int) -> Reader[dict, int]:
        return Reader.asks(lambda _: x + y)
    
    def multiply(x: int, y: int) -> Reader[dict, int]:
        return Reader.asks(lambda _: x * y)
    
    # Compose operations
    computation = (
        add(2, 3)  # 5
        .bind(lambda a: multiply(a, 4))  # 20
        .bind(lambda b: add(b, 1))  # 21
    )
    
    print(f"(2 + 3) * 4 + 1 = {computation.run({})}")

# Helper for creating a reader with a constant value
@overload
def reader_unit(a: A) -> Reader[Any, A]:
    ...

@overload
def reader_unit(e: type[E], a: A) -> Reader[E, A]:
    ...

def reader_unit(*args):
    if len(args) == 1:
        return Reader(lambda _: args[0])
    return Reader(lambda _: args[1])

# Add unit method to Reader class
Reader.unit = classmethod(lambda cls, a: reader_unit(a))  # type: ignore

if __name__ == "__main__":
    demonstrate()
