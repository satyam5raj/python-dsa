"""
================================================================
LEETCODE PHASE 1 (Problems 1-30): BASICS + ARRAYS
================================================================
For each problem:
  APPROACH 1: Brute force (worst case)
  APPROACH 2: Optimal
  COMPLEXITY: Time & Space
  INTERVIEW SCRIPT: What to say
================================================================
"""

from typing import List
from collections import defaultdict, Counter

# ================================================================
# 1. TWO SUM (Easy)
# ================================================================
"""
Given array of integers and target, return indices of two numbers summing to target.
Each input has exactly one solution. Can't use same element twice.
"""
def two_sum_brute(nums: List[int], target: int) -> List[int]:
    """APPROACH 1: O(n²) — check every pair"""
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    APPROACH 2: O(n) — HashMap

    INTERVIEW SCRIPT:
    "I'll use a hash map to store numbers I've seen.
     For each number, check if its complement (target - num) is in map.
     If yes: found! If no: add current number to map.
     Single pass, O(n) time, O(n) space.

     FOLLOW-UP: What if multiple solutions? Return all pairs using same approach.
     What if sorted? Use two pointers O(n) time O(1) space."
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

# Time: O(n), Space: O(n)

# ================================================================
# 2. CONTAINS DUPLICATE (Easy)
# ================================================================
"""
Return true if any value appears at least twice.
"""
def contains_duplicate_brute(nums: List[int]) -> bool:
    """APPROACH 1: O(n²) — compare each pair"""
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False

def contains_duplicate(nums: List[int]) -> bool:
    """
    APPROACH 2: O(n) — HashSet

    INTERVIEW SCRIPT:
    "I'll use a hash set to track seen values.
     If I encounter a number already in the set: return True.
     After all numbers: return False.
     Could also sort and check adjacent, but hash set is O(n)."
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Time: O(n), Space: O(n)

# ================================================================
# 3. VALID ANAGRAM (Easy)
# ================================================================
"""
Return true if t is an anagram of s (same chars, different order).
"""
def is_anagram_brute(s: str, t: str) -> bool:
    """APPROACH 1: O(n log n) — sort and compare"""
    return sorted(s) == sorted(t)

def is_anagram(s: str, t: str) -> bool:
    """
    APPROACH 2: O(n) — char frequency count

    INTERVIEW SCRIPT:
    "Anagrams have identical character frequencies.
     Count chars in s, decrement for t.
     If any count goes negative: not anagram.
     O(n) time, O(1) space (26 chars max).

     FOLLOW-UP: Unicode? Use general hash map."
    """
    if len(s) != len(t): return False
    count = Counter(s)
    for c in t:
        count[c] -= 1
        if count[c] < 0: return False
    return True

# Time: O(n), Space: O(1) — fixed alphabet

# ================================================================
# 4. RUNNING SUM OF 1D ARRAY (Easy)
# ================================================================
"""
Return running sum where running_sum[i] = sum(nums[0..i]).
"""
def running_sum(nums: List[int]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Simple prefix sum: running[i] = running[i-1] + nums[i].
     Can do in-place to save space."
    """
    for i in range(1, len(nums)):
        nums[i] += nums[i-1]
    return nums

# Time: O(n), Space: O(1) in-place

# ================================================================
# 5. FIND PIVOT INDEX (Easy)
# ================================================================
"""
Find leftmost index where left sum == right sum.
"""
def find_pivot_index(nums: List[int]) -> int:
    """
    INTERVIEW SCRIPT:
    "Compute total sum first.
     Iterate: maintain left_sum.
     Pivot: left_sum == total - left_sum - nums[i].
     Rearrange: 2*left_sum + nums[i] == total.
     Single pass after initial sum."
    """
    total = sum(nums)
    left_sum = 0
    for i, num in enumerate(nums):
        if left_sum == total - left_sum - num:
            return i
        left_sum += num
    return -1

