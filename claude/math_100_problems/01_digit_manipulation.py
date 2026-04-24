"""
================================================================
MATH PROBLEMS 1-15: DIGIT MANIPULATION
================================================================
"""

# ================================================================
# PROBLEM 1: Count digits of a number
# ================================================================
"""
INTERVIEW: "I'll count digits by repeatedly dividing by 10 until 0.
Alternatively: len(str(n)) for simplicity, but math approach shows understanding."
"""
def count_digits_brute(n: int) -> int:
    """APPROACH 1: Convert to string — O(d)"""
    return len(str(abs(n)))

def count_digits_math(n: int) -> int:
    """APPROACH 2: Math — O(d) where d = number of digits"""
    import math
    if n == 0: return 1
    return int(math.log10(abs(n))) + 1

def count_digits_loop(n: int) -> int:
    """APPROACH 3: Loop division — most interview-friendly"""
    n = abs(n)
    if n == 0: return 1
    count = 0
    while n:
        n //= 10
        count += 1
    return count

# Time: O(d), Space: O(1)

# ================================================================
# PROBLEM 2: Reverse a number
# ================================================================
"""
INTERVIEW: "Extract last digit with n%10, build reversed number.
Handle sign separately. Check overflow for 32-bit integers."
"""
def reverse_number(n: int) -> int:
    """
    APPROACH 1 (String): O(d)
    APPROACH 2 (Math): O(d) — preferred for interviews

    INTERVIEW SCRIPT:
    "Extract last digit: n%10. Build reversed: rev*10 + digit.
     Remove last digit: n//10. Repeat until n=0.
     Handle negative sign separately."
    """
    # String approach
    def string_approach(n):
        neg = n < 0
        n = abs(n)
        rev = int(str(n)[::-1])
        return -rev if neg else rev

    # Math approach
    neg = n < 0
    n = abs(n)
    rev = 0
    while n:
        rev = rev * 10 + n % 10
        n //= 10
    return -rev if neg else rev

# ================================================================
# PROBLEM 3: Check palindrome number
# ================================================================
"""
INTERVIEW: "A palindrome reads same forwards and backwards.
For numbers: reverse the number and check if equal to original.
Edge: negative numbers and multiples of 10 (ending in 0) are not palindromes."
"""
def is_palindrome_number(n: int) -> bool:
    """APPROACH 1: Convert to string — O(d)"""
    if n < 0:
        return False
    return str(n) == str(n)[::-1]

def is_palindrome_number_math(n: int) -> bool:
    """
    APPROACH 2: Math — O(d), O(1) space

    INTERVIEW SCRIPT:
    "Negative numbers can't be palindromes.
     Numbers ending in 0 (except 0 itself) can't be palindromes.
     Reverse only half the number to avoid overflow."
    """
    if n < 0 or (n % 10 == 0 and n != 0):
        return False
    rev = 0
    while n > rev:
        rev = rev * 10 + n % 10
        n //= 10
    return n == rev or n == rev // 10  # even or odd length

