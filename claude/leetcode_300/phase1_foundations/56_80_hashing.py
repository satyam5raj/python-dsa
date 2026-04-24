"""
================================================================
LEETCODE PHASE 1 (Problems 56-80): HASHING
================================================================
"""

from typing import List
from collections import defaultdict, Counter

# ================================================================
# 56. GROUP ANAGRAMS (Medium)
# ================================================================
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    APPROACH 1: O(n * k log k) — sort each string as key
    APPROACH 2: O(n * k) — character count as key

    INTERVIEW SCRIPT:
    "Anagrams have the same sorted representation.
     Use sorted string as hash key. Group by key.
     Optimization: use char count tuple as key (O(k) not O(k log k))."
    """
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))          # O(k log k)
        # key = tuple(Counter(s)[c] for c in 'abcdefghijklmnopqrstuvwxyz')  # O(k)
        groups[key].append(s)
    return list(groups.values())

# Time: O(n*k log k), Space: O(n*k)

# ================================================================
# 57. TOP K FREQUENT ELEMENTS (Medium)
# ================================================================
def top_k_frequent_brute(nums: List[int], k: int) -> List[int]:
    """APPROACH 1: O(n log n) — count then sort"""
    return [x for x, _ in Counter(nums).most_common(k)]

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    APPROACH 2: O(n) — bucket sort

    INTERVIEW SCRIPT:
    "Count frequencies with hash map O(n).
     Bucket sort: buckets[freq] = list of elements with that freq.
     Max frequency = n, so n+1 buckets.
     Scan from highest bucket to get top k. Total O(n)."
    """
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)
    result = []
    for i in range(len(buckets)-1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k: return result
    return result

# Time: O(n), Space: O(n)

# ================================================================
# 58. LONGEST CONSECUTIVE SEQUENCE (Medium)
# ================================================================
def longest_consecutive_brute(nums: List[int]) -> int:
    """APPROACH 1: O(n log n) — sort"""
    if not nums: return 0
    nums = sorted(set(nums))
    max_len = curr = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1] + 1: curr += 1
        else: curr = 1
        max_len = max(max_len, curr)
    return max_len

def longest_consecutive(nums: List[int]) -> int:
    """
    APPROACH 2: O(n) — HashSet

    INTERVIEW SCRIPT:
    "Put all numbers in a set for O(1) lookup.
     For each number, only start counting if num-1 is NOT in set.
     (It's a sequence start, so count forward from there.)
     Each element is visited at most twice → O(n) total."
    """
    num_set = set(nums)
    max_len = 0
    for num in num_set:
        if num - 1 not in num_set:       # start of sequence
            curr = num
            length = 1
            while curr + 1 in num_set:
                curr += 1; length += 1
            max_len = max(max_len, length)
    return max_len

# Time: O(n), Space: O(n)

# ================================================================
# 59. SUBARRAY SUM EQUALS K (Medium)
# ================================================================
def subarray_sum_brute(nums: List[int], k: int) -> int:
    """APPROACH 1: O(n²)"""
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k: count += 1
    return count

def subarray_sum(nums: List[int], k: int) -> int:
    """
    APPROACH 2: O(n) — prefix sum + hashmap

    INTERVIEW SCRIPT:
    "prefix[j] - prefix[i] = k means subarray (i, j] sums to k.
     For each j, I want to find how many i have prefix[i] = prefix[j] - k.
     Use hash map counting prefix sums seen so far.
     Initialize with {0: 1} for empty prefix."
    """
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    curr_sum = count = 0
    for num in nums:
        curr_sum += num
        count += prefix_count[curr_sum - k]
        prefix_count[curr_sum] += 1
    return count

# Time: O(n), Space: O(n)

# ================================================================
# 60. HAPPY NUMBER (Easy)
# ================================================================
def is_happy(n: int) -> bool:
    """
    APPROACH 1: HashSet to detect cycle
    APPROACH 2: Floyd's cycle detection O(1) space

    INTERVIEW SCRIPT:
    "Sum of squared digits repeatedly. Reach 1 → happy. Cycle → not happy.
     Floyd's: slow=one step, fast=two steps. If fast==1: happy.
     If fast==slow (not 1): cycle detected."
    """
    def digit_sq_sum(n):
        total = 0
        while n:
            d = n % 10; total += d*d; n //= 10
        return total

    slow, fast = n, digit_sq_sum(n)
    while fast != 1 and slow != fast:
        slow = digit_sq_sum(slow)
        fast = digit_sq_sum(digit_sq_sum(fast))
    return fast == 1

