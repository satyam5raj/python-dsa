# sum of digits 

def sum_of_digits(n):
    total = 0
    while n:
        total = total + n % 10
        n = n // 10
    return total

print(sum_of_digits(123))