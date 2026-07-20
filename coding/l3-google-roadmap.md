---
tags: [coding, google-l3, roadmap, ai-ml-loop]
topic: L3 Google Interview Roadmap
difficulty: meta
---

# Google L3 (SWE) AI/ML Loop — Hyper-Focused DSA Roadmap

> [!important] Read This First — What L3 AI/ML Actually Tests
> Google L3 AI/ML loops are **DSA-heavy**, not ML-theory-heavy.
> You will get 4–5 coding rounds. Each round is one LeetCode-style problem in 35–45 min.
> The bias is strongly toward **graphs, BFS/DFS, binary search on answer space, heaps, sliding window, tries, and DP**.
> System Design and Low-Level Design are **not tested at L3**.

---

## Tier Legend

| Badge | Meaning | Action |
|-------|---------|--------|
| `⚡ T1` | **TIER 1 — Must Master** | High-yield Google favorites. Every L3 loop has ≥2 of these. Build reflexes. |
| `🎯 T2` | **TIER 2 — Build Fluidity** | Highly probable. Know the core pattern. Don't over-index on edge cases. |
| `💤 T3` | **TIER 3 — Skim or Skip** | Overkill for L3. Read a 3-sentence summary; do NOT code these. |

---

## TIER 1: High-Yield Google Favorites — Must Master `⚡ T1`

> [!caution] These Are Non-Negotiable
> If you walk into a Google L3 loop without these being reflexive, you are not ready. Each topic below has appeared in >60% of documented Google L3 interviews.

### 1.1 Graph Traversals: BFS & DFS `⚡ T1`

**Why Google loves this**: Appears in nearly every loop disguised as grid problems, matrix problems, or connection problems.

**The 5 must-solve LeetCode problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **Number of Islands** `⚡ T1` | DFS/BFS on grid | Mark visited in-place; 4-directional flood fill |
| **Rotting Oranges** `⚡ T1` | Multi-source BFS | Add ALL sources to queue before starting BFS |
| **Pacific Atlantic Water Flow** `⚡ T1` | Reverse DFS from both coasts | Start from borders, not from cells |
| **Word Ladder** `⚡ T1` | BFS on implicit graph | Build adjacency by swapping each character |
| **Shortest Path in Binary Matrix** `⚡ T1` | BFS (8-directional) | BFS always gives shortest unweighted path |

**Key insight to internalize:**
```
BFS  → shortest path on UNWEIGHTED graphs; level-by-level processing
DFS  → connected components; cycle detection; path existence; flood fill
Both → O(V + E) time, O(V) space
```

**Files:** [graph.md](./data-structures/13-graph.md) · [graphs.md](../01-data-structures/13-graphs.md) · [graph-algorithms.md](./algorithms/13-graph-algorithms.md)

---

### 1.2 Topological Sort `⚡ T1`

**Why Google loves this**: Every "prerequisites" or "ordering with dependencies" problem uses this.

**The 3 must-solve problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **Course Schedule** `⚡ T1` | Kahn's BFS / cycle detection | If topological order length < n → cycle exists |
| **Course Schedule II** `⚡ T1` | Kahn's BFS with order | Return order array; empty = cycle |
| **Alien Dictionary** `⚡ T1` | Build graph from adjacent words | Compare adjacent words char-by-char to get edges |

