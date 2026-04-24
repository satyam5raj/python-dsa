"""
================================================================
MATH PROBLEMS 31-45: MATHEMATICAL FORMULAS
================================================================
"""

from typing import List

# ================================================================
# PROBLEM 31: Sum of first n numbers
# ================================================================
def sum_n_brute(n: int) -> int:
    """APPROACH 1: O(n) loop"""
    return sum(range(1, n + 1))

def sum_n_formula(n: int) -> int:
    """
    APPROACH 2: O(1) formula — n*(n+1)/2

    INTERVIEW SCRIPT:
    "Gauss's formula: 1+2+...+n = n*(n+1)/2.
     Proof: pair first and last (1+n), second and second-last (2+(n-1)).
     All pairs sum to n+1, and there are n/2 such pairs."
    """
    return n * (n + 1) // 2

# ================================================================
# PROBLEM 32: Sum of squares
# ================================================================
def sum_squares_brute(n: int) -> int:
    """O(n)"""
    return sum(i*i for i in range(1, n+1))

def sum_squares_formula(n: int) -> int:
    """
    APPROACH 2: O(1) — n*(n+1)*(2n+1)/6

    INTERVIEW SCRIPT:
    "Formula: n*(n+1)*(2n+1)/6.
     Derivation uses telescope sum and algebraic manipulation."
    """
    return n * (n + 1) * (2 * n + 1) // 6

# ================================================================
# PROBLEM 33: Sum of cubes
# ================================================================
def sum_cubes_brute(n: int) -> int:
    """O(n)"""
    return sum(i**3 for i in range(1, n+1))

def sum_cubes_formula(n: int) -> int:
    """
    APPROACH 2: O(1) — [n*(n+1)/2]²

    INTERVIEW SCRIPT:
    "Beautiful identity: sum of cubes = (sum of first n numbers)²
     = [n*(n+1)/2]²"
    """
    s = n * (n + 1) // 2
    return s * s

# ================================================================
# PROBLEM 34: Find missing number (1 to n)
# ================================================================
def missing_number_sum(arr: List[int], n: int) -> int:
    """
    APPROACH 1: Sum formula — O(n), O(1)

    INTERVIEW SCRIPT:
    "Expected sum = n*(n+1)/2. Actual sum = sum of array.
     Missing = expected - actual."
    """
    expected = n * (n + 1) // 2
    return expected - sum(arr)

def missing_number_xor(arr: List[int], n: int) -> int:
    """
    APPROACH 2: XOR — O(n), O(1)

    INTERVIEW SCRIPT:
    "XOR 1..n with all array elements. Pairs cancel → missing remains."
    """
    xor = 0
    for i in range(1, n + 1):
        xor ^= i
    for num in arr:
        xor ^= num
    return xor

# ================================================================
# PROBLEM 35: Find duplicate number
# ================================================================
def find_duplicate_sum(arr: List[int], n: int) -> int:
    """
    APPROACH 1: Sum formula — O(n)
    duplicate = actual_sum - expected_sum
    """
    expected = n * (n - 1) // 2  # sum of 0..n-1
    return sum(arr) - expected

def find_duplicate_xor(arr: List[int]) -> int:
    """APPROACH 2: XOR — O(n), O(1)"""
    xor = 0
    for num in arr:
        xor ^= num
    n = len(arr) - 1
    for i in range(1, n + 1):
        xor ^= i
    return xor

# ================================================================
# PROBLEM 36: Sum of arithmetic progression
# ================================================================
def sum_ap(a: int, d: int, n: int) -> int:
    """
    Sum of AP: n/2 * (2a + (n-1)d)
    a = first term, d = common difference, n = terms

    INTERVIEW SCRIPT:
    "AP sum formula: n/2 * (first + last).
     Last term = a + (n-1)*d.
     Or: n/2 * (2a + (n-1)*d)"
    """
    return n * (2 * a + (n - 1) * d) // 2

