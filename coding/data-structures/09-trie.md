---
tags: [coding, data-structures, trie]
topic: Trie
difficulty: mixed
---

# Trie Problems

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop. Do not move on until these are reflexive.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Highly probable; know the core patterns cold. Edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Know what it is conceptually; skip deep implementation practice.


Pattern tags: trie insert/search, prefix search, backtracking, XOR trie, suffix trie.




---

## Core Trie Implementation

### Implement Trie (Prefix Tree) `⚡ T1`

> [!example] Problem
> A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.
> Implement the Trie class
> 
> **Example 1:**
> ```
> Input
> ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
> [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
> Output
> [null, null, true, false, true, null, true]
> 
> Explanation
> Trie trie = new Trie();
> trie.insert("apple");
> trie.search("apple");   // return True
> trie.search("app");     // return False
> trie.startsWith("app"); // return True
> trie.insert("app");
> trie.search("app");     // return True
> ```
> 
> **Constraints:**
> - 1 <= word.length, prefix.length <= 2000
> - word and prefix consist only of lowercase English letters.
> - At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.

> [!info] Approach
> A hash set gives O(L) exact match but cannot answer "does any word start with prefix X?" without scanning all keys — O(N × L). A Trie shares common prefixes as tree paths, enabling O(L) prefix queries regardless of dictionary size N. N-ary tree where each edge carries one character. Each node holds a `children` dict and an `is_end` flag. The path from root to any node marked `is_end = True` spells a complete word.

>   - `insert`: walk the tree character by character, creating nodes as needed, set `is_end = True` at the last character.
>   - `search`: walk the tree; return False if any character is missing; return `node.is_end` at the end — this distinguishes "apple" (exact) from "app" (only prefix).
>   - `startsWith`: same walk as search but return True after the walk completes regardless of `is_end`.
> - **EDGE CASES:** The empty string is valid only if you explicitly mark the root as terminal; duplicate inserts are idempotent with a boolean trie; deletes must prune only dead branches so shared prefixes stay intact.

> [!note]- Python Solution
> ```python
> class TrieNode:
>     def __init__(self):
>         self.children: dict[str, TrieNode] = {}
>         self.is_end: bool = False
> 
> class Trie:
>     def __init__(self):
>         self.root = TrieNode()
> 
>     def insert(self, word):
>         node = self.root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = TrieNode()
>             node = node.children[c]
>         node.is_end = True
> 
>     def search(self, word):
>         node = self._walk(word)
>         return node is not None and node.is_end
> 
>     def starts_with(self, prefix):
>         return self._walk(prefix) is not None
> 
>     def _walk(self, s):
>         node = self.root
>         for c in s:
>             if c not in node.children:
>                 return None
>             node = node.children[c]
>         return node
> 
>     def delete(self, word):
>         """Remove word; prune dead branches. Returns True if word existed."""
>         def _del(node, depth):
>             if depth == len(word):
>                 if not node.is_end:
>                     return False, False
>                 node.is_end = False
>                 return True, len(node.children) == 0   # safe to prune if leaf
>             c = word[depth]
>             if c not in node.children:
>                 return False, False
>             existed, should_prune_child = _del(node.children[c], depth + 1)
>             if should_prune_child:
>                 del node.children[c]
>             return existed, not node.is_end and len(node.children) == 0
>         existed, _ = _del(self.root, 0)
>         return existed
> ```

> [!success] Complexity
> Time O(L) per operation where L = word/prefix length. Space O(total stored characters) with `dict` children, or O(nodes × Σ) with a fixed child array. If the alphabet is sparse or unknown, `dict` is usually the right tradeoff.

> [!tip] Alternatives
> - Hash set: O(L) exact search, O(N × L) prefix scan — no true prefix query support.
> - Sorted list + binary search: O(log N) prefix range, O(N) insert — no O(L) guarantee.
> - Fixed `children[26]` array instead of dict: faster constant (array index vs hash), but 26× memory waste for sparse alphabets.

---

## Autocomplete / Prefix Search

### Design Search Autocomplete System `⚡ T1`

