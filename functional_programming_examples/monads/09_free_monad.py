"""
9. The Free Monad

The Free monad provides a way to build domain-specific languages (DSLs) and
interpret them in different ways. It separates the representation of the computation
from its interpretation.
"""
from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar, Union, cast
from dataclasses import dataclass
from functools import partial

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
F = TypeVar('F')  # Functor type

class Functor(Generic[F, A]):
    """Type class for functors."""
    
    def fmap(self, f: Callable[[A], B]) -> Functor[F, B]:
        """Map a function over the functor."""
        raise NotImplementedError

class Free(Generic[F, A]):
    """The Free monad."""
    
    @classmethod
    def pure(cls, a: A) -> Free[F, A]:
        """Lift a value into the Free monad."""
        return Pure(a)
    
    def flat_map(self, f: Callable[[A], Free[F, B]]) -> Free[F, B]:
        """Chain computations in the Free monad."""
        if isinstance(self, Pure):
            return f(self.value)
        elif isinstance(self, Impure):
            return Impure(self.fa.fmap(lambda x: x.flat_map(f)))
        else:
            raise ValueError(f"Unknown Free type: {type(self)}")
    
    def map(self, f: Callable[[A], B]) -> Free[F, B]:
        """Map a function over the result of the computation."""
        return self.flat_map(lambda x: Free.pure(f(x)))
    
    def fold(self, pure: Callable[[A], B], impure: Callable[[Any], B]) -> B:
        """Fold over the Free structure."""
        if isinstance(self, Pure):
            return pure(self.value)
        elif isinstance(self, Impure):
            return impure(self.fa)
        else:
            raise ValueError(f"Unknown Free type: {type(self)}")
    
    def fold_map(self, f: Callable[[Any], Any], m: Any) -> Any:
        """Fold over the Free structure using a monad."""
        if isinstance(self, Pure):
            return m.pure(self.value)
        elif isinstance(self, Impure):
            # This is a simplification; in practice, you'd need to handle the functor
            # and monad instances properly
            return f(self.fa).flat_map(
                lambda x: x.fold_map(f, m)
            )
        else:
            raise ValueError(f"Unknown Free type: {type(self)}")
    
    def interpret(self, interpreter: Callable[[Any], Any]) -> Any:
        """Interpret the Free monad using a natural transformation."""
        if isinstance(self, Pure):
            return self.value
        elif isinstance(self, Impure):
            return self.fa.fmap(
                lambda x: x.interpret(interpreter)
            )
        else:
            raise ValueError(f"Unknown Free type: {type(self)}")
    
    def __or__(self, f: Callable[[A], Free[F, B]]) -> Free[F, B]:
        """Override | operator for flat_map."""
        return self.flat_map(f)
    
    def __rshift__(self, f: Callable[[A], Free[F, B]]) -> Free[F, B]:
        """Override >> operator for chaining."""
        return self.flat_map(f)

@dataclass
class Pure(Free[F, A]):
    """A pure computation that just returns a value."""
    value: A

@dataclass
class Impure(Free[F, A]):
    """An impure computation that produces a value wrapped in a functor."""
    fa: Any  # Should be a functor F[Free[F, A]]

