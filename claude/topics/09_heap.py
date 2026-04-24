"""
================================================================
TOPIC 9: HEAP / PRIORITY QUEUE
================================================================
Min Heap: parent <= children (root = minimum)
Max Heap: parent >= children (root = maximum)

Python: heapq module implements MIN HEAP
For max heap: negate values (push -val, pop gives -result)

KEY OPERATIONS: O(log n) insert, O(log n) delete, O(1) peek

INTERVIEW COMMUNICATION:
"When I need the kth largest/smallest, or always want the
 minimum/maximum efficiently, I'll use a heap.
 O(log n) insert/delete, O(1) peek — better than sorting everything."
================================================================
"""

import heapq
from typing import List, Optional
from collections import defaultdict

# ================================================================
# HEAP BASICS WITH Python's heapq
# ================================================================

def heap_demo():
    # MIN HEAP
    min_heap = []
    for val in [5, 3, 8, 1, 4]:
        heapq.heappush(min_heap, val)

    print("Min heap top:", min_heap[0])           # 1 — peek O(1)
    print("Pop min:", heapq.heappop(min_heap))     # 1 — O(log n)

    # MAX HEAP (negate values)
    max_heap = []
    for val in [5, 3, 8, 1, 4]:
        heapq.heappush(max_heap, -val)

    print("Max heap top:", -max_heap[0])           # 8
    print("Pop max:", -heapq.heappop(max_heap))    # 8

    # heapify existing list in O(n)
    arr = [5, 3, 8, 1, 4]
    heapq.heapify(arr)  # converts in-place to min-heap
    print("Heapified:", arr)

# ================================================================
# KTH LARGEST / SMALLEST — Most Common Interview Pattern
# ================================================================

def kth_largest_brute(nums: List[int], k: int) -> int:
    """
    APPROACH 1 (Sort): O(n log n)
    """
    return sorted(nums, reverse=True)[k - 1]

def kth_largest_heap(nums: List[int], k: int) -> int:
    """
    APPROACH 2 (Min Heap of size k): O(n log k)

    INTERVIEW SCRIPT:
    "Maintain a min-heap of size k.
     Heap contains the k largest elements seen so far.
     Heap top = smallest among top-k = kth largest.
     When heap exceeds size k, pop the minimum.
     Final heap top is the answer.
     O(n log k) — much better than O(n log n) sort when k << n."
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # remove smallest
    return heap[0]  # smallest of top-k = kth largest

def kth_largest_quickselect(nums: List[int], k: int) -> int:
    """
    APPROACH 3 (QuickSelect): O(n) average, O(n²) worst

    INTERVIEW SCRIPT:
    "QuickSelect is like QuickSort but only recurse on one side.
     We want kth largest = (n-k)th smallest position.
     After partition, if pivot position = target: found!
     If pivot > target: recurse left.
     If pivot < target: recurse right.
     O(n) average time."
    """
    import random
    k = len(nums) - k  # convert to kth smallest (0-indexed)

    def quickselect(left, right):
        pivot = nums[right]
        p = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]
                p += 1
        nums[p], nums[right] = nums[right], nums[p]

        if p == k:
            return nums[p]
        elif p < k:
            return quickselect(p + 1, right)
        else:
            return quickselect(left, p - 1)

    return quickselect(0, len(nums) - 1)

# ================================================================
# TOP K FREQUENT ELEMENTS
# ================================================================

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    O(n log k) with heap

    INTERVIEW SCRIPT:
    "Count frequencies with hash map.
     Use min-heap of size k on (frequency, element).
     When heap exceeds k, pop the least frequent.
     Final heap = top k frequent elements."
    """
    freq = defaultdict(int)
    for num in nums:
        freq[num] += 1

    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for _, num in heap]

# ================================================================
# K CLOSEST POINTS TO ORIGIN
# ================================================================

def k_closest_points(points: List[List[int]], k: int) -> List[List[int]]:
    """
    K points closest to origin (0,0)
    O(n log k) with max-heap

    INTERVIEW SCRIPT:
    "Distance = sqrt(x²+y²), but we can compare squared distances.
     Use max-heap of size k.
     Push (distance, point). If heap > k, pop the farthest.
     Max heap: negate distance.
     Final heap = k closest points."
    """
    heap = []
    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, x, y))  # max heap via negation
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]

# ================================================================
# FIND MEDIAN FROM DATA STREAM
# ================================================================

class MedianFinder:
    """
    Find median from a data stream.
    Two heaps: max-heap (lower half) + min-heap (upper half)

    INVARIANT:
    - lower half in max_heap (top = max of lower)
    - upper half in min_heap (top = min of upper)
    - sizes differ by at most 1

    INTERVIEW SCRIPT:
    "This is the classic two-heap solution.
     Lower half in max-heap, upper half in min-heap.
     Median: if equal sizes, average of two tops.
              if unequal, top of larger heap.
     On insert: maintain size balance.
     All operations O(log n)."
    """
    def __init__(self):
        self.lo = []  # max-heap (lower half) — store negated
        self.hi = []  # min-heap (upper half)

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)  # push to max-heap
        heapq.heappush(self.hi, -heapq.heappop(self.lo))  # balance

        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0

# ================================================================
# HEAP SORT
# ================================================================

