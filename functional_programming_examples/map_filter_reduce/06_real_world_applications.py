"""
6. Real-World Applications of Map, Filter, and Reduce

This module demonstrates practical applications of map, filter, and reduce
in real-world scenarios including data processing, web development, and more.
"""
from __future__ import annotations
from typing import TypeVar, Callable, Iterable, Any, List, Dict, Tuple, Optional, Union, Iterator
from functools import reduce, partial
from collections import defaultdict, Counter, namedtuple
import csv
import json
import time
from datetime import datetime, timedelta
import re
from pathlib import Path
import os
import sys
from urllib.request import urlopen
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from typing import NamedTuple
import statistics
import math

T = TypeVar('T')
U = TypeVar('U')

# 1. Data Processing Pipeline

def process_sales_data() -> None:
    """Process sales data to generate reports."""
    print("=== Sales Data Processing ===\n")
    
    # Sample sales data (in a real app, this would come from a database or file)
    sales_data = [
        {"id": 1, "product": "Laptop", "category": "Electronics", "price": 999.99, "quantity": 2, "date": "2023-01-15"},
        {"id": 2, "product": "Smartphone", "category": "Electronics", "price": 699.99, "quantity": 5, "date": "2023-01-15"},
        {"id": 3, "product": "Desk Chair", "category": "Furniture", "price": 149.99, "quantity": 1, "date": "2023-01-16"},
        {"id": 4, "product": "Coffee Maker", "category": "Appliances", "price": 49.99, "quantity": 3, "date": "2023-01-16"},
        {"id": 5, "product": "Headphones", "category": "Electronics", "price": 199.99, "quantity": 2, "date": "2023-01-17"},
        {"id": 6, "product": "Desk Lamp", "category": "Furniture", "price": 29.99, "quantity": 4, "date": "2023-01-17"},
        {"id": 7, "product": "Laptop", "category": "Electronics", "price": 999.99, "quantity": 1, "date": "2023-01-18"},
        {"id": 8, "product": "Smartphone", "category": "Electronics", "price": 699.99, "quantity": 3, "date": "2023-01-19"},
    ]
    
    # 1.1 Calculate total sales by category
    def calculate_category_sales(sales: List[Dict]) -> Dict[str, float]:
        """Calculate total sales amount by category."""
        return reduce(
            lambda acc, sale: {
                **acc,
                sale['category']: acc.get(sale['category'], 0) + (sale['price'] * sale['quantity'])
            },
            sales,
            {}
        )
    
    # 1.2 Find top selling products
    def find_top_products(sales: List[Dict], n: int = 3) -> List[Dict]:
        """Find top n products by total revenue."""
        product_revenue = defaultdict(float)
        for sale in sales:
            product_revenue[sale['product']] += sale['price'] * sale['quantity']
        
        return sorted(
            [{"product": p, "revenue": r} for p, r in product_revenue.items()],
            key=lambda x: x["revenue"],
            reverse=True
        )[:n]
    
    # 1.3 Calculate daily sales
    def calculate_daily_sales(sales: List[Dict]) -> Dict[str, float]:
        """Calculate total sales by date."""
        return reduce(
            lambda acc, sale: {
                **acc,
                sale['date']: acc.get(sale['date'], 0) + (sale['price'] * sale['quantity'])
            },
            sales,
            {}
        )
    
    # Run the analysis
    category_sales = calculate_category_sales(sales_data)
    top_products = find_top_products(sales_data)
    daily_sales = calculate_daily_sales(sales_data)
    
    # Print results
    print("Category Sales:")
    for category, amount in category_sales.items():
        print(f"  {category}: ${amount:.2f}")
    
    print("\nTop Products by Revenue:")
    for i, product in enumerate(top_products, 1):
        print(f"  {i}. {product['product']}: ${product['revenue']:.2f}")
    
    print("\nDaily Sales:")
    for date, amount in sorted(daily_sales.items()):
        print(f"  {date}: ${amount:.2f}")

# 2. Web Scraping and Data Extraction

