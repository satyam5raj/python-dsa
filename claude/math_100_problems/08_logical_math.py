"""
================================================================
MATH PROBLEMS 91-100: LOGICAL MATH PROBLEMS
================================================================
"""

from typing import List

# ================================================================
# PROBLEM 91: Josephus problem
# ================================================================
def josephus_brute(n: int, k: int) -> int:
    """
    n people in circle, every kth person eliminated. Find survivor.

    APPROACH 1 (Simulation): O(n²) using list removal
    """
    people = list(range(1, n+1))
    idx = 0
    while len(people) > 1:
        idx = (idx + k - 1) % len(people)
        people.pop(idx)
    return people[0]

def josephus_dp(n: int, k: int) -> int:
    """
    APPROACH 2 (DP): O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Classic DP: J(1,k) = 0.
     J(n,k) = (J(n-1,k) + k) % n (0-indexed).
     Add 1 for 1-indexed result.
     WHY: after removing kth person, remaining n-1 people
     form a new problem with shifted indices."
    """
    survivor = 0  # 0-indexed
    for i in range(2, n+1):
        survivor = (survivor + k) % i
    return survivor + 1  # 1-indexed

# ================================================================
# PROBLEM 92: Water jug problem
# ================================================================
def water_jug(m: int, n: int, d: int) -> bool:
    """
    Can we measure exactly d liters with two jugs of capacity m and n?

    INTERVIEW SCRIPT:
    "Using Bezout's identity: we can measure d liters if and only if
     d is divisible by GCD(m, n) AND d <= max(m, n).
     WHY: all achievable amounts are multiples of GCD(m,n)."
    """
    def gcd(a, b):
        while b: a, b = b, a % b
        return a

    return d <= max(m, n) and d % gcd(m, n) == 0

def water_jug_bfs(m: int, n: int, d: int) -> bool:
    """
    BFS simulation — find all reachable states

    INTERVIEW SCRIPT:
    "State = (amount_in_jug1, amount_in_jug2).
     BFS from (0,0). At each state, try 6 operations:
     fill jug1, fill jug2, empty jug1, empty jug2,
     pour jug1→jug2, pour jug2→jug1."
    """
    from collections import deque
    visited = set()
    queue = deque([(0, 0)])
    visited.add((0, 0))

    while queue:
        a, b = queue.popleft()
        if a == d or b == d:
            return True
        next_states = [
            (m, b), (a, n),         # fill jug1, fill jug2
            (0, b), (a, 0),         # empty jug1, empty jug2
            (min(a+b, m), max(0, a+b-m)),  # pour jug2 → jug1
            (max(0, a+b-n), min(a+b, n))   # pour jug1 → jug2
        ]
        for state in next_states:
            if state not in visited:
                visited.add(state)
                queue.append(state)
    return False

# ================================================================
# PROBLEM 93: Happy number
# ================================================================
def is_happy_number(n: int) -> bool:
    """
    Happy number: repeated sum of squared digits → 1.
    Non-happy numbers enter a cycle.

    APPROACH 1 (Set): O(n) space to detect cycle
    APPROACH 2 (Floyd's): O(1) space

    INTERVIEW SCRIPT:
    "Compute sum of squared digits repeatedly.
     If reaches 1: happy. If cycles: not happy.
     Use Floyd's cycle detection for O(1) space."
    """
    def digit_sq_sum(n):
        total = 0
        while n:
            d = n % 10
            total += d * d
            n //= 10
        return total

    # Floyd's two pointers
    slow = n
    fast = digit_sq_sum(n)
    while fast != 1 and slow != fast:
        slow = digit_sq_sum(slow)
        fast = digit_sq_sum(digit_sq_sum(fast))
    return fast == 1

# ================================================================
# PROBLEM 94: Digital root
# ================================================================
def digital_root_brute(n: int) -> int:
    """
    APPROACH 1: Repeatedly sum digits until single digit.
    O(log n * d) where d = digits
    """
    while n >= 10:
        total = 0
        while n:
            total += n % 10
            n //= 10
        n = total
    return n

def digital_root_formula(n: int) -> int:
    """
    APPROACH 2: O(1) formula!

    INTERVIEW SCRIPT:
    "Digital root formula:
     If n == 0: 0
     If n % 9 == 0: 9
     Else: n % 9
     WHY: digit sum ≡ n (mod 9) — property of decimal system."
    """
    if n == 0: return 0
    return 9 if n % 9 == 0 else n % 9

# ================================================================
# PROBLEM 95: Count trailing zeros in n!
# ================================================================
def count_trailing_zeros(n: int) -> int:
    """
    Count trailing zeros in n!
    O(log n)

    INTERVIEW SCRIPT:
    "Trailing zeros come from 10 = 2×5. More 2s than 5s always.
     Count multiples of 5: ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + ...
     WHY: 25 contributes TWO factors of 5, 125 contributes three, etc."
    """
    count = 0
    p = 5
    while p <= n:
        count += n // p
        p *= 5
    return count

# ================================================================
# PROBLEM 96: Check automorphic number
# ================================================================
def is_automorphic(n: int) -> bool:
    """
    Automorphic: n² ends with n.
    Examples: 5² = 25 (ends with 5) ✓, 6² = 36 (ends with 6) ✓, 76² = 5776 ✓

    INTERVIEW SCRIPT:
    "Compute n². Check if n² mod 10^(digits of n) == n."
    """
    square = n * n
    temp = n
    while temp:
        if square % 10 != temp % 10:
            return False
        square //= 10
        temp //= 10
    return True

