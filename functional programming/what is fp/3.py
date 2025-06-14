def get_median_font_size(font_sizes):
    # This is a pure function that demonstrates functional programming principles:
    # 1. It's deterministic - same input always produces same output
    # 2. No side effects - doesn't modify any external state
    # 3. Works with immutable data - creates new sorted list instead of modifying in-place
    
    # Handle empty input case
    if len(font_sizes) == 0:
        return None
    
    # Create a new sorted list (sorted() returns a new list, doesn't modify original)
    # This is important in functional programming - we don't modify the input
    sorted_sizes = sorted(font_sizes)
    
    # Calculate the middle index for the median
    # Using integer division to handle both even and odd lengths
    middle_index = (len(sorted_sizes) - 1) // 2
    
    # Return the median value
    # No variables are modified after their creation, which is common in functional style
    return sorted_sizes[middle_index]