def process_web_data() -> None:
    """Extract and process data from web sources."""
    print("\n=== Web Data Processing ===\n")
    
    # In a real application, we would fetch this from a URL
    # For demonstration, we'll use a sample XML string
    xml_data = """
    <rss>
        <channel>
            <item>
                <title>Python 3.11 Released</title>
                <link>https://example.com/python-3.11</link>
                <pubDate>Mon, 24 Oct 2022 00:00:00 GMT</pubDate>
                <description>Python 3.11 is now available with major performance improvements.</description>
            </item>
            <item>
                <title>Django 4.1 Released</title>
                <link>https://example.com/django-4.1</link>
                <pubDate>Wed, 03 Aug 2022 00:00:00 GMT</pubDate>
                <description>Django 4.1 includes async ORM and more.</description>
            </item>
            <item>
                <title>Flask 2.2 Released</title>
                <link>https://example.com/flask-2.2</link>
                <pubDate>Mon, 03 Oct 2022 00:00:00 GMT</pubDate>
                <description>Flask 2.2 introduces new features and improvements.</description>
            </item>
        </channel>
    </rss>
    """
    
    # Parse XML data
    root = ET.fromstring(xml_data)
    
    # Extract items using list comprehension (similar to map)
    items = [
        {
            'title': item.find('title').text,
            'link': item.find('link').text,
            'date': item.find('pubDate').text,
            'description': item.find('description').text
        }
        for item in root.findall('.//item')
    ]
    
    # Filter recent items (within last 60 days)
    def is_recent(date_str: str, days: int = 60) -> bool:
        """Check if a date is within the last N days."""
        try:
            date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            return (datetime.now() - date) < timedelta(days=days)
        except (ValueError, TypeError):
            return False
    
    recent_items = list(filter(
        lambda item: is_recent(item['date']),
        items
    ))
    
    # Print results
    print(f"Found {len(items)} items, {len(recent_items)} are recent")
    
    print("\nRecent Items:")
    for item in recent_items:
        print(f"  - {item['title']} ({item['date']})")

# 3. Log File Analysis

def analyze_logs() -> None:
    """Analyze web server logs to extract insights."""
    print("\n=== Log File Analysis ===\n")
    
    # Sample log entries (in a real app, read from a file)
    log_entries = [
        '127.0.0.1 - - [10/Jan/2023:10:15:30 +0000] "GET /api/users HTTP/1.1" 200 1234',
        '192.168.1.1 - - [10/Jan/2023:10:15:31 +0000] "POST /api/login HTTP/1.1" 200 567',
        '10.0.0.1 - - [10/Jan/2023:10:15:32 +0000] "GET /api/products HTTP/1.1" 200 8901',
        '127.0.0.1 - - [10/Jan/2023:10:15:33 +0000] "GET /api/users/123 HTTP/1.1" 404 45',
        '192.168.1.1 - - [10/Jan/2023:10:15:34 +0000] "GET /api/products/abc HTTP/1.1" 200 2345',
        '10.0.0.1 - - [10/Jan/2023:10:15:35 +0000] "POST /api/orders HTTP/1.1" 201 3456',
        '127.0.0.1 - - [10/Jan/2023:10:15:36 +0000] "GET /api/users HTTP/1.1" 200 1234',
        '192.168.1.1 - - [10/Jan/2023:10:15:37 +0000] "GET /api/products HTTP/1.1" 200 8901',
        '10.0.0.1 - - [10/Jan/2023:10:15:38 +0000] "GET /api/nonexistent HTTP/1.1" 404 45',
        '127.0.0.1 - - [10/Jan/2023:10:15:39 +0000] "POST /api/orders HTTP/1.1" 201 3456',
    ]
    
    # Parse log entries
    def parse_log_entry(entry: str) -> Optional[Dict]:
        """Parse a log entry into its components."""
        pattern = r'(\S+) - - \[(.*?)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)'
        match = re.match(pattern, entry)
        if not match:
            return None
        
        ip, timestamp, method, path, protocol, status_code, size = match.groups()
        
        return {
            'ip': ip,
            'timestamp': timestamp,
            'method': method,
            'path': path,
            'protocol': protocol,
            'status_code': int(status_code),
            'size': int(size)
        }
    
    # Parse all log entries
    parsed_logs = list(filter(None, map(parse_log_entry, log_entries)))
    
    # 3.1 Count requests by status code
    status_counts = Counter(log['status_code'] for log in parsed_logs)
    
    # 3.2 Group by endpoint
    endpoint_counts = Counter(
        log['path'].split('?')[0]  # Remove query parameters
        for log in parsed_logs
    )
    
    # 3.3 Calculate statistics
    response_sizes = [log['size'] for log in parsed_logs]
    stats = {
        'total_requests': len(parsed_logs),
        'unique_ips': len({log['ip'] for log in parsed_logs}),
        'unique_endpoints': len(endpoint_counts),
        'total_bytes': sum(response_sizes),
        'avg_response_size': statistics.mean(response_sizes) if response_sizes else 0,
        'status_codes': dict(status_counts),
        'top_endpoints': endpoint_counts.most_common(3)
    }
    
    # Print results
    print("Log Analysis Results:")
    print(f"  Total requests: {stats['total_requests']}")
    print(f"  Unique IPs: {stats['unique_ips']}")
    print(f"  Total data transferred: {stats['total_bytes'] / 1024:.2f} KB")
    print(f"  Average response size: {stats['avg_response_size']:.2f} bytes")
    
    print("\nStatus Codes:")
    for code, count in stats['status_codes'].items():
        print(f"  {code}: {count} requests")
    
    print("\nTop Endpoints:")
    for endpoint, count in stats['top_endpoints']:
        print(f"  {endpoint}: {count} requests")

