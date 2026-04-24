"""
================================================================
LEETCODE PHASE 3 (Problems 201-240): GRAPHS
================================================================
"""

from typing import List, Optional, Dict
from collections import defaultdict, deque
import heapq

# ================================================================
# 201. NUMBER OF ISLANDS (Medium)
# ================================================================
def num_islands_bfs(grid: List[List[str]]) -> int:
    """
    APPROACH 1: BFS — O(m*n) time and space

    INTERVIEW SCRIPT:
    "Each '1' not yet visited starts a new island.
     BFS/DFS marks all connected land as visited.
     Count how many BFS/DFS starts = number of islands."
    """
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def bfs(r, c):
        q = deque([(r, c)])
        visited.add((r, c))
        while q:
            row, col = q.popleft()
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = row+dr, col+dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1' and (nr,nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r,c) not in visited:
                bfs(r, c)
                count += 1
    return count

def num_islands_dfs(grid: List[List[str]]) -> int:
    """APPROACH 2: DFS in-place (modify grid) — O(m*n) time, O(m*n) recursion space"""
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1': return
        grid[r][c] = '0'  # mark visited
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            dfs(r+dr, c+dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count

# ================================================================
# 202. CLONE GRAPH (Medium)
# ================================================================
class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

def clone_graph(node: Optional[GraphNode]) -> Optional[GraphNode]:
    """
    INTERVIEW SCRIPT:
    "Use hashmap: original node → cloned node.
     BFS/DFS: for each node, clone it (if not cloned).
     For each neighbor: clone if not done, connect to clone.
     O(V+E) time and space."
    """
    if not node: return None
    cloned = {}

    def dfs(n):
        if n in cloned: return cloned[n]
        copy = GraphNode(n.val)
        cloned[n] = copy
        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)

# ================================================================
# 203. COURSE SCHEDULE I (Medium)
# ================================================================
def can_finish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    APPROACH 1: DFS cycle detection — O(V+E)

    INTERVIEW SCRIPT:
    "Model as directed graph. Course a → b means must take b before a.
     Cycle in graph = impossible to finish.
     DFS with 3 states: 0=unvisited, 1=visiting(in stack), 2=done.
     If we visit a node currently in stack → cycle detected."
    """
    graph = defaultdict(list)
    for a, b in prerequisites: graph[a].append(b)
    state = [0] * numCourses  # 0=unvisited, 1=visiting, 2=done

    def dfs(node):
        if state[node] == 1: return False  # cycle
        if state[node] == 2: return True   # already processed
        state[node] = 1
        for nei in graph[node]:
            if not dfs(nei): return False
        state[node] = 2
        return True

    return all(dfs(i) for i in range(numCourses))

def can_finish_topo(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """APPROACH 2: Kahn's BFS topological sort — O(V+E)"""
    indegree = [0] * numCourses
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1

    q = deque(i for i in range(numCourses) if indegree[i] == 0)
    count = 0
    while q:
        node = q.popleft()
        count += 1
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0: q.append(nei)
    return count == numCourses

