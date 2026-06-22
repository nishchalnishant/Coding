# Amazon SDE-2 — Pattern Triggers & Approach Templates

## How to use this
Read the problem → match trigger → apply template. Speed in pattern recognition is the differentiator at SDE-2.

---

## Pattern 1: Sliding Window

**Trigger words:** longest/shortest subarray/substring, at most K distinct, minimum window, contiguous subarray

**Fixed window:**
```
l = 0
for r in range(n):
    window.add(arr[r])
    if r - l + 1 == k:
        # process window
        window.remove(arr[l])
        l += 1
```

**Variable window (shrink when invalid):**
```
l = 0
for r in range(n):
    window.add(arr[r])
    while window_invalid():
        window.remove(arr[l])
        l += 1
    ans = max(ans, r - l + 1)
```

---

## Pattern 2: Two Pointers

**Trigger words:** sorted array, pair with target sum, palindrome check, in-place partition

**Opposite ends:**
```
l, r = 0, n - 1
while l < r:
    if condition: return (l, r)
    elif too_small: l += 1
    else: r -= 1
```

**Same direction (fast/slow):**
```
slow = 0
for fast in range(n):
    if keep(arr[fast]):
        arr[slow] = arr[fast]
        slow += 1
```

---

## Pattern 3: Prefix Sum

**Trigger words:** subarray sum equals K, number of subarrays with sum/product, range sum queries

```
prefix = {0: 1}  # or {0: [0]} for indices
running = 0
for x in arr:
    running += x
    if running - k in prefix:
        ans += prefix[running - k]
    prefix[running] = prefix.get(running, 0) + 1
```

---

## Pattern 4: BFS (level-order / shortest path)

**Trigger words:** shortest path, minimum steps, level by level, nearest X

```
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

**Multi-source BFS:** initialize queue with ALL sources at once, same template.

---

## Pattern 5: DFS on Tree / Graph

**Trigger words:** path sum, all paths, subtree, connected components, cycle detect

```
def dfs(node, state):
    if base_case: return value
    left = dfs(node.left, new_state)
    right = dfs(node.right, new_state)
    # post-order: combine left + right
    return combined
```

**Graph DFS with visited:**
```
visited = set()
def dfs(node):
    visited.add(node)
    for nb in graph[node]:
        if nb not in visited:
            dfs(nb)
```

---

## Pattern 6: Topological Sort (Kahn's BFS)

**Trigger words:** course schedule, dependency order, build order, detect cycle in directed graph

```
from collections import deque, defaultdict
indegree = defaultdict(int)
graph = defaultdict(list)
# build graph + indegree
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

## Pattern 7: Union-Find

**Trigger words:** connected components, cycle in undirected graph, redundant connection, accounts merge

```
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

## Pattern 8: Monotonic Stack

**Trigger words:** next greater/smaller element, largest rectangle, daily temperatures, stock span

**Monotonic Decreasing (next greater):**
```
stack = []  # stores indices
for i, val in enumerate(arr):
    while stack and arr[stack[-1]] < val:
        idx = stack.pop()
        ans[idx] = i - idx  # or val
    stack.append(i)
```

**Monotonic Increasing (next smaller / largest rect):**
```
stack = []
for i in range(n + 1):
    while stack and (i == n or arr[stack[-1]] > arr[i]):
        h = arr[stack.pop()]
        w = i if not stack else i - stack[-1] - 1
        ans = max(ans, h * w)
    stack.append(i)
```

---

## Pattern 9: Dynamic Programming — Decision Template

**Trigger words:** maximum/minimum cost, number of ways, can you achieve X, optimal subsequence

```
# 1. Define state: dp[i] = answer for subproblem of size i
# 2. Recurrence: dp[i] = f(dp[i-1], dp[i-2], ...)
# 3. Base cases: dp[0], dp[1]
# 4. Answer: dp[n]

# 2D (strings / grids):
dp = [[0] * (m+1) for _ in range(n+1)]
for i in range(1, n+1):
    for j in range(1, m+1):
        if match: dp[i][j] = dp[i-1][j-1] + 1
        else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

---

## Pattern 10: Binary Search on Answer

**Trigger words:** minimize the maximum, maximize the minimum, "is X possible with mid capacity", feasibility check

```
lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        hi = mid       # minimize: go left
        # lo = mid + 1  # maximize: go right
    else:
        lo = mid + 1   # minimize
        # hi = mid - 1  # maximize
return lo
```

---

## Pattern 11: Backtracking Template

**Trigger words:** all subsets, all permutations, all combinations, generate all valid X

```
def backtrack(start, current):
    if is_solution(current):
        result.append(current[:])
        return
    for i in range(start, n):
        if should_skip(i): continue  # prune / skip duplicates
        current.append(candidates[i])
        backtrack(i + 1, current)    # i+1 = no reuse; i = reuse allowed
        current.pop()
```

---

## Pattern 12: Heap Patterns

**Top K elements:** min-heap of size K → O(n log k)
**K-th largest:** min-heap size K; root = answer
**Merge K sorted:** min-heap with (val, list_idx, elem_idx)
**Median stream:** max-heap (lower) + min-heap (upper); balance sizes

---

## Pattern 13: Two Heaps (Median / Scheduling)

```
import heapq
lo = []  # max-heap (negate values)
hi = []  # min-heap

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

## Pattern 14: Trie

**Trigger words:** word search, prefix matching, autocomplete, start with prefix

```
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
```

---

## Complexity Quick-Reference

| Pattern | Time | Space |
|---|---|---|
| Sliding Window | O(n) | O(k) |
| Two Pointers | O(n) | O(1) |
| BFS/DFS | O(V+E) | O(V) |
| Topological Sort | O(V+E) | O(V) |
| Union-Find | O(α(n)) per op | O(n) |
| Heap (top-k) | O(n log k) | O(k) |
| Binary Search on answer | O(n log(range)) | O(1) |
| Backtracking (subsets) | O(2^n) | O(n) |
| DP (2D) | O(n*m) | O(n*m) or O(m) |
| Monotonic Stack | O(n) | O(n) |
