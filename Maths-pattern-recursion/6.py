# Armstrong number 

def count_digits(n):
    count = 0
    while n>0:
        n = n//10
        count += 1
    return count

def is_armstrong(num):
    original = num
    count = count_digits(original)
    total = 0
    while num:
        total = total + (num % 10) ** count
        num = num // 10
    return total == original

print(is_armstrong(153))