# ================================================================
# 204. COURSE SCHEDULE II (Medium)
# ================================================================
def find_order(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Same as Course Schedule I but return the actual order.
     Kahn's algorithm: process zero-indegree nodes first.
     BFS builds topological order naturally.
     If count != numCourses → cycle exists → return []."
    """
    indegree = [0] * numCourses
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1

    q = deque(i for i in range(numCourses) if indegree[i] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0: q.append(nei)
    return order if len(order) == numCourses else []

# ================================================================
# 205. PACIFIC ATLANTIC WATER FLOW (Medium)
# ================================================================
def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:
    """
    APPROACH 1: Brute force — O(m*n*(m*n)) — DFS from every cell

    APPROACH 2: Reverse BFS — O(m*n)

    INTERVIEW SCRIPT:
    "Key insight: instead of checking if water flows FROM cell to ocean,
     BFS/DFS FROM ocean inward. Water 'flows up' when going inland.
     Find cells reachable from Pacific AND Atlantic.
     Intersection = answer."
    """
    if not heights: return []
    rows, cols = len(heights), len(heights[0])

    def bfs(starts):
        visited = set(starts)
        q = deque(starts)
        while q:
            r, c = q.popleft()
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in visited and heights[nr][nc] >= heights[r][c]:
                    visited.add((nr, nc))
                    q.append((nr, nc))
        return visited

    pacific_starts = [(r,0) for r in range(rows)] + [(0,c) for c in range(1,cols)]
    atlantic_starts = [(r,cols-1) for r in range(rows)] + [(rows-1,c) for c in range(cols-1)]

    pacific = bfs(pacific_starts)
    atlantic = bfs(atlantic_starts)
    return [[r,c] for r,c in pacific & atlantic]

# ================================================================
# 206. SURROUNDED REGIONS (Medium)
# ================================================================
def solve_surrounded(board: List[List[str]]) -> None:
    """
    INTERVIEW SCRIPT:
    "Key insight: 'O's connected to border cannot be captured.
     BFS/DFS from all border 'O's to mark safe cells.
     Flip all unmarked 'O's to 'X', restore marked ones to 'O'."
    """
    if not board: return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O': return
        board[r][c] = 'S'  # safe
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            dfs(r+dr, c+dc)

    for r in range(rows):
        for c in range(cols):
            if (r in [0, rows-1] or c in [0, cols-1]) and board[r][c] == 'O':
                dfs(r, c)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O': board[r][c] = 'X'
            elif board[r][c] == 'S': board[r][c] = 'O'

# ================================================================
# 207. ROTTING ORANGES (Medium)
# ================================================================
def oranges_rotting(grid: List[List[int]]) -> int:
    """
    INTERVIEW SCRIPT:
    "Multi-source BFS: start from ALL rotten oranges simultaneously.
     Each BFS level = 1 minute.
     Track fresh count. If fresh > 0 after BFS → return -1."
    """
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2: q.append((r, c, 0))
            elif grid[r][c] == 1: fresh += 1

    minutes = 0
    while q:
        r, c, t = q.popleft()
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                minutes = t + 1
                q.append((nr, nc, t+1))
    return minutes if fresh == 0 else -1

# ================================================================
# 208. WORD LADDER (Hard)
# ================================================================
def ladder_length(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    APPROACH 1: BFS — O(n * m²) where n=wordList length, m=word length

    INTERVIEW SCRIPT:
    "BFS from beginWord. For each word: try all single-char changes.
     If result in wordList and not visited: add to queue.
     Return level when we reach endWord.
     Optimization: use set for O(1) lookup."
    """
    word_set = set(wordList)
    if endWord not in word_set: return 0
    q = deque([(beginWord, 1)])
    visited = {beginWord}

    while q:
        word, length = q.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word == endWord: return length + 1
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    q.append((new_word, length+1))
    return 0

def ladder_length_bidirectional(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    APPROACH 2: Bidirectional BFS — O(b^(d/2)) vs O(b^d) — much faster

    INTERVIEW SCRIPT:
    "Search from both ends simultaneously.
     When frontiers meet → found shortest path.
     At each step: expand the smaller frontier.
     Dramatically reduces search space."
    """
    word_set = set(wordList)
    if endWord not in word_set: return 0
    front, back = {beginWord}, {endWord}
    visited = {beginWord, endWord}
    length = 1

    while front:
        if len(front) > len(back): front, back = back, front
        next_front = set()
        for word in front:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in back: return length + 1
                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        next_front.add(new_word)
        front = next_front
        length += 1
    return 0

# ================================================================
# 209. NETWORK DELAY TIME (Medium)
# ================================================================
def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    INTERVIEW SCRIPT:
    "Dijkstra from source k. Find shortest path to all nodes.
     Answer = max of all shortest paths (time for signal to reach all).
     If any node unreachable → return -1.
     O((V+E) log V) with min-heap."
    """
    graph = defaultdict(list)
    for u, v, w in times: graph[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n+1)}
    dist[k] = 0
    heap = [(0, k)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1

# ================================================================
# 210. CHEAPEST FLIGHTS K STOPS (Medium)
# ================================================================
def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    APPROACH 1: Bellman-Ford with k+1 rounds — O(k*E)

    INTERVIEW SCRIPT:
    "Bellman-Ford: relax all edges k+1 times (k stops = k+1 edges).
     Use copy of prices to avoid using same edge twice in one round.
     O(k*E) time. Alternative: Dijkstra with (cost, node, stops)."
    """
    prices = [float('inf')] * n
    prices[src] = 0

    for _ in range(k+1):
        temp = prices[:]
        for u, v, w in flights:
            if prices[u] != float('inf') and prices[u] + w < temp[v]:
                temp[v] = prices[u] + w
        prices = temp

    return prices[dst] if prices[dst] != float('inf') else -1

def find_cheapest_price_dijkstra(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """APPROACH 2: Dijkstra with stop count — O(E log V)"""
    graph = defaultdict(list)
    for u, v, w in flights: graph[u].append((v, w))

    heap = [(0, src, 0)]  # (cost, node, stops)
    visited = {}  # (node, stops) → min_cost

    while heap:
        cost, node, stops = heapq.heappop(heap)
        if node == dst: return cost
        if stops > k: continue
        if (node, stops) in visited: continue
        visited[(node, stops)] = cost
        for nei, w in graph[node]:
            if (nei, stops+1) not in visited:
                heapq.heappush(heap, (cost+w, nei, stops+1))
    return -1

# ================================================================
# 211. REDUNDANT CONNECTION (Medium)
# ================================================================
def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Union-Find: process edges one by one.
     If two nodes already connected (same component) → edge is redundant.
     Return that edge.
     O(n * α(n)) ≈ O(n) with path compression + union by rank."
    """
    parent = list(range(len(edges)+1))
    rank = [0] * (len(edges)+1)

    def find(x):
        if parent[x] != x: parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return False
        if rank[px] < rank[py]: px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]: rank[px] += 1
        return True

    for u, v in edges:
        if not union(u, v): return [u, v]
    return []

# ================================================================
# 212. GRAPH VALID TREE (Medium)
# ================================================================
def valid_tree(n: int, edges: List[List[int]]) -> bool:
    """
    INTERVIEW SCRIPT:
    "Valid tree: n-1 edges AND all nodes connected (no cycles).
     Union-Find: process all edges.
     If cycle found → not a tree. If not fully connected → not a tree."
    """
    if len(edges) != n-1: return False
    parent = list(range(n))

    def find(x):
        if parent[x] != x: parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return False
        parent[px] = py
        return True

    return all(union(u, v) for u, v in edges)

# ================================================================
# 213. NUMBER OF CONNECTED COMPONENTS (Medium)
# ================================================================
def count_components(n: int, edges: List[List[int]]) -> int:
    """
    INTERVIEW SCRIPT:
    "Union-Find: start with n components.
     Each successful union reduces count by 1.
     Return final count."
    """
    parent = list(range(n))
    count = n

    def find(x):
        if parent[x] != x: parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal count
        px, py = find(x), find(y)
        if px == py: return
        parent[px] = py
        count -= 1

    for u, v in edges: union(u, v)
    return count

# ================================================================
# 214. ALIEN DICTIONARY (Hard)
# ================================================================
def alien_order(words: List[str]) -> str:
    """
    INTERVIEW SCRIPT:
    "Build graph from adjacent word comparisons.
     Compare word[i] and word[i+1]: first differing char gives order.
     Edge case: if word2 is prefix of word1 → invalid.
     Topological sort (DFS) gives the order.
     O(C) where C = total characters."
    """
    adj = {c: set() for w in words for c in w}

    for i in range(len(words)-1):
        w1, w2 = words[i], words[i+1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]: return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                adj[w1[j]].add(w2[j])
                break

    visited = {}  # False=visited, True=in current path
    result = []

    def dfs(c):
        if c in visited: return visited[c]
        visited[c] = True
        for nei in adj[c]:
            if dfs(nei): return True
        visited[c] = False
        result.append(c)
        return False

    for c in adj:
        if dfs(c): return ""
    return ''.join(reversed(result))

# ================================================================
# 215. RECONSTRUCT ITINERARY (Hard)
# ================================================================
def find_itinerary(tickets: List[List[str]]) -> List[str]:
    """
    INTERVIEW SCRIPT:
    "Hierholzer's algorithm: find Eulerian path.
     Sort destinations to get lexicographically smallest.
     DFS: greedily take first destination. When stuck, backtrack and add to result.
     Reverse result at end. O(E log E) for sorting."
    """
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):
        graph[src].append(dst)

    result = []
    def dfs(airport):
        while graph[airport]:
            dfs(graph[airport].pop())
        result.append(airport)

    dfs('JFK')
    return result[::-1]