# ================================================================
# PROBLEM 97: Check Harshad number
# ================================================================
def is_harshad(n: int) -> bool:
    """
    Harshad (Niven) number: divisible by sum of its digits.
    Examples: 18 (1+8=9, 18÷9=2) ✓, 12 (1+2=3, 12÷3=4) ✓

    INTERVIEW SCRIPT:
    "Compute digit sum. Check if n is divisible by it."
    """
    digit_sum = sum(int(d) for d in str(n))
    return n % digit_sum == 0

# ================================================================
# PROBLEM 98: Find nth magic number
# ================================================================
def nth_magic_number(n: int) -> int:
    """
    Magic number: sum of powers of 5 based on binary of n.
    Nth magic number = sum of 5^i for each set bit i in n.

    Pattern: 1→5, 2→25, 3→30(5+25), 4→125, 5→130(5+125), ...

    INTERVIEW SCRIPT:
    "Each bit in n corresponds to a power of 5.
     Bit 0 = 5^1, Bit 1 = 5^2, Bit 2 = 5^3, etc.
     Check each bit of n and add corresponding power."
    """
    power = 5
    result = 0
    while n:
        if n & 1:
            result += power
        n >>= 1
        power *= 5
    return result

# ================================================================
# PROBLEM 99: Gray code generation
# ================================================================
def gray_code(n: int) -> List[int]:
    """
    Generate n-bit Gray code.
    Each consecutive code differs by exactly 1 bit.

    APPROACH 1 (Formula): gray(i) = i ^ (i >> 1)
    APPROACH 2 (Recursive): mirror and prefix 0/1

    INTERVIEW SCRIPT:
    "Gray code formula: for number i, gray(i) = i XOR (i >> 1).
     WHY: XOR with right shift creates single-bit differences.
     Recursive: G(n) = {0 + G(n-1)} ∪ {1 + reverse(G(n-1))}"
    """
    # Formula approach
    codes = [i ^ (i >> 1) for i in range(1 << n)]
    return codes

def gray_code_recursive(n: int) -> List[int]:
    """Recursive: mirror approach"""
    if n == 1:
        return [0, 1]
    prev = gray_code_recursive(n - 1)
    return prev + [x | (1 << (n-1)) for x in reversed(prev)]

def gray_to_binary(gray: int) -> int:
    """Convert Gray code back to binary"""
    binary = gray
    while gray:
        gray >>= 1
        binary ^= gray
    return binary

# ================================================================
# PROBLEM 100: Catalan number
# ================================================================
def catalan_brute(n: int) -> int:
    """
    APPROACH 1: Recursive formula — O(3^n) without memoization
    C(0) = 1, C(n) = sum(C(i)*C(n-i-1)) for i=0..n-1
    """
    if n <= 1: return 1
    result = 0
    for i in range(n):
        result += catalan_brute(i) * catalan_brute(n-1-i)
    return result

def catalan_dp(n: int) -> int:
    """
    APPROACH 2: DP — O(n²)

    INTERVIEW SCRIPT:
    "Catalan numbers: C(n) = C(0)*C(n-1) + C(1)*C(n-2) + ... + C(n-1)*C(0)
     These count: valid parentheses, BSTs, monotone paths, etc.
     DP builds from C(0) up to C(n)."
    """
    dp = [0] * (n+1)
    dp[0] = dp[1] = 1
    for i in range(2, n+1):
        for j in range(i):
            dp[i] += dp[j] * dp[i-1-j]
    return dp[n]

def catalan_formula(n: int) -> int:
    """
    APPROACH 3: O(n) direct formula
    C(n) = C(2n, n) / (n+1) = (2n)! / ((n+1)! * n!)
    """
    from math import comb
    return comb(2*n, n) // (n+1)

def catalan_applications():
    """
    INTERVIEW SCRIPT:
    "Catalan numbers count:
     - Number of valid parenthesizations of n+1 factors
     - Number of full binary trees with n+1 leaves
     - Number of BSTs with n keys
     - Number of monotone lattice paths (Dyck paths)
     - Number of triangulations of (n+2)-gon
     First few: 1, 1, 2, 5, 14, 42, 132, 429..."
    """
    print("Catalan numbers C(0..10):", [catalan_formula(i) for i in range(11)])

# ================================================================
# TEST ALL
# ================================================================
if __name__ == "__main__":
    print("=== LOGICAL MATH PROBLEMS ===")
    print("91. Josephus(7,3):", josephus_dp(7, 3))                  # 4
    print("91. Josephus simulation(7,3):", josephus_brute(7, 3))     # 4
    print("92. Water jug(3,5,4):", water_jug(3, 5, 4))               # True
    print("92. Water jug BFS(3,5,4):", water_jug_bfs(3, 5, 4))      # True
    print("93. Happy number 19:", is_happy_number(19))               # True
    print("93. Happy number 4:", is_happy_number(4))                  # False
    print("94. Digital root 493:", digital_root_formula(493))        # 7
    print("95. Trailing zeros 100!:", count_trailing_zeros(100))     # 24
    print("96. Automorphic 5:", is_automorphic(5))                   # True
    print("96. Automorphic 76:", is_automorphic(76))                 # True
    print("97. Harshad 18:", is_harshad(18))                         # True
    print("98. 5th magic number:", nth_magic_number(5))              # 130
    print("99. Gray code n=3:", gray_code(3))
    print("100. Catalan n=5:", catalan_formula(5))                   # 42
    catalan_applications()
