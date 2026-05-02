# Check if number contains digit k 

def contains_digit(n: int, k: int) -> bool:
    n = abs(n)
    while n:
        if n % 10 == k:
            return True
        n = n // 10
    return False

print(contains_digit(1234, 2))