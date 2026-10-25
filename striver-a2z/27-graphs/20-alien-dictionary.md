---
module: striver-a2z/27-graphs
lesson: 20
topic: Alien dictionary
difficulty: Hard
source: https://takeuforward.org/learning/dsa/alien-dictionary?category=hard-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, topological-sort, strings]
---
# 20. Alien dictionary

← [Course Schedule II](19-course-schedule-ii.md) · [Part 27 index](README.md) · Next → [Shortest path in DAG](21-shortest-path-in-dag.md)

> [!abstract] Problem at a glance
> **Task:** Given words sorted in an alien language that uses the first `k` lowercase letters, return the letters in alien order (`""` if the input is inconsistent).
> **Key insight:** Compare **adjacent** words only. The first position where they differ gives one edge, `x → y` (x comes before y). Nothing after that position says anything. Topologically sort the `k` letters. A cycle, or a longer word placed before its own prefix (`"ab"` before `"a"`), means the dictionary is invalid.
> **Difficulty:** Hard · **Pattern:** Build a DAG from constraints + topological sort · **Also on:** LC 269 (premium)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/alien-dictionary?category=hard-problems&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All pairs of words + DFS topo](#3-all-pairs-of-words--dfs-topo) · [4. Adjacent pairs + Kahn](#4-adjacent-pairs--kahn) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`words` is a list of strings sorted lexicographically by the rules of an alien language whose alphabet is the first `k` lowercase English letters. Return a string of those `k` letters in the alien order. If no order is consistent with the input, return `""`. (Tests here have a unique valid order; real problems accept any valid one.)

| Input | Output | Why |
|---|---|---|
| `words = ["baa","abcd","abca","cab","cad"], k = 4` | `"bdac"` | b<a (baa/abcd), d<a (abcd/abca), a<c, b<d (cab/cad) |
| `words = ["ab","a"], k = 2` | `""` | a prefix must come first |

**Constraints:** `1 ≤ N ≤ 300`, `1 ≤ k ≤ 26`, `1 ≤ |word| ≤ 50`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All pairs of words + DFS topo | edge from every pair's first mismatch | O(N²·L + k) | O(k²) |
| Adjacent pairs + Kahn | first mismatch of neighbours → edge; Kahn on k letters | O(N·L + k) | O(k²) |

> [!tip] Interview angle
> Three gotchas to raise out loud: (1) only adjacent pairs matter, since comparing all pairs adds only transitive edges; (2) only the **first** mismatch gives an edge; (3) the prefix case is invalid. Letters with no constraints can go anywhere, which is why many outputs can be correct.

---

## 3. All pairs of words + DFS topo

**Intuition.** Compare every pair `i < j`, not only neighbours. The extra edges are implied by transitivity, so the answer is the same, just slower. Then run a 3-state DFS topological sort over the letters.

```python
import sys

def alien_order_pairs(words, k):
    sys.setrecursionlimit(10 ** 4)
    letters = [chr(97 + i) for i in range(k)]
    adj = {c: set() for c in letters}
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a, b = words[i], words[j]
            for x, y in zip(a, b):
                if x != y:
                    adj[x].add(y)
                    break
            else:
                if len(a) > len(b):
                    return ""
    st, out = {c: 0 for c in letters}, []
    def go(u):
        st[u] = 1
        for v in sorted(adj[u]):
            if st[v] == 1 or (st[v] == 0 and not go(v)):
                return False
        st[u] = 2
        out.append(u)
        return True
    for c in letters:
        if st[c] == 0 and not go(c):
            return ""
    return "".join(reversed(out))
```

**Complexity:** time **O(N²·L + k)**, space **O(k²)**.

---

## 4. Adjacent pairs + Kahn

**Intuition.** Scan neighbouring words for the first differing character and add `x → y` (deduplicated in a set so in-degrees stay correct). Detect the prefix case. Kahn over the `k` letters; if not all `k` come out, there is a cycle, so return `""`.

**Algorithm**

1. For each adjacent pair `(a, b)`: find the first `i` with `a[i] ≠ b[i]`; add edge `a[i] → b[i]` if new.
2. If no mismatch and `len(a) > len(b)`, return `""`.
3. Kahn over letters `0..k−1` with in-degrees.
4. Return the order as a string if it has `k` letters, else `""`.

**Dry run** — baa/abcd → b→a; abcd/abca → d→a; abca/cab → a→c; cab/cad → b→d. In-degree 0: b. Pop b → d free (a still waits on d). Pop d → a. Pop a → c. "bdac".

**C++**
```cpp
string alienOrder(vector<string>& words, int k) {
    vector<vector<bool>> has(k, vector<bool>(k, false));
    vector<vector<int>> adj(k);
    vector<int> indeg(k, 0);
    for (size_t w = 0; w + 1 < words.size(); w++) {
        const string &a = words[w], &b = words[w + 1];
        size_t i = 0;
        while (i < a.size() && i < b.size() && a[i] == b[i]) i++;
        if (i == a.size() || i == b.size()) {
            if (a.size() > b.size()) return "";
            continue;
        }
        int u = a[i] - 'a', v = b[i] - 'a';
        if (!has[u][v]) { has[u][v] = true; adj[u].push_back(v); indeg[v]++; }
    }
    queue<int> q;
    for (int i = 0; i < k; i++) if (indeg[i] == 0) q.push(i);
    string out;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        out += char('a' + u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    return (int)out.size() == k ? out : "";
}
```

**Java**
```java
static String alienOrder(String[] words, int k) {
    boolean[][] has = new boolean[k][k];
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < k; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[k];
    for (int w = 0; w + 1 < words.length; w++) {
        String a = words[w], b = words[w + 1];
        int i = 0;
        while (i < a.length() && i < b.length() && a.charAt(i) == b.charAt(i)) i++;
        if (i == a.length() || i == b.length()) {
            if (a.length() > b.length()) return "";
            continue;
        }
        int u = a.charAt(i) - 'a', v = b.charAt(i) - 'a';
        if (!has[u][v]) { has[u][v] = true; adj.get(u).add(v); indeg[v]++; }
    }
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < k; i++) if (indeg[i] == 0) q.add(i);
    StringBuilder out = new StringBuilder();
    while (!q.isEmpty()) {
        int u = q.poll();
        out.append((char) ('a' + u));
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.add(v);
    }
    return out.length() == k ? out.toString() : "";
}
```

**Python**
```python
from collections import deque

def alien_order(words, k):
    adj = [set() for _ in range(k)]
    indeg = [0] * k
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                u, v = ord(x) - 97, ord(y) - 97
                if v not in adj[u]:
                    adj[u].add(v)
                    indeg[v] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    q = deque(i for i in range(k) if indeg[i] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(chr(97 + u))
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return "".join(out) if len(out) == k else ''
```

**Complexity:** time **O(N·L + k)**, space **O(k²)** — O(N·L) to build at most N−1 edges, plus Kahn on k letters.

---

## Edge cases

- Single word: no edges; any order of the k letters is valid.
- A longer word before its own prefix: `""`.
- Contradictory edges (`a<b` and `b<a`): Kahn leaves letters behind → `""`.
- Duplicate edges: deduplicate, or the in-degree never reaches 0.

---

## Common mistakes

1. Adding an edge for every differing position, not just the first.
2. Missing the prefix-invalid check.
3. Counting a duplicate edge twice in `indeg` but adding it once to `adj` (or vice versa).

---

## Follow-ups

1. LC 269: the alphabet is only the letters that appear in the words?
2. Return all valid orders?

<details><summary>Answer sketches</summary>

**#1:** Collect the set of letters first and run Kahn over it.

**#2:** Backtracking over Kahn's choices: exponential in the worst case.
</details>

---

## Flashcards

**Alien dictionary edges come from…?** #flashcard
The first mismatching character of each adjacent pair.

**Invalid-input cases?** #flashcard
A cycle, or a word followed by its own proper prefix.

**Why only adjacent pairs?** #flashcard
Non-adjacent pairs only imply transitive edges.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
