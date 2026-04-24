"""
================================================================
TOPIC 12: GRAPHS — VERY IMPORTANT
================================================================
Representation: Adjacency List (preferred) or Matrix
Directed vs Undirected, Weighted vs Unweighted

Algorithms: BFS, DFS, Cycle Detection, Topological Sort,
            Dijkstra, Bellman-Ford, Union-Find

INTERVIEW COMMUNICATION:
"I'll represent the graph as an adjacency list.
 BFS for shortest path in unweighted graphs.
 DFS for connectivity, cycle detection, topological sort.
 Dijkstra for weighted shortest path with non-negative weights."
================================================================
"""

from typing import List, Dict, Optional, Tuple
from collections import defaultdict, deque
import heapq

# ================================================================
# GRAPH REPRESENTATION
# ================================================================

def build_adjacency_list(n: int, edges: List[List[int]], directed=False) -> Dict:
    """Build adjacency list — O(V + E) space"""
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph

def build_adjacency_matrix(n: int, edges: List[List[int]], directed=False) -> List[List[int]]:
    """Build adjacency matrix — O(V²) space"""
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = 1
        if not directed:
            matrix[v][u] = 1
    return matrix

# ================================================================
# BFS — Breadth First Search
# ================================================================

def bfs(graph: Dict, start: int) -> List[int]:
    """
    BFS traversal — O(V + E)
    USE: shortest path (unweighted), level-order exploration

    INTERVIEW SCRIPT:
    "BFS explores nodes level by level using a queue.
     Mark nodes visited when ENQUEUING (not dequeuing) to avoid duplicates.
     Guarantees shortest path in unweighted graphs."
    """
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

def bfs_shortest_path(graph: Dict, start: int, end: int) -> int:
    """
    Shortest path (unweighted) using BFS — O(V + E)

    INTERVIEW SCRIPT:
    "BFS level by level: distance from start increases by 1 each level.
     When we reach end: current level = shortest path length."
    """
    if start == end:
        return 0
    visited = {start}
    queue = deque([(start, 0)])

    while queue:
        node, dist = queue.popleft()
        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1  # not reachable

# ================================================================
# DFS — Depth First Search
# ================================================================

def dfs_recursive(graph: Dict, node: int, visited: set = None) -> List[int]:
    """
    Recursive DFS — O(V + E)
    USE: connectivity, cycle detection, topological sort

    INTERVIEW SCRIPT:
    "DFS goes as deep as possible before backtracking.
     Uses call stack (recursive) or explicit stack (iterative)."
    """
    if visited is None:
        visited = set()
    visited.add(node)
    order = [node]
    for neighbor in graph[node]:
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))
    return order

def dfs_iterative(graph: Dict, start: int) -> List[int]:
    """Iterative DFS using explicit stack"""
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
    return order

# ================================================================
# NUMBER OF ISLANDS
# ================================================================

def num_islands(grid: List[List[str]]) -> int:
    """
    Count islands in binary grid.
    O(m * n) — visit each cell once

    APPROACH 1: DFS flood fill
    APPROACH 2: BFS flood fill
    APPROACH 3: Union-Find

    INTERVIEW SCRIPT:
    "For each unvisited land cell ('1'), start BFS/DFS to mark
     the entire island as visited.
     Each time we start a new BFS/DFS: increment island count."
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '#'  # mark visited
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count

# ================================================================
# CYCLE DETECTION
# ================================================================

def has_cycle_undirected(graph: Dict, n: int) -> bool:
    """
    Detect cycle in undirected graph — O(V + E)

    INTERVIEW SCRIPT:
    "DFS: if we visit an already-visited node that isn't the parent,
     it's a back edge → cycle exists.
     Pass parent to avoid false cycle with direct parent."
    """
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for node in range(n):
        if node not in visited:
            if dfs(node, -1):
                return True
    return False

def has_cycle_directed(graph: Dict, n: int) -> bool:
    """
    Detect cycle in directed graph — O(V + E)

    INTERVIEW SCRIPT:
    "Need to track nodes in current DFS path (rec_stack).
     If we visit a node already in current path: cycle!
     Unlike undirected: just being visited before ≠ cycle.
     Colors: WHITE=unvisited, GRAY=in-progress, BLACK=done.
     Cycle exists if we see a GRAY node."
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in range(n)}

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # back edge → cycle
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
        color[node] = BLACK
        return False

    for node in range(n):
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False

