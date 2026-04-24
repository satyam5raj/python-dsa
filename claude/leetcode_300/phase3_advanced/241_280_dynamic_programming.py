"""
================================================================
LEETCODE PHASE 3 (Problems 241-280): DYNAMIC PROGRAMMING
================================================================
"""

from typing import List
from functools import lru_cache
import bisect

# ================================================================
# 241. CLIMBING STAIRS (Easy)
# ================================================================
def climb_stairs_memo(n: int) -> int:
    """
    APPROACH 1: Memoization — O(n) time and space

    INTERVIEW SCRIPT:
    "Classic DP. climb(n) = climb(n-1) + climb(n-2).
     Base cases: n<=2 → n ways. Fibonacci sequence essentially."
    """
    memo = {}
    def dp(i):
        if i <= 2: return i
        if i in memo: return memo[i]
        memo[i] = dp(i-1) + dp(i-2)
        return memo[i]
    return dp(n)

def climb_stairs(n: int) -> int:
    """APPROACH 2: O(n) time, O(1) space — two variables"""
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n+1): a, b = b, a+b
    return b

# ================================================================
# 242. HOUSE ROBBER (Medium)
# ================================================================
def rob(nums: List[int]) -> int:
    """
    APPROACH 1: O(n) DP with array

    INTERVIEW SCRIPT:
    "Can't rob adjacent houses. dp[i] = max money using houses 0..i.
     dp[i] = max(dp[i-1], dp[i-2] + nums[i]).
     Optimize to O(1) space with two variables."
    """
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    prev2, prev1 = 0, 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1

# ================================================================
# 243. HOUSE ROBBER II (Medium)
# ================================================================
def rob_ii(nums: List[int]) -> int:
    """
    INTERVIEW SCRIPT:
    "Circular: house[0] and house[n-1] are adjacent.
     Split into two linear problems:
     1) Rob houses 0..n-2 (exclude last)
     2) Rob houses 1..n-1 (exclude first)
     Answer = max of both. O(n) time, O(1) space."
    """
    def rob_linear(arr):
        prev2, prev1 = 0, 0
        for num in arr:
            prev2, prev1 = prev1, max(prev1, prev2 + num)
        return prev1

    if len(nums) == 1: return nums[0]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

# ================================================================
# 244. COIN CHANGE (Medium)
# ================================================================
def coin_change(coins: List[int], amount: int) -> int:
    """
    APPROACH 1: Bottom-up DP — O(amount * coins)

    INTERVIEW SCRIPT:
    "dp[i] = minimum coins to make amount i.
     For each amount, try all coins: dp[i] = min(dp[i], dp[i-coin]+1).
     Base: dp[0]=0. Initialize with infinity.
     O(amount * len(coins)) time, O(amount) space."
    """
    dp = [float('inf')] * (amount+1)
    dp[0] = 0
    for a in range(1, amount+1):
        for coin in coins:
            if coin <= a: dp[a] = min(dp[a], dp[a-coin]+1)
    return dp[amount] if dp[amount] != float('inf') else -1

