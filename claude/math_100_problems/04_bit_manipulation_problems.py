"""
================================================================
MATH PROBLEMS 46-60: BIT MANIPULATION
================================================================
"""

from typing import List

# ================================================================
# PROBLEM 46: Check even/odd using bit
# ================================================================
def is_even_bit(n: int) -> bool:
    """
    INTERVIEW SCRIPT:
    "Last bit of even number is 0, odd number is 1.
     n & 1 checks the last bit. O(1)."
    """
    return (n & 1) == 0

def is_odd_bit(n: int) -> bool:
    return (n & 1) == 1

# ================================================================
# PROBLEM 47: Count set bits (Hamming Weight)
# ================================================================
def count_set_bits_brute(n: int) -> int:
    """APPROACH 1: O(log n) — check each bit"""
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def count_set_bits_kernighan(n: int) -> int:
    """
    APPROACH 2: Brian Kernighan — O(k) where k = set bits

    INTERVIEW SCRIPT:
    "n & (n-1) removes the rightmost set bit each time.
     Count iterations until n becomes 0.
     Fastest when few bits are set."
    """
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count

def count_set_bits_builtin(n: int) -> int:
    """Python built-in: bin(n).count('1') or n.bit_count()"""
    return bin(n).count('1')

# ================================================================
# PROBLEM 48: Check power of 2 using bit
# ================================================================
def is_power_of_2_bit(n: int) -> bool:
    """
    INTERVIEW SCRIPT:
    "Power of 2 has exactly ONE bit set.
     n & (n-1) clears the lowest set bit.
     If n was power of 2: result = 0."
    """
    return n > 0 and (n & (n - 1)) == 0

# ================================================================
# PROBLEM 49: Find single number (XOR)
# ================================================================
def find_single_number(nums: List[int]) -> int:
    """
    Find element that appears once, all others appear twice.
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "XOR properties: a^a=0, a^0=a.
     XOR all numbers: duplicates cancel, single remains."
    """
    result = 0
    for num in nums:
        result ^= num
    return result

# ================================================================
# PROBLEM 50: Find two unique numbers
# ================================================================
def find_two_unique(nums: List[int]) -> List[int]:
    """
    Find two elements appearing once, all others appear twice.
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "XOR all → xor = a^b.
     a and b differ in at least one bit. Find rightmost differing bit.
     Divide into two groups by this bit.
     XOR each group → get a and b."
    """
    xor = 0
    for num in nums:
        xor ^= num

    diff_bit = xor & (-xor)  # rightmost set bit (where a and b differ)

    a = b = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num
    return sorted([a, b])

# ================================================================
# PROBLEM 51: Missing number using XOR
# ================================================================
def missing_number_xor(nums: List[int]) -> int:
    """
    Find missing in [0, n].
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "XOR all indices 0..n with all array values.
     Pairs cancel, only missing number remains."
    """
    xor = len(nums)
    for i, num in enumerate(nums):
        xor ^= i ^ num
    return xor

# ================================================================
# PROBLEM 52: Swap without temp variable
# ================================================================
def swap_xor(a: int, b: int) -> tuple:
    """
    XOR swap — no temp variable needed.

    INTERVIEW SCRIPT:
    "a ^= b makes a = a^b.
     b ^= a makes b = (a^b)^b = a (original a).
     a ^= b makes a = (a^b)^a = b (original b).
     Note: doesn't work if a and b are same variable!"
    """
    a ^= b   # a = a^b
    b ^= a   # b = b^(a^b) = a
    a ^= b   # a = (a^b)^a = b
    return a, b

# ================================================================
# PROBLEM 53: Turn off rightmost set bit
# ================================================================
def turn_off_rightmost_bit(n: int) -> int:
    """
    n & (n-1) turns off the rightmost set bit.
    Example: 1100 → 1000 (cleared rightmost 1 at position 2)

    INTERVIEW SCRIPT:
    "n-1 flips all bits from rightmost set bit downward.
     n & (n-1) keeps bits above rightmost set bit, clears the rest."
    """
    return n & (n - 1)

# ================================================================
# PROBLEM 54: Check ith bit set
# ================================================================
def is_ith_bit_set(n: int, i: int) -> bool:
    """
    Check if ith bit (0-indexed from right) is set.
    INTERVIEW SCRIPT:
    "Right shift n by i positions, check last bit: (n >> i) & 1"
    """
    return bool((n >> i) & 1)

# ================================================================
# PROBLEM 55: Set ith bit
# ================================================================
def set_ith_bit(n: int, i: int) -> int:
    """
    Set ith bit to 1 regardless of current value.
    n | (1 << i)
    """
    return n | (1 << i)

# ================================================================
# PROBLEM 56: Clear ith bit
# ================================================================
def clear_ith_bit(n: int, i: int) -> int:
    """
    Clear ith bit to 0.
    n & ~(1 << i)
    ~(1 << i) = ...111011... (all 1s except position i)
    """
    return n & ~(1 << i)

