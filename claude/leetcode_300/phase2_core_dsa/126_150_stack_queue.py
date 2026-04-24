"""
================================================================
LEETCODE PHASE 2 (Problems 126-150): STACK & QUEUE
================================================================
"""

from typing import List, Optional
from collections import deque

# ================================================================
# 126. VALID PARENTHESES (Easy)
# ================================================================
def is_valid_brute(s: str) -> bool:
    """APPROACH 1: O(n²) — keep removing matching pairs"""
    while '()' in s or '[]' in s or '{}' in s:
        s = s.replace('()','').replace('[]','').replace('{}','')
    return s == ''

def is_valid(s: str) -> bool:
    """
    APPROACH 2: O(n) — stack

    INTERVIEW SCRIPT:
    "For each char: if opening: push to stack.
     If closing: check if matches top of stack.
     Empty stack at end = valid.
     Edge: closing when stack empty → invalid."
    """
    stack = []
    mapping = {')':'(', ']':'[', '}':'{'}
    for c in s:
        if c in mapping:
            if not stack or stack[-1] != mapping[c]: return False
            stack.pop()
        else: stack.append(c)
    return not stack

# Time: O(n), Space: O(n)

# ================================================================
# 127. MIN STACK (Easy)
# ================================================================
class MinStack:
    """
    INTERVIEW SCRIPT:
    "Two stacks: main stack + min_stack.
     min_stack[i] = minimum at depth i.
     When pushing: new_min = min(val, current_min).
     Push to both stacks. Pop from both.
     getMin() = min_stack[-1]. O(1) for all ops."
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self) -> None:
        self.stack.pop(); self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

# ================================================================
# 128. IMPLEMENT QUEUE USING STACKS (Easy)
# ================================================================
class MyQueue:
    """
    INTERVIEW SCRIPT:
    "Two stacks: inbox (push here) and outbox (pop from here).
     Push: always to inbox.
     Pop/peek: if outbox empty, pour ALL of inbox into outbox (reverses order).
     Each element moves inbox→outbox exactly once → amortized O(1)."
    """
    def __init__(self):
        self.inbox = []; self.outbox = []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _transfer(self):
        if not self.outbox:
            while self.inbox: self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._transfer(); return self.outbox.pop()

    def peek(self) -> int:
        self._transfer(); return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox

# ================================================================
# 129. IMPLEMENT STACK USING QUEUES (Easy)
# ================================================================
class MyStack:
    """
    INTERVIEW SCRIPT:
    "Use one queue. On push: append, then rotate queue so new element is at front.
     Rotate: dequeue and enqueue n-1 times after pushing.
     This makes latest element always at front for O(1) top/pop."
    """
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q) - 1): self.q.append(self.q.popleft())

    def pop(self) -> int: return self.q.popleft()
    def top(self) -> int: return self.q[0]
    def empty(self) -> bool: return not self.q

# ================================================================
# 130. DAILY TEMPERATURES (Medium)
# ================================================================
def daily_temperatures_brute(temperatures: List[int]) -> List[int]:
    """APPROACH 1: O(n²) — for each day scan forward"""
    result = [0] * len(temperatures)
    for i in range(len(temperatures)):
        for j in range(i+1, len(temperatures)):
            if temperatures[j] > temperatures[i]:
                result[i] = j - i; break
    return result

def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    APPROACH 2: O(n) — monotonic decreasing stack

    INTERVIEW SCRIPT:
    "Monotonic decreasing stack of indices.
     For each temp: pop while stack top's temp < current temp.
     Popped index's answer = current index - popped index.
     Push current index."
    """
    result = [0] * len(temperatures)
    stack = []
    for i, temp in enumerate(temperatures):
        while stack and temp > temperatures[stack[-1]]:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx
        stack.append(i)
    return result

