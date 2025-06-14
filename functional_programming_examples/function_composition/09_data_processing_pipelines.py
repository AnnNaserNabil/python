"""
9. Real-World Data Processing Pipelines

Demonstrates how to build and compose data processing pipelines
for real-world scenarios like ETL, data cleaning, and analysis.
"""
from __future__ import annotations
from typing import (
    TypeVar, Callable, Any, Dict, List, Tuple, Iterator, Iterable, 
    Optional, Union, cast
)
from functools import partial, reduce
from dataclasses import dataclass, field
from datetime import datetime
import csv
import json
import re
from pathlib import Path
import gzip
import io
from collections import defaultdict, Counter

# Type variables for generic functions
T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# 1. Pipeline Components

class Pipeline(Generic[T, U]):
    """A pipeline that processes data through a series of steps."""
    
    def __init__(self, *steps: Callable[..., Any]):
        self.steps = steps
    
    def __call__(self, data: T) -> U:
        """Process data through the pipeline."""
        return reduce(lambda d, step: step(d), self.steps, data)
    
    def then(self, step: Callable[[U], V]) -> 'Pipeline[T, V]':
        """Add a step to the pipeline."""
        return Pipeline(*self.steps, step)
    
    def __or__(self, step: Callable[[U], V]) -> 'Pipeline[T, V]':
        """Pipe operator for chaining steps."""
        return self.then(step)
    
    @classmethod
    def of(cls, *steps: Callable[..., Any]) -> 'Pipeline[Any, Any]':
        """Create a new pipeline with the given steps."""
        return cls(*steps)

# 2. Data Processing Functions

def read_lines(file_path: str) -> Iterator[str]:
    """Read lines from a file, handling both regular and gzipped files."""
    path = Path(file_path)
    
    if path.suffix == '.gz':
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            yield from f
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            yield from f

def write_lines(file_path: str, lines: Iterable[str]) -> None:
    """Write lines to a file, handling gzipped output."""
    path = Path(file_path)
    
    if path.suffix == '.gz':
        with gzip.open(file_path, 'wt', encoding='utf-8') as f:
            f.writelines(lines)
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

def parse_json() -> Callable[[str], Dict[str, Any]]:
    """Create a JSON parser that handles malformed JSON."""
    def parser(line: str) -> Dict[str, Any]:
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON: {line[:100]}...")
            return {}
    return parser

def to_json(ensure_ascii: bool = False, indent: Optional[int] = None) -> Callable[[Any], str]:
    """Create a JSON serializer."""
    return lambda x: json.dumps(x, ensure_ascii=ensure_ascii, indent=indent) + '\n'

def parse_csv(
    fieldnames: Optional[List[str]] = None,
    delimiter: str = ',',
    **fmtparams: Any
) -> Callable[[str], Dict[str, str]]:
    """Create a CSV parser."""
    def parser(line: str) -> Dict[str, str]:
        reader = csv.DictReader(
            [line], 
            fieldnames=fieldnames,
            delimiter=delimiter,
            **fmtparams
        )
        return next(reader, {})
    return parser

def to_csv(
    fieldnames: Optional[List[str]] = None,
    delimiter: str = ',',
    **fmtparams: Any
) -> Callable[[Dict[str, Any]], str]:
    """Create a CSV serializer."""
    def to_str(d: Dict[str, Any]) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(
            output, 
            fieldnames=fieldnames or list(d.keys()),
            delimiter=delimiter,
            **fmtparams
        )
        if fieldnames is None:
            writer.writeheader()
        writer.writerow(d)
        return output.getvalue().strip()
    return to_str

# 3. Data Transformation Functions

