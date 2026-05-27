---
tags: [coding, data-structures, trie]
topic: Trie
difficulty: mixed
---

# Trie Problems

Pattern tags: trie insert/search, prefix search, backtracking, XOR trie, suffix trie.

---

## Core Trie Implementation

### Implement Trie (Prefix Tree)

> [!example] Problem
> Implement a Trie with `insert(word)`, `search(word)` (returns true only if the exact word was inserted), and `startsWith(prefix)` (returns true if any inserted word begins with `prefix`).

> [!info] Approach
> - **WHY:** A hash set gives O(L) exact match but cannot answer "does any word start with prefix X?" without scanning all keys — O(N × L). A Trie shares common prefixes as tree paths, enabling O(L) prefix queries regardless of dictionary size N.
> - **WHAT:** N-ary tree where each edge carries one character. Each node holds a `children` dict and an `is_end` flag. The path from root to any node marked `is_end = True` spells a complete word.
> - **HOW:**
>   - `insert`: walk the tree character by character, creating nodes as needed, set `is_end = True` at the last character.
>   - `search`: walk the tree; return False if any character is missing; return `node.is_end` at the end — this distinguishes "apple" (exact) from "app" (only prefix).
>   - `startsWith`: same walk as search but return True after the walk completes regardless of `is_end`.

> [!note]- Python Solution
> ```python
> class TrieNode:
>     def __init__(self) -> None:
>         self.children: dict[str, TrieNode] = {}
>         self.is_end: bool = False
> 
> class Trie:
>     def __init__(self) -> None:
>         self.root = TrieNode()
> 
>     def insert(self, word: str) -> None:
>         node = self.root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = TrieNode()
>             node = node.children[c]
>         node.is_end = True
> 
>     def search(self, word: str) -> bool:
>         node = self._walk(word)
>         return node is not None and node.is_end
> 
>     def startsWith(self, prefix: str) -> bool:
>         return self._walk(prefix) is not None
> 
>     def _walk(self, s: str) -> TrieNode | None:
>         node = self.root
>         for c in s:
>             if c not in node.children:
>                 return None
>             node = node.children[c]
>         return node
> 
>     def delete(self, word: str) -> bool:
>         """Remove word; prune dead branches. Returns True if word existed."""
>         def _del(node: TrieNode, depth: int) -> bool:
>             if depth == len(word):
>                 if not node.is_end:
>                     return False
>                 node.is_end = False
>                 return len(node.children) == 0   # safe to prune if leaf
>             c = word[depth]
>             if c not in node.children:
>                 return False
>             should_prune = _del(node.children[c], depth + 1)
>             if should_prune:
>                 del node.children[c]
>                 return not node.is_end and len(node.children) == 0
>             return False
>         return _del(self.root, 0)
> ```

> [!success] Complexity
> Time O(L) per operation where L = word/prefix length. Space O(N × L × Σ) total where N = words, Σ = alphabet size (26 for lowercase, use `dict` for arbitrary).

> [!tip] Alternatives
> - Hash set: O(L) exact search, O(N × L) prefix scan — no true prefix query support.
> - Sorted list + binary search: O(log N) prefix range, O(N) insert — no O(L) guarantee.
> - Fixed `children[26]` array instead of dict: faster constant (array index vs hash), but 26× memory waste for sparse alphabets.

---

## Autocomplete / Prefix Search

### Design Search Autocomplete System

> [!example] Problem
> Given initial sentences and their frequencies, design an autocomplete system. `input(c)` processes one character at a time; when `c == '#'` it saves the current input sentence and returns `[]`; otherwise returns the top 3 historical sentences with the current prefix, ranked by frequency descending (ties broken alphabetically).

