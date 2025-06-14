def stylize_title(document):
    # This function demonstrates function composition, a key concept in functional programming
    # It takes a document and applies two functions in sequence:
    # 1. First centers the title using center_title()
    # 2. Then adds a border using add_border()
    # The output of center_title() becomes the input to add_border()
    return add_border(center_title(document))


# Don't touch below this line


def center_title(document):
    # This is a pure function - it always produces the same output for the same input
    # and has no side effects (doesn't modify external state)
    width = 40
    # Extract the first line (title) from the document
    title = document.split("\n")[0]
    # Center the title within the specified width
    centered_title = title.center(width)
    # Return a new string with the centered title
    # Note: strings are immutable in Python, so we create a new string
    return document.replace(title, centered_title)


def add_border(document):
    # Another pure function that adds a border below the title
    # It takes a document and returns a new document with a border
    
    # Extract the title (first line)
    title = document.split("\n")[0]
    # Create a border of asterisks matching the title's length
    border = "*" * len(title)
    # Return a new string with the border added below the title
    # This demonstrates immutability - we're not modifying the original string
    return document.replace(title, title + "\n" + border)