# ================================================================
# PROBLEM 57: Toggle ith bit
# ================================================================
def toggle_ith_bit(n: int, i: int) -> int:
    """
    Flip ith bit (0→1 or 1→0).
    n ^ (1 << i)

    INTERVIEW SCRIPT:
    "XOR with 1 at position i: 0^1=1, 1^1=0."
    """
    return n ^ (1 << i)

# ================================================================
# PROBLEM 58: Count bits from 1 to n
# ================================================================
def count_bits_range(n: int) -> List[int]:
    """
    Count set bits for each number 0..n.
    O(n) using DP

    INTERVIEW SCRIPT:
    "dp[i] = dp[i >> 1] + (i & 1).
     i >> 1 removes last bit (same number of other set bits).
     i & 1 is last bit."
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp

# ================================================================
# PROBLEM 59: Subsets using bit masking
# ================================================================
def all_subsets_bitmask(arr: List) -> List[List]:
    """
    Generate all 2^n subsets using bit masking.
    O(n * 2^n)

    INTERVIEW SCRIPT:
    "For n elements: integers 0 to 2^n-1 represent all subsets.
     Bit i being set means include arr[i].
     Example: n=3, mask=5=101 → {arr[0], arr[2]}"
    """
    n = len(arr)
    result = []
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = [arr[i] for i in range(n) if (mask >> i) & 1]
        result.append(subset)
    return result

# ================================================================
# PROBLEM 60: XOR of range [l, r]
# ================================================================
def xor_range(l: int, r: int) -> int:
    """
    XOR of all numbers from l to r.
    O(1) — uses the pattern of XOR from 0 to n.

    INTERVIEW SCRIPT:
    "xor(l..r) = xor(0..r) ^ xor(0..l-1).
     XOR from 0 to n follows a 4-cycle pattern:
     n%4==0: n, n%4==1: 1, n%4==2: n+1, n%4==3: 0."
    """
    def xor_to_n(n: int) -> int:
        rem = n % 4
        if rem == 0: return n
        if rem == 1: return 1
        if rem == 2: return n + 1
        return 0  # rem == 3

    return xor_to_n(r) ^ xor_to_n(l - 1)

# ================================================================
# BONUS: BIT TRICKS COLLECTION
# ================================================================
def bit_tricks_demo():
    n = 13  # binary: 1101

    print(f"n = {n} = {bin(n)}")
    print(f"n & 1 (last bit) = {n & 1}")                        # 1 (odd)
    print(f"n >> 1 (divide by 2) = {n >> 1}")                   # 6
    print(f"n << 1 (multiply by 2) = {n << 1}")                 # 26
    print(f"n & (n-1) (clear LSB) = {n & (n-1)}")               # 12 = 1100
    print(f"n & (-n) (isolate LSB) = {n & (-n)}")               # 1
    print(f"n | (n+1) (set bit after LSB) = {n | (n+1)}")       # 15 = 1111
    print(f"~n & (n+1) (next bit after set block) = {~n & (n+1)}")

# ================================================================
# TEST ALL
# ================================================================
if __name__ == "__main__":
    print("=== BIT MANIPULATION ===")
    print("46. Is even 14:", is_even_bit(14))                          # True
    print("47. Count set bits 7:", count_set_bits_kernighan(7))       # 3
    print("48. Power of 2: 64:", is_power_of_2_bit(64))              # True
    print("49. Single number [4,1,2,1,2]:", find_single_number([4,1,2,1,2])) # 4
    print("50. Two unique [1,2,1,3,2,5]:", find_two_unique([1,2,1,3,2,5])) # [3,5]
    print("51. Missing [3,0,1]:", missing_number_xor([3,0,1]))        # 2
    print("52. Swap 5,7:", swap_xor(5, 7))                           # (7, 5)
    print("53. Turn off LSB 12:", bin(turn_off_rightmost_bit(12)))   # 0b1000
    print("54. 3rd bit set in 12:", is_ith_bit_set(12, 3))           # True
    print("55. Set bit 2 in 9:", bin(set_ith_bit(9, 2)))             # 0b1101
    print("56. Clear bit 3 in 12:", bin(clear_ith_bit(12, 3)))       # 0b0100
    print("57. Toggle bit 1 in 12:", bin(toggle_ith_bit(12, 1)))     # 0b1111
    print("58. Count bits 0..5:", count_bits_range(5))               # [0,1,1,2,1,2]
    print("59. Subsets [1,2,3]:", all_subsets_bitmask([1,2,3]))
    print("60. XOR range [2,5]:", xor_range(2, 5))                   # 2^3^4^5 = 0

    print("\n--- Bit Tricks Demo ---")
    bit_tricks_demo()
