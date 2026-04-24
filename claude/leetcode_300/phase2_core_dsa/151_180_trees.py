"""
================================================================
LEETCODE PHASE 2 (Problems 151-180): TREES
================================================================
"""

from typing import Optional, List
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
    def __repr__(self): return f"TreeNode({self.val})"

def build(vals):
    if not vals: return None
    root = TreeNode(vals[0]); q = deque([root]); i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); q.append(node.right)
        i += 1
    return root

# ================================================================
# 151. MAXIMUM DEPTH OF BINARY TREE (Easy)
# ================================================================
def max_depth(root: Optional[TreeNode]) -> int:
    """
    APPROACH 1: DFS recursive — O(n)
    APPROACH 2: BFS level-order — O(n)

    INTERVIEW SCRIPT:
    "DFS: depth = 1 + max(left_depth, right_depth). Base: null=0.
     BFS: count levels. O(n) time both.
     DFS: O(h) space. BFS: O(w) space (w=max width)."
    """
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# ================================================================
# 152. SAME TREE (Easy)
# ================================================================
def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """
    INTERVIEW SCRIPT:
    "Both null: True. One null: False.
     Values differ: False.
     Else: check both left and right subtrees recursively."
    """
    if not p and not q: return True
    if not p or not q or p.val != q.val: return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)

# ================================================================
# 153. INVERT BINARY TREE (Easy)
# ================================================================
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    INTERVIEW SCRIPT:
    "Swap left and right children recursively.
     Base: null or leaf node.
     Post-order: invert children first, then swap."
    """
    if not root: return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

# ================================================================
# 154. SYMMETRIC TREE (Easy)
# ================================================================
def is_symmetric_brute(root: Optional[TreeNode]) -> bool:
    """APPROACH 1: Serialize and check palindrome"""
    def serialize(node):
        if not node: return [None]
        return [node.val] + serialize(node.left) + serialize(node.right)
    left = serialize(root.left); right = serialize(root.right)
    return left == right[::-1]

def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    APPROACH 2: O(n) — mirror check

    INTERVIEW SCRIPT:
    "Tree is symmetric if left subtree is mirror of right.
     is_mirror(l, r): both null → True. One null → False.
     Values equal AND l.left mirrors r.right AND l.right mirrors r.left."
    """
    def is_mirror(l, r):
        if not l and not r: return True
        if not l or not r or l.val != r.val: return False
        return is_mirror(l.left, r.right) and is_mirror(l.right, r.left)
    return is_mirror(root.left, root.right) if root else True

# ================================================================
# 155. BINARY TREE LEVEL ORDER TRAVERSAL (Medium)
# ================================================================
def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "BFS with queue. Process one level at a time.
     Key: snapshot queue size = nodes in current level.
     Process exactly that many nodes per iteration."
    """
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result

# ================================================================
# 156. BINARY TREE RIGHT SIDE VIEW (Medium)
# ================================================================
def right_side_view_bfs(root: Optional[TreeNode]) -> List[int]:
    """
    APPROACH 1: BFS — last element of each level

    INTERVIEW SCRIPT:
    "Level-order BFS. Last node of each level is visible from right."
    """
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        for i in range(len(queue)):
            node = queue.popleft()
            if i == len(queue): result.append(node.val)  # last in level
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(node.val)  # last processed = rightmost
    return result

def right_side_view(root: Optional[TreeNode]) -> List[int]:
    """
    APPROACH 2: DFS — visit right before left, record first per depth
    """
    result = []
    def dfs(node, depth):
        if not node: return
        if depth == len(result): result.append(node.val)
        dfs(node.right, depth+1)   # right first!
        dfs(node.left, depth+1)
    dfs(root, 0)
    return result

# ================================================================
# 157. VALIDATE BST (Medium)
# ================================================================
def is_valid_bst_wrong(root: Optional[TreeNode]) -> bool:
    """WRONG APPROACH: only check parent, not full range"""
    if not root: return True
    if root.left and root.left.val >= root.val: return False
    if root.right and root.right.val <= root.val: return False
    return is_valid_bst_wrong(root.left) and is_valid_bst_wrong(root.right)
    # BUG: Doesn't handle values from higher ancestors!

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    CORRECT APPROACH: pass valid range

    INTERVIEW SCRIPT:
    "Each node must be in range (min_val, max_val).
     Root: (-inf, +inf).
     Left child: (min_val, parent.val).
     Right child: (parent.val, max_val).
     Common mistake: only comparing with immediate parent."
    """
    def validate(node, min_val, max_val):
        if not node: return True
        if node.val <= min_val or node.val >= max_val: return False
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    return validate(root, float('-inf'), float('inf'))

# ================================================================
# 158. KTH SMALLEST IN BST (Medium)
# ================================================================
def kth_smallest_brute(root: Optional[TreeNode], k: int) -> int:
    """APPROACH 1: O(n) — inorder to list"""
    def inorder(node):
        if not node: return []
        return inorder(node.left) + [node.val] + inorder(node.right)
    return inorder(root)[k-1]

