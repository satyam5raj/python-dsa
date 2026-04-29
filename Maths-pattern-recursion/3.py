# check palindrome number 

def plaindroe_number(n):
    original = n
    rev = 0
    while n > 0:
        digit = n % 10
        rev = rev * 10 + digit
        n = n // 10
    return original == rev

print(plaindroe_number(1221))