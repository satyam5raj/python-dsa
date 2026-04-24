"""
================================================================
TOPIC 14: TRIES (PREFIX TREES)
================================================================
A tree where each path from root represents a prefix.
USE: Autocomplete, spell checkers, IP routing, word search

INTERVIEW COMMUNICATION:
"A trie stores strings character by character.
 Each node = one character, root = empty.
 O(m) insert/search where m = key length.
 Perfect for prefix-based operations like autocomplete."
================================================================
"""

from typing import List, Optional

# ================================================================
# BASIC TRIE IMPLEMENTATION
# ================================================================

class TrieNode:
    def __init__(self):
        self.children = {}  # char → TrieNode
        self.is_end = False

class Trie:
    """
    Basic trie with insert, search, startsWith.
    All operations O(m) where m = string length.

    INTERVIEW SCRIPT:
    "Each node has a dictionary of children and an end flag.
     Insert: create nodes along path, mark last as end.
     Search: traverse path; if any char missing, return False.
     StartsWith: same as search but don't need is_end."

    USE CASE: Autocomplete, prefix matching, spell correction
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """O(m) — traverse/create m nodes"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """O(m) — must reach end node with is_end=True"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        """O(m) — just need to traverse prefix path"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def delete(self, word: str) -> bool:
        """Delete word from trie — O(m)"""
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            char = word[depth]
            if char not in node.children:
                return False
            should_delete = _delete(node.children[char], word, depth + 1)
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            return False
        return _delete(self.root, word, 0)

    def autocomplete(self, prefix: str) -> List[str]:
        """Find all words starting with prefix — O(p + n)"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        def dfs(curr_node, curr_prefix):
            if curr_node.is_end:
                results.append(curr_prefix)
            for char, child in curr_node.children.items():
                dfs(child, curr_prefix + char)

        dfs(node, prefix)
        return results

# ================================================================
# TRIE WITH ARRAY (fixed alphabet = 26 lowercase)
# ================================================================

class TrieNodeArray:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

class TrieArray:
    """
    Faster trie using array instead of dict.
    O(1) child lookup (no hashing), slightly more memory.
    """
    def __init__(self):
        self.root = TrieNodeArray()

    def _idx(self, c):
        return ord(c) - ord('a')

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            i = self._idx(char)
            if not node.children[i]:
                node.children[i] = TrieNodeArray()
            node = node.children[i]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            i = self._idx(char)
            if not node.children[i]:
                return False
            node = node.children[i]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            i = self._idx(char)
            if not node.children[i]:
                return False
            node = node.children[i]
        return True

# ================================================================
# WORD SEARCH II — Trie + Backtracking
# ================================================================

def find_words(board: List[List[str]], words: List[str]) -> List[str]:
    """
    Find all words in board (Word Search II).
    O(m * n * 4^L) where L = max word length

    INTERVIEW SCRIPT:
    "Brute force: run word search for each word — too slow.
     Better: build trie from all words, then DFS the board once.
     At each cell, follow trie node matching board characters.
     When trie node has is_end: found a word!
     Optimization: remove found words from trie to avoid duplicates."
    """
    trie = Trie()
    for word in words:
        trie.insert(word)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(r, c, node, path):
        if node.is_end:
            result.add(path)
            node.is_end = False  # avoid duplicates

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        char = board[r][c]
        if char not in node.children:
            return

        board[r][c] = '#'  # mark visited
        child = node.children[char]
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r+dr, c+dc, child, path+char)
        board[r][c] = char  # restore

        # Prune empty nodes
        if not child.children:
            del node.children[char]

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")

    return list(result)

# ================================================================
# TRIE FOR IP ROUTING (Prefix Matching)
# ================================================================

class IPTrie:
    """
    Longest prefix matching for network routing.
    USE CASE: Router lookup tables in networking
    """
    def __init__(self):
        self.root = [None, None, None]  # [left_child, right_child, next_hop]

    def insert(self, prefix: str, next_hop: str):
        """Insert IP prefix (binary string) with next hop"""
        node = self.root
        for bit in prefix:
            idx = int(bit)
            if not node[idx]:
                node[idx] = [None, None, None]
            node = node[idx]
        node[2] = next_hop  # store routing info

    def longest_prefix_match(self, ip: str) -> Optional[str]:
        """Find longest matching prefix for IP"""
        node = self.root
        best_hop = None
        for bit in ip:
            idx = int(bit)
            if not node[idx]:
                break
            node = node[idx]
            if node[2]:
                best_hop = node[2]
        return best_hop

# ================================================================
# REPLACE WORDS USING TRIE
# ================================================================

def replace_words(dictionary: List[str], sentence: str) -> str:
    """
    Replace words in sentence with their shortest root.
    O(n + m * L) where n = dict size, m = sentence words, L = avg word length

    INTERVIEW SCRIPT:
    "Insert all roots into trie.
     For each word in sentence: walk trie until end of word or root found.
     If root found: replace. Else: keep original."
    """
    trie = Trie()
    for root in dictionary:
        trie.insert(root)

    def replace(word):
        node = trie.root
        for i, char in enumerate(word):
            if char not in node.children:
                break
            node = node.children[char]
            if node.is_end:
                return word[:i+1]  # return shortest root
        return word

    return ' '.join(replace(w) for w in sentence.split())

# ================================================================
# COUNT WORDS WITH PREFIX — Trie with counts
# ================================================================

class TrieWithCount:
    """Trie that counts how many words pass through each node"""
    class Node:
        def __init__(self):
            self.children = {}
            self.word_count = 0
            self.prefix_count = 0

    def __init__(self):
        self.root = self.Node()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = self.Node()
            node = node.children[char]
            node.prefix_count += 1
        node.word_count += 1

    def count_words_with_prefix(self, prefix: str) -> int:
        """O(m) — return number of words that start with prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.prefix_count

    def search_count(self, word: str) -> int:
        node = self.root
        for char in word:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.word_count

# ================================================================
# USE CASES SUMMARY
# ================================================================
"""
Trie applications:
1. Autocomplete: Type 'py' → suggest 'python', 'pytest', 'pypi'
2. Spell checker: Find closest words to misspelled word
3. IP routing: Longest prefix matching in routers
4. Phone book: O(m) lookup vs O(log n) for sorted list
5. Word games: Scrabble, Boggle word validation
6. Genome analysis: DNA sequence prefix matching

WHEN TO USE TRIE vs HASH SET:
- Prefix operations: TRIE wins
- Exact match only: HASH SET wins (simpler)
- Memory: HASH SET often more compact
- Ordered traversal by prefix: TRIE
"""

if __name__ == "__main__":
    trie = Trie()
    words = ["apple", "app", "apricot", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)

    print("Search 'apple':", trie.search("apple"))
    print("Search 'app':", trie.search("app"))
    print("Search 'ap':", trie.search("ap"))
    print("Starts with 'app':", trie.startsWith("app"))
    print("Autocomplete 'ap':", trie.autocomplete("ap"))
    print("Autocomplete 'ban':", trie.autocomplete("ban"))

    # Replace words
    print("Replace words:", replace_words(["cat","bat","rat"],
                                          "the cattle was rattled by the battery"))

    # Word count trie
    twc = TrieWithCount()
    for w in words:
        twc.insert(w)
    print("Words with prefix 'app':", twc.count_words_with_prefix("app"))
    print("Words with prefix 'ban':", twc.count_words_with_prefix("ban"))
