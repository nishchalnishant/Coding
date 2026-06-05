---
module: 01-data-structures
topic: Trie
subtopic: 
status: unread
tags: [data-structures, trie]
---

← [Data structures index](./README.md) · [DS decision tree](./ds_tree.md)
## First-Principles Map

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.


```
WHY tries exist → WHAT they are → HOW they work → WHEN to use → WHAT can go wrong
       │                │                │               │               │
  [HashMaps can't      [tree where each  [insert: follow [autocomplete,  [memory blowup:
   answer "all words   edge = one char;  path char by    spell check,    26 children per
   with prefix 'pre'"; nodes share       char, create    IP routing,     node × depth =
   sorted arrays pay   common prefixes;  node if missing; word search,   O(alphabet×L×n)
   O(L×log n) for      each leaf/marked  search: follow  prefix count,   for n words of
   prefix queries]     node = word end]  until mismatch; longest prefix  length L]
                                         O(L) all ops]   matching]
       │                │                │
  [real-world:         [invariant:      [compressed trie (radix tree):
   phone book prefix   root is empty;    merge single-child chains;
   search; DNS         all strings in    reduces O(alphabet×L×n) nodes
   longest-prefix      the trie share    to O(n) nodes for n words;
   match]              common prefixes]  used in Linux kernel routing]
       ↓
[Decision: Trie vs alternatives]
  ├── vs HashMap    → trie supports prefix queries; hash only exact match O(1)
  ├── vs BST        → trie O(L) vs BST O(L×log n) for string keys
  └── vs Suffix Array → suffix array for substring queries; trie for prefix queries
```

## First-Principles Breakdown
- **Root problem**: Prefix-based operations (autocomplete, "all words starting with X") need O(L) time regardless of dictionary size — no hash or tree achieves this.
- **Core insight**: Sharing common prefixes as tree paths means each character is stored once per distinct prefix, not once per word.
- **Invariant**: The path from root to any marked node spells exactly one dictionary word; every node's depth equals the length of the shared prefix to that point.
- **Why it's fast**: Any operation (insert, search, prefix query) takes O(L) where L = string length — independent of dictionary size n.
- **Where it breaks**: Memory is O(alphabet_size × L × n) in the worst case; for Unicode alphabets this is impractical — use a HashMap of children instead of fixed array.

# Trie (Prefix Tree)

```
[TRIE (PREFIX TREE) — MINDMAP]
├── WHY IT EXISTS
│   ├── Problem it solves: O(L) prefix lookup / insert / delete where L = word length — hash maps can't do prefix range queries
│   ├── Hash map: O(L) per word but no shared structure → wastes memory for common prefixes
│   └── Analogy: a trie is like a directory tree — every path from root to leaf spells out a word; shared prefixes share nodes
├── WHAT IT IS (First Principles)
│   ├── Core definition: tree where each edge is labeled with a character; root = empty string; path root→node = prefix
│   ├── Node stores: children map (char → node), is_end flag (marks valid word terminus)
│   ├── Key property: all strings sharing a prefix share the same path segment from root
│   └── Alphabet size σ: 26 for lowercase English → fixed array[26]; arbitrary → hash map children
├── HOW IT WORKS
│   ├── Insert(word)
│   │   ├── Walk existing nodes character by character
│   │   ├── Create missing child nodes along the way
│   │   └── Set is_end = True on last node — O(L)
│   ├── Search(word)
│   │   ├── Walk nodes; if any child missing → word absent
│   │   └── Return is_end on last node — O(L)
│   ├── StartsWith(prefix)
│   │   ├── Walk nodes for each prefix char
│   │   └── If all chars found → prefix exists (don't check is_end) — O(L)
│   ├── Delete(word)
│   │   ├── DFS to end of word; unset is_end
│   │   └── Prune childless, non-terminal nodes on backtrack — O(L)
│   ├── Compressed Trie (Radix Tree / Patricia Trie)
│   │   ├── Merge single-child chains into one edge with a substring label
│   │   └── Reduces node count from O(total chars) to O(number of words)
│   └── Bitwise Trie (XOR Trie)
│       ├── Keys are integers; branch on bits from MSB to LSB (depth = 32 or 64)
│       └── Classic use: maximize XOR of two numbers in array — O(32·N)
├── COMPLEXITY SUMMARY
│   ├── Insert / Search / StartsWith: O(L) time, O(L·σ) space per node worst case
│   ├── Space total: O(N·L·σ) worst, O(N·L) with hash map children
│   ├── Autocomplete (all words with prefix): O(L + output_size)
│   └── XOR maximization: O(32·N) build + O(32) per query
├── WHEN TO USE
│   ├── Signal: "autocomplete / type-ahead" → trie with DFS from prefix node
│   ├── Signal: "count / list all words with given prefix" → trie
│   ├── Signal: "word search on a board with dictionary" → trie to prune DFS early
│   ├── Signal: "maximum XOR of any two numbers" → bitwise trie
│   ├── Signal: "wildcard match (. = any char)" → trie DFS with branching on '.'
│   └── Avoid when: only exact-match lookups needed (hash set is simpler and faster in practice)
└── COMMON MISTAKES / GOTCHAS
    ├── Forgetting is_end flag: "app" and "apple" share nodes — must mark word boundary separately
    ├── Fixed-size children array: wastes 26× memory for sparse alphabets — use dict children instead
    ├── Delete without pruning: leaves dead nodes, memory leak in long-running systems
    ├── Bitwise trie bit order: always process MSB first; mixing up order corrupts XOR queries
    ├── Off-by-one in depth: 32-bit int needs depth 32, not 31 — include sign bit if needed
    └── Returning prefix match as word match: StartsWith returning True ≠ Search returning True
```




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
> **Click Moment**: "autocomplete / prefix search / word dictionary" → Trie. If you also need "**maximum XOR `⚡ T1`**" or "**find number differing in most bits**" → XOR Trie (binary trie on bit representation).