def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """
    APPROACH 2: O(h+k) — early-stop iterative inorder

    INTERVIEW SCRIPT:
    "Inorder of BST gives sorted elements.
     Iterative with early stop: stop at exactly k-th element.
     O(h+k) time — no need to visit all nodes."
    """
    stack = []; curr = root; count = 0
    while curr or stack:
        while curr: stack.append(curr); curr = curr.left
        curr = stack.pop(); count += 1
        if count == k: return curr.val
        curr = curr.right

# ================================================================
# 159. LOWEST COMMON ANCESTOR OF BST (Easy)
# ================================================================
def lca_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    INTERVIEW SCRIPT:
    "BST property: left < root < right.
     If both p,q < root: LCA in left subtree.
     If both p,q > root: LCA in right subtree.
     Else: root is split point → LCA is root."
    """
    while root:
        if p.val < root.val and q.val < root.val: root = root.left
        elif p.val > root.val and q.val > root.val: root = root.right
        else: return root

# ================================================================
# 160. LOWEST COMMON ANCESTOR OF BINARY TREE (Medium)
# ================================================================
def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    INTERVIEW SCRIPT:
    "If root is None, p, or q: return root.
     Recurse left and right. If both non-null: root is LCA.
     If only one non-null: LCA is in that subtree."
    """
    if not root or root == p or root == q: return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right: return root   # p in one subtree, q in other
    return left or right

# ================================================================
# 161. DIAMETER OF BINARY TREE (Easy)
# ================================================================
def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    INTERVIEW SCRIPT:
    "Diameter = max path through any node = left_depth + right_depth.
     Compute depth while updating max diameter.
     Return depth (not diameter) to parent: 1 + max(left, right)."
    """
    max_diam = [0]
    def depth(node):
        if not node: return 0
        left = depth(node.left); right = depth(node.right)
        max_diam[0] = max(max_diam[0], left + right)
        return 1 + max(left, right)
    depth(root)
    return max_diam[0]

# ================================================================
# 162. BALANCED BINARY TREE (Easy)
# ================================================================
def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    INTERVIEW SCRIPT:
    "Check balance while computing height.
     Return -1 to signal 'unbalanced' upward.
     Balanced: |left_h - right_h| <= 1 at every node."
    """
    def check(node):
        if not node: return 0
        left = check(node.left); right = check(node.right)
        if left == -1 or right == -1 or abs(left-right) > 1: return -1
        return 1 + max(left, right)
    return check(root) != -1

# ================================================================
# 163. PATH SUM (Easy)
# ================================================================
def has_path_sum(root: Optional[TreeNode], targetSum: int) -> bool:
    """
    INTERVIEW SCRIPT:
    "Leaf node: check if remaining == leaf.val.
     Recurse: subtract current val from target going down."
    """
    if not root: return False
    if not root.left and not root.right: return root.val == targetSum
    return (has_path_sum(root.left, targetSum-root.val) or
            has_path_sum(root.right, targetSum-root.val))

