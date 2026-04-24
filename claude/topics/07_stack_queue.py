"""
================================================================
TOPIC 7: STACK & QUEUE
================================================================
STACK: LIFO — Last In, First Out
QUEUE: FIFO — First In, First Out
DEQUE: Double-ended queue — O(1) both ends

Key Algorithms:
- Monotonic Stack: Next Greater/Smaller Element
- Sliding Window Max/Min with Deque

INTERVIEW COMMUNICATION:
"Stacks are perfect when I need to track 'pending' operations
 or the most recent item. Queues for BFS, level-order processing.
 Monotonic stack: when I need next greater/smaller element in O(n)."
================================================================
"""

from collections import deque
from typing import List, Optional

# ================================================================
# STACK IMPLEMENTATION
# ================================================================

class Stack:
    """
    USE CASE: Function call stack, undo/redo, browser history,
              expression evaluation, DFS
    """
    def __init__(self):
        self._data = []

    def push(self, val):   # O(1)
        self._data.append(val)

    def pop(self):         # O(1)
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self):        # O(1)
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]

    def is_empty(self):    # O(1)
        return len(self._data) == 0

    def size(self):
        return len(self._data)

class MinStack:
    """
    Stack that supports getMin() in O(1)

    INTERVIEW SCRIPT:
    "Maintain two stacks: main stack and min_stack.
     min_stack[i] = minimum value in stack up to position i.
     Push to min_stack only when new min found (or always push current min).
     Pop from min_stack when popping from main stack."
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
        else:
            self.min_stack.append(self.min_stack[-1])

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

# ================================================================
# QUEUE IMPLEMENTATION
# ================================================================

class Queue:
    """
    USE CASE: BFS, task scheduling, print queues, breadth-first processing
    Python deque has O(1) append and popleft
    """
    def __init__(self):
        self._data = deque()

    def enqueue(self, val):  # O(1)
        self._data.append(val)

    def dequeue(self):       # O(1)
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.popleft()

    def front(self):         # O(1)
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

class CircularQueue:
    """
    Fixed-size circular queue — O(1) all operations
    USE CASE: Ring buffers, streaming data, CPU scheduling
    """
    def __init__(self, k: int):
        self.size = k
        self.queue = [0] * k
        self.head = self.tail = -1
        self.count = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        if self.isEmpty():
            self.head = 0
        self.tail = (self.tail + 1) % self.size
        self.queue[self.tail] = value
        self.count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        if self.head == self.tail:
            self.head = self.tail = -1
        else:
            self.head = (self.head + 1) % self.size
        self.count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.head]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.queue[self.tail]

    def isEmpty(self) -> bool:
        return self.count == 0

    def isFull(self) -> bool:
        return self.count == self.size

# ================================================================
# STACK USING QUEUES / QUEUE USING STACKS
# ================================================================

class QueueUsingStacks:
    """
    Implement queue using two stacks.
    AMORTIZED O(1) for all ops.

    INTERVIEW SCRIPT:
    "Use two stacks: inbox and outbox.
     Push always goes to inbox.
     Pop/peek: if outbox empty, pour inbox into outbox (reverses order).
     Each element moves from inbox to outbox at most once → amortized O(1)."
    """
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def pop(self) -> int:
        self._transfer()
        return self.outbox.pop()

    def peek(self) -> int:
        self._transfer()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox

    def _transfer(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

# ================================================================
# PATTERN: PARENTHESES VALIDATION
# ================================================================

def is_valid_parentheses(s: str) -> bool:
    """
    Valid brackets: (), [], {}
    O(n) time, O(n) space

    INTERVIEW SCRIPT:
    "Use a stack. For each char:
     - Opening bracket: push to stack.
     - Closing bracket: pop from stack, check if matching.
     - Stack empty before closing: invalid.
     After processing: stack must be empty."

    USE CASE: Compiler syntax checking, JSON/XML validation
    """
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in mapping:  # closing bracket
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:  # opening bracket
            stack.append(char)
    return len(stack) == 0

def decode_string(s: str) -> str:
    """
    Decode encoded string: k[encoded_string]
    E.g., "3[a]2[bc]" → "aaabcbc"
    O(n) time

    INTERVIEW SCRIPT:
    "Use two stacks: one for counts, one for strings built so far.
     When we see a digit: build the number.
     When we see '[': push current string and count onto stacks.
     When we see ']': pop count and string, repeat current * count,
                      append to popped string."
    """
    count_stack = []
    str_stack = []
    curr_str = ""
    curr_num = 0

    for char in s:
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        elif char == '[':
            count_stack.append(curr_num)
            str_stack.append(curr_str)
            curr_num = 0
            curr_str = ""
        elif char == ']':
            num = count_stack.pop()
            prev_str = str_stack.pop()
            curr_str = prev_str + curr_str * num
        else:
            curr_str += char
    return curr_str

# ================================================================
# MONOTONIC STACK — Key Interview Pattern
# ================================================================
"""
MONOTONIC STACK: stack that maintains elements in sorted order
- Monotonic Increasing: stack bottom > top
- Monotonic Decreasing: stack bottom < top

