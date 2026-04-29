# Count digits of a number 

def count_digits(num):
    n = abs(num)
    if n == 0: return 1
    count = 0
    while n:
        n = n // 10
        print("n", n)
        count = count + 1
        print("Count", count)
    return count

def count_digits_brute(num):
    return len(str(abs(num)))

print(count_digits(123))