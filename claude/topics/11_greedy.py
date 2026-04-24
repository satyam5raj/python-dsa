"""
================================================================
TOPIC 11: GREEDY ALGORITHMS
================================================================
Make locally optimal choices at each step, hoping for global optimal.

INTERVIEW COMMUNICATION:
"Greedy works here because the problem has the 'greedy choice property':
 a locally optimal choice leads to a globally optimal solution.
 I need to justify WHY greedy works (exchange argument or induction).
 Then implement: sort by some criterion, then make greedy picks."
================================================================
"""

from typing import List
import heapq

# ================================================================
# ACTIVITY SELECTION / INTERVAL SCHEDULING
# ================================================================

def activity_selection(start: List[int], end: List[int]) -> int:
    """
    Maximum non-overlapping activities.
    O(n log n) — sort by end time

    INTERVIEW SCRIPT:
    "Greedy: always pick activity that ends earliest.
     WHY? It leaves maximum time for future activities.
     Sort by end time. For each activity:
     If its start >= last selected end → select it."

    USE CASE: Meeting room scheduling, job scheduling
    """
    activities = sorted(zip(start, end), key=lambda x: x[1])
    count = 0
    last_end = float('-inf')

    for s, e in activities:
        if s >= last_end:
            count += 1
            last_end = e
    return count

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge all overlapping intervals.
    O(n log n)

    INTERVIEW SCRIPT:
    "Sort by start time. Iterate: if current overlaps with last merged
     (curr_start <= last_end), extend last merged.
     Otherwise, add as new interval."

    USE CASE: Calendar apps, genome analysis (overlapping gene segments)
    """
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= result[-1][1]:  # overlap
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result

def minimum_meeting_rooms(intervals: List[List[int]]) -> int:
    """
    Minimum meeting rooms needed.

    APPROACH 1 (Sort + Heap): O(n log n)
    APPROACH 2 (Events): O(n log n)

    INTERVIEW SCRIPT:
    "Sort by start time. Use a min-heap of end times.
     For each meeting: if heap top <= current start → room is free, reuse.
     Otherwise → need new room.
     Heap size = rooms in use at any moment."
    """
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []  # min-heap of end times

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)  # reuse room
        else:
            heapq.heappush(heap, end)     # new room

    return len(heap)

# ================================================================
# JUMP GAME
# ================================================================

def can_jump(nums: List[int]) -> bool:
    """
    Can you reach the last index?
    O(n) — greedy on max reachable index

    APPROACH 1 (DP): O(n) time, O(n) space
    APPROACH 2 (Greedy): O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Track the farthest reachable index.
     At each position i, if i > max_reach: can't proceed (return False).
     Update max_reach = max(max_reach, i + nums[i]).
     If we process all positions: return True."
    """
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True

def jump_game_min_jumps(nums: List[int]) -> int:
    """
    Minimum jumps to reach last index.
    O(n) — greedy with BFS-like thinking

    INTERVIEW SCRIPT:
    "Think in 'levels': how far can we reach from current level?
     curr_end: end of current jump's reach.
     curr_farthest: farthest we can reach from current level.
     When we pass curr_end: take a jump, update curr_end.
     Count = number of jumps taken."
    """
    jumps = curr_end = curr_farthest = 0
    for i in range(len(nums) - 1):
        curr_farthest = max(curr_farthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = curr_farthest
    return jumps

# ================================================================
# GAS STATION
# ================================================================

def can_complete_circuit(gas: List[int], cost: List[int]) -> int:
    """
    Find starting gas station to complete the circuit.
    O(n) — greedy

    INTERVIEW SCRIPT:
    "Key insights:
     1. If total gas >= total cost, a solution always exists.
     2. If we run out of gas at station i, stations 0..i can't be start.
        Reset start to i+1.
     WHY? If we can't reach i from start j (j < i),
          any intermediate station also can't reach i."
    """
    total_tank = curr_tank = 0
    start = 0

    for i, (g, c) in enumerate(zip(gas, cost)):
        gain = g - c
        total_tank += gain
        curr_tank += gain
        if curr_tank < 0:
            start = i + 1
            curr_tank = 0

    return start if total_tank >= 0 else -1

# ================================================================
# ASSIGN COOKIES
# ================================================================

def assign_cookies(g: List[int], s: List[int]) -> int:
    """
    Maximum number of content children.
    O(n log n + m log m)

    INTERVIEW SCRIPT:
    "Greedy: satisfy least greedy child with smallest sufficient cookie.
     Sort both arrays. Use two pointers.
     If smallest cookie satisfies least greedy child: pair them.
     Otherwise: move to next cookie."
    """
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    return child

# ================================================================
# CANDY DISTRIBUTION
# ================================================================

def candy(ratings: List[int]) -> int:
    """
    Distribute minimum candies such that:
    - Each child gets at least 1
    - Higher rating than neighbor → more candy
    O(n) — two-pass greedy

    INTERVIEW SCRIPT:
    "Two-pass approach:
     Pass 1 (left to right): if rating[i] > rating[i-1] → candy[i] = candy[i-1]+1 else 1.
     Pass 2 (right to left): if rating[i] > rating[i+1] → candy[i] = max(candy[i], candy[i+1]+1).
     WHY two passes? Need to satisfy both left and right neighbors."
    """
    n = len(ratings)
    candies = [1] * n

    # Left to right
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Right to left
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)

# ================================================================
# PARTITION LABELS
# ================================================================

def partition_labels(s: str) -> List[int]:
    """
    Partition string into as many parts as possible where
    each letter appears in at most one part.
    O(n)

    INTERVIEW SCRIPT:
    "For each character, find its last occurrence.
     Track the farthest end of current partition.
     When current index == partition end: cut here.
     This greedily extends current partition only as needed."
    """
    last = {c: i for i, c in enumerate(s)}
    result = []
    start = end = 0

    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            result.append(end - start + 1)
            start = i + 1

    return result

# ================================================================
# HUFFMAN CODING (Conceptual)
# ================================================================

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encoding(text: str):
    """
    Greedy compression algorithm — O(n log n)

    INTERVIEW SCRIPT:
    "Huffman coding: assign shorter codes to more frequent characters.
     Build a priority queue of (frequency, node).
     Greedily: pop two lowest frequency nodes,
     combine them into a new node with combined frequency,
     push back.
     Repeat until one node remains (the root).
     Left edge = 0, right edge = 1.
     Frequent chars get shorter paths from root."
    """
    from collections import Counter
    freq = Counter(text)

    heap = [HuffmanNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    root = heap[0]
    codes = {}

    def build_codes(node, code=""):
        if node.char is not None:
            codes[node.char] = code or "0"
            return
        build_codes(node.left, code + "0")
        build_codes(node.right, code + "1")

    build_codes(root)
    return codes

# ================================================================
# INTERVAL SCHEDULING MAXIMIZATION
# ================================================================

def non_overlapping_intervals(intervals: List[List[int]]) -> int:
    """
    Minimum intervals to remove to make rest non-overlapping.
    O(n log n)

    INTERVIEW SCRIPT:
    "Equivalent to: find max non-overlapping intervals, remove rest.
     Sort by END time (greedy: finish earliest, leave room for more).
     If current overlaps with last kept: remove current (remove = increment count).
     If no overlap: keep current, update end."
    """
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    remove = 0
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start < last_end:  # overlap
            remove += 1       # remove current interval
        else:
            last_end = end    # keep current, update end
    return remove

# ================================================================
# STOCK PROBLEMS
# ================================================================

def max_profit_one_transaction(prices: List[int]) -> int:
    """
    Best time to buy and sell stock (one transaction).
    O(n) — greedy track minimum

    INTERVIEW SCRIPT:
    "Track minimum buy price seen so far.
     At each price, max profit = current_price - min_price_so_far.
     Update running maximum profit."
    """
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

def max_profit_unlimited(prices: List[int]) -> int:
    """
    Best time with unlimited transactions.
    O(n) — collect every upward move

    INTERVIEW SCRIPT:
    "With unlimited transactions, collect every positive day-over-day gain.
     Greedy: if tomorrow is higher, buy today and sell tomorrow."
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Greedy algorithms work when:
✅ Problem has greedy choice property (local optimal → global optimal)
✅ Problem has optimal substructure