USE WHEN: Next Greater/Smaller Element, Largest Rectangle,
          Trapping Rain Water
"""

def next_greater_element(nums: List[int]) -> List[int]:
    """
    For each element, find next greater element.
    O(n) time — each element pushed/popped once

    INTERVIEW SCRIPT:
    "Use a monotonic decreasing stack.
     For each element, pop elements from stack that are smaller
     (current element is their 'next greater').
     Push current element.
     Remaining stack elements have no next greater → -1."
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    return result

def next_greater_circular(nums: List[int]) -> List[int]:
    """
    Next greater in CIRCULAR array (Next Greater Element II)
    O(n) — process array twice

    INTERVIEW SCRIPT:
    "Simulate circular array by iterating 2n times using modulo.
     Same monotonic stack approach."
    """
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(2 * n):
        while stack and nums[i % n] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i % n]
        if i < n:
            stack.append(i)
    return result

def daily_temperatures(temps: List[int]) -> List[int]:
    """
    How many days until warmer temperature?
    O(n) — monotonic stack on temperatures

    INTERVIEW SCRIPT:
    "For each day, we want the next day with higher temp.
     Monotonic decreasing stack of indices.
     When current temp > stack top temp: pop, answer = i - popped_index."
    """
    result = [0] * len(temps)
    stack = []  # indices

    for i, temp in enumerate(temps):
        while stack and temp > temps[stack[-1]]:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx
        stack.append(i)
    return result

def largest_rectangle_histogram(heights: List[int]) -> int:
    """
    Largest rectangle in histogram.
    O(n) — monotonic stack

    APPROACH 1 (Brute): O(n²) — try every bar as shortest
    APPROACH 2 (Monotonic Stack): O(n)

    INTERVIEW SCRIPT:
    "For each bar, find how far left and right it can extend
     while being the minimum height.
     Use monotonic increasing stack: when we pop a bar,
     the current bar is its right boundary,
     stack top is its left boundary.
     Area = height[popped] * (right - left - 1)."

    USE CASE: Building skyline analysis, histogram analysis
    """
    stack = [-1]
    max_area = 0

    for i, h in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    while stack[-1] != -1:
        height = heights[stack.pop()]
        width = len(heights) - stack[-1] - 1
        max_area = max(max_area, height * width)

    return max_area

# ================================================================
# DEQUE — SLIDING WINDOW MAXIMUM
# ================================================================

def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
    """
    Maximum in every sliding window of size k.
    O(n) time — monotonic decreasing deque

    APPROACH 1 (Brute): O(n*k) — find max in each window
    APPROACH 2 (Deque): O(n)

    INTERVIEW SCRIPT:
    "Maintain a deque storing indices in decreasing order of values.
     Front of deque = index of maximum in current window.
     For each new element:
      - Remove indices outside window from front.
      - Remove smaller elements from back (they'll never be max).
      - Add current index to back.
      - Front of deque = maximum for current window."
    """
    dq = deque()  # stores indices, decreasing values
    result = []

    for i, num in enumerate(nums):
        # Remove indices outside window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove smaller elements from back
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Window is fully formed
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# ================================================================
# EXPRESSION EVALUATION
# ================================================================

def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluate Reverse Polish Notation — O(n)

    INTERVIEW SCRIPT:
    "Reverse Polish Notation (postfix): operands before operators.
     Use a stack. Push numbers. For operators, pop two operands,
     compute, push result."
    """
    stack = []
    ops = {'+', '-', '*', '/'}

    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # truncate toward zero
        else:
            stack.append(int(token))
    return stack[0]

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Stack applications:
- Function call stack in runtimes
- DFS traversal (iterative)
- Undo/Redo in text editors
- Browser back/forward navigation
- Expression parsing/evaluation
- Monotonic stack for range queries

Queue applications:
- BFS traversal
- Task/job scheduling
- Print queue
- Event-driven systems
- Cache eviction (FIFO)

Deque applications:
- Sliding window max/min
- Palindrome checking
- Undo/Redo with complex history
"""

if __name__ == "__main__":
    # Parentheses
    print("Valid '{[]}':", is_valid_parentheses("{[]}"))
    print("Valid '([)]':", is_valid_parentheses("([)]"))

    # Decode string
    print("Decode '3[a]2[bc]':", decode_string("3[a]2[bc]"))

    # Monotonic stack
    print("Next greater [2,1,2,4,3]:", next_greater_element([2,1,2,4,3]))
    print("Daily temps [73,74,75,71,69,72,76,73]:",
          daily_temperatures([73,74,75,71,69,72,76,73]))

    # Sliding window max
    print("Sliding window max [1,3,-1,-3,5,3,6,7] k=3:",
          sliding_window_maximum([1,3,-1,-3,5,3,6,7], 3))

    # Largest rectangle
    print("Largest rectangle [2,1,5,6,2,3]:",
          largest_rectangle_histogram([2,1,5,6,2,3]))
