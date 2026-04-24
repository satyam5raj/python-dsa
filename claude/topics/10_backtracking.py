"""
================================================================
TOPIC 10: BACKTRACKING
================================================================
Explore ALL possibilities by building solutions incrementally.
Abandon ("backtrack") paths that violate constraints.

INTERVIEW COMMUNICATION:
"This is a backtracking problem — explore all possibilities.
 I'll build the solution incrementally:
 1. Choose: pick an option
 2. Explore: recurse deeper
 3. Unchoose: undo the choice (backtrack)
 Time complexity: O(branches^depth) — exponential but pruned."
================================================================
"""

from typing import List

# ================================================================
# BACKTRACKING TEMPLATE
# ================================================================
"""
def backtrack(path, choices, result):
    if is_solution(path):
        result.append(path.copy())
        return
    for choice in choices:
        if is_valid(choice, path):
            path.append(choice)          # CHOOSE
            backtrack(path, new_choices, result)  # EXPLORE
            path.pop()                   # UNCHOOSE (backtrack)
"""

# ================================================================
# SUBSETS (Power Set)
# ================================================================

def subsets_brute(nums: List[int]) -> List[List[int]]:
    """
    Generate all 2ⁿ subsets iteratively
    O(n * 2ⁿ) time
    """
    result = [[]]
    for num in nums:
        result += [subset + [num] for subset in result]
    return result

def subsets_backtrack(nums: List[int]) -> List[List[int]]:
    """
    APPROACH 2: Backtracking — O(n * 2ⁿ)

    INTERVIEW SCRIPT:
    "At each position, I have 2 choices: include or exclude.
     Use backtracking to explore both choices.
     Total: 2ⁿ subsets, each takes O(n) to copy."
    """
    result = []

    def backtrack(start, path):
        result.append(list(path))  # every path is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])          # choose
            backtrack(i + 1, path)        # explore
            path.pop()                    # unchoose

    backtrack(0, [])
    return result

def subsets_with_duplicates(nums: List[int]) -> List[List[int]]:
    """
    Subsets II — handle duplicates by sorting + skipping
    """
    nums.sort()
    result = []

    def backtrack(start, path):
        result.append(list(path))
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:  # skip duplicate
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result

# ================================================================
# PERMUTATIONS
# ================================================================

def permutations_backtrack(nums: List[int]) -> List[List[int]]:
    """
    All permutations — O(n! * n)

    INTERVIEW SCRIPT:
    "n! permutations exist. For each position, try every unused number.
     Track used numbers with a set or by swapping.
     Time: O(n * n!) — n! permutations, each O(n) to copy."
    """
    result = []

    def backtrack(path, remaining):
        if not remaining:
            result.append(list(path))
            return
        for i, num in enumerate(remaining):
            path.append(num)
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()

    backtrack([], nums)
    return result

def permutations_swap(nums: List[int]) -> List[List[int]]:
    """Permutations using in-place swap — O(n!) space, O(n!) time"""
    result = []

    def backtrack(start):
        if start == len(nums):
            result.append(list(nums))
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]  # choose
            backtrack(start + 1)                           # explore
            nums[start], nums[i] = nums[i], nums[start]  # unchoose

    backtrack(0)
    return result

def permutations_with_duplicates(nums: List[int]) -> List[List[int]]:
    """Unique permutations with duplicates"""
    nums.sort()
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(list(path))
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue  # skip duplicate
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result

# ================================================================
# COMBINATION SUM
# ================================================================