---

## Core Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_end = False
        self.count = 0  # number of words passing through this node

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

    def delete(self, word: str) -> bool:
        """
        Deletes a word from the Trie. Prunes dead nodes recursively and 
        synchronizes prefix count tracking. Returns True if word existed and was deleted.
        """
        def _recurse(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False  # Target word does not exist
                node.is_end = False
                return len(node.children) == 0  # Safe to prune if it is a leaf node

            ch = word[depth]
            if ch not in node.children:
                return False  # Path mismatch
            
            should_prune_child = _recurse(node.children[ch], word, depth + 1)
            
            if should_prune_child:
                del node.children[ch]
                # If current node is not a word endpoint and has no children left, prune it
                return not node.is_end and len(node.children) == 0
            
            # Decrement prefix count on backtrack if the child was not pruned
            node.children[ch].count -= 1
            return False

        return _recurse(self.root, word, 0)
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
1. **Design Search Autocomplete System `⚡ T1`**:
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

Build a Trie of all patterns + add **failure links** (like KMP's LPS, but across the trie). Lets you match all K patterns in a text of length N in O(N + total matches) — much faster than running KMP K times. See [string.md](../02-algorithms/string.md) for implementation sketch.

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Core Logic | Trickiness & Details |
|----------|---------|------------|----------------------|
| **Implement Trie `⚡ T1`** [E] | Trie Insert/Search | TrieNode with `children` dict + `is_end`; walk on insert/search/startsWith | Don't forget `is_end = True` after inserting last char |
| **Word Search II `⚡ T1`** [H] | Trie + Grid DFS Backtrack | Build trie of words; DFS from each cell; prune when no prefix match | Mark visited with `#`; prune dead trie nodes after finding to cut later DFS |
| **Maximum XOR of Two Numbers `⚡ T1`** [M] | XOR Trie (Binary, Greedy) | Binary XOR trie; greedily choose opposite bit | Process bits from MSB (bit 31) to LSB; handle negative numbers with sign bit |
| **Replace Words `⚡ T1`** [M] | Trie Prefix Lookup | Build trie of roots; for each word walk trie until is_end or end of word | Return shortest root prefix, not full word |
| **Design Search Autocomplete `⚡ T1`** [M] | Trie + DFS / Top-K Cache | Trie insert + DFS from prefix node; optionally rank by frequency | Store top-3 at each node (lazy — update on insert) to avoid DFS on every query |
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

- [backtracking.md](../02-algorithms/backtracking.md) — Word Search II uses Trie + backtracking together
- [bit-manipulation.md](../02-algorithms/bit-manipulation.md) — XOR Trie for max XOR pair
- [string.md](../02-algorithms/string.md) — Aho-Corasick for multi-pattern matching
- [hashing.md](hashing.md) — alternative for exact word lookups when prefix search not needed

## Flashcards

**Why does a Trie outperform a Sorted Array + Binary Search for prefix matching with string length L and dictionary size N?** #flashcard
Sorted array + binary search takes $O(L \log N)$ because each of the $\log N$ string comparisons takes up to $O(L)$ time. A Trie takes $O(L)$ time, which is completely independent of the dictionary size $N$.

**What is the worst-case space complexity of a standard Trie storing N words of maximum length L over an alphabet of size Σ?** #flashcard
$O(N \cdot L \cdot \Sigma)$ in the worst case where no words share any common prefixes, requiring a child pointer array of size $\Sigma$ at every node.

**Why does a Trie node require an `is_end` flag instead of just checking if a node is a leaf?** #flashcard
A node can be a complete word and also a prefix for longer words (e.g., "app" and "apple"). The `is_end` flag distinguishes valid word completions from intermediate prefix nodes.

**What is the critical optimization that prevents Word Search II (Trie + Backtracking) from TLEing on dense boards?** #flashcard
Pruning dead leaf nodes during backtracking: if a child `TrieNode` has no children remaining after exploration, delete it from its parent's `children` map (`del node.children[ch]`) to prevent subsequent DFS paths from re-exploring a dead branch.

**How does a Binary XOR Trie find the maximum XOR pair for a number X in O(32) time?** #flashcard
By processing bits from Most Significant Bit (MSB) to Least Significant Bit (LSB) and greedily choosing the path corresponding to the opposite bit of X at each step (since $1 \oplus 0 = 1$). If the opposite bit is unavailable, it falls back to the same bit.

**What is a Compressed Trie (Radix Tree) and when does it improve space complexity?** #flashcard
A Trie variant where all single-child intermediate chains are merged into single edges with substring labels. It reduces the node count to $O(N)$ for $N$ words, saving massive memory when there are many long non-branching sequences.

