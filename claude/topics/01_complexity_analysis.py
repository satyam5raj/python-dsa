"""
================================================================
TOPIC 1: COMPLEXITY ANALYSIS
================================================================
WHY IT MATTERS: Before writing any solution in an interview,
you MUST know how to analyze and communicate its complexity.
This is the language of DSA interviews.
================================================================

INTERVIEW COMMUNICATION TEMPLATE:
"Let me analyze the time and space complexity of this solution.
 The time complexity is O(...) because ...
 The space complexity is O(...) because ..."

================================================================
"""

# ----------------------------------------------------------------
# BIG-O NOTATION GUIDE
# ----------------------------------------------------------------
# O(1)       - Constant     - Array index access
# O(log n)   - Logarithmic  - Binary search
# O(n)       - Linear       - Single loop
# O(n log n) - Linearithmic - Merge sort, heap sort
# O(n²)      - Quadratic    - Nested loops
# O(2ⁿ)      - Exponential  - Recursive subsets
# O(n!)      - Factorial    - Permutations

# Ranking (best → worst):
# O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)

# ----------------------------------------------------------------
# 1. O(1) - CONSTANT TIME
# ----------------------------------------------------------------
def get_first_element(arr):
    return arr[0]  # Always 1 operation regardless of arr size

def is_even(n):
    return n % 2 == 0

# USE CASE: Hash map lookup, array indexing, stack push/pop

# ----------------------------------------------------------------
# 2. O(log n) - LOGARITHMIC TIME
# ----------------------------------------------------------------
def binary_search_complexity_demo(arr, target):
    """Each step HALVES the search space: n → n/2 → n/4 → ... → 1
    Number of steps = log₂(n)
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# USE CASE: Binary search, balanced BST operations, heap insert/delete

# ----------------------------------------------------------------
# 3. O(n) - LINEAR TIME
# ----------------------------------------------------------------
def find_max(arr):
    """Visit every element exactly once → O(n)"""
    max_val = arr[0]
    for x in arr:           # n iterations
        if x > max_val:
            max_val = x
    return max_val

# USE CASE: Linear search, single pass algorithms, traversals

# ----------------------------------------------------------------
# 4. O(n log n) - LINEARITHMIC TIME
# ----------------------------------------------------------------
def merge_sort_complexity_demo(arr):
    """
    Divide: O(log n) levels of recursion
    Conquer: O(n) work at each level
    Total: O(n log n)
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_complexity_demo(arr[:mid])
    right = merge_sort_complexity_demo(arr[mid:])
    return merge(left, right)

def merge(left, right):
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

# USE CASE: Efficient sorting, many divide-and-conquer algorithms

# ----------------------------------------------------------------
# 5. O(n²) - QUADRATIC TIME
# ----------------------------------------------------------------
def bubble_sort_complexity_demo(arr):
    """
    Outer loop: n iterations
    Inner loop: n iterations
    Total: n × n = O(n²)
    """
    n = len(arr)
    for i in range(n):          # O(n)
        for j in range(n - i - 1):  # O(n)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def two_sum_brute(nums, target):
    """Classic O(n²) brute force"""
    for i in range(len(nums)):         # O(n)
        for j in range(i + 1, len(nums)):  # O(n)
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# ----------------------------------------------------------------
# 6. O(2ⁿ) - EXPONENTIAL TIME
# ----------------------------------------------------------------
def fibonacci_exponential(n):
    """
    Each call branches into 2 more calls.
    Total calls ≈ 2⁰ + 2¹ + 2² + ... + 2ⁿ = O(2ⁿ)
    """
    if n <= 1:
        return n
    return fibonacci_exponential(n - 1) + fibonacci_exponential(n - 2)

# USE CASE: Naive recursion without memoization - AVOID in interviews

# ----------------------------------------------------------------
# 7. O(n!) - FACTORIAL TIME
# ----------------------------------------------------------------
def generate_permutations(arr):
    """n! permutations exist for n elements → O(n!)"""
    if len(arr) <= 1:
        return [arr[:]]
    result = []
    for i in range(len(arr)):
        arr[0], arr[i] = arr[i], arr[0]
        for perm in generate_permutations(arr[1:]):
            result.append([arr[0]] + perm)
        arr[0], arr[i] = arr[i], arr[0]
    return result

# ----------------------------------------------------------------
# SPACE COMPLEXITY ANALYSIS
# ----------------------------------------------------------------