def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    322 variant: Count number of ways (unbounded knapsack)

    INTERVIEW SCRIPT:
    "dp[i] = ways to make amount i. For each coin: add dp[i-coin] ways.
     Order matters: iterate amounts outer, coins inner for combinations."
    """
    dp = [0] * (amount+1)
    dp[0] = 1
    for coin in coins:
        for a in range(coin, amount+1):
            dp[a] += dp[a-coin]
    return dp[amount]

# ================================================================
# 245. LONGEST INCREASING SUBSEQUENCE (Medium)
# ================================================================
def length_of_lis_dp(nums: List[int]) -> int:
    """
    APPROACH 1: O(n²) DP

    INTERVIEW SCRIPT:
    "dp[i] = length of LIS ending at index i.
     For each j < i: if nums[j] < nums[i], dp[i] = max(dp[i], dp[j]+1).
     Answer = max(dp)."
    """
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]: dp[i] = max(dp[i], dp[j]+1)
    return max(dp)

def length_of_lis(nums: List[int]) -> int:
    """
    APPROACH 2: O(n log n) — patience sorting with binary search

    INTERVIEW SCRIPT:
    "Maintain 'tails' array: tails[i] = smallest tail of IS with length i+1.
     For each num: binary search in tails for insertion point.
     If larger than all: append (extends longest IS).
     Else: replace (maintains smallest possible tail).
     Length of tails = LIS length."
    """
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails): tails.append(num)
        else: tails[pos] = num
    return len(tails)

# ================================================================
# 246. LONGEST COMMON SUBSEQUENCE (Medium)
# ================================================================
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    APPROACH 1: O(m*n) DP 2D

    INTERVIEW SCRIPT:
    "dp[i][j] = LCS of text1[:i] and text2[:j].
     If chars match: dp[i][j] = dp[i-1][j-1] + 1.
     Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1]).
     Optimize to O(min(m,n)) space with two rows."
    """
    m, n = len(text1), len(text2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# ================================================================
# 247. EDIT DISTANCE (Hard)
# ================================================================
def min_distance(word1: str, word2: str) -> int:
    """
    INTERVIEW SCRIPT:
    "dp[i][j] = min ops to convert word1[:i] to word2[:j].
     If chars match: dp[i][j] = dp[i-1][j-1].
     Else: dp[i][j] = 1 + min(dp[i-1][j-1] (replace), dp[i-1][j] (delete), dp[i][j-1] (insert)).
     O(m*n) time and space. Optimize to O(min(m,n)) with two rows."
    """
    m, n = len(word1), len(word2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# ================================================================
# 248. WORD BREAK (Medium)
# ================================================================
def word_break(s: str, wordDict: List[str]) -> bool:
    """
    APPROACH 1: BFS — O(n² + dict lookup)
    APPROACH 2: DP — O(n²)

    INTERVIEW SCRIPT:
    "dp[i] = can s[:i] be segmented.
     For each end i: try all start j where dp[j]=True and s[j:i] in wordDict.
     Use set for O(1) lookup. O(n² * word_length) overall."
    """
    word_set = set(wordDict)
    dp = [False] * (len(s)+1)
    dp[0] = True
    for i in range(1, len(s)+1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]

# ================================================================
# 249. PARTITION EQUAL SUBSET SUM (Medium)
# ================================================================
def can_partition(nums: List[int]) -> bool:
    """
    APPROACH 1: DP set of possible sums — O(n * sum)

    INTERVIEW SCRIPT:
    "Find subset with sum = total/2 (0/1 knapsack).
     If total is odd → impossible.
     dp = set of achievable sums. For each num: update dp.
     Target = total // 2. O(n * sum) time, O(sum) space."
    """
    total = sum(nums)
    if total % 2: return False
    target = total // 2
    dp = {0}
    for num in nums:
        dp = {s + num for s in dp} | dp
        if target in dp: return True
    return False

# ================================================================
# 250. TARGET SUM (Medium)
# ================================================================
def find_target_sum_ways(nums: List[int], target: int) -> int:
    """
    APPROACH 1: Recursion — O(2^n)
    APPROACH 2: DP with Counter — O(n * sum)

    INTERVIEW SCRIPT:
    "Assign + or - to each number. Count assignments reaching target.
     DP: Counter {sum: ways}. For each num: new_dp = merge +num and -num.
     O(n * range_of_sums) time. Convert to knapsack: let P=pos, N=neg.
     P-N=target, P+N=sum → P=(target+sum)/2. Count subsets with sum P."
    """
    from collections import Counter
    dp = Counter({0: 1})
    for num in nums:
        new_dp = Counter()
        for s, cnt in dp.items():
            new_dp[s+num] += cnt
            new_dp[s-num] += cnt
        dp = new_dp
    return dp[target]

# ================================================================
# 251. UNIQUE PATHS (Medium)
# ================================================================
def unique_paths(m: int, n: int) -> int:
    """
    APPROACH 1: O(m*n) DP
    APPROACH 2: O(min(m,n)) math — C(m+n-2, m-1)

    INTERVIEW SCRIPT:
    "Can only move right or down. dp[i][j] = paths to reach (i,j).
     dp[i][j] = dp[i-1][j] + dp[i][j-1]. First row/col = 1.
     Math: total steps = m+n-2, choose m-1 downs. C(m+n-2, m-1)."
    """
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[n-1]

# ================================================================
# 252. UNIQUE PATHS II (Medium)
# ================================================================
def unique_paths_with_obstacles(grid: List[List[int]]) -> int:
    """
    INTERVIEW SCRIPT:
    "Same as Unique Paths but obstacles block paths.
     dp[j] = 0 if obstacle. Otherwise same recurrence.
     O(m*n) time, O(n) space."
    """
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = 1 if grid[0][0] == 0 else 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1: dp[j] = 0
            elif j > 0: dp[j] += dp[j-1]
    return dp[n-1]

# ================================================================
# 253. MINIMUM PATH SUM (Medium)
# ================================================================
def min_path_sum(grid: List[List[int]]) -> int:
    """
    INTERVIEW SCRIPT:
    "dp[i][j] = min sum to reach (i,j).
     dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]).
     O(m*n) time, O(n) space (one row)."
    """
    m, n = len(grid), len(grid[0])
    dp = grid[0][:]
    for j in range(1, n): dp[j] += dp[j-1]
    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j-1])
    return dp[n-1]

