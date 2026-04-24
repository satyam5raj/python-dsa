"""
================================================================
TOPIC 16: ADVANCED TOPICS
================================================================
Segment Trees, Fenwick Trees (BIT)
Range queries and updates in O(log n)

INTERVIEW COMMUNICATION:
"For range queries with updates, a segment tree or Fenwick tree
 gives O(log n) for both operations vs O(n) naive.
 Fenwick tree is simpler to implement; segment tree is more flexible."
================================================================
"""

from typing import List, Callable, Any

# ================================================================
# SEGMENT TREE
# ================================================================
"""
Segment Tree: Binary tree where each node stores aggregate (sum, min, max)
for a range of the array.

         [0,7] sum=36
        /              \
    [0,3] sum=10    [4,7] sum=26
    /      \          /       \
 [0,1]  [2,3]     [4,5]    [6,7]
  s=3    s=7       s=9      s=17

Operations:
- Build: O(n)
- Query (range): O(log n)
- Update (point): O(log n)
"""

class SegmentTree:
    """
    Generic segment tree for range sum queries and point updates.

    INTERVIEW SCRIPT:
    "Build: O(n) — bottom-up construction.
     Query: O(log n) — split range into O(log n) nodes.
     Update: O(log n) — update leaf and propagate up.
     4n space for n elements."
    """
    def __init__(self, nums: List[int], fn: Callable = lambda a, b: a + b, default: int = 0):
        self.n = len(nums)
        self.fn = fn         # aggregate function (sum, min, max)
        self.default = default
        self.tree = [default] * (4 * self.n)
        self._build(nums, 0, 0, self.n - 1)

    def _build(self, nums, node, start, end):
        if start == end:
            self.tree[node] = nums[start]
            return
        mid = (start + end) // 2
        self._build(nums, 2*node+1, start, mid)
        self._build(nums, 2*node+2, mid+1, end)
        self.tree[node] = self.fn(self.tree[2*node+1], self.tree[2*node+2])

    def update(self, idx: int, val: int, node=0, start=0, end=None):
        """Point update at index idx — O(log n)"""
        if end is None:
            end = self.n - 1
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(idx, val, 2*node+1, start, mid)
        else:
            self.update(idx, val, 2*node+2, mid+1, end)
        self.tree[node] = self.fn(self.tree[2*node+1], self.tree[2*node+2])

    def query(self, l: int, r: int, node=0, start=0, end=None) -> int:
        """Range query [l, r] — O(log n)"""
        if end is None:
            end = self.n - 1
        if r < start or end < l:
            return self.default  # out of range
        if l <= start and end <= r:
            return self.tree[node]  # fully within range
        mid = (start + end) // 2
        left = self.query(l, r, 2*node+1, start, mid)
        right = self.query(l, r, 2*node+2, mid+1, end)
        return self.fn(left, right)

class SegmentTreeIterative:
    """
    Iterative segment tree — simpler, faster constants.
    Index base: n to 2n-1 are leaves (0-indexed array stored at n+i)

    INTERVIEW SCRIPT:
    "Store tree in array of size 2n.
     Leaves at positions n to 2n-1.
     Parent of i is i//2, children of i are 2i and 2i+1.
     Update: update leaf at n+i, propagate up.
     Query: use two pointers, sum non-overlapping segments."
    """
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.tree = [0] * (2 * self.n)
        # fill leaves
        for i in range(self.n):
            self.tree[self.n + i] = nums[i]
        # fill internal nodes
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def update(self, i: int, val: int) -> None:
        """O(log n)"""
        i += self.n
        self.tree[i] = val
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def query(self, l: int, r: int) -> int:
        """Range sum [l, r] — O(log n)"""
        result = 0
        l += self.n
        r += self.n + 1
        while l < r:
            if l & 1:   # l is right child, include and move right
                result += self.tree[l]; l += 1
            if r & 1:   # r is right child, include left sibling
                r -= 1; result += self.tree[r]
            l >>= 1
            r >>= 1
        return result

# ================================================================
# FENWICK TREE (Binary Indexed Tree)
# ================================================================
"""
Fenwick Tree: More compact than segment tree.
Supports prefix sum queries and point updates in O(log n).
Uses the lowbit trick: i & (-i)

WHEN TO USE:
- Segment tree: range min/max/sum queries, range updates
- Fenwick tree: prefix sum, order statistics (simpler code)
"""

class FenwickTree:
    """
    Prefix sum queries and point updates in O(log n).

    INTERVIEW SCRIPT:
    "Fenwick tree index trick: each index i is responsible for
     a range of length i & (-i) (lowest set bit).
     Update: add to i, then all ancestors (i += i & (-i)).
     Query: sum to i, then go to parent (i -= i & (-i)).
     More memory efficient than segment tree."
    """
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i: int, delta: int) -> None:
        """Add delta to position i (1-indexed) — O(log n)"""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)  # move to next responsible index

    def query(self, i: int) -> int:
        """Prefix sum [1..i] — O(log n)"""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)  # move to parent
        return total

    def range_query(self, l: int, r: int) -> int:
        """Range sum [l..r] — O(log n)"""
        return self.query(r) - self.query(l - 1)

    def build(self, nums: List[int]) -> None:
        """Build from array — O(n log n)"""
        for i, num in enumerate(nums):
            self.update(i + 1, num)

