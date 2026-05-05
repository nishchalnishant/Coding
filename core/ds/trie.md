# Trie (Prefix Tree)

---

## Theory & Mental Models

**What it is:** An N-ary tree where each path from root to a node marked `is_end = True` spells a complete word. Each node represents a character prefix (not a single character); each edge is labeled with a character. Core invariant: root represents the empty string; `is_end` flag distinguishes word boundaries from mere prefixes.

**Why it exists:** Solves the problem of prefix-based search that a hash map cannot do — checking all words sharing a prefix requires O(1) navigation to the prefix node, then O(words) enumeration. Real-world analogy: a filing cabinet where folders are alphabetically nested — the path through folders spells the file name; any folder may contain both sub-folders and files.

**Memory layout:** Each `TrieNode` holds a `children` dict (or fixed array of 26 for lowercase ASCII) and an `is_end` flag. Space is O(ALPHABET_SIZE × total_characters) worst case — shared prefixes share nodes, so common-prefix-heavy datasets are space-efficient.

**Key invariants:**
- Root node represents the empty prefix — never stores a character itself.
- `is_end = True` marks a complete word; a node can be both `is_end` and have children (prefix of another word).
- Every node on a root-to-`is_end` path is a valid prefix of the corresponding word.
- Deletion must remove dead branches (no children, not `is_end`) to avoid memory leaks.

**Complexity at a glance:**

| Operation | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| Insert | O(L) | O(L × Σ) | L = word length, Σ = alphabet size |
| Search (exact) | O(L) | O(1) | Walk L edges, check `is_end` |
| startsWith (prefix) | O(L) | O(1) | Walk L edges, check reachability |
| Autocomplete | O(L + results) | O(results) | Walk to prefix node, then DFS |
| Delete | O(L) | O(1) | Prune dead branches on unwind |

**When to reach for it:**
- Autocomplete and prefix search — hash maps cannot enumerate all words with a prefix efficiently.
- Dictionary word problems with prefix pruning (Word Search II — prune dead subtrees).
- XOR maximization — binary trie processes numbers bit by bit to greedily maximize XOR.
- Word existence with wildcards (`.` matching any char) — DFS over children.
- Longest prefix matching (IP routing tables use compressed Patricia tries).

**Common mistakes:**
- Confusing node = character vs edge = character — the node represents the prefix accumulated so far; the edge label is the next character.
- Forgetting `is_end = True` after inserting the last character — `search("app")` returns `False` if only "apple" is inserted.
- Not pruning dead branches in Word Search II — re-exploring already-found dead paths causes TLE.
- Off-by-one when checking prefix vs full word — always check `is_end` for exact match, reachability for `startsWith`.

---

## Concept Overview

A **Trie** (pronounced "try") is an n-ary tree where each path from root to a node represents a prefix of some stored string. Used for efficient prefix-based operations that a hash map cannot do: autocomplete, prefix search, and longest prefix matching.

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(L) | O(L × Σ) per key |
| Search (exact) | O(L) | — |
| startsWith (prefix) | O(L) | — |
| Delete | O(L) | — |

L = length of key, Σ = alphabet size (26 for lowercase letters).

> [!IMPORTANT]
> **Click Moment**: "autocomplete / prefix search / word dictionary" → Trie. If you also need "**maximum XOR**" or "**find number differing in most bits**" → XOR Trie (binary trie on bit representation).

---

## Core Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end = False
        self.count = 0  # optional: number of words passing through this node

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def _walk(self, prefix: str) -> TrieNode | None:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

> [!TIP]
> Use `dict` (not a fixed array of 26) for children when the alphabet is unknown or sparse. Use `[None] * 26` with `ord(ch) - ord('a')` for pure lowercase ASCII when speed matters.

---

## Key Patterns

### Autocomplete / prefix search

```python
def autocomplete(self, prefix: str) -> list[str]:
    node = self._walk(prefix)
    if not node:
        return []
    results = []
    self._dfs(node, list(prefix), results)
    return results

def _dfs(self, node: TrieNode, path: list[str], results: list[str]) -> None:
    if node.is_end:
        results.append("".join(path))
    for ch, child in node.children.items():
        path.append(ch)
        self._dfs(child, path, results)
        path.pop()
```

#### Common Variants & Twists
1. **Design Search Autocomplete System**:
   - **What (The Problem & Goal):** Design a system that returns the top 3 most frequently searched words starting with a given prefix.
   - **How (Intuition & Mental Model):** Instead of a full DFS on every keystroke (which is slow), store a list of the "top 3 words" directly in each `TrieNode` during the insertion phase. When a word's frequency increases, update the "top 3" list in all its ancestor nodes.