# ================================================================
# 216. MIN COST TO CONNECT ALL POINTS (Medium)
# ================================================================
def min_cost_connect_points(points: List[List[int]]) -> int:
    """
    APPROACH 1: Prim's algorithm — O(n²)

    INTERVIEW SCRIPT:
    "Minimum Spanning Tree problem. Manhattan distance = edge weight.
     Prim's: start from any node. Always add cheapest edge to unvisited node.
     O(n²) for dense graphs (all n² edges). Better than Kruskal's here."
    """
    n = len(points)
    visited = [False] * n
    min_dist = [float('inf')] * n
    min_dist[0] = 0
    total = 0

    for _ in range(n):
        # Pick unvisited node with min distance
        u = min((i for i in range(n) if not visited[i]), key=lambda i: min_dist[i])
        visited[u] = True
        total += min_dist[u]
        # Update distances
        for v in range(n):
            if not visited[v]:
                d = abs(points[u][0]-points[v][0]) + abs(points[u][1]-points[v][1])
                min_dist[v] = min(min_dist[v], d)

    return total

# ================================================================
# 217. CRITICAL CONNECTIONS (Hard)
# ================================================================
def critical_connections(n: int, connections: List[List[int]]) -> List[List[int]]:
    """
    INTERVIEW SCRIPT:
    "Tarjan's bridge-finding algorithm.
     DFS: assign discovery time and low value to each node.
     low[v] = min(disc[v], min(low[neighbors])).
     Edge (u,v) is bridge if low[v] > disc[u]: v can't reach u without this edge."
    """
    graph = defaultdict(list)
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n
    low = [0] * n
    result = []
    timer = [0]

    def dfs(node, parent):
        disc[node] = low[node] = timer[0]
        timer[0] += 1
        for nei in graph[node]:
            if nei == parent: continue
            if disc[nei] == -1:
                dfs(nei, node)
                low[node] = min(low[node], low[nei])
                if low[nei] > disc[node]:
                    result.append([node, nei])
            else:
                low[node] = min(low[node], disc[nei])

    dfs(0, -1)
    return result

