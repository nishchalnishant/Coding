---
module: striver-a2z/27-graphs
lesson: 5
topic: Number of provinces
difficulty: Medium
source: https://takeuforward.org/learning/dsa/number-of-provinces?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, dfs, union-find]
---
# 5. Number of provinces

← [Connected Components](04-connected-components.md) · [Part 27 index](README.md) · Next → [Number of islands](06-number-of-islands.md)

> [!abstract] Problem at a glance
> **Task:** Given an `n × n` adjacency matrix `isConnected`, count the groups of directly or indirectly connected cities.
> **Key insight:** A province is a connected component. The input is already an adjacency matrix, so the DFS expands city `i` by scanning row `i`. With n² entries to read anyway, O(n²) is optimal.
> **Difficulty:** Medium · **Pattern:** Connected components (matrix input) · **Also on:** LC 547
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/number-of-provinces?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Union-find over the matrix](#3-union-find-over-the-matrix) · [4. DFS on the matrix](#4-dfs-on-the-matrix) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

There are `n` cities. `isConnected[i][j] = 1` if cities `i` and `j` are directly connected (the matrix is symmetric and `isConnected[i][i] = 1`). A province is a maximal group of cities connected directly or indirectly. Return the number of provinces.

| Input | Output | Why |
|---|---|---|
| `isConnected = [[1,1,0],[1,1,0],[0,0,1]]` | `2` | {0,1} and {2} |
| `isConnected = [[1,0,0],[0,1,0],[0,0,1]]` | `3` | no connections |

**Constraints:** `1 ≤ n ≤ 200`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Union-find over the matrix | union every `i < j` with a 1 | O(n² · α(n)) | O(n) |
| DFS on the matrix | for each unvisited city, DFS scanning its row | O(n²) | O(n) |

> [!tip] Interview angle
> Point out that converting the matrix to adjacency lists first is pointless: the input is already Θ(n²), so scanning the row is optimal. Offer union-find as the alternative, and note it also handles connections arriving in a stream.

---

## 3. Union-find over the matrix

**Intuition.** Start with `n` singletons; for every `isConnected[i][j] = 1` with `i < j`, union them and decrement the count when two different roots merge.

```python
def find_circle_num_dsu(M):
    n = len(M)
    par = list(range(n))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    comps = n
    for i in range(n):
        for j in range(i + 1, n):
            if M[i][j]:
                a, b = find(i), find(j)
                if a != b:
                    par[a] = b
                    comps -= 1
    return comps
```

**Complexity:** time **O(n² · α(n))**, space **O(n)**.

---

## 4. DFS on the matrix

**Intuition.** Outer loop over cities; each unvisited city starts a DFS (iterative stack) that, when expanding `u`, scans row `u` for unvisited neighbours. Count DFS starts.

**Algorithm**

1. `seen = [false]·n`, `count = 0`.
2. For each city `s` not seen: `count++`, mark it, push it.
3. While the stack is non-empty: pop `u`; for each `v` with `M[u][v] = 1` and not seen, mark and push.
4. Return `count`.

**Dry run** — [[1,1,0],[1,1,0],[0,0,1]]: s=0 → visits 0,1 (count 1). s=2 → visits 2 (count 2).

**C++**
```cpp
int findCircleNum(vector<vector<int>>& M) {
    int n = M.size(), count = 0;
    vector<bool> seen(n, false);
    for (int s = 0; s < n; s++) {
        if (seen[s]) continue;
        count++;
        seen[s] = true;
        vector<int> st = {s};
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v = 0; v < n; v++)
                if (M[u][v] && !seen[v]) { seen[v] = true; st.push_back(v); }
        }
    }
    return count;
}
```

**Java**
```java
static int findCircleNum(int[][] M) {
    int n = M.length, count = 0;
    boolean[] seen = new boolean[n];
    for (int s = 0; s < n; s++) {
        if (seen[s]) continue;
        count++;
        seen[s] = true;
        ArrayDeque<Integer> st = new ArrayDeque<>();
        st.push(s);
        while (!st.isEmpty()) {
            int u = st.pop();
            for (int v = 0; v < n; v++)
                if (M[u][v] == 1 && !seen[v]) { seen[v] = true; st.push(v); }
        }
    }
    return count;
}
```

**Python**
```python
def find_circle_num(M):
    n = len(M)
    seen = [False] * n
    count = 0
    for s in range(n):
        if seen[s]:
            continue
        count += 1
        seen[s] = True
        st = [s]
        while st:
            u = st.pop()
            for v in range(n):
                if M[u][v] and not seen[v]:
                    seen[v] = True
                    st.append(v)
    return count
```

**Complexity:** time **O(n²)**, space **O(n)** — each city is expanded once and expansion scans one row of length n.

---

## Edge cases

- `n = 1`: one province.
- Fully connected: one province.
- Identity matrix: `n` provinces.

---

## Common mistakes

1. Treating the diagonal `M[i][i] = 1` as a new edge to process (harmless with `visited`, but wasteful in DSU without `i < j`).
2. Using 1-indexed cities as in the GFG variant without adjusting the loops.
3. Counting visited cells instead of DFS starts.

---

## Follow-ups

1. Input as an edge list with up to 10⁵ cities?
2. Return the members of each province?

<details><summary>Answer sketches</summary>

**#1:** Build adjacency lists (or use DSU over the edges): O(V + E), not O(V²).

**#2:** Collect the nodes popped in each DFS run into a list.
</details>

---

## Flashcards

**Provinces = ?** #flashcard
Connected components of the city graph.

**Why is O(n²) optimal here?** #flashcard
The input matrix itself has n² entries.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