> [!info] Approach
> - **WHY:** Running a full DFS from the prefix node on every keystroke is O(output) per character — acceptable, but storing top-k cached at each node avoids DFS entirely at query time.
> - **WHAT:** Trie where each node stores a `counts` dict mapping `sentence → frequency` for all sentences whose prefix passes through this node. Query is O(1) + sort of the matched candidates at the node.
> - **HOW:** On `insert(sentence, freq)`: walk each character; at each node update `node.counts[sentence] += freq`. On `input(c)`: if `'#'`, save current input with frequency 1 (update all ancestor nodes on insertion path), reset state. Otherwise, advance `curr_node` by one character and return `sorted(curr_node.counts, key=lambda s: (-counts[s], s))[:3]`.

> [!note]- Python Solution
> ```python
> class ACNode:
>     def __init__(self) -> None:
>         self.children: dict[str, ACNode] = {}
>         self.counts: dict[str, int] = {}   # sentence → freq for all sentences through this node
> 
> class AutocompleteSystem:
>     def __init__(self, sentences: list[str], times: list[int]) -> None:
>         self.root = ACNode()
>         self.curr_node: ACNode | None = self.root
>         self.curr_input: list[str] = []
>         for s, t in zip(sentences, times):
>             self._insert(s, t)
> 
>     def _insert(self, sentence: str, freq: int) -> None:
>         node = self.root
>         for c in sentence:
>             if c not in node.children:
>                 node.children[c] = ACNode()
>             node = node.children[c]
>             node.counts[sentence] = node.counts.get(sentence, 0) + freq
> 
>     def input(self, c: str) -> list[str]:
>         if c == '#':
>             sentence = ''.join(self.curr_input)
>             self._insert(sentence, 1)
>             self.curr_input = []
>             self.curr_node = self.root
>             return []
>         self.curr_input.append(c)
>         if self.curr_node and c in self.curr_node.children:
>             self.curr_node = self.curr_node.children[c]
>         else:
>             self.curr_node = None
>         if not self.curr_node:
>             return []
>         return sorted(
>             self.curr_node.counts,
>             key=lambda s: (-self.curr_node.counts[s], s)   # type: ignore[union-attr]
>         )[:3]
> ```

> [!success] Complexity
> Time O(p + q log q) per input character where p = prefix length walked, q = number of matching sentences at the node. Space O(S × L) total — each sentence stored at every node on its path.

> [!tip] Alternatives
> - Trie with DFS at query time: store only `is_end` and frequency per node; DFS all matching sentences on each keystroke — O(output) per query, lower space per node.
> - Hash map only: store all sentences; filter by prefix on each query — O(N × L) per query. Simple but doesn't scale.

---

### Map Sum Pairs

> [!example] Problem
> Implement `MapSum` with `insert(key, val)` and `sum(prefix)` returning the sum of all key values whose keys start with `prefix`.

> [!info] Approach
> - **WHY:** A trie propagates prefix sums naturally — each node on the insertion path of a key can accumulate that key's value. `sum(prefix)` then just reads the accumulated value at the prefix endpoint.
> - **WHAT:** Trie where each node stores `prefix_sum` = sum of all values of keys passing through this node.
> - **HOW:** On `insert(key, val)`: if key already exists, compute `delta = val - old_val` to avoid double-counting. Walk each character of key; at each node add `delta` to `node.prefix_sum`. On `sum(prefix)`: walk to the prefix node and return `node.prefix_sum`.

> [!note]- Python Solution
> ```python
> class MSNode:
>     def __init__(self) -> None:
>         self.children: dict[str, MSNode] = {}
>         self.prefix_sum: int = 0
> 
> class MapSum:
>     def __init__(self) -> None:
>         self.root = MSNode()
>         self.key_map: dict[str, int] = {}   # tracks inserted key values
> 
>     def insert(self, key: str, val: int) -> None:
>         delta = val - self.key_map.get(key, 0)
>         self.key_map[key] = val
>         node = self.root
>         for c in key:
>             if c not in node.children:
>                 node.children[c] = MSNode()
>             node = node.children[c]
>             node.prefix_sum += delta
> 
>     def sum(self, prefix: str) -> int:
>         node = self.root
>         for c in prefix:
>             if c not in node.children:
>                 return 0
>             node = node.children[c]
>         return node.prefix_sum
> ```