# ================================================================
# 218. SHORTEST PATH IN BINARY MATRIX (Medium)
# ================================================================
def shortest_path_binary_matrix(grid: List[List[int]]) -> int:
    """
    INTERVIEW SCRIPT:
    "BFS in 8-directional grid. Start from (0,0) if 0.
     BFS guarantees shortest path.
     Each cell visited at most once. O(n²)."
    """
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1: return -1
    q = deque([(0, 0, 1)])
    grid[0][0] = 1  # mark visited
    dirs = [(dr,dc) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0)]

    while q:
        r, c, dist = q.popleft()
        if r == n-1 and c == n-1: return dist
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1
                q.append((nr, nc, dist+1))
    return -1

# ================================================================
# 219. PATH WITH MINIMUM EFFORT (Medium)
# ================================================================
def minimum_effort_path(heights: List[List[int]]) -> int:
    """
    INTERVIEW SCRIPT:
    "Modified Dijkstra: instead of minimizing sum, minimize max difference.
     dist[r][c] = min effort to reach (r,c).
     Heap: (effort, r, c). Effort = max diff along path.
     O(m*n * log(m*n))."
    """
    rows, cols = len(heights), len(heights[0])
    effort = [[float('inf')] * cols for _ in range(rows)]
    effort[0][0] = 0
    heap = [(0, 0, 0)]

    while heap:
        e, r, c = heapq.heappop(heap)
        if e > effort[r][c]: continue
        if r == rows-1 and c == cols-1: return e
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_e = max(e, abs(heights[nr][nc] - heights[r][c]))
                if new_e < effort[nr][nc]:
                    effort[nr][nc] = new_e
                    heapq.heappush(heap, (new_e, nr, nc))
    return 0

# ================================================================
# 220. EVALUATE DIVISION (Medium)
# ================================================================
def calc_equation(equations: List[List[str]], values: List[float],
                  queries: List[List[str]]) -> List[float]:
    """
    INTERVIEW SCRIPT:
    "Build weighted graph: a/b=k means edge a→b with weight k and b→a with 1/k.
     For each query: BFS/DFS to find path from src to dst.
     Multiply weights along path. If no path: return -1.0."
    """
    graph = defaultdict(dict)
    for (a, b), val in zip(equations, values):
        graph[a][b] = val
        graph[b][a] = 1.0 / val

    def bfs(src, dst):
        if src not in graph or dst not in graph: return -1.0
        if src == dst: return 1.0
        visited = set()
        q = deque([(src, 1.0)])
        while q:
            node, prod = q.popleft()
            if node == dst: return prod
            visited.add(node)
            for nei, w in graph[node].items():
                if nei not in visited:
                    q.append((nei, prod * w))
        return -1.0

    return [bfs(a, b) for a, b in queries]