# ================================================================
# 254. BURST BALLOONS (Hard)
# ================================================================
def max_coins(nums: List[int]) -> int:
    """
    APPROACH 1: Brute force — O(n! * n)
    APPROACH 2: Interval DP — O(n³)

    INTERVIEW SCRIPT:
    "Key insight: think in REVERSE — which balloon is burst LAST in range.
     Add sentinel 1s on both sides.
     dp[l][r] = max coins from bursting all balloons between l and r.
     For each k as the last balloon burst: dp[l][r] = max(dp[l][k]+dp[k][r]+nums[l]*nums[k]*nums[r]).
     O(n³) time, O(n²) space."
    """
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0]*n for _ in range(n)]

    for length in range(2, n):
        for l in range(0, n-length):
            r = l + length
            for k in range(l+1, r):
                dp[l][r] = max(dp[l][r], nums[l]*nums[k]*nums[r] + dp[l][k] + dp[k][r])
    return dp[0][n-1]

# ================================================================
# 255. PALINDROMIC SUBSTRINGS (Medium)
# ================================================================
def count_substrings(s: str) -> int:
    """
    APPROACH 1: DP — O(n²)
    APPROACH 2: Expand around center — O(n²) same but simpler

    INTERVIEW SCRIPT:
    "For each center (n odd + n-1 even centers), expand outward.
     Count valid palindromes as we expand.
     O(n²) time, O(1) space — better than DP's O(n²) space."
    """
    count = 0
    def expand(l, r):
        nonlocal count
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1; l -= 1; r += 1
    for i in range(len(s)):
        expand(i, i)    # odd
        expand(i, i+1)  # even
    return count

# ================================================================
# 256. LONGEST PALINDROMIC SUBSTRING (Medium)
# ================================================================
def longest_palindrome(s: str) -> str:
    """
    APPROACH 1: O(n²) — expand around center
    APPROACH 2: O(n) — Manacher's algorithm

    INTERVIEW SCRIPT:
    "Expand around each center. Track best palindrome.
     2n-1 centers: each char + between each pair.
     O(n²) time, O(1) space."
    """
    res, resLen = "", 0
    def expand(l, r):
        nonlocal res, resLen
        while l >= 0 and r < len(s) and s[l] == s[r]: l -= 1; r += 1
        if r - l - 1 > resLen:
            res = s[l+1:r]; resLen = r - l - 1
    for i in range(len(s)):
        expand(i, i); expand(i, i+1)
    return res

