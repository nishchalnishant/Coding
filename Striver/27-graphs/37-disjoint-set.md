---
module: striver/27-graphs
lesson: 37
topic: Disjoint Set (Union-Find)
difficulty: Medium
source: https://takeuforward.org/learning/dsa/disjoint-set-?category=minimum-spanning-tree&source=strivers-a2z-dsa-sheet
tags: [striver, graph, union-find, dsu, design]
---
# 37. Disjoint Set (Union-Find)

← [Swim in rising water](36-swim-in-rising-water.md) · [Part 27 index](README.md) · Next → [Find the MST weight](38-find-the-mst-weight.md)

> [!abstract] Problem at a glance
> **Task:** Implement a disjoint-set structure on `0..n−1` with `unite(u, v)`, `connected(u, v)` and `size(u)` in near-constant amortised time.
> **Key insight:** Represent each set as a tree whose root is the set's name. `find` walks to the root and **compresses** the path; `unite` hangs the **smaller** tree under the larger root. Together these give O(α(n)) amortised per operation, which is ≤ 4 for any practical n.
> **Difficulty:** Medium · **Pattern:** Union by size + path compression
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/disjoint-set-?category=minimum-spanning-tree&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Naive parent pointers](#3-naive-parent-pointers) · [4. Union by size + path compression](#4-union-by-size--path-compression) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Design `DisjointSet(n)`:

- `unite(u, v)`: merge the sets containing `u` and `v` (no-op if already together).
- `connected(u, v)`: `true` if `u` and `v` are in the same set.
- `size(u)`: the number of elements in `u`'s set.

Striver's lesson implements both **union by rank** and **union by size**; size is shown here because it also answers `size(u)`.

| Input | Output | Why |
|---|---|---|
| `n = 7; unite(0,1), unite(1,2), unite(3,4), unite(5,6)` | `connected(0,2) = true, connected(2,3) = false` | {0,1,2} {3,4} {5,6} |
| `then unite(4,5); size(6)` | `4` | {3,4,5,6} |

**Constraints:** `1 ≤ n ≤ 10⁵`, up to `10⁵` operations.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Naive parent pointers | link root of u under root of v; no balancing | O(n) per op worst case | O(n) |
| Union by size + path compression | smaller root under larger; find flattens the path | O(α(n)) amortised | O(n) |

> [!tip] Interview angle
> Say the two optimisations by name and what each guarantees: union by size/rank keeps height O(log n) on its own; path compression on its own is O(log n) amortised; both together are O(α(n)). Write `find` recursively with compression (`p[x] = find(p[x])`), or iteratively with path halving if recursion depth worries you.

---

## 3. Naive parent pointers

**Intuition.** Same tree representation but always link the first root under the second and never compress. A chain `unite(0,1), unite(1,2), …` builds a path of height n, so `find` degrades to O(n).

```python
class NaiveDSU:
    def __init__(self, n):
        self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            x = self.p[x]
        return x
    def unite(self, u, v):
        a, b = self.find(u), self.find(v)
        if a != b:
            self.p[a] = b
    def connected(self, u, v):
        return self.find(u) == self.find(v)
    def size(self, u):
        r = self.find(u)
        return sum(self.find(x) == r for x in range(len(self.p)))
```

**Complexity:** time **O(n) per op worst case**, space **O(n)**.

---

## 4. Union by size + path compression

**Intuition.** Keep `parent[]` and `sz[]` (valid at roots). `find(x)`: if `x` is not a root, set `parent[x] = find(parent[x])` so every node on the path now points straight at the root. `unite`: find both roots; if equal stop; otherwise attach the smaller-size root under the larger and add the sizes.

**Algorithm**

1. `parent[i] = i`, `sz[i] = 1`.
2. `find(x)`: `x == parent[x]` ? x : `parent[x] = find(parent[x])`.
3. `unite(u, v)`: `a = find(u)`, `b = find(v)`; if `a == b` return; if `sz[a] < sz[b]` swap; `parent[b] = a`; `sz[a] += sz[b]`.
4. `connected` compares roots; `size(u)` returns `sz[find(u)]`.

**Dry run** — unite(0,1): root 0 size 2. unite(1,2): find(1) = 0, 2 joins → size 3. unite(3,4), unite(5,6). unite(4,5): roots 3 and 5, equal sizes → 5 under 3, sz[3] = 4. size(6): find(6) → 5 → 3, path compressed to 6 → 3; answer 4.

**C++**
```cpp
class DisjointSet {
    vector<int> parent, sz;
public:
    DisjointSet(int n) : parent(n), sz(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }
    void unite(int u, int v) {
        int a = find(u), b = find(v);
        if (a == b) return;
        if (sz[a] < sz[b]) swap(a, b);
        parent[b] = a;
        sz[a] += sz[b];
    }
    bool connected(int u, int v) { return find(u) == find(v); }
    int size(int u) { return sz[find(u)]; }
};
```

**Java**
```java
static class DisjointSet {
    private final int[] parent, sz;
    DisjointSet(int n) {
        parent = new int[n];
        sz = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; sz[i] = 1; }
    }
    int find(int x) {
        return parent[x] == x ? x : (parent[x] = find(parent[x]));
    }
    void unite(int u, int v) {
        int a = find(u), b = find(v);
        if (a == b) return;
        if (sz[a] < sz[b]) { int t = a; a = b; b = t; }
        parent[b] = a;
        sz[a] += sz[b];
    }
    boolean connected(int u, int v) { return find(u) == find(v); }
    int size(int u) { return sz[find(u)]; }
}
```

**Python**
```python
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.sz = [1] * n
    def find(self, x):
        while self.parent[x] != x:                      # path halving
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def unite(self, u, v):
        a, b = self.find(u), self.find(v)
        if a == b:
            return
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.parent[b] = a
        self.sz[a] += self.sz[b]
    def connected(self, u, v):
        return self.find(u) == self.find(v)
    def size(self, u):
        return self.sz[self.find(u)]
```

**Complexity:** time **O(α(n)) amortised**, space **O(n)** — α is the inverse Ackermann function; the bound needs both optimisations.

---

## Edge cases

- `unite(x, x)` or uniting two already-joined nodes: no-op, sizes unchanged.
- 1-indexed problems: allocate `n + 1`.
- Recursive `find` on 10⁵ nodes before any compression: fine with union by size (height ≤ log n), risky without it.

---

## Common mistakes

1. Comparing `parent[u] == parent[v]` instead of `find(u) == find(v)`.
2. Updating `sz` at the non-root, or reading `sz[u]` without `find`.
3. Linking `u` under `v` (the nodes) instead of root under root.

---

## Follow-ups

1. Union by rank vs by size?
2. Support delete / split?
3. Count components?

<details><summary>Answer sketches</summary>

**#1:** Equivalent bounds. Rank is an upper bound on height and only increments on ties; size also gives component sizes for free.

**#2:** Plain DSU cannot split. Offline: process in reverse (deletions become unions). Online: needs link-cut trees, out of scope.

**#3:** Start at n; decrement on every successful union.
</details>

---

## Flashcards

**DSU two optimisations?** #flashcard
Union by size/rank + path compression → O(α(n)) amortised.

**DSU `find` with compression (one line)?** #flashcard
`return p[x] == x ? x : p[x] = find(p[x]);`

**DSU `size` valid where?** #flashcard
Only at roots: `sz[find(u)]`.

**Interview track →** [Union-find deep-dive](../../02-algorithms/14-union-find.md)