> [!success] Complexity
> Time O(L) per operation. Space O(N × L).

> [!tip] Alternatives
> - Hash map + linear scan: `sum(v for k, v in d.items() if k.startswith(prefix))` — O(N × L) per query. Simple for small N.

---

### Longest Word in Dictionary

> [!example] Problem
> Given a list of strings, find the longest word that can be built one character at a time — each prefix of the word must also be in the list. If there's a tie, return the lexicographically smallest.

> [!info] Approach
> - **WHY:** "Each prefix must also be in the dictionary" maps exactly to "each ancestor in the trie must have `is_end = True`". Trie lets us enforce this constraint during a BFS/DFS traversal.
> - **WHAT:** Insert all words. Then traverse the trie only through nodes with `is_end = True` (the root is the empty prefix — treat it as `is_end = True` for traversal purposes). Track the longest path reached.
> - **HOW:** Insert all words. BFS from root — only enqueue child nodes where `is_end = True`. At each node, track the current word. Update the answer when a longer (or lexicographically smaller tie) word is found.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class LWNode:
>     def __init__(self) -> None:
>         self.children: dict[str, LWNode] = {}
>         self.is_end: bool = False
>         self.word: str = ""
> 
> class Solution:
>     def longestWord(self, words: list[str]) -> str:
>         root = LWNode()
>         for w in sorted(words):   # sort so lexicographically earlier words are inserted first
>             node = root
>             for c in w:
>                 if c not in node.children:
>                     node.children[c] = LWNode()
>                 node = node.children[c]
>             node.is_end = True
>             node.word = w
> 
>         best = ""
>         # BFS only through is_end nodes
>         queue: deque[LWNode] = deque([root])
>         while queue:
>             node = queue.popleft()
>             for child in node.children.values():
>                 if child.is_end:
>                     if len(child.word) > len(best) or \
>                        (len(child.word) == len(best) and child.word < best):
>                         best = child.word
>                     queue.append(child)
>         return best
> ```

> [!success] Complexity
> Time O(N × L log(N × L)) for sorted insert + O(N × L) BFS. Space O(N × L).

> [!tip] Alternatives
> - Sort by length then DFS: sort words by length; insert progressively — a word is valid iff its `word[:-1]` is already in a set. O(N × L) time. Simpler, no trie needed.

---

### Replace Words

> [!example] Problem
> Given a dictionary of root words and a sentence, replace each word in the sentence with its shortest matching root. If a word has multiple roots, use the shortest one.

> [!info] Approach
> - **WHY:** For each word in the sentence, we need to find the shortest dictionary root that is a prefix of that word. A trie answers "what is the shortest prefix of this string that exists in the dictionary?" in O(L) — walk until the first `is_end` node.
> - **WHAT:** Trie of all root words. For each sentence word, walk the trie character by character — return as soon as `is_end` is hit (shortest root match).
> - **HOW:** Insert all roots into the trie. For each word in the sentence, walk the trie; if `is_end` is reached at depth `d`, replace the word with `word[:d]`. If the walk exits without finding a root, keep the original word.

> [!note]- Python Solution
> ```python
> class RWNode:
>     def __init__(self) -> None:
>         self.children: dict[str, RWNode] = {}
>         self.is_end: bool = False
> 
> def replaceWords(dictionary: list[str], sentence: str) -> str:
>     root = RWNode()
>     for word in dictionary:
>         node = root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = RWNode()
>             node = node.children[c]
>         node.is_end = True
> 
>     def replace(word: str) -> str:
>         node = root
>         for i, c in enumerate(word):
>             if c not in node.children:
>                 break
>             node = node.children[c]
>             if node.is_end:
>                 return word[:i + 1]   # shortest root found
>         return word   # no root matched
> 
>     return " ".join(replace(w) for w in sentence.split())
> ```

> [!success] Complexity
> Time O(D × L + S × L) where D = dictionary size, L = max word length, S = sentence word count. Space O(D × L).

> [!tip] Alternatives
> - Hash set + prefix scan: for each sentence word, try `word[:1]`, `word[:2]`, ..., checking if each is in the set — O(L² per word). Simpler but slower.
> - Sort roots by length, linear scan: sort dictionary; for each sentence word, try each root — O(D × L per word). Correct but O(S × D × L) total.

---

## Trie + Backtracking

### Word Search II

> [!example] Problem
> Given a board of characters and a list of words, return all words that appear on the board. A word is valid if it can be traced through adjacent (4-directional) cells without reusing any cell within the same word.

> [!info] Approach
> - **WHY:** Searching the board independently for each word is O(W × M × 4 × 3^(L-1)) where W = words, M = board cells, L = max word length. The trie prunes entire word subtrees: if the current board path matches no trie prefix, stop immediately — shared prefixes across words are explored only once.
> - **WHAT:** Trie of all target words. DFS from every board cell; at each step check if the current character exists in the current trie node's children.
> - **HOW:** Build trie, storing the actual word string at `is_end` nodes. DFS: if `ch` not in `node.children`, return immediately. If `node.word` is set, record and clear it (deduplication). Mark cell as `'#'` during DFS; restore on backtrack. After DFS, prune dead trie nodes (`del node.children[ch]` when subtree is empty) to avoid re-exploring exhausted branches.

> [!note]- Python Solution
> ```python
> class WSNode:
>     def __init__(self) -> None:
>         self.children: dict[str, WSNode] = {}
>         self.word: str | None = None   # stores the full word at the end node
> 
> def findWords(board: list[list[str]], words: list[str]) -> list[str]:
>     root = WSNode()
>     for w in words:
>         node = root
>         for c in w:
>             node = node.children.setdefault(c, WSNode())
>         node.word = w
> 
>     rows, cols = len(board), len(board[0])
>     result: list[str] = []
> 
>     def dfs(node: WSNode, r: int, c: int) -> None:
>         ch = board[r][c]
>         if ch not in node.children:
>             return
>         next_node = node.children[ch]
>         if next_node.word:
>             result.append(next_node.word)
>             next_node.word = None   # deduplicate: clear so same word isn't found again
>         board[r][c] = '#'   # mark visited
>         for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
>                 dfs(next_node, nr, nc)
>         board[r][c] = ch   # restore
>         # prune empty subtree — critical for performance
>         if not next_node.children and not next_node.word:
>             del node.children[ch]
> 
>     for r in range(rows):
>         for c in range(cols):
>             dfs(root, r, c)
>     return result
> ```

> [!success] Complexity
> Time O(M × 4 × 3^(L-1)) where M = board cells, L = max word length — 3 because after the first step, the cell we came from is marked visited (not 4). Trie pruning makes this much faster in practice. Space O(W × L) for trie.

> [!tip] Alternatives
> - DFS per word: O(W × M × 3^L) — no shared prefix benefit.
> - BFS per word: BFS doesn't naturally handle the "no cell reuse per word" constraint — DFS + backtracking is the fit.

---

### Word Squares

> [!example] Problem
> Given a list of words (all same length), find all word squares. A word square is a set of words where the k-th row and k-th column form the same string.

> [!info] Approach
> - **WHY:** At row `k` of a partial word square, the k-th column of all previously placed words determines the prefix that the next word must start with. A trie makes it O(L) to enumerate all words matching that prefix.
> - **WHAT:** Trie with word lists cached at each node (all words reachable from that node). Backtracking over rows, using column-prefix constraints to look up candidates.
> - **HOW:** Build trie; at each node store all words whose prefix passes through it (`node.words`). Backtrack row by row: at row `k`, the required prefix = `square[0][k] + square[1][k] + ... + square[k-1][k]` (k-th column of already-placed words). Look up all words with that prefix in the trie. Try each as `square[k]`; recurse to row `k+1`. Base case: `len(square) == word_length` → record result.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def wordSquares(words: list[str]) -> list[list[str]]:
>     n = len(words[0]) if words else 0
>     # trie: prefix → list of matching words
>     prefix_map: dict[str, list[str]] = defaultdict(list)
>     for w in words:
>         for i in range(len(w) + 1):
>             prefix_map[w[:i]].append(w)
> 
>     result: list[list[str]] = []
> 
>     def backtrack(square: list[str]) -> None:
>         if len(square) == n:
>             result.append(square[:])
>             return
>         k = len(square)
>         # k-th column prefix = chars at position k from each placed word
>         col_prefix = "".join(row[k] for row in square)
>         for candidate in prefix_map[col_prefix]:
>             square.append(candidate)
>             backtrack(square)
>             square.pop()
> 
>     for word in words:
>         backtrack([word])
>     return result
> ```

