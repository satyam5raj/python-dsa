"""
================================================================
TOPIC 5: SEARCHING & SORTING
================================================================
LINEAR SEARCH: O(n) — unsorted data
BINARY SEARCH: O(log n) — SORTED data (or monotonic function)
SORTING: Bubble O(n²), Merge O(n log n), Quick O(n log n) avg

INTERVIEW COMMUNICATION:
"Binary search works when: array is sorted, OR we can define
 a monotonic predicate (true/false) over the search space.
 Think: 'Is this value feasible?' YES/NO answer = Binary Search."
================================================================
"""

from typing import List
import random

# ================================================================
# LINEAR SEARCH
# ================================================================

def linear_search(arr: List[int], target: int) -> int:
    """O(n) time, O(1) space — works on unsorted data"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# ================================================================
# BINARY SEARCH — CLASSIC
# ================================================================

def binary_search_iterative(arr: List[int], target: int) -> int:
    """
    O(log n) time, O(1) space

    INTERVIEW SCRIPT:
    "Maintain [left, right] search space.
     Calculate mid = left + (right-left)//2 (avoids overflow).
     Shrink the search space each iteration by half.
     3 conditions: found, go left, go right."
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # prevent integer overflow
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def search_insert_position(nums: List[int], target: int) -> int:
    """
    Find where target is or should be inserted.
    Standard binary search returning left (insertion point).
    """
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

def find_first_last_position(nums: List[int], target: int) -> List[int]:
    """
    Find first and last occurrence of target.
    O(log n) — two binary searches

    INTERVIEW SCRIPT:
    "Two separate binary searches:
     First: find leftmost (bias left when found).
     Second: find rightmost (bias right when found)."
    """
    def find_left():
        left, right, result = 0, len(nums) - 1, -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                result = mid
                right = mid - 1  # bias left
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    def find_right():
        left, right, result = 0, len(nums) - 1, -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                result = mid
                left = mid + 1  # bias right
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result

    return [find_left(), find_right()]

# ================================================================
# BINARY SEARCH ON ANSWER (Advanced)
# ================================================================
"""
PATTERN: When you see "minimize maximum" or "maximize minimum"
or "find minimum feasible value" → Binary search on the ANSWER

Template:
  left, right = min_possible, max_possible
  while left < right:
      mid = (left + right) // 2
      if feasible(mid):
          right = mid       # try smaller
      else:
          left = mid + 1    # need larger
  return left
"""

def koko_eating_bananas(piles: List[int], h: int) -> int:
    """
    Find minimum eating speed k such that Koko finishes in h hours.
    O(n log m) where m = max(piles)

    INTERVIEW SCRIPT:
    "Binary search on the answer (eating speed).
     Low = 1, High = max(piles).
     For a given speed k, check if all piles can be eaten in h hours.
     If yes, try lower speed. If no, need higher speed.
     feasible(k) = sum(ceil(pile/k) for pile in piles) <= h"
    """
    import math
    def feasible(speed):
        return sum(math.ceil(p / speed) for p in piles) <= h

    left, right = 1, max(piles)
    while left < right:
        mid = (left + right) // 2
        if feasible(mid):
            right = mid    # can eat slower?
        else:
            left = mid + 1  # need to eat faster
    return left

def capacity_to_ship(weights: List[int], days: int) -> int:
    """
    Min ship capacity to ship all packages within days.
    O(n log(sum)) — binary search on capacity

    INTERVIEW SCRIPT:
    "Binary search on capacity.
     Low = max(weights) — must fit heaviest package.
     High = sum(weights) — can ship everything in 1 day.
     feasible(cap) = can we ship in <= days with this capacity?"
    """
    def feasible(cap):
        d = 1
        curr_load = 0
        for w in weights:
            if curr_load + w > cap:
                d += 1
                curr_load = 0
            curr_load += w
        return d <= days

    left, right = max(weights), sum(weights)
    while left < right:
        mid = (left + right) // 2
        if feasible(mid):
            right = mid
        else:
            left = mid + 1
    return left