# ================================================================
# PROBLEM 37: Sum of geometric progression
# ================================================================
def sum_gp(a: float, r: float, n: int) -> float:
    """
    Sum of GP: a*(r^n - 1)/(r - 1) if r != 1, else a*n
    a = first term, r = common ratio, n = terms

    INTERVIEW SCRIPT:
    "GP sum: a*(1-r^n)/(1-r) for |r| < 1, or a*(r^n-1)/(r-1) for r > 1."
    """
    if r == 1:
        return a * n
    return a * (r**n - 1) / (r - 1)

# ================================================================
# PROBLEM 38: Trailing zeros in factorial
# ================================================================
def trailing_zeros_factorial(n: int) -> int:
    """
    Count trailing zeros in n!

    APPROACH 1 (Compute n!): Too large for big n
    APPROACH 2 (Count factors of 5): O(log n)

    INTERVIEW SCRIPT:
    "Trailing zeros come from factors of 10 = 2 × 5.
     There are more factors of 2 than 5, so count factors of 5.
     n! has ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ... factors of 5.
     Why? 5 contributes 1, 25 contributes 2 (extra), etc."
    """
    count = 0
    power = 5
    while power <= n:
        count += n // power
        power *= 5
    return count

# ================================================================
# PROBLEM 39: Factorial of n
# ================================================================
def factorial_iterative(n: int) -> int:
    """O(n) iterative — preferred over recursive in interviews"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_recursive(n: int) -> int:
    """O(n) recursive, O(n) space"""
    if n <= 1: return 1
    return n * factorial_recursive(n - 1)

# ================================================================
# PROBLEM 40: Fast power a^n
# ================================================================
def power_brute(base: float, exp: int) -> float:
    """APPROACH 1: O(n) — multiply n times"""
    result = 1
    for _ in range(abs(exp)):
        result *= base
    return result if exp >= 0 else 1/result

def power_fast(base: float, exp: int) -> float:
    """
    APPROACH 2: Binary Exponentiation — O(log n)

    INTERVIEW SCRIPT:
    "a^n = a^(n/2) * a^(n/2) if n is even.
     a^n = a * a^(n-1) if n is odd.
     This halves the exponent each time → O(log n)."
    """
    if exp < 0:
        return power_fast(1/base, -exp)
    result = 1
    while exp > 0:
        if exp % 2 == 1:      # odd: multiply base once
            result *= base
        base *= base           # square the base
        exp //= 2
    return result

# ================================================================
# PROBLEM 41: Modular exponentiation
# ================================================================
def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    (base^exp) % mod — O(log exp)

    INTERVIEW SCRIPT:
    "Same as fast power but apply modulo at each step.
     (a * b) % m = ((a % m) * (b % m)) % m
     This prevents integer overflow with huge numbers."
    """
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# ================================================================
# PROBLEM 42: Check power of 2
# ================================================================
def is_power_of_2(n: int) -> bool:
    """
    APPROACH 1: O(log n) — keep dividing by 2
    APPROACH 2: O(1) bit trick — n & (n-1) == 0

    INTERVIEW SCRIPT:
    "Power of 2 has exactly one bit set in binary.
     n & (n-1) clears the lowest set bit.
     If result is 0, only one bit was set."
    """
    return n > 0 and (n & (n - 1)) == 0

# ================================================================
# PROBLEM 43: Check power of 3
# ================================================================
def is_power_of_3_brute(n: int) -> bool:
    """APPROACH 1: O(log n) — keep dividing by 3"""
    if n <= 0: return False
    while n % 3 == 0:
        n //= 3
    return n == 1

def is_power_of_3_math(n: int) -> bool:
    """
    APPROACH 2: O(1) — largest power of 3 that fits in int

    INTERVIEW SCRIPT:
    "Largest 3^k that fits in 32-bit int is 3^19 = 1162261467.
     n is a power of 3 if and only if n divides 3^19."
    """
    return n > 0 and 1162261467 % n == 0

# ================================================================
# PROBLEM 44: Square root (binary search)
# ================================================================
def sqrt_brute(n: int) -> int:
    """APPROACH 1: O(√n) — linear search"""
    i = 0
    while (i+1) * (i+1) <= n:
        i += 1
    return i