> [!success] Complexity
> Time O(N × L × N^L) worst case (N = vocab size, L = word length) — heavily pruned by prefix constraint. Space O(N × L) for prefix map.

> [!tip] Alternatives
> - Pure backtracking without trie: generate all permutations and check validity — exponential without pruning.
> - DFS with trie node traversal instead of prefix_map: avoids building separate dict, same O(L) prefix lookup.

---

## XOR Trie

### Maximum XOR of Two Numbers in an Array

> [!example] Problem
> Given an integer array, find the maximum XOR value of any two elements.

> [!info] Approach
> - **WHY:** Brute force is O(n²). XOR is maximized bit by bit from the MSB. A binary trie lets us greedily pick the opposite bit at each level, constructing the maximum XOR in O(32) per element after O(32n) build.
> - **WHAT:** Binary trie where each number is inserted bit by bit from bit 31 (MSB) to bit 0. For each number, greedily navigate the trie choosing the opposite bit to maximize XOR contribution at each level.
> - **HOW:** `insert(num)`: for bits 31 → 0, compute `b = (num >> bit) & 1`, follow or create the `b` branch. `max_xor(num)`: for each bit, try to go to `1 - b` (opposite = XOR bit = 1); if that branch exists, take it and add `1 << bit` to the XOR; otherwise take the `b` branch. Build the trie with all numbers, then query each number for its best XOR pair.

