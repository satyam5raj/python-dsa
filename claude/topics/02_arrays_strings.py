"""
================================================================
TOPIC 2: ARRAYS & STRINGS
================================================================
Core patterns: Traversal, Prefix Sum, Kadane's, Two Pointers,
               Sliding Window
================================================================

INTERVIEW COMMUNICATION:
"Arrays are contiguous memory blocks with O(1) random access.
 The key patterns I'll consider are:
 - Two Pointers: when we need to compare/move from both ends
 - Sliding Window: for subarray/substring problems
 - Prefix Sum: for range sum queries
 - Kadane's: for maximum subarray"
================================================================
"""

from typing import List

# ================================================================
# PATTERN 1: TRAVERSAL
# ================================================================

def find_max_min(arr: List[int]):
    """Single pass traversal — O(n) time, O(1) space"""
    if not arr:
        return None, None
    max_val = min_val = arr[0]
    for x in arr[1:]:
        if x > max_val:
            max_val = x
        if x < min_val:
            min_val = x
    return max_val, min_val

def reverse_array(arr: List[int]) -> List[int]:
    """In-place reversal — O(n) time, O(1) space"""
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr

def rotate_right(arr: List[int], k: int) -> List[int]:
    """
    Rotate array right by k positions.
    Trick: reverse sub-arrays
    O(n) time, O(1) space
    """
    n = len(arr)
    k = k % n
    arr.reverse()
    arr[:k] = arr[:k][::-1]
    arr[k:] = arr[k:][::-1]
    return arr

# ================================================================
# PATTERN 2: PREFIX SUM
# ================================================================
"""
KEY INSIGHT: Precompute prefix[i] = sum of arr[0..i]
Then range sum query [l, r] = prefix[r] - prefix[l-1] in O(1)
"""

def build_prefix_sum(arr: List[int]) -> List[int]:
    """Build prefix sum array — O(n) time, O(n) space"""
    prefix = [0] * (len(arr) + 1)
    for i, val in enumerate(arr):
        prefix[i + 1] = prefix[i] + val
    return prefix

def range_sum_query(prefix: List[int], left: int, right: int) -> int:
    """O(1) range sum using prefix array"""
    return prefix[right + 1] - prefix[left]

def subarray_sum_equals_k(nums: List[int], k: int) -> int:
    """
    Count subarrays with sum = k
    USE CASE: Analytics — count windows with exactly k revenue

    APPROACH 1 (Brute): O(n²) — check every subarray
    APPROACH 2 (Prefix + HashMap): O(n) — optimal

    INTERVIEW SCRIPT:
    "I see we need contiguous subarrays summing to k.
     Brute force is O(n²). Let me think about prefix sums...
     If prefix[j] - prefix[i] = k, then subarray [i+1..j] sums to k.
     We want prefix[j] - k to exist in previous prefixes.
     So we use a hash map storing count of each prefix sum."
    """
    # APPROACH 1: BRUTE FORCE O(n²)
    def brute_force():
        count = 0
        for i in range(len(nums)):
            curr_sum = 0
            for j in range(i, len(nums)):
                curr_sum += nums[j]
                if curr_sum == k:
                    count += 1
        return count

    # APPROACH 2: OPTIMAL O(n) with prefix sum + hashmap
    from collections import defaultdict
    prefix_count = defaultdict(int)
    prefix_count[0] = 1  # empty prefix
    curr_sum = 0
    count = 0
    for num in nums:
        curr_sum += num
        count += prefix_count[curr_sum - k]
        prefix_count[curr_sum] += 1
    return count

# ================================================================
# PATTERN 3: KADANE'S ALGORITHM - Maximum Subarray
# ================================================================

def max_subarray_brute(nums: List[int]) -> int:
    """
    APPROACH 1 (Brute): O(n²)
    Check every possible subarray
    """
    max_sum = float('-inf')
    for i in range(len(nums)):
        curr = 0
        for j in range(i, len(nums)):
            curr += nums[j]
            max_sum = max(max_sum, curr)
    return max_sum

def max_subarray_kadane(nums: List[int]) -> int:
    """
    APPROACH 2: Kadane's Algorithm — O(n) time, O(1) space

    KEY INSIGHT: At each position, decide:
    - Extend current subarray? (curr_sum + num)
    - Start fresh from here? (num)
    Take whichever is bigger.

    INTERVIEW SCRIPT:
    "Kadane's algorithm tracks the maximum subarray ending at each index.
     For each element, we either extend the previous subarray or start new.
     We take max(current_element, current_element + previous_max).
     Time O(n), Space O(1) — optimal."

    USE CASE: Stock profit maximization, signal processing peak detection
    """
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

def max_subarray_with_indices(nums: List[int]):
    """Returns max sum AND the subarray indices"""
    max_sum = curr_sum = nums[0]
    start = end = temp_start = 0
    for i in range(1, len(nums)):
        if nums[i] > curr_sum + nums[i]:
            curr_sum = nums[i]
            temp_start = i
        else:
            curr_sum += nums[i]
        if curr_sum > max_sum:
            max_sum = curr_sum
            start = temp_start
            end = i
    return max_sum, start, end

# ================================================================
# PATTERN 4: TWO POINTERS
# ================================================================
"""
USE WHEN: Sorted array, palindrome check, finding pairs/triplets
KEY INSIGHT: Two pointers moving toward each other eliminates O(n²)
"""

