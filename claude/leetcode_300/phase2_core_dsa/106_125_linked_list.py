"""
================================================================
LEETCODE PHASE 2 (Problems 106-125): LINKED LIST
================================================================
"""

from typing import Optional, List

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __repr__(self):
        vals, curr, seen = [], self, set()
        while curr and id(curr) not in seen:
            vals.append(str(curr.val)); seen.add(id(curr)); curr = curr.next
        return " -> ".join(vals)

def build(vals):
    if not vals: return None
    head = ListNode(vals[0])
    curr = head
    for v in vals[1:]: curr.next = ListNode(v); curr = curr.next
    return head

# ================================================================
# 106. REVERSE LINKED LIST (Easy)
# ================================================================
def reverse_list_brute(head: Optional[ListNode]) -> Optional[ListNode]:
    """APPROACH 1: O(n) extra space — collect values, rebuild"""
    vals = []
    curr = head
    while curr: vals.append(curr.val); curr = curr.next
    curr = head
    for v in reversed(vals): curr.val = v; curr = curr.next
    return head

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    APPROACH 2: O(1) space — three pointer iterative

    INTERVIEW SCRIPT:
    "Three pointers: prev=None, curr=head, next_node.
     Save next, reverse pointer, advance both.
     After loop, prev is new head."
    """
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    APPROACH 3: Recursive — O(n) space

    INTERVIEW SCRIPT:
    "Trust recursion to reverse rest. head.next.next = head (reverse one link).
     head.next = None (disconnect). Return new_head from recursion."
    """
    if not head or not head.next: return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head

# ================================================================
# 107. MERGE TWO SORTED LISTS (Easy)
# ================================================================
def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    INTERVIEW SCRIPT:
    "Use dummy node to simplify edge cases.
     Compare heads, append smaller, advance that pointer.
     Attach remaining list when one is exhausted."
    """
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val: curr.next = l1; l1 = l1.next
        else: curr.next = l2; l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

# Time: O(m+n), Space: O(1)

# ================================================================
# 108. LINKED LIST CYCLE (Easy)
# ================================================================
def has_cycle_hashset(head: Optional[ListNode]) -> bool:
    """APPROACH 1: O(n) space — hash set of visited nodes"""
    seen = set()
    curr = head
    while curr:
        if id(curr) in seen: return True
        seen.add(id(curr)); curr = curr.next
    return False

def has_cycle(head: Optional[ListNode]) -> bool:
    """
    APPROACH 2: O(1) space — Floyd's cycle detection

    INTERVIEW SCRIPT:
    "Slow moves 1 step, fast moves 2 steps.
     If cycle: fast catches slow (relative speed 1, they meet).
     If no cycle: fast reaches None.
     Like two runners on a track — if circular, faster one laps slower."
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next; fast = fast.next.next
        if slow is fast: return True
    return False

# ================================================================
# 109. LINKED LIST CYCLE II — Find Cycle Start (Medium)
# ================================================================
def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    INTERVIEW SCRIPT:
    "Step 1: Detect cycle with Floyd's (slow and fast meet at some node).
     Step 2: Reset slow to head. Move both one step at a time.
     They meet at cycle start.
     MATH: distance(head→start) = distance(meeting→start)."
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next; fast = fast.next.next
        if slow is fast: break
    else: return None

    slow = head
    while slow is not fast:
        slow = slow.next; fast = fast.next
    return slow

