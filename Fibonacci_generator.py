def fibonacci_generator(n):
    """Generate the first 'n' Fibonacci numbers."""
    fib_series = []
    a, b = 0, 1  # Start with 0 and 1
    for _ in range(n):
        fib_series.append(a)
        a, b = b, a + b  # Update values
    return fib_series


# Usage
n = 100  # Generate the first 100 Fibonacci numbers
print("Fibonacci Series:", fibonacci_generator(n))

