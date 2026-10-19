---
module: striver/27-graphs
lesson: 39
topic: Number of operations to make network connected
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-operations-to-make-network-connected?category=hard-problems-ii&source=strivers-a2z-dsa-sheet
tags: [striver, graph, union-find, connected-components]
---
# 39. Number of operations to make network connected

← [Find the MST weight](38-find-the-mst-weight.md) · [Part 27 index](README.md) · Next → [Accounts merge](40-accounts-merge.md)

> [!abstract] Problem at a glance
> **Task:** Move cables between computers so all `n` are connected; return the minimum number of moves, or −1 if impossible.
> **Key insight:** Joining `c` components needs exactly `c − 1` cables. Any cable that closes a cycle is spare and can be moved. So: if `E < n − 1` there aren't enough cables (−1); otherwise the answer is `components − 1`, and enough spares are guaranteed.
> **Difficulty:** Medium · **Pattern:** DSU component count · **Also on:** LC 1319
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-operations-to-make-network-connected?category=hard-problems-ii&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS component count](#3-dfs-component-count) · [4. DSU](#4-dsu) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`connections[i] = [a, b]` is a cable between computers `a` and `b` (0-indexed). In one operation you can remove a cable and place it between any two disconnected computers. Return the minimum operations to connect all computers, or `-1`.

| Input | Output | Why |
|---|---|---|
| `n = 4, connections = [[0,1],[0,2],[1,2]]` | `1` | move 1–2 to 1–3 |
| `n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]` | `-1` | 4 cables < 5 needed |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ connections.length ≤ min(n(n−1)/2, 10⁵)`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS component count | count components with DFS; check E ≥ n − 1 | O(n + E) | O(n + E) |
| DSU | union every cable; components = n − successful unions | O(n + E·α(n)) | O(n) |

> [!tip] Interview angle
> State the counting argument before coding: a connected graph on n nodes needs n − 1 edges, and a graph with c components and E ≥ n − 1 edges always has at least c − 1 redundant edges. Then it's one DSU pass.

---

## 3. DFS component count

**Intuition.** Same argument, components counted with an iterative DFS over an adjacency list.

```python
def make_connected_dfs(n, connections):
    if len(connections) < n - 1:
        return -1
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
    seen, comps = [False] * n, 0
    for s in range(n):
        if seen[s]:
            continue
        comps += 1
        seen[s] = True
        st = [s]
        while st:
            u = st.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    st.append(v)
    return comps - 1
```

**Complexity:** time **O(n + E)**, space **O(n + E)**.

---

## 4. DSU

**Intuition.** Start with `n` components; each union of two different roots reduces the count by one. Cables whose ends are already joined are the spares. Answer `comps − 1` once `E ≥ n − 1` is checked.

**Algorithm**

1. If `len(connections) < n − 1` return −1.
2. DSU on n; `comps = n`.
3. For each cable: if roots differ, union and `comps −= 1`.
4. Return `comps − 1`.

**Dry run** — n = 6, cables 0–1, 0–2, 0–3, 1–2, 1–3: unions succeed for the first three (comps 3), 1–2 and 1–3 are spares. Components {0,1,2,3}, {4}, {5} → 2 moves.

**C++**
```cpp
int makeConnected(int n, vector<vector<int>>& connections) {
    if ((int)connections.size() < n - 1) return -1;
    vector<int> parent(n);
    iota(parent.begin(), parent.end(), 0);
    function<int(int)> find = [&](int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); };
    int comps = n;
    for (auto& c : connections) {
        int a = find(c[0]), b = find(c[1]);
        if (a != b) { parent[a] = b; comps--; }
    }
    return comps - 1;
}
```

**Java**
```java
static int[] parent;
static int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
static int makeConnected(int n, int[][] connections) {
    if (connections.length < n - 1) return -1;
    parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    int comps = n;
    for (int[] c : connections) {
        int a = find(c[0]), b = find(c[1]);
        if (a != b) { parent[a] = b; comps--; }
    }
    return comps - 1;
}
```

**Python**
```python
def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    comps = n
    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            comps -= 1
    return comps - 1
```

**Complexity:** time **O(n + E·α(n))**, space **O(n)** — one pass of near-constant DSU operations.

---

## Edge cases

- n = 1: 0.
- Already connected: 0.
- E = n − 1 exactly but disconnected: impossible to have spares? No: E = n − 1 with c components means c − 1 cycle edges, still enough.

---

## Common mistakes

1. Counting spare edges and comparing with c − 1 (correct but redundant once E ≥ n − 1 is checked).
2. Returning `comps` instead of `comps − 1`.
3. Checking `E < n − 1` after the DSU pass and returning the wrong value for tiny inputs.

---

## Follow-ups

1. Return which cables to move?
2. Cables have costs to move?

<details><summary>Answer sketches</summary>

**#1:** Record the redundant cables during the pass and pair each with an edge between consecutive component roots.

**#2:** Becomes an MST-style problem; Kruskal over all candidate pairs.
</details>

---

## Flashcards

**LC 1319 formula?** #flashcard
−1 if E < n − 1, else components − 1.

**Why are there always enough spare cables?** #flashcard
c components with E ≥ n − 1 edges contain ≥ c − 1 cycle edges.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md)