# ================================================================
# PROBLEM 4: Sum of digits
# ================================================================
def sum_of_digits(n: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Extract each digit with n%10, add to sum, divide by 10."
    """
    n = abs(n)
    total = 0
    while n:
        total += n % 10
        n //= 10
    return total

# O(d) time, O(1) space

# ================================================================
# PROBLEM 5: Product of digits
# ================================================================
def product_of_digits(n: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Same as sum but multiply. If any digit is 0, product is 0."
    """
    n = abs(n)
    product = 1
    while n:
        product *= n % 10
        n //= 10
    return product

# ================================================================
# PROBLEM 6: Armstrong number
# ================================================================
"""
Armstrong number: sum of each digit raised to power of number of digits equals n.
Example: 153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153 ✓
"""
def is_armstrong(n: int) -> bool:
    """
    INTERVIEW SCRIPT:
    "Count digits first to get the power.
     Then check if sum of (digit^power) equals n."
    """
    digits = str(abs(n))
    power = len(digits)
    return sum(int(d) ** power for d in digits) == abs(n)

def is_armstrong_math(n: int) -> bool:
    """Math approach"""
    import math
    if n < 0: return False
    d = count_digits_loop(n)
    temp = n
    total = 0
    while temp:
        total += (temp % 10) ** d
        temp //= 10
    return total == n

# ================================================================
# PROBLEM 7: Count zeros in number
# ================================================================
def count_zeros(n: int) -> int:
    """Count how many zeros in the digits"""
    n = abs(n)
    count = 0
    while n:
        if n % 10 == 0:
            count += 1
        n //= 10
    return count

# ================================================================
# PROBLEM 8: Remove last digit
# ================================================================
def remove_last_digit(n: int) -> int:
    """Integer division by 10 removes last digit"""
    return n // 10  # e.g., 1234 → 123

# ================================================================
# PROBLEM 9: Extract first digit
# ================================================================
def first_digit(n: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Keep dividing by 10 until single digit remains."
    """
    n = abs(n)
    while n >= 10:
        n //= 10
    return n

def first_digit_math(n: int) -> int:
    """Math: divide by 10^(d-1)"""
    import math
    n = abs(n)
    d = int(math.log10(n))
    return n // (10 ** d)

# ================================================================
# PROBLEM 10: Check if number contains digit k
# ================================================================
def contains_digit(n: int, k: int) -> bool:
    """
    INTERVIEW SCRIPT:
    "Extract each digit and compare with k."
    """
    n = abs(n)
    while n:
        if n % 10 == k:
            return True
        n //= 10
    return k == 0 and n == 0

# ================================================================
# PROBLEM 11: Replace all 0s with 1s
# ================================================================
def replace_zero_with_one(n: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Build number digit by digit. Replace 0 → 1."
    """
    if n == 0:
        return 1
    result = 0
    place = 1
    while n:
        d = n % 10
        if d == 0:
            d = 1
        result += d * place
        place *= 10
        n //= 10
    return result

# ================================================================
# PROBLEM 12: Largest digit in number
# ================================================================
def largest_digit(n: int) -> int:
    n = abs(n)
    max_d = 0
    while n:
        max_d = max(max_d, n % 10)
        n //= 10
    return max_d

# ================================================================
# PROBLEM 13: Smallest digit in number
# ================================================================
def smallest_digit(n: int) -> int:
    n = abs(n)
    min_d = 9
    while n:
        min_d = min(min_d, n % 10)
        n //= 10
    return min_d

# ================================================================
# PROBLEM 14: Count even/odd digits
# ================================================================
def count_even_odd_digits(n: int):
    """
    INTERVIEW SCRIPT:
    "Even digit: d % 2 == 0. Odd digit: d % 2 == 1."
    """
    n = abs(n)
    even_count = odd_count = 0
    while n:
        d = n % 10
        if d % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
        n //= 10
    return even_count, odd_count

# ================================================================
# PROBLEM 15: Rotate digits left/right
# ================================================================
def rotate_left(n: int) -> int:
    """
    Rotate digits left: 1234 → 2341
    INTERVIEW SCRIPT:
    "First digit goes to end. Remove first digit, append to right."
    """
    d = count_digits_loop(n)
    first = n // (10 ** (d - 1))
    return (n % (10 ** (d - 1))) * 10 + first

def rotate_right(n: int) -> int:
    """
    Rotate digits right: 1234 → 4123
    INTERVIEW SCRIPT:
    "Last digit goes to front."
    """
    d = count_digits_loop(n)
    last = n % 10
    return last * (10 ** (d - 1)) + n // 10

# ================================================================
# TEST ALL
# ================================================================
if __name__ == "__main__":
    print("=== DIGIT MANIPULATION ===")
    print("1. Count digits 12345:", count_digits_loop(12345))        # 5
    print("2. Reverse 12345:", reverse_number(12345))                 # 54321
    print("3. Is palindrome 121:", is_palindrome_number_math(121))   # True
    print("3. Is palindrome 123:", is_palindrome_number_math(123))   # False
    print("4. Sum of digits 12345:", sum_of_digits(12345))            # 15
    print("5. Product of digits 123:", product_of_digits(123))        # 6
    print("6. Is Armstrong 153:", is_armstrong(153))                   # True
    print("6. Is Armstrong 123:", is_armstrong(123))                   # False
    print("7. Count zeros 10230:", count_zeros(10230))                # 2
    print("8. Remove last digit 1234:", remove_last_digit(1234))     # 123
    print("9. First digit 54321:", first_digit(54321))                # 5
    print("10. Contains 5 in 12345:", contains_digit(12345, 5))      # True
    print("11. Replace 0→1 in 10023:", replace_zero_with_one(10023)) # 11123
    print("12. Largest digit 46821:", largest_digit(46821))          # 8
    print("13. Smallest digit 46821:", smallest_digit(46821))        # 1
    print("14. Even/Odd digits 1234:", count_even_odd_digits(1234))  # (2, 2)
    print("15. Rotate left 1234:", rotate_left(1234))                 # 2341
    print("15. Rotate right 1234:", rotate_right(1234))               # 4123
