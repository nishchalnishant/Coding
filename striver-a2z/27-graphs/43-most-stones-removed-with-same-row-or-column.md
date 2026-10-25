---
module: striver-a2z/27-graphs
lesson: 43
topic: Most stones removed with same row or column
difficulty: Medium
source: https://takeuforward.org/learning/dsa/most-stones-removed-with-same-row-or-column?category=hard-problems-ii&source=strivers-a2z-dsa-sheet
tags: [striver, graph, union-find, graph]
---
# 43. Most stones removed with same row or column

← [Making a large island](42-making-a-large-island.md) · [Part 27 index](README.md) · Next → [Kosaraju's algorithm](44-kosarajus-algorithm.md)

> [!abstract] Problem at a glance
> **Task:** A stone can be removed if another stone shares its row or column; return the maximum number of stones removable.
> **Key insight:** Stones sharing a row or column form connected components, and every component can be peeled down to exactly **one** stone (remove leaves of a spanning tree first). So the answer is `n − components`. Treat each row and each column as a DSU node and union `row r` with `col c` for every stone: no O(n²) pairing needed.
> **Difficulty:** Medium · **Pattern:** DSU on rows ∪ columns · **Also on:** LC 947
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/most-stones-removed-with-same-row-or-column?category=hard-problems-ii&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pairwise graph + DFS](#3-pairwise-graph--dfs) · [4. DSU on row and column nodes](#4-dsu-on-row-and-column-nodes) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`stones[i] = [x, y]` are distinct points on a 2D grid. A stone can be removed if it shares a row or column with another stone that has not been removed. Return the largest possible number of removals.

| Input | Output | Why |
|---|---|---|
| `[[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]` | `5` | all six are one component |
| `[[0,0],[0,2],[1,1],[2,0],[2,2]]` | `3` | two components: {corners}, {(1,1)} |

**Constraints:** `1 ≤ n ≤ 1000`, `0 ≤ x, y ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pairwise graph + DFS | edge between stones sharing row or column; n − components | O(n²) | O(n²) |
| DSU on row and column nodes | union(row x, col y + OFFSET) per stone; count roots among used nodes | O(n·α) | O(R + C) |

> [!tip] Interview angle
> The interviewer wants the reduction: prove that a component of size s loses exactly s − 1 stones (remove in reverse BFS order from any root, never the last). Then present the row/column-node trick to get O(n·α) instead of O(n²).

---

## 3. Pairwise graph + DFS

**Intuition.** Connect every pair of stones that share a coordinate, count components with DFS, answer `n − comps`.

```python
def remove_stones_pairs(stones):
    n = len(stones)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i):
            if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:
                adj[i].append(j)
                adj[j].append(i)
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
    return n - comps
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. DSU on row and column nodes

**Intuition.** Node `x` is row x; node `y + 10001` is column y. Each stone unions its row with its column, so two stones sharing a row or column end up in one set. Components = distinct roots among the nodes actually touched.

**Algorithm**

1. DSU over `20002` nodes (or a hash map).
2. For each stone: `union(x, y + 10001)`; record both nodes as used.
3. `comps` = number of used nodes that are roots.
4. Return `n − comps`.

**Dry run** — Example 2: (0,0) joins R0–C0; (0,2) R0–C2; (2,0) R2–C0; (2,2) R2–C2 → one set {R0,R2,C0,C2}. (1,1) → {R1,C1}. comps = 2 → 5 − 2 = 3.

**C++**
```cpp
int removeStones(vector<vector<int>>& stones) {
    const int OFF = 10001;
    vector<int> parent(2 * OFF);
    iota(parent.begin(), parent.end(), 0);
    function<int(int)> find = [&](int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); };
    unordered_set<int> used;
    for (auto& s : stones) {
        int a = find(s[0]), b = find(s[1] + OFF);
        if (a != b) parent[a] = b;
        used.insert(s[0]);
        used.insert(s[1] + OFF);
    }
    int comps = 0;
    for (int u : used) if (find(u) == u) comps++;
    return (int)stones.size() - comps;
}
```

**Java**
```java
static int[] parent;
static int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
static int removeStones(int[][] stones) {
    final int OFF = 10001;
    parent = new int[2 * OFF];
    for (int i = 0; i < 2 * OFF; i++) parent[i] = i;
    Set<Integer> used = new HashSet<>();
    for (int[] s : stones) {
        int a = find(s[0]), b = find(s[1] + OFF);
        if (a != b) parent[a] = b;
        used.add(s[0]);
        used.add(s[1] + OFF);
    }
    int comps = 0;
    for (int u : used) if (find(u) == u) comps++;
    return stones.length - comps;
}
```

**Python**
```python
def remove_stones(stones):
    OFF = 10001
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for x, y in stones:
        a, b = find(x), find(y + OFF)
        if a != b:
            parent[a] = b
    comps = sum(1 for u in parent if find(u) == u)
    return len(stones) - comps
```

**Complexity:** time **O(n·α)**, space **O(R + C)** — one union per stone; the root count scans ≤ 2n used nodes (plus array init in C++/Java).

---

## Edge cases

- Single stone: 0.
- No two stones share a line: 0.
- Coordinates at the bound 10⁴: offset must be > 10⁴ so rows and columns don't collide.

---

## Common mistakes

1. Offset too small, so row 5 and column 5 become the same node.
2. Counting components over all 20002 nodes instead of only used ones.
3. Returning `components` instead of `n − components`.

---

## Follow-ups

1. Output an actual removal order?
2. Coordinates up to 10⁹?

<details><summary>Answer sketches</summary>

**#1:** DFS each component and remove in post-order (leaves first), keeping the root.

**#2:** Use the hash-map DSU (as in the Python version) with column keys `~y` or `y + 10⁹+1`.
</details>

---

## Flashcards

**LC 947 answer?** #flashcard
n − number of components (rows/columns linked by stones).

**LC 947 DSU nodes?** #flashcard
Rows and columns (column y → y + offset), not stones.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md)
