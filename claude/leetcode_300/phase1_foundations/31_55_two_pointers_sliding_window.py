"""
================================================================
LEETCODE PHASE 1 (Problems 31-55): TWO POINTERS + SLIDING WINDOW
================================================================
"""

from typing import List
from collections import defaultdict, deque

# ================================================================
# 31. REMOVE ELEMENT (Easy)
# ================================================================
def remove_element(nums: List[int], val: int) -> int:
    """
    Remove all occurrences of val in-place. Return new length.

    INTERVIEW SCRIPT:
    "Two pointers: k tracks insertion position.
     For each element not equal to val: write to position k.
     Return k as the new length."
    """
    k = 0
    for num in nums:
        if num != val:
            nums[k] = num
            k += 1
    return k

# Time: O(n), Space: O(1)

# ================================================================
# 32. VALID PALINDROME II (Easy)
# ================================================================
def valid_palindrome_ii(s: str) -> bool:
    """
    Can string become palindrome by deleting at most one character?

    INTERVIEW SCRIPT:
    "Two pointers. When mismatch: try skipping left OR right character.
     Check if either resulting substring is palindrome."
    """
    def is_palindrome(s, l, r):
        while l < r:
            if s[l] != s[r]: return False
            l += 1; r -= 1
        return True

    l, r = 0, len(s)-1
    while l < r:
        if s[l] != s[r]:
            return is_palindrome(s, l+1, r) or is_palindrome(s, l, r-1)
        l += 1; r -= 1
    return True

# ================================================================
# 33. TWO SUM II — INPUT ARRAY IS SORTED (Medium)
# ================================================================
def two_sum_ii(numbers: List[int], target: int) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Array is sorted → two pointers O(n) vs hash map O(n).
     Sorted enables: if sum < target: move left right.
     If sum > target: move right left."
    """
    left, right = 0, len(numbers)-1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target: return [left+1, right+1]  # 1-indexed
        elif s < target: left += 1
        else: right -= 1

# Time: O(n), Space: O(1)

# ================================================================
# 34. CONTAINER WITH MOST WATER (Medium)
# ================================================================
def max_area(height: List[int]) -> int:
    """
    INTERVIEW SCRIPT:
    "Two pointers at both ends. Area = min(h[l], h[r]) * (r-l).
     Always move the shorter side (moving taller can't increase area).
     WHY? Moving taller side: width decreases AND height can't improve.
          Moving shorter side: width decreases BUT height might improve."
    """
    left, right = 0, len(height)-1
    max_water = 0
    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        if height[left] < height[right]: left += 1
        else: right -= 1
    return max_water

# Time: O(n), Space: O(1)

# ================================================================
# 35. 3SUM (Medium)
# ================================================================
def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Find all unique triplets summing to 0.

    APPROACH 1: O(n³) — triple nested loops
    APPROACH 2: O(n²) — sort + two pointers

    INTERVIEW SCRIPT:
    "Sort first: O(n log n).
     Fix one element, use two pointers for remaining sum.
     Skip duplicates: if nums[i] == nums[i-1]: skip.
     After finding triplet: skip duplicates at both pointers.
     O(n²) time, O(1) extra space (excluding output)."
    """
    nums.sort()
    result = []
    for i in range(len(nums)-2):
        if i > 0 and nums[i] == nums[i-1]: continue  # skip duplicate
        left, right = i+1, len(nums)-1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left+1]: left += 1
                while left < right and nums[right] == nums[right-1]: right -= 1
                left += 1; right -= 1
            elif s < 0: left += 1
            else: right -= 1
    return result

# Time: O(n²), Space: O(1)

# ================================================================
# 36. LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS (Medium)
# ================================================================
def length_of_longest_substring_brute(s: str) -> int:
    """APPROACH 1: O(n²) — check each starting position"""
    max_len = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen: break
            seen.add(s[j])
            max_len = max(max_len, j-i+1)
    return max_len

def length_of_longest_substring(s: str) -> int:
    """
    APPROACH 2: O(n) — sliding window

    INTERVIEW SCRIPT:
    "Variable sliding window: track last occurrence of each char.
     Left pointer moves when duplicate found.
     Key: left = max(left, last_seen[char]+1) to handle non-adjacent dupes."
    """
    char_idx = {}
    left = max_len = 0
    for right, c in enumerate(s):
        if c in char_idx and char_idx[c] >= left:
            left = char_idx[c] + 1
        char_idx[c] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# Time: O(n), Space: O(min(n, alphabet))