# Time: O(n), Space: O(1)

# ================================================================
# 6. MAXIMUM SUBARRAY (Easy) — KADANE'S
# ================================================================
"""
Find contiguous subarray with largest sum.
"""
def max_subarray_brute(nums: List[int]) -> int:
    """APPROACH 1: O(n²) — try all subarrays"""
    max_sum = float('-inf')
    for i in range(len(nums)):
        curr = 0
        for j in range(i, len(nums)):
            curr += nums[j]
            max_sum = max(max_sum, curr)
    return max_sum

def max_subarray(nums: List[int]) -> int:
    """
    APPROACH 2: Kadane's Algorithm — O(n)

    INTERVIEW SCRIPT:
    "Kadane's algorithm: at each position, decide:
     extend current subarray OR start fresh.
     curr = max(nums[i], curr + nums[i]).
     Update global max at each step.
     This is optimal: O(n) time, O(1) space."
    """
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

# Time: O(n), Space: O(1)

# ================================================================
# 7. BEST TIME TO BUY AND SELL STOCK (Easy)
# ================================================================
"""
Find max profit: buy on one day, sell on future day.
"""
def max_profit_brute(prices: List[int]) -> int:
    """APPROACH 1: O(n²) — try every buy/sell pair"""
    max_p = 0
    for i in range(len(prices)):
        for j in range(i+1, len(prices)):
            max_p = max(max_p, prices[j] - prices[i])
    return max_p

def max_profit(prices: List[int]) -> int:
    """
    APPROACH 2: O(n) — track minimum buy price

    INTERVIEW SCRIPT:
    "I want to maximize sell_price - buy_price.
     Track the minimum price seen so far (best buy day).
     At each price, check if selling today gives max profit.
     Update min_price as we go.
     O(n) single pass, O(1) space."
    """
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

# Time: O(n), Space: O(1)

# ================================================================
# 8. MOVE ZEROES (Easy)
# ================================================================
"""
Move all 0s to end while maintaining relative order of non-zeros.
In-place, minimize operations.
"""
def move_zeroes_brute(nums: List[int]) -> None:
    """APPROACH 1: Use extra space"""
    non_zeros = [x for x in nums if x != 0]
    nums[:len(non_zeros)] = non_zeros
    nums[len(non_zeros):] = [0] * (len(nums) - len(non_zeros))

def move_zeroes(nums: List[int]) -> None:
    """
    APPROACH 2: Two pointers in-place — O(n), O(1)

    INTERVIEW SCRIPT:
    "Two pointers: insert_pos tracks where next non-zero should go.
     Scan with right pointer: when non-zero found, place at insert_pos.
     Fill rest with zeros. Single pass O(n), O(1) space."
    """
    insert_pos = 0
    for num in nums:
        if num != 0:
            nums[insert_pos] = num
            insert_pos += 1
    while insert_pos < len(nums):
        nums[insert_pos] = 0
        insert_pos += 1

# Time: O(n), Space: O(1)

# ================================================================
# 9. REMOVE DUPLICATES FROM SORTED ARRAY (Easy)
# ================================================================
"""
Remove duplicates in-place from sorted array.
Return count of unique elements.
"""
def remove_duplicates(nums: List[int]) -> int:
    """
    APPROACH: Two pointers — O(n), O(1)

    INTERVIEW SCRIPT:
    "Since sorted, duplicates are adjacent.
     Slow pointer: position to write next unique.
     Fast pointer: scan all elements.
     When fast finds new unique: write to slow position.
     Return slow+1 as count."
    """
    if not nums: return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1

# Time: O(n), Space: O(1)

