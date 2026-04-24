"""
================================================================
TOPIC 3: HASHING
================================================================
HashMap / HashSet — The most powerful tool for reducing
O(n²) solutions to O(n)

KEY IDEA: Trade O(n) space for O(1) lookup time.
"Have I seen this before?" → Use a HashSet
"How many times did I see X?" → Use a HashMap

INTERVIEW COMMUNICATION:
"I'll use a hash map here to get O(1) lookups instead of
 scanning the array each time, reducing from O(n²) to O(n)."
================================================================
"""

from collections import defaultdict, Counter
from typing import List, Optional

# ================================================================
# CORE CONCEPTS
# ================================================================

# Python dict (HashMap): O(1) average insert/lookup/delete
# Python set (HashSet): O(1) average insert/lookup/delete
# collections.Counter: specialized frequency map
# collections.defaultdict: dict with default value

# ================================================================
# PATTERN 1: FREQUENCY COUNTING
# ================================================================

def valid_anagram_brute(s: str, t: str) -> bool:
    """
    APPROACH 1 (Brute): Sort both strings — O(n log n)
    """
    return sorted(s) == sorted(t)

def valid_anagram_optimal(s: str, t: str) -> bool:
    """
    APPROACH 2 (HashMap): Count frequencies — O(n), O(1) space
    (O(1) space because only 26 lowercase letters)

    INTERVIEW SCRIPT:
    "Two strings are anagrams if they have identical character frequencies.
     I'll count chars in s, then decrement for t.
     If any count goes negative, not an anagram.
     O(n) time, O(1) space (26 chars max)."

    USE CASE: Spell checkers, plagiarism detection, word games
    """
    if len(s) != len(t):
        return False
    count = Counter(s)
    for char in t:
        count[char] -= 1
        if count[char] < 0:
            return False
    return True

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group strings that are anagrams of each other.
    O(n * k log k) where k is max string length

    INTERVIEW SCRIPT:
    "Key insight: all anagrams have the same sorted string.
     Use sorted string as key in hash map.
     Group all strings with same key together."

    USE CASE: Search engines (query normalization), autocorrect grouping
    """
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # or ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

def top_k_frequent_elements(nums: List[int], k: int) -> List[int]:
    """
    Return k most frequent elements.

    APPROACH 1 (Sort): O(n log n) — sort by frequency
    APPROACH 2 (Bucket Sort): O(n) — optimal

    INTERVIEW SCRIPT:
    "Count frequencies with a hash map.
     Instead of sorting (O(n log n)), use bucket sort:
     Create buckets[i] = list of elements with frequency i.
     Since max frequency is n, we have n+1 buckets.
     Iterate buckets from high to low to get top k."
    """
    # Approach 1: O(n log n)
    def with_sort():
        return [x for x, _ in Counter(nums).most_common(k)]

    # Approach 2: Bucket Sort O(n)
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)

    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result

# ================================================================
# PATTERN 2: LOOKUP OPTIMIZATION (Two Sum pattern)
# ================================================================

def two_sum_brute(nums: List[int], target: int) -> List[int]:
    """
    APPROACH 1 (Brute): O(n²) — check every pair
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

def two_sum_optimal(nums: List[int], target: int) -> List[int]:
    """
    APPROACH 2 (HashMap): O(n) time, O(n) space

    INTERVIEW SCRIPT:
    "For each number, I need its complement (target - num).
     Instead of scanning the array for the complement each time,
     I store visited numbers in a hash map.
     First occurrence of complement? Return immediately.
     O(n) single pass."

    USE CASE: Financial reconciliation, pair matching in databases
    """
    seen = {}  # {value: index}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

def longest_consecutive_sequence(nums: List[int]) -> int:
    """
    Find length of longest consecutive sequence.
    O(n) time — optimal despite appearances

    APPROACH 1 (Sort): O(n log n)
    APPROACH 2 (HashSet): O(n)

    INTERVIEW SCRIPT:
    "Sort-based is O(n log n). Can we do O(n)?
     Key insight: only start counting from sequence starts.
     A number n is a sequence start if n-1 is NOT in the set.
     From each start, count how long the sequence goes.
     Each number is visited at most twice → O(n) total."

    USE CASE: Data deduplication, finding gaps in ID sequences
    """
    # Approach 1: Sort O(n log n)
    def sort_approach():
        if not nums:
            return 0
        nums_sorted = sorted(set(nums))
        max_len = curr_len = 1
        for i in range(1, len(nums_sorted)):
            if nums_sorted[i] == nums_sorted[i-1] + 1:
                curr_len += 1
                max_len = max(max_len, curr_len)
            else:
                curr_len = 1
        return max_len

    # Approach 2: HashSet O(n)
    num_set = set(nums)
    max_len = 0
    for num in num_set:
        if num - 1 not in num_set:  # start of sequence
            curr = num
            length = 1
            while curr + 1 in num_set:
                curr += 1
                length += 1
            max_len = max(max_len, length)
    return max_len

