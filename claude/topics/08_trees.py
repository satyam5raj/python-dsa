"""
================================================================
TOPIC 8: TREES — SUPER IMPORTANT
================================================================
Binary Tree, BST, Traversals, LCA, Height, Diameter

INTERVIEW COMMUNICATION:
"Trees are recursive by nature. I'll use DFS for path problems
 and BFS for level-order/shortest path. Most tree problems
 can be solved with a single recursive DFS."
================================================================
"""

from typing import Optional, List
from collections import deque

# ================================================================
# TREE NODE
# ================================================================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"

# Build tree from level-order array
def build_tree_levelorder(vals: List) -> Optional[TreeNode]:
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root

# ================================================================
# TREE TRAVERSALS
# ================================================================

def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """Left → Root → Right (gives BST in sorted order!)"""
    if not root:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)

def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """Root → Left → Right (useful for tree serialization)"""
    if not root:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)

def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
    """Left → Right → Root (useful for deletion, expression trees)"""
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.val]

def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Iterative inorder with explicit stack — O(n) time, O(h) space

    INTERVIEW SCRIPT:
    "Use a stack to simulate recursion.
     Go as far left as possible, pushing nodes.
     Pop, record, then go right."
    """
    result = []
    stack = []
    curr = root
    while curr or stack:
        while curr:         # go as far left as possible
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()  # process node
        result.append(curr.val)
        curr = curr.right   # go right
    return result

def level_order_bfs(root: Optional[TreeNode]) -> List[List[int]]:
    """
    BFS level-order traversal — O(n) time, O(n) space

    INTERVIEW SCRIPT:
    "Use a queue (deque). Process nodes level by level.
     Key: snapshot queue size at start of each level = nodes in that level.
     Process exactly that many nodes for each level."
    """
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):  # process one level
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result

# ================================================================
# TREE PROPERTIES
# ================================================================

def max_depth(root: Optional[TreeNode]) -> int:
    """
    Maximum depth (height) of binary tree.
    O(n) — visit every node

    INTERVIEW SCRIPT:
    "Depth = 1 + max(left_depth, right_depth).
     Base case: null node has depth 0.
     This is a classic post-order traversal."
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def min_depth(root: Optional[TreeNode]) -> int:
    """
    Minimum depth — be careful! Min != max, and null children don't count.
    """
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))

def diameter_of_tree(root: Optional[TreeNode]) -> int:
    """
    Diameter = longest path between any two nodes.
    The path doesn't have to go through root!
    O(n) — track diameter as we compute depths

    INTERVIEW SCRIPT:
    "For each node, diameter through it = left_depth + right_depth.
     Use a global max, update at each node.
     Return depth (not diameter) to parent."
    """
    self_diameter = [0]

    def depth(node):
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        self_diameter[0] = max(self_diameter[0], left + right)
        return 1 + max(left, right)

    depth(root)
    return self_diameter[0]

def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    Height-balanced: for every node, |left_height - right_height| <= 1
    O(n) — check while computing height

    INTERVIEW SCRIPT:
    "Check balance and height simultaneously.
     Return -1 to signal 'unbalanced' to parent.
     If any subtree is unbalanced, propagate -1 upward."
    """
    def check(node):
        if not node:
            return 0
        left = check(node.left)
        right = check(node.right)
        if left == -1 or right == -1:
            return -1
        if abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return check(root) != -1

def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """
    O(n) — compare every node

    INTERVIEW SCRIPT:
    "Two trees are same if: both null (base case),
     or both have same value AND left subtrees same AND right subtrees same."
    """
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)

def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    Mirror symmetric tree check — O(n)

    INTERVIEW SCRIPT:
    "Check if left and right subtrees are mirror images.
     Helper: is_mirror(left, right) checks if trees are mirrors:
     - Both null: true
     - One null: false
     - Values equal AND left.left mirrors right.right AND left.right mirrors right.left"
    """
    def is_mirror(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and
                is_mirror(left.left, right.right) and
                is_mirror(left.right, right.left))
    return is_mirror(root.left, root.right) if root else True

def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Invert (mirror) binary tree — O(n)

    INTERVIEW SCRIPT:
    "Recursively swap left and right children.
     Base case: null node."
    """
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

# ================================================================
# LOWEST COMMON ANCESTOR (LCA)
# ================================================================

def lca_binary_tree(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    LCA in binary tree (not BST) — O(n)

    INTERVIEW SCRIPT:
    "If root is null, return null.
     If root is p or q, return root (found one of them).
     Recurse on both sides.
     If both sides return non-null: root is the LCA.
     If only one side: LCA is in that side."
    """
    if not root or root == p or root == q:
        return root

    left = lca_binary_tree(root.left, p, q)
    right = lca_binary_tree(root.right, p, q)

    if left and right:
        return root  # p is in one subtree, q in other
    return left or right  # both in same subtree