def search_rotated_array(nums: List[int], target: int) -> int:
    """
    Binary search on rotated sorted array.
    O(log n)

    INTERVIEW SCRIPT:
    "Key: even in a rotated array, one half is always sorted.
     Check which half is sorted, then check if target is in it.
     If yes, search that half. If no, search the other."
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1

def find_minimum_rotated(nums: List[int]) -> int:
    """
    Find minimum in rotated sorted array — O(log n)

    INTERVIEW SCRIPT:
    "Minimum is at the rotation point.
     If nums[mid] > nums[right]: minimum is in right half.
     Else: minimum is in left half (including mid)."
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]

# ================================================================
# SORTING ALGORITHMS
# ================================================================

def bubble_sort(arr: List[int]) -> List[int]:
    """
    O(n²) time, O(1) space
    BEST CASE: O(n) if already sorted (with early termination)

    INTERVIEW SCRIPT:
    "Repeatedly swap adjacent elements if out of order.
     After each pass, largest element bubbles to end.
     Optimization: track if any swap occurred — if not, sorted."
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # already sorted
    return arr

def selection_sort(arr: List[int]) -> List[int]:
    """
    O(n²) time, O(1) space
    Always O(n²) — no best case optimization

    INTERVIEW SCRIPT:
    "Find minimum in unsorted portion, swap to front.
     Unlike bubble sort, can't terminate early."
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr: List[int]) -> List[int]:
    """
    O(n²) time, O(1) space
    BEST CASE: O(n) — nearly sorted data
    STABLE sort, good for small/nearly sorted arrays

    INTERVIEW SCRIPT:
    "Think of sorting playing cards.
     Pick each element and insert into correct position in sorted portion.
     Efficient for nearly-sorted data."
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr: List[int]) -> List[int]:
    """
    O(n log n) time, O(n) space — STABLE sort

    INTERVIEW SCRIPT:
    "Divide array in half, sort each half recursively, merge.
     Merge is the key step: O(n) per level, O(log n) levels → O(n log n).
     Stable and predictable — preferred for external sorting."
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr: List[int], low: int = 0, high: int = None) -> List[int]:
    """
    O(n log n) average, O(n²) worst, O(log n) space
    UNSTABLE sort, but cache-friendly (in-place)

    INTERVIEW SCRIPT:
    "Choose a pivot, partition array around it.
     Elements < pivot go left, elements > pivot go right.
     Recursively sort both sides.
     Random pivot avoids O(n²) worst case on sorted input."
    """
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_idx = _partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    return arr

def _partition(arr: List[int], low: int, high: int) -> int:
    pivot = arr[high]  # choose last element as pivot
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_random_pivot(arr: List[int]) -> List[int]:
    """Quick sort with random pivot to avoid worst case"""
    if len(arr) <= 1:
        return arr
    pivot_idx = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_idx]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_random_pivot(left) + middle + quick_sort_random_pivot(right)

# ================================================================
# SORTING CHEAT SHEET
# ================================================================
"""
Algorithm      Time(avg)    Time(worst)  Space    Stable
─────────────────────────────────────────────────────────
Bubble Sort    O(n²)        O(n²)        O(1)     Yes
Selection Sort O(n²)        O(n²)        O(1)     No
Insertion Sort O(n²)        O(n²)        O(1)     Yes
Merge Sort     O(n log n)   O(n log n)   O(n)     Yes
Quick Sort     O(n log n)   O(n²)        O(log n) No
Heap Sort      O(n log n)   O(n log n)   O(1)     No
Tim Sort       O(n log n)   O(n log n)   O(n)     Yes  ← Python's sort()

WHEN TO USE WHAT:
- Small/nearly sorted data → Insertion Sort
- Need stable sort → Merge Sort
- In-place, average performance → Quick Sort (with random pivot)
- Memory constrained → Heap Sort
- General purpose → Python's sort() (Tim Sort)
"""

if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]

    print("Binary search:", binary_search_iterative([1,3,5,7,9,11], 7))
    print("Search rotated [4,5,6,7,0,1,2] target=0:", search_rotated_array([4,5,6,7,0,1,2], 0))
    print("Find min rotated [3,4,5,1,2]:", find_minimum_rotated([3,4,5,1,2]))
    print("Koko bananas [3,6,7,11] h=8:", koko_eating_bananas([3,6,7,11], 8))

    import copy
    print("Bubble sort:", bubble_sort(copy.copy(arr)))
    print("Merge sort:", merge_sort(copy.copy(arr)))
    print("Quick sort:", quick_sort(copy.copy(arr)))
