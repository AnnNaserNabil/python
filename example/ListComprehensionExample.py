# 20 Python Functions Using List Comprehension
# Gradually increasing in complexity

# 1. BASIC - Generate squares of numbers
def squares(n):
    """Return list of squares from 0 to n-1"""
    return [x**2 for x in range(n)]

# 2. BASIC - Convert strings to uppercase
def uppercase_words(words):
    """Convert all words in list to uppercase"""
    return [word.upper() for word in words]

# 3. BASIC WITH FILTER - Get even numbers
def even_numbers(numbers):
    """Return only even numbers from the list"""
    return [x for x in numbers if x % 2 == 0]

# 4. BASIC WITH FILTER - Get words longer than n characters
def long_words(words, min_length):
    """Return words longer than min_length"""
    return [word for word in words if len(word) > min_length]

# 5. SIMPLE TRANSFORMATION - Get string lengths
def word_lengths(words):
    """Return list of word lengths"""
    return [len(word) for word in words]

# 6. SIMPLE MATH - Apply mathematical operations
def apply_formula(numbers):
    """Apply formula: 2x + 1 to each number"""
    return [2*x + 1 for x in numbers]

# 7. STRING MANIPULATION - Extract first character
def first_chars(words):
    """Extract first character of each non-empty word"""
    return [word[0] for word in words if word]

# 8. CONDITIONAL TRANSFORMATION - Different operations based on condition
def conditional_transform(numbers):
    """Square positive numbers, negate negative numbers"""
    return [x**2 if x > 0 else -x for x in numbers]

# 9. NESTED STRUCTURE - Flatten 2D list
def flatten_matrix(matrix):
    """Flatten a 2D matrix into 1D list"""
    return [item for row in matrix for item in row]

# 10. MULTIPLE CONDITIONS - Complex filtering
def filter_numbers(numbers):
    """Get numbers that are positive and divisible by 3"""
    return [x for x in numbers if x > 0 and x % 3 == 0]

# 11. STRING PROCESSING - Clean and filter strings
def clean_strings(strings):
    """Remove whitespace and get non-empty strings starting with uppercase"""
    return [s.strip() for s in strings if s.strip() and s.strip()[0].isupper()]

# 12. NESTED LOOPS WITH CONDITION - Generate coordinate pairs
def valid_coordinates(max_x, max_y):
    """Generate coordinates where x + y is even"""
    return [(x, y) for x in range(max_x) for y in range(max_y) if (x + y) % 2 == 0]

# 13. DICTIONARY OPERATIONS - Extract values with condition
def extract_scores(students):
    """Extract scores of students who passed (score >= 60)"""
    return [student['score'] for student in students if student.get('score', 0) >= 60]

# 14. COMPLEX STRING MANIPULATION - Process file extensions
def process_filenames(filenames):
    """Get uppercase extensions of Python files"""
    return [fname.split('.')[-1].upper() for fname in filenames 
            if '.' in fname and fname.endswith('.py')]

# 15. MATHEMATICAL SEQUENCES - Generate Fibonacci-like sequence
def fibonacci_like(n, a=0, b=1):
    """Generate first n numbers of Fibonacci-like sequence"""
    result = [a, b]
    return result + [result[i-1] + result[i-2] for i in range(2, n)][:n]

# 16. NESTED COMPREHENSION - Process nested data structures
def extract_nested_values(data):
    """Extract all numeric values from nested dictionaries"""
    return [val for item in data for val in item.values() 
            if isinstance(val, (int, float))]

# 17. COMPLEX FILTERING - Multiple conditions with string operations
def filter_emails(emails):
    """Get valid Gmail addresses with specific criteria"""
    return [email.lower() for email in emails 
            if '@gmail.com' in email.lower() 
            and len(email.split('@')[0]) >= 3
            and '.' not in email.split('@')[0]]

# 18. ADVANCED NESTED - Matrix operations
def matrix_diagonal_sums(matrices):
    """Calculate sum of main diagonal for each square matrix"""
    return [sum(matrix[i][i] for i in range(len(matrix))) 
            for matrix in matrices 
            if len(matrix) == len(matrix[0]) and len(matrix) > 0]

# 19. COMPLEX TRANSFORMATION - Process complex data structures
def process_transactions(transactions):
    """Process financial transactions: get amounts of completed high-value transactions"""
    return [trans['amount'] * (1 - trans.get('fee_rate', 0)) 
            for trans in transactions 
            if trans.get('status') == 'completed' 
            and trans.get('amount', 0) > 1000
            and trans.get('type') != 'refund']

# 20. ADVANCED ALGORITHM - Generate Pascal's Triangle row
def pascal_triangle_row(n):
    """Generate nth row of Pascal's triangle using list comprehension"""
    if n == 0:
        return [1]
    prev_row = pascal_triangle_row(n-1)
    return [1] + [prev_row[i] + prev_row[i+1] for i in range(len(prev_row)-1)] + [1]


# Test functions with sample data
if __name__ == "__main__":
    print("1. Squares:", squares(5))
    print("2. Uppercase:", uppercase_words(['hello', 'world']))
    print("3. Even numbers:", even_numbers([1, 2, 3, 4, 5, 6]))
    print("4. Long words:", long_words(['cat', 'elephant', 'dog'], 3))
    print("5. Word lengths:", word_lengths(['hello', 'world', 'python']))
    print("6. Formula applied:", apply_formula([1, 2, 3, 4]))
    print("7. First chars:", first_chars(['hello', 'world', '']))
    print("8. Conditional transform:", conditional_transform([-2, -1, 0, 1, 2]))
    print("9. Flatten matrix:", flatten_matrix([[1, 2], [3, 4], [5, 6]]))
    print("10. Filtered numbers:", filter_numbers([-3, 3, 6, 9, 10, 12]))
    
    print("11. Clean strings:", clean_strings(['  Hello', 'world  ', '  Python  ', ' test']))
    print("12. Valid coordinates:", valid_coordinates(3, 3))
    
    students = [{'name': 'Alice', 'score': 85}, {'name': 'Bob', 'score': 45}, {'name': 'Charlie', 'score': 92}]
    print("13. Passed scores:", extract_scores(students))
    
    files = ['main.py', 'test.txt', 'utils.py', 'README.md']
    print("14. Python extensions:", process_filenames(files))
    
    print("15. Fibonacci-like:", fibonacci_like(8))
    
    nested_data = [{'a': 1, 'b': 'text'}, {'c': 3.14, 'd': True}, {'e': 42}]
    print("16. Nested values:", extract_nested_values(nested_data))
    
    emails = ['john.doe@gmail.com', 'ab@gmail.com', 'valid123@gmail.com', 'test@yahoo.com']
    print("17. Valid emails:", filter_emails(emails))
    
    matrices = [[[1, 2], [3, 4]], [[5, 6, 7], [8, 9, 10], [11, 12, 13]]]
    print("18. Diagonal sums:", matrix_diagonal_sums(matrices))
    
    transactions = [
        {'amount': 1500, 'status': 'completed', 'fee_rate': 0.02, 'type': 'purchase'},
        {'amount': 500, 'status': 'completed', 'fee_rate': 0.01, 'type': 'purchase'},
        {'amount': 2000, 'status': 'pending', 'fee_rate': 0.03, 'type': 'purchase'}
    ]
    print("19. Processed transactions:", process_transactions(transactions))
    
    print("20. Pascal's triangle row 4:", pascal_triangle_row(4))