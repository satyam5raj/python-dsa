"""
================================================================
MATH PROBLEMS 16-30: PRIME & DIVISIBILITY
================================================================
"""

from typing import List

# ================================================================
# PROBLEM 16: Check prime
# ================================================================
def is_prime_brute(n: int) -> bool:
    """
    APPROACH 1 (Brute): O(n) — check all divisors 2..n-1
    """
    if n < 2: return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def is_prime_optimal(n: int) -> bool:
    """
    APPROACH 2: O(√n) — only check up to √n

    INTERVIEW SCRIPT:
    "If n has a factor greater than √n, it also has one less than √n.
     So we only need to check up to √n.
     Special cases: 2 is prime, even numbers > 2 are not.
     Then check only odd numbers from 3 to √n."
    """
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# ================================================================
# PROBLEM 17: Print primes in range
# ================================================================
def primes_in_range_brute(l: int, r: int) -> List[int]:
    """O(n * √n) — check each number in range"""
    return [n for n in range(l, r+1) if is_prime_optimal(n)]

def primes_in_range_sieve(l: int, r: int) -> List[int]:
    """
    APPROACH 2: Sieve of Eratosthenes — O(r log log r)
    Better for ranges starting near 0.
    """
    sieve = sieve_of_eratosthenes(r)
    return [n for n in range(max(l, 2), r+1) if sieve[n]]

# ================================================================
# PROBLEM 18: Count primes ≤ n
# ================================================================
def count_primes(n: int) -> int:
    """
    Count primes less than n using Sieve of Eratosthenes.
    O(n log log n) time, O(n) space

    INTERVIEW SCRIPT:
    "Sieve: start with all True, mark multiples of each prime as False.
     Start sieving from p² (all smaller multiples already marked)."
    """
    if n <= 2: return 0
    sieve = [True] * n
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n, i):  # start from i² !
                sieve[j] = False
    return sum(sieve)

# ================================================================
# PROBLEM 19: Prime factors of n
# ================================================================
def prime_factors_brute(n: int) -> List[int]:
    """
    APPROACH 1: O(n) — trial division by all numbers
    """
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def prime_factors_optimal(n: int) -> List[int]:
    """
    APPROACH 2: O(√n) — trial division optimized

    INTERVIEW SCRIPT:
    "Divide out 2s first, then check only odd numbers.
     After the loop, if n > 1, n itself is prime (remaining factor)."
    """
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 2:
        factors.append(n)
    return factors

# ================================================================
# PROBLEM 20: All divisors of n
# ================================================================
def all_divisors_brute(n: int) -> List[int]:
    """APPROACH 1: O(n) — check all numbers 1..n"""
    return [i for i in range(1, n+1) if n % i == 0]

def all_divisors_optimal(n: int) -> List[int]:
    """
    APPROACH 2: O(√n) — divisors come in pairs

    INTERVIEW SCRIPT:
    "For each i up to √n: if i divides n, both i and n/i are divisors.
     Careful with perfect squares: n/i == i (don't add twice)."
    """
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

# ================================================================
# PROBLEM 21: Count divisors
# ================================================================
def count_divisors(n: int) -> int:
    """O(√n) — count pairs"""
    count = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            count += 2 if i != n // i else 1
    return count

# ================================================================
# PROBLEM 22: Check perfect number
# ================================================================
"""
Perfect number: sum of proper divisors (excluding itself) equals n.
Examples: 6 = 1+2+3, 28 = 1+2+4+7+14
"""
def is_perfect(n: int) -> bool:
    """
    INTERVIEW SCRIPT:
    "Sum all divisors except n itself. Check if equal to n.
     Use O(√n) divisor finding."
    """
    if n <= 1: return False
    divisor_sum = 1  # 1 is always a divisor
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisor_sum += i
            if i != n // i:
                divisor_sum += n // i
    return divisor_sum == n

# ================================================================
# PROBLEM 23: Check coprime (GCD = 1)
# ================================================================
def are_coprime(a: int, b: int) -> bool:
    """Two numbers are coprime if their GCD is 1"""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    return gcd(a, b) == 1

# ================================================================
# PROBLEM 24: GCD of two numbers
# ================================================================
def gcd_brute(a: int, b: int) -> int:
    """APPROACH 1: O(min(a,b)) — check all numbers"""
    for i in range(min(a, b), 0, -1):
        if a % i == 0 and b % i == 0:
            return i
    return 1

