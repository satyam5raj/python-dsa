"""
================================================================
MATH PROBLEMS 61-70: RECURSION BASICS
================================================================
"""

from typing import List

# ================================================================
# PROBLEM 61: Print 1 to n
# ================================================================
def print_1_to_n(n: int):
    """
    INTERVIEW SCRIPT:
    "Base case: n < 1, stop. Print small numbers first (recurse then print)."
    """
    if n < 1: return
    print_1_to_n(n - 1)  # recurse first
    print(n)              # print after return

# Or: print then recurse (different order)
def print_1_to_n_v2(n: int, curr: int = 1):
    if curr > n: return
    print(curr)
    print_1_to_n_v2(n, curr + 1)

# ================================================================
# PROBLEM 62: Print n to 1
# ================================================================
def print_n_to_1(n: int):
    """Print then recurse (print n first, then n-1, etc.)"""
    if n < 1: return
    print(n)
    print_n_to_1(n - 1)

# ================================================================
# PROBLEM 63: Sum of n numbers using recursion
# ================================================================
def sum_n_recursive(n: int) -> int:
    """
    APPROACH 1 (Brute/Recursive): O(n) time, O(n) space
    APPROACH 2 (Formula): O(1) — n*(n+1)/2

    INTERVIEW SCRIPT:
    "sum(n) = n + sum(n-1). Base: sum(0) = 0.
     Each call adds n and waits for sum(n-1)."
    """
    if n == 0: return 0
    return n + sum_n_recursive(n - 1)

# ================================================================
# PROBLEM 64: Factorial using recursion
# ================================================================
def factorial(n: int) -> int:
    """
    n! = n * (n-1)!
    Base: 0! = 1

    INTERVIEW SCRIPT:
    "Classic recursion. n! = n * (n-1)!
     O(n) time, O(n) space (call stack).
     For large n: prefer iterative to avoid stack overflow."
    """
    if n <= 1: return 1
    return n * factorial(n - 1)

# ================================================================
# PROBLEM 65: Fibonacci using recursion
# ================================================================
def fib_naive(n: int) -> int:
    """
    O(2^n) — NEVER use this in interviews without memoization!
    Shows what NOT to do.
    """
    if n <= 1: return n
    return fib_naive(n-1) + fib_naive(n-2)

def fib_memoized(n: int, memo: dict = None) -> int:
    """
    O(n) time, O(n) space — always use this

    INTERVIEW SCRIPT:
    "Memoize results to avoid recomputation.
     Without memo: O(2^n). With memo: O(n)."
    """
    if memo is None: memo = {}
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib_memoized(n-1, memo) + fib_memoized(n-2, memo)
    return memo[n]

from functools import lru_cache

@lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    """Pythonic way with lru_cache"""
    if n <= 1: return n
    return fib_lru(n-1) + fib_lru(n-2)

# ================================================================
# PROBLEM 66: Power (a^n) using recursion
# ================================================================
def power_brute(a: float, n: int) -> float:
    """APPROACH 1 (Linear): O(n) — multiply n times"""
    if n == 0: return 1
    return a * power_brute(a, n - 1)

def power_fast(a: float, n: int) -> float:
    """
    APPROACH 2 (Fast Power): O(log n)

    INTERVIEW SCRIPT:
    "Divide exponent in half each time.
     a^n = (a^(n/2))^2 if n is even.
     a^n = a * (a^(n/2))^2 if n is odd."
    """
    if n == 0: return 1
    if n < 0: return power_fast(1/a, -n)
    half = power_fast(a, n // 2)
    if n % 2 == 0:
        return half * half
    return a * half * half

# ================================================================
# PROBLEM 67: Reverse number using recursion
# ================================================================
def reverse_number_recursive(n: int, rev: int = 0) -> int:
    """
    Tail-recursive style.
    Extract last digit, build reversed number.

    INTERVIEW SCRIPT:
    "Extract last digit n%10. Shift current reverse left: rev*10 + digit.
     Reduce n by dividing by 10. Base: n=0."
    """
    if n == 0: return rev
    return reverse_number_recursive(n // 10, rev * 10 + n % 10)

# ================================================================
# PROBLEM 68: Sum of digits using recursion
# ================================================================
def sum_digits_recursive(n: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Last digit: n%10. Sum of rest: sum_digits(n//10).
     Base: single digit, return as-is."
    """
    n = abs(n)
    if n < 10: return n
    return n % 10 + sum_digits_recursive(n // 10)

# ================================================================
# PROBLEM 69: GCD using recursion (Euclidean)
# ================================================================
def gcd_recursive(a: int, b: int) -> int:
    """
    Euclidean Algorithm — O(log min(a,b))

    INTERVIEW SCRIPT:
    "gcd(a,b) = gcd(b, a%b).
     Base: gcd(a,0) = a.
     Proof: gcd(a,b) divides a and b → divides a-b → divides a mod b."
    """
    if b == 0: return a
    return gcd_recursive(b, a % b)

# ================================================================
# PROBLEM 70: Tower of Hanoi
# ================================================================
def tower_of_hanoi(n: int, source: str = 'A', destination: str = 'C', auxiliary: str = 'B') -> int:
    """
    Move n disks from source to destination using auxiliary.
    Minimum moves = 2^n - 1

    INTERVIEW SCRIPT:
    "Recursive decomposition:
     1. Move n-1 disks from source to auxiliary (using destination).
     2. Move disk n from source to destination (direct).
     3. Move n-1 disks from auxiliary to destination (using source).

     T(n) = 2*T(n-1) + 1 = 2^n - 1 total moves.

     WHY this is minimal? Each move is necessary — you can prove
     you need at least 2^n - 1 moves by induction."
    """
    if n == 1:
        print(f"Move disk 1: {source} → {destination}")
        return 1
    moves = 0
    moves += tower_of_hanoi(n-1, source, auxiliary, destination)
    print(f"Move disk {n}: {source} → {destination}")
    moves += 1
    moves += tower_of_hanoi(n-1, auxiliary, destination, source)
    return moves

# ================================================================
# VISUALIZING RECURSION — THE CALL TREE
# ================================================================
def visualize_fibonacci_calls(n: int, depth: int = 0) -> int:
    """Shows the exponential call tree of naive Fibonacci"""
    indent = "  " * depth
    print(f"{indent}fib({n}) called")
    if n <= 1:
        print(f"{indent}fib({n}) = {n} (base case)")
        return n
    left = visualize_fibonacci_calls(n-1, depth+1)
    right = visualize_fibonacci_calls(n-2, depth+1)
    result = left + right
    print(f"{indent}fib({n}) = {result}")
    return result

# ================================================================
# TEST ALL
# ================================================================
if __name__ == "__main__":
    print("=== RECURSION BASICS ===")
    print("61. Print 1 to 5:"); print_1_to_n(5)
    print("62. Print 5 to 1:"); print_n_to_1(5)
    print("63. Sum 1..5 recursive:", sum_n_recursive(5))            # 15
    print("64. Factorial(6):", factorial(6))                         # 720
    print("65. Fibonacci(10) memoized:", fib_memoized(10))           # 55
    print("66. Power 2^10 fast:", power_fast(2, 10))                 # 1024
    print("67. Reverse 12345:", reverse_number_recursive(12345))     # 54321
    print("68. Sum digits 12345:", sum_digits_recursive(12345))      # 15
    print("69. GCD(48,18):", gcd_recursive(48, 18))                  # 6
    print("70. Tower of Hanoi (3 disks):")
    moves = tower_of_hanoi(3)
    print(f"Total moves: {moves}")                                     # 7
