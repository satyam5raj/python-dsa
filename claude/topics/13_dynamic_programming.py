"""
================================================================
TOPIC 13: DYNAMIC PROGRAMMING — MOST IMPORTANT
================================================================
Memoization (Top-Down) vs Tabulation (Bottom-Up)
State Definition is the KEY challenge.

INTERVIEW COMMUNICATION:
"This has overlapping subproblems and optimal substructure → DP.
 Step 1: Define state — dp[i] means...
 Step 2: Find recurrence — dp[i] = f(dp[i-1], ...)
 Step 3: Base cases
 Step 4: Fill order (bottom-up) or memoize (top-down)"
================================================================
"""

from typing import List
from functools import lru_cache

# ================================================================
# 1D DP PROBLEMS
# ================================================================

def climbing_stairs_brute(n: int) -> int:
    """
    Ways to climb n stairs (1 or 2 at a time).
    APPROACH 1 (Naive): O(2ⁿ) — exponential, like Fibonacci
    """
    if n <= 2:
        return n
    return climbing_stairs_brute(n-1) + climbing_stairs_brute(n-2)

def climbing_stairs_dp(n: int) -> int:
    """
    APPROACH 2: Bottom-up DP — O(n) time, O(n) space
    APPROACH 3: Space optimized — O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "State: dp[i] = number of ways to reach step i.
     Recurrence: dp[i] = dp[i-1] + dp[i-2]
     (from i-1 take 1 step, or from i-2 take 2 steps)
     Base: dp[1]=1, dp[2]=2.
     This is exactly Fibonacci!"
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def house_robber(nums: List[int]) -> int:
    """
    Max rob without adjacent houses.
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "State: dp[i] = max money from first i houses.
     Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
     (skip i-th house OR rob i-th house = skip i-1).
     Optimize: only need prev two values."
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = 0, 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1

def house_robber_ii(nums: List[int]) -> int:
    """
    Houses in a circle — can't rob first AND last.
    O(n) — run house robber twice

    INTERVIEW SCRIPT:
    "Since first and last are adjacent, solve two sub-problems:
     1. Rob from house 0 to n-2 (exclude last)
     2. Rob from house 1 to n-1 (exclude first)
     Answer = max of both."
    """
    def rob(arr):
        prev2 = prev1 = 0
        for num in arr:
            prev2, prev1 = prev1, max(prev1, prev2 + num)
        return prev1

    return max(nums[0], rob(nums[:-1]), rob(nums[1:]))

# ================================================================
# COIN CHANGE
# ================================================================

def coin_change_brute(coins: List[int], amount: int) -> int:
    """APPROACH 1: Brute force recursion — O(S^n) where S=amount, n=coins"""
    def helper(remaining):
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')
        return 1 + min(helper(remaining - c) for c in coins)
    result = helper(amount)
    return result if result != float('inf') else -1

def coin_change_dp(coins: List[int], amount: int) -> int:
    """
    APPROACH 2: Bottom-up DP — O(amount * len(coins))

    INTERVIEW SCRIPT:
    "State: dp[i] = min coins to make amount i.
     Recurrence: dp[i] = min(dp[i - coin] + 1) for each coin.
     Base: dp[0] = 0, dp[i] = infinity initially.
     Build up from amount 0 to target."
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1

    return dp[amount] if dp[amount] != float('inf') else -1

def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    Coin Change II — number of ways (not minimum count).
    O(amount * len(coins))

    INTERVIEW SCRIPT:
    "This is the Unbounded Knapsack pattern.
     dp[i] = number of ways to make amount i.
     For each coin, for each amount:
     dp[i] += dp[i - coin]
     Order matters: coins outer loop (avoids counting order variations)."
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # one way to make 0

    for coin in coins:          # coin outer → combinations (not permutations)
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]

# ================================================================
# LONGEST INCREASING SUBSEQUENCE (LIS)
# ================================================================

def lis_brute(nums: List[int]) -> int:
    """APPROACH 1: O(2ⁿ) — check all subsequences"""
    n = len(nums)
    result = [1]

    def helper(prev, curr):
        if curr == n:
            return 0
        taken = 0
        if nums[curr] > prev:
            taken = 1 + helper(nums[curr], curr + 1)
        not_taken = helper(prev, curr + 1)
        return max(taken, not_taken)

    return helper(float('-inf'), 0)

def lis_dp(nums: List[int]) -> int:
    """
    APPROACH 2: O(n²) DP

    INTERVIEW SCRIPT:
    "State: dp[i] = LIS ending at index i.
     Recurrence: dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i].
     Base: dp[i] = 1 (each element is LIS of length 1).
     Answer = max(dp)."
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