# ================================================================
# 257. DECODE WAYS (Medium)
# ================================================================
def num_decodings(s: str) -> int:
    """
    INTERVIEW SCRIPT:
    "dp[i] = ways to decode s[:i].
     One-char decode: s[i-1] in '1'-'9' → dp[i] += dp[i-1].
     Two-char decode: s[i-2:i] in '10'-'26' → dp[i] += dp[i-2].
     O(n) time, O(1) space with two variables."
    """
    if not s or s[0] == '0': return 0
    prev2, prev1 = 1, 1
    for i in range(1, len(s)):
        curr = 0
        if s[i] != '0': curr += prev1
        two = int(s[i-1:i+1])
        if 10 <= two <= 26: curr += prev2
        prev2, prev1 = prev1, curr
    return prev1

# ================================================================
# 258. BEST TIME TO BUY AND SELL STOCK WITH COOLDOWN (Medium)
# ================================================================
def max_profit_cooldown(prices: List[int]) -> int:
    """
    INTERVIEW SCRIPT:
    "States: hold (own stock), sold (just sold, in cooldown), rest (available to buy).
     hold = max(hold, rest - price)   → buy if more profitable
     sold = hold + price              → sell
     rest = max(rest, sold)           → cooldown passed
     O(n) time, O(1) space."
    """
    hold, sold, rest = float('-inf'), 0, 0
    for price in prices:
        prev_sold = sold
        sold = hold + price
        hold = max(hold, rest - price)
        rest = max(rest, prev_sold)
    return max(sold, rest)