2. **Implement Magic Dictionary**:
   - **What (The Problem & Goal):** Build a dictionary where a search returns `True` if you can change *exactly one* character in the search word to match a word in the dictionary.
   - **How (Intuition & Mental Model):** Use DFS to explore the Trie. Pass a `mismatches` count down the recursion. At each node, try all possible children. If the child's character doesn't match the current character of the search word, increment `mismatches`. If `mismatches` exceeds 1, prune that branch. Return `True` if you reach the end of the search word with `mismatches == 1`.

### Count words with prefix

```python
def count_prefix(self, prefix: str) -> int:
    node = self._walk(prefix)
    return node.count if node else 0
```

---

## Word Search II — Trie + Backtracking

**Problem:** Given a board and a list of words, find all words that exist in the board (connected adjacent cells, no reuse).

**Why Trie:** Searching each word independently = O(W × 4^L) where W = number of words. Trie lets you prune the entire subtree when no word shares the current path's prefix.

```python
def findWords(board: list[list[str]], words: list[str]) -> list[str]:
    trie = Trie()
    for w in words:
        trie.insert(w)

    rows, cols = len(board), len(board[0])
    found = []

    def dfs(r, c, node, path):
        ch = board[r][c]
        if ch not in node.children:
            return
        next_node = node.children[ch]
        path.append(ch)
        if next_node.is_end:
            found.append("".join(path))
            next_node.is_end = False  # deduplicate

        board[r][c] = "#"  # mark visited
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, next_node, path)
        board[r][c] = ch   # restore
        path.pop()

        # prune: if subtree is empty, remove node from parent
        if not next_node.children:
            del node.children[ch]

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, [])

    return found
```

> [!IMPORTANT]
> **Pruning leaf nodes** (`del node.children[ch]` when subtree is empty) is the critical optimization. Without it, already-found dead-end paths are re-explored.

#### Common Variants & Twists
1. **Boggle Game (Maximum Non-overlapping Words)**:
   - **What (The Problem & Goal):** Find the maximum number of words from a dictionary that can be formed on a Boggle board without reusing any cell across *different* words.
   - **How (Intuition & Mental Model):** This is backtracking on top of backtracking. Use the Trie to find a valid word, then "consume" those cells (mark as used) and recursively try to find more words from the remaining cells. You need to backtrack on the entire "word set" choice to find the global maximum.
2. **Concatenated Words**:
   - **What (The Problem & Goal):** Given a list of words, find all words that are formed by concatenating *two or more* shorter words from the same list.
   - **How (Intuition & Mental Model):** Insert all words into a Trie. For each word, use DFS/DP to see if it can be partitioned into multiple prefixes that are each marked as `is_end` in the Trie. If a prefix is a valid word, recursively check if the remainder of the string is also a valid (concatenated) word.

---

## XOR Trie — Maximum XOR Pair

**Problem:** Given an array, find the maximum XOR of any two elements.

**Idea:** Build a binary trie (bit 31 → bit 0) for all numbers. For each number, greedily pick the opposite bit at every level to maximize XOR.

```python
class XORTrie:
    def __init__(self):
        self.root = {}

    def insert(self, num: int) -> None:
        node = self.root
        for bit in range(31, -1, -1):
            b = (num >> bit) & 1
            if b not in node:
                node[b] = {}
            node = node[b]

    def max_xor(self, num: int) -> int:
        node = self.root
        xor = 0
        for bit in range(31, -1, -1):
            b = (num >> bit) & 1
            want = 1 - b  # flip bit to maximize XOR
            if want in node:
                xor |= (1 << bit)
                node = node[want]
            else:
                node = node[b]
        return xor

def findMaximumXOR(nums: list[int]) -> int:
    t = XORTrie()
    for n in nums:
        t.insert(n)
    return max(t.max_xor(n) for n in nums)
```

**Complexity:** O(N × 32) time, O(N × 32) space.

#### Common Variants & Twists
1. **Maximum XOR With an Element From Array**:
   - **What (The Problem & Goal):** Given an array `nums` and queries `(x, m)`, find the maximum XOR of `x` with any `nums[i]` where `nums[i] <= m`.
   - **How (Intuition & Mental Model):** An offline query processing twist. Sort both the array and the queries by their limit `m`. Iterate through the sorted queries, and for each query, insert all numbers from the array that are less than or equal to the current `m` into the XOR Trie. Then perform the standard greedy max-XOR search for `x`.

---

## SDE-3 Deep Dives

### Compressed Trie (Patricia Trie)

When paths have long chains with no branching, merge them into one edge labeled with the full substring. Reduces space from O(total chars) to O(words). Used in IP routing tables (longest prefix match).

### Delete operation

```python
def delete(self, word: str) -> bool:
    def _del(node, word, depth):
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0  # safe to delete if leaf
        ch = word[depth]
        if ch not in node.children:
            return False
        should_delete_child = _del(node.children[ch], word, depth + 1)
        if should_delete_child:
            del node.children[ch]
            return not node.is_end and len(node.children) == 0
        return False
    _del(self.root, word, 0)
```