def space_o1_example(n):
    """O(1) space - only fixed variables regardless of input"""
    total = 0      # 1 variable
    for i in range(n):
        total += i
    return total

def space_on_example(n):
    """O(n) space - array grows with input"""
    result = []    # grows up to size n
    for i in range(n):
        result.append(i)
    return result

def space_recursion_example(n):
    """O(n) space - call stack grows to depth n"""
    if n == 0:
        return 0
    return n + space_recursion_example(n - 1)  # n frames on call stack

# ----------------------------------------------------------------
# AMORTIZED ANALYSIS
# ----------------------------------------------------------------
class DynamicArray:
    """
    Python list is a dynamic array.
    Single append: O(n) worst case (when resize needed)
    But AMORTIZED over n appends: O(1) per append

    Why? Array doubles when full:
    - Resize at sizes: 1, 2, 4, 8, 16, ...
    - Total copies: 1 + 2 + 4 + ... + n = 2n = O(n)
    - Per element: O(n) / n = O(1) amortized
    """
    def __init__(self):
        self.data = []
        self.size = 0
        self.capacity = 1

    def append(self, val):
        if self.size == self.capacity:
            self._resize()
        self.data.append(val)
        self.size += 1

    def _resize(self):
        self.capacity *= 2  # double capacity
        # In real implementation, copy old data to new array

# ----------------------------------------------------------------
# ITERATIVE vs RECURSIVE COMPLEXITY
# ----------------------------------------------------------------

# Iterative fibonacci: O(n) time, O(1) space
def fib_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Recursive fibonacci (naive): O(2ⁿ) time, O(n) space
def fib_recursive_naive(n):
    if n <= 1:
        return n
    return fib_recursive_naive(n-1) + fib_recursive_naive(n-2)

# Recursive fibonacci (memoized): O(n) time, O(n) space
def fib_memoized(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memoized(n-1, memo) + fib_memoized(n-2, memo)
    return memo[n]

# ----------------------------------------------------------------
# CHEAT SHEET FOR INTERVIEWS
# ----------------------------------------------------------------
"""
QUICK REFERENCE - Memorize these:

Data Structure Operations:
┌──────────────┬──────────┬──────────┬──────────┬──────────┐
│              │ Access   │ Search   │ Insert   │ Delete   │
├──────────────┼──────────┼──────────┼──────────┼──────────┤
│ Array        │ O(1)     │ O(n)     │ O(n)     │ O(n)     │
│ Linked List  │ O(n)     │ O(n)     │ O(1)     │ O(1)     │
│ Hash Table   │ N/A      │ O(1)avg  │ O(1)avg  │ O(1)avg  │
│ BST          │ O(log n) │ O(log n) │ O(log n) │ O(log n) │
│ Heap         │ O(1)top  │ O(n)     │ O(log n) │ O(log n) │
│ Stack/Queue  │ O(n)     │ O(n)     │ O(1)     │ O(1)     │
└──────────────┴──────────┴──────────┴──────────┴──────────┘

Sorting Algorithms:
┌──────────────┬──────────────┬──────────────┬──────────┐
│              │ Best         │ Average      │ Space    │
├──────────────┼──────────────┼──────────────┼──────────┤
│ Bubble Sort  │ O(n)         │ O(n²)        │ O(1)     │
│ Merge Sort   │ O(n log n)   │ O(n log n)   │ O(n)     │
│ Quick Sort   │ O(n log n)   │ O(n log n)   │ O(log n) │
│ Heap Sort    │ O(n log n)   │ O(n log n)   │ O(1)     │
│ Tim Sort     │ O(n)         │ O(n log n)   │ O(n)     │
└──────────────┴──────────────┴──────────────┴──────────┘

HOW TO TALK ABOUT COMPLEXITY IN INTERVIEWS:
1. Start with brute force: "The naive approach would be O(n²)..."
2. Identify bottleneck: "The bottleneck is this nested loop..."
3. Propose optimization: "We can reduce this to O(n) by using a hash map..."
4. Confirm trade-offs: "This trades O(n) extra space for O(n) time savings."
"""

if __name__ == "__main__":
    # Demo
    arr = [1, 3, 5, 7, 9, 11, 13]
    print("Binary search for 7:", binary_search_complexity_demo(arr, 7))
    print("Merge sort [3,1,4,1,5,9]:", merge_sort_complexity_demo([3,1,4,1,5,9]))
    print("Fib(10) iterative:", fib_iterative(10))
    print("Fib(10) memoized:", fib_memoized(10))