# ================================================================
# 221. ACCOUNTS MERGE (Medium)
# ================================================================
def accounts_merge(accounts: List[List[str]]) -> List[List[str]]:
    """
    INTERVIEW SCRIPT:
    "Union-Find on emails. Each email maps to account owner.
     For each account: union all emails together (first email is root).
     Group emails by root. Prepend account name. Sort emails.
     O(n * α(n)) ≈ O(n)."
    """
    parent = {}
    email_to_name = {}

    def find(x):
        if parent.setdefault(x, x) != x: parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        parent[find(x)] = find(y)

    for account in accounts:
        name = account[0]
        for email in account[1:]:
            email_to_name[email] = name
            union(email, account[1])

    groups = defaultdict(list)
    for email in email_to_name:
        groups[find(email)].append(email)

    return [[email_to_name[root]] + sorted(emails) for root, emails in groups.items()]

# ================================================================
# 222. IS BIPARTITE (Medium)
# ================================================================
def is_bipartite(graph: List[List[int]]) -> bool:
    """
    INTERVIEW SCRIPT:
    "2-colorable check. BFS: try to color with 2 colors.
     If adjacent nodes have same color → not bipartite.
     Handle disconnected graphs: check all nodes.
     O(V+E)."
    """
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1: continue
        q = deque([start])
        color[start] = 0
        while q:
            node = q.popleft()
            for nei in graph[node]:
                if color[nei] == -1:
                    color[nei] = 1 - color[node]
                    q.append(nei)
                elif color[nei] == color[node]:
                    return False
    return True

