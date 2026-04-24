"""
================================================================
LEETCODE PHASE 3 (Problems 281-300): BACKTRACKING
================================================================
"""

from typing import List
from collections import Counter

# ================================================================
# 281. SUBSETS (Medium)
# ================================================================
def subsets_brute(nums: List[int]) -> List[List[int]]:
    """APPROACH 1: Bitmask — O(n * 2^n)"""
    result = []
    n = len(nums)
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result

def subsets(nums: List[int]) -> List[List[int]]:
    """
    APPROACH 2: Backtracking — O(n * 2^n)

    INTERVIEW SCRIPT:
    "Backtracking decision tree: at each index, include or skip.
     Result has 2^n subsets. O(n * 2^n) — n for copying each subset.
     Iterative: start with [[]], for each num extend all existing subsets."
    """
    result = [[]]
    def backtrack(start, path):
        for i in range(start, len(nums)):
            path.append(nums[i])
            result.append(path[:])
            backtrack(i+1, path)
            path.pop()
    backtrack(0, [])
    return result

# ================================================================
# 282. SUBSETS II (Medium) — with duplicates
# ================================================================
def subsets_with_dup(nums: List[int]) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Sort first to group duplicates.
     Skip duplicate at same recursion level (not same branch).
     If nums[i] == nums[i-1] and i > start: skip.
     O(n * 2^n) — same as Subsets I."
    """
    nums.sort()
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]: continue
            path.append(nums[i])
            backtrack(i+1, path)
            path.pop()
    backtrack(0, [])
    return result

# ================================================================
# 283. PERMUTATIONS (Medium)
# ================================================================
def permutations_brute(nums: List[int]) -> List[List[int]]:
    """APPROACH 1: Use Python itertools (not interview-valid)"""
    from itertools import permutations
    return [list(p) for p in permutations(nums)]

def permute(nums: List[int]) -> List[List[int]]:
    """
    APPROACH 2: Backtracking — O(n! * n)

    INTERVIEW SCRIPT:
    "Swap each element with current position, recurse, swap back.
     n! permutations, each costs O(n) to copy.
     Alternatively: use 'used' boolean array + path building."
    """
    result = []
    def backtrack(start):
        if start == len(nums): result.append(nums[:])
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start+1)
            nums[start], nums[i] = nums[i], nums[start]
    backtrack(0)
    return result

# ================================================================
# 284. PERMUTATIONS II (Medium) — with duplicates
# ================================================================
def permute_unique(nums: List[int]) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Sort + used array. Skip if nums[i]==nums[i-1] and nums[i-1] not used.
     This ensures we always use left duplicate before right.
     O(n! * n) but many branches pruned early."
    """
    nums.sort()
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums): result.append(path[:])
        for i in range(len(nums)):
            if used[i]: continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result

# ================================================================
# 285. COMBINATION SUM (Medium)
# ================================================================
def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Candidates can be reused. DFS with remaining target.
     Prune: if remaining < 0, stop.
     Sort candidates: allows early termination.
     O(n^(T/M)) where T=target, M=min candidate."
    """
    result = []
    candidates.sort()
    def backtrack(start, path, remaining):
        if remaining == 0: result.append(path[:]); return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i, not i+1 (reuse)
            path.pop()
    backtrack(0, [], target)
    return result

# ================================================================
# 286. COMBINATION SUM II (Medium) — no reuse, unique combos
# ================================================================
def combination_sum_ii(candidates: List[int], target: int) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Sort to group duplicates. Each candidate used at most once.
     Skip duplicates at same level: if candidates[i]==candidates[i-1] and i>start: skip.
     O(2^n) — each element included or not."
    """
    candidates.sort()
    result = []
    def backtrack(start, path, remaining):
        if remaining == 0: result.append(path[:]); return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining: break
            if i > start and candidates[i] == candidates[i-1]: continue
            path.append(candidates[i])
            backtrack(i+1, path, remaining - candidates[i])
            path.pop()
    backtrack(0, [], target)
    return result

# ================================================================
# 287. WORD SEARCH (Medium)
# ================================================================
def word_search(board: List[List[str]], word: str) -> bool:
    """
    INTERVIEW SCRIPT:
    "DFS from every cell. Mark visited (in-place: replace with '#').
     4-directional. Backtrack: restore original char.
     O(m*n * 4^L) where L=word length. Pruning helps in practice."
    """
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word): return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]: return False
        temp = board[r][c]
        board[r][c] = '#'
        found = (dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or
                 dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1))
        board[r][c] = temp
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