> [!note]- Python Solution
> ```python
> class XORNode:
>     def __init__(self) -> None:
>         self.children: dict[int, XORNode] = {}
> 
> class XORTrie:
>     def __init__(self) -> None:
>         self.root = XORNode()
> 
>     def insert(self, num: int) -> None:
>         node = self.root
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             if b not in node.children:
>                 node.children[b] = XORNode()
>             node = node.children[b]
> 
>     def max_xor(self, num: int) -> int:
>         node = self.root
>         xor = 0
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             want = 1 - b   # opposite bit maximizes XOR at this position
>             if want in node.children:
>                 xor |= (1 << bit)
>                 node = node.children[want]
>             else:
>                 node = node.children[b]
>         return xor
> 
> def findMaximumXOR(nums: list[int]) -> int:
>     trie = XORTrie()
>     for n in nums:
>         trie.insert(n)
>     return max(trie.max_xor(n) for n in nums)
> ```

> [!success] Complexity
> Time O(32n) = O(n). Space O(32n) = O(n).

> [!tip] Alternatives
> - Brute force O(n²): try all pairs — correct, too slow for large inputs.
> - Prefix XOR + hash set: for each bit from MSB, assume that bit can be 1 in the answer, check if the required pair exists using a prefix hash set — O(32n), same complexity, no trie, harder to reason about.

---

## Miscellaneous

### Number of Distinct Substrings in a String

> [!example] Problem
> Given string `s`, return the number of distinct non-empty substrings.

