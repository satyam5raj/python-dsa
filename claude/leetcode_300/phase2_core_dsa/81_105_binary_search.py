"""
================================================================
LEETCODE PHASE 2 (Problems 81-105): BINARY SEARCH
================================================================
"""

from typing import List
import math

# ================================================================
# 81. BINARY SEARCH (Easy)
# ================================================================
def search(nums: List[int], target: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Classic binary search. Three pointers: left, right, mid.
     mid = left + (right-left)//2 prevents integer overflow.
     Three cases: found, search left, search right.
     Loop condition: left <= right (inclusive both ends)."
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1

# Time: O(log n), Space: O(1)

# ================================================================
# 82. SEARCH INSERT POSITION (Easy)
# ================================================================
def search_insert(nums: List[int], target: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Standard binary search. If not found, left pointer is the insertion position.
     WHY? Left ends up at first element >= target."
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target: left = mid + 1
        else: right = mid
    return left

# ================================================================
# 83. SQRT(x) (Easy)
# ================================================================
def my_sqrt_brute(x: int) -> int:
    """APPROACH 1: O(√x) linear search"""
    i = 0
    while (i+1)*(i+1) <= x: i += 1
    return i

def my_sqrt(x: int) -> int:
    """
    APPROACH 2: O(log x) binary search

    INTERVIEW SCRIPT:
    "Binary search for integer square root.
     Search space: [0, x//2+1].
     Find largest mid such that mid*mid <= x."
    """
    if x < 2: return x
    left, right = 1, x // 2
    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid == x: return mid
        elif mid * mid < x: left = mid + 1
        else: right = mid - 1
    return right

# ================================================================
# 84. GUESS NUMBER HIGHER OR LOWER (Easy)
# ================================================================
def guess_number(n: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Standard binary search. API: guess(num) returns -1 (too high),
     1 (too low), 0 (correct)."
    """
    def guess(num): pass  # API provided

    left, right = 1, n
    while left <= right:
        mid = left + (right - left) // 2
        result = guess(mid)
        if result == 0: return mid
        elif result == 1: left = mid + 1
        else: right = mid - 1
    return -1

# ================================================================
# 85. FIRST BAD VERSION (Easy)
# ================================================================
def first_bad_version(n: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Binary search for first True in [False,...,False,True,...,True].
     Once a version is bad, all subsequent are bad.
     Find LEFTMOST bad version: when isBadVersion(mid)=True, search left."
    """
    def isBadVersion(v): pass  # API

    left, right = 1, n
    while left < right:
        mid = left + (right - left) // 2
        if isBadVersion(mid): right = mid      # might be first bad
        else: left = mid + 1
    return left

# ================================================================
# 86. FIND PEAK ELEMENT (Medium)
# ================================================================
def find_peak_element(nums: List[int]) -> int:
    """
    APPROACH 1: O(n) — linear scan
    APPROACH 2: O(log n) — binary search

    INTERVIEW SCRIPT:
    "KEY INSIGHT: if nums[mid] < nums[mid+1], peak is to the right.
     if nums[mid] > nums[mid+1], peak is at mid or to the left.
     WHY? Moving toward the larger neighbor guarantees reaching a peak."
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid+1]: left = mid + 1
        else: right = mid
    return left

# ================================================================
# 87. SEARCH IN ROTATED SORTED ARRAY (Medium)
# ================================================================
def search_rotated(nums: List[int], target: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Even in rotated array, ONE half is always sorted.
     Determine which half: if nums[left] <= nums[mid]: left is sorted.
     Check if target in sorted half. If yes: search there. Else: other half."
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target: return mid
        if nums[left] <= nums[mid]:            # left half sorted
            if nums[left] <= target < nums[mid]: right = mid - 1
            else: left = mid + 1
        else:                                   # right half sorted
            if nums[mid] < target <= nums[right]: left = mid + 1
            else: right = mid - 1
    return -1

# ================================================================
# 88. FIND MINIMUM IN ROTATED SORTED ARRAY (Medium)
# ================================================================
def find_min(nums: List[int]) -> int:
    """
    INTERVIEW SCRIPT:
    "Minimum is at the rotation point.
     If nums[mid] > nums[right]: minimum is in right half (after mid).
     Else: minimum is in left half including mid.
     Invariant: nums[right] is always to the right of minimum."
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]: left = mid + 1
        else: right = mid
    return nums[left]

# ================================================================
# 89. SEARCH A 2D MATRIX (Medium)
# ================================================================
def search_matrix_brute(matrix: List[List[int]], target: int) -> bool:
    """APPROACH 1: O(m*n) — check each element"""
    return any(target in row for row in matrix)

def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    APPROACH 2: O(log(m*n)) — treat as flat sorted array

    INTERVIEW SCRIPT:
    "Matrix rows are sorted, last of row i < first of row i+1.
     Treat as a flat sorted array of m*n elements.
     Binary search: idx → row=idx//cols, col=idx%cols."
    """
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m*n - 1
    while left <= right:
        mid = (left + right) // 2
        val = matrix[mid // n][mid % n]
        if val == target: return True
        elif val < target: left = mid + 1
        else: right = mid - 1
    return False

# ================================================================
# 90. KOKO EATING BANANAS (Medium) — BINARY SEARCH ON ANSWER
# ================================================================
def min_eating_speed(piles: List[int], h: int) -> int:
    """
    APPROACH 1: O(max(piles) * n) — try each speed
    APPROACH 2: O(n log max(piles)) — binary search on speed

    INTERVIEW SCRIPT:
    "Binary search on the ANSWER (eating speed).
     Low=1, High=max(piles). For speed k: hours = sum(ceil(pile/k)).
     If hours <= h: speed k works, try slower (search left).
     If hours > h: too slow, need faster (search right).
     Find minimum feasible speed."
    """
    def can_finish(speed):
        return sum(math.ceil(p / speed) for p in piles) <= h

    left, right = 1, max(piles)
    while left < right:
        mid = (left + right) // 2
        if can_finish(mid): right = mid     # might find smaller
        else: left = mid + 1
    return left

# ================================================================
# 91. CAPACITY TO SHIP PACKAGES (Medium)
# ================================================================
def ship_within_days(weights: List[int], days: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Binary search on capacity.
     Low=max(weights) (must fit heaviest), High=sum(weights) (1 day).
     For capacity cap: count days needed to ship all.
     Find minimum feasible capacity."
    """
    def can_ship(cap):
        d, curr = 1, 0
        for w in weights:
            if curr + w > cap: d += 1; curr = 0
            curr += w
        return d <= days

    left, right = max(weights), sum(weights)
    while left < right:
        mid = (left + right) // 2
        if can_ship(mid): right = mid
        else: left = mid + 1
    return left

# ================================================================
# 92. SPLIT ARRAY LARGEST SUM (Hard)
# ================================================================
def split_array(nums: List[int], k: int) -> int:
    """
    Split into k subarrays, minimize the largest sum.

    INTERVIEW SCRIPT:
    "Binary search on answer (the largest subarray sum).
     Low=max(nums), High=sum(nums).
     For a given max_sum, greedily count number of subarrays needed.
     Find minimum max_sum that allows splitting into <= k subarrays."
    """
    def can_split(max_sum):
        count, curr = 1, 0
        for num in nums:
            if curr + num > max_sum: count += 1; curr = 0
            curr += num
        return count <= k

    left, right = max(nums), sum(nums)
    while left < right:
        mid = (left + right) // 2
        if can_split(mid): right = mid
        else: left = mid + 1
    return left

# ================================================================
# 93. MEDIAN OF TWO SORTED ARRAYS (Hard)
# ================================================================
def find_median_sorted_arrays(nums1: List[int], nums2: List[int]) -> float:
    """
    APPROACH 1: O((m+n) log(m+n)) — merge and find median
    APPROACH 2: O(log(min(m,n))) — binary search on partition

    INTERVIEW SCRIPT:
    "Binary search on smaller array.
     Partition both arrays such that left halves have all smaller elements.
     Find correct partition: nums1[mid1-1] <= nums2[mid2] AND nums2[mid2-1] <= nums1[mid1].
     Median = avg of max(lefts) and min(rights) for even total, max(lefts) for odd."
    """
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
        mid1 = (left + right) // 2
        mid2 = (m + n + 1) // 2 - mid1

        l1 = nums1[mid1-1] if mid1 > 0 else float('-inf')
        r1 = nums1[mid1]   if mid1 < m else float('inf')
        l2 = nums2[mid2-1] if mid2 > 0 else float('-inf')
        r2 = nums2[mid2]   if mid2 < n else float('inf')

        if l1 <= r2 and l2 <= r1:
            if (m + n) % 2 == 0:
                return (max(l1, l2) + min(r1, r2)) / 2.0
            return float(max(l1, l2))
        elif l1 > r2: right = mid1 - 1
        else: left = mid1 + 1

# ================================================================
# 94. FIND FIRST AND LAST POSITION (Medium)
# ================================================================
def search_range(nums: List[int], target: int) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Two binary searches: one biased left, one biased right.
     Left: when found, keep searching left (right = mid-1).
     Right: when found, keep searching right (left = mid+1)."
    """
    def find_left():
        left, right, pos = 0, len(nums)-1, -1
        while left <= right:
            mid = (left+right)//2
            if nums[mid] == target: pos = mid; right = mid-1
            elif nums[mid] < target: left = mid+1
            else: right = mid-1
        return pos

    def find_right():
        left, right, pos = 0, len(nums)-1, -1
        while left <= right:
            mid = (left+right)//2
            if nums[mid] == target: pos = mid; left = mid+1
            elif nums[mid] < target: left = mid+1
            else: right = mid-1
        return pos

    return [find_left(), find_right()]

# ================================================================
# 95. SINGLE ELEMENT IN SORTED ARRAY (Medium)
# ================================================================
def single_non_duplicate(nums: List[int]) -> int:
    """
    All elements appear twice except one. O(log n).

    INTERVIEW SCRIPT:
    "Pattern: before single element, pairs are at (even,odd) indices.
     After single element, pairs are at (odd,even) indices.
     Binary search: check if mid is on correct pair.
     If nums[mid]==nums[mid^1]: single is to the right.
     Else: single is at mid or to the left."
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if mid % 2 == 1: mid -= 1          # ensure mid is even
        if nums[mid] == nums[mid+1]: left = mid + 2  # pair intact, single is right
        else: right = mid                    # pair broken, single is here or left
    return nums[left]

# ================================================================
# 96. FIND K CLOSEST ELEMENTS (Medium)
# ================================================================
def find_closest_elements_brute(arr: List[int], k: int, x: int) -> List[int]:
    """APPROACH 1: O(n log n) — sort by distance"""
    return sorted(sorted(arr, key=lambda a: (abs(a-x), a))[:k])

def find_closest_elements(arr: List[int], k: int, x: int) -> List[int]:
    """
    APPROACH 2: O(log(n-k) + k) — binary search on window start

    INTERVIEW SCRIPT:
    "Binary search for left bound of k-element window.
     Compare arr[mid] vs arr[mid+k]: which is closer to x?
     If arr[mid+k]-x < x-arr[mid]: window should move right.
     Else: window should stay or move left."
    """
    left, right = 0, len(arr) - k
    while left < right:
        mid = (left + right) // 2
        if x - arr[mid] > arr[mid+k] - x: left = mid + 1
        else: right = mid
    return arr[left:left+k]

# ================================================================
# 97. TIME BASED KEY-VALUE STORE (Medium)
# ================================================================
class TimeMap:
    """
    INTERVIEW SCRIPT:
    "Store (timestamp, value) pairs per key.
     Since timestamps are strictly increasing: binary search for timestamp <= given.
     Use bisect_right to find insertion point, then check previous entry."
    """
    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        import bisect
        vals = self.store[key]
        idx = bisect.bisect_right(vals, (timestamp, chr(127)))
        return vals[idx-1][1] if idx > 0 else ""

# ================================================================
# 98. MINIMUM NUMBER OF DAYS TO MAKE BOUQUETS (Medium)
# ================================================================
def min_days(bloomDay: List[int], m: int, k: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Binary search on the answer (number of days).
     If m*k > n: impossible. Low=min(bloomDay), High=max(bloomDay).
     For a given day d: count bouquets possible (consecutive bloomed flowers).
     Find minimum d where bouquets >= m."
    """
    n = len(bloomDay)
    if m * k > n: return -1

    def can_make(d):
        bouquets = consecutive = 0
        for day in bloomDay:
            if day <= d: consecutive += 1
            else: consecutive = 0
            if consecutive == k: bouquets += 1; consecutive = 0
        return bouquets >= m

    left, right = min(bloomDay), max(bloomDay)
    while left < right:
        mid = (left + right) // 2
        if can_make(mid): right = mid
        else: left = mid + 1
    return left

# ================================================================
# 99. VALID PERFECT SQUARE (Easy)
# ================================================================
def is_perfect_square(num: int) -> bool:
    """
    INTERVIEW SCRIPT:
    "Binary search for integer square root.
     If sqrt is integer: perfect square. O(log n)."
    """
    if num < 2: return True
    left, right = 1, num // 2
    while left <= right:
        mid = (left + right) // 2
        sq = mid * mid
        if sq == num: return True
        elif sq < num: left = mid + 1
        else: right = mid - 1
    return False

# ================================================================
# 100. ARRANGE COINS (Easy)
# ================================================================
def arrange_coins(n: int) -> int:
    """
    Find max complete rows of staircase (row k needs k coins).
    1+2+...+k = k(k+1)/2 <= n

    INTERVIEW SCRIPT:
    "Binary search for max k where k*(k+1)/2 <= n.
     Or math formula: k = (-1 + sqrt(1+8n)) / 2."
    """
    left, right = 0, n
    while left <= right:
        mid = (left + right) // 2
        if mid * (mid+1) // 2 <= n: left = mid + 1
        else: right = mid - 1
    return right

# ================================================================
# 101. COUNT NEGATIVE NUMBERS IN SORTED MATRIX (Easy)
# ================================================================
def count_negatives(grid: List[List[int]]) -> int:
    """
    INTERVIEW SCRIPT:
    "Start from top-right. If negative: all below are negative (count+rows-r).
     Move left. If non-negative: move down.
     O(m+n) — staircase traversal. Or binary search each row: O(m log n)."
    """
    rows, cols = len(grid), len(grid[0])
    r, c = 0, cols - 1
    count = 0
    while r < rows and c >= 0:
        if grid[r][c] < 0: count += rows - r; c -= 1
        else: r += 1
    return count

# ================================================================
# 102-105. ADDITIONAL BINARY SEARCH
# ================================================================

def peak_index_mountain(arr: List[int]) -> int:
    """852. Peak Index in Mountain Array (Medium)"""
    left, right = 0, len(arr)-1
    while left < right:
        mid = (left+right)//2
        if arr[mid] < arr[mid+1]: left = mid+1
        else: right = mid
    return left

def find_smallest_greater_letter(letters: List[str], target: str) -> str:
    """744. Find Smallest Letter Greater Than Target (Easy)"""
    left, right = 0, len(letters)
    while left < right:
        mid = (left+right)//2
        if letters[mid] <= target: left = mid+1
        else: right = mid
    return letters[left % len(letters)]

def missing_ranges(nums: List[int], lower: int, upper: int) -> List[str]:
    """163. Missing Ranges"""
    result = []
    prev = lower - 1
    for num in nums + [upper + 1]:
        if num - prev == 2: result.append(str(prev+1))
        elif num - prev > 2: result.append(f"{prev+1}->{num-1}")
        prev = num
    return result

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Binary Search [1,3,5,7,9] t=5:", search([1,3,5,7,9], 5))
    print("Search Insert [1,3,5,6] t=2:", search_insert([1,3,5,6], 2))
    print("Sqrt(8):", my_sqrt(8))
    print("Find Peak [1,2,3,1]:", find_peak_element([1,2,3,1]))
    print("Search Rotated [4,5,6,7,0,1,2] t=0:", search_rotated([4,5,6,7,0,1,2], 0))
    print("Find Min Rotated [3,4,5,1,2]:", find_min([3,4,5,1,2]))
    print("Koko Eating [3,6,7,11] h=8:", min_eating_speed([3,6,7,11], 8))
    print("Capacity to Ship [1,2,3,4,5,6,7,8,9,10] d=5:", ship_within_days([1,2,3,4,5,6,7,8,9,10], 5))
    print("Median of [1,3],[2]:", find_median_sorted_arrays([1,3],[2]))
    print("Search Range [5,7,7,8,8,10] t=8:", search_range([5,7,7,8,8,10], 8))
    print("Single Non-dup [1,1,2,3,3,4,4,8,8]:", single_non_duplicate([1,1,2,3,3,4,4,8,8]))