def lis_binary_search(nums: List[int]) -> int:
    """
    APPROACH 3: O(n log n) with patience sorting + binary search

    INTERVIEW SCRIPT:
    "Maintain 'tails' array where tails[i] = smallest tail element
     of all increasing subsequences of length i+1.
     For each number:
     - If larger than all tails: extend longest subsequence.
     - Otherwise: replace the first tail >= number (binary search).
     Length of tails = LIS length."
    """
    import bisect
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)

# ================================================================
# LONGEST COMMON SUBSEQUENCE (LCS)
# ================================================================

def lcs_brute(s1: str, s2: str) -> int:
    """APPROACH 1: O(2^(m+n)) brute force"""
    def helper(i, j):
        if i == len(s1) or j == len(s2):
            return 0
        if s1[i] == s2[j]:
            return 1 + helper(i+1, j+1)
        return max(helper(i+1, j), helper(i, j+1))
    return helper(0, 0)

def lcs_dp(s1: str, s2: str) -> int:
    """
    APPROACH 2: O(m * n) DP — classic 2D DP

    INTERVIEW SCRIPT:
    "State: dp[i][j] = LCS of s1[:i] and s2[:j].
     Recurrence:
       If s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
       Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
     Base: dp[0][j] = dp[i][0] = 0 (empty string)."
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

# ================================================================
# EDIT DISTANCE
# ================================================================

def edit_distance(word1: str, word2: str) -> int:
    """
    Minimum operations (insert, delete, replace) to convert word1 to word2.
    O(m * n) time and space

    INTERVIEW SCRIPT:
    "State: dp[i][j] = min ops to convert word1[:i] to word2[:j].
     If chars match: dp[i][j] = dp[i-1][j-1] (no op needed).
     Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
     (delete, insert, replace respectively).
     Base: dp[i][0] = i, dp[0][j] = j."
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # delete
                                    dp[i][j-1],    # insert
                                    dp[i-1][j-1])  # replace
    return dp[m][n]

# ================================================================
# 0/1 KNAPSACK
# ================================================================

def knapsack_brute(weights: List[int], values: List[int], capacity: int) -> int:
    """APPROACH 1: O(2ⁿ) — try all subsets"""
    n = len(weights)
    def helper(i, remaining):
        if i == n or remaining == 0:
            return 0
        if weights[i] > remaining:
            return helper(i + 1, remaining)
        return max(helper(i + 1, remaining),
                   values[i] + helper(i + 1, remaining - weights[i]))
    return helper(0, capacity)

def knapsack_dp(weights: List[int], values: List[int], capacity: int) -> int:
    """
    APPROACH 2: O(n * capacity) DP

    INTERVIEW SCRIPT:
    "State: dp[i][w] = max value using first i items with capacity w.
     Recurrence:
       Don't take item i: dp[i][w] = dp[i-1][w]
       Take item i (if fits): dp[i][w] = values[i] + dp[i-1][w-weights[i]]
       Take max of both.
     Space optimization: use 1D array, iterate right to left."
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):  # right to left!
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])

    return dp[capacity]

# ================================================================
# PARTITION EQUAL SUBSET SUM
# ================================================================

def can_partition(nums: List[int]) -> bool:
    """
    Can array be partitioned into two equal sum subsets?
    Reduces to: find subset with sum = total/2
    O(n * sum) — 0/1 Knapsack variant

    INTERVIEW SCRIPT:
    "Total sum must be even (else impossible).
     Target = total/2.
     dp[j] = True if subset sums to j.
     For each num: dp[j] |= dp[j - num] (right to left)."
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2

    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for j in range(target, num - 1, -1):  # right to left
            dp[j] = dp[j] or dp[j - num]

    return dp[target]

# ================================================================
# DP ON GRIDS
# ================================================================

