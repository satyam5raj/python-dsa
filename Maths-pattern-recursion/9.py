# Extract first Digit 

def first_digit(n):
    while n >= 10:
        n = n // 10
    return n

print(first_digit(1234))