> [!info] Approach
> - **WHY:** Every substring `s[i..j]` corresponds to a unique path in the suffix trie. The number of distinct substrings equals the number of edges in the suffix trie (each edge = one new character extending a unique prefix). Building the full suffix trie is O(n²) nodes but straightforward to count.
> - **WHAT:** Insert all suffixes `s[i:]` for i in 0..n-1 into a trie. Each new node created during all insertions corresponds to one new distinct substring. Total new nodes = answer.
> - **HOW:** Start with an empty trie. For each suffix, insert it — count the number of new nodes created. The total count is the number of distinct substrings. (Equivalently: total nodes in the trie minus the root.)

> [!note]- Python Solution
> ```python
> class DSNode:
>     def __init__(self) -> None:
>         self.children: dict[str, DSNode] = {}
> 
> def countDistinctSubstrings(s: str) -> int:
>     root = DSNode()
>     count = 0
>     for i in range(len(s)):
>         node = root
>         for c in s[i:]:
>             if c not in node.children:
>                 node.children[c] = DSNode()
>                 count += 1   # new node = new distinct substring
>             node = node.children[c]
>     return count
> ```

> [!success] Complexity
> Time O(n²) — n suffixes, each up to length n. Space O(n²) — the suffix trie has O(n²) nodes in the worst case (all characters distinct).

> [!tip] Alternatives
> - Suffix array + LCP array: O(n log n) build. Number of distinct substrings = `n*(n+1)/2 - sum(LCP)`. Optimal for large strings but complex to implement.
> - Rolling hash: generate all O(n²) substrings, hash each — O(n²) time with O(n²) hash set. Same complexity as suffix trie approach but no shared-prefix benefit.
> - Suffix automaton (SAM): O(n) time and space — each state represents a set of substrings; number of distinct substrings = sum over all states of `(len[state] - len[link[state]])`. Most efficient, highly complex to implement.

---

## Aho-Corasick — Multi-Pattern Matching

### Aho-Corasick Algorithm (Conceptual + Implementation)

> [!example] Problem
> Given a text and a dictionary of patterns, find all occurrences of all patterns in the text simultaneously in O(n + m + z) where n = text length, m = total pattern length, z = number of matches.

