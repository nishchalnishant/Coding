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
2.  **Maximum XOR of Two Numbers**: Use a Binary Trie. Insert numbers into the Trie, and for each number, try to greedily find the path corresponding to its bitwise complement.

---

## Segment Trees
Crucial for answering range sum/min/max queries over an array, with the ability to update the array in $O(\log n)$.

### Node Structure
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.build(data, 0, 0, self.n - 1)

    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self.build(data, 2 * node + 1, start, mid)
        self.build(data, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if start <= idx <= mid:
            self.update(2 * node + 1, start, mid, idx, val)
        else:
            self.update(2 * node + 2, mid + 1, end, idx, val)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, node, start, end, l, r):
        if r < start or l > end:
            return 0  # In sum query, return 0; for min, return infinity
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_sum = self.query(2 * node + 1, start, mid, l, r)
        right_sum = self.query(2 * node + 2, mid + 1, end, l, r)
        return left_sum + right_sum
```

### Lazy Propagation
For range update queries, SDE 3 level questions often require Lazy Propagation to avoid deep recursive updates immediately.

### Alternative: Fenwick Tree (Binary Indexed Tree)
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