def gcd_euclidean(a: int, b: int) -> int:
    """
    APPROACH 2: Euclidean Algorithm — O(log min(a,b))

    INTERVIEW SCRIPT:
    "gcd(a,b) = gcd(b, a mod b).
     Base: gcd(a,0) = a.
     This is optimal — O(log min(a,b)) steps."
    """
    while b:
        a, b = b, a % b
    return a

# ================================================================
# PROBLEM 25: LCM of two numbers
# ================================================================
def lcm(a: int, b: int) -> int:
    """
    LCM = a * b / GCD(a, b)

    INTERVIEW SCRIPT:
    "Use the identity: LCM(a,b) * GCD(a,b) = a * b.
     So LCM = (a // GCD) * b to avoid overflow."
    """
    return (a // gcd_euclidean(a, b)) * b

# ================================================================
# PROBLEM 26: GCD of array
# ================================================================
def gcd_array(arr: List[int]) -> int:
    """
    GCD(a, b, c) = GCD(GCD(a, b), c) — property of GCD
    O(n log m) where m = max element
    """
    result = arr[0]
    for num in arr[1:]:
        result = gcd_euclidean(result, num)
    return result

# ================================================================
# PROBLEM 27: LCM of array
# ================================================================
def lcm_array(arr: List[int]) -> int:
    """Similar to GCD of array"""
    result = arr[0]
    for num in arr[1:]:
        result = lcm(result, num)
    return result

# ================================================================
# PROBLEM 28: Sum of divisors
# ================================================================
def sum_of_divisors(n: int) -> int:
    """O(√n) — sum all divisors including n"""
    total = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total

# ================================================================
# PROBLEM 29: Largest prime factor
# ================================================================
def largest_prime_factor(n: int) -> int:
    """
    O(√n) — find prime factors, return largest

    INTERVIEW SCRIPT:
    "Divide out all small prime factors.
     What remains is the largest prime factor."
    """
    largest = -1
    while n % 2 == 0:
        largest = 2
        n //= 2
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            largest = i
            n //= i
    if n > 2:
        largest = n
    return largest

# ================================================================
# PROBLEM 30: Sieve of Eratosthenes
# ================================================================
def sieve_of_eratosthenes(limit: int) -> List[bool]:
    """
    Generate all primes up to limit.
    O(n log log n) time, O(n) space

    INTERVIEW SCRIPT:
    "Classic algorithm: mark all as prime, then for each prime p,
     mark all multiples of p (starting from p²) as composite.
     Why p²? All smaller multiples already marked by smaller primes."
    """
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            for multiple in range(p*p, limit+1, p):
                is_prime[multiple] = False
    return is_prime

def get_all_primes(limit: int) -> List[int]:
    """Return list of all primes up to limit"""
    sieve = sieve_of_eratosthenes(limit)
    return [i for i, v in enumerate(sieve) if v]

# ================================================================
# TEST ALL
# ================================================================
if __name__ == "__main__":
    print("=== PRIME & DIVISIBILITY ===")
    print("16. Is prime 17:", is_prime_optimal(17))                    # True
    print("16. Is prime 15:", is_prime_optimal(15))                    # False
    print("17. Primes in [10,30]:", primes_in_range_brute(10, 30))
    print("18. Count primes < 20:", count_primes(20))                  # 8
    print("19. Prime factors 84:", prime_factors_optimal(84))          # [2,2,3,7]
    print("20. All divisors 12:", all_divisors_optimal(12))            # [1,2,3,4,6,12]
    print("21. Count divisors 12:", count_divisors(12))                # 6
    print("22. Is perfect 6:", is_perfect(6))                          # True
    print("22. Is perfect 28:", is_perfect(28))                        # True
    print("23. Coprime 7,13:", are_coprime(7, 13))                    # True
    print("24. GCD 48,18:", gcd_euclidean(48, 18))                    # 6
    print("25. LCM 4,6:", lcm(4, 6))                                  # 12
    print("26. GCD array [4,8,12]:", gcd_array([4, 8, 12]))           # 4
    print("27. LCM array [4,6,8]:", lcm_array([4, 6, 8]))             # 24
    print("28. Sum divisors 12:", sum_of_divisors(12))                 # 28
    print("29. Largest prime factor 56:", largest_prime_factor(56))   # 7
    print("30. All primes ≤ 30:", get_all_primes(30))
