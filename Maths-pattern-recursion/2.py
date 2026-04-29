# Reverse a number 

def reverse_number(n):
    rev = 0
    while n:
        digit = n % 10
        rev = rev * 10 + digit
        n = n // 10
    return rev

print(reverse_number(1234))