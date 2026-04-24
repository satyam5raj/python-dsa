"""
================================================================
TOPIC 4: RECURSION
================================================================
Foundation for: DFS, Trees, Backtracking, DP, Divide & Conquer

INTERVIEW COMMUNICATION:
"I'll use recursion here. Let me identify:
 1. Base case — when to stop
 2. Recursive case — how to break down the problem
 3. Trust the recursion — assume smaller subproblem works"
================================================================
"""

from typing import List

# ================================================================
# FUNDAMENTALS — HOW RECURSION WORKS
# ================================================================
"""
Call Stack Visualization for factorial(4):
factorial(4)
  → factorial(3)
      → factorial(2)
          → factorial(1)  ← BASE CASE returns 1
          ← returns 1
      ← returns 2*1 = 2
  ← returns 3*2 = 6
← returns 4*6 = 24

Key: Each call waits for its sub-calls to complete (LIFO stack)
"""

# ================================================================
# BASIC RECURSION PATTERNS
# ================================================================

def factorial(n: int) -> int:
    """
    n! = n * (n-1) * ... * 1
    Time: O(n), Space: O(n) call stack

    INTERVIEW SCRIPT:
    "Base case: factorial(0) = 1.
     Recursive case: factorial(n) = n * factorial(n-1).
     Stack depth is n → O(n) space."
    """
    if n == 0:  # base case
        return 1
    return n * factorial(n - 1)  # recursive case

def fibonacci(n: int) -> int:
    """
    Naive recursive Fibonacci — O(2ⁿ) time (AVOID in interviews)
    Shows the PROBLEM with naive recursion: redundant computation
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # two branches!

def fibonacci_optimized(n: int, memo: dict = {}) -> int:
    """
    Memoized Fibonacci — O(n) time, O(n) space
    ALWAYS prefer this over naive recursive

    INTERVIEW SCRIPT:
    "Naive Fibonacci is O(2ⁿ) due to recomputation.
     Memoization caches results → each subproblem solved once.
     O(n) time and space."
    """
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_optimized(n-1, memo) + fibonacci_optimized(n-2, memo)
    return memo[n]

# ================================================================
# DIVIDE & CONQUER PATTERN
# ================================================================
"""
PATTERN: Divide problem into smaller subproblems,
         solve recursively, combine results

Steps:
1. Divide: Split into smaller subproblems
2. Conquer: Solve recursively
3. Combine: Merge solutions
"""

def binary_search_recursive(arr: List[int], target: int, left: int = 0, right: int = None) -> int:
    """
    Recursive binary search — O(log n) time, O(log n) space

    INTERVIEW SCRIPT:
    "Divide: check middle element.
     If target found: return index.
     If target < mid: recurse on left half.
     If target > mid: recurse on right half.
     Base case: left > right means not found."
    """
    if right is None:
        right = len(arr) - 1
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

def merge_sort(arr: List[int]) -> List[int]:
    """
    Classic divide & conquer sorting — O(n log n) time, O(n) space

    INTERVIEW SCRIPT:
    "Divide array in half recursively until size 1.
     Merge sorted halves by comparing element by element.
     Merge step: O(n). Recursion depth: O(log n). Total: O(n log n)."
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # divide
    right = merge_sort(arr[mid:])  # divide
    return _merge(left, right)     # combine

def _merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def power(base: float, exp: int) -> float:
    """
    Fast power using divide & conquer — O(log n) time
    Better than O(n) iterative multiplication

    INTERVIEW SCRIPT:
    "base^exp = base^(exp//2) * base^(exp//2) if even.
     If odd, multiply one extra base.
     This halves the exponent each time → O(log n)."
    """
    if exp == 0:
        return 1
    if exp < 0:
        return 1 / power(base, -exp)
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    return base * power(base, exp - 1)

# ================================================================
# TREE-LIKE RECURSION (multiple branches)
# ================================================================

def count_paths(n: int, m: int) -> int:
    """
    Count paths in n×m grid moving only right or down.
    SHOWS tree-like recursion — each call branches into 2

    INTERVIEW SCRIPT:
    "At each cell, I can go right or down.
     count_paths(n,m) = count_paths(n-1,m) + count_paths(n,m-1)
     Base case: if at row 1 or col 1, only 1 path exists."
    """
    if n == 1 or m == 1:
        return 1
    return count_paths(n - 1, m) + count_paths(n, m - 1)

def count_paths_memo(n: int, m: int, memo: dict = {}) -> int:
    """Same but memoized — O(n*m) time vs O(2^(n+m)) naive"""
    if (n, m) in memo:
        return memo[(n, m)]
    if n == 1 or m == 1:
        return 1
    memo[(n, m)] = count_paths_memo(n-1, m, memo) + count_paths_memo(n, m-1, memo)
    return memo[(n, m)]

