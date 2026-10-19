---
module: striver/27-graphs
lesson: 19
topic: Course Schedule II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/course-schedule-ii?category=hard-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, topological-sort]
---
# 19. Course Schedule II

← [Course Schedule I](18-course-schedule-i.md) · [Part 27 index](README.md) · Next → [Alien dictionary](20-alien-dictionary.md)

> [!abstract] Problem at a glance
> **Task:** Return any order in which all `n` courses can be taken (prerequisite `[a, b]`: `b` before `a`), or an empty list if impossible.
> **Key insight:** Same graph as Course Schedule I, but now output Kahn's processing order. If the order has fewer than `n` courses, a cycle blocked the rest, so return `[]`.
> **Difficulty:** Medium · **Pattern:** Topological sort with output · **Also on:** LC 210
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/course-schedule-ii?category=hard-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS reverse post-order](#3-dfs-reverse-post-order) · [4. Kahn's algorithm](#4-kahns-algorithm) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

There are `numCourses` courses and prerequisite pairs `[a, b]` meaning `b` must be taken before `a`. Return any valid ordering of all courses, or `[]` if none exists.

| Input | Output | Why |
|---|---|---|
| `n = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]` | `[0,1,2,3] or [0,2,1,3]` | 3 needs both 1 and 2 |
| `n = 2, prerequisites = [[1,0],[0,1]]` | `[]` | cycle |

**Constraints:** `1 ≤ n ≤ 2000`, `0 ≤ prerequisites.length ≤ n·(n−1)`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS reverse post-order | 3-state DFS; reversed finish order | O(V + E) | O(V) |
| Kahn's algorithm | pop in-degree-0 courses in order | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Many valid orders exist; the checker accepts any of them. Explain why Kahn's order is valid: a course is popped only after its in-degree reaches 0, i.e. after every prerequisite has been popped.

---

## 3. DFS reverse post-order

**Intuition.** DFS on `b → a` with cycle detection; append nodes on finish, then reverse. Return `[]` on a back edge.

```python
import sys

def find_order_dfs(n, pre):
    sys.setrecursionlimit(10 ** 6)
    adj = [[] for _ in range(n)]
    for a, b in pre:
        adj[b].append(a)
    st = [0] * n
    out = []
    def go(u):
        st[u] = 1
        for v in adj[u]:
            if st[v] == 1 or (st[v] == 0 and not go(v)):
                return False
        st[u] = 2
        out.append(u)
        return True
    for i in range(n):
        if st[i] == 0 and not go(i):
            return []
    return out[::-1]
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. Kahn's algorithm

**Intuition.** Exactly Course Schedule I, recording each popped course. Return it if it has length `n`, else `[]`.

**Algorithm**

1. Build `b → a`, in-degrees.
2. Queue in-degree-0 courses.
3. Pop → append → decrement dependants → queue new zeros.
4. Return the order if it has `n` entries, else `[]`.

**Dry run** — [[1,0],[2,0],[3,1],[3,2]]: queue 0 → frees 1, 2 → pop 1 (indeg[3] 1) → pop 2 (indeg[3] 0) → pop 3. Order [0,1,2,3].

**C++**
```cpp
vector<int> findOrder(int n, vector<vector<int>>& pre) {
    vector<vector<int>> adj(n);
    vector<int> indeg(n, 0), order;
    for (auto& p : pre) { adj[p[1]].push_back(p[0]); indeg[p[0]]++; }
    queue<int> q;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    if ((int)order.size() != n) order.clear();
    return order;
}
```

**Java**
```java
static int[] findOrder(int n, int[][] pre) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[n];
    for (int[] p : pre) { adj.get(p[1]).add(p[0]); indeg[p[0]]++; }
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.add(i);
    int[] order = new int[n];
    int k = 0;
    while (!q.isEmpty()) {
        int u = q.poll();
        order[k++] = u;
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.add(v);
    }
    return k == n ? order : new int[0];
}
```

**Python**
```python
from collections import deque

def find_order(n, pre):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in pre:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — the standard Kahn traversal.

---

## Edge cases

- No prerequisites: any permutation.
- Cycle: `[]`.
- Duplicate prerequisite pairs: in-degree counts both copies and both decrements happen; still correct.

---

## Common mistakes

1. Building `a → b` and outputting a reversed order.
2. Returning a partial order when a cycle exists.
3. Java: returning `null` instead of `new int[0]`.

---

## Follow-ups

1. Minimum number of semesters if you can take any number of courses per semester?
2. At most k courses per semester (LC 1494)?

<details><summary>Answer sketches</summary>

**#1:** Number of Kahn levels (process the queue in batches).

**#2:** NP-hard in general; bitmask DP for n ≤ 15.
</details>

---

## Flashcards

**Course Schedule II output?** #flashcard
Kahn's pop order, or [] if fewer than n popped.

**Why is Kahn's order valid?** #flashcard
A node is popped only after all its prerequisites were popped.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../coding/algorithms/13-graph-algorithms.md)
