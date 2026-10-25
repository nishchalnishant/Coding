---
module: striver-a2z/27-graphs
lesson: 18
topic: Course Schedule I
difficulty: Medium
source: https://takeuforward.org/learning/dsa/course-schedule-i?category=hard-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, topological-sort]
---
# 18. Course Schedule I

← [Find eventual safe states](17-find-eventual-safe-states.md) · [Part 27 index](README.md) · Next → [Course Schedule II](19-course-schedule-ii.md)

> [!abstract] Problem at a glance
> **Task:** Given `n` courses and prerequisite pairs `[a, b]` (take `b` before `a`), return whether all courses can be finished.
> **Key insight:** Courses are nodes and the edge `b → a` means `b` comes before `a`. Every course can be finished iff that graph has no cycle, i.e. iff Kahn's algorithm processes all `n` nodes. Watch the edge direction: `[a, b]` means `b → a`.
> **Difficulty:** Medium · **Pattern:** Topological sort feasibility · **Also on:** LC 207
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/course-schedule-i?category=hard-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DFS cycle detection](#3-dfs-cycle-detection) · [4. Kahn's algorithm](#4-kahns-algorithm) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

There are `numCourses` courses labelled `0..n-1`. `prerequisites[i] = [a, b]` means you must take `b` before `a`. Return `true` if you can finish all courses.

| Input | Output | Why |
|---|---|---|
| `n = 2, prerequisites = [[1,0]]` | `true` | take 0 then 1 |
| `n = 2, prerequisites = [[1,0],[0,1]]` | `false` | mutual dependency |

**Constraints:** `1 ≤ n ≤ 2000`, `0 ≤ prerequisites.length ≤ 5000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DFS cycle detection | 3-state DFS over b → a | O(V + E) | O(V) |
| Kahn's algorithm | process in-degree 0 courses; all n processed? | O(V + E) | O(V + E) |

> [!tip] Interview angle
> Say 'this is cycle detection in a directed graph' immediately, then code Kahn. Either edge direction gives the right boolean, but Course Schedule II needs the correct one, so set it up properly here.

---

## 3. DFS cycle detection

**Intuition.** Build `b → a` and run the grey/black DFS; any back edge means some courses can never be taken.

```python
import sys

def can_finish_dfs(n, pre):
    sys.setrecursionlimit(10 ** 6)
    adj = [[] for _ in range(n)]
    for a, b in pre:
        adj[b].append(a)
    st = [0] * n
    def cyc(u):
        st[u] = 1
        for v in adj[u]:
            if st[v] == 1 or (st[v] == 0 and cyc(v)):
                return True
        st[u] = 2
        return False
    return not any(st[i] == 0 and cyc(i) for i in range(n))
```

**Complexity:** time **O(V + E)**, space **O(V)**.

---

## 4. Kahn's algorithm

**Intuition.** In-degree of `a` = number of its prerequisites. Courses with none can be taken now; taking one reduces its dependants' counts.

**Algorithm**

1. For each `[a, b]`: `adj[b].append(a)`, `indeg[a]++`.
2. Queue every course with in-degree 0.
3. Pop, count, decrement dependants, queue new zeros.
4. Return `count == n`.

**Dry run** — n = 4, [[1,0],[2,1],[3,2]]: queue 0 → frees 1 → frees 2 → frees 3. count = 4 → true.

**C++**
```cpp
bool canFinish(int n, vector<vector<int>>& pre) {
    vector<vector<int>> adj(n);
    vector<int> indeg(n, 0);
    for (auto& p : pre) { adj[p[1]].push_back(p[0]); indeg[p[0]]++; }
    queue<int> q;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.push(i);
    int done = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        done++;
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    return done == n;
}
```

**Java**
```java
static boolean canFinish(int n, int[][] pre) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[n];
    for (int[] p : pre) { adj.get(p[1]).add(p[0]); indeg[p[0]]++; }
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.add(i);
    int done = 0;
    while (!q.isEmpty()) {
        int u = q.poll();
        done++;
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.add(v);
    }
    return done == n;
}
```

**Python**
```python
from collections import deque

def can_finish(n, pre):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in pre:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return done == n
```

**Complexity:** time **O(V + E)**, space **O(V + E)** — the standard Kahn traversal.

---

## Edge cases

- No prerequisites: true.
- A self-prerequisite `[a, a]`: false.
- A cycle among a subset of courses: false even if the rest is fine.

---

## Common mistakes

1. Reversing the pair meaning (harmless for I, fatal for II).
2. Returning `queue empty` instead of comparing the processed count with `n`.

---

## Follow-ups

1. Return an order (Course Schedule II)?
2. Course Schedule IV: is `u` a prerequisite of `v`, for many queries?

<details><summary>Answer sketches</summary>

**#1:** Collect the popped nodes; return `[]` if fewer than n.

**#2:** Precompute reachability: Floyd-Warshall boolean closure (n ≤ 100) or a bitset per node in topo order.
</details>

---

## Flashcards

**Course Schedule I reduces to…?** #flashcard
Cycle detection in the prerequisite digraph.

**Edge for prerequisite `[a, b]`?** #flashcard
`b → a`.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
