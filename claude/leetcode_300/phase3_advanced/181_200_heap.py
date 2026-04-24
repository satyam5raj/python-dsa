"""
================================================================
LEETCODE PHASE 3 (Problems 181-200): HEAP / PRIORITY QUEUE
================================================================
"""

from typing import List, Optional
import heapq
from collections import defaultdict, Counter

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val; self.next = next
    def __repr__(self):
        vals, curr = [], self
        while curr: vals.append(str(curr.val)); curr = curr.next
        return " -> ".join(vals)

# ================================================================
# 181. KTH LARGEST ELEMENT IN ARRAY (Medium)
# ================================================================
def find_kth_largest_sort(nums: List[int], k: int) -> int:
    """APPROACH 1: O(n log n) — sort"""
    return sorted(nums, reverse=True)[k-1]

def find_kth_largest_heap(nums: List[int], k: int) -> int:
    """
    APPROACH 2: O(n log k) — min heap of size k

    INTERVIEW SCRIPT:
    "Maintain min-heap of size k. Top = smallest of k largest = kth largest.
     For each num: push. If heap > k: pop minimum.
     After processing: heap top is kth largest.
     O(n log k) — better than O(n log n) when k << n."
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k: heapq.heappop(heap)
    return heap[0]

def find_kth_largest_quickselect(nums: List[int], k: int) -> int:
    """
    APPROACH 3: O(n) average — QuickSelect

    INTERVIEW SCRIPT:
    "QuickSelect: like QuickSort but recurse only on one side.
     Target position = n - k (kth largest from end).
     Average O(n), worst O(n²). Use random pivot to avoid worst case."
    """
    import random
    target = len(nums) - k
    def quickselect(l, r):
        pivot = nums[r]
        p = l
        for i in range(l, r):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]; p += 1
        nums[p], nums[r] = nums[r], nums[p]
        if p == target: return nums[p]
        elif p < target: return quickselect(p+1, r)
        else: return quickselect(l, p-1)
    return quickselect(0, len(nums)-1)

# ================================================================
# 182. TOP K FREQUENT ELEMENTS (Medium)
# ================================================================
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    APPROACH 1: O(n log k) — heap
    APPROACH 2: O(n) — bucket sort

    INTERVIEW SCRIPT:
    "Bucket sort: buckets[freq] = elements with that frequency.
     Scan from highest frequency bucket. O(n) overall."
    """
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums)+1)]
    for num, cnt in freq.items(): buckets[cnt].append(num)
    result = []
    for i in range(len(buckets)-1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k: return result
    return result

# ================================================================
# 183. FIND MEDIAN FROM DATA STREAM (Hard)
# ================================================================
class MedianFinder:
    """
    INTERVIEW SCRIPT:
    "Two heaps: max-heap (lower half) + min-heap (upper half).
     Lower: max-heap stores negated values.
     Upper: min-heap.
     Invariant: all lower <= all upper, sizes differ by at most 1.
     Median: equal sizes → avg of both tops. Else → top of larger.
     Each addNum: O(log n). findMedian: O(1)."
    """
    def __init__(self):
        self.lo = []  # max-heap (negate)
        self.hi = []  # min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi): return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0

# ================================================================
# 184. MERGE K SORTED LISTS (Hard)
# ================================================================
def merge_k_lists_brute(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """APPROACH 1: O(n log n) — collect all, sort"""
    vals = []
    for l in lists:
        while l: vals.append(l.val); l = l.next
    dummy = curr = ListNode(0)
    for v in sorted(vals): curr.next = ListNode(v); curr = curr.next
    return dummy.next

def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    APPROACH 2: O(n log k) — min heap

    INTERVIEW SCRIPT:
    "Push first node from each list to min-heap.
     Pop minimum, add to result, push that node's next.
     n total nodes processed, each heap op O(log k).
     Total O(n log k) — much better than O(n log n) when k << n."
    """
    heap = []
    for i, node in enumerate(lists):
        if node: heapq.heappush(heap, (node.val, i, node))
    dummy = curr = ListNode(0)
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node; curr = curr.next
        if node.next: heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next

# ================================================================
# 185. K CLOSEST POINTS TO ORIGIN (Medium)
# ================================================================
def k_closest_brute(points: List[List[int]], k: int) -> List[List[int]]:
    """APPROACH 1: O(n log n) — sort by distance"""
    return sorted(points, key=lambda p: p[0]**2+p[1]**2)[:k]

def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    APPROACH 2: O(n log k) — max heap of size k

    INTERVIEW SCRIPT:
    "Use max-heap of size k. For each point:
     Push (-distance, point). If heap > k: pop max distance.
     Remaining k points are closest.
     No need to compute sqrt (compare squared distances)."
    """
    heap = []
    for x, y in points:
        heapq.heappush(heap, (-(x*x+y*y), [x,y]))
        if len(heap) > k: heapq.heappop(heap)
    return [p for _, p in heap]

# ================================================================
# 186. TASK SCHEDULER (Medium)
# ================================================================
def least_interval_math(tasks: List[str], n: int) -> int:
    """
    APPROACH 1: O(m log m) mathematical formula

    INTERVIEW SCRIPT:
    "Key insight: arrange around most frequent task.
     (max_freq-1)*(n+1) = frames for the most frequent task.
     + count_max_freq = remaining slots for tasks with max frequency.
     Take max with len(tasks) (when no idling needed)."
    """
    freq = Counter(tasks)
    max_freq = max(freq.values())
    count_max = sum(1 for f in freq.values() if f == max_freq)
    return max(len(tasks), (max_freq-1)*(n+1) + count_max)

def least_interval_simulation(tasks: List[str], n: int) -> int:
    """APPROACH 2: Simulation with max-heap and cooldown queue"""
    freq = Counter(tasks)
    heap = [-f for f in freq.values()]
    heapq.heapify(heap)
    time = 0
    cooldown = []  # (available_at, freq)

    while heap or cooldown:
        time += 1
        if heap:
            freq = heapq.heappop(heap) + 1  # -(f-1) = -(f)+1
            if freq < 0: cooldown.append((time+n, freq))
        if cooldown and cooldown[0][0] <= time:
            heapq.heappush(heap, cooldown.pop(0)[1])
    return time

# ================================================================
# 187. REORGANIZE STRING (Medium)
# ================================================================
def reorganize_string(s: str) -> str:
    """
    INTERVIEW SCRIPT:
    "Greedily place most frequent available char.
     Use max-heap. At each step: pop top (most frequent).
     If prev char same: pop second most frequent, push prev back.
     If heap empty and we'd place same char: impossible."
    """
    freq = Counter(s)
    heap = [(-cnt, char) for char, cnt in freq.items()]
    heapq.heapify(heap)
    result = []
    prev_cnt, prev_char = 0, ''

    while heap or prev_cnt < 0:
        if not heap: return ""
        cnt, char = heapq.heappop(heap)
        result.append(char)
        if prev_cnt < 0: heapq.heappush(heap, (prev_cnt, prev_char))
        prev_cnt, prev_char = cnt+1, char  # cnt+1 because negated

    return ''.join(result)

# ================================================================
# 188. FURTHEST BUILDING YOU CAN REACH (Medium)
# ================================================================
def furthest_building(heights: List[int], bricks: int, ladders: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Use ladders for largest climbs (don't know future, so use greedy).
     For each climb: use a ladder (push to min-heap).
     If ladders used > available: swap smallest ladder use with bricks.
     If not enough bricks: can't proceed, return current index."
    """
    heap = []  # min-heap of climbs using ladders
    for i in range(len(heights)-1):
        diff = heights[i+1] - heights[i]
        if diff <= 0: continue
        heapq.heappush(heap, diff)
        if len(heap) > ladders:
            smallest = heapq.heappop(heap)
            bricks -= smallest
            if bricks < 0: return i
    return len(heights)-1

# ================================================================
# 189. SMALLEST RANGE COVERING ELEMENTS (Hard)
# ================================================================
def smallest_range(nums: List[List[int]]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Use min-heap: each element is (value, row, col).
     Initialize with first element of each row.
     Track max value in heap.
     Pop min, update range if smaller, push next from same row.
     Stop when any row exhausted."
    """
    heap = [(row[0], i, 0) for i, row in enumerate(nums)]
    heapq.heapify(heap)
    curr_max = max(row[0] for row in nums)
    result = [heap[0][0], curr_max]

    while True:
        curr_min, i, j = heapq.heappop(heap)
        if curr_max - curr_min < result[1] - result[0]:
            result = [curr_min, curr_max]
        if j+1 >= len(nums[i]): break
        next_val = nums[i][j+1]
        curr_max = max(curr_max, next_val)
        heapq.heappush(heap, (next_val, i, j+1))
    return result

# ================================================================
# 190-200: MORE HEAP PROBLEMS
# ================================================================

def ugly_number_ii(n: int) -> int:
    """
    264. Ugly Number II — nth number whose only prime factors are 2,3,5

    INTERVIEW SCRIPT:
    "Use min-heap. Start with 1. Pop min, push min*2, min*3, min*5.
     Use set to avoid duplicates. nth pop = answer."
    """
    heap = [1]; seen = {1}; val = 1
    for _ in range(n):
        val = heapq.heappop(heap)
        for factor in [2, 3, 5]:
            new_val = val * factor
            if new_val not in seen:
                seen.add(new_val); heapq.heappush(heap, new_val)
    return val

def find_k_pairs_smallest_sums(nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
    """
    373. Find K Pairs with Smallest Sums

    INTERVIEW SCRIPT:
    "Start with pairs (nums1[i], nums2[0]) for all i.
     Min-heap: pop smallest sum pair.
     Push next pair from same row: (nums1[i], nums2[j+1])."
    """
    if not nums1 or not nums2: return []
    heap = [(nums1[i]+nums2[0], i, 0) for i in range(min(len(nums1), k))]
    heapq.heapify(heap)
    result = []
    while heap and len(result) < k:
        _, i, j = heapq.heappop(heap)
        result.append([nums1[i], nums2[j]])
        if j+1 < len(nums2):
            heapq.heappush(heap, (nums1[i]+nums2[j+1], i, j+1))
    return result

def meeting_rooms_ii(intervals: List[List[int]]) -> int:
    """
    253. Meeting Rooms II — min rooms needed

    INTERVIEW SCRIPT:
    "Sort by start time. Use min-heap of end times (active meetings).
     For each new meeting: if earliest ending meeting ends before start → reuse room.
     Else: need new room."
    """
    if not intervals: return 0
    intervals.sort(key=lambda x: x[0])
    heap = []
    for start, end in intervals:
        if heap and heap[0] <= start: heapq.heapreplace(heap, end)
        else: heapq.heappush(heap, end)
    return len(heap)

def kth_smallest_matrix(matrix: List[List[int]], k: int) -> int:
    """
    378. Kth Smallest Element in Sorted Matrix

    INTERVIEW SCRIPT:
    "Min-heap with first column. Pop min, push next in same row.
     O(k log n). Alternative: binary search on value."
    """
    n = len(matrix)
    heap = [(matrix[i][0], i, 0) for i in range(n)]
    heapq.heapify(heap)
    for _ in range(k-1):
        val, r, c = heapq.heappop(heap)
        if c+1 < n: heapq.heappush(heap, (matrix[r][c+1], r, c+1))
    return heapq.heappop(heap)[0]

def course_schedule_iii(courses: List[List[int]]) -> int:
    """
    630. Course Schedule III — max courses with deadlines

    INTERVIEW SCRIPT:
    "Sort by deadline. Greedy: take each course if time allows.
     If time > deadline after adding: replace longest course in schedule.
     Max-heap of durations. O(n log n)."
    """
    courses.sort(key=lambda x: x[1])
    heap = []  # max-heap (negate durations)
    time = 0
    for duration, deadline in courses:
        heapq.heappush(heap, -duration)
        time += duration
        if time > deadline:
            time += heapq.heappop(heap)  # remove longest (negated, so this adds back)
    return len(heap)

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Kth Largest [3,2,1,5,6,4] k=2:", find_kth_largest_heap([3,2,1,5,6,4], 2))
    print("Top K Frequent [1,1,1,2,2,3] k=2:", top_k_frequent([1,1,1,2,2,3], 2))
    mf = MedianFinder()
    for n in [1,2,3]: mf.addNum(n)
    print("Median of [1,2,3]:", mf.findMedian())
    print("Task Scheduler 'AABABC' n=2:", least_interval_math(list("AABABC"), 2))
    print("Reorganize 'aab':", reorganize_string("aab"))
    print("Furthest Building [4,2,7,6,9,14,12] b=5 l=1:", furthest_building([4,2,7,6,9,14,12],5,1))
    print("K Closest [[1,3],[-2,2]] k=1:", k_closest([[1,3],[-2,2]], 1))
    print("Meeting Rooms II [[0,30],[5,10],[15,20]]:", meeting_rooms_ii([[0,30],[5,10],[15,20]]))