# ================================================================
# 131. NEXT GREATER ELEMENT I (Easy)
# ================================================================
def next_greater_element(nums1: List[int], nums2: List[int]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Build NGE map for nums2 using monotonic stack.
     next_greater[x] = next greater element after x in nums2.
     Then answer for each num in nums1 = next_greater.get(num, -1)."
    """
    next_greater = {}
    stack = []
    for num in nums2:
        while stack and num > stack[-1]:
            next_greater[stack.pop()] = num
        stack.append(num)
    return [next_greater.get(num, -1) for num in nums1]

# ================================================================
# 132. NEXT GREATER ELEMENT II (Medium)
# ================================================================
def next_greater_elements(nums: List[int]) -> List[int]:
    """
    Circular array version.

    INTERVIEW SCRIPT:
    "Simulate circular by iterating 2n times with index % n.
     Only push to stack for first n elements (avoid duplicates in result)."
    """
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[i % n] > nums[stack[-1]]:
            result[stack.pop()] = nums[i % n]
        if i < n: stack.append(i)
    return result

# ================================================================
# 133. EVALUATE REVERSE POLISH NOTATION (Medium)
# ================================================================
def eval_rpn(tokens: List[str]) -> int:
    """
    INTERVIEW SCRIPT:
    "Postfix notation: operators come after operands.
     Stack: push numbers, on operator pop two, compute, push result.
     Division truncates toward zero: int(a/b) not a//b."
    """
    stack = []
    ops = {'+', '-', '*', '/'}
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            if token == '+': stack.append(a+b)
            elif token == '-': stack.append(a-b)
            elif token == '*': stack.append(a*b)
            else: stack.append(int(a/b))  # truncate toward zero
        else: stack.append(int(token))
    return stack[0]

# ================================================================
# 134. DECODE STRING (Medium)
# ================================================================
def decode_string_brute(s: str) -> str:
    """APPROACH 1: Recursive"""
    def decode(s, i):
        result = ""
        while i < len(s) and s[i] != ']':
            if s[i].isdigit():
                k = 0
                while s[i].isdigit(): k = k*10 + int(s[i]); i += 1
                i += 1  # skip '['
                inner, i = decode(s, i)
                i += 1  # skip ']'
                result += inner * k
            else: result += s[i]; i += 1
        return result, i
    return decode(s, 0)[0]

def decode_string(s: str) -> str:
    """
    APPROACH 2: O(n) — two stacks

    INTERVIEW SCRIPT:
    "Two stacks: count_stack and string_stack.
     Digit: accumulate count.
     '[': push current string and count to stacks, reset.
     ']': pop count and prev_str, curr = prev_str + curr*count.
     Letter: append to current string."
    """
    count_stack, str_stack = [], []
    curr_str, curr_num = "", 0
    for c in s:
        if c.isdigit():
            curr_num = curr_num * 10 + int(c)
        elif c == '[':
            count_stack.append(curr_num); str_stack.append(curr_str)
            curr_num = 0; curr_str = ""
        elif c == ']':
            k = count_stack.pop(); prev = str_stack.pop()
            curr_str = prev + curr_str * k
        else: curr_str += c
    return curr_str

# ================================================================
# 135. BASIC CALCULATOR II (Medium)
# ================================================================
def calculate(s: str) -> int:
    """
    INTERVIEW SCRIPT:
    "Process without parentheses (+ - * /).
     Stack: push positive numbers as-is.
     For '+': push num. For '-': push -num.
     For '*' and '/': pop, compute with num, push result.
     Sum stack at end."
    """
    stack = []; num = 0; op = '+'
    s = s.replace(' ', '')
    for i, c in enumerate(s):
        if c.isdigit(): num = num * 10 + int(c)
        if c in '+-*/' or i == len(s)-1:
            if op == '+': stack.append(num)
            elif op == '-': stack.append(-num)
            elif op == '*': stack.append(stack.pop() * num)
            elif op == '/': stack.append(int(stack.pop() / num))
            op = c; num = 0
    return sum(stack)

# ================================================================
# 136. LARGEST RECTANGLE IN HISTOGRAM (Hard)
# ================================================================
def largest_rectangle_brute(heights: List[int]) -> int:
    """APPROACH 1: O(n²) — try each bar as shortest"""
    max_area = 0
    for i in range(len(heights)):
        min_h = heights[i]
        for j in range(i, len(heights)):
            min_h = min(min_h, heights[j])
            max_area = max(max_area, min_h * (j-i+1))
    return max_area

def largest_rectangle(heights: List[int]) -> int:
    """
    APPROACH 2: O(n) — monotonic increasing stack

    INTERVIEW SCRIPT:
    "For each bar, it can extend left to the first shorter bar on its left,
     and right to the first shorter bar on its right.
     Monotonic increasing stack gives us this info efficiently.
     When we pop bar i (because current bar is shorter):
       width = current_index - stack_top - 1 (between two shorter bars)
       area = heights[i] * width."
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
# 137. SLIDING WINDOW MAXIMUM (Hard)
# ================================================================
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Monotonic decreasing deque of indices.
     Front = max of current window.
     For each element: remove stale indices from front (outside window).
     Remove smaller elements from back (useless).
     Push current. If window full: append front to result."
    """
    dq, result = deque(), []
    for i, num in enumerate(nums):
        while dq and dq[0] <= i-k: dq.popleft()
        while dq and nums[dq[-1]] < num: dq.pop()
        dq.append(i)
        if i >= k-1: result.append(nums[dq[0]])
    return result

# ================================================================
# 138. ONLINE STOCK SPAN (Medium)
# ================================================================
class StockSpanner:
    """
    Find the span of stock price (consecutive days with price <= today).

    INTERVIEW SCRIPT:
    "Monotonic decreasing stack of (price, span) pairs.
     For current price: pop all pairs with price <= current.
     Accumulate their spans (current span covers all those days too).
     Push (current_price, accumulated_span)."
    """
    def __init__(self):
        self.stack = []  # (price, span)

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span

# ================================================================
# 139. SIMPLIFY PATH (Medium)
# ================================================================
def simplify_path(path: str) -> str:
    """
    INTERVIEW SCRIPT:
    "Split by '/'. Use stack for directory navigation.
     '..' means go up (pop if stack not empty).
     '.' and '' mean stay (skip).
     Any other name: push to stack.
     Join with '/' prefixed with '/'."
    """
    stack = []
    for part in path.split('/'):
        if part == '..':
            if stack: stack.pop()
        elif part and part != '.':
            stack.append(part)
    return '/' + '/'.join(stack)

# ================================================================
# 140. REMOVE K DIGITS (Medium)
# ================================================================
def remove_k_digits(num: str, k: int) -> str:
    """
    Remove k digits to make smallest number.

    INTERVIEW SCRIPT:
    "Monotonic increasing stack (greedy).
     For each digit: while stack[-1] > current digit AND k > 0:
       pop from stack and decrement k.
     If k remaining: remove from end.
     Result is stack joined (or '0' if empty)."
    """
    stack = []
    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop(); k -= 1
        stack.append(digit)
    if k: stack = stack[:-k]
    return ''.join(stack).lstrip('0') or '0'

# ================================================================
# 141-145. MORE STACK PROBLEMS
# ================================================================

def asteroid_collision(asteroids: List[int]) -> List[int]:
    """
    735. Asteroid Collision
    Positive goes right, negative goes left. Equal destroy each other.

    INTERVIEW SCRIPT:
    "Stack: push positive asteroids. When negative: handle collision.
     Pop positives smaller than |negative| (negative destroys them).
     If equal: pop both. If positive larger: negative is destroyed.
     If stack empty or negative on top: push negative."
    """
    stack = []
    for a in asteroids:
        destroyed = False
        while stack and a < 0 < stack[-1]:
            if stack[-1] < -a: stack.pop(); continue
            elif stack[-1] == -a: stack.pop()
            destroyed = True; break
        if not destroyed: stack.append(a)
    return stack

def car_fleet(target: int, position: List[int], speed: List[int]) -> int:
    """
    853. Car Fleet
    Cars join a fleet if slower car catches slower car.

    INTERVIEW SCRIPT:
    "Sort by position descending. Compute time to reach target.
     Stack: if current car arrives LATER than top of stack → new fleet.
     If arrives same time or earlier: joins existing fleet (pop)."
    """
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    for pos, spd in cars:
        time = (target - pos) / spd
        if not stack or time > stack[-1]: stack.append(time)
    return len(stack)

def score_of_parentheses(s: str) -> int:
    """
    856. Score of Parentheses
    '()' = 1, 'AB' = A+B, '(A)' = 2*A

    INTERVIEW SCRIPT:
    "Stack: push 0 for each '(' (placeholder).
     On ')': pop top. If top==0: it's '()' → push 1.
             Else: it's '(A)' → push 2*top. Merge: while peek is int, add."
    """
    stack = [0]
    for c in s:
        if c == '(': stack.append(0)
        else:
            v = stack.pop()
            stack[-1] += max(2*v, 1)
    return stack[0]

def exclusive_time(n: int, logs: List[str]) -> List[int]:
    """
    636. Exclusive Time of Functions

    INTERVIEW SCRIPT:
    "Stack of running functions. Process start/end events.
     On start: if stack non-empty, charge time to current top. Push new.
     On end: pop, charge time to popped function. Update prev_time."
    """
    result = [0] * n
    stack = []
    prev_time = 0
    for log in logs:
        fid, event, time = log.split(':')
        fid, time = int(fid), int(time)
        if event == 'start':
            if stack: result[stack[-1]] += time - prev_time
            stack.append(fid); prev_time = time
        else:
            result[stack.pop()] += time - prev_time + 1
            prev_time = time + 1
    return result

def moving_average(size: int):
    """
    346. Moving Average from Data Stream

    INTERVIEW SCRIPT:
    "Use deque as sliding window. Track running sum.
     On add: if full, remove oldest and subtract from sum.
     Add new to deque and sum. Return sum / current_size."
    """
    from collections import deque
    window = deque()
    window_sum = 0

    def next_val(val):
        nonlocal window_sum
        window_sum += val
        window.append(val)
        if len(window) > size:
            window_sum -= window.popleft()
        return window_sum / len(window)

    return next_val

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Valid Parentheses '()[]{}':", is_valid("()[]{}"))
    print("Valid Parentheses '(]':", is_valid("(]"))
    print("Daily Temps [73,74,75,71,69,72,76,73]:", daily_temperatures([73,74,75,71,69,72,76,73]))
    print("Next Greater [4,1,2],[1,3,4,2]:", next_greater_element([4,1,2],[1,3,4,2]))
    print("Eval RPN ['2','1','+','3','*']:", eval_rpn(['2','1','+','3','*']))
    print("Decode '3[a]2[bc]':", decode_string("3[a]2[bc]"))
    print("Largest Rectangle [2,1,5,6,2,3]:", largest_rectangle([2,1,5,6,2,3]))
    print("Sliding Window Max [1,3,-1,-3,5,3,6,7] k=3:", max_sliding_window([1,3,-1,-3,5,3,6,7],3))
    print("Simplify '/home//foo/':", simplify_path("/home//foo/"))
    print("Remove K Digits '1432219' k=3:", remove_k_digits("1432219",3))
    print("Asteroid Collision [5,10,-5]:", asteroid_collision([5,10,-5]))