# ================================================================
# 37. LONGEST REPEATING CHARACTER REPLACEMENT (Medium)
# ================================================================
def character_replacement(s: str, k: int) -> int:
    """
    Longest substring with at most k replacements to make all same char.

    INTERVIEW SCRIPT:
    "Sliding window: track max frequency char in window.
     Window is valid if: window_size - max_freq <= k.
     If invalid: shrink from left.
     Insight: we don't need to recompute max_freq when shrinking —
     we only care about finding windows larger than current best."
    """
    count = defaultdict(int)
    left = max_count = max_len = 0
    for right, c in enumerate(s):
        count[c] += 1
        max_count = max(max_count, count[c])
        if (right - left + 1) - max_count > k:
            count[s[left]] -= 1
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len

# Time: O(n), Space: O(1) — 26 chars

# ================================================================
# 38. PERMUTATION IN STRING (Medium)
# ================================================================
def check_inclusion(s1: str, s2: str) -> bool:
    """
    Does any permutation of s1 exist as substring of s2?

    INTERVIEW SCRIPT:
    "Fixed sliding window of size len(s1).
     Track char frequencies. Compare s1_count with window_count.
     Slide: add right char, remove left char.
     Optimization: track how many chars are 'satisfied' (count matches)."
    """
    if len(s1) > len(s2): return False
    s1_count = defaultdict(int)
    window = defaultdict(int)
    for c in s1: s1_count[c] += 1

    for i, c in enumerate(s2):
        window[c] += 1
        if i >= len(s1):
            left_c = s2[i - len(s1)]
            window[left_c] -= 1
            if window[left_c] == 0: del window[left_c]
        if window == s1_count: return True
    return False

# ================================================================
# 39. MINIMUM SIZE SUBARRAY SUM (Medium)
# ================================================================
def min_subarray_len_brute(target: int, nums: List[int]) -> int:
    """APPROACH 1: O(n²)"""
    min_len = float('inf')
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                min_len = min(min_len, j-i+1)
                break
    return min_len if min_len != float('inf') else 0

def min_subarray_len(target: int, nums: List[int]) -> int:
    """
    APPROACH 2: O(n) — sliding window

    INTERVIEW SCRIPT:
    "Variable sliding window. Expand right, shrink left when sum >= target.
     Track minimum length at each valid window."
    """
    left = curr_sum = 0
    min_len = float('inf')
    for right, num in enumerate(nums):
        curr_sum += num
        while curr_sum >= target:
            min_len = min(min_len, right - left + 1)
            curr_sum -= nums[left]
            left += 1
    return min_len if min_len != float('inf') else 0

# ================================================================
# 40. SUBARRAY PRODUCT LESS THAN K (Medium)
# ================================================================
def num_subarray_product_less_than_k(nums: List[int], k: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Sliding window: maintain product of current window.
     When product >= k: shrink from left.
     Count of valid subarrays ending at right = right - left + 1."
    """
    if k <= 1: return 0
    left = product = 0
    result = 0
    product = 1
    for right, num in enumerate(nums):
        product *= num
        while product >= k:
            product //= nums[left]
            left += 1
        result += right - left + 1
    return result

# ================================================================
# 41. SLIDING WINDOW MAXIMUM (Hard)
# ================================================================
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    APPROACH 1: O(n*k) — naive
    APPROACH 2: O(n) — monotonic deque

    INTERVIEW SCRIPT:
    "Maintain a monotonic decreasing deque of indices.
     Front = maximum for current window.
     For each element:
       1. Remove indices outside window from front.
       2. Remove smaller elements from back (they'll never be max).
       3. Append current index.
       4. If window is full: add front element to result."
    """
    dq = deque()  # stores indices
    result = []
    for i, num in enumerate(nums):
        while dq and dq[0] <= i - k: dq.popleft()
        while dq and nums[dq[-1]] < num: dq.pop()
        dq.append(i)
        if i >= k-1: result.append(nums[dq[0]])
    return result

# Time: O(n), Space: O(k)

# ================================================================
# 42. MINIMUM WINDOW SUBSTRING (Hard)
# ================================================================
def min_window_brute(s: str, t: str) -> str:
    """APPROACH 1: O(n²) — check all substrings"""
    from collections import Counter
    target = Counter(t)
    min_len = float('inf')
    result = ""
    for i in range(len(s)):
        window = defaultdict(int)
        for j in range(i, len(s)):
            window[s[j]] += 1
            if all(window[c] >= target[c] for c in target):
                if j - i + 1 < min_len:
                    min_len = j - i + 1
                    result = s[i:j+1]
                break
    return result

def min_window(s: str, t: str) -> str:
    """
    APPROACH 2: O(n) — sliding window with have/need

    INTERVIEW SCRIPT:
    "Use 'have' and 'need' counters.
     Expand right: when new char satisfies a need, increment 'have'.
     When have == need: valid window found.
     Shrink left: if removing left char breaks condition, decrement 'have'.
     Track minimum valid window."
    """
    from collections import Counter
    if not t: return ""
    need = Counter(t)
    window = defaultdict(int)
    have = required = len(need)
    left = 0
    min_len = float('inf')
    result = ""
    for right, c in enumerate(s):
        window[c] += 1
        if c in need and window[c] == need[c]: have += 1
        while have == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right+1]
            window[s[left]] -= 1
            if s[left] in need and window[s[left]] < need[s[left]]: have -= 1
            left += 1
    return result