# ================================================================
# PATTERN 3: SLIDING WINDOW + HASHING
# ================================================================

def first_unique_character(s: str) -> int:
    """
    First non-repeating character index.
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Two passes: first pass count frequencies,
     second pass find first with count 1."
    """
    freq = Counter(s)
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i
    return -1

def happy_number(n: int) -> bool:
    """
    Is n a happy number? (repeated digit sum of squares → 1)
    DETECT CYCLE with a set.

    INTERVIEW SCRIPT:
    "A number is happy if it eventually reaches 1.
     Non-happy numbers cycle. Use a set to detect the cycle.
     Alternatively, use Floyd's cycle detection (no extra space)."
    """
    def digit_sum_squares(num):
        total = 0
        while num:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    # With set (O(n) space)
    seen = set()
    while n != 1:
        n = digit_sum_squares(n)
        if n in seen:
            return False
        seen.add(n)
    return True

    # Floyd's (O(1) space) — two pointer approach
    # slow = n; fast = digit_sum_squares(n)
    # while fast != 1 and slow != fast:
    #     slow = digit_sum_squares(slow)
    #     fast = digit_sum_squares(digit_sum_squares(fast))
    # return fast == 1

def subarrays_k_different_integers(nums: List[int], k: int) -> int:
    """
    Count subarrays with exactly k distinct integers.

    TRICK: exactly(k) = atMost(k) - atMost(k-1)
    O(n) time

    INTERVIEW SCRIPT:
    "Exactly k distinct is hard directly.
     Key trick: exactly(k) = atMost(k) - atMost(k-1).
     atMost(k) uses sliding window with a frequency map."
    """
    def at_most_k(k):
        count = defaultdict(int)
        left = result = 0
        for right, num in enumerate(nums):
            count[num] += 1
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            result += right - left + 1
        return result

    return at_most_k(k) - at_most_k(k - 1)

# ================================================================
# HASHING IN PRACTICE — DESIGN PROBLEMS
# ================================================================

class MyHashMap:
    """
    Design a HashMap without using built-in hash libraries.
    USE CASE: Understanding how hash tables work internally
    """
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))

    def get(self, key: int) -> int:
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        self.buckets[idx] = [(k, v) for k, v in self.buckets[idx] if k != key]

class MyHashSet:
    """Design a HashSet"""
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        return key % self.size

    def add(self, key: int) -> None:
        idx = self._hash(key)
        if key not in self.buckets[idx]:
            self.buckets[idx].append(key)

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        if key in self.buckets[idx]:
            self.buckets[idx].remove(key)

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        return key in self.buckets[idx]

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Real-world applications of hashing:
- Databases: Index structures, JOIN operations
- Caches: LRU cache (dict + doubly linked list)
- Deduplication: Finding unique records
- Frequency analysis: Log analysis, analytics dashboards
- Two Sum pattern: Pair/triplet matching in datasets
- Grouping: Group by operations in SQL → group_anagrams pattern
- Counting: Word frequency in documents, histogram computation
"""

if __name__ == "__main__":
    print("Anagram check 'anagram','nagaram':", valid_anagram_optimal("anagram", "nagaram"))
    print("Group anagrams:", group_anagrams(["eat","tea","tan","ate","nat","bat"]))
    print("Two Sum [2,7,11,15] target=9:", two_sum_optimal([2, 7, 11, 15], 9))
    print("Longest consecutive [100,4,200,1,3,2]:",
          longest_consecutive_sequence([100, 4, 200, 1, 3, 2]))
    print("Top 2 frequent [1,1,1,2,2,3]:", top_k_frequent_elements([1,1,1,2,2,3], 2))
    print("Happy number 19:", happy_number(19))
