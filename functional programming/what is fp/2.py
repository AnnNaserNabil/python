def add_prefix(document, documents):
    # This function demonstrates immutability and pure functions in functional programming
    # It takes a document and a tuple of documents, and returns a new tuple with the prefixed document added
    
    # Create a prefix based on the current number of documents
    # In functional programming, we avoid modifying state, so we calculate based on inputs
    prefix = f"{len(documents)}. "
    
    # Create a new document with the prefix
    # Note: We're not modifying the original document
    new_doc = prefix + document
    
    # Return a new tuple with the new document added
    # Tuples are immutable in Python, so we create a new one instead of modifying the original
    # This follows the principle of immutability in functional programming
    return documents + (new_doc,)