class FenwickTree2D:
    """2D Fenwick tree for 2D prefix sums"""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]

    def update(self, r: int, c: int, delta: int) -> None:
        i = r
        while i <= self.rows:
            j = c
            while j <= self.cols:
                self.tree[i][j] += delta
                j += j & (-j)
            i += i & (-i)

    def query(self, r: int, c: int) -> int:
        total = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                total += self.tree[i][j]
                j -= j & (-j)
            i -= i & (-i)
        return total

    def range_query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (self.query(r2, c2) - self.query(r1-1, c2) -
                self.query(r2, c1-1) + self.query(r1-1, c1-1))

# ================================================================
# RANGE MINIMUM QUERY (Sparse Table — O(1) query, O(n log n) build)
# ================================================================

class SparseTable:
    """
    For static arrays (no updates), sparse table gives O(1) range min/max.

    INTERVIEW SCRIPT:
    "Precompute: st[i][j] = min of 2^j elements starting at i.
     Build: O(n log n). Query: O(1).
     For query [l, r]: find k such that 2^k fits in [l,r].
     Answer = min(st[l][k], st[r-2^k+1][k]) — ranges can overlap for min/max."
    """
    def __init__(self, nums: List[int]):
        import math
        n = len(nums)
        k = int(math.log2(n)) + 1 if n > 0 else 1
        self.table = [[float('inf')] * k for _ in range(n)]
        self.log = [0] * (n + 1)

        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1

        for i in range(n):
            self.table[i][0] = nums[i]

        for j in range(1, k):
            for i in range(n - (1 << j) + 1):
                self.table[i][j] = min(self.table[i][j-1],
                                       self.table[i + (1 << (j-1))][j-1])

    def query_min(self, l: int, r: int) -> int:
        """O(1) range minimum query"""
        k = self.log[r - l + 1]
        return min(self.table[l][k], self.table[r - (1 << k) + 1][k])

# ================================================================
# PRACTICAL APPLICATIONS
# ================================================================

class NumArray:
    """
    Range Sum Query with updates — classic Segment Tree application.

    INTERVIEW SCRIPT:
    "If updates are rare: prefix sum O(1) query, O(n) update.
     If updates are frequent: segment tree O(log n) both."
    """
    def __init__(self, nums: List[int]):
        self.nums = nums
        self.n = len(nums)
        self.bit = FenwickTree(self.n)
        self.bit.build(nums)

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self.bit.update(index + 1, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self.bit.range_query(left + 1, right + 1)

def count_inversions(nums: List[int]) -> int:
    """
    Count inversions in array using Fenwick Tree or Merge Sort.
    An inversion is a pair (i, j) where i < j but nums[i] > nums[j].

    Merge Sort approach: O(n log n)

    INTERVIEW SCRIPT:
    "During merge sort, when we take element from right array
     before elements from left: it forms inversions with all
     remaining left elements."
    """
    count = [0]

    def merge_count(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_count(arr[:mid])
        right = merge_count(arr[mid:])

        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
                count[0] += len(left) - i  # all remaining left > right[j]
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    merge_count(nums)
    return count[0]

# ================================================================
# COMPARISON: WHEN TO USE WHAT
# ================================================================
"""
Data Structure Comparison for Range Queries:
─────────────────────────────────────────────────────────────
Structure     Build    Query    Update   Range Update   Space
─────────────────────────────────────────────────────────────
Prefix Sum    O(n)     O(1)     O(n)     No             O(n)
Segment Tree  O(n)     O(log n) O(log n) Yes (lazy)     O(n)
Fenwick Tree  O(n log n) O(log n) O(log n) Partial     O(n)
Sparse Table  O(n log n) O(1)   N/A      No             O(n log n)
─────────────────────────────────────────────────────────────

Choose:
- No updates, many queries: Sparse Table (O(1) query)
- Updates + sum queries: Fenwick Tree (simpler)
- Updates + min/max/custom: Segment Tree (more flexible)
- Few updates: Prefix Sum (simplest)
"""

if __name__ == "__main__":
    nums = [1, 3, 5, 7, 9, 11]

    # Segment Tree
    st = SegmentTree(nums)
    print("Segment Tree sum [1,3]:", st.query(1, 3))  # 15
    st.update(2, 6)  # change index 2 to 6
    print("After update, sum [0,2]:", st.query(0, 2))  # 10

    # Iterative Segment Tree
    ist = SegmentTreeIterative(nums)
    print("Iterative ST sum [0,2]:", ist.query(0, 2))  # 9

    # Fenwick Tree
    bit = FenwickTree(len(nums))
    bit.build(nums)
    print("Fenwick sum [2,4] (1-indexed → [3,5] original):", bit.range_query(2, 4))  # 15
    bit.update(2, 3)  # add 3 to position 2
    print("Fenwick prefix sum [1,4]:", bit.query(4))

    # NumArray
    na = NumArray([1, 3, 5])
    print("Range sum [0,2]:", na.sumRange(0, 2))  # 9
    na.update(1, 2)
    print("After update, range sum [0,2]:", na.sumRange(0, 2))  # 8

    # Count inversions
    print("Inversions in [8,4,2,1]:", count_inversions([8,4,2,1]))  # 6

    # Sparse Table
    sparse = SparseTable([2, 4, 3, 1, 6, 7, 8, 9, 1, 7])
    print("Range min [2,7]:", sparse.query_min(2, 7))  # 1