# ================================================================
# 10. MERGE SORTED ARRAY (Easy)
# ================================================================
"""
Merge nums2 into nums1 in-place. nums1 has enough space.
"""
def merge_sorted_array_brute(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    """APPROACH 1: O((m+n) log(m+n)) — insert and sort"""
    nums1[m:] = nums2
    nums1.sort()

def merge_sorted_array(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    """
    APPROACH 2: O(m+n) — merge from END to avoid overwriting

    INTERVIEW SCRIPT:
    "Merge from the end: use three pointers.
     p1=m-1, p2=n-1, p=m+n-1 (writing position).
     Compare nums1[p1] and nums2[p2]: place larger at p.
     When nums2 is exhausted: done (nums1 is already there).
     WHY from end? Avoids overwriting unprocessed nums1 elements."
    """
    p1, p2, p = m-1, n-1, m+n-1
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]; p1 -= 1
        else:
            nums1[p] = nums2[p2]; p2 -= 1
        p -= 1
    while p2 >= 0:
        nums1[p] = nums2[p2]; p -= 1; p2 -= 1

# Time: O(m+n), Space: O(1)

# ================================================================
# 11. SQUARES OF A SORTED ARRAY (Easy)
# ================================================================
"""
Return array of squares sorted in non-decreasing order.
"""
def sorted_squares_brute(nums: List[int]) -> List[int]:
    """APPROACH 1: O(n log n) — square then sort"""
    return sorted(x*x for x in nums)

def sorted_squares(nums: List[int]) -> List[int]:
    """
    APPROACH 2: O(n) — two pointers from ends

    INTERVIEW SCRIPT:
    "Largest squares come from either end (most negative or most positive).
     Two pointers: left=0, right=n-1.
     Compare |nums[left]| vs |nums[right]|.
     Fill result from right to left (largest first).
     O(n) single pass."
    """
    n = len(nums)
    result = [0] * n
    left, right = 0, n-1
    pos = n-1
    while left <= right:
        l_sq, r_sq = nums[left]**2, nums[right]**2
        if l_sq > r_sq:
            result[pos] = l_sq; left += 1
        else:
            result[pos] = r_sq; right -= 1
        pos -= 1
    return result

# Time: O(n), Space: O(n)

# ================================================================
# 12. MISSING NUMBER (Easy)
# ================================================================
"""
Find missing number in range [0, n].
"""
def missing_number_sort(nums: List[int]) -> int:
    """APPROACH 1: O(n log n) — sort"""
    nums.sort()
    for i in range(len(nums)):
        if nums[i] != i: return i
    return len(nums)

def missing_number(nums: List[int]) -> int:
    """
    APPROACH 2: O(n) — sum formula

    INTERVIEW SCRIPT:
    "Expected sum 0..n = n*(n+1)/2.
     Actual sum = sum of array.
     Missing = expected - actual.
     Alternative: XOR approach O(n) time O(1) space."
    """
    n = len(nums)
    return n*(n+1)//2 - sum(nums)

# Time: O(n), Space: O(1)

# ================================================================
# 13. INTERSECTION OF TWO ARRAYS (Easy)
# ================================================================
def intersection(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Convert one array to set. Iterate other, check membership.
     Use set intersection: set(nums1) & set(nums2)."
    """
    return list(set(nums1) & set(nums2))

# Time: O(m+n), Space: O(m)

# ================================================================
# 14. PLUS ONE (Easy)
# ================================================================
"""
Increment integer represented as array of digits.
"""
def plus_one(digits: List[int]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Process from right to left.
     If digit < 9: increment and return.
     If digit == 9: set to 0 and carry over.
     If we exit loop with carry: prepend 1 (e.g., [9,9] → [1,0,0])."
    """
    for i in range(len(digits)-1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits  # overflow: 9...9 → 1 0...0

# Time: O(n), Space: O(1) amortized

# ================================================================
# 15. VALID PALINDROME (Easy)
# ================================================================
"""
Alphanumeric characters only, case-insensitive.
"""
def is_palindrome_brute(s: str) -> bool:
    """APPROACH 1: O(n) — filter then compare"""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

def is_palindrome(s: str) -> bool:
    """
    APPROACH 2: O(n) — two pointers, no extra space

    INTERVIEW SCRIPT:
    "Two pointers: left and right.
     Skip non-alphanumeric characters.
     Compare characters (case-insensitive).
     Move pointers inward until they meet."
    """
    left, right = 0, len(s)-1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1; right -= 1
    return True

# Time: O(n), Space: O(1)

# ================================================================
# 16. REVERSE STRING (Easy)
# ================================================================
def reverse_string(s: List[str]) -> None:
    """
    INTERVIEW SCRIPT:
    "Two pointers: swap from both ends until they meet.
     In-place, O(n) time, O(1) space."
    """
    left, right = 0, len(s)-1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1; right -= 1

# ================================================================
# 17. LENGTH OF LAST WORD (Easy)
# ================================================================
def length_of_last_word(s: str) -> int:
    """
    INTERVIEW SCRIPT:
    "Strip trailing spaces, find last word.
     Pythonic: s.split()[-1] but let me show manual approach.
     Scan from end skipping spaces, count until space or start."
    """
    s = s.rstrip()
    count = 0
    for c in reversed(s):
        if c == ' ': break
        count += 1
    return count

# ================================================================
# 18. MAJORITY ELEMENT (Easy)
# ================================================================
"""
Find element appearing more than n/2 times. Guaranteed to exist.
"""
def majority_element_brute(nums: List[int]) -> int:
    """APPROACH 1: O(n) — hash map count"""
    count = Counter(nums)
    return max(count, key=count.get)

def majority_element(nums: List[int]) -> int:
    """
    APPROACH 2: Boyer-Moore Voting — O(n), O(1)

    INTERVIEW SCRIPT:
    "Boyer-Moore Voting: maintain candidate and count.
     If count == 0: new candidate.
     If same as candidate: count++. Else: count--.
     Since majority element > n/2, it survives all cancellations.
     O(n) time, O(1) space — optimal."
    """
    candidate, count = None, 0
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    return candidate

# Time: O(n), Space: O(1)

# ================================================================
# 19. SINGLE NUMBER (Easy)
# ================================================================
def single_number(nums: List[int]) -> int:
    """
    INTERVIEW SCRIPT:
    "XOR approach: a^a=0, a^0=a.
     XOR all numbers. Pairs cancel, single remains.
     O(n) time, O(1) space — optimal."
    """
    result = 0
    for num in nums:
        result ^= num
    return result

# ================================================================
# 20. PASCAL'S TRIANGLE (Easy)
# ================================================================
def generate_pascals(numRows: int) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Each row starts and ends with 1.
     Middle: row[i][j] = prev[j-1] + prev[j].
     Build iteratively, each row from previous."
    """
    triangle = [[1]]
    for i in range(1, numRows):
        row = [1]
        for j in range(1, i):
            row.append(triangle[i-1][j-1] + triangle[i-1][j])
        row.append(1)
        triangle.append(row)
    return triangle

# ================================================================
# 21. ROTATE ARRAY (Medium)
# ================================================================
"""
Rotate array right by k steps.
"""
def rotate_brute(nums: List[int], k: int) -> None:
    """APPROACH 1: O(n*k) — rotate one at a time"""
    k %= len(nums)
    for _ in range(k):
        nums.insert(0, nums.pop())

def rotate(nums: List[int], k: int) -> None:
    """
    APPROACH 2: O(n) — reverse trick

    INTERVIEW SCRIPT:
    "Reverse approach:
     1. Reverse entire array.
     2. Reverse first k elements.
     3. Reverse last n-k elements.
     WHY: rotating right by k = reversing sub-arrays.
     Example: [1,2,3,4,5], k=2 → [4,5,1,2,3]."
    """
    n = len(nums)
    k %= n
    def rev(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1
    rev(0, n-1)    # reverse all
    rev(0, k-1)    # reverse first k
    rev(k, n-1)    # reverse rest

# Time: O(n), Space: O(1)

# ================================================================
# 22-30. MORE ARRAY PROBLEMS
# ================================================================

def find_disappeared_numbers(nums: List[int]) -> List[int]:
    """
    438. Find All Numbers Disappeared in Array (Easy)
    Numbers from 1..n. Find missing ones.

    INTERVIEW SCRIPT:
    "In-place marking: for each num, mark nums[|num|-1] as negative.
     Second pass: indices with positive values are missing numbers.
     O(n) time, O(1) extra space."
    """
    for num in nums:
        idx = abs(num) - 1
        nums[idx] = -abs(nums[idx])  # mark as visited
    return [i+1 for i, num in enumerate(nums) if num > 0]

def third_maximum(nums: List[int]) -> int:
    """
    414. Third Maximum Number (Easy)

    INTERVIEW SCRIPT:
    "Track top 3 distinct maximums using min-heap or explicit 3 vars.
     If less than 3 distinct: return maximum."
    """
    uniq = set(nums)
    if len(uniq) < 3:
        return max(uniq)
    uniq.remove(max(uniq))
    uniq.remove(max(uniq))
    return max(uniq)

def assign_cookies(g: List[int], s: List[int]) -> int:
    """
    455. Assign Cookies (Easy)

    INTERVIEW SCRIPT:
    "Greedy: sort both arrays.
     Assign smallest sufficient cookie to least greedy child.
     Two pointers: advance child when satisfied."
    """
    g.sort(); s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    return child

def sort_array_by_parity(nums: List[int]) -> List[int]:
    """
    905. Sort Array By Parity (Easy) — evens then odds

    INTERVIEW SCRIPT:
    "Two pointers: left scans for odd, right scans for even.
     Swap them. O(n) time, O(1) space."
    """
    left, right = 0, len(nums)-1
    while left < right:
        while left < right and nums[left] % 2 == 0:
            left += 1
        while left < right and nums[right] % 2 == 1:
            right -= 1
        if left < right:
            nums[left], nums[right] = nums[right], nums[left]
    return nums

def is_monotonic(nums: List[int]) -> bool:
    """
    896. Monotonic Array (Easy)

    INTERVIEW SCRIPT:
    "Check if all differences are same sign (all ≥0 or all ≤0)."
    """
    return (all(nums[i] <= nums[i+1] for i in range(len(nums)-1)) or
            all(nums[i] >= nums[i+1] for i in range(len(nums)-1)))

def valid_mountain_array(arr: List[int]) -> bool:
    """
    941. Valid Mountain Array (Easy)

    INTERVIEW SCRIPT:
    "Two pointers: left climbs up, right climbs down.
     Valid if they meet at same non-edge peak."
    """
    n = len(arr)
    left, right = 0, n-1
    while left+1 < n and arr[left] < arr[left+1]:
        left += 1
    while right-1 >= 0 and arr[right] < arr[right-1]:
        right -= 1
    return left == right and left != 0 and right != n-1

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Two Sum [2,7,11,15] t=9:", two_sum([2,7,11,15], 9))
    print("Contains Dup [1,2,3,1]:", contains_duplicate([1,2,3,1]))
    print("Valid Anagram 'anagram','nagaram':", is_anagram("anagram","nagaram"))
    print("Max Subarray [-2,1,-3,4,-1,2,1,-5,4]:", max_subarray([-2,1,-3,4,-1,2,1,-5,4]))
    print("Max Profit [7,1,5,3,6,4]:", max_profit([7,1,5,3,6,4]))
    print("Missing Number [3,0,1]:", missing_number([3,0,1]))
    print("Majority Element [3,2,3]:", majority_element([3,2,3]))
    print("Single Number [4,1,2,1,2]:", single_number([4,1,2,1,2]))
    nums = [1,2,3,4,5]
    rotate(nums, 2)
    print("Rotate [1,2,3,4,5] by 2:", nums)