# 4. Data Cleaning and Transformation

def clean_and_transform_data() -> None:
    """Demonstrate data cleaning and transformation."""
    print("\n=== Data Cleaning and Transformation ===\n")
    
    # Sample data (in a real app, this would come from a CSV or database)
    raw_data = [
        {"id": 1, "name": "John Doe ", "email": "JOHN@example.com ", "age": "30", "salary": "50000"},
        {"id": 2, "name": " Jane Smith ", "email": "jane.smith@example.com", "age": "25", "salary": "60000"},
        {"id": 3, "name": "Bob Johnson ", "email": "bob@example", "age": "35", "salary": "75000"},
        {"id": 4, "name": "Alice", "email": "alice@example.com", "age": "28", "salary": "55000"},
        {"id": 5, "name": "Charlie Brown", "email": "charlie@example.com", "age": "40", "salary": "80000"},
    ]
    
    # 4.1 Define cleaning functions
    def clean_string(s: str) -> str:
        """Remove extra whitespace and convert to title case."""
        return s.strip().title()
    
    def clean_email(email: str) -> str:
        """Clean and validate email address."""
        email = email.strip().lower()
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return ""
        return email
    
    def clean_age(age: str) -> int:
        """Convert age to integer, handle invalid values."""
        try:
            age_int = int(age)
            return age_int if 18 <= age_int <= 120 else 0
        except (ValueError, TypeError):
            return 0
    
    def clean_salary(salary: str) -> float:
        """Convert salary to float, handle invalid values."""
        try:
            return float(salary)
        except (ValueError, TypeError):
            return 0.0
    
    # 4.2 Apply cleaning functions to each record
    cleaned_data = []
    for record in raw_data:
        cleaned_record = {
            'id': record['id'],
            'name': clean_string(record['name']),
            'email': clean_email(record['email']),
            'age': clean_age(record['age']),
            'salary': clean_salary(record['salary'])
        }
        cleaned_data.append(cleaned_record)
    
    # 4.3 Filter out invalid records
    valid_data = list(filter(
        lambda x: x['email'] and x['age'] > 0 and x['salary'] > 0,
        cleaned_data
    ))
    
    # 4.4 Calculate statistics
    if valid_data:
        avg_age = statistics.mean(record['age'] for record in valid_data)
        avg_salary = statistics.mean(record['salary'] for record in valid_data)
        total_records = len(valid_data)
    else:
        avg_age = avg_salary = 0.0
        total_records = 0
    
    # Print results
    print(f"Processed {len(raw_data)} records, {total_records} valid")
    print(f"Average age: {avg_age:.1f}")
    print(f"Average salary: ${avg_salary:,.2f}")
    
    print("\nCleaned Data:")
    for record in valid_data:
        print(f"  {record['name']} ({record['email']}): ${record['salary']:,.2f}")