def two_sum_sorted(nums: List[int], target: int):
    """
    Find pair summing to target in SORTED array
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Since the array is sorted, I can use two pointers.
     Left pointer at start, right at end.
     If sum == target: found it.
     If sum < target: move left pointer right (need bigger number).
     If sum > target: move right pointer left (need smaller number)."
    """
    left, right = 0, len(nums) - 1
    while left < right:
        curr_sum = nums[left] + nums[right]
        if curr_sum == target:
            return [left, right]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return []

def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Find all unique triplets summing to 0.
    O(n²) time — optimal for this problem

    APPROACH 1 (Brute): O(n³) three nested loops
    APPROACH 2 (Sort + Two Pointers): O(n²)

    INTERVIEW SCRIPT:
    "Sort first — O(n log n). Then fix one element and use
     two pointers for the remaining pair. Skip duplicates carefully.
     Overall O(n²) which is optimal since output can be O(n²)."
    """
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:  # skip duplicate
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return result

def is_palindrome(s: str) -> bool:
    """
    Check palindrome with two pointers
    O(n) time, O(1) space

    USE CASE: DNA sequence analysis, text processing
    """
    s = ''.join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

def container_with_most_water(heights: List[int]) -> int:
    """
    Find two lines that form a container holding most water.
    O(n) time — optimal

    INTERVIEW SCRIPT:
    "Start with widest container (left=0, right=n-1).
     Area = min(h[left], h[right]) * (right - left).
     Moving the taller side inward can only decrease width WITHOUT
     possibly increasing height — so always move the shorter side.
     This greedy choice is optimal."
    """
    left, right = 0, len(heights) - 1
    max_water = 0
    while left < right:
        water = min(heights[left], heights[right]) * (right - left)
        max_water = max(max_water, water)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return max_water

# ================================================================
# PATTERN 5: SLIDING WINDOW
# ================================================================
"""
USE WHEN: Contiguous subarray/substring with a constraint
FIXED WINDOW: window size is given
VARIABLE WINDOW: expand/shrink based on condition
"""

def max_sum_subarray_size_k(arr: List[int], k: int) -> int:
    """
    Fixed sliding window — O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Instead of recomputing sum for each window from scratch,
     I slide the window: subtract leftmost, add new rightmost.
     Each element is processed exactly once."
    """
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

def longest_substring_no_repeat(s: str) -> int:
    """
    Variable sliding window — O(n) time, O(min(n,alphabet)) space

    INTERVIEW SCRIPT:
    "Use a set to track characters in current window.
     Right pointer expands window, left pointer shrinks when duplicate found.
     Each character is added and removed at most once → O(n)."

    USE CASE: Password generation, unique token generation
    """
    # APPROACH 1: BRUTE FORCE O(n²)
    def brute():
        n = len(s)
        max_len = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                if s[j] in seen:
                    break
                seen.add(s[j])
                max_len = max(max_len, j - i + 1)
        return max_len

    # APPROACH 2: SLIDING WINDOW O(n)
    char_index = {}
    left = max_len = 0
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len

def longest_repeating_char_replacement(s: str, k: int) -> int:
    """
    Longest substring with at most k replacements to make all same char.
    O(n) time

    INTERVIEW SCRIPT:
    "Key insight: for a valid window of size len, we need
     len - max_count <= k (at most k replacements needed).
     Track the count of the most frequent character.
     If window is invalid, shrink from left."
    """
    from collections import defaultdict
    count = defaultdict(int)
    left = max_count = max_len = 0
    for right, char in enumerate(s):
        count[char] += 1
        max_count = max(max_count, count[char])
        window_size = right - left + 1
        if window_size - max_count > k:
            count[s[left]] -= 1
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len

def minimum_window_substring(s: str, t: str) -> str:
    """
    Minimum window in s containing all chars of t.
    O(n) time — optimal

    INTERVIEW SCRIPT:
    "This is a variable sliding window with frequency tracking.
     I need a 'have' count vs 'need' count.
     Expand right to include needed chars.
     When all chars are satisfied, shrink left to minimize window.
     Update answer at each valid window."
    """
    from collections import Counter
    if not t or not s:
        return ""

    need = Counter(t)
    window = {}
    have, required = 0, len(need)
    left = 0
    min_len = float('inf')
    result = ""

    for right, char in enumerate(s):
        window[char] = window.get(char, 0) + 1
        if char in need and window[char] == need[char]:
            have += 1
        while have == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]
            window[s[left]] -= 1
            if s[left] in need and window[s[left]] < need[s[left]]:
                have -= 1
            left += 1
    return result

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Arrays are used everywhere:
- Prefix Sum: Range query systems, image processing (2D prefix)
- Kadane's: Stock analysis, signal peak detection
- Two Pointers: Database join operations, merge operations
- Sliding Window: Network packet analysis, real-time metrics,
                  rate limiting, moving averages
"""

if __name__ == "__main__":
    # Prefix Sum
    arr = [1, 2, 3, 4, 5]
    prefix = build_prefix_sum(arr)
    print("Range sum [1,3]:", range_sum_query(prefix, 1, 3))  # 9

    # Kadane's
    print("Max subarray [-2,1,-3,4,-1,2,1,-5,4]:",
          max_subarray_kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6

    # Two Pointers
    print("Container with most water [1,8,6,2,5,4,8,3,7]:",
          container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49

    # Sliding Window
    print("Longest no-repeat in 'abcabcbb':",
          longest_substring_no_repeat("abcabcbb"))  # 3

    # Minimum Window
    print("Min window 'ADOBECODEBANC', 'ABC':",
          minimum_window_substring("ADOBECODEBANC", "ABC"))  # "BANC"