> [!example] Problem
> Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character `'#'`).
> 
> You are given a string array `sentences` and an integer array `times` both of length `n` where `sentences[i]` is a previously typed sentence and `times[i]` is the corresponding number of times the sentence was typed. For each input character except `'#'`, return the top `3` historical hot sentences that have the same prefix as the part of the sentence already typed.
> 
> Here are the specific rules:
> 
> 	
> - The hot degree for a sentence is defined as the number of times a user typed the exactly same sentence before.
> 	
> - The returned top `3` hot sentences should be sorted by hot degree (The first is the hottest one). If several sentences have the same hot degree, use ASCII-code order (smaller one appears first).
> 	
> - If less than `3` hot sentences exist, return as many as you can.
> 	
> - When the input is a special character, it means the sentence ends, and in this case, you need to return an empty list.
> 
> Implement the `AutocompleteSystem` class:
> 
> 	
> - `AutocompleteSystem(String[] sentences, int[] times)` Initializes the object with the `sentences` and `times` arrays.
> 	`List<String> input(char c)` This indicates that the user typed the character `c`.
> 	
> 		
> - Returns an empty array `[]` if `c == '#'` and stores the inputted sentence in the system.
> 		
> - Returns the top `3` historical hot sentences that have the same prefix as the part of the sentence already typed. If there are fewer than `3` matches, return them all.
> 	
> 	
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input**
> ["AutocompleteSystem", "input", "input", "input", "input"]
> [[["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]], ["i"], [" "], ["a"], ["#"]]
> **Output**
> [null, ["i love you", "island", "i love leetcode"], ["i love you", "i love leetcode"], [], []]
> 
> **Explanation**
> AutocompleteSystem obj = new AutocompleteSystem(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]);
> obj.input("i"); // return ["i love you", "island", "i love leetcode"]. There are four sentences that have prefix "i". Among them, "ironman" and "i love leetcode" have same hot degree. Since ' ' has ASCII code 32 and 'r' has ASCII code 114, "i love leetcode" should be in front of "ironman". Also we only need to output top 3 hot sentences, so "ironman" will be ignored.
> obj.input(" "); // return ["i love you", "i love leetcode"]. There are only two sentences that have prefix "i ".
> obj.input("a"); // return []. There are no sentences that have prefix "i a".
> obj.input("#"); // return []. The user finished the input, the sentence "i a" should be saved as a historical sentence in system. And the following input will be counted as a new search.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `n == sentences.length`
> 	
> - `n == times.length`
> 	
> - `1 <= n <= 100`
> 	
> - `1 <= sentences[i].length <= 100`
> 	
> - `1 <= times[i] <= 50`
> 	
> - `c` is a lowercase English letter, a hash `'#'`, or space `' '`.
> 	
> - Each tested sentence will be a sequence of characters `c` that end with the character `'#'`.
> 	
> - Each tested sentence will have a length in the range `[1, 200]`.
> 	
> - The words in each input sentence are separated by single spaces.
> 	
> - At most `5000` calls will be made to `input`.

> [!info] Approach
> Running a full DFS from the prefix node on every keystroke is O(output) per character — acceptable, but storing top-k cached at each node avoids DFS entirely at query time. Trie where each node stores a `counts` dict mapping `sentence → frequency` for all sentences whose prefix passes through this node. Query stays local to the matched prefix node; this simpler version sorts only that node's candidate bucket. On `insert(sentence, freq)`: walk each character; at each node update `node.counts[sentence] += freq`. On `input(c)`: if `'#'`, save the current input with frequency 1 (updating all ancestor nodes), reset state. Otherwise, advance `curr_node` by one character and return the top 3 sentences from `curr_node.counts`, ordered by `(-frequency, sentence)`.


> [!note]- Python Solution
> ```python
> class ACNode:
>     def __init__(self):
>         self.children: dict[str, ACNode] = {}
>         self.counts: dict[str, int] = {}   # sentence → freq for all sentences through this node
> 
> class AutocompleteSystem:
>     def __init__(self, sentences, times):
>         self.root = ACNode()
>         self.curr_node: ACNode | None = self.root
>         self.curr_input: list[str] = []
>         for s, t in zip(sentences, times):
>             self._insert(s, t)
> 
>     def _insert(self, sentence, freq):
>         node = self.root
>         for c in sentence:
>             if c not in node.children:
>                 node.children[c] = ACNode()
>             node = node.children[c]
>             node.counts[sentence] = node.counts.get(sentence, 0) + freq
> 
>     def input(self, c):
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
> Design a map that allows you to do the following:
> Implement the MapSum class
> 
> **Example 1:**
> ```
> Input
> ["MapSum", "insert", "sum", "insert", "sum"]
> [[], ["apple", 3], ["ap"], ["app", 2], ["ap"]]
> Output
> [null, null, 3, null, 5]
> 
> Explanation
> MapSum mapSum = new MapSum();
> mapSum.insert("apple", 3);  
> mapSum.sum("ap");           // return 3 (apple = 3)
> mapSum.insert("app", 2);    
> mapSum.sum("ap");           // return 5 (apple + app = 3 + 2 = 5)
> ```
> 
> **Constraints:**
> - 1 <= key.length, prefix.length <= 50
> - key and prefix consist of only lowercase English letters.
> - 1 <= val <= 1000
> - At most 50 calls will be made to insert and sum.

> [!info] Approach
> A trie propagates prefix sums naturally — each node on the insertion path of a key can accumulate that key's value. `sum(prefix)` then just reads the accumulated value at the prefix endpoint. Trie where each node stores `prefix_sum` = sum of all values of keys passing through this node. On `insert(key, val)`: if key already exists, compute `delta = val - old_val` to avoid double-counting. Walk each character of key; at each node add `delta` to `node.prefix_sum`. On `sum(prefix)`: walk to the prefix node and return `node.prefix_sum`.


> [!note]- Python Solution
> ```python
> class MSNode:
>     def __init__(self):
>         self.children: dict[str, MSNode] = {}
>         self.prefix_sum: int = 0
> 
> class MapSum:
>     def __init__(self):
>         self.root = MSNode()
>         self.key_map: dict[str, int] = {}   # tracks inserted key values
> 
>     def insert(self, key, val):
>         delta = val - self.key_map.get(key, 0)
>         self.key_map[key] = val
>         node = self.root
>         for c in key:
>             if c not in node.children:
>                 node.children[c] = MSNode()
>             node = node.children[c]
>             node.prefix_sum += delta
> 
>     def sum(self, prefix):
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
> Given an array of strings words representing an English Dictionary, return the longest word in words that can be built one character at a time by other words in words.
> If there is more than one possible answer, return the longest word with the smallest lexicographical order. If there is no answer, return the empty string.
> Note that the word should be built from left to right with each additional character being added to the end of a previous word.
> 
> **Example 1:**
> ```
> Input: words = ["w","wo","wor","worl","world"]
> Output: "world"
> Explanation: The word "world" can be built one character at a time by "w", "wo", "wor", and "worl".
> ```
> 
> **Example 2:**
> ```
> Input: words = ["a","banana","app","appl","ap","apply","apple"]
> Output: "apple"
> Explanation: Both "apply" and "apple" can be built from other words in the dictionary. However, "apple" is lexicographically smaller than "apply".
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 1000
> - 1 <= words[i].length <= 30
> - words[i] consists of lowercase English letters.

> [!info] Approach
> "Each prefix must also be in the dictionary" maps exactly to "each ancestor in the trie must have `is_end = True`". Trie lets us enforce this constraint during a BFS/DFS traversal. Insert all words. Then traverse the trie only through nodes with `is_end = True` (the root is the empty prefix — treat it as `is_end = True` for traversal purposes). Track the longest path reached. Insert all words. BFS from root — only enqueue child nodes where `is_end = True`. At each node, track the current word. Update the answer when a longer (or lexicographically smaller tie) word is found.


> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class LWNode:
>     def __init__(self):
>         self.children: dict[str, LWNode] = {}
>         self.is_end: bool = False
>         self.word: str = ""
> 
> class Solution:
>     def longest_word(self, words):
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

### Replace Words `⚡ T1`

> [!example] Problem
> In English, we have a concept called root, which can be followed by some other word to form another longer word - let's call this word derivative. For example, when the root "help" is followed by the word "ful", we can form a derivative "helpful".
> Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace all the derivatives in the sentence with the root forming it. If a derivative can be replaced by more than one root, replace it with the root that has the shortest length.
> Return the sentence after the replacement.
> 
> **Example 1:**
> ```
> Input: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
> Output: "the cat was rat by the bat"
> ```
> 
> **Example 2:**
> ```
> Input: dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
> Output: "a a b c"
> ```
> 
> **Constraints:**
> - 1 <= dictionary.length <= 1000
> - 1 <= dictionary[i].length <= 100
> - dictionary[i] consists of only lower-case letters.
> - 1 <= sentence.length <= 10^6
> - sentence consists of only lower-case letters and spaces.
> - The number of words in sentence is in the range [1, 1000]
> - The length of each word in sentence is in the range [1, 1000]
> - Every two consecutive words in sentence will be separated by exactly one space.
> - sentence does not have leading or trailing spaces.

> [!info] Approach
> For each word in the sentence, we need to find the shortest dictionary root that is a prefix of that word. A trie answers "what is the shortest prefix of this string that exists in the dictionary?" in O(L) — walk until the first `is_end` node. Trie of all root words. For each sentence word, walk the trie character by character — return as soon as `is_end` is hit (shortest root match). Insert all roots into the trie. For each word in the sentence, walk the trie; if `is_end` is reached at depth `d`, replace the word with `word[:d]`. If the walk exits without finding a root, keep the original word.


> [!note]- Python Solution
> ```python
> class RWNode:
>     def __init__(self):
>         self.children: dict[str, RWNode] = {}
>         self.is_end: bool = False
> 
> def replace_words(dictionary, sentence):
>     root = RWNode()
>     for word in dictionary:
>         node = root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = RWNode()
>             node = node.children[c]
>         node.is_end = True
> 
>     def replace(word):
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

### Word Search II `⚡ T1`

> [!example] Problem
> Given an m x n board of characters and a list of strings words, return all words on the board.
> Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
> 
> **Example 1:**
> ```
> Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
> Output: ["eat","oath"]
> ```
> 
> **Example 2:**
> ```
> Input: board = [["a","b"],["c","d"]], words = ["abcb"]
> Output: []
> ```
> 
> **Constraints:**
> - m == board.length
> - n == board[i].length
> - 1 <= m, n <= 12
> - board[i][j] is a lowercase English letter.
> - 1 <= words.length <= 3 * 10^4
> - 1 <= words[i].length <= 10
> - words[i] consists of lowercase English letters.
> - All the strings of words are unique.

> [!info] Approach
> Searching the board independently for each word is O(W × M × 4 × 3^(L-1)) where W = words, M = board cells, L = max word length. The trie prunes entire word subtrees: if the current board path matches no trie prefix, stop immediately — shared prefixes across words are explored only once. Trie of all target words. DFS from every board cell; at each step check if the current character exists in the current trie node's children. Build trie, storing the actual word string at `is_end` nodes. DFS: if `ch` not in `node.children`, return immediately. If `node.word` is set, record and clear it (deduplication). Mark cell as `'#'` during DFS; restore on backtrack. After DFS, prune dead trie nodes (`del node.children[ch]` when subtree is empty) to avoid re-exploring exhausted branches.


> [!note]- Python Solution
> ```python
> class WSNode:
>     def __init__(self):
>         self.children: dict[str, WSNode] = {}
>         self.word: str | None = None   # stores the full word at the end node
> 
> def find_words(board, words):
>     root = WSNode()
>     for w in words:
>         node = root
>         for c in w:
>             node = node.children.setdefault(c, WSNode())
>         node.word = w
> 
>     rows, cols = len(board), len(board[0])
>     result = []
> 
>     def dfs(node, r, c):
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
> Given an array of **unique `🎯 T2`** strings `words`, return *all the ***[word squares](https://en.wikipedia.org/wiki/Word_square)*** you can build from *`words`. The same word from `words` can be used **multiple times**. You can return the answer in **any order**.
> 
> A sequence of strings forms a valid **word square** if the `k^th` row and column read the same string, where `0 <= k < max(numRows, numColumns)`.
> 
> 	
> - For example, the word sequence `["ball","area","lead","lady"]` forms a word square because each word reads the same both horizontally and vertically.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** words = ["area","lead","wall","lady","ball"]
> **Output:** [["ball","area","lead","lady"],["wall","area","lead","lady"]]
> **Explanation:**
> The output consists of two word squares. The order of output does not matter (just the order of words in each word square matters).
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** words = ["abat","baba","atan","atal"]
> **Output:** [["baba","abat","baba","atal"],["baba","abat","baba","atan"]]
> **Explanation:**
> The output consists of two word squares. The order of output does not matter (just the order of words in each word square matters).
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= words.length <= 1000`
> 	
> - `1 <= words[i].length <= 4`
> 	
> - All `words[i]` have the same length.
> 	
> - `words[i]` consists of only lowercase English letters.
> 	
> - All `words[i]` are **unique `🎯 T2`**.

> [!info] Approach
> At row `k` of a partial word square, the k-th column of all previously placed words determines the prefix that the next word must start with. A trie makes it O(L) to enumerate all words matching that prefix. Trie with word lists cached at each node (all words reachable from that node). Backtracking over rows, using column-prefix constraints to look up candidates. Build trie; at each node store all words whose prefix passes through it (`node.words`). Backtrack row by row: at row `k`, the required prefix = `square[0][k] + square[1][k] + ... + square[k-1][k]` (k-th column of already-placed words). Look up all words with that prefix in the trie. Try each as `square[k]`; recurse to row `k+1`. Base case: `len(square) == word_length` → record result.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def word_squares(words):
>     n = len(words[0]) if words else 0
>     # trie: prefix → list of matching words
>     prefix_map = defaultdict(list)
>     for w in words:
>         for i in range(len(w) + 1):
>             prefix_map[w[:i]].append(w)
> 
>     result = []
> 
>     def backtrack(square):
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

### Maximum XOR of Two Numbers in an Array `⚡ T1`

> [!example] Problem
> Given an integer array nums, return the maximum result of nums[i] XOR nums[j], where 0 <= i <= j < n.
> 
> **Example 1:**
> ```
> Input: nums = [3,10,5,25,2,8]
> Output: 28
> Explanation: The maximum result is 5 XOR 25 = 28.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [14,70,53,83,49,91,36,80,92,51,66,70]
> Output: 127
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^5
> - 0 <= nums[i] <= 2^{31} - 1

> [!info] Approach
> Brute force is O(n²). XOR is maximized bit by bit from the MSB. A binary trie lets us greedily pick the opposite bit at each level, constructing the maximum XOR in O(32) per element after O(32n) build. Binary trie where each number is inserted bit by bit from bit 31 (MSB) to bit 0. For each number, greedily navigate the trie choosing the opposite bit to maximize XOR contribution at each level. `insert(num)`: for bits 31 → 0, compute `b = (num >> bit) & 1`, follow or create the `b` branch. `max_xor(num)`: for each bit, try to go to `1 - b` (opposite = XOR bit = 1); if that branch exists, take it and add `1 << bit` to the XOR; otherwise take the `b` branch. Build the trie with all numbers, then query each number for its best XOR pair.


> [!note]- Python Solution
> ```python
> class XORNode:
>     def __init__(self):
>         self.children: dict[int, XORNode] = {}
> 
> class XORTrie:
>     def __init__(self):
>         self.root = XORNode()
> 
>     def insert(self, num):
>         node = self.root
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             if b not in node.children:
>                 node.children[b] = XORNode()
>             node = node.children[b]
> 
>     def max_xor(self, num):
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
> def find_maximum_xor(nums):
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
> Given a string `s`, return *the number of **distinct `🎯 T2`** substrings of* `s`.
> 
> A **substring** of a string is obtained by deleting any number of characters (possibly zero) from the front of the string and any number (possibly zero) from the back of the string.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** s = "aabbaba"
> **Output:** 21
> **Explanation:** The set of distinct strings is ["a","b","aa","bb","ab","ba","aab","abb","bab","bba","aba","aabb","abba","bbab","baba","aabba","abbab","bbaba","aabbab","abbaba","aabbaba"]
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** s = "abcdefg"
> **Output:** 28
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= s.length <= 500`
> 	
> - `s` consists of lowercase English letters.
> 
>  
> 
> **Follow up:** Can you solve this problem in `O(n)` time complexity?

> [!info] Approach
> Every substring `s[i..j]` corresponds to a unique path in the suffix trie. The number of distinct substrings equals the number of edges in the suffix trie (each edge = one new character extending a unique prefix). Building the full suffix trie is O(n²) nodes but straightforward to count. Insert all suffixes `s[i:]` for i in 0..n-1 into a trie. Each new node created during all insertions corresponds to one new distinct substring. Total new nodes = answer. Start with an empty trie. For each suffix, insert it — count the number of new nodes created. The total count is the number of distinct substrings. (Equivalently: total nodes in the trie minus the root.)


> [!note]- Python Solution
> ```python
> class DSNode:
>     def __init__(self):
>         self.children: dict[str, DSNode] = {}
> 
> def count_distinct_substrings(s):
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
> KMP handles one pattern in O(n+m). For k patterns, naive KMP is O(k*(n+m)). Aho-Corasick builds a single automaton from all patterns and runs one pass over text — O(n + total_pattern_length + matches). Build a Trie from all patterns. Add "failure links" (like KMP failure function) between Trie nodes — when a match fails at node v, follow failure link to the longest proper suffix of the current string that is also a prefix of some pattern. Add "output links" to capture multi-pattern matches at each node.

>   1. Insert all patterns into Trie.
>   2. BFS to build failure links: root's children fail back to root. For node v reached from parent p via char c: `failure[v] = goto[failure[p]][c]` if that child exists, else root.
>   3. Build output links: `output[v]` = patterns ending at v + `output[failure[v]]`.
>   4. Search: start at root. For each char in text: follow goto or failure links. At each node, report all matches via output links.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> class AhoCorasick:
>     def __init__(self):
>         # Each node: children dict, failure link, output list (pattern indices ending here)
>         self.goto: list[dict[str, int]] = [{}]   # goto[state][char] = next_state
>         self.fail: list[int] = [0]
>         self.output: list[list[int]] = [[]]       # output[state] = list of pattern indices
>         self.patterns: list[str] = []
> 
>     def _new_state(self):
>         self.goto.append({})
>         self.fail.append(0)
>         self.output.append([])
>         return len(self.goto) - 1
> 
>     def add_pattern(self, pattern):
>         idx = len(self.patterns)
>         self.patterns.append(pattern)
>         state = 0
>         for c in pattern:
>             if c not in self.goto[state]:
>                 self.goto[state][c] = self._new_state()
>             state = self.goto[state][c]
>         self.output[state].append(idx)
> 
>     def build(self):
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
>     def search(self, text):
>         """Returns list of (end_index, pattern) for all matches."""
>         results = []
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
> Naive approach: for each small string, run Python's `in` operator — O(b × s × len(small)) total. Aho-Corasick scans the big string once — O(b + total_small_chars + matches). For large inputs with many patterns, this is the optimal approach. Build an Aho-Corasick automaton from all small strings. Search the big string once. Any pattern found is marked True. vs. Word Search II (Trie + DFS on a 2D grid): that problem requires path-tracing on a grid, so Trie + DFS/backtracking is the fit. This problem is linear text search — Aho-Corasick is direct.


> [!note]- Python Solution
> ```python
> def multi_string_search(bigString, smallStrings):
>     ac = AhoCorasick()
>     for s in smallStrings:
>         ac.add_pattern(s)
>     ac.build()
> 
>     found = set()
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

## Core Trie Operations (Extended)

### Add and Search Word `⚡ T1`

> [!example] Problem
> Design a data structure with `addWord(word)` and `search(word)`. `search` supports the wildcard character `.` which matches any single letter. Return true if the word (with wildcards) matches any previously added word.

> [!info] Approach
> Exact-match trie search is O(L). The `.` wildcard requires branching — at each `.` we must try all children. A standard trie provides the tree structure needed for this DFS with branching. Standard trie insert. Search becomes a recursive DFS: literal characters follow the exact child; `.` recursively searches all children at the current node. `addWord`: standard trie insert. `search(word, node, i)`: if `i == len(word)` return `node.is_end`. If `word[i] == '.'`, recurse into every child and return True if any succeeds. Otherwise follow the exact child as usual.


> [!note]- Python Solution
> ```python
> class WCNode:
>     def __init__(self):
>         self.children: dict[str, WCNode] = {}
>         self.is_end: bool = False
> 
> class WordDictionary:
>     def __init__(self):
>         self.root = WCNode()
> 
>     def add_word(self, word):
>         node = self.root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = WCNode()
>             node = node.children[c]
>         node.is_end = True
> 
>     def search(self, word):
>         return self._dfs(self.root, word, 0)
> 
>     def _dfs(self, node, word, i):
>         if i == len(word):
>             return node.is_end
>         c = word[i]
>         if c == '.':
>             for child in node.children.values():
>                 if self._dfs(child, word, i + 1):
>                     return True
>             return False
>         if c not in node.children:
>             return False
>         return self._dfs(node.children[c], word, i + 1)
> ```

> [!success] Complexity
> Time O(L) average; O(26^L) worst case for an all-`.` pattern against a full dictionary of L-length words. Space O(N × L) for the trie.

> [!tip] Alternatives
> - Regex: `re.fullmatch` on every stored word — O(N × L) per query. Simple but doesn't scale.
> - Hash map per word length: group words by length; for `.` patterns, scan the right bucket — still O(N × L) per query in the worst case.

---

## Prefix Problems

### Search Suggestions System `⚡ T1`

> [!example] Problem
> You are given an array of strings products and a string searchWord.
> Design a system that suggests at most three product names from products after each character of searchWord is typed. Suggested products should have common prefix with searchWord. If there are more than three products with a common prefix return the three lexicographically minimums products.
> Return a list of lists of the suggested products after each character of searchWord is typed.
> 
> **Example 1:**
> ```
> Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
> Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
> Explanation: products sorted lexicographically = ["mobile","moneypot","monitor","mouse","mousepad"].
> After typing m and mo all products match and we show user ["mobile","moneypot","monitor"].
> After typing mou, mous and mouse the system suggests ["mouse","mousepad"].
> ```
> 
> **Example 2:**
> ```
> Input: products = ["havana"], searchWord = "havana"
> Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
> Explanation: The only word "havana" will be always suggested while typing the search word.
> ```
> 
> **Constraints:**
> - 1 <= products.length <= 1000
> - 1 <= products[i].length <= 3000
> - 1 <= sum(products[i].length) <= 2 * 10^4
> - All the strings of products are unique.
> - products[i] consists of lowercase English letters.
> - 1 <= searchWord.length <= 1000
> - searchWord consists of lowercase English letters.

> [!info] Approach
> After inserting and sorting, a trie lets us walk to the prefix node once and collect the first 3 words in lexicographic order via a bounded DFS — O(prefix_length + output) per query. Insert all products (sorted) into the trie. At each node store up to 3 of the lexicographically smallest words that pass through it (filled at insert time since we sort first). Sort `products`. Insert each: at every node on the path, append the word to `node.suggestions` if `len < 3`. Query: walk the search word prefix character by character; at each step return `node.suggestions` (or `[]` if the branch doesn't exist, and stay dead for subsequent characters).


> [!note]- Python Solution
> ```python
> class SSNode:
>     def __init__(self):
>         self.children: dict[str, SSNode] = {}
>         self.suggestions: list[str] = []
> 
> class Solution:
>     def suggested_products(self, products, searchWord):
>         root = SSNode()
>         for product in sorted(products):
>             node = root
>             for c in product:
>                 if c not in node.children:
>                     node.children[c] = SSNode()
>                 node = node.children[c]
>                 if len(node.suggestions) < 3:
>                     node.suggestions.append(product)
> 
>         result = []
>         node: SSNode | None = root
>         for c in searchWord:
>             if node and c in node.children:
>                 node = node.children[c]
>             else:
>                 node = None
>             result.append(node.suggestions if node else [])
>         return result
> ```

> [!success] Complexity
> Time O(N × L log(N × L)) to sort and insert + O(|searchWord|) to query. Space O(N × L).

> [!tip] Alternatives
> - Binary search on sorted list: for each prefix, binary-search the start and collect next 3 — O(N log N) sort + O(L × log N) query. Simpler, nearly as fast in practice.
> - Two-pointer on sorted array: same idea but with `bisect_left` — O(log N) per prefix.

---

### Prefix and Suffix Search

> [!example] Problem
> Design a special dictionary that searches the words in it by a prefix and a suffix.
> Implement the WordFilter class
> 
> **Example 1:**
> ```
> Input
> ["WordFilter", "f"]
> [[["apple"]], ["a", "e"]]
> Output
> [null, 0]
> Explanation
> WordFilter wordFilter = new WordFilter(["apple"]);
> wordFilter.f("a", "e"); // return 0, because the word at index 0 has prefix = "a" and suffix = "e".
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 10^4
> - 1 <= words[i].length <= 7
> - 1 <= pref.length, suff.length <= 7
> - words[i], pref and suff consist of lowercase English letters only.
> - At most 10^4 calls will be made to the function f.

> [!info] Approach
> Checking all words for every query is O(N × L). We need O(L) query time. The trick: a word `w` matches `f(pref, suff)` iff the combined string `suff + '#' + pref` is a prefix of some inserted `suff + '#' + w`. Build a trie of all `suff + '#' + word` combinations. At every visited node, store the maximum word index seen so far so later words win ties automatically. For each word `words[i]`, insert every suffix of that word followed by `'#'` and the full word. Query `f(pref, suff)` walks `suff + '#' + pref` in the trie and returns the stored max index, or -1 if the path is missing.


> [!note]- Python Solution
> ```python
> class WordFilter:
>     def __init__(self, words):
>         self.root = WFNode()
>         for idx, word in enumerate(words):
>             n = len(word)
>             for k in range(n + 1):
>                 node = self.root
>                 node.idx = idx
>                 for c in word[k:] + '#' + word:
>                     if c not in node.children:
>                         node.children[c] = WFNode()
>                     node = node.children[c]
>                     node.idx = idx   # later word index wins ties automatically
> 
>     def f(self, pref, suff):
>         node = self.root
>         for c in suff + '#' + pref:
>             if c not in node.children:
>                 return -1
>             node = node.children[c]
>         return node.idx
> 
> class WFNode:
>     def __init__(self):
>         self.children: dict[str, WFNode] = {}
>         self.idx: int = -1
> ```

> [!success] Complexity
> Build O(N × L²) — N words, each generates O(L) suffixes, each key is O(L). Query O(L). Space O(N × L²).

> [!tip] Alternatives
> - Trie-based (true trie of `suff#word`): same O(N × L²) build, O(L) query, more memory per node but no Python dict overhead.
> - Pair of tries (prefix trie + suffix trie): intersect candidate sets — O(N × L) build but O(output) query for intersection.

---

### Count Words With Given Prefix

> [!example] Problem
> Given a list of words and a prefix string `pref`, return the number of strings in `words` that contain `pref` as a prefix.

> [!info] Approach
> A trie answers prefix-count queries in O(L) after O(N × L) build — count of words in the subtree rooted at the prefix node. Trie where each node stores `count` = number of words inserted through it (prefix count). Insert each word, incrementing `node.count` at every node on the path. Query: walk `pref`; if the walk succeeds, return `node.count`. If any character is missing, return 0.


> [!note]- Python Solution
> ```python
> class CWNode:
>     def __init__(self):
>         self.children: dict[str, CWNode] = {}
>         self.count: int = 0
> 
> def prefix_count(words, pref):
>     root = CWNode()
>     for word in words:
>         node = root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = CWNode()
>             node = node.children[c]
>             node.count += 1
> 
>     node = root
>     for c in pref:
>         if c not in node.children:
>             return 0
>         node = node.children[c]
>     return node.count
> ```

> [!success] Complexity
> Time O(N × L) build + O(|pref|) query. Space O(N × L).

> [!tip] Alternatives
> - Linear scan: `sum(1 for w in words if w.startswith(pref))` — O(N × L), one-liner, fine for small inputs or one-off queries.

---

### Implement Magic Dictionary

> [!example] Problem
> Design a data structure that is initialized with a list of different words. Provided a string, you should determine if you can change exactly one character in this string to match any word in the data structure.
> Implement the MagicDictionary class
> 
> **Example 1:**
> ```
> Input
> ["MagicDictionary", "buildDict", "search", "search", "search", "search"]
> [[], [["hello", "leetcode"]], ["hello"], ["hhllo"], ["hell"], ["leetcoded"]]
> Output
> [null, null, false, true, false, false]
> 
> Explanation
> MagicDictionary magicDictionary = new MagicDictionary();
> magicDictionary.buildDict(["hello", "leetcode"]);
> magicDictionary.search("hello"); // return False
> magicDictionary.search("hhllo"); // We can change the second 'h' to 'e' to match "hello" so we return True
> magicDictionary.search("hell"); // return False
> magicDictionary.search("leetcoded"); // return False
> ```
> 
> **Constraints:**
> - 1 <= dictionary.length <= 100
> - 1 <= dictionary[i].length <= 100
> - dictionary[i] consists of only lower-case English letters.
> - All the strings in dictionary are distinct.
> - 1 <= searchWord.length <= 100
> - searchWord consists of only lower-case English letters.
> - buildDict will be called only once before search.
> - At most 100 calls will be made to search.

> [!info] Approach
> We need "exactly one substitution" match, not exact or prefix match. A trie DFS lets us track a mismatch counter — proceed only if mismatches ≤ 1, returning True only if we reach `is_end` with exactly 1 mismatch. Standard trie of dictionary words. `search`: recursive DFS passing a `diff` counter (max 1 allowed). At each character, follow exact child (diff unchanged) or any other child (diff += 1, only if diff < 1 before). `_dfs(node, word, i, diff)`: base case `i == len(word)` → return `node.is_end and diff == 1`. At each step: for exact char, recurse with same diff. For all other children, recurse with `diff + 1` (only if `diff == 0`). Return True if any branch returns True.


> [!note]- Python Solution
> ```python
> class MDNode:
>     def __init__(self):
>         self.children: dict[str, MDNode] = {}
>         self.is_end: bool = False
> 
> class MagicDictionary:
>     def __init__(self):
>         self.root = MDNode()
> 
>     def build_dict(self, dictionary):
>         for word in dictionary:
>             node = self.root
>             for c in word:
>                 if c not in node.children:
>                     node.children[c] = MDNode()
>                 node = node.children[c]
>             node.is_end = True
> 
>     def search(self, searchWord):
>         return self._dfs(self.root, searchWord, 0, 0)
> 
>     def _dfs(self, node, word, i, diff):
>         if diff > 1:
>             return False
>         if i == len(word):
>             return node.is_end and diff == 1
>         c = word[i]
>         for ch, child in node.children.items():
>             next_diff = diff + (0 if ch == c else 1)
>             if next_diff <= 1 and self._dfs(child, word, i + 1, next_diff):
>                 return True
>         return False
> ```

> [!success] Complexity
> Time O(N × L) build; O(26 × L) search — at each node we try at most 26 children but with the diff constraint we only branch once. Space O(N × L).

> [!tip] Alternatives
> - For each stored word, count character differences — O(N × L) per query. Simple, no trie needed for small N.
> - Generate all one-off variants of `searchWord` and check membership in a set — O(L × 26) query with O(N × L) build. Equivalent complexity.

---

## XOR Trie (Extended)

### Maximum XOR With an Element From Array

> [!example] Problem
> You are given an array nums consisting of non-negative integers. You are also given a queries array, where queries[i] = [xi, mi].
> The answer to the ith query is the maximum bitwise XOR value of xi and any element of nums that does not exceed mi. In other words, the answer is max(nums[j] XOR xi) for all j such that nums[j] <= mi. If all elements in nums are larger than mi, then the answer is -1.
> Return an integer array answer where answer.length == queries.length and answer[i] is the answer to the ith query.
> 
> **Example 1:**
> ```
> Input: nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
> Output: [3,3,7]
> Explanation:
> 1) 0 and 1 are the only two integers not greater than 1. 0 XOR 3 = 3 and 1 XOR 3 = 2. The larger of the two is 3.
> 2) 1 XOR 2 = 3.
> 3) 5 XOR 2 = 7.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]
> Output: [15,-1,5]
> ```
> 
> **Constraints:**
> - 1 <= nums.length, queries.length <= 10^5
> - queries[i].length == 2
> - 0 <= nums[j], xi, mi <= 10^9

> [!info] Approach
> If we could insert all `nums` freely, a standard XOR trie answers each query in O(32). The constraint `num ≤ mi` complicates things. Offline processing sorts both arrays and inserts elements into the trie incrementally as `mi` increases — this way the trie always contains only valid elements. Sort queries by `mi`. Sort `nums`. Process queries in order; before answering query `(xi, mi)`, insert all `nums[j] ≤ mi` into the XOR trie. Then query the trie for max XOR with `xi`. Sort `nums`. Sort queries by `mi` (keep original index for output). Two pointers: pointer `j` into nums. For each query `(xi, mi)`, advance `j` while `nums[j] <= mi`, inserting into trie. If trie is empty (no `num ≤ mi`), answer is -1. Otherwise query `max_xor(xi)`.


> [!note]- Python Solution
> ```python
> class XNode:
>     def __init__(self):
>         self.children: dict[int, XNode] = {}
> 
> class XORTrie2:
>     def __init__(self):
>         self.root = XNode()
>         self.size = 0
> 
>     def insert(self, num):
>         node = self.root
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             if b not in node.children:
>                 node.children[b] = XNode()
>             node = node.children[b]
>         self.size += 1
> 
>     def max_xor(self, num):
>         node = self.root
>         xor = 0
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             want = 1 - b
>             if want in node.children:
>                 xor |= (1 << bit)
>                 node = node.children[want]
>             else:
>                 node = node.children[b]
>         return xor
> 
> def maximize_xor(nums, queries):
>     nums.sort()
>     indexed_queries = sorted(enumerate(queries), key=lambda x: x[1][1])
>     ans = [-1] * len(queries)
>     trie = XORTrie2()
>     j = 0
>     for orig_idx, (xi, mi) in indexed_queries:
>         while j < len(nums) and nums[j] <= mi:
>             trie.insert(nums[j])
>             j += 1
>         if trie.size > 0:
>             ans[orig_idx] = trie.max_xor(xi)
>     return ans
> ```

> [!success] Complexity
> Time O((N + Q) log(N + Q)) for sorting + O((N + Q) × 32) for trie operations = O((N + Q) log(N + Q)). Space O(N × 32).

> [!tip] Alternatives
> - Brute force per query: O(N × Q) — too slow.
> - Persistent segment tree on sorted values: O(N log V + Q log V) — same complexity, more complex.

---

### Count Pairs With XOR in a Range

> [!example] Problem
> Given a (0-indexed) integer array nums and two integers low and high, return the number of nice pairs.
> A nice pair is a pair (i, j) where 0 <= i < j < nums.length and low <= (nums[i] XOR nums[j]) <= high.
> 
> **Example 1:**
> ```
> Input: nums = [1,4,2,7], low = 2, high = 6
> Output: 6
> Explanation: All nice pairs (i, j) are as follows:
>     - (0, 1): nums[0] XOR nums[1] = 5 
>     - (0, 2): nums[0] XOR nums[2] = 3
>     - (0, 3): nums[0] XOR nums[3] = 6
>     - (1, 2): nums[1] XOR nums[2] = 6
>     - (1, 3): nums[1] XOR nums[3] = 3
>     - (2, 3): nums[2] XOR nums[3] = 5
> ```
> 
> **Example 2:**
> ```
> Input: nums = [9,8,4,2,1], low = 5, high = 14
> Output: 8
> Explanation: All nice pairs (i, j) are as follows:
> ​​​​​    - (0, 2): nums[0] XOR nums[2] = 13
>     - (0, 3): nums[0] XOR nums[3] = 11
>     - (0, 4): nums[0] XOR nums[4] = 8
>     - (1, 2): nums[1] XOR nums[2] = 12
>     - (1, 3): nums[1] XOR nums[3] = 10
>     - (1, 4): nums[1] XOR nums[4] = 9
>     - (2, 3): nums[2] XOR nums[3] = 6
>     - (2, 4): nums[2] XOR nums[4] = 5
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - 1 <= nums[i] <= 2 * 10^4
> - 1 <= low <= high <= 2 * 10^4

> [!info] Approach
> Brute force O(n²). XOR trie allows us to count, for a fixed `num`, how many previously inserted numbers produce XOR < `threshold` in O(32) — so `count_pairs_xor_leq(high) - count_pairs_xor_leq(low - 1)`. Insert numbers one by one. Before inserting `nums[i]`, query the trie for how many existing numbers produce XOR ≤ T with `nums[i]`. The answer is `count(high) - count(low - 1)`. `count_leq(num, limit)`: walk bit by bit from MSB. At each bit `b` of `num` and `l` of `limit`: if `l == 1`, all numbers with XOR bit 0 at this position contribute (they have XOR < current prefix) — add `node.children[b].size` if it exists, then continue down the `1-b` branch to keep XOR bit = 1. If `l == 0`, must go down `b` branch (XOR bit = 0).


> [!note]- Python Solution
> ```python
> class CPNode:
>     def __init__(self):
>         self.children: dict[int, CPNode] = {}
>         self.cnt: int = 0   # numbers passing through this node
> 
> class XORTrieCount:
>     def __init__(self):
>         self.root = CPNode()
> 
>     def insert(self, num):
>         node = self.root
>         for bit in range(14, -1, -1):   # nums[i] <= 2^14
>             b = (num >> bit) & 1
>             if b not in node.children:
>                 node.children[b] = CPNode()
>             node = node.children[b]
>             node.cnt += 1
> 
>     def count_leq(self, num, limit):
>         """Count of inserted numbers x such that num XOR x <= limit."""
>         node = self.root
>         result = 0
>         for bit in range(14, -1, -1):
>             b = (num >> bit) & 1
>             l = (limit >> bit) & 1
>             if l == 1:
>                 # XOR bit = 0 branch: go down b (same bit as num → XOR = 0 < 1)
>                 if b in node.children:
>                     result += node.children[b].cnt
>                 # Continue with XOR bit = 1: go down 1 - b
>                 nxt = 1 - b
>                 if nxt not in node.children:
>                     break
>                 node = node.children[nxt]
>             else:
>                 # Must keep XOR bit = 0: go down b
>                 if b not in node.children:
>                     break
>                 node = node.children[b]
>         else:
>             result += 1   # equal case: num XOR x == limit
>         return result
> 
> def count_pairs(nums, low, high):
>     trie = XORTrieCount()
>     ans = 0
>     for num in nums:
>         ans += trie.count_leq(num, high) - trie.count_leq(num, low - 1)
>         trie.insert(num)
>     return ans
> ```

> [!success] Complexity
> Time O(N × 32). Space O(N × 32).

> [!tip] Alternatives
> - Brute force: O(N²) — correct for small N.
> - Merge sort / divide and conquer: O(N log N × log(max_val)) — more complex, same asymptotic.

---

## Bitwise Trie / Other

### Design File System

> [!example] Problem
> You are asked to design a file system that allows you to create new paths and associate them with different values.
> 
> The format of a path is one or more concatenated strings of the form: `/` followed by one or more lowercase English letters. For example, "`/leetcode"` and "`/leetcode/problems"` are valid paths while an empty string `""` and `"/"` are not.
> 
> Implement the `FileSystem` class:
> 
> 	
> - `bool createPath(string path, int value)` Creates a new `path` and associates a `value` to it if possible and returns `true`. Returns `false` if the path **already exists** or its parent path **doesn't exist**.
> 	
> - `int get(string path)` Returns the value associated with `path` or returns `-1` if the path doesn't exist.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** 
> ["FileSystem","createPath","get"]
> [[],["/a",1],["/a"]]
> **Output:** 
> [null,true,1]
> **Explanation:** 
> FileSystem fileSystem = new FileSystem();
> 
> fileSystem.createPath("/a", 1); // return true
> fileSystem.get("/a"); // return 1
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** 
> ["FileSystem","createPath","createPath","get","createPath","get"]
> [[],["/leet",1],["/leet/code",2],["/leet/code"],["/c/d",1],["/c"]]
> **Output:** 
> [null,true,true,2,false,-1]
> **Explanation:** 
> FileSystem fileSystem = new FileSystem();
> 
> fileSystem.createPath("/leet", 1); // return true
> fileSystem.createPath("/leet/code", 2); // return true
> fileSystem.get("/leet/code"); // return 2
> fileSystem.createPath("/c/d", 1); // return false because the parent path "/c" doesn't exist.
> fileSystem.get("/c"); // return -1 because this path doesn't exist.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `2 <= path.length <= 100`
> 	
> - `1 <= value <= 10^9`
> 	
> - Each `path` is **valid `🎯 T2`** and consists of lowercase English letters and `'/'`.
> 	
> - At most `10^4` calls **in total** will be made to `createPath` and `get`.

> [!info] Approach
> A trie over path components (split by `/`) models the hierarchical file system naturally. `createPath` is insert with a parent-existence check; `get` is lookup. Trie where children keys are path component strings (directory names). Each node stores a `value` (default -1 meaning not created). `createPath(path, value)`: split path by `/`, ignore leading empty string. Walk all but the last component — if any is missing, return False. At the last component, if the node already exists and was explicitly created (value != -1), return False; else create it with the value. `get(path)`: walk all components; return node's value or -1 if path doesn't exist.


> [!note]- Python Solution
> ```python
> class FSNode:
>     def __init__(self):
>         self.children: dict[str, FSNode] = {}
>         self.value: int = -1
> 
> class FileSystem:
>     def __init__(self):
>         self.root = FSNode()
> 
>     def create_path(self, path, value):
>         parts = path.split('/')[1:]   # skip leading empty string from '/'
>         node = self.root
>         for part in parts[:-1]:
>             if part not in node.children:
>                 return False   # parent doesn't exist
>             node = node.children[part]
>         last = parts[-1]
>         if last in node.children and node.children[last].value != -1:
>             return False   # already exists
>         if last not in node.children:
>             node.children[last] = FSNode()
>         node.children[last].value = value
>         return True
> 
>     def get(self, path):
>         parts = path.split('/')[1:]
>         node = self.root
>         for part in parts:
>             if part not in node.children:
>                 return -1
>             node = node.children[part]
>         return node.value
> ```

> [!success] Complexity
> Time O(L) per operation where L = path length (number of components). Space O(N × L) total.

> [!tip] Alternatives
> - Hash map: store full path strings as keys — O(1) average get, O(1) insert, but parent-existence check requires `path.rsplit('/', 1)[0]` lookup. Simpler, slightly less intuitive.

---

### Stream of Characters

> [!example] Problem
> Design an algorithm that accepts a stream of characters and checks if a suffix of these characters is a string of a given array of strings words.
> For example, if words = ["abc", "xyz"] and the stream added the four characters (one by one) 'a', 'x', 'y', and 'z', your algorithm should detect that the suffix "xyz" of the characters "axyz" matches "xyz" from words.
> Implement the StreamChecker class
> 
> **Example 1:**
> ```
> Input
> ["StreamChecker", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query"]
> [[["cd", "f", "kl"]], ["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"], ["h"], ["i"], ["j"], ["k"], ["l"]]
> Output
> [null, false, false, false, true, false, true, false, false, false, false, false, true]
> 
> Explanation
> StreamChecker streamChecker = new StreamChecker(["cd", "f", "kl"]);
> streamChecker.query("a"); // return False
> streamChecker.query("b"); // return False
> streamChecker.query("c"); // return False
> streamChecker.query("d"); // return True, because 'cd' is in the wordlist
> streamChecker.query("e"); // return False
> streamChecker.query("f"); // return True, because 'f' is in the wordlist
> streamChecker.query("g"); // return False
> streamChecker.query("h"); // return False
> streamChecker.query("i"); // return False
> streamChecker.query("j"); // return False
> streamChecker.query("k"); // return False
> streamChecker.query("l"); // return True, because 'kl' is in the wordlist
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 2000
> - 1 <= words[i].length <= 200
> - words[i] consists of lowercase English letters.
> - letter is a lowercase English letter.
> - At most 4 * 10^4 calls will be made to query.

> [!info] Approach
> Checking all words against the current stream suffix by suffix is O(W × L) per query. Building a trie of reversed words and maintaining an active set of in-progress matches reduces this significantly. Insert all words reversed into a trie. Maintain a list of active trie nodes — the nodes currently being matched by the stream's recent suffix. On each `query(c)`: advance all active nodes by `c` (on the reversed trie = checking if `c` is a character moving backwards from the end of any word). Add root's child for `c` to start new potential matches. Build trie of reversed words. Keep `active: list[TrieNode]`. On `query(c)`: new_active = []; for each node in active, if `c` in node.children, add child to new_active. Also check root for `c` (new suffix starting). If any node in new_active has `is_end = True`, return True.


> [!note]- Python Solution
> ```python
> class SCNode:
>     def __init__(self):
>         self.children: dict[str, SCNode] = {}
>         self.is_end: bool = False
> 
> class StreamChecker:
>     def __init__(self, words):
>         self.root = SCNode()
>         for word in words:
>             node = self.root
>             for c in reversed(word):   # insert reversed
>                 if c not in node.children:
>                     node.children[c] = SCNode()
>                 node = node.children[c]
>             node.is_end = True
>         self.active: list[SCNode] = []   # nodes currently being extended
> 
>     def query(self, letter):
>         new_active = []
>         # Try to extend root (start of new suffix match)
>         if letter in self.root.children:
>             new_active.append(self.root.children[letter])
>         # Extend all ongoing matches
>         for node in self.active:
>             if letter in node.children:
>                 new_active.append(node.children[letter])
>         self.active = new_active
>         for n in self.active:
>             if n.is_end:
>                 return True
>         return False
> ```

> [!success] Complexity
> Build O(W × L). Query O(|active| × 1) per call — `active` is bounded by the number of distinct word lengths in the dictionary (at most min(stream_length, W × L)). Space O(W × L) trie + O(stream_length) active list.

> [!tip] Alternatives
> - Aho-Corasick on reversed stream: equivalent approach, handles the same problem with failure links for guaranteed O(text_length + matches) — more complex to implement.
> - KMP per word: O(W × L) per query character — degrades with large dictionaries.

---

### Palindrome Pairs `⚡ T1`

> [!example] Problem
> You are given a 0-indexed array of unique strings words.
> A palindrome pair is a pair of integers (i, j) such that:
> Return an array of all the palindrome pairs of words.
> You must write an algorithm with O(sum of words[i].length) runtime complexity.
> 
> **Example 1:**
> ```
> Input: words = ["abcd","dcba","lls","s","sssll"]
> Output: [[0,1],[1,0],[3,2],[2,4]]
> Explanation: The palindromes are ["abcddcba","dcbaabcd","slls","llssssll"]
> ```
> 
> **Example 2:**
> ```
> Input: words = ["bat","tab","cat"]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["battab","tabbat"]
> ```
> 
> **Example 3:**
> ```
> Input: words = ["a",""]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["a","a"]
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 5000
> - 0 <= words[i].length <= 300
> - words[i] consists of lowercase English letters.

> [!info] Approach
> Brute force O(N² × L). A trie of reversed words reduces the search: for each word `w`, we look for reversed words that can pair with it to form a palindrome. Insert all reversed words into a trie, tagging each end node with the word's index. For each word `w`, walk the trie with `w`'s characters; if we reach a word end before exhausting `w`, check if the remaining suffix of `w` is a palindrome (then `w + rev_word` is a palindrome). If we exhaust `w` first, collect all words in the trie subtree whose corresponding remaining suffix is a palindrome. At each trie node, store a list of word indices whose reversed word ends here but the trie path continues — these are "prefix palindrome" candidates. Walk trie with `w`; if `node.word_idx != -1` and the remaining `w[i:]` is a palindrome, record `(word_idx, i_word)`. After exhausting `w`, collect from `node.palindrome_suffixes` (stored during build).


> [!note]- Python Solution
> ```python
> def palindrome_pairs(words):
>     def is_palindrome(s):
>         return s == s[::-1]
> 
>     word_map = {w: i for i, w in enumerate(words)}
>     result = []
> 
>     for i, word in enumerate(words):
>         n = len(word)
>         for j in range(n + 1):
>             # Case 1: word[:j] is palindrome → rev(word[j:]) + word is palindrome
>             prefix, suffix = word[:j], word[j:]
>             if is_palindrome(prefix):
>                 rev_suf = suffix[::-1]
>                 if rev_suf in word_map and word_map[rev_suf] != i:
>                     result.append([word_map[rev_suf], i])
>             # Case 2: word[j:] is palindrome → word + rev(word[:j]) is palindrome
>             if j < n and is_palindrome(suffix):
>                 rev_pre = prefix[::-1]
>                 if rev_pre in word_map and word_map[rev_pre] != i:
>                     result.append([i, word_map[rev_pre]])
>         # Avoid duplicates when j == 0 in both cases (empty prefix/suffix overlap)
>     return result
> ```

> [!success] Complexity
> Time O(N × L²) — N words, each generates O(L) splits, palindrome check O(L) each. Space O(N × L) for hash map.

> [!tip] Alternatives
> - Trie of reversed words (true trie approach): walk each word through the reversed-word trie; at each step check partial palindromes — same O(N × L²) complexity, more complex code with similar performance in Python.
> - Brute force with hash map: check `word + rev(other_word)` — O(N² × L).

---

### Design Search Autocomplete System (Trie + DFS Variant) `⚡ T1`

> [!example] Problem
> Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character `'#'`).
> 
> You are given a string array `sentences` and an integer array `times` both of length `n` where `sentences[i]` is a previously typed sentence and `times[i]` is the corresponding number of times the sentence was typed. For each input character except `'#'`, return the top `3` historical hot sentences that have the same prefix as the part of the sentence already typed.
> 
> Here are the specific rules:
> 
> 	
> - The hot degree for a sentence is defined as the number of times a user typed the exactly same sentence before.
> 	
> - The returned top `3` hot sentences should be sorted by hot degree (The first is the hottest one). If several sentences have the same hot degree, use ASCII-code order (smaller one appears first).
> 	
> - If less than `3` hot sentences exist, return as many as you can.
> 	
> - When the input is a special character, it means the sentence ends, and in this case, you need to return an empty list.
> 
> Implement the `AutocompleteSystem` class:
> 
> 	
> - `AutocompleteSystem(String[] sentences, int[] times)` Initializes the object with the `sentences` and `times` arrays.
> 	`List<String> input(char c)` This indicates that the user typed the character `c`.
> 	
> 		
> - Returns an empty array `[]` if `c == '#'` and stores the inputted sentence in the system.
> 		
> - Returns the top `3` historical hot sentences that have the same prefix as the part of the sentence already typed. If there are fewer than `3` matches, return them all.
> 	
> 	
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input**
> ["AutocompleteSystem", "input", "input", "input", "input"]
> [[["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]], ["i"], [" "], ["a"], ["#"]]
> **Output**
> [null, ["i love you", "island", "i love leetcode"], ["i love you", "i love leetcode"], [], []]
> 
> **Explanation**
> AutocompleteSystem obj = new AutocompleteSystem(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]);
> obj.input("i"); // return ["i love you", "island", "i love leetcode"]. There are four sentences that have prefix "i". Among them, "ironman" and "i love leetcode" have same hot degree. Since ' ' has ASCII code 32 and 'r' has ASCII code 114, "i love leetcode" should be in front of "ironman". Also we only need to output top 3 hot sentences, so "ironman" will be ignored.
> obj.input(" "); // return ["i love you", "i love leetcode"]. There are only two sentences that have prefix "i ".
> obj.input("a"); // return []. There are no sentences that have prefix "i a".
> obj.input("#"); // return []. The user finished the input, the sentence "i a" should be saved as a historical sentence in system. And the following input will be counted as a new search.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `n == sentences.length`
> 	
> - `n == times.length`
> 	
> - `1 <= n <= 100`
> 	
> - `1 <= sentences[i].length <= 100`
> 	
> - `1 <= times[i] <= 50`
> 	
> - `c` is a lowercase English letter, a hash `'#'`, or space `' '`.
> 	
> - Each tested sentence will be a sequence of characters `c` that end with the character `'#'`.
> 	
> - Each tested sentence will have a length in the range `[1, 200]`.
> 	
> - The words in each input sentence are separated by single spaces.
> 	
> - At most `5000` calls will be made to `input`.

> [!info] Approach
> The main LC 642 solution stores all sentences at every ancestor node — O(S × L) extra space. This variant stores only frequency at terminal nodes; DFS is O(output) per query but saves memory. Trie with `freq` at terminal nodes only. Query: walk to prefix node, run DFS to collect all `(freq, sentence)` pairs, return top 3 by `(-freq, sentence)`. `insert(sentence, freq)`: standard trie, set `node.freq = freq` at terminal. `query(prefix)`: walk to prefix node. DFS collecting `(freq, built_string)` for all `is_end` nodes. Sort and return top 3.


> [!note]- Python Solution
> ```python
> class ACNode2:
>     def __init__(self):
>         self.children: dict[str, ACNode2] = {}
>         self.freq: int = 0
> 
> class AutocompleteSystemV2:
>     def __init__(self, sentences, times):
>         self.root = ACNode2()
>         self.curr_prefix: list[str] = []
>         self.curr_node: ACNode2 | None = self.root
>         for s, t in zip(sentences, times):
>             self._insert(s, t)
> 
>     def _insert(self, sentence, freq):
>         node = self.root
>         for c in sentence:
>             if c not in node.children:
>                 node.children[c] = ACNode2()
>             node = node.children[c]
>         node.freq += freq
> 
>     def _dfs(self, node, path, results, str]]):
>         if node.freq > 0:
>             results.append((node.freq, ''.join(path)))
>         for ch, child in node.children.items():
>             path.append(ch)
>             self._dfs(child, path, results)
>             path.pop()
> 
>     def input(self, c):
>         if c == '#':
>             sentence = ''.join(self.curr_prefix)
>             self._insert(sentence, 1)
>             self.curr_prefix = []
>             self.curr_node = self.root
>             return []
>         self.curr_prefix.append(c)
>         if self.curr_node and c in self.curr_node.children:
>             self.curr_node = self.curr_node.children[c]
>         else:
>             self.curr_node = None
>         if not self.curr_node:
>             return []
>         results = []
>         self._dfs(self.curr_node, self.curr_prefix[:], results)
>         results.sort(key=lambda x: (-x[0], x[1]))
>         return [s for _, s in results[:3]]
> ```

> [!success] Complexity
> Time O(p + output × L) per input character where p = prefix length, output = matching sentences. Space O(N × L) — no per-node sentence lists.

> [!tip] Alternatives
> - Per-node cached lists (LC 642 main solution): O(1) query time after O(S × L) build space — trades memory for speed.

---

## Suffix Trie / Advanced

### Implement Trie II (Count Operations) `⚡ T1`

> [!example] Problem
> Implement a trie with `insert(word)`, `countWordsEqualTo(word)` (exact count of that word inserted), `countWordsStartingWith(prefix)` (count of all inserted words with that prefix), and `erase(word)` (remove one occurrence).

> [!info] Approach
> The basic trie only tracks `is_end` (bool). Tracking insertion counts enables frequency-aware operations — needed when words are inserted multiple times and erased individually. Each node stores `pass_count` (how many words passed through during insert) and `end_count` (how many words ended here). `erase` decrements both along the path. `insert`: walk, incrementing `node.pass_count` at every node, `node.end_count` at terminal. `countWordsStartingWith(prefix)`: walk to prefix node, return `node.pass_count`. `countWordsEqualTo(word)`: walk to terminal, return `node.end_count`. `erase(word)`: walk, decrementing `node.pass_count`; decrement `node.end_count` at terminal. Optionally prune nodes where `pass_count == 0`.


> [!note]- Python Solution
> ```python
> class T2Node:
>     def __init__(self):
>         self.children: dict[str, T2Node] = {}
>         self.pass_count: int = 0
>         self.end_count: int = 0
> 
> class Trie2:
>     def __init__(self):
>         self.root = T2Node()
> 
>     def insert(self, word):
>         node = self.root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = T2Node()
>             node = node.children[c]
>             node.pass_count += 1
>         node.end_count += 1
> 
>     def count_words_equal_to(self, word):
>         node = self.root
>         for c in word:
>             if c not in node.children:
>                 return 0
>             node = node.children[c]
>         return node.end_count
> 
>     def count_words_starting_with(self, prefix):
>         node = self.root
>         for c in prefix:
>             if c not in node.children:
>                 return 0
>             node = node.children[c]
>         return node.pass_count
> 
>     def erase(self, word):
>         node = self.root
>         for c in word:
>             node = node.children[c]
>             node.pass_count -= 1
>         node.end_count -= 1
> ```

> [!success] Complexity
> Time O(L) per operation. Space O(N × L).

> [!tip] Alternatives
> - Hash map `word → count` + prefix counter using a separate hash map — O(1) exact count, O(N × L) prefix scan. Simpler but slow for prefix queries.

---

### Shortest Unique Prefix for Every Word

> [!example] Problem
> Given a list of words, find the shortest prefix for each word that uniquely identifies it (no other word starts with that prefix).

> [!info] Approach
> "Unique prefix" means the trie node at the end of the prefix has `pass_count == 1` — only one word passes through it. Walk each word's trie path and stop at the first node with `pass_count == 1`. Trie with `pass_count` at each node. For each word, walk until `pass_count == 1` — that depth gives the shortest unique prefix. Insert all words, incrementing `node.pass_count` at each node. For each word, walk character by character; the first node with `pass_count == 1` marks the end of the shortest unique prefix.


> [!note]- Python Solution
> ```python
> class SUPNode:
>     def __init__(self):
>         self.children: dict[str, SUPNode] = {}
>         self.pass_count: int = 0
> 
> def shortest_unique_prefixes(words):
>     root = SUPNode()
>     for word in words:
>         node = root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = SUPNode()
>             node = node.children[c]
>             node.pass_count += 1
> 
>     result = []
>     for word in words:
>         node = root
>         for i, c in enumerate(word):
>             node = node.children[c]
>             if node.pass_count == 1:
>                 result.append(word[:i + 1])
>                 break
>         else:
>             result.append(word)   # entire word is needed (duplicate or full match)
>     return result
> ```

> [!success] Complexity
> Time O(N × L) build + O(N × L) query. Space O(N × L).

> [!tip] Alternatives
> - Sort words; compare adjacent: O(N × L log N). For each word find the LCP with its neighbor, take LCP+1 as the unique prefix length.

---

### Maximum XOR of Two Numbers — Prefix Hash Approach `⚡ T1`

> [!example] Problem (Variant of LC 421)
> Same as LC 421 (max XOR in array) but solved without an explicit trie node class — using a set-based prefix approach to contrast with the trie solution.

> [!info] Approach
> Demonstrates the equivalence of "XOR trie greedy" and "prefix hash greedy" for this problem. Useful to know both for interviews. Iterate from bit 31 to 0. At each step maintain a set of prefixes (first `k` bits) of all numbers. Assume the answer's current bit is 1; check if any two prefixes XOR to match the assumed answer so far. If yes, keep the 1-bit; otherwise set it to 0. `max_xor = 0`. For bit `b` from 31 to 0: `mask = max_xor | (1 << b)`. Compute prefix set `{num & mask for num in nums}`. Try `candidate = max_xor | (1 << b)`. If any two prefixes `a, b` in the set satisfy `a ^ b == candidate` (i.e., `candidate ^ a` is in the set), then `max_xor = candidate`. Else leave `max_xor` unchanged (this bit stays 0).


> [!note]- Python Solution
> ```python
> def find_maximum_xor_hash(nums):
>     max_xor = 0
>     mask = 0
>     for bit in range(31, -1, -1):
>         mask |= (1 << bit)
>         prefixes = {num & mask for num in nums}
>         candidate = max_xor | (1 << bit)
>         pair_found = False
>         for p in prefixes:
>             if (candidate ^ p) in prefixes:
>                 pair_found = True
>                 break
>         if pair_found:
>             max_xor = candidate
>     return max_xor
> ```

> [!success] Complexity
> Time O(32 × N). Space O(N) for prefix set. Same asymptotic as trie approach.

> [!tip] Alternatives
> - XOR Trie (see earlier entry): O(32 × N) time, O(32 × N) space — same complexity, trie is more intuitive for the greedy argument.

---

## See Also

[[string-algorithms]] | [[backtracking]] | [[hashing]]
### Implement Trie II (Count Prefixes and Equal Words) `⚡ T1`

> [!example] Problem
> Extend a trie so you can count how many words equal a string and how many words have a given prefix.

> [!info] Approach
> Standard trie nodes need counters, not just child pointers, when queries ask for multiplicity. Each node stores `pass` (words passing through) and `end` (words ending here). Increment `pass` while descending during insertion and increment `end` at the final node. Decrement counters on erase.


> [!note]- Python Solution
> ```python
> class TrieNode:
>     def __init__(self):
>         self.children = {}
>         self.pass_count = 0
>         self.end_count = 0
> 
> class Trie:
>     def __init__(self):
>         self.root = TrieNode()
> ```

> [!success] Complexity
> O(L) per insert/search/erase, where `L` is the word length.

> [!tip] Alternatives
> A hash map can count whole words, but prefix counts require a trie or another prefix-aware structure.

---

## Trie Applications

### Replace Words (LC 648) `⚡ T1`

> [!example] Problem
> In English, we have a concept called root, which can be followed by some other word to form another longer word - let's call this word derivative. For example, when the root "help" is followed by the word "ful", we can form a derivative "helpful".
> Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace all the derivatives in the sentence with the root forming it. If a derivative can be replaced by more than one root, replace it with the root that has the shortest length.
> Return the sentence after the replacement.
> 
> **Example 1:**
> ```
> Input: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
> Output: "the cat was rat by the bat"
> ```
> 
> **Example 2:**
> ```
> Input: dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
> Output: "a a b c"
> ```
> 
> **Constraints:**
> - 1 <= dictionary.length <= 1000
> - 1 <= dictionary[i].length <= 100
> - dictionary[i] consists of only lower-case letters.
> - 1 <= sentence.length <= 10^6
> - sentence consists of only lower-case letters and spaces.
> - The number of words in sentence is in the range [1, 1000]
> - The length of each word in sentence is in the range [1, 1000]
> - Every two consecutive words in sentence will be separated by exactly one space.
> - sentence does not have leading or trailing spaces.

> [!info] Approach
> For each word in the sentence we need to find if any dictionary root is a prefix of it, and we want the shortest such root. A trie makes prefix lookup O(L) and naturally returns the shortest match first. Build a trie from the dictionary roots. For each word in the sentence, walk down the trie character by character. The moment you hit a terminal node (end of a root), that is the shortest matching root. Insert all roots. For each sentence word, traverse the trie; if a node has `is_end = True`, return the prefix built so far. If traversal ends without a match, keep the original word.


> [!note]- Python Solution
> ```python
> class TrieNode:
>     def __init__(self):
>         self.children = {}
>         self.is_end = False
> >
> def replace_words(dictionary, sentence):
>     root = TrieNode()
>     for word in dictionary:
>         node = root
>         for ch in word:
>             if ch not in node.children:
>                 node.children[ch] = TrieNode()
>             node = node.children[ch]
>         node.is_end = True
> >
>     def replace(word):
>         node = root
>         prefix = []
>         for ch in word:
>             if ch not in node.children:
>                 break
>             node = node.children[ch]
>             prefix.append(ch)
>             if node.is_end:
>                 return ''.join(prefix)
>         return word
> >
>     return ' '.join(replace(word) for word in sentence.split())
> ```

> [!success] Complexity
> Time O(D + S) where D = total characters in dictionary, S = total characters in sentence. Space O(D).

> [!tip] Alternatives
> - Sort dictionary by word length, check each word for prefix match: O(D * S) — too slow.
> - Key insight: stopping at the first `is_end` node guarantees the *shortest* root is returned, since shorter roots are encountered before longer ones when traversing from the root.

---

### Palindrome Pairs (LC 336) `⚡ T1`

> [!example] Problem
> You are given a 0-indexed array of unique strings words.
> A palindrome pair is a pair of integers (i, j) such that:
> Return an array of all the palindrome pairs of words.
> You must write an algorithm with O(sum of words[i].length) runtime complexity.
> 
> **Example 1:**
> ```
> Input: words = ["abcd","dcba","lls","s","sssll"]
> Output: [[0,1],[1,0],[3,2],[2,4]]
> Explanation: The palindromes are ["abcddcba","dcbaabcd","slls","llssssll"]
> ```
> 
> **Example 2:**
> ```
> Input: words = ["bat","tab","cat"]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["battab","tabbat"]
> ```
> 
> **Example 3:**
> ```
> Input: words = ["a",""]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["a","a"]
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 5000
> - 0 <= words[i].length <= 300
> - words[i] consists of lowercase English letters.

> [!info] Approach
> For `words[i] + words[j]` to be a palindrome, either: (a) one is the reverse of the other, (b) one word has a palindromic suffix/prefix and its prefix/suffix reverse exists in the list. Build a hash map of `word -> index`. For each word, consider all splits into `(prefix, suffix)`. If `prefix` is a palindrome and `reverse(suffix)` is in the map, that's a valid pair. Similarly for palindromic suffixes. For each word at index `i`, split at every position `k` (0 to len): if `word[:k]` is a palindrome and `reverse(word[k:])` is in the map (and not `i`), add `(map[reverse], i)`. If `word[k:]` is a palindrome and `reverse(word[:k])` is in the map, add `(i, map[reverse])`. Avoid duplicates by only doing suffix-palindrome check for `k > 0`.


> [!note]- Python Solution
> ```python
> def palindrome_pairs(words):
>     word_map = {word: i for i, word in enumerate(words)}
>     result = []
> >
>     def is_palindrome(s):
>         return s == s[::-1]
> >
>     for i, word in enumerate(words):
>         for k in range(len(word) + 1):
>             prefix = word[:k]
>             suffix = word[k:]
>             if is_palindrome(prefix):
>                 rev_suffix = suffix[::-1]
>                 if rev_suffix in word_map and word_map[rev_suffix] != i:
>                     result.append([word_map[rev_suffix], i])
>             if k > 0 and is_palindrome(suffix):
>                 rev_prefix = prefix[::-1]
>                 if rev_prefix in word_map and word_map[rev_prefix] != i:
>                     result.append([i, word_map[rev_prefix]])
>     return result
> ```

> [!success] Complexity
> Time O(n * L²) where n = number of words, L = average word length. Space O(n * L).

> [!tip] Alternatives
> - Trie-based: insert reversed words into a trie; for each word walk the trie and check for palindromic remainders. Same asymptotic complexity but avoids hashing.
> - Key edge case: empty string `""` — it forms a palindrome with any word that is itself a palindrome.

---

### Word Squares (LC 425)

> [!example] Problem
> Given an array of **unique `🎯 T2`** strings `words`, return *all the ***[word squares](https://en.wikipedia.org/wiki/Word_square)*** you can build from *`words`. The same word from `words` can be used **multiple times**. You can return the answer in **any order**.
> 
> A sequence of strings forms a valid **word square** if the `k^th` row and column read the same string, where `0 <= k < max(numRows, numColumns)`.
> 
> 	
> - For example, the word sequence `["ball","area","lead","lady"]` forms a word square because each word reads the same both horizontally and vertically.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** words = ["area","lead","wall","lady","ball"]
> **Output:** [["ball","area","lead","lady"],["wall","area","lead","lady"]]
> **Explanation:**
> The output consists of two word squares. The order of output does not matter (just the order of words in each word square matters).
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** words = ["abat","baba","atan","atal"]
> **Output:** [["baba","abat","baba","atal"],["baba","abat","baba","atan"]]
> **Explanation:**
> The output consists of two word squares. The order of output does not matter (just the order of words in each word square matters).
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= words.length <= 1000`
> 	
> - `1 <= words[i].length <= 4`
> 	
> - All `words[i]` have the same length.
> 	
> - `words[i]` consists of only lowercase English letters.
> 	
> - All `words[i]` are **unique `🎯 T2`**.

> [!info] Approach
> When building the square row by row, the prefix of each new row is already determined by the column values filled in so far. A trie with prefix-to-words index lets us quickly find all words matching a required prefix. Build a trie where each node stores all words that pass through it (i.e., all words with that prefix). Backtrack: at row `k`, the required prefix is `square[0][k] + square[1][k] + ... + square[k-1][k]`. Fetch all matching words from the trie and try each. Insert all words into the trie, at each node also storing the list of words with that prefix. Backtrack with `build(step, square)`: if `step == n`, save the square. Otherwise extract prefix from the current partial square, look up matching words in the trie, and recurse.


> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def word_squares(words):
>     n = len(words[0])
>     prefix_map = defaultdict(list)
>     for word in words:
>         for i in range(n + 1):
>             prefix_map[word[:i]].append(word)
> >
>     result = []
> >
>     def backtrack(step, square):
>         if step == n:
>             result.append(square[:])
>             return
>         prefix = ''.join(square[i][step] for i in range(step))
>         for candidate in prefix_map[prefix]:
>             square.append(candidate)
>             backtrack(step + 1, square)
>             square.pop()
> >
>     for word in words:
>         backtrack(1, [word])
>     return result
> ```

> [!success] Complexity
> Time O(n * 26^n) worst case (bounded by trie pruning in practice), Space O(n² + total prefix entries).

> [!tip] Alternatives
> - Without a trie: binary search or set lookups for prefix matching — same logic, slightly less efficient.
> - Key insight: the trie's word lists at each prefix node are the core lookup structure; this is essentially a hash map of prefix → word list but structured as a trie for clarity.

---

## See Also

[[string-algorithms]] | [[backtracking]] | [[hashing]] | [[dynamic-programming]]