def lca_bst(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    LCA in BST — O(h) time, exploits BST property

    INTERVIEW SCRIPT:
    "BST property: left < root < right.
     If both p, q < root: LCA is in left subtree.
     If both p, q > root: LCA is in right subtree.
     Otherwise: root is the LCA (split point)."
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root

# ================================================================
# BST OPERATIONS
# ================================================================

def validate_bst(root: Optional[TreeNode]) -> bool:
    """
    Validate BST property — O(n)
    WRONG APPROACH: just check left.val < root.val < right.val
    CORRECT: pass valid range [min, max] down

    INTERVIEW SCRIPT:
    "Each node must be within a valid range.
     Root: (-inf, +inf).
     Left child: (-inf, parent.val).
     Right child: (parent.val, +inf).
     These constraints propagate down."
    """
    def is_valid(node, min_val, max_val):
        if not node:
            return True
        if node.val <= min_val or node.val >= max_val:
            return False
        return (is_valid(node.left, min_val, node.val) and
                is_valid(node.right, node.val, max_val))

    return is_valid(root, float('-inf'), float('inf'))

def kth_smallest_bst(root: Optional[TreeNode], k: int) -> int:
    """
    Kth smallest in BST using inorder traversal — O(h + k)

    INTERVIEW SCRIPT:
    "Inorder traversal of BST gives elements in sorted order.
     The kth element in inorder is the kth smallest."
    """
    count = [0]
    result = [None]

    def inorder(node):
        if not node or result[0] is not None:
            return
        inorder(node.left)
        count[0] += 1
        if count[0] == k:
            result[0] = node.val
            return
        inorder(node.right)

    inorder(root)
    return result[0]

# ================================================================
# PATH SUM PROBLEMS
# ================================================================

def has_path_sum(root: Optional[TreeNode], target: int) -> bool:
    """Does any root-to-leaf path sum to target? O(n)"""
    if not root:
        return False
    if not root.left and not root.right:  # leaf
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))

def path_sum_all(root: Optional[TreeNode], target: int) -> List[List[int]]:
    """Find ALL root-to-leaf paths summing to target — O(n²) worst"""
    result = []

    def dfs(node, remaining, path):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            result.append(list(path))
        else:
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        path.pop()  # backtrack

    dfs(root, target, [])
    return result

def max_path_sum(root: Optional[TreeNode]) -> int:
    """
    Maximum path sum (path can start/end anywhere) — O(n)

    INTERVIEW SCRIPT:
    "Path = sequence of nodes. Can go left-root-right through any node.
     For each node: gain from left (if positive), gain from right (if positive).
     Update global max with left + root + right.
     Return to parent: root + max(left, right) [can't go both directions when going up]."
    """
    max_sum = [float('-inf')]

    def gain(node):
        if not node:
            return 0
        left_gain = max(gain(node.left), 0)   # 0 if negative
        right_gain = max(gain(node.right), 0)  # 0 if negative
        max_sum[0] = max(max_sum[0], node.val + left_gain + right_gain)
        return node.val + max(left_gain, right_gain)  # return one direction

    gain(root)
    return max_sum[0]

# ================================================================
# TREE CONSTRUCTION
# ================================================================

def build_from_preorder_inorder(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Construct binary tree from preorder + inorder traversals.
    O(n²) naive, O(n) with hash map

    INTERVIEW SCRIPT:
    "Preorder: first element is always root.
     Inorder: root divides left and right subtrees.
     Find root in inorder, split left/right, recurse.
     Use hash map for O(1) inorder index lookup."
    """
    if not preorder or not inorder:
        return None

    inorder_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = [0]

    def build(in_left, in_right):
        if in_left > in_right:
            return None
        root_val = preorder[pre_idx[0]]
        pre_idx[0] += 1
        root = TreeNode(root_val)
        idx = inorder_map[root_val]
        root.left = build(in_left, idx - 1)
        root.right = build(idx + 1, in_right)
        return root

    return build(0, len(inorder) - 1)

def sorted_array_to_bst(nums: List[int]) -> Optional[TreeNode]:
    """Convert sorted array to height-balanced BST — O(n)"""
    if not nums:
        return None
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid+1:])
    return root

# ================================================================
# SERIALIZE / DESERIALIZE
# ================================================================

def serialize(root: Optional[TreeNode]) -> str:
    """Preorder serialization with null markers"""
    if not root:
        return "null"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data: str) -> Optional[TreeNode]:
    """Reconstruct tree from serialized string"""
    vals = iter(data.split(','))

    def build():
        val = next(vals)
        if val == 'null':
            return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node

    return build()

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Trees are everywhere:
- File systems (directory trees)
- HTML/XML DOM (document tree)
- Databases (B-trees, B+ trees for indexing)
- Compilers (abstract syntax trees)
- Network routing (spanning trees)
- AI decision making (decision trees)
- Autocomplete (tries — a type of tree)
"""

if __name__ == "__main__":
    # Build tree: [3,9,20,null,null,15,7]
    root = build_tree_levelorder([3, 9, 20, None, None, 15, 7])

    print("Inorder:", inorder_recursive(root))
    print("Level order:", level_order_bfs(root))
    print("Max depth:", max_depth(root))
    print("Is balanced:", is_balanced(root))
    print("Is symmetric:", is_symmetric(build_tree_levelorder([1,2,2,3,4,4,3])))

    # Max path sum
    root2 = build_tree_levelorder([-10, 9, 20, None, None, 15, 7])
    print("Max path sum:", max_path_sum(root2))  # 42

    # Serialize/Deserialize
    serialized = serialize(root)
    print("Serialized:", serialized)
    deserialized = deserialize(serialized)
    print("Deserialized inorder:", inorder_recursive(deserialized))
