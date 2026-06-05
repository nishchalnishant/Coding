---
tags: [coding, google-interview, complexity, cheatsheet, big-o]
topic: Complexity Cheat Sheet
difficulty: reference
---

# Complexity Cheat Sheet — Complete Reference

> [!abstract] L3 Google Interview — Tier Legend
> `💤 T3` — **This entire file is TIER 3 / Lower Priority for L3.**
> Skim for conceptual awareness. Do NOT spend deep implementation time here.
> Redirect time to Tier 1 (graphs, binary search, heaps, tries) and Tier 2 (DP, backtracking, trees).




> [!tip] How to Use This
> Before every interview, scan this page for 10 minutes. When asked "what's the complexity?", your answer must include BOTH time AND space, and the WHY — not just the label.

---

## Big-O Quick Reference

```
O(1)        — constant     : hash lookup, array index access
O(log n)    — logarithmic  : binary search, balanced BST ops
O(n)        — linear       : single scan, BFS/DFS
O(n log n)  — linearithmic : merge sort, heap sort, most efficient comparison sorts
O(n²)       — quadratic    : nested loops, bubble sort, brute force pairs
O(n³)       — cubic        : matrix multiplication (naive), Floyd-Warshall
O(2^n)      — exponential  : all subsets, recursive fibonacci (no memo)
O(n!)       — factorial    : all permutations, brute-force TSP
```

**Growth order** (n = 10^6):
```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2^n) < O(n!)
  1  <    20    < 10^6 <   2×10^7   <  10^12 <  ∞    <  ∞
```

**Rule of thumb for interview:**
- n ≤ 20 → O(2^n) or O(n!) is fine
- n ≤ 500 → O(n²) is ok
- n ≤ 10^4 → O(n²) is borderline; O(n log n) is safe
- n ≤ 10^6 → O(n) or O(n log n)
- n ≤ 10^8 → O(n) only
- n ≤ 10^18 → O(log n) or O(1)

---

## Data Structure Operations

| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Dynamic Array (list) | O(1) amort. | O(n) | O(1) amort. | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) at head | O(1) if ptr known | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Map | O(1) avg | O(1) avg | O(1) avg | O(1) avg | O(n) |
| Hash Set | — | O(1) avg | O(1) avg | O(1) avg | O(n) |
| Binary Search Tree | O(h) | O(h) | O(h) | O(h) | O(n) |
| Balanced BST (AVL/RB) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Heap (Binary) | O(1) top | O(n) | O(log n) | O(log n) | O(n) |
| Trie | — | O(m) | O(m) | O(m) | O(ALPHABET × N × m) |
| Segment Tree | — | O(log n) | O(log n) | O(log n) | O(n) |
| Fenwick Tree (BIT) | — | O(log n) | O(log n) | O(log n) | O(n) |
| Disjoint Set (Union-Find) | — | O(α(n))≈O(1) | O(α(n))≈O(1) | — | O(n) |
| Skip List | O(log n) avg | O(log n) avg | O(log n) avg | O(log n) avg | O(n log n) |

*h = height; m = key length; α = inverse Ackermann (essentially constant)*

---

## Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable? |
|-----------|------|---------|-------|-------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅ |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n+k) | ✅ |
| Tim Sort (Python default) | O(n) | O(n log n) | O(n log n) | O(n) | ✅ |

**When to choose:**
- General purpose → Merge Sort (stable, predictable O(n log n))
- In-place, don't care about stability → Quick Sort (cache-friendly)
- Almost-sorted input → Insertion Sort (O(n) best case)
- Integers in small range → Counting Sort (O(n+k))
- Large numbers of strings → Radix Sort

---

