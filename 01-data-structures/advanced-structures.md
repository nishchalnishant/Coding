# Advanced Data Structures: Tries and Segment Trees

## Tries (Prefix Trees)
Tries are mainly used in SDE 3 interviews for problems involving prefix matching, wildcard string searches, or bitwise XOR maximization.

### Node Structure
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

### 1. Standard Trie Implementation
```python
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

### Common SDE 3 Trie Problems:
1.  **Word Search II**: Use a Trie to store words, then perform backtracking on the grid to search for them efficiently.
2.  **[Maximum XOR of Two Numbers](../google-sde2/PROBLEM_DETAILS.md#maximum-xor-of-two-numbers)**: Use a Binary Trie. Insert numbers into the Trie, and for each number, try to greedily find the path corresponding to its bitwise complement.

---

---

## Segment Trees
Crucial for answering range sum/min/max queries over an array, with the ability to update the array in $O(\log n)$.

> [!TIP]
> **Full Deep Dive**: See the dedicated [Segment Trees Guide](segment-tree.md) for canonical implementations, Lazy Propagation, and SDE-3 Interview variants.

---

## Fenwick Tree (Binary Indexed Tree)
More memory efficient `O(N)` and easier to implement than segment trees for simple sum queries.
```python
class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def update(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
```

---

## Pattern Recognition

- **Trie**: Prefix match, autocomplete, word search in grid (store words, backtrack). Binary Trie: max XOR (prefer opposite bit).
- **Segment Tree**: Range sum/min/max with point or range updates; O(log N) query/update. Lazy propagation for range add/update.
- **Fenwick**: Range sum + point update; simpler than segment tree; O(N) space.

## Interview Strategy

- **Identify**: "Prefix" / "autocomplete" / "word dictionary" → Trie. "Range query" with updates → Segment tree or Fenwick.
- **Common mistakes**: Trie — forgetting is_end; Segment tree — wrong segment bounds; Fenwick — 1-indexed.

## Quick Revision

- **Trie**: insert/search/startsWith O(L). Binary trie for max XOR. Word Search II: Trie + backtrack.
- **Segment tree**: 4*N nodes; build O(N); query/update O(log N). Lazy for range update.
- **Fenwick**: update(i, delta), query(i) prefix sum; i += i&-i / i -= i&-i.