# ================================================================
# 288. N-QUEENS (Hard)
# ================================================================
def solve_n_queens(n: int) -> List[List[str]]:
    """
    APPROACH 1: Backtracking with sets — O(n!)

    INTERVIEW SCRIPT:
    "Place queen row by row. Track: columns, diagonals (r-c), anti-diagonals (r+c).
     If no conflict: place queen, recurse to next row, backtrack.
     O(n!) — pruning makes it much faster in practice.
     Sets for O(1) conflict check vs O(n)."
    """
    result = []
    board = [['.']*n for _ in range(n)]
    cols = set(); diag1 = set(); diag2 = set()

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2: continue
            board[row][col] = 'Q'
            cols.add(col); diag1.add(row-col); diag2.add(row+col)
            backtrack(row+1)
            board[row][col] = '.'
            cols.discard(col); diag1.discard(row-col); diag2.discard(row+col)

    backtrack(0)
    return result

def total_n_queens(n: int) -> int:
    """N-Queens II — just count solutions"""
    count = [0]
    cols = set(); diag1 = set(); diag2 = set()

    def backtrack(row):
        if row == n: count[0] += 1; return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2: continue
            cols.add(col); diag1.add(row-col); diag2.add(row+col)
            backtrack(row+1)
            cols.discard(col); diag1.discard(row-col); diag2.discard(row+col)

    backtrack(0)
    return count[0]

