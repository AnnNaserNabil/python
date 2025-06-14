"""
5. Practical Examples of Partial Application

This module demonstrates real-world use cases of partial application,
including configuration, event handling, and API wrappers.
"""
from functools import partial
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast
from dataclasses import dataclass
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

T = TypeVar('T')

# Example 1: Configuration Management
class ConfigManager:
    """A configuration manager that uses partial application for configuration."""
    
    def __init__(self, defaults: Dict[str, Any]):
        self.defaults = defaults
        self.overrides: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with a fallback."""
        return self.overrides.get(key, self.defaults.get(key, default))
    
    def configure(self, **kwargs: Any) -> 'ConfigManager':
        """Update configuration values."""
        self.overrides.update(kwargs)
        return self
    
    def get_configured(self, **defaults: Any) -> Callable[[str], Any]:
        """Create a getter with default values."""
        def getter(key: str) -> Any:
            return self.get(key, defaults.get(key, None))
        return getter

def demonstrate_config() -> None:
    """Demonstrate configuration management with partial application."""
    print("=== Configuration Management ===\n")
    
    # Create a config manager with defaults
    config = ConfigManager({
        "api_url": "https://api.example.com",
        "timeout": 30,
        "retries": 3,
        "debug": False
    })
    
    # Create specialized getters
    get_api_setting = partial(config.get, default={})
    get_network_setting = config.get_configured(timeout=60, retries=5)
    
    # Use the getters
    print(f"API URL: {get_api_setting('api_url')}")
    print(f"Timeout: {get_network_setting('timeout')} seconds")
    print(f"Retries: {get_network_setting('retries')}")
    print(f"Debug mode: {get_network_setting('debug')}")
    
    # Update configuration
    config.configure(debug=True, timeout=10)
    
    print("\nAfter configuration update:")
    print(f"Timeout: {get_network_setting('timeout')} seconds")
    print(f"Debug mode: {get_network_setting('debug')}")

# Example 2: API Client
class APIClient:
    """A flexible API client using partial application for common parameters."""
    
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        json_data: Any = None
    ) -> Dict[str, Any]:
        """Make an HTTP request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Prepare headers
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)
        
        # Prepare query parameters
        if params:
            query_string = urllib.parse.urlencode(params, doseq=True)
            url = f"{url}?{query_string}"
        
        # Prepare request data
        req_data = None
        if data:
            req_data = data.encode('utf-8') if isinstance(data, str) else data
        elif json_data is not None:
            req_data = json.dumps(json_data).encode('utf-8')
            request_headers.setdefault('Content-Type', 'application/json')
        
        # Create and send request
        req = urllib.request.Request(
            url,
            data=req_data,
            headers=request_headers,
            method=method.upper()
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                return {
                    'status': response.status,
                    'headers': dict(response.headers),
                    'data': json.loads(response_data) if response_data else None
                }
        except urllib.error.HTTPError as e:
            return {
                'status': e.code,
                'headers': dict(e.headers),
                'error': str(e)
            }
    
    # Create partial methods for common HTTP methods
    get = partial(_request, method='GET')
    post = partial(_request, method='POST')
    put = partial(_request, method='PUT')
    delete = partial(_request, method='DELETE')
    patch = partial(_request, method='PATCH')

def demonstrate_api_client() -> None:
    """Demonstrate API client usage with partial application."""
    print("\n=== API Client ===\n")
    
    # Create an API client
    client = APIClient(
        base_url="https://jsonplaceholder.typicode.com",
        default_headers={
            'User-Agent': 'MyAPIClient/1.0',
            'Accept': 'application/json'
        }
    )
    
    # Create specialized API methods
    get_posts = client.get
    get_post = partial(client.get, endpoint="posts/{id}")
    create_post = partial(
        client.post,
        endpoint="posts",
        headers={'Content-Type': 'application/json'}
    )
    
    # Use the API
    print("Fetching all posts...")
    posts = get_posts(endpoint="posts")
    print(f"Found {len(posts['data'])} posts (status: {posts['status']})")
    
    print("\nFetching post #1...")
    post = get_post(endpoint=("posts/1"))
    print(f"Post #1: {post['data']['title']}" if post['status'] == 200 else "Error fetching post")
    
    # Note: The following is a mock since jsonplaceholder doesn't actually save data
    print("\nCreating a new post...")
    new_post = {
        'title': 'My New Post',
        'body': 'This is the content of my new post.',
        'userId': 1
    }
    result = create_post(json_data=new_post)
    print(f"Created post with ID: {result['data']['id'] if 'data' in result else 'error'}")

# Example 3: Event Handling
class EventEmitter:
    """A simple event emitter that supports partial application for event handlers."""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable[..., None]]] = {}
    
    def on(self, event: str, handler: Callable[..., None]) -> Callable[[], None]:
        """Register an event handler and return an unregister function."""
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)
        
        # Return a function to unregister this handler
        def unregister() -> None:
            if event in self._handlers and handler in self._handlers[event]:
                self._handlers[event].remove(handler)
        
        return unregister
    
    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Emit an event with the given arguments."""
        for handler in self._handlers.get(event, []):
            handler(*args, **kwargs)
    
    def create_handler(self, event: str, *args: Any, **kwargs: Any) -> Callable[..., None]:
        """Create a pre-configured event handler."""
        def handler(*more_args: Any, **more_kwargs: Any) -> None:
            all_args = args + more_args
            all_kwargs = {**kwargs, **more_kwargs}
            self.emit(event, *all_args, **all_kwargs)
        return handler

def demonstrate_event_handling() -> None:
    """Demonstrate event handling with partial application."""
    print("\n=== Event Handling ===\n")
    
    emitter = EventEmitter()
    
    # Create some event handlers
    def log_event(event: str, *args: Any, **kwargs: Any) -> None:
        print(f"\n[{datetime.now().isoformat()}] Event: {event}")
        if args:
            print(f"  Args: {args}")
        if kwargs:
            print(f"  Kwargs: {kwargs}")
    
    def send_notification(recipient: str, message: str, priority: str = "normal") -> None:
        print(f"\nSending {priority} notification to {recipient}:")
        print(f"  {message}")
    
    # Register handlers
    emitter.on("*", log_event)  # Log all events
    
    # Create specialized notification handlers
    notify_admin = partial(
        send_notification,
        recipient="admin@example.com",
        priority="high"
    )
    
    # Register the specialized handler
    emitter.on("error", notify_admin)
    
    # Create a handler with some arguments pre-filled
    user_notification = emitter.create_handler(
        "user_notification",
        recipient="user@example.com"
    )
    
    # Emit some events
    print("Emitting events...")
    emitter.emit("user_login", user_id=123, ip="192.168.1.1")
    
    # Use the pre-configured handler
    user_notification(
        message="Your account has been updated.",
        priority="info"
    )
    
    # Emit an error
    try:
        1 / 0
    except Exception as e:
        emitter.emit(
            "error",
            message="Division by zero error",
            exception=str(e),
            timestamp=datetime.now().isoformat()
        )

# Example 4: Retry Mechanism
def retry(
    func: Callable[..., T],
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None
) -> Callable[..., T]:
    """A retry decorator with configurable parameters."""
    import time
    
    def wrapper(*args: Any, **kwargs: Any) -> T:
        last_exception = None
        for attempt in range(1, max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                last_exception = e
                if on_retry:
                    on_retry(attempt, e)
                if attempt < max_attempts:
                    time.sleep(delay * attempt)  # Exponential backoff
        raise last_exception  # type: ignore
    
    return wrapper

def demonstrate_retry() -> None:
    """Demonstrate the retry mechanism."""
    print("\n=== Retry Mechanism ===\n")
    
    # A flaky function that fails a few times before succeeding
    attempt_count = 0
    
    def flaky_operation() -> str:
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ConnectionError(f"Connection failed (attempt {attempt_count})")
        return "Operation succeeded!"
    
    # Create a retry configuration
    retry_config = partial(
        retry,
        max_attempts=5,
        delay=0.5,
        exceptions=(ConnectionError,),
        on_retry=lambda attempt, e: print(f"  Attempt {attempt} failed: {e}")
    )
    
    # Apply the retry configuration to our flaky function
    reliable_operation = retry_config(flaky_operation)
    
    print("Running a flaky operation with retry...")
    try:
        result = reliable_operation()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Operation failed after retries: {e}")
    
    print(f"Total attempts made: {attempt_count}")

def main() -> None:
    """Run all demonstrations."""
    demonstrate_config()
    demonstrate_api_client()
    demonstrate_event_handling()
    demonstrate_retry()
    
    print("\n=== All examples completed successfully ===")

if __name__ == "__main__":
    main()
