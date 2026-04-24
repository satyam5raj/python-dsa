# Sum of natural numbers 

def sum(n):
    if n==1:
        return 1
    
    x = n + sum(n-1)
    print(x)
    return x

n = 5
print(sum(n))
