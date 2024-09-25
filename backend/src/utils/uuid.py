import random

def simple_uuid(length: int, symbols: str = "ABCDEFGHKLMNORUVS123456789") -> str:
    # Validate the length and symbols arguments
    if length <= 0:
        raise ValueError("Length must be a positive integer.")
    if not symbols:
        raise ValueError("Symbols must be a non-empty string.")
    
    # Generate the UUID-like string
    return ''.join(random.choice(symbols) for _ in range(length))