**Template (Kahn's — memorize this):**
```python
from collections import defaultdict, deque

def topo_sort(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    q = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)
    
    return order if len(order) == n else []  # [] = cycle
```

**Files:** [graph-algorithms.md](./algorithms/13-graph-algorithms.md) · [graphs.md](../01-data-structures/13-graphs.md) · [13-graph.md](../01-data-structures/13-graphs.md)

---

### 1.3 Union-Find (DSU) `⚡ T1`

**Why Google loves this**: Connectivity questions, grouping, MST — fast and clean solution.

**The 3 must-solve problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **Redundant Connection** `⚡ T1` | DSU cycle detection | union() returns False → that edge is redundant |
| **Accounts Merge** `⚡ T1` | DSU grouping by key | Union emails under same account |
| **Number of Provinces** `⚡ T1` | DSU or DFS components | Count distinct `find()` roots |

**Template (memorize this — path compression + union by rank):**
```python
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])  # path compression
        return self.p[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False  # already connected
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.p[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
```

**Files:** [union-find.md](./algorithms/14-union-find.md)

---

### 1.4 Binary Search on Solution Space `⚡ T1`

**Why Google loves this**: Disguised as "find minimum X such that Y is possible" — most candidates miss it.

**The 4 must-solve problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **Koko Eating Bananas** `⚡ T1` | BS on speed (1..max) | `can_finish(speed)` is monotonic → binary search |
| **Capacity To Ship Packages** `⚡ T1` | BS on capacity | Check if capacity can ship all within D days |
| **Split Array Largest Sum** `⚡ T1` | BS on answer | Minimize the maximum → binary search |
| **Search in Rotated Sorted Array** `⚡ T1` | BS with pivot logic | Identify which half is sorted; recurse on valid half |

**The universal "search on answer" template:**
```python
def solve(arr, limit):
    def feasible(mid):
        # Check if 'mid' satisfies the condition
        ...
    
    lo, hi = MIN_ANSWER, MAX_ANSWER
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid      # valid → try smaller
        else:
            lo = mid + 1  # invalid → need bigger
    return lo
```

**The recognition signal:** "minimum/maximum X such that [condition]" → binary search on X.

**Files:** [binary-search.md](./algorithms/11-binary-search.md) · [11-binary-search.md](../02-algorithms/11-binary-search.md)

---

### 1.5 Heaps / Priority Queues `⚡ T1`

**Why Google loves this**: K-th element problems, streaming data, scheduling — all heaps.

**The 5 must-solve problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **Kth Largest Element** `⚡ T1` | Min-heap of size K | Pop when size > K; top = Kth largest |
| **K Closest Points to Origin** `⚡ T1` | Max-heap of size K | Use negative distance; smallest K remain |
| **Merge K Sorted Lists** `⚡ T1` | K-way merge with heap | Push (val, list_idx, elem_idx) |
| **Find Median from Data Stream** `⚡ T1` | Two heaps (max + min) | Max-heap for lower half, min-heap for upper half |
| **Task Scheduler** `⚡ T1` | Greedy + max-heap | Always schedule most frequent task next |

**Key Python heap operations:**
```python
import heapq
heapq.heapify(arr)          # O(n) — convert list to min-heap in-place
heapq.heappush(h, val)      # O(log n)
heapq.heappop(h)            # O(log n) — removes and returns smallest
# Max-heap: push -val, negate on pop
heapq.nlargest(k, arr)      # O(n log k) — top K largest
```

**Files:** [heap.md](./data-structures/10-heap.md)

---

### 1.6 Sliding Window `⚡ T1`

**Why Google loves this**: String and subarray optimization — near-universal at Google L3.

**The 4 must-solve problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **Minimum Window Substring** `⚡ T1` | Variable window, shrink when valid | Two pointers + frequency map |
| **Longest Substring Without Repeating** `⚡ T1` | Expand right, shrink when duplicate | `last_seen` dict eliminates set |
| **Sliding Window Maximum** `⚡ T1` | Monotonic deque | Deque front = max; pop smaller from back |
| **Permutation in String** `⚡ T1` | Fixed window = len(p) | Compare frequency maps of window and target |

**Key pattern — "shrink when invalid":**
```python
left = 0
for right in range(len(s)):
    # Expand: add s[right] to window state
    while WINDOW_IS_INVALID:
        # Shrink: remove s[left] from window state
        left += 1
    # Window is valid here — update answer
```

**Files:** [sliding-window.md](./algorithms/04-sliding-window.md)

---

### 1.7 Two Pointers `⚡ T1`

**Why Google loves this**: Foundational — appears standalone and inside harder problems.

**The 4 must-solve problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **3Sum** `⚡ T1` | Sort + two pointers | Fix one, binary search the pair; skip duplicates |
| **Trapping Rain Water** `⚡ T1` | Two pointers from ends | `min(left_max, right_max) - height[i]` |
| **Container With Most Water** `⚡ T1` | Greedy two-pointer | Move the shorter wall inward |
| **Linked List Cycle** `⚡ T1` | Fast/slow (Floyd's) | If they meet → cycle; else fast hits null |

**Files:** [two-pointers.md](./algorithms/03-two-pointers.md)

---

### 1.8 Tries `⚡ T1`

**Why Google loves this**: Prefix problems and autocomplete — Google literally builds these for a living.

**The 3 must-solve problems:**
| Problem | Pattern | Insight |
|---------|---------|---------|
| **Implement Trie** `⚡ T1` | Build trie from scratch | children dict + is_end flag |
| **Word Search II** `⚡ T1` | Trie + DFS on grid | Insert all words in trie; DFS prunes when prefix not in trie |
| **Add and Search Word** `⚡ T1` | Trie + wildcard DFS | `.` means try all children recursively |

**Template:**
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
```

**Files:** [trie.md](./data-structures/09-trie.md)

---

## TIER 2: Highly Probable — Build Fluidity `🎯 T2`

> [!note] Pattern Over Perfection
> For Tier 2, know the core pattern cold. You do NOT need to handle every edge case from memory — you will be able to derive edge cases if you know the pattern.

### 2.1 Dynamic Programming `🎯 T2`

**Focus only on these DP patterns for L3:**

| Pattern | Representative problems | Key insight |
|---------|------------------------|-------------|
| **1D linear DP** | Climbing Stairs, House Robber, Coin Change, Word Break | `dp[i]` depends on small window of previous |
| **0/1 Knapsack** | Partition Equal Subset Sum, Target Sum | Backward inner loop to prevent reuse |
| **Grid DP** | Unique Paths, Minimum Path Sum, Maximal Square | `dp[i][j] = f(dp[i-1][j], dp[i][j-1])` |
| **LCS/Edit family** | LCS, Edit Distance | 2D table; match = diagonal; else max(sides) |
| **LIS** | Longest Increasing Subsequence | O(n²) DP or O(n log n) with patience sort |
| **Stock problems** | Best Time to Buy/Sell (all variants) | State machine: hold / not-hold |

**Skip for L3:** Bitmask DP, Digit DP, Interval DP (Burst Balloons), Tree DP (complex variants)

**Files:** [dynamic-programming.md](./algorithms/15-dynamic-programming.md) · [recursion-to-dp.md](../02-algorithms/10-recursion-to-dp.md)

---

### 2.2 Backtracking `🎯 T2`

**Focus on these patterns:**

| Pattern | Problems | Key pruning |
|---------|----------|-------------|
| **Subsets** | Subsets, Subsets II | `start` index prevents backward picks |
| **Permutations** | Permutations, Permutations II | `used[]` array; sort for duplicate skipping |
| **Combination Sum** | Combination Sum I/II | Reuse (same `i`) vs no-reuse (advance `i+1`) |
| **Grid backtracking** | Word Search, N-Queens | Mark cell visited; restore on backtrack |

**The universal template:**
```python
def backtrack(path, start, choices):
    if is_complete(path):
        result.append(path[:])
        return
    for i in range(start, len(choices)):
        if should_prune(i, path, choices): continue
        path.append(choices[i])
        backtrack(path, next_start(i), choices)
        path.pop()
```

**Files:** [backtracking.md](./algorithms/12-backtracking.md)

---

### 2.3 Binary Trees & BST `🎯 T2`

**Focus on these problems:**

| Problem | Pattern | Key insight |
|---------|---------|-------------|
| **LCA of Binary Tree** `🎯 T2` | Post-order DFS | Both children return non-null → current node is LCA |
| **Serialize/Deserialize** `🎯 T2` | Pre-order DFS | Root first; null markers; use deque iterator for deserialization |
| **Binary Tree Max Path Sum** `🎯 T2` | Post-order + global max | `max(0, child)` to drop negative arms |
| **Level Order Traversal** `🎯 T2` | BFS with snapshot | `q_size = len(queue)` before inner loop |
| **Validate BST** `🎯 T2` | DFS with bounds | Pass `(lo, hi)` bounds — NOT just check immediate children |
| **Diameter of Binary Tree** `🎯 T2` | Post-order heights | `left_h + right_h` at each node; track global max |

**Files:** [tree.md](./data-structures/08-tree.md)

---

### 2.4 Greedy `🎯 T2`

**Must-know greedy problems for L3:**

| Problem | Insight |
|---------|---------|
| **Merge Intervals** `🎯 T2` | Sort by start; extend end if overlap |
| **Jump Game** `🎯 T2` | Track max reachable index; if ever `i > max_reach` → false |
| **Gas Station** `🎯 T2` | Total gas ≥ total cost is necessary; find start where running sum never goes negative |

---

### 2.5 Stack Patterns `🎯 T2`

| Problem | Pattern |
|---------|---------|
| **Largest Rectangle in Histogram** `🎯 T2` | Monotonic increasing stack; pop when shorter bar found |
| **Daily Temperatures** `🎯 T2` | Monotonic decreasing stack of indices |
| **Valid Parentheses** `🎯 T2` | Push opens; match and pop on closes |

---

### 2.6 Linked Lists `🎯 T2`

Know these cold:

| Problem | Pattern |
|---------|---------|
| **Reverse Linked List** `🎯 T2` | Three pointers: prev, curr, next |
| **Merge Two Sorted Lists** `🎯 T2` | Dummy head; compare and advance |
| **LRU Cache** `🎯 T2` | Doubly linked list + hash map; O(1) get and put |
| **Linked List Cycle** `🎯 T2` | Fast/slow pointers |

---

## TIER 3: Overkill / Lower Priority for L3 `💤 T3` {#tier-3-skip}

> [!warning] Do NOT Code These
> These topics almost never appear in Google L3 interviews. Skimming a conceptual summary is enough. Redirect time to Tier 1.

| Topic | What it is (3-sentence summary) | Skip? |
|-------|--------------------------------|-------|
| **Segment Tree** | A tree structure for range queries (sum/min/max) with O(log n) update and query. Built bottom-up from an array; each node stores aggregate of its range. For L3, prefix sums or BIT handle most interview use cases. | ✅ Skip coding |
| **Fenwick Tree (BIT)** | Compact array structure for prefix sum with point updates in O(log n). Uses bit tricks to find parent/child nodes. Replaceable by simpler prefix sum for most L3 problems. | ✅ Skip coding |
| **Tarjan's SCC** | Single-pass DFS algorithm finding strongly connected components using discovery time and low-link values. Uses an explicit stack to identify SCC boundaries. Never appears in documented L3 loops. | ✅ Skip entirely |
| **Kosaraju's SCC** | Two-pass DFS: first pass on original graph gets finish order; second pass on reversed graph reveals SCCs. Conceptually cleaner than Tarjan's but same complexity. | ✅ Skip entirely |
| **Bellman-Ford** | Shortest path with negative weights; O(VE). Relax all edges V-1 times. Dijkstra is preferred when weights are non-negative (≈ always in L3). | 💤 Know concept |
| **Floyd-Warshall** | All-pairs shortest path in O(V³). Simple triple-nested loop. Not tested at L3 — brute force is too slow for any realistic constraint. | ✅ Skip entirely |
| **Bitmask DP / TSP** | DP where state includes a bitmask of visited nodes. Used for NP-hard problems on small N (≤20). Burst Balloons, TSP. Overkill for L3. | ✅ Skip coding |
| **Digit DP** | DP over digits of a number while respecting an upper bound constraint using a `tight` flag. Very niche. Not L3 material. | ✅ Skip entirely |
| **Suffix Array** | Sorted array of all suffixes of a string for O(log n) substring queries. Used in text search systems. Never in L3 coding rounds. | ✅ Skip entirely |
| **Concurrency / Threading** | Mutex, semaphore, producer-consumer patterns. L3 AI/ML loops are pure DSA — concurrency appears only at SDE3+ system design. | ✅ Skip entirely |
| **SQL** | Joins, window functions, CTEs. Not tested in L3 coding rounds. | ✅ Skip entirely |
| **System Design** | High-level architecture: databases, caching, sharding. Not required at L3. | ✅ Skip entirely |
| **OOP / Design Patterns** | SOLID, Factory, Observer, etc. Not tested in L3 coding rounds. | ✅ Skip entirely |

---

## L3 Study Schedule (4-Week Sprint) `⚡ T1`

> [!tip] The Only Schedule That Works
> Each day: **1 topic study (30 min) + 2 LeetCode problems (60 min) + 1 review (15 min)**
> Total: ~105 min/day. Non-negotiable.

### Week 1 — Tier 1 Core (Graphs + Binary Search + Heaps)
| Day | Topic | LeetCode problems |
|-----|-------|------------------|
| Day 1 | BFS on graphs/grids | Number of Islands, Rotting Oranges |
| Day 2 | DFS on graphs/grids | Pacific Atlantic, Flood Fill |
| Day 3 | Topological Sort | Course Schedule, Course Schedule II |
| Day 4 | Union-Find | Redundant Connection, Accounts Merge |
| Day 5 | Binary Search on Answer | Koko Eating Bananas, Capacity to Ship |
| Day 6 | Binary Search variants | Search Rotated Array, Find Minimum Rotated |
| Day 7 | Review + 3 problems from weak spots | — |

### Week 2 — Tier 1 Core (Heaps + Sliding Window + Two Pointers + Tries)
| Day | Topic | LeetCode problems |
|-----|-------|------------------|
| Day 8 | Heap top-K pattern | K Closest Points, Kth Largest Element |
| Day 9 | Heap K-way merge + two heaps | Merge K Lists, Find Median from Data Stream |
| Day 10 | Sliding Window fixed+variable | Minimum Window Substring, Longest No Repeat |
| Day 11 | Sliding Window + Monotonic Deque | Sliding Window Maximum, Permutation in String |
| Day 12 | Two Pointers | 3Sum, Trapping Rain Water |
| Day 13 | Tries | Implement Trie, Word Search II |
| Day 14 | Full mock round (35 min, 1 problem, Tier 1) | — |

### Week 3 — Tier 2 (DP + Backtracking + Trees)
| Day | Topic | LeetCode problems |
|-----|-------|------------------|
| Day 15 | 1D DP | House Robber, Coin Change |
| Day 16 | Knapsack DP | Partition Equal Subset Sum |
| Day 17 | Grid DP | Unique Paths, Minimum Path Sum |
| Day 18 | LCS / Edit Distance | Longest Common Subsequence, Edit Distance |
| Day 19 | Backtracking: subsets + permutations | Subsets, Permutations, Combination Sum |
| Day 20 | Tree traversals + LCA | LCA Binary Tree, Level Order |
| Day 21 | Tree DP + BST | Max Path Sum, Validate BST, Serialize/Deserialize |

### Week 4 — Integration + Mocks
| Day | Topic | Action |
|-----|-------|--------|
| Day 22 | Greedy + Stack | Merge Intervals, Largest Rectangle |
| Day 23 | Linked Lists | Reverse Linked List, LRU Cache |
| Day 24 | Mixed T1 + T2 | 3 problems, random pick |
| Day 25 | Full mock (2 problems, 70 min) | Record yourself explaining out loud |
| Day 26 | Review all wrong answers | Fix gaps |
| Day 27 | 2 more full mocks | Interviewing.io or Pramp |
| Day 28 | Light review only — rest | — |

---

## Quick-Reference: "What Pattern Is This?" `⚡ T1`

| Problem description contains… | Use this |
|-------------------------------|----------|
| "shortest path", "minimum steps", unweighted graph | **BFS** |
| "all paths", "connected components", "flood fill" | **DFS** |
| "prerequisites", "dependencies", "ordering" | **Topological Sort** |
| "connected groups", "merge groups" | **Union-Find** |
| "minimum X that satisfies Y", "find boundary in range" | **Binary Search on Answer** |
| "kth largest/smallest", "top K", "median of stream" | **Heap** |
| "longest/shortest subarray/substring with condition" | **Sliding Window** |
| "two numbers sum to target", sorted array, palindrome | **Two Pointers** |
| "all subsets/permutations/combinations" | **Backtracking** |
| "prefix matching", "autocomplete", "word dictionary" | **Trie** |
| "maximum/minimum over subrange", overlapping subproblems | **DP** |
| "next greater", "largest rectangle", "bracket matching" | **Monotonic Stack** |

---

## Files in This Repository — By Tier

### ⚡ TIER 1 — Study These First
- [graph-algorithms.md](./algorithms/13-graph-algorithms.md) — BFS, DFS, Topological Sort
- [union-find.md](./algorithms/14-union-find.md) — DSU with path compression
- [binary-search.md](./algorithms/11-binary-search.md) — All BS variants
- [heap.md](./data-structures/10-heap.md) — All heap patterns
- [sliding-window.md](./algorithms/04-sliding-window.md) — Fixed + variable window
- [two-pointers.md](./algorithms/03-two-pointers.md) — Converging + fast/slow
- [trie.md](./data-structures/09-trie.md) — Trie + Trie+DFS
- [array.md](./data-structures/01-array.md) — Two-pointer/window/prefix patterns
- [hashing.md](./data-structures/02-hashing.md) — Hash map patterns
- [graphs.md](../01-data-structures/13-graphs.md) — Graph deep dive: Dijkstra, topo, BFS variants
- [matrix.md](../01-data-structures/04-matrix.md) — Grid as implicit graph; multi-source BFS, grid DP

### 🎯 TIER 2 — Study After Tier 1
- [dynamic-programming.md](./algorithms/15-dynamic-programming.md)
- [backtracking.md](./algorithms/12-backtracking.md)
- [tree.md](./data-structures/08-tree.md)
- [recursion-to-dp.md](../02-algorithms/10-recursion-to-dp.md)
- [linked-list.md](./data-structures/07-linked-list.md)
- [stack.md](./data-structures/05-stack.md)
- [greedy.md](./algorithms/16-greedy.md)
- [sorting.md](./algorithms/00-sorting.md)
- [string.md](./data-structures/03-string.md)
- [string-algorithms.md](../02-algorithms/02-string-algorithms.md) — KMP, Z, rolling hash; expand-around-center first

### 💤 TIER 3 — Not in L3 navigation (skip)

- MINDMAP.md — skim once for the big picture; not a study file

**Behavioral (required):** [`04-behavioral/BEHAVIORAL_GOOGLINESS.md`](../04-behavioral/BEHAVIORAL_GOOGLINESS.md)