# Time: O(n), Space: O(|t| + |s|)

# ================================================================
# 43. MAX CONSECUTIVE ONES III (Medium)
# ================================================================
def longest_ones(nums: List[int], k: int) -> int:
    """
    Flip at most k zeros. Find max consecutive 1s.

    INTERVIEW SCRIPT:
    "Sliding window: track number of zeros in window.
     When zeros > k: shrink from left.
     Same as 'longest repeating character replacement' with 1s."
    """
    left = zeros = 0
    max_len = 0
    for right, num in enumerate(nums):
        if num == 0: zeros += 1
        while zeros > k:
            if nums[left] == 0: zeros -= 1
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len

# ================================================================
# 44. FRUITS INTO BASKETS (Medium)
# ================================================================
def total_fruit(fruits: List[int]) -> int:
    """
    Max fruits picked with 2 baskets (each basket: 1 type).
    = Longest subarray with at most 2 distinct values.

    INTERVIEW SCRIPT:
    "Sliding window: track fruit counts in window.
     When more than 2 types: shrink from left.
     Max window size = answer."
    """
    basket = defaultdict(int)
    left = max_len = 0
    for right, fruit in enumerate(fruits):
        basket[fruit] += 1
        while len(basket) > 2:
            basket[fruits[left]] -= 1
            if basket[fruits[left]] == 0: del basket[fruits[left]]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len

# ================================================================
# 45. FIND ALL ANAGRAMS IN A STRING (Medium)
# ================================================================
def find_anagrams(s: str, p: str) -> List[int]:
    """
    Return start indices of anagrams of p in s.

    INTERVIEW SCRIPT:
    "Fixed sliding window of size len(p).
     Track character frequencies.
     Use 'matches' counter to avoid O(26) comparison each step."
    """
    from collections import Counter
    p_count = Counter(p)
    window = defaultdict(int)
    result = []
    matches = 0
    needed = len(p_count)

    for i, c in enumerate(s):
        window[c] += 1
        if c in p_count and window[c] == p_count[c]: matches += 1
        if i >= len(p):
            left_c = s[i - len(p)]
            if left_c in p_count and window[left_c] == p_count[left_c]: matches -= 1
            window[left_c] -= 1
            if window[left_c] == 0: del window[left_c]
        if matches == needed: result.append(i - len(p) + 1)
    return result

# ================================================================
# 46. MAXIMUM AVERAGE SUBARRAY I (Easy)
# ================================================================
def find_max_average(nums: List[int], k: int) -> float:
    """
    INTERVIEW SCRIPT:
    "Fixed sliding window of size k.
     Compute initial sum, slide: add right, remove left."
    """
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum / k

# ================================================================
# 47. BINARY SUBARRAYS WITH SUM (Medium)
# ================================================================
def num_subarrays_with_sum(nums: List[int], goal: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Prefix sum + hashmap: count subarrays with sum = goal.
     Same as 'Subarray Sum Equals K'."
    """
    prefix_count = defaultdict(int)
    prefix_count[0] = 1
    curr_sum = count = 0
    for num in nums:
        curr_sum += num
        count += prefix_count[curr_sum - goal]
        prefix_count[curr_sum] += 1
    return count

# ================================================================
# 48. SUBARRAYS WITH K DIFFERENT INTEGERS (Hard)
# ================================================================
def subarrays_with_k_distinct(nums: List[int], k: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Exactly k distinct = at_most(k) - at_most(k-1).
     at_most(k) counts subarrays with <= k distinct values."
    """
    def at_most(k):
        count = defaultdict(int)
        left = result = 0
        for right, num in enumerate(nums):
            count[num] += 1
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0: del count[nums[left]]
                left += 1
            result += right - left + 1
        return result

    return at_most(k) - at_most(k-1)

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("3Sum [-1,0,1,2,-1,-4]:", three_sum([-1,0,1,2,-1,-4]))
    print("Container [1,8,6,2,5,4,8,3,7]:", max_area([1,8,6,2,5,4,8,3,7]))
    print("Longest no-repeat 'abcabcbb':", length_of_longest_substring("abcabcbb"))
    print("Min window 'ADOBECODEBANC','ABC':", min_window("ADOBECODEBANC","ABC"))
    print("Sliding max [1,3,-1,-3,5,3,6,7] k=3:", max_sliding_window([1,3,-1,-3,5,3,6,7],3))
    print("Char replacement 'AABABBA' k=1:", character_replacement("AABABBA",1))
    print("Find anagrams 'cbaebabacd','abc':", find_anagrams("cbaebabacd","abc"))