Proving greedy correctness:
- Exchange argument: show swapping greedy choice with any other
  choice doesn't improve result
- Induction: show greedy is at least as good as any other strategy

Real-world applications:
- Dijkstra's algorithm (shortest path)
- Prim's/Kruskal's (minimum spanning tree)
- Huffman coding (data compression)
- Job/task scheduling
- Network routing
- Fractional Knapsack
"""

if __name__ == "__main__":
    print("Activity selection:", activity_selection([1, 3, 0, 5, 8, 5], [2, 4, 6, 7, 9, 9]))
    print("Merge intervals [[1,3],[2,6],[8,10],[15,18]]:",
          merge_intervals([[1,3],[2,6],[8,10],[15,18]]))
    print("Can jump [2,3,1,1,4]:", can_jump([2,3,1,1,4]))
    print("Min jumps [2,3,1,1,4]:", jump_game_min_jumps([2,3,1,1,4]))
    print("Gas station:", can_complete_circuit([1,2,3,4,5], [3,4,5,1,2]))
    print("Candy [1,0,2]:", candy([1,0,2]))
    print("Partition labels 'ababcbacadefegdehijhklij':",
          partition_labels("ababcbacadefegdehijhklij"))
    print("Huffman 'aabbbcccc':", huffman_encoding("aabbbcccc"))