# 5. Data Aggregation and Reporting

def generate_reports() -> None:
    """Generate various reports from data."""
    print("\n=== Data Aggregation and Reporting ===\n")
    
    # Sample sales data (in a real app, this would come from a database)
    sales_data = [
        {"region": "North", "product": "Laptop", "amount": 1200, "quantity": 5, "date": "2023-01-15"},
        {"region": "South", "product": "Laptop", "amount": 1200, "quantity": 3, "date": "2023-01-15"},
        {"region": "East", "product": "Tablet", "amount": 500, "quantity": 10, "date": "2023-01-15"},
        {"region": "West", "product": "Phone", "amount": 800, "quantity": 8, "date": "2023-01-15"},
        {"region": "North", "product": "Tablet", "amount": 500, "quantity": 6, "date": "2023-01-16"},
        {"region": "South", "product": "Phone", "amount": 800, "quantity": 4, "date": "2023-01-16"},
        {"region": "East", "product": "Laptop", "amount": 1200, "quantity": 2, "date": "2023-01-16"},
        {"region": "West", "product": "Tablet", "amount": 500, "quantity": 7, "date": "2023-01-16"},
        {"region": "North", "product": "Phone", "amount": 800, "quantity": 5, "date": "2023-01-17"},
        {"region": "South", "product": "Laptop", "amount": 1200, "quantity": 4, "date": "2023-01-17"},
    ]
    
    # 5.1 Sales by region
    def sales_by_region(sales: List[Dict]) -> Dict[str, float]:
        """Calculate total sales by region."""
        return reduce(
            lambda acc, sale: {
                **acc,
                sale['region']: acc.get(sale['region'], 0) + sale['amount'] * sale['quantity']
            },
            sales,
            {}
        )
    
    # 5.2 Sales by product
    def sales_by_product(sales: List[Dict]) -> Dict[str, Dict]:
        """Calculate sales statistics by product."""
        product_data = defaultdict(lambda: {'total_sales': 0, 'total_quantity': 0, 'regions': set()})
        
        for sale in sales:
            product = sale['product']
            product_data[product]['total_sales'] += sale['amount'] * sale['quantity']
            product_data[product]['total_quantity'] += sale['quantity']
            product_data[product]['regions'].add(sale['region'])
        
        return {
            product: {
                'total_sales': data['total_sales'],
                'total_quantity': data['total_quantity'],
                'avg_price': data['total_sales'] / data['total_quantity'] if data['total_quantity'] else 0,
                'regions_served': len(data['regions'])
            }
            for product, data in product_data.items()
        }
    
    # 5.3 Daily sales trend
    def daily_sales_trend(sales: List[Dict]) -> Dict[str, float]:
        """Calculate daily sales totals."""
        return reduce(
            lambda acc, sale: {
                **acc,
                sale['date']: acc.get(sale['date'], 0) + sale['amount'] * sale['quantity']
            },
            sales,
            {}
        )
    
    # Generate reports
    region_sales = sales_by_region(sales_data)
    product_stats = sales_by_product(sales_data)
    daily_trend = daily_sales_trend(sales_data)
    
    # Print reports
    print("=== Sales by Region ===")
    for region, sales in sorted(region_sales.items()):
        print(f"  {region}: ${sales:,.2f}")
    
    print("\n=== Product Performance ===")
    for product, stats in product_stats.items():
        print(f"\n{product}:")
        print(f"  Total Sales: ${stats['total_sales']:,.2f}")
        print(f"  Units Sold: {stats['total_quantity']}")
        print(f"  Average Price: ${stats['avg_price']:,.2f}")
        print(f"  Regions Served: {stats['regions_served']}")
    
    print("\n=== Daily Sales Trend ===")
    for date, sales in sorted(daily_trend.items()):
        print(f"  {date}: ${sales:,.2f}")

def main() -> None:
    """Run all demonstrations."""
    process_sales_data()
    process_web_data()
    analyze_logs()
    clean_and_transform_data()
    generate_reports()

if __name__ == "__main__":
    main()
