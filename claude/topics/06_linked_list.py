"""
================================================================
TOPIC 6: LINKED LIST
================================================================
Singly, Doubly Linked Lists
Key Algorithms: Reversal, Fast/Slow Pointers, Floyd's Cycle

INTERVIEW COMMUNICATION:
"Linked lists allow O(1) insert/delete at known positions.
 The trade-off is O(n) random access vs O(1) for arrays.
 Key patterns: two-pointer (fast/slow), dummy node, in-place reversal."
================================================================
"""

from typing import Optional, List

# ================================================================
# NODE DEFINITION
# ================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals = []
        curr = self
        seen = set()
        while curr and id(curr) not in seen:
            vals.append(str(curr.val))
            seen.add(id(curr))
            curr = curr.next
        return " -> ".join(vals)

# Helper functions
def build_list(values: List[int]) -> Optional[ListNode]:
    if not values:
        return None
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def list_to_array(head: Optional[ListNode]) -> List[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

# ================================================================
# BASIC OPERATIONS
# ================================================================

def insert_at_head(head: Optional[ListNode], val: int) -> ListNode:
    """O(1) — new node points to old head"""
    new_node = ListNode(val)
    new_node.next = head
    return new_node

def insert_at_tail(head: Optional[ListNode], val: int) -> ListNode:
    """O(n) — traverse to end"""
    new_node = ListNode(val)
    if not head:
        return new_node
    curr = head
    while curr.next:
        curr = curr.next
    curr.next = new_node
    return head

def delete_by_value(head: Optional[ListNode], val: int) -> Optional[ListNode]:
    """
    O(n) — uses dummy node pattern

    INTERVIEW SCRIPT:
    "Use a dummy node pointing to head.
     This handles edge case of deleting the head node uniformly."
    """
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    curr = head
    while curr:
        if curr.val == val:
            prev.next = curr.next
        else:
            prev = curr
        curr = curr.next
    return dummy.next

# ================================================================
# REVERSAL — Most Important LL Algorithm
# ================================================================

def reverse_linked_list_iterative(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse singly linked list — O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Three pointers: prev, curr, next_node.
     Save next before overwriting.
     Point curr.next to prev (reverse the pointer).
     Move all three pointers forward.
     Repeat until curr is None. Return prev (new head)."

    USE CASE: Display order reversal, undo operations
    """
    prev = None
    curr = head
    while curr:
        next_node = curr.next   # save next
        curr.next = prev        # reverse pointer
        prev = curr             # move prev forward
        curr = next_node        # move curr forward
    return prev  # new head

def reverse_linked_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Recursive reversal — O(n) time, O(n) space (call stack)

    INTERVIEW SCRIPT:
    "Base: if 0 or 1 nodes, already reversed.
     Trust recursion to reverse rest.
     After recursion: head.next points to old second node (now tail of reversed).
     Make old second node point back to head.
     Disconnect head.next."
    """
    if not head or not head.next:
        return head
    new_head = reverse_linked_list_recursive(head.next)
    head.next.next = head  # old next points back to head
    head.next = None       # disconnect
    return new_head

def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    Reverse nodes in k-group — O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Check if k nodes remain. If not, leave as-is.
     Reverse k nodes using standard reversal.
     Connect reversed group to result of recursing on remainder."
    """
    def has_k_nodes(node, k):
        count = 0
        while node and count < k:
            node = node.next
            count += 1
        return count == k

    if not has_k_nodes(head, k):
        return head

    prev, curr = None, head
    for _ in range(k):
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    head.next = reverse_k_group(curr, k)
    return prev

# ================================================================
# FAST & SLOW POINTERS (Floyd's Algorithm)
# ================================================================

def has_cycle(head: Optional[ListNode]) -> bool:
    """
    Detect cycle in linked list — O(n) time, O(1) space

    APPROACH 1 (HashSet): O(n) space — store visited nodes
    APPROACH 2 (Floyd's): O(1) space — fast/slow pointers

    INTERVIEW SCRIPT:
    "Floyd's cycle detection: slow moves 1 step, fast moves 2.
     If cycle exists, they MUST meet (like runners on a circular track).
     If fast reaches null, no cycle.
     WHY they meet: relative speed is 1, so fast catches up."
    """
    # Approach 1: HashSet
    def with_hashset():
        seen = set()
        curr = head
        while curr:
            if id(curr) in seen:
                return True
            seen.add(id(curr))
            curr = curr.next
        return False

    # Approach 2: Floyd's O(1) space
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def find_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Find where cycle begins — O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "After slow and fast meet, reset one pointer to head.
     Move both one step at a time. Where they meet = cycle start.
     Mathematical proof: distance from head to cycle start =
     distance from meeting point to cycle start."
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None  # no cycle

    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow

def find_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Find middle node — O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "Fast/slow pointers: fast moves 2x speed.
     When fast reaches end, slow is at middle.
     For even-length: slow will be at second middle."
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def is_palindrome_list(head: Optional[ListNode]) -> bool:
    """
    Check if linked list is palindrome — O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "1. Find middle with fast/slow pointers.
     2. Reverse second half.
     3. Compare first and second halves.
     4. (Optionally restore the list)"
    """
    if not head or not head.next:
        return True

    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    second_half = reverse_linked_list_iterative(slow)
    first_half = head

    p1, p2 = first_half, second_half
    result = True
    while p2:
        if p1.val != p2.val:
            result = False
            break
        p1 = p1.next
        p2 = p2.next
    return result

# ================================================================
# REMOVE Nth NODE FROM END
# ================================================================

def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Remove nth node from end — O(L) time, O(1) space (L = list length)

    APPROACH 1: Two passes — find length, then remove
    APPROACH 2: One pass with two pointers

    INTERVIEW SCRIPT:
    "One-pass solution: use fast/slow pointers n apart.
     Advance fast pointer n+1 steps first.
     Then advance both until fast reaches null.
     Slow is now at node before the target.
     Use dummy node to handle edge case of removing head."
    """
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy

    for _ in range(n + 1):
        fast = fast.next

    while fast:
        slow = slow.next
        fast = fast.next

    slow.next = slow.next.next
    return dummy.next

# ================================================================
# MERGE SORTED LISTS
# ================================================================

def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merge two sorted linked lists — O(n+m) time, O(1) space

    INTERVIEW SCRIPT:
    "Use dummy head to simplify logic.
     Compare heads of both lists, append smaller.
     When one list exhausted, append rest of other."
    """
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

def merge_k_sorted_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted lists — O(n log k) with heap

    APPROACH 1 (Brute): Collect all, sort → O(n log n)
    APPROACH 2 (Heap): Process k heads simultaneously → O(n log k)

    INTERVIEW SCRIPT:
    "Use a min-heap of size k.
     Add first node from each list to heap.
     Pop minimum, add to result, push that node's next.
     O(n log k) — log k for heap operations, n total nodes."
    """
    import heapq

    dummy = ListNode(0)
    curr = dummy
    heap = []

    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next

# ================================================================
# REORDER LIST
# ================================================================

def reorder_list(head: Optional[ListNode]) -> None:
    """
    Reorder: L0→L1→...→Ln → L0→Ln→L1→Ln-1→...
    O(n) time, O(1) space

    INTERVIEW SCRIPT:
    "3-step approach:
     1. Find middle with slow/fast pointers.
     2. Reverse second half.
     3. Merge two halves alternately."
    """
    if not head or not head.next:
        return

    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    second = reverse_linked_list_iterative(slow.next)
    slow.next = None

    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2

# ================================================================
# COPY LIST WITH RANDOM POINTER
# ================================================================

class RandomNode:
    def __init__(self, x: int, next=None, random=None):
        self.val = x
        self.next = next
        self.random = random

def copy_random_list(head: Optional[RandomNode]) -> Optional[RandomNode]:
    """
    Deep copy linked list with random pointers.
    O(n) time, O(n) space

    INTERVIEW SCRIPT:
    "Use a hash map: original node → copy node.
     First pass: create all copies (just vals, no pointers).
     Second pass: set next and random using hash map lookup."
    """
    if not head:
        return None

    node_map = {}
    curr = head
    while curr:
        node_map[curr] = RandomNode(curr.val)
        curr = curr.next

    curr = head
    while curr:
        if curr.next:
            node_map[curr].next = node_map[curr.next]
        if curr.random:
            node_map[curr].random = node_map[curr.random]
        curr = curr.next

    return node_map[head]

# ================================================================
# DOUBLY LINKED LIST
# ================================================================

class DLLNode:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """
    USE CASE: Browser history (back/forward), LRU Cache,
              Undo/Redo operations
    """
    def __init__(self):
        self.head = DLLNode(0)  # dummy head
        self.tail = DLLNode(0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_to_front(self, node: DLLNode):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: DLLNode):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_last(self) -> Optional[DLLNode]:
        if self.tail.prev == self.head:
            return None
        last = self.tail.prev
        self.remove(last)
        return last

if __name__ == "__main__":
    # Reverse
    lst = build_list([1, 2, 3, 4, 5])
    print("Original:", lst)
    print("Reversed:", reverse_linked_list_iterative(lst))

    # Merge sorted
    l1 = build_list([1, 2, 4])
    l2 = build_list([1, 3, 4])
    print("Merged sorted:", merge_two_sorted_lists(l1, l2))

    # Find middle
    lst = build_list([1, 2, 3, 4, 5])
    print("Middle of [1,2,3,4,5]:", find_middle(lst).val)

    # Remove nth from end
    lst = build_list([1, 2, 3, 4, 5])
    print("Remove 2nd from end:", remove_nth_from_end(lst, 2))