def sqrt_binary_search(n: int) -> int:
    """
    APPROACH 2: O(log n) — binary search

    INTERVIEW SCRIPT:
    "Binary search for integer square root.
     Search space: [0, n]. For each mid: check if mid² ≤ n.
     Find largest mid such that mid² ≤ n."
    """
    if n < 2: return n
    left, right = 1, n // 2
    while left <= right:
        mid = (left + right) // 2
        if mid * mid == n:
            return mid
        elif mid * mid < n:
            left = mid + 1
        else:
            right = mid - 1
    return right

def sqrt_newton(n: int) -> float:
    """
    APPROACH 3: Newton's Method — O(log n) converges very fast

    INTERVIEW SCRIPT:
    "Newton's method: x_next = (x + n/x) / 2.
     Converges quadratically — each step doubles correct digits."
    """
    if n < 0: raise ValueError("Negative input")
    if n == 0: return 0
    x = n
    while True:
        x_next = (x + n / x) / 2
        if abs(x - x_next) < 1e-7:
            return x_next
        x = x_next

# ================================================================
# PROBLEM 45: Nth Fibonacci
# ================================================================
def fib_brute(n: int) -> int:
    """APPROACH 1: O(2^n) — naive recursion (NEVER use in interviews)"""
    if n <= 1: return n
    return fib_brute(n-1) + fib_brute(n-2)

def fib_dp(n: int) -> int:
    """APPROACH 2: O(n) time, O(1) space — space-optimized DP"""
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

def fib_matrix(n: int) -> int:
    """
    APPROACH 3: Matrix exponentiation — O(log n)

    INTERVIEW SCRIPT:
    "Using matrix:
     [F(n+1)]   [1 1]^n   [F(1)]
     [F(n)  ] = [1 0]   * [F(0)]
     Matrix exponentiation using fast power → O(log n)."
    """
    def mat_mul(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0],
                 A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0],
                 A[1][0]*B[0][1] + A[1][1]*B[1][1]]]

    def mat_pow(M, n):
        result = [[1, 0], [0, 1]]  # identity matrix
        while n > 0:
            if n % 2 == 1:
                result = mat_mul(result, M)
            M = mat_mul(M, M)
            n //= 2
        return result

    if n <= 1: return n
    M = [[1, 1], [1, 0]]
    return mat_pow(M, n)[0][1]

# ================================================================
# TEST ALL
# ================================================================
if __name__ == "__main__":
    print("=== MATHEMATICAL FORMULAS ===")
    print("31. Sum 1 to 100:", sum_n_formula(100))                    # 5050
    print("32. Sum squares 1 to 10:", sum_squares_formula(10))        # 385
    print("33. Sum cubes 1 to 5:", sum_cubes_formula(5))              # 225
    print("34. Missing in [1,2,4,5] n=5:", missing_number_sum([1,2,4,5], 5))  # 3
    print("35. Duplicate in [1,3,4,2,2]:", find_duplicate_sum([1,3,4,2,2], 5)) # 2
    print("36. AP sum a=1,d=2,n=5:", sum_ap(1, 2, 5))                # 25
    print("37. GP sum a=1,r=2,n=5:", sum_gp(1, 2, 5))                # 31
    print("38. Trailing zeros 100!:", trailing_zeros_factorial(100))  # 24
    print("39. Factorial 10:", factorial_iterative(10))                # 3628800
    print("40. Fast power 2^10:", power_fast(2, 10))                  # 1024
    print("41. Mod pow 2^10 mod 1000:", mod_pow(2, 10, 1000))        # 24
    print("42. Power of 2: 16:", is_power_of_2(16))                   # True
    print("43. Power of 3: 27:", is_power_of_3_brute(27))            # True
    print("44. Sqrt 144:", sqrt_binary_search(144))                   # 12
    print("45. Fib(10):", fib_dp(10))                                 # 55
    print("45. Fib(10) matrix:", fib_matrix(10))                      # 55