# ================================================================
# 289. SUDOKU SOLVER (Hard)
# ================================================================
def solve_sudoku(board: List[List[str]]) -> None:
    """
    INTERVIEW SCRIPT:
    "Backtracking: find empty cell, try 1-9.
     Check: not in same row, col, or 3x3 box.
     If valid: place and recurse. If recurse fails: backtrack.
     O(9^(empty cells)) — but many branches pruned early."
    """
    def is_valid(r, c, num):
        for i in range(9):
            if board[r][i] == num: return False
            if board[i][c] == num: return False
            if board[3*(r//3)+i//3][3*(c//3)+i%3] == num: return False
        return True

    def solve():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for num in '123456789':
                        if is_valid(r, c, num):
                            board[r][c] = num
                            if solve(): return True
                            board[r][c] = '.'
                    return False
        return True

    solve()

# ================================================================
# 290. RESTORE IP ADDRESSES (Medium)
# ================================================================
def restore_ip_addresses(s: str) -> List[str]:
    """
    INTERVIEW SCRIPT:
    "Backtracking with 4 parts constraint.
     Each part: 1-3 digits, value 0-255, no leading zeros.
     Prune: remaining string too long or too short for remaining parts.
     O(3^4) = O(81) — very fast, fixed branching."
    """
    result = []

    def backtrack(start, parts):
        if len(parts) == 4 and start == len(s):
            result.append('.'.join(parts))
            return
        if len(parts) == 4 or start == len(s): return
        for length in range(1, 4):
            if start + length > len(s): break
            seg = s[start:start+length]
            if len(seg) > 1 and seg[0] == '0': break  # no leading zeros
            if int(seg) > 255: break
            backtrack(start+length, parts+[seg])

    backtrack(0, [])
    return result

# ================================================================
# 291. PALINDROME PARTITIONING (Medium)
# ================================================================
def partition_palindrome(s: str) -> List[List[str]]:
    """
    APPROACH 1: Backtracking — O(n * 2^n)
    APPROACH 2: Backtracking + DP precompute — O(n² + 2^n)

    INTERVIEW SCRIPT:
    "Backtrack: at each position, try all end indices.
     If s[start:end] is palindrome: recurse on rest.
     Optimize: precompute palindrome table in O(n²).
     is_pal[i][j] in O(1) during backtracking."
    """
    n = len(s)
    # Precompute palindrome table
    is_pal = [[False]*n for _ in range(n)]
    for i in range(n): is_pal[i][i] = True
    for i in range(n-1): is_pal[i][i+1] = (s[i]==s[i+1])
    for length in range(3, n+1):
        for i in range(n-length+1):
            j = i + length - 1
            is_pal[i][j] = s[i]==s[j] and is_pal[i+1][j-1]

    result = []
    def backtrack(start, path):
        if start == n: result.append(path[:]); return
        for end in range(start+1, n+1):
            if is_pal[start][end-1]:
                path.append(s[start:end])
                backtrack(end, path)
                path.pop()
    backtrack(0, [])
    return result

# ================================================================
# 292. LETTER COMBINATIONS PHONE (Medium)
# ================================================================
def letter_combinations(digits: str) -> List[str]:
    """
    INTERVIEW SCRIPT:
    "Map digits to letters. Backtracking: for each digit, try all its letters.
     Result: 4^n combinations in worst case (n digits, max 4 letters each).
     BFS (iterative) works too: start with [''], extend with each digit's letters."
    """
    if not digits: return []
    phone = {'2':'abc','3':'def','4':'ghi','5':'jkl',
             '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    result = []
    def backtrack(idx, path):
        if idx == len(digits): result.append(''.join(path)); return
        for c in phone[digits[idx]]:
            path.append(c); backtrack(idx+1, path); path.pop()
    backtrack(0, [])
    return result

# ================================================================
# 293. GENERATE PARENTHESES (Medium)
# ================================================================
def generate_parentheses(n: int) -> List[str]:
    """
    INTERVIEW SCRIPT:
    "Backtracking: add '(' if open count < n.
     Add ')' if close count < open count.
     Result: Catalan(n) = C(2n,n)/(n+1) valid combinations.
     O(4^n / √n) — nth Catalan number."
    """
    result = []
    def backtrack(path, opens, closes):
        if len(path) == 2*n: result.append(path); return
        if opens < n: backtrack(path+'(', opens+1, closes)
        if closes < opens: backtrack(path+')', opens, closes+1)
    backtrack('', 0, 0)
    return result

# ================================================================
# 294. EXPRESSION ADD OPERATORS (Hard)
# ================================================================
def add_operators(num: str, target: int) -> List[str]:
    """
    INTERVIEW SCRIPT:
    "DFS: at each position, try all splits as operand, try +, -, *.
     Track current value and last multiplied value (for * undo).
     Multiply: cur - last + last*next (undo last add, apply multiply).
     O(4^n * n) — 3 operators + concatenation, n digits."
    """
    result = []

    def backtrack(idx, path, value, last):
        if idx == len(num):
            if value == target: result.append(path)
            return
        for end in range(idx+1, len(num)+1):
            s = num[idx:end]
            if len(s) > 1 and s[0] == '0': break  # no leading zeros
            n = int(s)
            if idx == 0:
                backtrack(end, s, n, n)
            else:
                backtrack(end, path+'+'+s, value+n, n)
                backtrack(end, path+'-'+s, value-n, -n)
                backtrack(end, path+'*'+s, value-last+last*n, last*n)

    backtrack(0, '', 0, 0)
    return result

# ================================================================
# 295. DIFFERENT WAYS TO ADD PARENTHESES (Medium)
# ================================================================
def diff_ways_to_compute(expression: str) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Divide and conquer: for each operator, split expression.
     Recursively compute left and right parts.
     Combine: every left result with every right result using operator.
     Memoize for repeated subexpressions. O(n * Catalan(n))."
    """
    memo = {}

    def compute(expr):
        if expr in memo: return memo[expr]
        if expr.isdigit() or (expr[0] == '-' and expr[1:].isdigit()):
            return [int(expr)]
        result = []
        for i, c in enumerate(expr):
            if c in '+-*':
                left = compute(expr[:i])
                right = compute(expr[i+1:])
                for l in left:
                    for r in right:
                        if c == '+': result.append(l+r)
                        elif c == '-': result.append(l-r)
                        else: result.append(l*r)
        memo[expr] = result
        return result

    return compute(expression)

# ================================================================
# 296. GRAY CODE (Medium)
# ================================================================
def gray_code(n: int) -> List[int]:
    """
    APPROACH 1: Formula — O(2^n)
    APPROACH 2: Backtracking/reflection — O(2^n)

    INTERVIEW SCRIPT:
    "Gray code: i ^ (i >> 1) gives the ith Gray code.
     Reflection method: start with [0,1]. For each bit, mirror and add bit.
     Formula: O(2^n) time, O(1) extra space."
    """
    return [i ^ (i >> 1) for i in range(1 << n)]

# ================================================================
# 297. COMBINATION SUM III (Medium)
# ================================================================
def combination_sum_iii(k: int, n: int) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Use digits 1-9 exactly once. Find k digits summing to n.
     Backtracking: start from 'start', try each digit.
     Prune: if sum exceeds n or not enough digits left."
    """
    result = []
    def backtrack(start, path, remaining):
        if len(path) == k and remaining == 0:
            result.append(path[:]); return
        if len(path) == k or remaining <= 0: return
        for num in range(start, 10):
            if num > remaining: break
            path.append(num)
            backtrack(num+1, path, remaining-num)
            path.pop()
    backtrack(1, [], n)
    return result

# ================================================================
# 298. FACTOR COMBINATIONS (Medium)
# ================================================================
def get_factors(n: int) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Backtracking: try all factors from 2 to sqrt(n).
     For factor f of n: recurse on n//f.
     Each result list: sorted factors ending at n (if n>1).
     O(n log n) — bounded by number of factorizations."
    """
    result = []
    def backtrack(n, start, path):
        if path:
            result.append(path + [n])
        for f in range(start, int(n**0.5)+1):
            if n % f == 0:
                backtrack(n//f, f, path+[f])
    backtrack(n, 2, [])
    return result

# ================================================================
# 299. MATCHSTICKS TO SQUARE (Medium)
# ================================================================
def matchsticks_to_square(matchsticks: List[int]) -> bool:
    """
    INTERVIEW SCRIPT:
    "Partition 4 equal-sum subsets (target = total/4).
     Sort descending (prune large first).
     Backtracking: try placing each stick into one of 4 sides.
     Skip identical sides to avoid duplicate work.
     O(4^n) — very prunable in practice."
    """
    total = sum(matchsticks)
    if total % 4: return False
    target = total // 4
    matchsticks.sort(reverse=True)
    if matchsticks[0] > target: return False
    sides = [0] * 4

    def backtrack(idx):
        if idx == len(matchsticks): return all(s == target for s in sides)
        seen = set()
        for i in range(4):
            if sides[i] in seen: continue
            if sides[i] + matchsticks[idx] <= target:
                seen.add(sides[i])
                sides[i] += matchsticks[idx]
                if backtrack(idx+1): return True
                sides[i] -= matchsticks[idx]
        return False

    return backtrack(0)

# ================================================================
# 300. STROBOGRAMMATIC NUMBER II (Medium)
# ================================================================
def find_strobogrammatic(n: int) -> List[str]:
    """
    INTERVIEW SCRIPT:
    "Strobogrammatic: looks same when rotated 180°. Valid: 0,1,6,8,9.
     Build inside-out. Base: n=0→[''], n=1→['0','1','8'].
     Wrap each with valid pairs: 1x1, 6x9, 8x8, 9x6.
     For outer wrap: don't use '0' (leading zero).
     O(5^(n/2)) — 5 pairs to choose from."
    """
    def helper(n, total):
        if n == 0: return ['']
        if n == 1: return ['0', '1', '8']
        middles = helper(n-2, total)
        result = []
        for middle in middles:
            for pair in [('1','1'),('6','9'),('8','8'),('9','6')]:
                result.append(pair[0] + middle + pair[1])
            if n != total:  # not outermost → allow leading zero
                result.append('0' + middle + '0')
        return result

    return helper(n, n)

# ================================================================
# BONUS: WORD SEARCH II (Trie + Backtracking)
# ================================================================
def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    """
    INTERVIEW SCRIPT:
    "Build Trie from all words. DFS on board, traverse Trie simultaneously.
     When word found in Trie: add to result and mark to avoid duplicates.
     O(M * 4 * 3^(L-1)) where M=cells, L=max word length.
     Much better than checking each word individually."
    """
    # Build Trie
    trie = {}
    for word in words:
        node = trie
        for c in word:
            node = node.setdefault(c, {})
        node['#'] = word  # end marker stores the word

    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r, c, node):
        char = board[r][c]
        if char not in node: return
        next_node = node[char]
        if '#' in next_node:
            result.append(next_node['#'])
            del next_node['#']  # prevent duplicates
        board[r][c] = '#'  # mark visited
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        board[r][c] = char  # restore

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie)

    return result

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Subsets [1,2,3]:", subsets([1,2,3]))
    print("Subsets II [1,2,2]:", subsets_with_dup([1,2,2]))
    print("Permutations [1,2,3]:", permute([1,2,3]))
    print("Permutations II [1,1,2]:", permute_unique([1,1,2]))
    print("Combination Sum [2,3,6,7] t=7:", combination_sum([2,3,6,7], 7))
    print("Combination Sum II [10,1,2,7,6,1,5] t=8:", combination_sum_ii([10,1,2,7,6,1,5], 8))
    print("Word Search ABCCED:", word_search(
        [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"))
    print("N-Queens 4:", len(solve_n_queens(4)), "solutions")
    print("Total N-Queens 4:", total_n_queens(4))
    print("Restore IP '25525511135':", restore_ip_addresses("25525511135"))
    print("Palindrome Partition 'aab':", partition_palindrome("aab"))
    print("Letter Combinations '23':", letter_combinations("23"))
    print("Generate Parentheses 3:", generate_parentheses(3))
    print("Add Operators '123' t=6:", add_operators("123", 6))
    print("Diff Ways '2-1-1':", diff_ways_to_compute("2-1-1"))
    print("Gray Code 2:", gray_code(2))
    print("Combination Sum III k=3 n=7:", combination_sum_iii(3, 7))
    print("Matchsticks [1,1,2,2,2]:", matchsticks_to_square([1,1,2,2,2]))
    print("Strobogrammatic n=2:", find_strobogrammatic(2))
    board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    print("Word Search II:", find_words(board, ["oath","pea","eat","rain"]))