# ================================================================
# TOPOLOGICAL SORT
# ================================================================

def topological_sort_dfs(graph: Dict, n: int) -> List[int]:
    """
    Topological ordering of a DAG — O(V + E)
    POST-ORDER DFS: add node AFTER all its dependencies are processed

    INTERVIEW SCRIPT:
    "Valid for DAGs (Directed Acyclic Graphs).
     DFS: push node to stack AFTER visiting all its neighbors.
     Reverse the stack at the end.
     If cycle exists, topological sort is impossible."
    """
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)

    for node in range(n):
        if node not in visited:
            dfs(node)
    return stack[::-1]

def topological_sort_kahn(graph: Dict, n: int) -> List[int]:
    """
    Kahn's algorithm (BFS-based) — O(V + E)
    Also detects cycles (if result length < n, cycle exists)

    INTERVIEW SCRIPT:
    "Build in-degree array. Add all zero in-degree nodes to queue.
     BFS: process each node, decrement neighbors' in-degree.
     If neighbor's in-degree becomes 0: add to queue.
     Result length < n → cycle exists."

    USE CASE: Course scheduling, build systems, dependency resolution
    """
    in_degree = [0] * n
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == n else []  # empty if cycle

# ================================================================
# DIJKSTRA'S ALGORITHM
# ================================================================

def dijkstra(graph: Dict, start: int, n: int) -> List[int]:
    """
    Shortest path from start to all nodes (non-negative weights).
    O((V + E) log V) with min-heap

    INTERVIEW SCRIPT:
    "Greedy algorithm using a min-heap (priority queue).
     Always process the node with smallest known distance.
     Relax edges: if dist[u] + w < dist[v], update dist[v].
     Works only with non-negative edge weights.
     For negative weights: use Bellman-Ford."

    graph format: {node: [(neighbor, weight), ...]}
    """
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]  # (distance, node)

    while heap:
        curr_dist, u = heapq.heappop(heap)
        if curr_dist > dist[u]:
            continue  # stale entry
        for v, weight in graph[u]:
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return dist