def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all combinations summing to target (can reuse elements).
    O(n^(t/m)) where t=target, m=min candidate

    INTERVIEW SCRIPT:
    "Classic backtracking. At each step, try each candidate.
     Allow reuse: pass same index (not i+1).
     Prune: if remaining < 0, backtrack early.
     Sort candidates for better pruning."
    """
    result = []
    candidates.sort()

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(list(path))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # pruning — sorted, all further too large
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # reuse allowed
            path.pop()

    backtrack(0, [], target)
    return result

def combination_sum_no_reuse(candidates: List[int], target: int) -> List[List[int]]:
    """Combination Sum II — no reuse, handle duplicates"""
    candidates.sort()
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(list(path))
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i-1]:
                continue  # skip duplicate
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])  # no reuse
            path.pop()

    backtrack(0, [], target)
    return result

# ================================================================
# WORD SEARCH
# ================================================================

def word_search(board: List[List[str]], word: str) -> bool:
    """
    Find if word exists in grid (can't reuse cell).
    O(m * n * 4^len(word)) — worst case

    INTERVIEW SCRIPT:
    "DFS/backtracking on the grid.
     Start from every cell matching word[0].
     At each step, try 4 directions.
     Mark cell as visited (or modify board), backtrack by restoring.
     Pruning: early return if character doesn't match."
    """
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False

        temp = board[r][c]
        board[r][c] = '#'  # mark visited

        found = (dfs(r+1, c, idx+1) or dfs(r-1, c, idx+1) or
                 dfs(r, c+1, idx+1) or dfs(r, c-1, idx+1))

        board[r][c] = temp  # restore (backtrack)
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False

# ================================================================
# N-QUEENS
# ================================================================

def n_queens(n: int) -> List[List[str]]:
    """
    Place n queens on n×n board so no two attack each other.
    O(n!) — prune aggressively

    INTERVIEW SCRIPT:
    "One queen per row. For each row, try all columns.
     Check: no two queens in same column or diagonal.
     Diagonals: row-col is constant for one diagonal,
                row+col is constant for the other.
     Use sets for O(1) conflict checking.
     Backtrack when constraint violated."
    """
    result = []
    cols = set()
    diag1 = set()  # r - c constant
    diag2 = set()  # r + c constant

    board = [['.'] * n for _ in range(n)]

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue
            # Place queen
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = 'Q'
            # Explore
            backtrack(row + 1)
            # Remove queen (backtrack)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row][col] = '.'

    backtrack(0)
    return result

# ================================================================
# SUDOKU SOLVER
# ================================================================

def solve_sudoku(board: List[List[str]]) -> None:
    """
    Solve sudoku in-place using backtracking.
    O(9^m) where m = empty cells

    INTERVIEW SCRIPT:
    "For each empty cell, try digits 1-9.
     Check if placement is valid (row, col, 3x3 box).
     If valid, place and recurse.
     If recursion fails, remove and try next digit.
     If no digit works, return False to trigger backtrack."
    """
    def is_valid(board, r, c, num):
        for i in range(9):
            if board[r][i] == num:
                return False
            if board[i][c] == num:
                return False
            box_r = 3 * (r // 3) + i // 3
            box_c = 3 * (c // 3) + i % 3
            if board[box_r][box_c] == num:
                return False
        return True

    def solve(board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for num in '123456789':
                        if is_valid(board, r, c, num):
                            board[r][c] = num      # choose
                            if solve(board):
                                return True
                            board[r][c] = '.'      # unchoose
                    return False  # no valid number
        return True  # board complete

    solve(board)

# ================================================================
# PALINDROME PARTITIONING
# ================================================================

def palindrome_partition(s: str) -> List[List[str]]:
    """
    Partition string so every substring is palindrome.
    O(n * 2ⁿ) — up to 2ⁿ partitions, each checked in O(n)

    INTERVIEW SCRIPT:
    "Try every prefix. If it's a palindrome, recurse on suffix.
     Backtrack if no valid partition found.
     Optimization: precompute palindrome check with DP."
    """
    result = []

    def is_palindrome(sub):
        return sub == sub[::-1]

    def backtrack(start, path):
        if start == len(s):
            result.append(list(path))
            return
        for end in range(start + 1, len(s) + 1):
            prefix = s[start:end]
            if is_palindrome(prefix):
                path.append(prefix)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    return result

# ================================================================
# GENERATE PARENTHESES
# ================================================================

def generate_parentheses(n: int) -> List[str]:
    """
    Generate all valid combinations of n pairs of parentheses.
    O(4ⁿ/√n) — Catalan number

    INTERVIEW SCRIPT:
    "At each step: add '(' if open < n, add ')' if close < open.
     This ensures validity without checking the whole string.
     Prune: if close >= open, can't add ')'.
     Base: when both reach n, add to result."
    """
    result = []

    def backtrack(s, open_count, close_count):
        if len(s) == 2 * n:
            result.append(s)
            return
        if open_count < n:
            backtrack(s + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(s + ')', open_count, close_count + 1)

    backtrack('', 0, 0)
    return result

# ================================================================
# RAT IN A MAZE
# ================================================================

def rat_in_maze(maze: List[List[int]]) -> List[List[List[int]]]:
    """
    Find all paths from top-left to bottom-right.
    Cells with 1 are open, 0 are blocked.
    """
    n = len(maze)
    result = []
    path = [[0] * n for _ in range(n)]

    def solve(r, c):
        if r == n-1 and c == n-1:
            result.append([row[:] for row in path])
            return
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and maze[nr][nc] == 1 and path[nr][nc] == 0:
                path[nr][nc] = 1
                solve(nr, nc)
                path[nr][nc] = 0  # backtrack

    if maze[0][0] == 1:
        path[0][0] = 1
        solve(0, 0)
    return result

# ================================================================
# LETTER COMBINATIONS PHONE NUMBER
# ================================================================

def letter_combinations(digits: str) -> List[str]:
    """
    Phone keypad letter combinations — O(4ⁿ * n)

    INTERVIEW SCRIPT:
    "Map each digit to its letters.
     At each position, try all letters for current digit.
     Backtrack to explore all combinations."
    """
    if not digits:
        return []

    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    result = []

    def backtrack(idx, path):
        if idx == len(digits):
            result.append(''.join(path))
            return
        for char in phone[digits[idx]]:
            path.append(char)
            backtrack(idx + 1, path)
            path.pop()

    backtrack(0, [])
    return result

if __name__ == "__main__":
    print("Subsets [1,2,3]:", subsets_backtrack([1, 2, 3]))
    print("Permutations [1,2,3]:", permutations_backtrack([1, 2, 3]))
    print("Combination sum [2,3,6,7] target=7:", combination_sum([2, 3, 6, 7], 7))
    print("N-Queens (4):", len(n_queens(4)), "solutions")
    print("Generate parentheses (3):", generate_parentheses(3))
    print("Letter combinations '23':", letter_combinations("23"))
    print("Palindrome partitions 'aab':", palindrome_partition("aab"))
