"""
================================================================
MATH PROBLEMS 71-80: RECURSION + BACKTRACKING
================================================================
"""

from typing import List

# ================================================================
# PROBLEM 71: Print all subsets
# ================================================================
def print_all_subsets(arr: List, index: int = 0, current: List = None):
    """
    Print all 2^n subsets of arr.

    INTERVIEW SCRIPT:
    "At each index, two choices: include or exclude current element.
     Base: index == len(arr) → print current subset.
     This generates all 2^n subsets."
    """
    if current is None: current = []
    if index == len(arr):
        print(current)
        return
    # Include arr[index]
    current.append(arr[index])
    print_all_subsets(arr, index + 1, current)
    current.pop()  # backtrack
    # Exclude arr[index]
    print_all_subsets(arr, index + 1, current)

def get_all_subsets(arr: List) -> List[List]:
    """Returns all subsets as a list"""
    result = []
    def backtrack(index, current):
        if index == len(arr):
            result.append(list(current))
            return
        current.append(arr[index])
        backtrack(index + 1, current)
        current.pop()
        backtrack(index + 1, current)
    backtrack(0, [])
    return result

# ================================================================
# PROBLEM 72: Subset sum
# ================================================================
def has_subset_sum(arr: List[int], target: int) -> bool:
    """
    Does any subset sum equal target?
    O(2^n) recursive, O(n*target) DP

    APPROACH 1 (Brute/Recursive):
    APPROACH 2 (DP — preferred):

    INTERVIEW SCRIPT:
    "For each element: either include or exclude.
     If include: check if remaining arr sums to target-element.
     If exclude: check if remaining arr sums to target.
     DP approach: dp[i][j] = can first i elements sum to j."
    """
    # Recursive O(2^n)
    def recursive(index, remaining):
        if remaining == 0: return True
        if index == len(arr) or remaining < 0: return False
        return (recursive(index+1, remaining - arr[index]) or
                recursive(index+1, remaining))

    # DP O(n * target)
    def dp_approach():
        n = len(arr)
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = True  # empty subset sums to 0
        for i in range(1, n + 1):
            for j in range(target + 1):
                dp[i][j] = dp[i-1][j]  # exclude
                if j >= arr[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j - arr[i-1]]  # include
        return dp[n][target]

    return dp_approach()

# ================================================================
# PROBLEM 73: Generate permutations
# ================================================================
def generate_permutations(arr: List) -> List[List]:
    """
    All n! permutations.
    O(n * n!) time

    INTERVIEW SCRIPT:
    "For each position, try each unused element.
     Use swap approach for in-place: swap current with each subsequent.
     Backtrack by swapping back."
    """
    result = []

    def backtrack(start):
        if start == len(arr):
            result.append(list(arr))
            return
        for i in range(start, len(arr)):
            arr[start], arr[i] = arr[i], arr[start]  # choose
            backtrack(start + 1)                       # explore
            arr[start], arr[i] = arr[i], arr[start]  # unchoose

    backtrack(0)
    return result

