# Amazon SDE-2 — Pattern Triggers & Approach Templates

Ordered by priority — same order as coding-questions.md. Master Tier 1 templates before touching Tier 3.

---

## TIER 1 — Must Know Cold

---

### Pattern 1: BFS (Trees + Graphs)

**Trigger words:** level order, shortest path, minimum steps, nearest X, rotting/spreading

**Level-order / shortest path:**
```python
from collections import deque
q = deque([start])
visited = {start}
steps = 0
while q:
    for _ in range(len(q)):
        node = q.popleft()
        if node == target: return steps
        for nb in neighbors(node):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
    steps += 1
```

**Multi-source BFS:** initialize queue with ALL sources at step 0, same template.

---

### Pattern 2: DFS on Tree / Graph

**Trigger words:** path sum, all paths, subtree check, connected components, flood fill, cycle detect

**Tree DFS (post-order — most common):**
```python
def dfs(node):
    if not node: return base_value
    left = dfs(node.left)
    right = dfs(node.right)
    # combine left + right at current node
    return combined
```

**Graph DFS with visited:**
```python
visited = set()
def dfs(node):
    visited.add(node)
    for nb in graph[node]:
        if nb not in visited:
            dfs(nb)
```

---

### Pattern 3: Dynamic Programming

**Trigger words:** maximum/minimum cost, number of ways, can you achieve X, optimal subsequence, count paths

**1D DP:**
```python
dp = [initial] * (n + 1)
dp[0] = base_case
for i in range(1, n + 1):
    dp[i] = f(dp[i-1], dp[i-2], ...)
return dp[n]
```

**2D DP (strings / grids):**
```python
dp = [[0] * (m+1) for _ in range(n+1)]
for i in range(1, n+1):
    for j in range(1, m+1):
        if match:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Decision checklist:**
1. Define state: `dp[i]` = answer for subproblem ending at i
2. Write recurrence: how does `dp[i]` depend on previous states?
3. Set base cases
4. Identify answer: `dp[n]` or `max(dp)`

---

### Pattern 4: Sliding Window

**Trigger words:** longest/shortest subarray/substring, at most K distinct, minimum window, contiguous

**Fixed window:**
```python
l = 0
for r in range(n):
    window.add(arr[r])
    if r - l + 1 == k:
        # process window
        window.remove(arr[l])
        l += 1
```

**Variable window (shrink when invalid):**
```python
l = 0
for r in range(n):
    window.add(arr[r])
    while window_invalid():
        window.remove(arr[l])
        l += 1
    ans = max(ans, r - l + 1)
```

---

### Pattern 5: Two Pointers

**Trigger words:** sorted array, pair sum, palindrome check, in-place partition, remove duplicates

**Opposite ends:**
```python
l, r = 0, n - 1
while l < r:
    if condition: return (l, r)
    elif too_small: l += 1
    else: r -= 1
```

**Fast/slow (same direction):**
```python
slow = 0
for fast in range(n):
    if keep(arr[fast]):
        arr[slow] = arr[fast]
        slow += 1
```

---

### Pattern 6: Prefix Sum

**Trigger words:** subarray sum equals K, number of subarrays with sum, range sum queries

```python
prefix = {0: 1}
running = 0
for x in arr:
    running += x
    if running - k in prefix:
        ans += prefix[running - k]
    prefix[running] = prefix.get(running, 0) + 1
```

---

### Pattern 7: Topological Sort (Kahn's BFS)

**Trigger words:** course schedule, dependency order, build order, cycle in directed graph

```python
from collections import deque, defaultdict
indegree = defaultdict(int)
graph = defaultdict(list)
# build graph + indegree from edges

q = deque([n for n in nodes if indegree[n] == 0])
order = []
while q:
    node = q.popleft()
    order.append(node)
    for nb in graph[node]:
        indegree[nb] -= 1
        if indegree[nb] == 0:
            q.append(nb)
# cycle exists if len(order) != total nodes
```

---

### Pattern 8: Heap — Top-K / Median

**Top K elements:** min-heap of size K → evict when size > K → O(n log k)
**K-th largest:** min-heap size K; root = answer
**Merge K sorted:** min-heap with `(val, list_idx, elem_idx)`

**Two Heaps (median from stream):**
```python
import heapq
lo = []  # max-heap (negate values) — lower half
hi = []  # min-heap — upper half