# ================================================================
# 61. FIRST UNIQUE CHARACTER IN STRING (Easy)
# ================================================================
def first_uniq_char(s: str) -> int:
    """
    INTERVIEW SCRIPT:
    "Two passes: count frequencies, then find first with count 1.
     O(n) time, O(1) space (26 letters)."
    """
    count = Counter(s)
    for i, c in enumerate(s):
        if count[c] == 1: return i
    return -1

# ================================================================
# 62. INTERSECTION OF TWO ARRAYS II (Easy)
# ================================================================
def intersect(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    Include duplicates in result (unlike set intersection).

    APPROACH 1: O(n log n + m log m) — sort + two pointers
    APPROACH 2: O(n + m) — HashMap count

    INTERVIEW SCRIPT:
    "Count frequencies of nums1. For each num in nums2:
     if count > 0, add to result and decrement count.

     FOLLOW-UP: What if arrays are sorted? Two pointers O(1) space.
     What if one array much larger? Hash the smaller array."
    """
    count = Counter(nums1)
    result = []
    for num in nums2:
        if count[num] > 0:
            result.append(num)
            count[num] -= 1
    return result

# ================================================================
# 63. FIND ALL DUPLICATES IN ARRAY (Medium)
# ================================================================
def find_duplicates(nums: List[int]) -> List[int]:
    """
    Numbers in [1, n]. Each appears once or twice. O(1) extra space.

    INTERVIEW SCRIPT:
    "Use array as hash: for each num, negate nums[|num|-1].
     If already negative when we try to negate: it's a duplicate.
     O(n) time, O(1) space (excluding output)."
    """
    result = []
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            result.append(abs(num))
        else:
            nums[idx] = -nums[idx]
    return result

# ================================================================
# 64. ENCODE AND DECODE STRINGS (Medium)
# ================================================================
class Codec:
    """
    Encode list of strings to single string, decode back.
    Challenge: strings can contain any character including delimiter.

    INTERVIEW SCRIPT:
    "Use length-prefix encoding: '5#hello3#foo'.
     Encode: for each word, prepend 'len#word'.
     Decode: read length until '#', then read exactly that many chars.
     This handles any characters in strings including special ones."
    """
    def encode(self, strs: List[str]) -> str:
        return ''.join(f'{len(s)}#{s}' for s in strs)

    def decode(self, s: str) -> List[str]:
        result, i = [], 0
        while i < len(s):
            j = s.index('#', i)
            length = int(s[i:j])
            result.append(s[j+1:j+1+length])
            i = j + 1 + length
        return result

# ================================================================
# 65. DESIGN HASHMAP (Easy)
# ================================================================
class MyHashMap:
    """
    INTERVIEW SCRIPT:
    "Use array of buckets (linked list or array for each bucket).
     Hash function: key % size.
     Handle collisions with chaining (each bucket is a list of (k,v) pairs).
     Resize when load factor too high — but simplified version uses fixed size."
    """
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key): return key % self.size

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value); return
        self.buckets[idx].append((key, value))

    def get(self, key: int) -> int:
        for k, v in self.buckets[self._hash(key)]:
            if k == key: return v
        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        self.buckets[idx] = [(k,v) for k,v in self.buckets[idx] if k != key]

# ================================================================
# 66. COUNT PRIMES (Medium)
# ================================================================
def count_primes(n: int) -> int:
    """
    Count primes less than n — Sieve of Eratosthenes

    INTERVIEW SCRIPT:
    "Sieve: mark all as prime. For each prime p up to √n,
     mark multiples starting from p² as composite.
     Why p²? All smaller multiples already marked by smaller primes.
     O(n log log n) time — much better than O(n√n) naive."
    """
    if n <= 2: return 0
    sieve = [True] * n
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n, i):
                sieve[j] = False
    return sum(sieve)

# Time: O(n log log n), Space: O(n)

# ================================================================
# 67. RANSOM NOTE (Easy)
# ================================================================
def can_construct(ransomNote: str, magazine: str) -> bool:
    """
    INTERVIEW SCRIPT:
    "Count chars in magazine. For each char in ransomNote,
     decrement. If any count goes negative: can't construct."
    """
    mag_count = Counter(magazine)
    for c in ransomNote:
        mag_count[c] -= 1
        if mag_count[c] < 0: return False
    return True

# ================================================================
# 68. BULLS AND COWS (Medium)
# ================================================================
def get_hint(secret: str, guess: str) -> str:
    """
    Bulls: right digit right position. Cows: right digit wrong position.

    INTERVIEW SCRIPT:
    "First pass: count exact matches (bulls).
     Second pass: use frequency maps for remaining chars.
     Cows = min(secret_count[c], guess_count[c]) summed over all chars."
    """
    bulls = sum(s == g for s, g in zip(secret, guess))
    secret_count = Counter(s for s, g in zip(secret, guess) if s != g)
    guess_count = Counter(g for s, g in zip(secret, guess) if s != g)
    cows = sum(min(secret_count[c], guess_count[c]) for c in secret_count)
    return f"{bulls}A{cows}B"

# ================================================================
# 69. ISOMORPHIC STRINGS (Easy)
# ================================================================
def is_isomorphic(s: str, t: str) -> bool:
    """
    INTERVIEW SCRIPT:
    "Two strings are isomorphic if chars can be replaced consistently.
     Map each char in s to corresponding char in t AND vice versa.
     Bidirectional mapping prevents many-to-one mapping."
    """
    s_to_t, t_to_s = {}, {}
    for cs, ct in zip(s, t):
        if cs in s_to_t and s_to_t[cs] != ct: return False
        if ct in t_to_s and t_to_s[ct] != cs: return False
        s_to_t[cs] = ct; t_to_s[ct] = cs
    return True

# ================================================================
# 70. WORD PATTERN (Easy)
# ================================================================
def word_pattern(pattern: str, s: str) -> bool:
    """
    INTERVIEW SCRIPT:
    "Same as isomorphic strings but with words.
     Map pattern char to word and word to pattern char (bidirectional)."
    """
    words = s.split()
    if len(pattern) != len(words): return False
    char_to_word, word_to_char = {}, {}
    for c, w in zip(pattern, words):
        if c in char_to_word and char_to_word[c] != w: return False
        if w in word_to_char and word_to_char[w] != c: return False
        char_to_word[c] = w; word_to_char[w] = c
    return True

# ================================================================
# 71. CONTAINS DUPLICATE II (Easy)
# ================================================================
def contains_nearby_duplicate(nums: List[int], k: int) -> bool:
    """
    Duplicate within k index distance.

    INTERVIEW SCRIPT:
    "Hash map: num → last seen index. If duplicate found and
     distance <= k: return True."
    """
    last_seen = {}
    for i, num in enumerate(nums):
        if num in last_seen and i - last_seen[num] <= k: return True
        last_seen[num] = i
    return False

# ================================================================
# 72. SORT CHARACTERS BY FREQUENCY (Medium)
# ================================================================
def frequency_sort(s: str) -> str:
    """
    INTERVIEW SCRIPT:
    "Count frequencies. Sort by frequency descending.
     Build result string."
    """
    freq = Counter(s)
    return ''.join(c * count for c, count in freq.most_common())

# ================================================================
# 73. MAJORITY ELEMENT II (Medium)
# ================================================================
def majority_element_ii(nums: List[int]) -> List[int]:
    """
    Find all elements appearing more than n/3 times.
    At most 2 such elements can exist.

    INTERVIEW SCRIPT:
    "Extended Boyer-Moore: track 2 candidates with 2 counts.
     First pass: find candidates. Second pass: verify counts.
     WHY: at most 2 elements > n/3 (since 3 * n/3 = n)."
    """
    cand1 = cand2 = None
    count1 = count2 = 0
    for num in nums:
        if num == cand1: count1 += 1
        elif num == cand2: count2 += 1
        elif count1 == 0: cand1 = num; count1 = 1
        elif count2 == 0: cand2 = num; count2 = 1
        else: count1 -= 1; count2 -= 1

    result = []
    for cand in [cand1, cand2]:
        if cand is not None and nums.count(cand) > len(nums) // 3:
            result.append(cand)
    return result

# ================================================================
# 74. MINIMUM INDEX SUM OF TWO LISTS (Easy)
# ================================================================
def find_restaurant(list1: List[str], list2: List[str]) -> List[str]:
    """
    Find common strings with minimum index sum.

    INTERVIEW SCRIPT:
    "Index map for list1. For each string in list2 that's also in list1,
     compute index sum. Track minimum."
    """
    index1 = {s: i for i, s in enumerate(list1)}
    min_sum = float('inf')
    result = []
    for j, s in enumerate(list2):
        if s in index1:
            idx_sum = index1[s] + j
            if idx_sum < min_sum:
                min_sum = idx_sum; result = [s]
            elif idx_sum == min_sum:
                result.append(s)
    return result

# ================================================================
# 75-80: MORE HASHING PROBLEMS
# ================================================================

def find_the_difference(s: str, t: str) -> str:
    """
    389. Find the Difference (Easy) — one extra char added to t
    INTERVIEW SCRIPT: "XOR all chars in both strings. Extra char remains."
    """
    result = 0
    for c in s + t: result ^= ord(c)
    return chr(result)

def check_pairs_divisible(arr: List[int], k: int) -> bool:
    """
    1497. Check If Array Pairs Are Divisible by k (Medium)
    INTERVIEW SCRIPT:
    "For each pair, remainders must sum to k (or both 0).
     Count remainders. remainder r pairs with k-r."
    """
    remainder_count = defaultdict(int)
    for num in arr:
        remainder_count[num % k] += 1
    for r, cnt in remainder_count.items():
        if r == 0:
            if cnt % 2 != 0: return False
        elif remainder_count[r] != remainder_count[k - r]:
            return False
    return True

def relative_sort_array(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    1122. Relative Sort Array (Easy)
    INTERVIEW SCRIPT:
    "Sort arr1: elements in arr2 come first (in arr2 order),
     remaining elements sorted numerically at end."
    """
    order = {v: i for i, v in enumerate(arr2)}
    return sorted(arr1, key=lambda x: (order.get(x, len(arr2)), x))

def height_checker(heights: List[int]) -> int:
    """
    1051. Height Checker (Easy)
    INTERVIEW SCRIPT: "Count positions where heights[i] != sorted[i]."
    """
    return sum(a != b for a, b in zip(heights, sorted(heights)))

def num_unique_emails(emails: List[str]) -> int:
    """
    929. Unique Email Addresses (Easy)
    INTERVIEW SCRIPT:
    "Apply email rules: in local part, dots ignored, '+...' stripped.
     Domain unchanged. Count unique cleaned emails."
    """
    unique = set()
    for email in emails:
        local, domain = email.split('@')
        local = local.split('+')[0].replace('.', '')
        unique.add(local + '@' + domain)
    return len(unique)

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Group Anagrams:", group_anagrams(["eat","tea","tan","ate","nat","bat"]))
    print("Top K Frequent [1,1,1,2,2,3] k=2:", top_k_frequent([1,1,1,2,2,3], 2))
    print("Longest Consecutive [100,4,200,1,3,2]:", longest_consecutive([100,4,200,1,3,2]))
    print("Subarray Sum [1,1,1] k=2:", subarray_sum([1,1,1], 2))
    print("Happy 19:", is_happy(19))
    print("First Unique 'leetcode':", first_uniq_char("leetcode"))
    print("Intersect [4,9,5],[9,4,9,8,4]:", intersect([4,9,5],[9,4,9,8,4]))
    print("Find duplicates [4,3,2,7,8,2,3,1]:", find_duplicates([4,3,2,7,8,2,3,1]))
    print("Count Primes 10:", count_primes(10))
    print("Is Isomorphic 'egg','add':", is_isomorphic("egg","add"))
    print("Majority Element II [3,2,3]:", majority_element_ii([3,2,3]))
