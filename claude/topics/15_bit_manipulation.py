"""
================================================================
TOPIC 15: BIT MANIPULATION
================================================================
Work directly with binary representations.
Extremely fast (single CPU instruction).

INTERVIEW COMMUNICATION:
"I notice this problem involves powers of 2 or unique numbers —
 bit manipulation can solve this in O(1) space elegantly.
 Let me think about the binary representation..."
================================================================
"""

from typing import List

# ================================================================
# BIT OPERATIONS CHEATSHEET
# ================================================================
"""
Operation        Syntax          Example (5=101, 3=011)
─────────────────────────────────────────────────────
AND              a & b           101 & 011 = 001 (1)
OR               a | b           101 | 011 = 111 (7)
XOR              a ^ b           101 ^ 011 = 110 (6)
NOT              ~a              ~101 = ...11111010 (-6 in 2's complement)
Left shift       a << k          101 << 1 = 1010 (10) — multiply by 2^k
Right shift      a >> k          101 >> 1 = 10 (2)  — divide by 2^k

XOR PROPERTIES (memorize these!):
  a ^ 0 = a          (XOR with 0 gives same)
  a ^ a = 0          (XOR with self gives 0)
  a ^ b = b ^ a      (commutative)
  (a ^ b) ^ c = a ^ (b ^ c)  (associative)

USEFUL TRICKS:
  Check if even:    n & 1 == 0
  Check if odd:     n & 1 == 1
  Check bit i:      (n >> i) & 1
  Set bit i:        n | (1 << i)
  Clear bit i:      n & ~(1 << i)
  Toggle bit i:     n ^ (1 << i)
  Turn off LSB:     n & (n - 1)
  Isolate LSB:      n & (-n)
  Check power of 2: n > 0 and (n & (n-1)) == 0
"""

# ================================================================
# BASIC BIT OPERATIONS
# ================================================================

def is_even(n: int) -> bool:
    return (n & 1) == 0

def is_odd(n: int) -> bool:
    return (n & 1) == 1

def check_bit(n: int, i: int) -> bool:
    """Check if ith bit is set"""
    return bool((n >> i) & 1)

def set_bit(n: int, i: int) -> int:
    """Set ith bit to 1"""
    return n | (1 << i)

def clear_bit(n: int, i: int) -> int:
    """Clear ith bit to 0"""
    return n & ~(1 << i)

def toggle_bit(n: int, i: int) -> int:
    """Toggle ith bit"""
    return n ^ (1 << i)

def turn_off_lsb(n: int) -> int:
    """Turn off lowest set bit (e.g., 1010 → 1000)"""
    return n & (n - 1)

def isolate_lsb(n: int) -> int:
    """Isolate lowest set bit (e.g., 1010 → 0010)"""
    return n & (-n)

# ================================================================
# COUNT SET BITS (Hamming Weight / popcount)
# ================================================================

def count_set_bits_linear(n: int) -> int:
    """O(log n) — shift and check each bit"""
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def count_set_bits_optimal(n: int) -> int:
    """
    O(number of set bits) — Brian Kernighan's Algorithm
    Repeatedly clear the lowest set bit.

    INTERVIEW SCRIPT:
    "n & (n-1) clears the lowest set bit each time.
     Count how many times until n = 0.
     O(k) where k = number of set bits."
    """
    count = 0
    while n:
        n &= (n - 1)  # clear lowest set bit
        count += 1
    return count