# ================================================================
# 164. PATH SUM II (Medium)
# ================================================================
def path_sum_ii(root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "DFS with backtracking. Add node to path.
     At leaf: check sum. Add to result if matches.
     Backtrack: remove node from path after recursion."
    """
    result = []
    def dfs(node, remaining, path):
        if not node: return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            result.append(list(path))
        else:
            dfs(node.left, remaining-node.val, path)
            dfs(node.right, remaining-node.val, path)
        path.pop()  # backtrack
    dfs(root, targetSum, [])
    return result

# ================================================================
# 165. CONSTRUCT BINARY TREE FROM PREORDER AND INORDER (Medium)
# ================================================================
def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    INTERVIEW SCRIPT:
    "Preorder first element = root. Find root in inorder.
     Elements left of root in inorder = left subtree.
     Elements right of root in inorder = right subtree.
     Recurse. Use hash map for O(1) inorder lookups."
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = [0]
    def build(in_left, in_right):
        if in_left > in_right: return None
        root_val = preorder[pre_idx[0]]; pre_idx[0] += 1
        root = TreeNode(root_val)
        mid = inorder_map[root_val]
        root.left = build(in_left, mid-1)
        root.right = build(mid+1, in_right)
        return root
    return build(0, len(inorder)-1)

# ================================================================
# 166. SERIALIZE AND DESERIALIZE BINARY TREE (Hard)
# ================================================================
class Codec:
    """
    INTERVIEW SCRIPT:
    "Serialize: preorder DFS, use 'null' for None nodes.
     Deserialize: parse string, build tree using same preorder DFS.
     Iterator over values makes it clean."
    """
    def serialize(self, root: Optional[TreeNode]) -> str:
        if not root: return "null"
        return f"{root.val},{self.serialize(root.left)},{self.serialize(root.right)}"

    def deserialize(self, data: str) -> Optional[TreeNode]:
        vals = iter(data.split(','))
        def build():
            val = next(vals)
            if val == 'null': return None
            node = TreeNode(int(val))
            node.left = build(); node.right = build()
            return node
        return build()

# ================================================================
# 167. BINARY TREE MAXIMUM PATH SUM (Hard)
# ================================================================
def max_path_sum_brute(root: Optional[TreeNode]) -> int:
    """APPROACH 1: O(n²) — compute path sum for all pairs"""
    # Not practical to implement naively for interview

def max_path_sum(root: Optional[TreeNode]) -> int:
    """
    APPROACH 2: O(n) — DFS with global max

    INTERVIEW SCRIPT:
    "For each node, max path through it = node.val + max(0,left) + max(0,right).
     But returning to parent: can only extend ONE direction.
     Return: node.val + max(0, max(left, right)).
     Update global max with both-direction path at each node."
    """
    max_sum = [float('-inf')]
    def gain(node):
        if not node: return 0
        left_gain = max(gain(node.left), 0)   # ignore if negative
        right_gain = max(gain(node.right), 0)
        max_sum[0] = max(max_sum[0], node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)  # one direction only
    gain(root)
    return max_sum[0]

# ================================================================
# 168-180: MORE TREE PROBLEMS
# ================================================================

def count_good_nodes(root: TreeNode) -> int:
    """
    1448. Count Good Nodes — node where max on path ≤ node.val
    """
    def dfs(node, max_so_far):
        if not node: return 0
        count = 1 if node.val >= max_so_far else 0
        max_so_far = max(max_so_far, node.val)
        return count + dfs(node.left, max_so_far) + dfs(node.right, max_so_far)
    return dfs(root, float('-inf'))

def sum_numbers(root: Optional[TreeNode]) -> int:
    """129. Sum Root to Leaf Numbers"""
    def dfs(node, curr):
        if not node: return 0
        curr = curr*10 + node.val
        if not node.left and not node.right: return curr
        return dfs(node.left, curr) + dfs(node.right, curr)
    return dfs(root, 0)

def zigzag_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """103. Binary Tree Zigzag Level Order Traversal"""
    if not root: return []
    result, queue, left_to_right = [], deque([root]), True
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level if left_to_right else level[::-1])
        left_to_right = not left_to_right
    return result

def flatten_tree(root: Optional[TreeNode]) -> None:
    """114. Flatten Binary Tree to Linked List (in-place)"""
    def dfs(node):
        if not node: return None
        if not node.left and not node.right: return node
        left_tail = dfs(node.left)
        right_tail = dfs(node.right)
        if left_tail:
            left_tail.next = node.right
            node.right = node.left
            node.left = None
    dfs(root)

def sorted_array_to_bst(nums: List[int]) -> Optional[TreeNode]:
    """108. Convert Sorted Array to Binary Search Tree"""
    if not nums: return None
    mid = len(nums)//2
    root = TreeNode(nums[mid])
    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid+1:])
    return root

def min_depth(root: Optional[TreeNode]) -> int:
    """111. Minimum Depth of Binary Tree"""
    if not root: return 0
    if not root.left: return 1 + min_depth(root.right)
    if not root.right: return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))

def subtree_of_another(root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
    """572. Subtree of Another Tree"""
    if not root: return not subRoot
    if is_same_tree(root, subRoot): return True
    return subtree_of_another(root.left, subRoot) or subtree_of_another(root.right, subRoot)

def recover_bst(root: Optional[TreeNode]) -> None:
    """
    99. Recover BST — exactly two nodes are swapped

    INTERVIEW SCRIPT:
    "Inorder of valid BST is sorted. Find two violations.
     First violation: prev > curr → first = prev.
     Second violation: prev > curr → second = curr.
     Swap values of first and second nodes."
    """
    first = second = prev = None
    def inorder(node):
        nonlocal first, second, prev
        if not node: return
        inorder(node.left)
        if prev and prev.val > node.val:
            if not first: first = prev
            second = node
        prev = node
        inorder(node.right)
    inorder(root)
    first.val, second.val = second.val, first.val

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    root = build([3,9,20,None,None,15,7])
    print("Max Depth:", max_depth(root))
    print("Level Order:", level_order(root))
    print("Right View:", right_side_view(root))
    print("Is Symmetric [1,2,2,3,4,4,3]:", is_symmetric(build([1,2,2,3,4,4,3])))
    print("Is Valid BST [5,1,4,null,null,3,6]:", is_valid_bst(build([5,1,4,None,None,3,6])))
    print("Kth Smallest [3,1,4,null,2] k=1:", kth_smallest(build([3,1,4,None,2]), 1))
    print("Diameter [1,2,3,4,5]:", diameter_of_binary_tree(build([1,2,3,4,5])))
    print("Max Path Sum [-10,9,20,null,null,15,7]:", max_path_sum(build([-10,9,20,None,None,15,7])))

    # Codec
    codec = Codec()
    serialized = codec.serialize(root)
    print("Serialized:", serialized)
    deserialized = codec.deserialize(serialized)
    print("Deserialized depth:", max_depth(deserialized))