def add(num):
    heapq.heappush(lo, -num)
    heapq.heappush(hi, -heapq.heappop(lo))
    if len(hi) > len(lo):
        heapq.heappush(lo, -heapq.heappop(hi))

def get_median():
    if len(lo) > len(hi): return -lo[0]
    return (-lo[0] + hi[0]) / 2
```

---

## TIER 2 — High Probability

---

### Pattern 9: Intervals

**Trigger words:** overlapping intervals, meeting rooms, schedule, free time, merge ranges

```python
intervals.sort(key=lambda x: x[0])
merged = [intervals[0]]
for start, end in intervals[1:]:
    if start <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], end)
    else:
        merged.append([start, end])
```

**Meeting Rooms II (min rooms needed):**
```python
import heapq
intervals.sort()
heap = []  # end times
for start, end in intervals:
    if heap and heap[0] <= start:
        heapq.heappop(heap)
    heapq.heappush(heap, end)
return len(heap)
```

---

### Pattern 10: Binary Search on Answer (Parametric)

**Trigger words:** minimize the maximum, maximize the minimum, "is X possible with capacity mid"

```python
lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        hi = mid        # minimizing
        # lo = mid + 1  # maximizing
    else:
        lo = mid + 1    # minimizing
        # hi = mid - 1  # maximizing
return lo
```

**Standard binary search (sorted array):**
```python
lo, hi = 0, n - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
return -1
```

---

### Pattern 11: Union-Find

**Trigger words:** connected components, cycle in undirected graph, accounts merge, redundant connection

```python
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # path compression
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py: return False  # already connected
    if rank[px] < rank[py]: px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]: rank[px] += 1
    return True
```

---

## TIER 3 — Know the Template

---

### Pattern 12: Monotonic Stack

**Trigger words:** next greater/smaller element, largest rectangle, daily temperatures, stock span

**Monotonic Decreasing (next greater):**
```python
stack = []  # indices
for i, val in enumerate(arr):
    while stack and arr[stack[-1]] < val:
        idx = stack.pop()
        ans[idx] = i - idx  # or val
    stack.append(i)
```

**Monotonic Increasing (next smaller / largest rectangle):**
```python
stack = []
for i in range(n + 1):
    while stack and (i == n or arr[stack[-1]] > arr[i]):
        h = arr[stack.pop()]
        w = i if not stack else i - stack[-1] - 1
        ans = max(ans, h * w)
    stack.append(i)
```

---

### Pattern 13: Backtracking

**Trigger words:** all subsets, all permutations, all combinations, generate all valid X

```python
def backtrack(start, current):
    if is_solution(current):
        result.append(current[:])
        return
    for i in range(start, n):
        if should_skip(i): continue  # prune duplicates
        current.append(candidates[i])
        backtrack(i + 1, current)    # i+1 = no reuse; i = reuse allowed
        current.pop()
```

---

## TIER 4 — Skim Only

---

### Pattern 14: Dijkstra (Weighted Shortest Path)

**Trigger words:** cheapest path, minimum cost route, weighted graph

```python
import heapq
dist = {node: float('inf') for node in graph}
dist[src] = 0
heap = [(0, src)]
while heap:
    d, u = heapq.heappop(heap)
    if d > dist[u]: continue
    for v, w in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(heap, (dist[v], v))
```

---

### Pattern 15: Trie

**Trigger words:** prefix search, autocomplete, word dictionary, starts with

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self): self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.children.setdefault(c, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children: return False
            node = node.children[c]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children: return False
            node = node.children[c]
        return True
```

---

## Complexity Quick-Reference

| Pattern | Time | Space |
|---|---|---|
| BFS / DFS | O(V+E) | O(V) |
| DP (1D) | O(n) | O(n) or O(1) |
| DP (2D) | O(n·m) | O(n·m) or O(m) |
| Sliding Window | O(n) | O(k) |
| Two Pointers | O(n) | O(1) |
| Prefix Sum | O(n) | O(n) |
| Topological Sort | O(V+E) | O(V) |
| Union-Find | O(α(n)) per op | O(n) |
| Heap top-K | O(n log k) | O(k) |
| Binary Search on answer | O(n log(range)) | O(1) |
| Monotonic Stack | O(n) | O(n) |
| Backtracking (subsets) | O(2^n) | O(n) |
| Dijkstra | O((V+E) log V) | O(V) |