# ================================================================
# 110. REMOVE NTH NODE FROM END (Medium)
# ================================================================
def remove_nth_from_end_two_pass(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """APPROACH 1: O(L) two pass — find length, then remove"""
    dummy = ListNode(0); dummy.next = head
    length = 0; curr = head
    while curr: length += 1; curr = curr.next
    curr = dummy
    for _ in range(length - n): curr = curr.next
    curr.next = curr.next.next
    return dummy.next

def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    APPROACH 2: O(L) one pass — two pointers n apart

    INTERVIEW SCRIPT:
    "Advance fast pointer n+1 steps first.
     Then advance both until fast is None.
     Slow is now at node BEFORE the target.
     Remove: slow.next = slow.next.next.
     Dummy node handles removing the head."
    """
    dummy = ListNode(0); dummy.next = head
    fast = slow = dummy
    for _ in range(n+1): fast = fast.next
    while fast: slow = slow.next; fast = fast.next
    slow.next = slow.next.next
    return dummy.next

# ================================================================
# 111. ADD TWO NUMBERS (Medium)
# ================================================================
def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Numbers stored in reverse. Add like elementary school.

    INTERVIEW SCRIPT:
    "Simulate addition: traverse both lists simultaneously.
     Sum = l1.val + l2.val + carry. carry = sum // 10.
     Create new node with sum % 10.
     After loop: if carry remains, add final node."
    """
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    while l1 or l2 or carry:
        val = carry
        if l1: val += l1.val; l1 = l1.next
        if l2: val += l2.val; l2 = l2.next
        carry, val = divmod(val, 10)
        curr.next = ListNode(val); curr = curr.next
    return dummy.next

# ================================================================
# 112. INTERSECTION OF TWO LINKED LISTS (Easy)
# ================================================================
def get_intersection_node_brute(headA, headB):
    """APPROACH 1: O(m*n) — for each A node, scan B"""
    curr_a = headA
    while curr_a:
        curr_b = headB
        while curr_b:
            if curr_a is curr_b: return curr_a
            curr_b = curr_b.next
        curr_a = curr_a.next
    return None

def get_intersection_node(headA, headB):
    """
    APPROACH 2: O(m+n) — two pointer trick

    INTERVIEW SCRIPT:
    "Two pointers start at heads. When one reaches end, redirect to other's head.
     They meet at intersection (or None if no intersection).
     WHY? Both travel distance a + b + c (same total), meeting at intersection."
    """
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a

# ================================================================
# 113. PALINDROME LINKED LIST (Easy)
# ================================================================
def is_palindrome_list(head: Optional[ListNode]) -> bool:
    """
    APPROACH 1: O(n) space — copy to array
    APPROACH 2: O(1) space — reverse second half

    INTERVIEW SCRIPT:
    "1. Find middle with fast/slow pointers.
     2. Reverse second half.
     3. Compare first and second halves.
     4. (Optional: restore list)."
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next; fast = fast.next.next

    # Reverse second half
    prev, curr = None, slow
    while curr:
        nxt = curr.next; curr.next = prev; prev = curr; curr = nxt

    # Compare
    left, right = head, prev
    while right:
        if left.val != right.val: return False
        left = left.next; right = right.next
    return True

# ================================================================
# 114. REORDER LIST (Medium)
# ================================================================
def reorder_list(head: Optional[ListNode]) -> None:
    """
    L0→L1→…→Ln → L0→Ln→L1→Ln-1→…

    INTERVIEW SCRIPT:
    "3 steps:
     1. Find middle (fast/slow pointer).
     2. Reverse second half.
     3. Merge alternately: one from first half, one from reversed second."
    """
    if not head or not head.next: return

    # Find middle
    slow = fast = head
    while fast and fast.next: slow = slow.next; fast = fast.next.next

    # Reverse second half
    second = slow.next; slow.next = None
    prev, curr = None, second
    while curr:
        nxt = curr.next; curr.next = prev; prev = curr; curr = nxt
    second = prev

    # Merge alternately
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second; second.next = tmp1
        first = tmp1; second = tmp2

# ================================================================
# 115. COPY LIST WITH RANDOM POINTER (Medium)
# ================================================================
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = x; self.next = next; self.random = random

def copy_random_list_brute(head: Optional[Node]) -> Optional[Node]:
    """APPROACH 1: O(n) space — two passes with hashmap"""
    if not head: return None
    node_map = {}
    curr = head
    while curr:
        node_map[curr] = Node(curr.val); curr = curr.next
    curr = head
    while curr:
        if curr.next: node_map[curr].next = node_map[curr.next]
        if curr.random: node_map[curr].random = node_map[curr.random]
        curr = curr.next
    return node_map[head]

def copy_random_list(head: Optional[Node]) -> Optional[Node]:
    """
    APPROACH 2: O(1) space — interleave original and copy nodes

    INTERVIEW SCRIPT:
    "Three passes:
     1. Insert copy of each node right after original.
     2. Set random pointers: copy.random = original.random.next.
     3. Separate original and copy lists."
    """
    if not head: return None

    # Insert copies
    curr = head
    while curr:
        copy = Node(curr.val, curr.next)
        curr.next = copy; curr = copy.next

    # Set random
    curr = head
    while curr:
        if curr.random: curr.next.random = curr.random.next
        curr = curr.next.next

    # Separate
    dummy = Node(0)
    copy_curr = dummy; curr = head
    while curr:
        copy_curr.next = curr.next
        curr.next = curr.next.next
        copy_curr = copy_curr.next; curr = curr.next

    return dummy.next

# ================================================================
# 116. ROTATE LIST (Medium)
# ================================================================
def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    INTERVIEW SCRIPT:
    "Find length and tail. k = k % length (handle k > length).
     Connect tail to head (make circular).
     New tail is at position (length - k - 1).
     Break the circle there."
    """
    if not head or not head.next or k == 0: return head
    length = 1; tail = head
    while tail.next: tail = tail.next; length += 1
    tail.next = head  # make circular
    k = k % length
    steps = length - k
    new_tail = head
    for _ in range(steps - 1): new_tail = new_tail.next
    new_head = new_tail.next; new_tail.next = None
    return new_head

# ================================================================
# 117. PARTITION LIST (Medium)
# ================================================================
def partition(head: Optional[ListNode], x: int) -> Optional[ListNode]:
    """
    Partition list: all nodes < x come before nodes >= x.
    Preserve relative order.

    INTERVIEW SCRIPT:
    "Two dummy-headed lists: less and greater.
     Traverse original: append to less if val<x, else to greater.
     Connect less list to greater list. O(n) time, O(1) space."
    """
    less = less_dummy = ListNode(0)
    greater = greater_dummy = ListNode(0)
    curr = head
    while curr:
        if curr.val < x: less.next = curr; less = less.next
        else: greater.next = curr; greater = greater.next
        curr = curr.next
    greater.next = None
    less.next = greater_dummy.next
    return less_dummy.next

# ================================================================
# 118. SWAP NODES IN PAIRS (Medium)
# ================================================================
def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    INTERVIEW SCRIPT:
    "Recursive: swap first two, then recurse on rest.
     Or iterative: use dummy node, process pairs.
     O(n) time, O(1) iterative space."
    """
    dummy = ListNode(0); dummy.next = head; prev = dummy
    while prev.next and prev.next.next:
        a = prev.next; b = prev.next.next
        prev.next = b; a.next = b.next; b.next = a
        prev = a
    return dummy.next

# ================================================================
# 119. REVERSE NODES IN K-GROUP (Hard)
# ================================================================
def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    INTERVIEW SCRIPT:
    "Check if k nodes remain. If not: return as-is (no reversal).
     Reverse k nodes. Connect reversed group to result of recursing on remainder.
     The original head becomes new tail of reversed group."
    """
    def has_k_nodes(node, k):
        count = 0
        while node and count < k: node = node.next; count += 1
        return count == k

    if not has_k_nodes(head, k): return head

    prev, curr = None, head
    for _ in range(k):
        nxt = curr.next; curr.next = prev; prev = curr; curr = nxt

    head.next = reverse_k_group(curr, k)
    return prev

# ================================================================
# 120. DELETE NODE IN LINKED LIST (Medium)
# ================================================================
def delete_node(node: ListNode) -> None:
    """
    Can't access head! Only given the node to delete.

    INTERVIEW SCRIPT:
    "Copy next node's value to current, then delete next node.
     This 'shifts' the deletion forward."
    """
    node.val = node.next.val
    node.next = node.next.next

# ================================================================
# 121-125. MORE LINKED LIST PROBLEMS
# ================================================================

def remove_elements(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """203. Remove Linked List Elements"""
    dummy = ListNode(0); dummy.next = head; curr = dummy
    while curr.next:
        if curr.next.val == val: curr.next = curr.next.next
        else: curr = curr.next
    return dummy.next

def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """876. Middle of Linked List — fast/slow pointer"""
    slow = fast = head
    while fast and fast.next: slow = slow.next; fast = fast.next.next
    return slow

def odd_even_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    328. Odd Even Linked List — group odd-indexed then even-indexed

    INTERVIEW SCRIPT:
    "Two pointers: odd and even. Alternate assignment.
     Connect odd list's tail to even list's head."
    """
    if not head: return head
    odd = head; even = head.next; even_head = even
    while even and even.next:
        odd.next = even.next; odd = odd.next
        even.next = odd.next; even = even.next
    odd.next = even_head
    return head

def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    148. Sort List — O(n log n) merge sort on linked list

    INTERVIEW SCRIPT:
    "Merge sort: find middle (fast/slow), split, sort each half, merge.
     O(n log n) time. O(log n) space (recursion stack) or O(1) bottom-up."
    """
    if not head or not head.next: return head
    slow, fast = head, head.next
    while fast and fast.next: slow = slow.next; fast = fast.next.next
    mid = slow.next; slow.next = None
    left = sort_list(head); right = sort_list(mid)
    return merge_two_lists(left, right)

def flatten_multilevel(head) -> Optional[ListNode]:
    """
    430. Flatten Multilevel Doubly Linked List

    INTERVIEW SCRIPT:
    "DFS: when child found, insert child list between current and next.
     Process entire child list before continuing."
    """
    if not head: return head
    curr = head
    while curr:
        if curr.child:
            child = curr.child; nxt = curr.next
            curr.next = child; child.prev = curr; curr.child = None
            tail = child
            while tail.next: tail = tail.next
            tail.next = nxt
            if nxt: nxt.prev = tail
        curr = curr.next
    return head

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Reverse [1,2,3,4,5]:", reverse_list(build([1,2,3,4,5])))
    print("Merge [1,2,4] and [1,3,4]:", merge_two_lists(build([1,2,4]), build([1,3,4])))
    print("Remove 2nd from end [1,2,3,4,5]:", remove_nth_from_end(build([1,2,3,4,5]), 2))
    print("Palindrome [1,2,2,1]:", is_palindrome_list(build([1,2,2,1])))
    l1 = build([2,4,3]); l2 = build([5,6,4])
    print("Add [2,4,3]+[5,6,4]:", add_two_numbers(l1, l2))
    print("Middle [1,2,3,4,5]:", middle_node(build([1,2,3,4,5])).val)
    print("Swap pairs [1,2,3,4]:", swap_pairs(build([1,2,3,4])))