def unique_paths(m: int, n: int) -> int:
    """
    Count unique paths from top-left to bottom-right (right/down only).
    O(m * n) DP

    INTERVIEW SCRIPT:
    "dp[i][j] = paths to reach cell (i,j).
     dp[i][j] = dp[i-1][j] + dp[i][j-1] (came from top or left).
     Optimization: only need previous row → O(n) space."
    """
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[n-1]

def minimum_path_sum(grid: List[List[int]]) -> int:
    """
    Minimum sum path from top-left to bottom-right.
    O(m * n)

    INTERVIEW SCRIPT:
    "dp[i][j] = min cost to reach (i,j).
     dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])."
    """
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j-1]
            elif j == 0:
                grid[i][j] += grid[i-1][j]
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
    return grid[m-1][n-1]

# ================================================================
# BURST BALLOONS (Hard)
# ================================================================

def max_coins(nums: List[int]) -> int:
    """
    Burst all balloons, maximize coins collected.
    O(n³) — interval DP

    INTERVIEW SCRIPT:
    "KEY INSIGHT: think of which balloon to burst LAST in a range [i,j].
     If k is the last burst in [i,j]:
     coins = nums[i-1] * nums[k] * nums[j+1] + dp[i][k-1] + dp[k+1][j]
     We extend nums with 1s on both sides.
     Build dp for increasing interval lengths."
    """
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    nums[left] * nums[k] * nums[right] + dp[left][k] + dp[k][right]
                )
    return dp[0][n-1]

# ================================================================
# DECODE WAYS
# ================================================================

def decode_ways(s: str) -> int:
    """
    Number of ways to decode a digit string.
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "dp[i] = ways to decode s[:i].
     Single digit s[i-1]: if not '0', dp[i] += dp[i-1].
     Double digit s[i-2:i]: if 10-26, dp[i] += dp[i-2]."
    """
    if not s or s[0] == '0':
        return 0
    n = len(s)
    prev2, prev1 = 1, 1

    for i in range(1, n):
        curr = 0
        if s[i] != '0':
            curr += prev1
        two_digit = int(s[i-1:i+1])
        if 10 <= two_digit <= 26:
            curr += prev2
        prev2, prev1 = prev1, curr

    return prev1

# ================================================================
# DP PATTERNS SUMMARY
# ================================================================
"""
DP PATTERNS TO RECOGNIZE:

1. Linear DP (1D): Fibonacci, Climbing stairs, House robber
   dp[i] depends on dp[i-1], dp[i-2]

2. Interval DP: Burst balloons, Matrix chain multiplication
   dp[l][r] = optimal for range [l, r]

3. Knapsack (0/1): Partition equal subset, target sum
   dp[j] = consider each item, update right to left

4. Unbounded Knapsack: Coin change, coin change ways
   dp[j] = consider each item, update left to right

5. Subsequence DP (2D): LCS, Edit distance, Wildcard matching
   dp[i][j] = optimal for s1[:i] and s2[:j]

6. Grid DP: Unique paths, minimum path sum
   dp[i][j] = optimal for cell (i,j)

7. Tree DP: House robber III, binary tree camera
   dfs returns (with_node, without_node)

SIGNS YOU NEED DP:
- "Count number of ways..."
- "Find minimum/maximum..."
- "Is it possible..."
- Overlapping subproblems (same computation repeated)
- Optimal substructure (optimal solution from optimal subproblems)
"""

if __name__ == "__main__":
    print("Climbing stairs(5):", climbing_stairs_dp(5))
    print("House robber [2,7,9,3,1]:", house_robber([2,7,9,3,1]))
    print("Coin change [1,5,11] amount=15:", coin_change_dp([1,5,11], 15))
    print("LIS [10,9,2,5,3,7,101,18]:", lis_dp([10,9,2,5,3,7,101,18]))
    print("LCS 'ABCBDAB' 'BDCAB':", lcs_dp("ABCBDAB", "BDCAB"))
    print("Edit distance 'horse' 'ros':", edit_distance("horse", "ros"))
    print("Knapsack:", knapsack_dp([1,3,4,5],[1,4,5,7], 7))
    print("Can partition [1,5,11,5]:", can_partition([1,5,11,5]))
    print("Unique paths 3x7:", unique_paths(3, 7))
    print("Decode ways '226':", decode_ways("226"))
    print("Burst balloons [3,1,5,8]:", max_coins([3,1,5,8]))
