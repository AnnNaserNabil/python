#!/usr/bin/env python3
"""
🧪 Interactive Mini Project: Pythonic Practice Tasks
A collection of Python functions demonstrating various programming concepts
"""

def count_emojis(text):
    """Count how many emojis are in a given string"""
    emojis = {"❤️", "🐍", "😍", "😭", "🔥", "✨", "🚀", "💻", "📚", "🎉"}
    return sum(1 for char in text if char in emojis)

def find_palindromes(words):
    """Return all palindromes in a list of words"""
    return [word for word in words if word == word[::-1]]

def count_capital_words(sentence):
    """Count how many words start with a capital letter"""
    return sum(1 for word in sentence.split() if word.istitle())

def even_length_words(words):
    """Filter words that have even length"""
    return [word for word in words if len(word) % 2 == 0]

def grade_scores(scores):
    """Convert numeric scores to letter grades"""
    return [
        'A' if s >= 90 else 'B' if s >= 80 else 'C' if s >= 60 else 'F'
        for s in scores
    ]

def clean_hashtags(tags):
    """Clean hashtags by removing # and extra spaces, then join them"""
    return " ".join(tag.strip().lstrip("#") for tag in tags)

def sum_of_squares_odds(nums):
    """Calculate sum of squares of odd numbers"""
    return sum(x**2 for x in nums if x % 2 == 1)

def word_length_map(words):
    """Create a dictionary mapping words to their lengths"""
    return {word: len(word) for word in words}

def all_lowercase(sentence):
    """Check if all words in a sentence are lowercase"""
    return all(word.islower() for word in sentence.split())

def extract_vowels(text):
    """Extract unique vowels from text (no duplicates)"""
    vowels = {'a', 'e', 'i', 'o', 'u'}
    return list({char.lower() for char in text if char.lower() in vowels})

# 🎯 Bonus Functions for Extra Practice
def reverse_words(sentence):
    """Reverse each word in a sentence while keeping word order"""
    return " ".join(word[::-1] for word in sentence.split())

def count_vowels_consonants(text):
    """Count vowels and consonants in text"""
    vowels = {'a', 'e', 'i', 'o', 'u'}
    vowel_count = sum(1 for char in text.lower() if char in vowels)
    consonant_count = sum(1 for char in text.lower() if char.isalpha() and char not in vowels)
    return {"vowels": vowel_count, "consonants": consonant_count}

def find_longest_word(words):
    """Find the longest word in a list"""
    return max(words, key=len) if words else ""

def remove_duplicates_preserve_order(items):
    """Remove duplicates while preserving original order"""
    seen = set()
    return [item for item in items if not (item in seen or seen.add(item))]

def digital_root(n):
    """Calculate digital root of a number (sum digits until single digit)"""
    while n >= 10:
        n = sum(int(digit) for digit in str(n))
    return n

# ✅ Test all functions
if __name__ == "__main__":
    print("🧪 PYTHONIC PRACTICE TASKS - TEST RESULTS")
    print("=" * 50)
    
    # Task 1: Emoji Counter
    print("1. Emoji Count:", count_emojis("I ❤️ Python 🐍 😍 😭 🔥"))
    
    # Task 2: Palindrome Filter
    print("2. Palindromes:", find_palindromes(["level", "world", "radar", "madam", "python"]))
    
    # Task 3: Count Capital Words
    print("3. Capital Words:", count_capital_words("Python Is A Great Programming Language"))
    
    # Task 4: Filter Even-Length Words
    print("4. Even Length Words:", even_length_words(["hello", "code", "AI", "no", "Python"]))
    
    # Task 5: Score Grade Evaluator
    print("5. Grades:", grade_scores([95, 82, 67, 45, 100, 78, 91]))
    
    # Task 6: Clean and Join Hashtags
    print("6. Clean Tags:", clean_hashtags([" #Python ", " #AI", " #CodeNewbie ", "#MachineLearning"]))
    
    # Task 7: Sum of Squares of Odd Numbers
    print("7. Sum of Squares (Odds):", sum_of_squares_odds([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    
    # Task 8: Word Length Mapper
    print("8. Word Length Map:", word_length_map(["Python", "is", "awesome", "!"]))
    
    # Task 9: Check if All Words Are Lowercase
    print("9. All Lowercase:", all_lowercase("python is amazing"))
    print("   All Lowercase (mixed):", all_lowercase("Python is Amazing"))
    
    # Task 10: Vowel Extractor
    print("10. Unique Vowels:", extract_vowels("Programming is fun and educational"))
    
    print("\n🎯 BONUS FUNCTIONS:")
    print("-" * 30)
    
    # Bonus functions
    print("11. Reverse Words:", reverse_words("Hello World Python"))
    print("12. Vowel/Consonant Count:", count_vowels_consonants("Hello World"))
    print("13. Longest Word:", find_longest_word(["Python", "JavaScript", "AI", "Programming"]))
    print("14. Remove Duplicates:", remove_duplicates_preserve_order([1, 2, 2, 3, 1, 4, 5, 3]))
    print("15. Digital Root:", digital_root(9875))
    
    print("\n✨ All functions completed successfully!")
    print("🚀 Ready for more Python challenges!")