def cheapest_flights(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    Cheapest flight with at most k stops — modified Dijkstra/Bellman-Ford
    O(k * E log V)

    INTERVIEW SCRIPT:
    "Modified Dijkstra: state is (cost, node, stops).
     Constraint: at most k stops.
     Use (cost, stops, node) in heap.
     Visited check: node + stops remaining."
    """
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    heap = [(0, src, 0)]  # (cost, node, stops)
    visited = {}

    while heap:
        cost, node, stops = heapq.heappop(heap)
        if node == dst:
            return cost
        if stops > k:
            continue
        if (node, stops) in visited:
            continue
        visited[(node, stops)] = cost

        for neighbor, price in graph[node]:
            heapq.heappush(heap, (cost + price, neighbor, stops + 1))

    return -1

# ================================================================
# BELLMAN-FORD
# ================================================================

def bellman_ford(n: int, edges: List[List[int]], start: int) -> List[int]:
    """
    Shortest path with NEGATIVE weights (but no negative cycles).
    O(V * E)

    INTERVIEW SCRIPT:
    "Relax all edges V-1 times.
     After V-1 iterations: all shortest paths found.
     V-th iteration: if any distance still decreases → negative cycle."
    """
    dist = [float('inf')] * n
    dist[start] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Check for negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return []  # negative cycle exists

    return dist

# ================================================================
# UNION-FIND (DISJOINT SET UNION)
# ================================================================

class UnionFind:
    """
    Efficiently group nodes into connected components.
    Nearly O(1) amortized with path compression + union by rank.

    INTERVIEW SCRIPT:
    "Union-Find maintains disjoint sets.
     find(x): returns root of x's set (with path compression).
     union(x, y): merge x's and y's sets (by rank).
     Path compression flattens tree → near O(1) amortized."

    USE CASE: Detecting cycles, Kruskal's MST, social networks clustering
    """
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

def number_of_islands_uf(grid: List[List[str]]) -> int:
    """Number of islands using Union-Find"""
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)
    count = sum(grid[r][c] == '1' for r in range(rows) for c in range(cols))

    def idx(r, c):
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                        if uf.union(idx(r, c), idx(nr, nc)):
                            count -= 1
    return count

# ================================================================
# WORD LADDER
# ================================================================

def word_ladder(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    Shortest transformation sequence.
    O(n * m²) where n = wordList size, m = word length

    INTERVIEW SCRIPT:
    "Model as graph: nodes are words, edges between words differing by 1 char.
     BFS gives shortest transformation path.
     Optimization: use intermediate states (ho*se) to group words."
    """
    word_set = set(wordList)
    if endWord not in word_set:
        return 0

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word == endWord:
                    return length + 1
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))
    return 0

# ================================================================
# PACIFIC ATLANTIC WATER FLOW
# ================================================================

def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    """
    Find cells from which water can flow to both oceans.
    O(m * n) — reverse BFS from both oceans

    INTERVIEW SCRIPT:
    "Reverse the problem: instead of water flowing down,
     flow UP from each ocean boundary.
     BFS/DFS from Pacific borders → cells reachable from Pacific.
     BFS/DFS from Atlantic borders → cells reachable from Atlantic.
     Answer = intersection of both sets."
    """
    rows, cols = len(heights), len(heights[0])

    def bfs(starts):
        visited = set(starts)
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    (nr, nc) not in visited and
                    heights[nr][nc] >= heights[r][c]):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return visited

    pacific = [(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)]
    atlantic = [(rows-1, c) for c in range(cols)] + [(r, cols-1) for r in range(rows)]

    pac_reach = bfs(pacific)
    atl_reach = bfs(atlantic)

    return [[r, c] for r, c in pac_reach & atl_reach]

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Graphs model relationships everywhere:
- Social networks (friendship graphs)
- Maps/Navigation (weighted graphs with Dijkstra)
- Network topology (connectivity)
- Dependency resolution (topological sort in build systems, npm)
- Web crawling (BFS from a start URL)
- Recommendation systems (bipartite graphs)
- Fraud detection (cycle detection)
"""

if __name__ == "__main__":
    # Build a simple graph
    edges = [[0,1],[0,2],[1,3],[2,3],[3,4]]
    graph = build_adjacency_list(5, edges)

    print("BFS from 0:", bfs(graph, 0))
    print("DFS from 0:", dfs_recursive(graph, 0))
    print("Shortest path 0→4:", bfs_shortest_path(graph, 0, 4))

    # Islands
    grid = [["1","1","0","0","0"],
            ["1","1","0","0","0"],
            ["0","0","1","0","0"],
            ["0","0","0","1","1"]]
    print("Number of islands:", num_islands([row[:] for row in grid]))

    # Dijkstra
    weighted_graph = {0: [(1,4),(2,1)], 1: [(3,1)], 2: [(1,2),(3,5)], 3: []}
    print("Dijkstra from 0:", dijkstra(weighted_graph, 0, 4))

    # Union Find
    uf = UnionFind(5)
    uf.union(0, 1); uf.union(1, 2)
    print("0 and 2 connected:", uf.connected(0, 2))
    print("Components:", uf.components)
