---
tags: [coding, amazon-interview, patterns, templates, quick-reference]
topic: Pattern Templates & Quick Reference — Amazon SDE-2
difficulty: reference
---

# Pattern Templates & Quick Reference — Amazon SDE-2




> [!tip] How to Use This
> These are exact code templates to internalize. In an interview, you should be able to write any of these from memory within 2 minutes. Study one pattern per day.

---

## Pattern 1: Sliding Window

**Trigger**: "subarray/substring of length k", "minimum/maximum window", "longest with condition"

### Fixed-Size Window
```python
def max_sum_subarray_k(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

### Variable-Size Window (Shrink when invalid)
```python
def longest_substr_no_repeat(s):
    freq = {}
    left = 0
    max_len = 0
    for right, c in enumerate(s):
        freq[c] = freq.get(c, 0) + 1
        while freq[c] > 1:              # window invalid
            freq[s[left]] -= 1
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len
```

### Minimum Window (Shrink after valid)
```python
def min_window(s, t):
    need = Counter(t)
    have, total = {}, 0
    left, min_len, res = 0, float('inf'), ""
    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            total += 1
        while total == len(need):       # window valid — shrink
            if right - left + 1 < min_len:
                min_len = right - left + 1
                res = s[left:right+1]
            have[s[left]] -= 1
            if s[left] in need and have[s[left]] < need[s[left]]:
                total -= 1
            left += 1
    return res
```

---

## Pattern 2: Two Pointers

**Trigger**: sorted array, pairs summing to target, palindrome check, partition

### Converging (opposite ends)
```python
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target: return [left, right]
        elif s < target: left += 1
        else: right -= 1
    return []
```

### Fast/Slow (Floyd's cycle detection)
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def find_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow
```

---

## Pattern 3: Binary Search

**Trigger**: sorted array, "minimum X that satisfies Y", "find boundary"

```python
# Template — find leftmost position satisfying condition
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2      # avoid overflow
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Binary search on answer
def min_days(piles, h):
    def can_finish(speed):
        return sum((p + speed - 1) // speed for p in piles) <= h

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid           # valid → try smaller
        else:
            lo = mid + 1       # invalid → need bigger
    return lo
```

**Common pitfalls:**
- Use `lo + (hi - lo) // 2` not `(lo + hi) // 2` — avoids integer overflow
- `lo < hi` for answer-search; `lo <= hi` for find-exact
- When `can_finish(mid)` is True, set `hi = mid` (not `mid - 1`) for answer search

---

## Pattern 4: DFS Templates

### Graph DFS (iterative)
```python
def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

### Tree DFS (recursive)
```python
def dfs_tree(root):
    if not root:
        return
    # Pre-order: process here
    dfs_tree(root.left)
    # In-order: process here
    dfs_tree(root.right)
    # Post-order: process here
```

### Grid DFS
```python
def dfs_grid(grid, r, c, visited):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if visited[r][c] or grid[r][c] == 0:
        return
    visited[r][c] = True
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        dfs_grid(grid, r+dr, c+dc, visited)
```

---

## Pattern 5: BFS Templates

### Graph BFS (shortest path)
```python
from collections import deque

def bfs_shortest_path(graph, start, target):
    queue = deque([(start, 0)])  # (node, distance)
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1
```

### Multi-Source BFS
```python
def bfs_multi_source(grid):
    queue = deque()
    visited = set()
    # Add ALL sources first
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == SOURCE:
                queue.append((r, c, 0))
                visited.add((r, c))
    while queue:
        r, c, dist = queue.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if (0 <= nr < len(grid) and 0 <= nc < len(grid[0])
                    and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
```

---

## Pattern 6: Topological Sort

**Trigger**: dependencies, prerequisites, ordering constraints, DAG

```python
from collections import defaultdict, deque

def topo_sort_kahn(n, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * n
    for a, b in prerequisites:
        graph[b].append(a)
        in_degree[a] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == n else []  # empty = cycle exists
```

---

## Pattern 7: Dijkstra's Algorithm

**Trigger**: weighted graph, shortest path, minimum cost

```python
import heapq
from collections import defaultdict

def dijkstra(n, edges, src):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((w, v))

    dist = [float('inf')] * n
    dist[src] = 0
    heap = [(0, src)]   # (cost, node)

    while heap:
        cost, node = heapq.heappop(heap)
        if cost > dist[node]:   # stale entry — skip
            continue
        for w, neighbor in graph[node]:
            new_cost = cost + w
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))

    return dist
```

---

## Pattern 8: Union-Find

**Trigger**: connected components, cycle detection, Kruskal's MST

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False   # already connected (cycle!)
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x, y) -> bool:
        return self.find(x) == self.find(y)
```

---

## Pattern 9: Monotonic Stack

**Trigger**: "next greater element", "largest rectangle", "daily temperatures", "stock span"

```python
# Next Greater Element
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # indices, decreasing values
    for i, n in enumerate(nums):
        while stack and nums[stack[-1]] < n:
            result[stack.pop()] = n
        stack.append(i)
    return result

# Largest Rectangle in Histogram
def largest_rectangle(heights):
    stack = []  # (index, height)
    max_area = 0
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
    return max_area
```

---

## Pattern 10: DP on Intervals