def heap_sort(arr: List[int]) -> List[int]:
    """
    Heap sort — O(n log n) time, O(1) space
    In-place sorting using max-heap

    INTERVIEW SCRIPT:
    "Two phases:
     1. Build max-heap from array: O(n) using heapify.
     2. Repeatedly extract max, place at end: O(n log n).
     Total: O(n log n), in-place O(1) space."
    """
    n = len(arr)

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    # Build max-heap: O(n)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements: O(n log n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # move max to end
        heapify(arr, n, 0)  # re-heapify reduced heap

    return arr

# ================================================================
# TASK SCHEDULER
# ================================================================

def task_scheduler(tasks: List[str], n: int) -> int:
    """
    Min time to finish all tasks with cooldown n.
    O(m log m) where m = unique tasks

    INTERVIEW SCRIPT:
    "Greedily execute most frequent task.
     After executing, it must cool down for n periods.
     Use max-heap on (frequency, task).
     Use a queue to track cooling tasks.
     Each round: execute from heap if available, else idle."
    """
    from collections import Counter
    freq = Counter(tasks)
    heap = [-f for f in freq.values()]
    heapq.heapify(heap)

    time = 0
    cooling = deque()  # (available_at, freq_remaining)

    from collections import deque

    while heap or cooling:
        time += 1
        if heap:
            freq_remaining = 1 + heapq.heappop(heap)  # -(-f)+1 = f-1 → negate
            # Actually: pop gives -f, so remaining = -(-f) - 1 = f - 1
            freq_remaining = heapq.heappop(heap) + 1  # +1 because heap stores -freq
            # Wait, let me redo: heap has -freq, pop gives -f, +1 makes -(f-1)
            new_freq = heapq.heappop(heap) + 1  # -(f-1) — still negative if f > 1
            if new_freq < 0:
                cooling.append((time + n, new_freq))
        if cooling and cooling[0][0] <= time:
            heapq.heappush(heap, cooling.popleft()[1])

    return time

def task_scheduler_math(tasks: List[str], n: int) -> int:
    """
    O(m) mathematical approach — cleaner

    INTERVIEW SCRIPT:
    "Key formula: result = max(len(tasks), (max_freq-1)*(n+1) + count_max_freq)
     (max_freq-1)*(n+1): frames of n+1 slots, each with max-freq task
     +count_max_freq: final partial frame
     Take max with len(tasks) in case no idling needed."
    """
    from collections import Counter
    freq = Counter(tasks)
    max_freq = max(freq.values())
    count_max = sum(1 for f in freq.values() if f == max_freq)
    return max(len(tasks), (max_freq - 1) * (n + 1) + count_max)

# ================================================================
# MERGE K SORTED LISTS
# ================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_sorted(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists — O(n log k)

    INTERVIEW SCRIPT:
    "Use min-heap of size k, one element per list.
     Pop minimum, add to result.
     Push next element from that list.
     n total elements, each heap op is O(log k)."
    """
    dummy = ListNode(0)
    curr = dummy
    heap = []

    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next

# ================================================================
# FURTHEST BUILDING YOU CAN REACH
# ================================================================

def furthest_building(heights: List[int], bricks: int, ladders: int) -> int:
    """
    Use ladders for largest climbs, bricks for small climbs.
    Greedy + Min Heap — O(n log k) where k = ladders

    INTERVIEW SCRIPT:
    "Use ladders for the largest height differences.
     We don't know future climbs, so be greedy with a min-heap:
     Store all climbs made with ladders.
     If we exceed ladder count, swap out the smallest ladder use
     with bricks instead. If not enough bricks, can't proceed."
    """
    heap = []  # min-heap of climbs using ladders
    brick_remaining = bricks

    for i in range(len(heights) - 1):
        diff = heights[i+1] - heights[i]
        if diff <= 0:
            continue
        heapq.heappush(heap, diff)
        if len(heap) > ladders:  # used too many ladders
            smallest_ladder_use = heapq.heappop(heap)
            brick_remaining -= smallest_ladder_use
            if brick_remaining < 0:
                return i
    return len(heights) - 1

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Heaps are used when:
- Need top-k elements efficiently (avoid sorting everything)
- Continuous stream of data, maintain running statistics
- Priority-based scheduling (OS task scheduler)
- Graph algorithms: Dijkstra's shortest path
- Merge k sorted arrays/files (external sorting)
- Finding median in a stream
- Event-driven simulation (process events by time)
"""

if __name__ == "__main__":
    heap_demo()
    print("\nKth largest (k=2) [3,2,1,5,6,4]:", kth_largest_heap([3,2,1,5,6,4], 2))
    print("Top 2 frequent [1,1,1,2,2,3]:", top_k_frequent([1,1,1,2,2,3], 2))

    mf = MedianFinder()
    for num in [1, 2]:
        mf.addNum(num)
    print("Median of [1,2]:", mf.findMedian())
    mf.addNum(3)
    print("Median of [1,2,3]:", mf.findMedian())

    print("Heap sort [5,3,8,1,4]:", heap_sort([5,3,8,1,4]))
    print("Task scheduler 'AABABC' n=2:", task_scheduler_math(list("AABABC"), 2))
    print("Furthest building [4,2,7,6,9,14,12] bricks=5 ladders=1:",
          furthest_building([4,2,7,6,9,14,12], 5, 1))
