# Language Templates (SDE-2)

These are interview-speed templates you should be able to type from memory. Target: each template in under 2 minutes without looking. Practice by closing this file and writing from scratch.

---

## Python

### BFS (graph)
```python
from collections import deque

def bfs(start, adj):
    q = deque([start])
    dist = {start: 0}
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

### BFS (grid, 4-dir)
```python
from collections import deque

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def bfs_grid(grid, sr, sc):
    R, C = len(grid), len(grid[0])
    q = deque([(sr, sc)])
    seen = {(sr, sc)}
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
```

### Topological sort (Kahn)
```python
from collections import deque, defaultdict

def topo(n, edges):   # edges: u -> v
    adj = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    q = deque([i for i in range(n) if indeg[i] == 0])
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

### Sliding window (at most K distinct)
```python
def at_most_k_distinct(nums, k):
    if k == 0:
        return 0
    freq = {}
    i = 0
    best = 0
    for j, x in enumerate(nums):
        freq[x] = freq.get(x, 0) + 1
        while len(freq) > k:
            freq[nums[i]] -= 1
            if freq[nums[i]] == 0:
                del freq[nums[i]]
            i += 1
        best = max(best, j - i + 1)
    return best
```

### Binary search (lower bound)
```python
def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

### Heap — min-heap and top-K patterns
```python
import heapq

# Min-heap (default)
h = []
heapq.heappush(h, val)
smallest = heapq.heappop(h)

# Max-heap: negate values
heapq.heappush(h, -val)
largest = -heapq.heappop(h)

# Top-K smallest — O(n log k)
def top_k_smallest(nums, k):
    return heapq.nsmallest(k, nums)

# K-th largest using size-k min-heap
def kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]  # root = k-th largest

# Heap with (priority, value) tuples — tie-break on second field
heapq.heappush(h, (priority, value))
```

### Monotonic stack (indices)
```python
# Next greater element — O(n)
def next_greater(nums):
    n = len(nums)
    res = [-1] * n
    stack = []  # stores indices, decreasing values
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            res[stack.pop()] = x
        stack.append(i)
    return res

# Largest rectangle in histogram — O(n)
def largest_rect(heights):
    stack = []  # indices of increasing heights
    max_area = 0
    heights = heights + [0]  # sentinel to flush stack
    for i, h in enumerate(heights):
        start = i
        while stack and heights[stack[-1]] > h:
            j = stack.pop()
            width = i - (stack[-1] + 1 if stack else 0)
            max_area = max(max_area, heights[j] * width)
            start = j
        stack.append(start)
    return max_area
```

### Binary search (upper bound)
```python
def upper_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo  # first index where a[i] > x
```

### DSU / Union-Find
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.count -= 1
        return True
```

---

## Java

### BFS (graph)
```java
Deque<Integer> q = new ArrayDeque<>();
Map<Integer, Integer> dist = new HashMap<>();
q.add(start);
dist.put(start, 0);

while (!q.isEmpty()) {
  int u = q.pollFirst();
  for (int v : adj.getOrDefault(u, List.of())) {
    if (!dist.containsKey(v)) {
      dist.put(v, dist.get(u) + 1);
      q.addLast(v);
    }
  }
}
```

### Topological sort (Kahn)
```java
List<List<Integer>> adj = new ArrayList<>();
for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
int[] indeg = new int[n];
for (int[] e : edges) { // e[0] -> e[1]
  adj.get(e[0]).add(e[1]);
  indeg[e[1]]++;
}

Deque<Integer> q = new ArrayDeque<>();
for (int i = 0; i < n; i++) if (indeg[i] == 0) q.addLast(i);
List<Integer> order = new ArrayList<>();

while (!q.isEmpty()) {
  int u = q.pollFirst();
  order.add(u);
  for (int v : adj.get(u)) {
    if (--indeg[v] == 0) q.addLast(v);
  }
}
// if (order.size() != n) => cycle
```

### Heap (PriorityQueue)
```java
// Min-heap (default)
PriorityQueue<Integer> minH = new PriorityQueue<>();

// Max-heap
PriorityQueue<Integer> maxH = new PriorityQueue<>(Comparator.reverseOrder());

// Custom comparator — e.g., sort intervals by end
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);

// K-th largest: maintain size-k min-heap
for (int x : nums) {
    minH.offer(x);
    if (minH.size() > k) minH.poll();
}
int kthLargest = minH.peek();
```

### Monotonic stack (next greater element)
```java
int n = nums.length;
int[] res = new int[n];
Arrays.fill(res, -1);
Deque<Integer> stack = new ArrayDeque<>(); // stores indices
for (int i = 0; i < n; i++) {
    while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
        res[stack.pop()] = nums[i];
    }
    stack.push(i);
}
```

### DSU / Union-Find
```java
class DSU {
  int[] parent, rank;
  DSU(int n) {
    parent = new int[n];
    rank = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
  }
  int find(int x) {
    if (parent[x] != x) parent[x] = find(parent[x]);
    return parent[x];
  }
  boolean union(int a, int b) {
    int ra = find(a), rb = find(b);
    if (ra == rb) return false;
    if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
    parent[rb] = ra;
    if (rank[ra] == rank[rb]) rank[ra]++;
    return true;
  }
}
```