**Trigger**: "minimum cost to split/burst/merge", "score of optimal game on array"

```python
# Burst Balloons — classic interval DP
def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):           # interval length
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):  # k = LAST balloon to burst
                coins = (nums[left] * nums[k] * nums[right]
                         + dp[left][k] + dp[k][right])
                dp[left][right] = max(dp[left][right], coins)

    return dp[0][n - 1]
```

---

## Pattern 11: Tree DP

**Trigger**: "optimal assignment on tree nodes", "diameter", "max path sum"

```python
# Generic tree DP: return multiple values from each node
def tree_dp(root):
    ans = 0  # or float('-inf')

    def dfs(node):
        nonlocal ans
        if not node:
            return 0
        left = max(0, dfs(node.left))   # max(0,...) to ignore negative subtrees
        right = max(0, dfs(node.right))
        # Update global answer using both subtrees
        ans = max(ans, left + right + node.val)
        # Return single-arm gain upward
        return max(left, right) + node.val

    dfs(root)
    return ans

# House Robber III — two return values
def rob_tree(root):
    def dfs(node):
        if not node:
            return (0, 0)   # (rob_this_node, skip_this_node)
        left_rob, left_skip = dfs(node.left)
        right_rob, right_skip = dfs(node.right)
        rob = node.val + left_skip + right_skip
        skip = max(left_rob, left_skip) + max(right_rob, right_skip)
        return (rob, skip)
    return max(dfs(root))
```

---

## Pattern 12: Backtracking Template

```python
def backtrack(result, path, choices, start):
    # Base case: path is complete
    if is_complete(path):
        result.append(path[:])   # deep copy!
        return

    for i in range(start, len(choices)):
        # Pruning: skip invalid choices early
        if should_skip(choices, i, path):
            continue

        path.append(choices[i])         # choose
        backtrack(result, path, choices, next_start(i))  # explore
        path.pop()                       # unchoose
```

**Common pruning strategies:**
- `if sum(path) > target: continue` — prune over-budget paths
- `if i > start and choices[i] == choices[i-1]: continue` — skip duplicates
- `if n - i + 1 < k - len(path): break` — not enough elements left

---

## Pattern 13: LRU Cache

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()  # maintains insertion order

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)   # evict LRU (front)
```

---

## Pattern 14: Trie

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True
```

---

## Pattern 15: Heap Patterns

```python
import heapq

# Top-K Largest (min-heap of size K)
def top_k_largest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)
    return list(heap)   # K largest elements

# Top-K Smallest (max-heap: negate values)
def top_k_smallest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, -n)
        if len(heap) > k:
            heapq.heappop(heap)
    return [-x for x in heap]

# K-Way Merge
def merge_k_sorted(lists):
    result = []
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    return result
```

---

## Common Gotchas

| Gotcha | Wrong | Right |
|--------|-------|-------|
| Binary search mid | `(lo + hi) // 2` | `lo + (hi - lo) // 2` |
| Empty heap pop | `heap.pop()` | `heappop(heap)` — crashes if empty |
| In-order BST | Assumes left < right for immediate children | Must pass (lo, hi) bounds recursively |
| DFS visited set | Add before exploring | Add before exploring, not after returning |
| BFS visited set | Add when popping | Add when **pushing** (else duplicates in queue) |
| Prefix sum base | Start from index 0 | `prefix[0] = 0` then `prefix[i+1] = prefix[i] + arr[i]` |
| String immutability | `s += char` in loop | `''.join(chars)` |
| Modular arithmetic | `(a + b) % MOD` | `((a % MOD) + (b % MOD)) % MOD` |
| Graph init | `graph = {}` | `defaultdict(list)` |
| Comparing floats | `a == b` | `abs(a - b) < 1e-9` |

---

## Pattern Selector — "What do I use for this?"

| Problem type | Pattern |
|-------------|---------|
| Consecutive subarray/substring optimal | Sliding Window |
| Two elements in array summing to X | Two Pointers or Hash Map |
| Sorted array, find target | Binary Search |
| Shortest path (unweighted) | BFS |
| Shortest path (weighted, non-negative) | Dijkstra |
| Shortest path (negative weights) | Bellman-Ford |
| All-pairs shortest path | Floyd-Warshall |
| Connected components | BFS/DFS or Union-Find |
| Topological ordering | Kahn's BFS or DFS+visited |
| "Next greater/smaller element" | Monotonic Stack |
| "Optimal choice at each step" | Greedy or DP |
| Overlapping subproblems, optimal substructure | DP |
| Generate all possibilities | Backtracking |
| Prefix matching, autocomplete | Trie |
| K largest/smallest | Heap |
| Merge K sorted | Heap |
| Cycle detection | Floyd's Two Pointers or Union-Find |
| Minimum spanning tree | Kruskal (sort edges) or Prim (greedy) |
| Median of stream | Two Heaps (max-heap + min-heap) |

---

## See Also

- [Amazon Interview Strategy](./google-interview-strategy.md)
- [Complexity Cheat Sheet](./complexity-cheatsheet.md)
- [Dynamic Programming](./algorithms/dynamic-programming.md)
- [Graph Algorithms](./algorithms/graph-algorithms.md)
- [Backtracking](./algorithms/backtracking.md)