## Graph Algorithm Complexities

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| BFS | O(V+E) | O(V) | Shortest path (unweighted), level-order |
| DFS | O(V+E) | O(V) | Connectivity, cycle detection, SCC |
| Topological Sort (Kahn's) | O(V+E) | O(V) | DAG ordering |
| Dijkstra (binary heap) | O((V+E) log V) | O(V) | Shortest path, non-negative weights |
| Dijkstra (Fibonacci heap) | O(E + V log V) | O(V) | Dense graphs, theoretical optimum |
| Bellman-Ford | O(VE) | O(V) | Shortest path with negative weights |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
| Prim's MST (binary heap) | O((V+E) log V) | O(V) | MST, dense graphs |
| Kruskal's MST | O(E log E) | O(V) | MST, sparse graphs |
| Kosaraju's SCC | O(V+E) | O(V) | Strongly connected components |
| Tarjan's SCC | O(V+E) | O(V) | SCC (single pass) |
| Bridge Finding (Tarjan) | O(V+E) | O(V) | Critical edges |

**V = vertices, E = edges**

---

## Dynamic Programming Complexities

| Problem | Time | Space | Optimized Space |
|---------|------|-------|-----------------|
| Fibonacci | O(n) | O(n) | O(1) |
| Climbing Stairs | O(n) | O(n) | O(1) |
| House Robber | O(n) | O(n) | O(1) |
| 0/1 Knapsack | O(n×W) | O(n×W) | O(W) |
| Unbounded Knapsack | O(n×W) | O(n×W) | O(W) |
| Longest Common Subsequence | O(m×n) | O(m×n) | O(min(m,n)) |
| Edit Distance | O(m×n) | O(m×n) | O(min(m,n)) |
| Unique Paths | O(m×n) | O(m×n) | O(n) |
| Longest Increasing Subsequence | O(n²) | O(n) | O(n log n) with BS |
| Coin Change | O(n×amount) | O(amount) | O(amount) |
| Burst Balloons | O(n³) | O(n²) | — |
| Matrix Chain Multiplication | O(n³) | O(n²) | — |
| Bitmask DP (TSP) | O(2^n × n²) | O(2^n × n) | — |
| Digit DP | O(digits × states) | varies | — |

---

## Tree Algorithm Complexities

| Operation | Balanced BST | Unbalanced BST | Heap |
|-----------|-------------|----------------|------|
| Search | O(log n) | O(n) | O(n) |
| Insert | O(log n) | O(n) | O(log n) |
| Delete | O(log n) | O(n) | O(log n) |
| Min/Max | O(log n) | O(n) | O(1) |
| Traverse | O(n) | O(n) | O(n) |

| Tree Problem | Time | Space |
|-------------|------|-------|
| BFS (level order) | O(n) | O(w) — w=max width |
| DFS (any order) | O(n) | O(h) — h=height |
| LCA | O(n) | O(h) |
| Serialize/Deserialize | O(n) | O(n) |
| Diameter | O(n) | O(h) |
| Max Path Sum | O(n) | O(h) |
| Validate BST | O(n) | O(h) |
| Kth Smallest BST | O(h + k) | O(h) |
| Morris Inorder | O(n) | O(1) |

---

## String Algorithm Complexities

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| Brute Force Search | O(n×m) | O(1) | n=text, m=pattern |
| KMP | O(n+m) | O(m) | Single pattern match |
| Rabin-Karp | O(n+m) avg, O(nm) worst | O(1) | Rolling hash, multiple patterns |
| Z-Algorithm | O(n+m) | O(n+m) | Pattern matching |
| Aho-Corasick | O(n + m + z) | O(m×Σ) | Multiple pattern match |
| Suffix Array | O(n log n) or O(n) | O(n) | All substring queries |
| Trie search | O(m) | — | m = query length |
| Palindrome (Manacher) | O(n) | O(n) | All palindromic substrings |
| Edit Distance | O(n×m) | O(n×m) | Dynamic programming |

---

## Heap / Priority Queue Complexities

| Operation | Binary Heap | Fibonacci Heap |
|-----------|------------|----------------|
| Insert | O(log n) | O(1) amortized |
| Extract Min/Max | O(log n) | O(log n) amortized |
| Peek Min/Max | O(1) | O(1) |
| Decrease Key | O(log n) | O(1) amortized |
| Merge | O(n) | O(1) |
| Build from array | O(n) | — |

**heapq in Python (min-heap):**
```python
heapq.heapify(arr)        # O(n)
heapq.heappush(h, x)      # O(log n)
heapq.heappop(h)          # O(log n)
heapq.nlargest(k, arr)    # O(n log k)
heapq.nsmallest(k, arr)   # O(n log k)
# Max heap: push -x, pop and negate
```

---

## Space Optimization Techniques

### Rolling Array (DP space reduction)

```python
# Before: O(n×m) space
dp = [[0]*(m+1) for _ in range(n+1)]
for i in range(1, n+1):
    for j in range(1, m+1):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]  # only need row i-1

# After: O(m) space
prev = [0]*(m+1)
for i in range(1, n+1):
    curr = [0]*(m+1)
    for j in range(1, m+1):
        curr[j] = prev[j] + curr[j-1]
    prev = curr
```

### 1D Knapsack (backward iteration)

```python
# Crucial: iterate j BACKWARD for 0/1 knapsack (each item used at most once)
dp = [0]*(W+1)
for item in items:
    for w in range(W, item.weight-1, -1):  # backward!
        dp[w] = max(dp[w], dp[w-item.weight] + item.value)

# Forward iteration = unbounded knapsack (item can be used multiple times)
for item in items:
    for w in range(item.weight, W+1):  # forward
        dp[w] = max(dp[w], dp[w-item.weight] + item.value)
```

### In-Place Array Tricks

```python
# Mark visited without extra space: negate value at index
# (works when values are positive indices)
for num in nums:
    idx = abs(num) - 1
    nums[idx] = -abs(nums[idx])  # mark as seen

# XOR trick: find missing number in [0..n]
missing = 0
for i, num in enumerate(nums):
    missing ^= (i+1) ^ num
```

---

## Amortized Analysis

Some operations are expensive occasionally but cheap on average:

| Structure | Operation | Worst Case | Amortized |
|-----------|-----------|------------|-----------|
| Dynamic Array | append | O(n) (resize) | O(1) |
| Stack | push/pop | O(1) | O(1) |
| Hash Map | insert | O(n) (rehash) | O(1) |
| Fibonacci Heap | insert | O(1) | O(1) |
| Splay Tree | any op | O(n) | O(log n) |
| Union-Find | union/find | O(log n) | O(α(n)) ≈ O(1) |

**Explanation for dynamic array:**
```
Start: capacity=1
After n inserts: capacity doubled k times where 2^k ≈ n
Total resize cost: 1 + 2 + 4 + ... + n = 2n = O(n)
Amortized per insert: O(n)/n = O(1)
```

---

## Master Theorem (Divide & Conquer)

For recurrences of the form: **T(n) = aT(n/b) + f(n)**

where a ≥ 1, b > 1, f(n) is the cost of dividing/combining:

```
Case 1: f(n) = O(n^(log_b(a) - ε))  →  T(n) = Θ(n^log_b(a))
        (subproblem work dominates)

Case 2: f(n) = Θ(n^log_b(a))        →  T(n) = Θ(n^log_b(a) × log n)
        (equal contribution)

Case 3: f(n) = Ω(n^(log_b(a) + ε))  →  T(n) = Θ(f(n))
        (combining work dominates)
```

**Common examples:**

| Recurrence | a | b | log_b(a) | Result |
|------------|---|---|----------|--------|
| Binary Search: T(n) = T(n/2) + O(1) | 1 | 2 | 0 | O(log n) |
| Merge Sort: T(n) = 2T(n/2) + O(n) | 2 | 2 | 1 | O(n log n) |
| Strassen: T(n) = 7T(n/2) + O(n²) | 7 | 2 | 2.81 | O(n^2.81) |
| Naive Matrix Mult: T(n) = 8T(n/2) + O(n²) | 8 | 2 | 3 | O(n³) |
| Karatsuba: T(n) = 3T(n/2) + O(n) | 3 | 2 | 1.58 | O(n^1.58) |

---

## Complexity Pitfalls at Google Interviews

### Pitfall 1: Hidden O(n) operations
```python
# This looks O(n) but is O(n²):
result = []
for i in range(n):
    result = result + [i]  # list concatenation is O(n)!
# Fix:
result.append(i)  # O(1) amortized
```

### Pitfall 2: Python dict/set operations
```python
# Average O(1) but worst case O(n) due to hash collisions
# In competitive programming, adversarial inputs can cause TLE
# For critical paths: use sorted containers or explicit hash functions
```

### Pitfall 3: Recursion space
```python
# DFS on a tree/graph: space = O(h) for call stack, not O(1)
# For balanced tree: O(log n); for skewed: O(n)
# Interviewer may ask: "can you do this iteratively to reduce stack space?"
```

### Pitfall 4: String concatenation
```python
# O(n²) — each += creates a new string
s = ""
for c in chars:
    s += c  # BAD

# O(n) — join at end
s = "".join(chars)  # GOOD
```

### Pitfall 5: Slice vs index
```python
arr[l:r]   # O(r-l) — creates a copy
arr[l]     # O(1) — index access
# Pass l, r as indices instead of slicing when calling recursively
```

---

## See Also

- [Google Interview Strategy](./google-interview-strategy.md)
- [Dynamic Programming](./algorithms/dynamic-programming.md)
- [Graph Algorithms](./algorithms/graph-algorithms.md)