# ================================================================
# 259. BEST TIME TO BUY AND SELL STOCK WITH TRANSACTION FEE (Medium)
# ================================================================
def max_profit_with_fee(prices: List[int], fee: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Two states: cash (no stock held), hold (stock held).
     cash = max(cash, hold + price - fee)  → sell
     hold = max(hold, cash - price)        → buy
     O(n) time, O(1) space."
    """
    cash, hold = 0, float('-inf')
    for price in prices:
        cash = max(cash, hold + price - fee)
        hold = max(hold, cash - price)
    return cash

# ================================================================
# 260. MAXIMUM PRODUCT SUBARRAY (Medium)
# ================================================================
def max_product(nums: List[int]) -> int:
    """
    APPROACH 1: O(n²) brute force
    APPROACH 2: O(n) — track min and max

    INTERVIEW SCRIPT:
    "Track both max and min products (negatives can flip).
     curr_max = max(num, curr_max*num, curr_min*num).
     curr_min = min(num, curr_max*num, curr_min*num).
     Update global max. O(n) time, O(1) space."
    """
    res = max(nums)
    curr_min = curr_max = 1
    for num in nums:
        if num == 0: curr_min = curr_max = 1; continue
        prev_max = curr_max
        curr_max = max(num, curr_max*num, curr_min*num)
        curr_min = min(num, prev_max*num, curr_min*num)
        res = max(res, curr_max)
    return res

# ================================================================
# 261. INTEGER BREAK (Medium)
# ================================================================
def integer_break(n: int) -> int:
    """
    APPROACH 1: DP — O(n²)
    APPROACH 2: Math — O(1)

    INTERVIEW SCRIPT:
    "Math: split into 3s as much as possible.
     Never use 1s. If remainder=1: use 2+2 instead of 3+1.
     DP: dp[i] = max product for integer i.
     dp[i] = max over j: max(j, dp[j]) * max(i-j, dp[i-j])."
    """
    if n <= 3: return n - 1
    q, r = divmod(n, 3)
    if r == 0: return 3**q
    if r == 1: return 3**(q-1) * 4
    return 3**q * 2

# ================================================================
# 262. RUSSIAN DOLL ENVELOPES (Hard)
# ================================================================
def max_envelopes(envelopes: List[List[int]]) -> int:
    """
    APPROACH 1: O(n²) DP (similar to LIS)
    APPROACH 2: O(n log n) — sort + patience sort

    INTERVIEW SCRIPT:
    "Sort by width ASC, then height DESC (for same width).
     Why DESC for same width? Prevents using two same-width envelopes.
     Then find LIS on heights only.
     Descending height for same width ensures we pick at most one per width."
    """
    envelopes.sort(key=lambda x: (x[0], -x[1]))
    heights = [e[1] for e in envelopes]
    tails = []
    for h in heights:
        pos = bisect.bisect_left(tails, h)
        if pos == len(tails): tails.append(h)
        else: tails[pos] = h
    return len(tails)

# ================================================================
# 263. DISTINCT SUBSEQUENCES (Hard)
# ================================================================
def num_distinct(s: str, t: str) -> int:
    """
    INTERVIEW SCRIPT:
    "dp[i][j] = ways to form t[:j] from s[:i].
     If s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] + dp[i-1][j].
     Else: dp[i][j] = dp[i-1][j].
     Use 1D array. O(m*n) time, O(n) space."
    """
    m, n = len(s), len(t)
    dp = [0] * (n+1)
    dp[0] = 1
    for c in s:
        for j in range(n, 0, -1):
            if c == t[j-1]: dp[j] += dp[j-1]
    return dp[n]

# ================================================================
# 264. INTERLEAVING STRING (Medium)
# ================================================================
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """
    INTERVIEW SCRIPT:
    "dp[i][j] = can s3[:i+j] be formed by interleaving s1[:i] and s2[:j].
     Transition: dp[i][j] = (dp[i-1][j] and s1[i-1]==s3[i+j-1]) OR (dp[i][j-1] and s2[j-1]==s3[i+j-1]).
     O(m*n) time and space. Optimize to O(n) with 1D DP."
    """
    m, n = len(s1), len(s2)
    if m + n != len(s3): return False
    dp = [False] * (n+1)
    dp[0] = True
    for j in range(1, n+1): dp[j] = dp[j-1] and s2[j-1] == s3[j-1]
    for i in range(1, m+1):
        dp[0] = dp[0] and s1[i-1] == s3[i-1]
        for j in range(1, n+1):
            dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or (dp[j-1] and s2[j-1] == s3[i+j-1])
    return dp[n]

# ================================================================
# 265. REGEX MATCHING (Hard)
# ================================================================
def is_match_regex(s: str, p: str) -> bool:
    """
    APPROACH 1: Recursion — exponential
    APPROACH 2: DP — O(m*n)

    INTERVIEW SCRIPT:
    "dp[i][j] = does s[:i] match p[:j].
     Case 1: p[j-1]='*': match 0 occurrences → dp[i][j-2], OR
             match 1+ occurrences if s[i-1] matches p[j-2] → dp[i-1][j].
     Case 2: s[i-1]==p[j-1] or p[j-1]=='.': dp[i][j] = dp[i-1][j-1].
     O(m*n) time and space."
    """
    m, n = len(s), len(p)
    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True
    for j in range(2, n+1):
        if p[j-1] == '*': dp[0][j] = dp[0][j-2]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-2]  # zero occurrences
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    return dp[m][n]

# ================================================================
# 266. WILDCARD MATCHING (Hard)
# ================================================================
def is_match_wildcard(s: str, p: str) -> bool:
    """
    INTERVIEW SCRIPT:
    "Similar to regex but '*' matches any sequence (including empty).
     dp[i][j] = does s[:i] match p[:j].
     '*' case: dp[i][j] = dp[i-1][j] (match one char) OR dp[i][j-1] (match empty).
     '?' or char match: dp[i][j] = dp[i-1][j-1]."
    """
    m, n = len(s), len(p)
    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True
    for j in range(1, n+1):
        if p[j-1] == '*': dp[0][j] = dp[0][j-1]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
            elif p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    return dp[m][n]

# ================================================================
# 267. STONE GAME (Medium)
# ================================================================
def stone_game(piles: List[int]) -> bool:
    """
    APPROACH 1: DP — O(n²)
    APPROACH 2: Math — O(1)

    INTERVIEW SCRIPT:
    "Alex always wins when n piles is even and total is fixed.
     Proof: Alex can always choose 'odd-indexed' or 'even-indexed' strategy.
     Math insight: return True always (Alex has first-mover advantage).
     DP: dp[i][j] = score diff (Alex-Lee) for piles[i..j].
     dp[i][j] = max(piles[i]-dp[i+1][j], piles[j]-dp[i][j-1])."
    """
    return True  # Alex always wins with optimal play

def stone_game_dp(piles: List[int]) -> bool:
    n = len(piles)
    dp = piles[:]
    for d in range(1, n):
        for i in range(n-d):
            dp[i] = max(piles[i]-dp[i+1], piles[i+d]-dp[i])
    return dp[0] > 0

# ================================================================
# 268. JUMP GAME (Medium)
# ================================================================
def can_jump(nums: List[int]) -> bool:
    """
    APPROACH 1: DP — O(n²)
    APPROACH 2: Greedy — O(n)

    INTERVIEW SCRIPT:
    "Greedy: track furthest reachable index.
     For each position, if we can't reach it → return False.
     Update furthest reach. If we reach last index → True.
     O(n) time, O(1) space."
    """
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach: return False
        max_reach = max(max_reach, i + jump)
    return True

# ================================================================
# 269. JUMP GAME II (Medium)
# ================================================================
def jump(nums: List[int]) -> int:
    """
    APPROACH 1: DP — O(n²)
    APPROACH 2: Greedy BFS — O(n)

    INTERVIEW SCRIPT:
    "Greedy BFS: track current range end and next range end.
     When we reach current range end, increment jumps and extend to next range.
     Like BFS levels. O(n) time, O(1) space."
    """
    jumps = curr_end = furthest = 0
    for i in range(len(nums)-1):
        furthest = max(furthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = furthest
    return jumps

# ================================================================
# 270. MAXIMUM SUM OF NON-ADJACENT (variation)
# ================================================================
def max_sum_non_adjacent(nums: List[int]) -> int:
    """
    INTERVIEW SCRIPT:
    "Same as House Robber. dp[i] = max sum ending at or before i.
     dp[i] = max(dp[i-1], dp[i-2] + nums[i]).
     O(n) time, O(1) space."
    """
    if not nums: return 0
    prev2 = prev1 = 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1

# ================================================================
# 271-280: MORE DP PROBLEMS
# ================================================================

def can_partition_k_subsets(nums: List[int], k: int) -> bool:
    """
    698. Partition to K Equal Sum Subsets

    INTERVIEW SCRIPT:
    "Total must be divisible by k. Target = total/k.
     Backtracking with bitmask DP.
     dp[mask] = remaining sum in current bucket when nums in mask are used.
     O(n * 2^n)."
    """
    total = sum(nums)
    if total % k: return False
    target = total // k
    nums.sort(reverse=True)
    if nums[0] > target: return False

    dp = [-1] * (1 << len(nums))
    dp[0] = 0

    for mask in range(1 << len(nums)):
        if dp[mask] == -1: continue
        for i, num in enumerate(nums):
            if mask & (1 << i): continue
            next_mask = mask | (1 << i)
            if dp[next_mask] != -1: continue
            if (dp[mask] % target) + num <= target:
                dp[next_mask] = dp[mask] + num
    return dp[(1 << len(nums)) - 1] == total

def beautiful_arrangement(n: int) -> int:
    """
    526. Beautiful Arrangement

    INTERVIEW SCRIPT:
    "Backtracking with bitmask DP.
     dp[mask] = arrangements using nums in mask for positions 1..popcount(mask).
     For each mask: try adding each unused number to next position.
     O(n * 2^n) time, O(2^n) space."
    """
    memo = {}
    def backtrack(pos, visited):
        if pos > n: return 1
        if (pos, visited) in memo: return memo[(pos, visited)]
        count = 0
        for i in range(1, n+1):
            if not (visited >> i & 1) and (i % pos == 0 or pos % i == 0):
                count += backtrack(pos+1, visited | (1 << i))
        memo[(pos, visited)] = count
        return count
    return backtrack(1, 0)

def max_vacation_days(flights: List[List[int]], days: List[List[int]]) -> int:
    """
    568. Maximum Vacation Days (Hard)

    INTERVIEW SCRIPT:
    "DP: dp[week][city] = max vacation days after week in city.
     For each week and city: try all cities reachable by flight or stay.
     O(n² * k) where n=cities, k=weeks."
    """
    n, k = len(flights), len(days[0])
    INF = float('-inf')
    dp = [INF] * n
    dp[0] = 0  # start at city 0

    for week in range(k):
        new_dp = [INF] * n
        for to in range(n):
            for frm in range(n):
                if dp[frm] == INF: continue
                if frm == to or flights[frm][to]:
                    new_dp[to] = max(new_dp[to], dp[frm] + days[to][week])
        dp = new_dp
    return max(dp)

def count_vowels_permutation(n: int) -> int:
    """
    1220. Count Vowels Permutation

    INTERVIEW SCRIPT:
    "DP where state is the last vowel.
     Rules: a→e, e→a/i, i→a/e/o/u, o→i/u, u→a.
     dp[v] = strings of length i ending in vowel v.
     O(n) time, O(1) space."
    """
    MOD = 10**9 + 7
    a = e = i = o = u = 1
    for _ in range(n-1):
        a, e, i, o, u = (e + i + u) % MOD, (a + i) % MOD, (e + o) % MOD, i % MOD, (i + o) % MOD
    return (a + e + i + o + u) % MOD

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Climb Stairs 5:", climb_stairs(5))
    print("House Robber [2,7,9,3,1]:", rob([2,7,9,3,1]))
    print("House Robber II [2,3,2]:", rob_ii([2,3,2]))
    print("Coin Change [1,5,11] amount=15:", coin_change([1,5,11], 15))
    print("LIS [10,9,2,5,3,7,101,18]:", length_of_lis([10,9,2,5,3,7,101,18]))
    print("LCS 'abcde' 'ace':", longest_common_subsequence("abcde","ace"))
    print("Edit Distance 'horse' 'ros':", min_distance("horse","ros"))
    print("Word Break 'leetcode' [leet,code]:", word_break("leetcode",["leet","code"]))
    print("Partition Equal Subset [1,5,11,5]:", can_partition([1,5,11,5]))
    print("Max Coins [3,1,5,8]:", max_coins([3,1,5,8]))
    print("Palindromic Substrings 'abc':", count_substrings("abc"))
    print("Longest Palindrome 'babad':", longest_palindrome("babad"))
    print("Decode Ways '226':", num_decodings("226"))
    print("Max Product [-2,3,-4]:", max_product([-2,3,-4]))
    print("Max Profit Cooldown [1,2,3,0,2]:", max_profit_cooldown([1,2,3,0,2]))
    print("Russian Doll [[5,4],[6,4],[6,7],[2,3]]:", max_envelopes([[5,4],[6,4],[6,7],[2,3]]))
    print("Regex 'aa' 'a*':", is_match_regex("aa","a*"))
    print("Jump Game [2,3,1,1,4]:", can_jump([2,3,1,1,4]))
    print("Jump Game II [2,3,1,1,4]:", jump([2,3,1,1,4]))