def map_field(
    field: str, 
    func: Callable[[Any], Any], 
    default: Any = None
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Apply a function to a specific field in a dictionary."""
    def transform(record: Dict[str, Any]) -> Dict[str, Any]:
        if field in record:
            try:
                record[field] = func(record[field])
            except (TypeError, ValueError) as e:
                if default is not None:
                    record[field] = default
                else:
                    print(f"Warning: {e} for field '{field}' in record {record}")
        return record
    return transform

def filter_records(
    predicate: Callable[[Dict[str, Any]], bool]
) -> Callable[[Iterator[Dict[str, Any]]], Iterator[Dict[str, Any]]]:
    """Filter records based on a predicate."""
    return lambda records: filter(predicate, records)

def add_field(
    field: str, 
    value: Union[Any, Callable[[Dict[str, Any]], Any]]
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """Add a field to each record."""
    def transform(record: Dict[str, Any]) -> Dict[str, Any]:
        record[field] = value(record) if callable(value) else value
        return record
    return transform

# 4. Data Analysis Functions

def group_by(
    key: Union[str, Callable[[Dict[str, Any]], Any]]
) -> Callable[[Iterable[Dict[str, Any]]], Dict[Any, List[Dict[str, Any]]]]:
    """Group records by a key or key function."""
    def grouper(records: Iterable[Dict[str, Any]]) -> Dict[Any, List[Dict[str, Any]]]:
        groups: Dict[Any, List[Dict[str, Any]]] = defaultdict(list)
        
        if isinstance(key, str):
            key_func = lambda r: r.get(key)
        else:
            key_func = key
        
        for record in records:
            groups[key_func(record)].append(record)
            
        return dict(groups)
    return grouper

def aggregate(
    group_key: Union[str, Callable[[Dict[str, Any]], Any]],
    **aggregations: Dict[str, Tuple[str, Callable[[List[Any]], Any]]]
) -> Callable[[Iterable[Dict[str, Any]]], List[Dict[str, Any]]]:
    """Aggregate data by a key with multiple aggregation functions."""
    def aggregator(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Group records
        grouped = group_by(group_key)(list(records))
        
        results = []
        for key, group in grouped.items():
            result = {'group': key}
            
            # Apply each aggregation
            for field, (source_field, agg_func) in aggregations.items():
                values = [r.get(source_field) for r in group 
                         if source_field in r and r[source_field] is not None]
                if values:
                    result[field] = agg_func(values)
            
            results.append(result)
            
        return results
    return aggregator

# 5. Example Pipelines

def process_web_logs() -> None:
    """Process web server logs and generate statistics."""
    print("=== Web Log Processing Pipeline ===")
    
    # Parse a common log format line
    # Example: 127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/data HTTP/1.1" 200 1234
    log_pattern = re.compile(
        r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)'
    )
    
    def parse_log_line(line: str) -> Dict[str, Any]:
        match = log_pattern.match(line.strip())
        if not match:
            return {}
            
        ip, timestamp, method, path, protocol, status_code, size = match.groups()
        
        # Parse timestamp
        try:
            dt = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z')
            date_str = dt.strftime('%Y-%m-%d')
            hour = dt.hour
        except ValueError:
            date_str = 'unknown'
            hour = -1
        
        return {
            'ip': ip,
            'timestamp': timestamp,
            'date': date_str,
            'hour': hour,
            'method': method,
            'path': path,
            'protocol': protocol.split('/')[0],
            'status': int(status_code),
            'size': int(size) if size != '-' else 0
        }
    
    # Define the pipeline
    pipeline = Pipeline.of(
        # Read and parse logs
        read_lines,
        map(parse_log_line),
        filter(lambda x: x),  # Remove empty/None records
        
        # Add some derived fields
        add_field('is_api', lambda r: r['path'].startswith('/api/')),
        add_field('is_success', lambda r: 200 <= r['status'] < 300),
        
        # Convert to list for multiple passes
        list,
        
        # Calculate statistics
        lambda records: {
            'total_requests': len(records),
            'total_bytes': sum(r['size'] for r in records),
            'success_rate': sum(1 for r in records if r['is_success']) / len(records) * 100,
            'api_requests': sum(1 for r in records if r['is_api']),
            'by_status': dict(Counter(r['status'] for r in records)),
            'by_hour': dict(Counter(r['hour'] for r in records)),
            'top_ips': dict(Counter(r['ip'] for r in records).most_common(10)),
            'top_paths': dict(Counter(r['path'] for r in records).most_common(10))
        },
        
        # Convert to pretty-printed JSON
        lambda x: json.dumps(x, indent=2)
    )
    
    # Process a sample log file (in a real scenario, this would be your log file)
    sample_logs = """
    127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/data HTTP/1.1" 200 1234
    192.168.1.1 - - [10/Oct/2023:13:55:37 +0000] "GET /index.html HTTP/1.1" 200 5678
    10.0.0.1 - - [10/Oct/2023:13:55:38 +0000] "POST /api/submit HTTP/1.1" 201 42
    127.0.0.1 - - [10/Oct/2023:13:56:01 +0000] "GET /api/data?page=2 HTTP/1.1" 200 2345
    192.168.1.1 - - [10/Oct/2023:13:56:02 +0000] "GET /images/logo.png HTTP/1.1" 200 9876
    10.0.0.1 - - [10/Oct/2023:13:56:03 +0000] "GET /api/data?page=3 HTTP/1.1" 404 123
    127.0.0.1 - - [10/Oct/2023:13:56:04 +0000] "GET /favicon.ico HTTP/1.1" 200 1234
    """.strip().split('\n')
    
    # Run the pipeline
    result = pipeline(sample_logs)
    print(result)

def process_ecommerce_data() -> None:
    """Process e-commerce transaction data."""
    print("\n=== E-commerce Data Processing Pipeline ===")
    
    # Sample data (in a real scenario, this would be read from a file/database)
    transactions = [
        {'order_id': '1001', 'customer_id': 'C101', 'product_id': 'P001', 
         'quantity': 2, 'unit_price': 19.99, 'date': '2023-10-01'},
        {'order_id': '1001', 'customer_id': 'C101', 'product_id': 'P002', 
         'quantity': 1, 'unit_price': 49.99, 'date': '2023-10-01'},
        {'order_id': '1002', 'customer_id': 'C102', 'product_id': 'P001', 
         'quantity': 3, 'unit_price': 19.99, 'date': '2023-10-02'},
        {'order_id': '1003', 'customer_id': 'C101', 'product_id': 'P003', 
         'quantity': 1, 'unit_price': 99.99, 'date': '2023-10-03'},
        {'order_id': '1004', 'customer_id': 'C103', 'product_id': 'P002', 
         'quantity': 2, 'unit_price': 49.99, 'date': '2023-10-03'},
    ]
    
    # Define the pipeline
    pipeline = Pipeline.of(
        # Add calculated fields
        lambda records: [
            {**r, 'total_price': r['quantity'] * r['unit_price']} 
            for r in records
        ],
        
        # Calculate order totals
        lambda records: {
            'total_sales': sum(r['total_price'] for r in records),
            'total_orders': len({r['order_id'] for r in records}),
            'total_customers': len({r['customer_id'] for r in records}),
            'total_products': len({r['product_id'] for r in records}),
            'sales_by_date': aggregate(
                'date',
                total_sales=('total_price', sum),
                order_count=('order_id', lambda x: len(set(x)))
            )(records),
            'top_customers': aggregate(
                'customer_id',
                total_spent=('total_price', sum),
                order_count=('order_id', lambda x: len(set(x))),
                avg_order_value=('total_price', lambda x: sum(x) / len(x))
            )(records),
            'top_products': aggregate(
                'product_id',
                total_quantity=('quantity', sum),
                total_revenue=('total_price', sum),
                order_count=('order_id', lambda x: len(set(x)))
            )(records)
        },
        
        # Convert to pretty-printed JSON
        lambda x: json.dumps(x, indent=2, default=str)
    )
    
    # Run the pipeline
    result = pipeline(transactions)
    print(result)

def process_csv_data() -> None:
    """Process CSV data with a pipeline."""
    print("\n=== CSV Data Processing Pipeline ===")
    
    # Sample CSV data (in a real scenario, this would be a file)
    csv_data = """name,age,city,score
Alice,30,New York,85.5
Bob,25,Los Angeles,92.3
Charlie,35,Chicago,78.9
Diana,28,New York,95.1
Eve,40,Los Angeles,88.7
""".strip().split('\n')
    
    # Define the pipeline
    pipeline = Pipeline.of(
        # Parse CSV lines
        lambda lines: map(parse_csv(), lines),
        
        # Convert types
        map_field('age', int, 0),
        map_field('score', float, 0.0),
        
        # Filter and transform
        filter_records(lambda r: r.get('age', 0) >= 25),
        add_field('is_high_score', lambda r: r['score'] >= 90.0),
        
        # Calculate statistics
        lambda records: list(records),  # Materialize the iterator
        lambda records: {
            'total_records': len(records),
            'average_age': sum(r['age'] for r in records) / len(records),
            'average_score': sum(r['score'] for r in records) / len(records),
            'high_scorers': [r['name'] for r in records if r['is_high_score']],
            'by_city': aggregate(
                'city',
                count=('name', len),
                avg_age=('age', lambda x: sum(x) / len(x)),
                avg_score=('score', lambda x: sum(x) / len(x))
            )(records)
        },
        
        # Convert to pretty-printed JSON
        lambda x: json.dumps(x, indent=2)
    )
    
    # Run the pipeline
    result = pipeline(csv_data)
    print(result)

if __name__ == "__main__":
    process_web_logs()
    process_ecommerce_data()
    process_csv_data()
    
    print("\n=== Key Takeaways ===")
    print("1. Pipelines help organize data processing into clear, reusable steps")
    print("2. Each step should have a single responsibility")
    print("3. Use lazy evaluation with generators for large datasets")
    print("4. Handle errors and edge cases gracefully")
    print("5. Make pipelines configurable and reusable")
    print("6. Document the expected input and output of each step")