# Example usage
def demonstrate() -> None:
    """Demonstrate the Free monad."""
    print("=== Free Monad ===\n")
    
    # 1. Basic usage with a simple DSL
    print("1. Basic usage with a simple DSL:")
    
    # Define a simple DSL for key-value storage
    class KVStore(Generic[A]):
        pass
    
    @dataclass
    class Get(Generic[A], KVStore[A]):
        key: str
        k: Callable[[Any], A]
        
        def fmap(self, f):
            return Get(self.key, lambda x: f(self.k(x)))
    
    @dataclass
    class Put(Generic[A], KVStore[A]):
        key: str
        value: Any
        k: Callable[[None], A]
        
        def fmap(self, f):
            return Put(self.key, self.value, lambda x: f(self.k(x)))
    
    @dataclass
    class Delete(Generic[A], KVStore[A]):
        key: str
        k: Callable[[None], A]
        
        def fmap(self, f):
            return Delete(self.key, lambda x: f(self.k(x)))
    
    # Smart constructors
    def get(key: str) -> Free[KVStore, Any]:
        return Impure(Get(key, lambda x: Pure(x)))
    
    def put(key: str, value: Any) -> Free[KVStore, None]:
        return Impure(Put(key, value, lambda: Pure(None)))
    
    def delete(key: str) -> Free[KVStore, None]:
        return Impure(Delete(key, lambda: Pure(None)))
    
    # Example program
    def program() -> Free[KVStore, str]:
        return (
            put("name", "Alice")
            .flat_map(lambda _: get("name"))
            .flat_map(lambda name: (
                put("greeting", f"Hello, {name}!")
                .flat_map(lambda _: get("greeting"))
            ))
        )
    
    # Interpreters
    def interpret_kv_store(program: Free[KVStore, Any], state: dict = None) -> Any:
        if state is None:
            state = {}
            
        if isinstance(program, Pure):
            return program.value
        elif isinstance(program, Impure):
            fa = program.fa
            
            if isinstance(fa, Get):
                value = state.get(fa.key)
                return interpret_kv_store(fa.k(value), state)
                
            elif isinstance(fa, Put):
                state[fa.key] = fa.value
                return interpret_kv_store(fa.k(None), state)
                
            elif isinstance(fa, Delete):
                if fa.key in state:
                    del state[fa.key]
                return interpret_kv_store(fa.k(None), state)
                
            else:
                raise ValueError(f"Unknown KVStore operation: {fa}")
        else:
            raise ValueError(f"Unknown Free type: {type(program)}")
    
    # Run the program
    print("Running KV store program:")
    result = interpret_kv_store(program())
    print(f"Result: {result}")
    
    # 2. File system DSL
    print("\n2. File system DSL:")
    
    class FileSystem(Generic[A]):
        pass
    
    @dataclass
    class ReadFile(Generic[A], FileSystem[A]):
        path: str
        k: Callable[[str], A]
        
        def fmap(self, f):
            return ReadFile(self.path, lambda x: f(self.k(x)))
    
    @dataclass
    class WriteFile(Generic[A], FileSystem[A]):
        path: str
        content: str
        k: Callable[[None], A]
        
        def fmap(self, f):
            return WriteFile(self.path, self.content, lambda x: f(self.k(x)))
    
    @dataclass
    class ListDir(Generic[A], FileSystem[A]):
        path: str
        k: Callable[[list[str]], A]
        
        def fmap(self, f):
            return ListDir(self.path, lambda x: f(self.k(x)))
    
    # Smart constructors
    def read_file(path: str) -> Free[FileSystem, str]:
        return Impure(ReadFile(path, lambda x: Pure(x)))
    
    def write_file(path: str, content: str) -> Free[FileSystem, None]:
        return Impure(WriteFile(path, content, lambda: Pure(None)))
    
    def list_dir(path: str) -> Free[FileSystem, list[str]]:
        return Impure(ListDir(path, lambda x: Pure(x)))
    
    # Example program
    def file_operation() -> Free[FileSystem, str]:
        return (
            write_file("test.txt", "Hello, Free Monad!")
            .flat_map(lambda _: read_file("test.txt"))
            .flat_map(lambda content: (
                write_file("test_copy.txt", content.upper())
                .flat_map(lambda _: read_file("test_copy.txt"))
            ))
        )
    
    # Mock interpreter for demonstration
    def interpret_file_system(program: Free[FileSystem, Any], fs: dict = None) -> Any:
        if fs is None:
            fs = {}
            
        if isinstance(program, Pure):
            return program.value
        elif isinstance(program, Impure):
            fa = program.fa
            
            if isinstance(fa, ReadFile):
                content = fs.get(fa.path, "")
                return interpret_file_system(fa.k(content), fs)
                
            elif isinstance(fa, WriteFile):
                fs[fa.path] = fa.content
                return interpret_file_system(fa.k(None), fs)
                
            elif isinstance(fa, ListDir):
                # Simple implementation: return keys that start with the path
                files = [k for k in fs.keys() if k.startswith(fa.path)]
                return interpret_file_system(fa.k(files), fs)
                
            else:
                raise ValueError(f"Unknown FileSystem operation: {fa}")
        else:
            raise ValueError(f"Unknown Free type: {type(program)}")
    
    # Run the program
    print("Running file system program:")
    result = interpret_file_system(file_operation())
    print(f"Result: {result}")
    
    # 3. Combining multiple DSLs with coproducts
    print("\n3. Combining multiple DSLs:")
    
    # We'll combine the KVStore and FileSystem DSLs
    class Combined(Generic[A]):
        pass
    
    # Injections for KVStore
    @dataclass
    class KVStoreI(Generic[A], Combined[A]):
        kv: Any  # KVStore[A]
        
        def fmap(self, f):
            return KVStoreI(self.kv.fmap(f))
    
    # Injections for FileSystem
    @dataclass
    class FileSystemI(Generic[A], Combined[A]):
        fs: Any  # FileSystem[A]
        
        def fmap(self, f):
            return FileSystemI(self.fs.fmap(f))
    
    # Smart constructors for the combined DSL
    def lift_kv(kv: KVStore[A]) -> Free[Combined, A]:
        return Impure(KVStoreI(kv))
    
    def lift_fs(fs: FileSystem[A]) -> Free[Combined, A]:
        return Impure(FileSystemI(fs))
    
    # Combined program
    def combined_program() -> Free[Combined, str]:
        return (
            lift_kv(Put("config_file", "config.txt", lambda: Pure(None))))
            .flat_map(lambda _: lift_kv(Get("config_file", lambda path: Pure(path))))
            .flat_map(lambda path: 
                lift_fs(ReadFile(path, lambda content: Pure(content))))
            .flat_map(lambda content: 
                lift_kv(Put("config_content", content, lambda: Pure(None))))
            .flat_map(lambda _: lift_kv(Get("config_content", lambda content: Pure(content.upper()))))
        )
    
    # Combined interpreter
    def interpret_combined(program: Free[Combined, Any], state: dict = None, fs: dict = None) -> Any:
        if state is None:
            state = {}
        if fs is None:
            fs = {}
            
        if isinstance(program, Pure):
            return program.value
        elif isinstance(program, Impure):
            fa = program.fa
            
            if isinstance(fa, KVStoreI):
                # Delegate to KVStore interpreter
                kv = fa.kv
                
                if isinstance(kv, Get):
                    value = state.get(kv.key)
                    return interpret_combined(kv.k(value), state, fs)
                    
                elif isinstance(kv, Put):
                    state[kv.key] = kv.value
                    return interpret_combined(kv.k(None), state, fs)
                    
                elif isinstance(kv, Delete):
                    if kv.key in state:
                        del state[kv.key]
                    return interpret_combined(kv.k(None), state, fs)
                    
                else:
                    raise ValueError(f"Unknown KVStore operation: {kv}")
                    
            elif isinstance(fa, FileSystemI):
                # Delegate to FileSystem interpreter
                fs_op = fa.fs
                
                if isinstance(fs_op, ReadFile):
                    content = fs.get(fs_op.path, "")
                    return interpret_combined(fs_op.k(content), state, fs)
                    
                elif isinstance(fs_op, WriteFile):
                    fs[fs_op.path] = fs_op.content
                    return interpret_combined(fs_op.k(None), state, fs)
                    
                elif isinstance(fs_op, ListDir):
                    files = [k for k in fs.keys() if k.startswith(fs_op.path)]
                    return interpret_combined(fs_op.k(files), state, fs)
                    
                else:
                    raise ValueError(f"Unknown FileSystem operation: {fs_op}")
                    
            else:
                raise ValueError(f"Unknown Combined operation: {fa}")
        else:
            raise ValueError(f"Unknown Free type: {type(program)}")
    
    # Run the combined program
    print("Running combined program:")
    
    # Set up initial file system state
    fs_state = {
        "config.txt": "key1=value1\nkey2=value2"
    }
    
    result = interpret_combined(combined_program(), fs=fs_state)
    print(f"Result: {result}")

if __name__ == "__main__":
    demonstrate()
