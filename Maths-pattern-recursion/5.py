# product od digits 

def product_of_digits(n):
    product = 1
    while n:
        product = product * n%10
        n = n // 10
    return product

print(product_of_digits(123))