def count_bits_dp(n: int) -> List[int]:
    """
    Count bits for ALL numbers 0 to n — O(n)
    dp[i] = dp[i >> 1] + (i & 1)

    INTERVIEW SCRIPT:
    "dp[i] = dp[i/2] + last_bit.
     i/2 is i right-shifted by 1 (remove last bit).
     Last bit is i & 1."
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp

# ================================================================
# XOR PROBLEMS
# ================================================================

def single_number(nums: List[int]) -> int:
    """
    Find the one number that appears once (others appear twice).
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "XOR property: a ^ a = 0, a ^ 0 = a.
     XOR all numbers. Pairs cancel (a^a=0).
     Only the single number remains."

    USE CASE: Error detection, data integrity verification
    """
    result = 0
    for num in nums:
        result ^= num
    return result

def two_single_numbers(nums: List[int]) -> List[int]:
    """
    Find two numbers that appear once (others appear twice).
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "XOR all → get a^b (both unique numbers XORed).
     Find any set bit in a^b (differs between a and b).
     Use rightmost set bit: divide numbers into two groups.
     Group 1: bit is set, Group 2: bit is not set.
     XOR each group → get a and b separately."
    """
    xor = 0
    for num in nums:
        xor ^= num  # xor = a ^ b

    rightmost_bit = xor & (-xor)  # isolate rightmost set bit

    a = b = 0
    for num in nums:
        if num & rightmost_bit:
            a ^= num
        else:
            b ^= num
    return [a, b]

def missing_number_xor(nums: List[int]) -> int:
    """
    Find missing number in [0, n].
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "XOR all array elements AND indices 0 to n.
     Pairs that appear twice cancel.
     Only missing number remains."
    """
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result

def swap_without_temp(a: int, b: int):
    """Swap two numbers without a temporary variable"""
    a ^= b   # a = a ^ b
    b ^= a   # b = b ^ (a ^ b) = a
    a ^= b   # a = (a ^ b) ^ a = b
    return a, b

# ================================================================
# POWER OF 2 / POWERS
# ================================================================

def is_power_of_two(n: int) -> bool:
    """
    Check if n is a power of 2 in O(1).

    INTERVIEW SCRIPT:
    "Power of 2 in binary: exactly one bit set (e.g., 4=100, 8=1000).
     n & (n-1) clears lowest set bit.
     If n has only one bit: n & (n-1) == 0."
    """
    return n > 0 and (n & (n - 1)) == 0

def is_power_of_four(n: int) -> bool:
    """
    Power of 4: power of 2 AND that bit is at odd position (0, 2, 4...).
    0x55555555 = 01010101... (bits at even positions)
    """
    return n > 0 and (n & (n-1)) == 0 and (n & 0x55555555) != 0

# ================================================================
# SUBSET GENERATION USING BIT MASKING
# ================================================================

def generate_subsets_bitmask(arr: List) -> List[List]:
    """
    Generate all 2ⁿ subsets using bit masks.
    O(n * 2ⁿ)

    INTERVIEW SCRIPT:
    "For n elements: 2ⁿ subsets. Use integers 0 to 2ⁿ-1 as masks.
     Each bit in mask represents whether element is included.
     E.g., mask=5=101 → include elements at indices 0 and 2."

    USE CASE: Exhaustive search, power set generation
    """
    n = len(arr)
    result = []
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = [arr[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result

# ================================================================
# XOR RANGE QUERY
# ================================================================

def xor_range(l: int, r: int) -> int:
    """
    XOR of all numbers from l to r.
    Use: XOR(0..r) ^ XOR(0..l-1)

    INTERVIEW SCRIPT:
    "XOR from 0 to n follows a pattern:
     n%4==0: n
     n%4==1: 1
     n%4==2: n+1
     n%4==3: 0"
    """
    def xor_to_n(n):
        if n % 4 == 0: return n
        if n % 4 == 1: return 1
        if n % 4 == 2: return n + 1
        return 0

    return xor_to_n(r) ^ xor_to_n(l - 1)

# ================================================================
# SUM OF TWO INTEGERS WITHOUT + OPERATOR
# ================================================================

def get_sum(a: int, b: int) -> int:
    """
    Add a and b without + or -.
    O(1) — maximum 32 iterations

    INTERVIEW SCRIPT:
    "Use bit manipulation to simulate addition.
     XOR gives sum without carry.
     AND then shift left gives carry.
     Repeat until no carry."
    """
    mask = 0xFFFFFFFF  # 32 bits

    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry

    return a if b == 0 else a & mask  # handle overflow for Python

# ================================================================
# REVERSE BITS
# ================================================================

def reverse_bits(n: int) -> int:
    """Reverse bits of a 32-bit unsigned integer — O(1)"""
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

# ================================================================
# GRAY CODE
# ================================================================

def gray_code(n: int) -> List[int]:
    """
    Generate n-bit Gray code sequence.
    Each consecutive number differs by exactly 1 bit.
    O(2ⁿ)

    INTERVIEW SCRIPT:
    "Formula: gray(i) = i ^ (i >> 1).
     WHY: Gray code for i is obtained by XORing i with i/2."
    """
    return [i ^ (i >> 1) for i in range(1 << n)]

# ================================================================
# BIT MANIPULATION APPLICATIONS
# ================================================================

def find_duplicate_number(nums: List[int]) -> int:
    """
    Find duplicate using XOR: XOR 1..n with array.
    (Works if exactly one number appears twice)

    INTERVIEW SCRIPT:
    "XOR all values 1..n and all array elements.
     All non-duplicate numbers appear twice → cancel.
     Duplicate appears 3 times → XOR of 3 same = same.
     Wait, this gives the duplicate ^ unique... use variant."
    """
    xor = 0
    n = len(nums) - 1  # array has n+1 elements, values 1..n
    for i in range(1, n + 1):
        xor ^= i
    for num in nums:
        xor ^= num
    return xor

def max_xor(nums: List[int]) -> int:
    """
    Maximum XOR of two numbers in array.
    O(n log n) using trie on binary representations

    INTERVIEW SCRIPT:
    "Build binary trie from all numbers.
     For each number, greedily find its pair that maximizes XOR:
     At each bit, try to go opposite direction (maximize that bit)."
    """
    max_val = 0
    mask = 0
    for bit in range(31, -1, -1):
        mask |= (1 << bit)
        prefixes = {num & mask for num in nums}
        candidate = max_val | (1 << bit)
        for prefix in prefixes:
            if candidate ^ prefix in prefixes:
                max_val = candidate
                break
    return max_val

# ================================================================
# PRACTICAL USE CASES SUMMARY
# ================================================================
"""
Bit manipulation in real world:
1. Flags/permissions: Unix file permissions (rwx = 3 bits)
2. Bloom filters: Hash to bit positions
3. Feature flags: Bitmask of enabled features
4. Encryption: XOR cipher, cryptographic operations
5. Graphics: Pixel color manipulation
6. Networking: IP address masking (192.168.1.0/24)
7. Compression: Huffman uses bit-level encoding
8. Hardware: Low-level device control registers
"""

if __name__ == "__main__":
    print("is_even(4):", is_even(4))
    print("count_set_bits(7) [111]:", count_set_bits_optimal(7))
    print("count_bits_dp(5):", count_bits_dp(5))
    print("single_number [2,2,1]:", single_number([2,2,1]))
    print("two_single_numbers [1,2,1,3,2,5]:", two_single_numbers([1,2,1,3,2,5]))
    print("missing_number [3,0,1]:", missing_number_xor([3,0,1]))
    print("is_power_of_two(16):", is_power_of_two(16))
    print("subsets of [1,2,3]:", generate_subsets_bitmask([1,2,3]))
    print("gray_code(3):", gray_code(3))
    print("get_sum(3,5):", get_sum(3,5))
    print("reverse_bits(43261596):", reverse_bits(43261596))