# ================================================================
# PROBLEM 74: Combination sum
# ================================================================
def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Find all combinations summing to target. Can reuse candidates.
    O(n^(target/min_candidate))

    INTERVIEW SCRIPT:
    "Backtracking with pruning: sort candidates, stop when current > target.
     Allow reuse: pass same index (not i+1) to recursive call."
    """
    candidates.sort()
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(list(path))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # sorted, so all further too large
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i not i+1 (reuse)
            path.pop()

    backtrack(0, [], target)
    return result

# ================================================================
# PROBLEM 75: N-Queens
# ================================================================
def n_queens(n: int) -> int:
    """
    Place n queens on n×n board — no two attack each other.
    Return count of valid solutions.

    INTERVIEW SCRIPT:
    "One queen per row. For each row, try each column.
     Maintain sets for used columns and diagonals.
     Diagonals: row-col (constant on ↗ diagonal),
                row+col (constant on ↘ diagonal)."
    """
    count = [0]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row):
        if row == n:
            count[0] += 1
            return
        for col in range(n):
            if col in cols or row-col in diag1 or row+col in diag2:
                continue
            cols.add(col); diag1.add(row-col); diag2.add(row+col)
            backtrack(row + 1)
            cols.remove(col); diag1.remove(row-col); diag2.remove(row+col)

    backtrack(0)
    return count[0]

# ================================================================
# PROBLEM 76: Rat in a maze
# ================================================================
def rat_in_maze(maze: List[List[int]]) -> List[str]:
    """
    Find all paths from top-left to bottom-right.
    Cells with 1 are open (can enter), 0 are blocked.

    INTERVIEW SCRIPT:
    "DFS/Backtracking on 4 directions (Down, Left, Right, Up).
     Mark cell as visited before recursing, unmark after (backtrack).
     Collect path string at each step."
    """
    n = len(maze)
    if not maze[0][0] or not maze[n-1][n-1]: return []

    paths = []
    visited = [[False]*n for _ in range(n)]

    directions = [('D', 1, 0), ('L', 0, -1), ('R', 0, 1), ('U', -1, 0)]

    def dfs(r, c, path):
        if r == n-1 and c == n-1:
            paths.append(path)
            return
        for direction, dr, dc in directions:
            nr, nc = r+dr, c+dc
            if (0 <= nr < n and 0 <= nc < n and
                maze[nr][nc] == 1 and not visited[nr][nc]):
                visited[nr][nc] = True
                dfs(nr, nc, path + direction)
                visited[nr][nc] = False  # backtrack

    visited[0][0] = True
    dfs(0, 0, "")
    return paths

# ================================================================
# PROBLEM 77: Sudoku solver
# ================================================================
def solve_sudoku(board: List[List[str]]) -> bool:
    """
    Solve 9x9 Sudoku in-place.
    O(9^m) where m = empty cells

    INTERVIEW SCRIPT:
    "For each empty cell, try digits 1-9.
     For each digit: check row, column, 3×3 box validity.
     If valid: place and recurse.
     If recursion fails: remove digit and try next (backtrack).
     If no digit works: return False."
    """
    def is_valid(r, c, ch):
        for i in range(9):
            if board[r][i] == ch: return False
            if board[i][c] == ch: return False
            box_r = 3*(r//3) + i//3
            box_c = 3*(c//3) + i%3
            if board[box_r][box_c] == ch: return False
        return True

    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                for ch in '123456789':
                    if is_valid(r, c, ch):
                        board[r][c] = ch
                        if solve_sudoku(board): return True
                        board[r][c] = '.'
                return False  # no valid digit
    return True  # complete

# ================================================================
# PROBLEM 78: Palindrome partitioning
# ================================================================
def palindrome_partitioning(s: str) -> List[List[str]]:
    """
    Partition s such that every substring is a palindrome.
    O(n * 2^n)

    INTERVIEW SCRIPT:
    "Try every prefix. If palindrome: recurse on suffix.
     Backtrack if no valid partition.
     Optimization: precompute isPalindrome[i][j] with DP."
    """
    result = []

    # Precompute palindrome check with DP
    n = len(s)
    is_pal = [[False]*n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for i in range(n-1):
        is_pal[i][i+1] = s[i] == s[i+1]
    for length in range(3, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = s[i] == s[j] and is_pal[i+1][j-1]

    def backtrack(start, path):
        if start == n:
            result.append(list(path))
            return
        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start:end+1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return result

# ================================================================
# PROBLEM 79: Word search
# ================================================================
def word_search(board: List[List[str]], word: str) -> bool:
    """
    Find word in grid (no cell reuse).
    O(m * n * 4^L) where L = word length

    INTERVIEW SCRIPT:
    "Try starting from every cell.
     DFS/backtracking: at each step, try 4 directions.
     Mark cell visited (modify board), backtrack by restoring.
     Pruning: return early if character doesn't match."
    """
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word): return True
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != word[idx]): return False

        temp = board[r][c]
        board[r][c] = '#'  # mark visited
        found = (dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or
                 dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1))
        board[r][c] = temp  # restore
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0): return True
    return False

# ================================================================
# PROBLEM 80: Generate parentheses
# ================================================================
def generate_parentheses(n: int) -> List[str]:
    """
    All valid combinations of n pairs of parentheses.
    O(4^n / sqrt(n)) — Catalan number

    INTERVIEW SCRIPT:
    "Build string character by character.
     Add '(' if open_count < n.
     Add ')' if close_count < open_count.
     Base: string length == 2n → add to result.
     This naturally ensures validity."
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
# TEST ALL
# ================================================================
if __name__ == "__main__":
    print("=== RECURSION + BACKTRACKING ===")
    print("71. All subsets [1,2,3]:"); print_all_subsets([1, 2, 3])
    print("72. Has subset sum [3,1,5] target=4:", has_subset_sum([3,1,5], 4))
    print("73. Permutations [1,2,3]:", generate_permutations([1,2,3]))
    print("74. Combination sum [2,3,6,7] target=7:", combination_sum([2,3,6,7], 7))
    print("75. N-Queens(4):", n_queens(4), "solutions")
    maze = [[1,0,0,0],[1,1,0,1],[1,1,0,0],[0,1,1,1]]
    print("76. Rat in maze:", rat_in_maze(maze))
    print("78. Palindrome partitions 'aab':", palindrome_partitioning("aab"))
    board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    print("79. Word search 'ABCCED':", word_search([row[:] for row in board], "ABCCED"))
    print("80. Generate parentheses(3):", generate_parentheses(3))
