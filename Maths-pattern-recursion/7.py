# Count zeros in number 

def count_zeros(n):
    count = 0
    while n:
        if n%10 == 0:
            count += 1
        n = n//10
    return count

print(count_zeros(120201))