# ================================================================
# RECURSION ON STRINGS
# ================================================================

def reverse_string_recursive(s: str) -> str:
    """
    Reverse string recursively — O(n) time, O(n) space

    INTERVIEW SCRIPT:
    "First char goes to end. Reverse rest recursively."
    """
    if len(s) <= 1:
        return s
    return reverse_string_recursive(s[1:]) + s[0]

def is_palindrome_recursive(s: str) -> bool:
    """
    Check palindrome recursively

    INTERVIEW SCRIPT:
    "Palindrome: first == last, and middle is also palindrome."
    """
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome_recursive(s[1:-1])

def sum_of_digits(n: int) -> int:
    """Sum of digits recursively"""
    if n < 10:
        return n
    return n % 10 + sum_of_digits(n // 10)

# ================================================================
# TOWER OF HANOI — Classic recursion problem
# ================================================================

def tower_of_hanoi(n: int, source: str, destination: str, auxiliary: str) -> int:
    """
    Move n disks from source to destination using auxiliary peg.
    Minimum moves required: 2ⁿ - 1

    INTERVIEW SCRIPT:
    "Classic recursive problem. To move n disks:
     1. Move n-1 disks from source to auxiliary (recursively)
     2. Move disk n from source to destination (base step)
     3. Move n-1 disks from auxiliary to destination (recursively)
     Base case: 1 disk — just move it directly.
     Minimum moves = 2ⁿ - 1."
    """
    if n == 1:
        print(f"Move disk 1 from {source} to {destination}")
        return 1

    moves = 0
    moves += tower_of_hanoi(n - 1, source, auxiliary, destination)
    print(f"Move disk {n} from {source} to {destination}")
    moves += 1
    moves += tower_of_hanoi(n - 1, auxiliary, destination, source)
    return moves

# ================================================================
# GCD — EUCLIDEAN ALGORITHM (Recursive)
# ================================================================

def gcd(a: int, b: int) -> int:
    """
    GCD using Euclidean algorithm — O(log min(a,b)) time

    KEY: gcd(a, b) = gcd(b, a % b)
    When b = 0, gcd = a

    INTERVIEW SCRIPT:
    "Euclidean algorithm: gcd(a,b) = gcd(b, a mod b).
     Why? Because any divisor of a and b also divides a mod b.
     Terminates because b decreases each step.
     O(log min(a,b)) — extremely fast."
    """
    if b == 0:
        return a
    return gcd(b, a % b)

def lcm(a: int, b: int) -> int:
    return (a * b) // gcd(a, b)

# ================================================================
# RECURSION vs ITERATION COMPARISON
# ================================================================
"""
WHEN TO USE RECURSION:
✅ Tree/graph problems (natural recursive structure)
✅ Divide & conquer (merge sort, binary search)
✅ Backtracking (explore all paths)
✅ Problem has overlapping subproblems (→ use memoization)

WHEN TO PREFER ITERATION:
✅ Simple loops (sum, factorial with large n)
✅ Risk of stack overflow (n > 10000)
✅ Performance critical (function call overhead)

TAIL RECURSION NOTE:
Python does NOT optimize tail recursion.
Default recursion limit: sys.getrecursionlimit() = 1000
"""

import sys

def increase_recursion_limit():
    """Call this if you need deep recursion in Python"""
    sys.setrecursionlimit(10000)

# ================================================================
# CALL STACK ANALYSIS
# ================================================================

def analyze_stack_depth(n: int, depth: int = 0):
    """Shows how recursion depth builds the call stack"""
    print(f"  {'  ' * depth}→ call with n={n} (depth={depth})")
    if n == 0:
        print(f"  {'  ' * depth}← BASE CASE")
        return 0
    result = n + analyze_stack_depth(n - 1, depth + 1)
    print(f"  {'  ' * depth}← returning {result}")
    return result

if __name__ == "__main__":
    print("Factorial(5):", factorial(5))
    print("Fibonacci(10) memoized:", fibonacci_optimized(10))
    print("Power(2, 10):", power(2, 10))
    print("GCD(48, 18):", gcd(48, 18))
    print("LCM(4, 6):", lcm(4, 6))
    print("Merge sort [3,1,4,1,5,9]:", merge_sort([3, 1, 4, 1, 5, 9]))
    print("\nTower of Hanoi (3 disks):")
    moves = tower_of_hanoi(3, "A", "C", "B")
    print(f"Total moves: {moves}")

    print("\nCall stack analysis for n=3:")
    analyze_stack_depth(3)