> [!info] Approach
> - **WHY:** KMP handles one pattern in O(n+m). For k patterns, naive KMP is O(k*(n+m)). Aho-Corasick builds a single automaton from all patterns and runs one pass over text — O(n + total_pattern_length + matches).
> - **WHAT:** Build a Trie from all patterns. Add "failure links" (like KMP failure function) between Trie nodes — when a match fails at node v, follow failure link to the longest proper suffix of the current string that is also a prefix of some pattern. Add "output links" to capture multi-pattern matches at each node.
> - **HOW:**
>   1. Insert all patterns into Trie.
>   2. BFS to build failure links: root's children fail back to root. For node v reached from parent p via char c: `failure[v] = goto[failure[p]][c]` if that child exists, else root.
>   3. Build output links: `output[v]` = patterns ending at v + `output[failure[v]]`.
>   4. Search: start at root. For each char in text: follow goto or failure links. At each node, report all matches via output links.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class AhoCorasick:
>     def __init__(self) -> None:
>         # Each node: children dict, failure link, output list (pattern indices ending here)
>         self.goto: list[dict[str, int]] = [{}]   # goto[state][char] = next_state
>         self.fail: list[int] = [0]
>         self.output: list[list[int]] = [[]]       # output[state] = list of pattern indices
>         self.patterns: list[str] = []
> 
>     def _new_state(self) -> int:
>         self.goto.append({})
>         self.fail.append(0)
>         self.output.append([])
>         return len(self.goto) - 1
> 
>     def add_pattern(self, pattern: str) -> None:
>         idx = len(self.patterns)
>         self.patterns.append(pattern)
>         state = 0
>         for c in pattern:
>             if c not in self.goto[state]:
>                 self.goto[state][c] = self._new_state()
>             state = self.goto[state][c]
>         self.output[state].append(idx)
> 
>     def build(self) -> None:
>         """BFS to compute failure links and propagate output links."""
>         q: deque[int] = deque()
>         # Root's immediate children fail back to root
>         for c, s in self.goto[0].items():
>             self.fail[s] = 0
>             q.append(s)
>         while q:
>             r = q.popleft()
>             for c, s in self.goto[r].items():
>                 q.append(s)
>                 # Walk failure links of r to find where c leads
>                 f = self.fail[r]
>                 while f != 0 and c not in self.goto[f]:
>                     f = self.fail[f]
>                 self.fail[s] = self.goto[f].get(c, 0)
>                 if self.fail[s] == s:
>                     self.fail[s] = 0
>                 # Propagate output: patterns matching at failure link also match here
>                 self.output[s] = self.output[s] + self.output[self.fail[s]]
> 
>     def search(self, text: str) -> list[tuple[int, str]]:
>         """Returns list of (end_index, pattern) for all matches."""
>         results: list[tuple[int, str]] = []
>         state = 0
>         for i, c in enumerate(text):
>             # Follow failure links until a valid transition is found
>             while state != 0 and c not in self.goto[state]:
>                 state = self.fail[state]
>             state = self.goto[state].get(c, 0)
>             for pat_idx in self.output[state]:
>                 pat = self.patterns[pat_idx]
>                 results.append((i - len(pat) + 1, pat))
>         return results
> 
> # Usage
> ac = AhoCorasick()
> for p in ["he", "she", "his", "hers"]:
>     ac.add_pattern(p)
> ac.build()
> print(ac.search("ahishers"))
> # [(1, 'his'), (3, 'she'), (3, 'hers'), (6, 'he'), ...]  (order may vary)
> ```

> [!success] Complexity
> Build O(total_pattern_chars × alphabet_size) for goto table; BFS failure links O(total_pattern_chars). Search O(text_length + matches). Overall O(n + m + z).

> [!tip] Alternatives
> - KMP per pattern: O(k × (n + m)) — simpler, correct, but linear in number of patterns.
> - Rabin-Karp multi-pattern: O(n × k) average with hash collisions — no worst-case guarantee.
> - Suffix automaton: O(n) build on text, O(m) query per pattern — different use case (fixed text, varying patterns).

---

### Multi String Search (AlgoExpert / similar)

> [!example] Problem
> Given a big string and an array of small strings, return a list of booleans indicating whether each small string appears as a substring in the big string.

> [!info] Approach
> - **WHY:** Naive approach: for each small string, run Python's `in` operator — O(b × s × len(small)) total. Aho-Corasick scans the big string once — O(b + total_small_chars + matches). For large inputs with many patterns, this is the optimal approach.
> - **WHAT:** Build an Aho-Corasick automaton from all small strings. Search the big string once. Any pattern found is marked True.
> - **HOW:** vs. Word Search II (Trie + DFS on a 2D grid): that problem requires path-tracing on a grid, so Trie + DFS/backtracking is the fit. This problem is linear text search — Aho-Corasick is direct.

> [!note]- Python Solution
> ```python
> def multiStringSearch(bigString: str, smallStrings: list[str]) -> list[bool]:
>     ac = AhoCorasick()
>     for s in smallStrings:
>         ac.add_pattern(s)
>     ac.build()
> 
>     found: set[str] = set()
>     for _, pat in ac.search(bigString):
>         found.add(pat)
> 
>     return [s in found for s in smallStrings]
> ```

> [!success] Complexity
> Build O(total_small_chars). Search O(len(bigString) + matches). Total O(b + m + z) where b = big string length, m = sum of small string lengths, z = total matches.

> [!tip] Alternatives
> - Per-string search: O(b × k) with Python `in` — acceptable for small k, degrades linearly.
> - Trie + suffix walk: build a Trie of small strings, walk each suffix of bigString — O(b² + m) build+search, worse than Aho-Corasick.

---

## See Also

[[string-algorithms]] | [[backtracking]] | [[hashing]]