# ================================================================
# 223. EVENTUAL SAFE STATES (Medium)
# ================================================================
def eventual_safe_nodes(graph: List[List[int]]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Safe node: eventually reaches a terminal or all cycles avoided.
     DFS with 3 states: 0=unvisited, 1=visiting, 2=safe.
     If DFS reaches cycle → not safe. If all paths lead to safe → safe.
     O(V+E)."
    """
    n = len(graph)
    state = [0] * n  # 0=unvisited, 1=visiting, 2=safe

    def dfs(node):
        if state[node] == 1: return False  # cycle
        if state[node] == 2: return True
        state[node] = 1
        for nei in graph[node]:
            if not dfs(nei): return False
        state[node] = 2
        return True

    return [i for i in range(n) if dfs(i)]

# ================================================================
# 224. MINIMUM HEIGHT TREES (Medium)
# ================================================================
def find_min_height_trees(n: int, edges: List[List[int]]) -> List[int]:
    """
    INTERVIEW SCRIPT:
    "Root of MHT = center of the tree (one or two nodes).
     Iteratively trim leaf nodes (degree 1) layer by layer.
     Like BFS from outside inward. Stop when ≤ 2 nodes remain.
     O(n) time."
    """
    if n == 1: return [0]
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    leaves = deque(node for node in range(n) if len(adj[node]) == 1)
    remaining = n

    while remaining > 2:
        remaining -= len(leaves)
        new_leaves = deque()
        for leaf in leaves:
            nei = adj[leaf].pop()
            adj[nei].remove(leaf)
            if len(adj[nei]) == 1: new_leaves.append(nei)
        leaves = new_leaves

    return list(leaves)

# ================================================================
# 225. DETECT CYCLE IN DIRECTED GRAPH (Medium)
# ================================================================
def has_cycle_directed(n: int, edges: List[List[int]]) -> bool:
    """
    INTERVIEW SCRIPT:
    "DFS with 3-color marking: WHITE/GRAY/BLACK.
     GRAY = currently in DFS stack. If we visit GRAY node → cycle.
     BLACK = fully processed. O(V+E)."
    """
    graph = defaultdict(list)
    for u, v in edges: graph[u].append(v)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(node):
        color[node] = GRAY
        for nei in graph[node]:
            if color[nei] == GRAY: return True
            if color[nei] == WHITE and dfs(nei): return True
        color[node] = BLACK
        return False

    return any(dfs(i) for i in range(n) if color[i] == WHITE)

# ================================================================
# 226-240: ADDITIONAL GRAPH PROBLEMS
# ================================================================

def word_ladder_ii(beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
    """
    126. Word Ladder II — all shortest transformation sequences (Hard)

    INTERVIEW SCRIPT:
    "BFS to find shortest distance. Then DFS backtrack to find all paths.
     Two-step: 1) BFS build distance map 2) DFS find all shortest paths.
     O(n * m² + paths) complexity."
    """
    word_set = set(wordList)
    if endWord not in word_set: return []

    layer = {beginWord}
    parents = defaultdict(set)
    found = False

    while layer and not found:
        word_set -= layer
        next_layer = set()
        for word in layer:
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in word_set:
                        next_layer.add(new_word)
                        parents[new_word].add(word)
                        if new_word == endWord: found = True
        layer = next_layer

    result = []
    def backtrack(word, path):
        if word == beginWord:
            result.append(path[::-1])
            return
        for parent in parents[word]:
            backtrack(parent, path + [parent])

    if found: backtrack(endWord, [endWord])
    return result

def swim_in_rising_water(grid: List[List[int]]) -> int:
    """
    778. Swim in Rising Water (Hard)

    INTERVIEW SCRIPT:
    "Minimize the maximum elevation along any path from (0,0) to (n-1,n-1).
     Modified Dijkstra: dist[r][c] = min max elevation to reach (r,c).
     O(n² log n)."
    """
    n = len(grid)
    visited = [[False]*n for _ in range(n)]
    heap = [(grid[0][0], 0, 0)]

    while heap:
        t, r, c = heapq.heappop(heap)
        if visited[r][c]: continue
        visited[r][c] = True
        if r == n-1 and c == n-1: return t
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
    return -1

def bellman_ford(n: int, edges: List[List[int]], src: int) -> List[int]:
    """
    Bellman-Ford — single source shortest path with negative edges

    INTERVIEW SCRIPT:
    "Relax all edges V-1 times. After V-1 iterations, shortest paths found.
     On V-th iteration: if any edge still relaxable → negative cycle.
     O(V*E) — slower than Dijkstra but handles negative edges."
    """
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n-1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Check negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return []  # negative cycle exists
    return dist

def regions_cut_by_slashes(grid: List[str]) -> int:
    """
    959. Regions Cut By Slashes

    INTERVIEW SCRIPT:
    "Each cell splits into 4 triangles (top/right/bottom/left).
     '/' connects top-left to bottom-right, '\\' does opposite.
     Union-Find: merge triangles within and across cells.
     Count connected components."
    """
    n = len(grid)
    parent = list(range(4 * n * n))

    def find(x):
        if parent[x] != x: parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        parent[find(x)] = find(y)

    def idx(r, c, t): return (r * n + c) * 4 + t

    for r in range(n):
        for c in range(n):
            # 0=top, 1=right, 2=bottom, 3=left
            if grid[r][c] == '/':
                union(idx(r,c,0), idx(r,c,3))
                union(idx(r,c,1), idx(r,c,2))
            elif grid[r][c] == '\\':
                union(idx(r,c,0), idx(r,c,1))
                union(idx(r,c,2), idx(r,c,3))
            else:
                union(idx(r,c,0), idx(r,c,1))
                union(idx(r,c,1), idx(r,c,2))
                union(idx(r,c,2), idx(r,c,3))
            # Merge with right neighbor
            if c+1 < n: union(idx(r,c,1), idx(r,c+1,3))
            # Merge with bottom neighbor
            if r+1 < n: union(idx(r,c,2), idx(r+1,c,0))

    return len(set(find(i) for i in range(4*n*n)))

# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    grid = [["1","1","0"],["0","1","0"],["0","0","1"]]
    print("Islands:", num_islands_bfs([row[:] for row in grid]))

    print("Course schedule [2,[[1,0]]]:", can_finish(2, [[1,0]]))
    print("Course order [4, [[1,0],[2,0],[3,1],[3,2]]]:", find_order(4, [[1,0],[2,0],[3,1],[3,2]]))

    h = [[1,4],[0,5],[1,5]]
    print("Pacific Atlantic:", pacific_atlantic(h))

    print("Rotting Oranges [[2,1,1],[1,1,0],[0,1,1]]:", oranges_rotting([[2,1,1],[1,1,0],[0,1,1]]))
    print("Word Ladder hit→cog:", ladder_length("hit","cog",["hot","dot","dog","lot","log","cog"]))
    print("Network Delay [[2,1,1],[2,3,1],[3,4,1]] n=4 k=2:", network_delay_time([[2,1,1],[2,3,1],[3,4,1]],4,2))
    print("Cheapest Flights k=1:", find_cheapest_price(3,[[0,1,100],[1,2,100],[0,2,500]],0,2,1))
    print("Bipartite [[1,3],[0,2],[1,3],[0,2]]:", is_bipartite([[1,3],[0,2],[1,3],[0,2]]))
    print("Min Height Trees n=4:", find_min_height_trees(4,[[1,0],[1,2],[1,3]]))
