---
module: striver/27-graphs
lesson: 23
topic: Word ladder I
difficulty: Hard
source: https://takeuforward.org/learning/dsa/word-ladder-i?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, graph, bfs, strings, implicit-graph]
---
# 23. Word ladder I

← [Shortest path in undirected graph with unit weights](22-shortest-path-unit-weights.md) · [Part 27 index](README.md) · Next → [Word ladder II](24-word-ladder-ii.md)

> [!abstract] Problem at a glance
> **Task:** Return the number of words in the shortest transformation sequence from `beginWord` to `endWord`, changing one letter at a time through words in `wordList` (0 if impossible).
> **Key insight:** Words are nodes, and an edge joins two words that differ in one letter, so this is unweighted shortest path, i.e. BFS. Don't build the graph by comparing all pairs. Generate each word's neighbours on the fly: try all 26 letters at each position and keep the candidates that are in the word set. **Delete a word from the set when it is enqueued**; that is the visited mark.
> **Difficulty:** Hard · **Pattern:** BFS on an implicit graph · **Also on:** LC 127
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/word-ladder-i?category=shortest-path-algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS with all-pairs adjacency](#3-bfs-with-all-pairs-adjacency) · [4. BFS with on-the-fly neighbours](#4-bfs-with-on-the-fly-neighbours) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `beginWord`, `endWord` and a dictionary `wordList`, return the number of words in the shortest sequence `beginWord → w₁ → … → endWord`, where each adjacent pair differs in exactly one letter and every `wᵢ` (including `endWord`) is in `wordList`. Return 0 if no sequence exists. `beginWord` need not be in the list.

| Input | Output | Why |
|---|---|---|
| `begin = "hit", end = "cog", list = ["hot","dot","dog","lot","log","cog"]` | `5` | hit → hot → dot → dog → cog |
| `same, without "cog"` | `0` | endWord is not in the list |

**Constraints:** `1 ≤ L ≤ 10`, `1 ≤ |wordList| ≤ 5000`, lowercase letters, all words have length L.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS with all-pairs adjacency | compare every pair of words to build edges | O(N²·L) | O(N²) |
| BFS with on-the-fly neighbours | try 26 letters per position; remove from set when queued | O(N·L²·26) | O(N·L) |

> [!tip] Interview angle
> State the cost: O(N · L · 26) candidate generation, each costing O(L) to build and hash, so O(N · L² · 26). The all-pairs graph would be O(N² · L). Bidirectional BFS, expanding the smaller frontier each step, is the standard optimisation to mention.

---

## 3. BFS with all-pairs adjacency

**Intuition.** Build the explicit graph by checking every pair for a one-letter difference, then BFS from `beginWord`. Fine for small N, quadratic for 5000 words.

```python
from collections import deque

def ladder_pairs(begin, end, words):
    nodes = list(dict.fromkeys([begin] + words))
    if end not in words:
        return 0
    idx = {w: i for i, w in enumerate(nodes)}
    adj = [[] for _ in nodes]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if sum(a != b for a, b in zip(nodes[i], nodes[j])) == 1:
                adj[i].append(j)
                adj[j].append(i)
    dist = [0] * len(nodes)
    dist[0] = 1
    q = deque([0])
    while q:
        u = q.popleft()
        if nodes[u] == end:
            return dist[u]
        for v in adj[u]:
            if not dist[v]:
                dist[v] = dist[u] + 1
                q.append(v)
    return 0
```

**Complexity:** time **O(N²·L)**, space **O(N²)**.

---

## 4. BFS with on-the-fly neighbours

**Intuition.** Store the dictionary in a hash set. BFS from `beginWord` with its sequence length. For each popped word, try every position and every letter; a candidate still in the set is removed (visited) and enqueued with length + 1. Return the length when `endWord` is popped.

**Algorithm**

1. `s` = set(wordList); return 0 if `endWord ∉ s`.
2. Queue `(beginWord, 1)`; remove `beginWord` from `s` if present.
3. Pop `(w, d)`; if `w == endWord`, return `d`.
4. For each position and letter: build `cand`; if `cand ∈ s`, remove it and enqueue `(cand, d + 1)`.
5. Return 0.

**Dry run** — hit(1) → hot(2) → dot, lot(3) → dog, log(4) → cog(5).

**C++**
```cpp
int ladderLength(string begin, string end, vector<string>& words) {
    unordered_set<string> s(words.begin(), words.end());
    if (!s.count(end)) return 0;
    s.erase(begin);
    queue<pair<string, int>> q; q.push({begin, 1});
    while (!q.empty()) {
        auto [w, d] = q.front(); q.pop();
        if (w == end) return d;
        for (size_t i = 0; i < w.size(); i++) {
            char orig = w[i];
            for (char c = 'a'; c <= 'z'; c++) {
                w[i] = c;
                if (s.count(w)) { s.erase(w); q.push({w, d + 1}); }
            }
            w[i] = orig;
        }
    }
    return 0;
}
```

**Java**
```java
static int ladderLength(String begin, String end, String[] words) {
    Set<String> s = new HashSet<>(Arrays.asList(words));
    if (!s.contains(end)) return 0;
    s.remove(begin);
    ArrayDeque<String> q = new ArrayDeque<>();
    q.add(begin);
    for (int d = 1; !q.isEmpty(); d++) {
        for (int k = q.size(); k > 0; k--) {
            char[] w = q.poll().toCharArray();
            if (new String(w).equals(end)) return d;
            for (int i = 0; i < w.length; i++) {
                char orig = w[i];
                for (char c = 'a'; c <= 'z'; c++) {
                    w[i] = c;
                    String cand = new String(w);
                    if (s.remove(cand)) q.add(cand);
                }
                w[i] = orig;
            }
        }
    }
    return 0;
}
```

**Python**
```python
from collections import deque

def ladder_length(begin, end, words):
    s = set(words)
    if end not in s:
        return 0
    s.discard(begin)
    q = deque([(begin, 1)])
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                cand = w[:i] + c + w[i + 1:]
                if cand in s:
                    s.remove(cand)
                    q.append((cand, d + 1))
    return 0
```

**Complexity:** time **O(N·L²·26)**, space **O(N·L)** — each word is enqueued once and generates 26·L candidates of length L.

---

## Edge cases

- `endWord` not in the list: 0.
- `beginWord` in the list: remove it first so it isn't revisited.
- `beginWord` one step from `endWord`: 2.

---

## Common mistakes

1. Marking visited on pop, so words are enqueued many times (TLE).
2. Returning the number of **transformations** (edges) instead of words.
3. Building the all-pairs graph for 5000 words.

---

## Follow-ups

1. Bidirectional BFS?
2. Return the actual sequences?

<details><summary>Answer sketches</summary>

**#1:** Grow frontiers from both ends, always expanding the smaller; stop when they meet. It explores roughly 2·b^(d/2) instead of b^d nodes.

**#2:** Word Ladder II (next problem).
</details>

---

## Flashcards

**Word ladder graph?** #flashcard
Implicit: neighbours are one-letter edits that are in the dictionary.

**Visited mark in word ladder?** #flashcard
Remove the word from the set when it is enqueued.

**Optimisation to mention?** #flashcard
Bidirectional BFS.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