### Aho-Corasick (multi-pattern matching in a stream)

Build a Trie of all patterns + add **failure links** (like KMP's LPS, but across the trie). Lets you match all K patterns in a text of length N in O(N + total matches) — much faster than running KMP K times. See [string.md](../algorithms/string.md) for implementation sketch.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Core Logic | Trickiness & Details |
|----------|---------|------------|----------------------|
| **Implement Trie** [E] | Trie Insert/Search | TrieNode with `children` dict + `is_end`; walk on insert/search/startsWith | Don't forget `is_end = True` after inserting last char |
| **Word Search II** [H] | Trie + Grid DFS Backtrack | Build trie of words; DFS from each cell; prune when no prefix match | Mark visited with `#`; prune dead trie nodes after finding to cut later DFS |
| **Maximum XOR of Two Numbers** [M] | XOR Trie (Binary, Greedy) | Binary XOR trie; greedily choose opposite bit | Process bits from MSB (bit 31) to LSB; handle negative numbers with sign bit |
| **Replace Words** [M] | Trie Prefix Lookup | Build trie of roots; for each word walk trie until is_end or end of word | Return shortest root prefix, not full word |
| **Design Search Autocomplete** [M] | Trie + DFS / Top-K Cache | Trie insert + DFS from prefix node; optionally rank by frequency | Store top-3 at each node (lazy — update on insert) to avoid DFS on every query |
| **Longest Word in Dictionary** [M] | Trie BFS on is_end Nodes | Insert all; BFS/DFS only on `is_end` nodes; track longest | Must be buildable one char at a time from root — only traverse via `is_end` nodes |
| **Map Sum Pairs** [M] | Trie with Subtree Sums | Trie where each node stores sum of all key values in its subtree | On insert, if key already exists, subtract old value before adding new |
| **Word Squares** [H] | Trie + Backtrack (Column Prefix) | Build trie; at row `k` need prefix = column `k` of all previous words | Store word list at each trie node; backtrack using prefix constraint per row |
| **Number of Distinct Substrings** [H] | Suffix Trie / Suffix Array | Build suffix trie (or suffix array); count non-root edges | Suffix trie has O(N²) nodes; suffix array with LCP is O(N log N) — mention tradeoff |

---

## Common Gotchas

> [!CAUTION]
> **`is_end` vs prefix**: `search("app")` must return `False` if only "apple" was inserted. Never conflate prefix reachability with word completion — `is_end` is the only reliable check.

> [!CAUTION]
> **Word Search II deduplication**: If the same word appears twice on the board, you'll add it twice. Set `node.is_end = False` immediately after recording it, or use a set for results.

> [!CAUTION]
> **XOR Trie bit width**: Use 31 bits for non-negative integers. If the array can contain negatives, use 32 bits and treat them as unsigned.

---

## Quick Revision

| Trigger | → Use |
|---------|-------|
| Autocomplete / prefix search | Trie insert + DFS from prefix node |
| Dictionary word check with prefix pruning | Trie + backtracking (Word Search II) |
| Maximum XOR of two numbers | XOR Trie (binary, MSB→LSB, greedy opposite bit) |
| Multi-pattern stream matching | Aho-Corasick (Trie + failure links) |
| IP longest prefix match | Compressed trie / Patricia trie |

---

## Quick Revision Triggers

- If the problem says "autocomplete" or "return all words with prefix X" → think Trie; walk to prefix node in O(L), then DFS all `is_end` descendants.
- If the problem says "does any word in the dictionary start with this prefix" → think Trie `startsWith`; O(L) regardless of dictionary size.
- If the problem says "find all words on a board" (Word Search II) → think Trie + DFS Backtracking; prune when no prefix match and delete dead nodes after finding.
- If the problem says "maximum XOR of two numbers" → think Binary XOR Trie; process bits MSB→LSB, greedily choose opposite bit at each level.
- If the problem says "replace words with shortest root" → think Trie; insert all roots, walk each word until `is_end` hit.
- If the problem says "design search autocomplete with ranking" → think Trie with top-K list cached at each node; avoid full DFS on every query.
- If you need multi-pattern matching in a stream → think Aho-Corasick (Trie + failure links); O(N + matches) vs O(N×K) for K patterns.

## See also

- [backtracking.md](../algorithms/backtracking.md) — Word Search II uses Trie + backtracking together
- [bit-manipulation.md](../algorithms/bit-manipulation.md) — XOR Trie for max XOR pair
- [string.md](../algorithms/string.md) — Aho-Corasick for multi-pattern matching
- [hashing.md](hashing.md) — alternative for exact word lookups when prefix search not needed
