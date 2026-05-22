# First-Principles Map — Complexity Cheatsheet

```
WHY a Complexity Cheatsheet exists
├── Under pressure, complexity is derived incorrectly → wrong complexity claim → credibility hit
├── Memorizing the right Big-O for canonical structures eliminates a derivation step during interview
└── Space/time tradeoffs must be communicated instantly — lookup table beats re-derivation

WHAT it is
├── A reference map: data structure / algorithm → time complexity (avg/worst) → space complexity
├── Covers: all core DS, all sorting algorithms, graph algorithms, DP patterns, Master Theorem
└── Examples:
    ├── Hash map: O(1) avg lookup, O(n) worst (all collisions), O(n) space
    ├── Heap insert/delete: O(log n), heapify: O(n), peek: O(1)
    └── DFS/BFS: O(V+E) time, O(V) space (recursion stack / queue)

HOW it works
├── Data structure complexities:
│   ├── Array: access O(1), search O(n), insert/delete O(n)
│   ├── Linked list: access O(n), insert/delete O(1) at head
│   ├── BST (balanced): search/insert/delete O(log n); unbalanced: O(n)
│   ├── Hash map: O(1) avg all ops; O(n) worst
│   ├── Heap: insert O(log n), extract-min O(log n), build O(n)
│   └── Trie: insert/search O(L) where L = key length
├── Sorting complexities:
│   ├── Merge sort: O(n log n) time, O(n) space — stable
│   ├── Quick sort: O(n log n) avg, O(n²) worst, O(log n) space — in-place
│   ├── Heap sort: O(n log n) time, O(1) space — not stable
│   └── Counting/Radix: O(n+k) time — only for bounded integer keys
├── Graph algorithm complexities:
│   ├── BFS/DFS: O(V+E) time, O(V) space
│   ├── Dijkstra (binary heap): O((V+E) log V)
│   ├── Bellman-Ford: O(VE)
│   └── Floyd-Warshall: O(V³)
├── Master Theorem (T(n) = aT(n/b) + f(n)):
│   ├── f(n) = O(n^(log_b a - ε)) → T(n) = Θ(n^log_b a)
│   ├── f(n) = Θ(n^log_b a) → T(n) = Θ(n^log_b a · log n)
│   └── f(n) = Ω(n^(log_b a + ε)) → T(n) = Θ(f(n))
└── Space/time tradeoff landmarks:
    ├── Hash map: O(n) space → O(1) lookup (classic tradeoff)
    ├── Prefix sum: O(n) preprocess → O(1) range query
    └── Memoization: O(n) space → eliminates exponential recomputation

WHEN to use
├── Immediately after arriving at a solution: state complexity before interviewer asks
├── When choosing between two approaches: use complexity to justify selection
└── Decision:
    ├── Both O(n log n) → prefer lower constant (e.g., merge sort vs heap sort)
    ├── Space constrained → prefer in-place (quick sort, two-pointer)
    └── Need stable sort → merge sort (not heap sort, not quick sort)

WHAT can go wrong
├── Stating O(n log n) for a BST on unsorted input (insert n elements = O(n log n), not O(n))
├── Forgetting recursion stack space in DFS complexity (O(h) space, not O(1))
├── Claiming O(1) hash map without noting worst-case O(n) for hash collisions
└── Applying Master Theorem when subproblems are unequal size (not applicable)
```

## First-Principles Breakdown

- **Root problem:** Complexity analysis requires holding the algorithm structure in working memory while deriving — under pressure, this fails; a lookup table removes the derivation load.
- **Core insight:** Almost all interview complexity claims reduce to 5 families: O(1), O(log n), O(n), O(n log n), O(n²) — any other answer requires explicit justification.
- **Invariant:** Time complexity is dominated by the innermost loop or recursion depth × branching factor; space is dominated by the largest auxiliary structure allocated.
- **Why it works:** Memorizing the table once is O(1) amortized retrieval during any future interview — the investment cost is front-loaded.
- **Where it breaks:** Hash map worst-case and amortized costs are frequently confused; always clarify "average case" vs "worst case" when stating O(1) for hash operations.

---

# Revision Hub — Cheatsheets + Day-Before Checklist

## Key Resources

| Resource | What's in it |
|----------|-------------|
| [`interview-cheatsheet.md`](../03-patterns/interview-cheatsheet.md) | Full pattern cheatsheet — pattern triggers, templates |
| [`GOOGLE_QUICK_SHEET.md`](../03-patterns/GOOGLE_QUICK_SHEET.md) | Google-specific quick reference |
| [`GOOGLE_INTERVIEW_REVISION.md`](../03-patterns/GOOGLE_INTERVIEW_REVISION.md) | Deep revision guide |
| [`patterns-master.md`](../03-patterns/patterns-master.md) | Pattern recognition master guide |

---

## Day Before — Checklist

### DO
- [ ] Review complexity table below (5 minutes)
- [ ] Read Python gotchas section below (5 minutes)
- [ ] Re-read `03-patterns/patterns-master.md` — skim only, focus on trigger keywords
- [ ] Code LRU Cache from scratch (both `OrderedDict` and manual versions)
- [ ] Mentally walk through one DP problem you know cold
- [ ] Review your 3 behavioral STAR stories — just the outcomes
- [ ] Sleep 8 hours — non-negotiable

### DO NOT
- [ ] Don't start a new topic you haven't studied before
- [ ] Don't do timed contests under pressure — it spikes anxiety without benefit
- [ ] Don't re-read entire algorithm files end-to-end
- [ ] Don't skip meals or stay up late "cramming"

---

## 30-Minute Interview-Day Reading List (in order)

| Priority | What to read | Why |
|----------|-------------|-----|
| 1 | `03-patterns/interview-cheatsheet.md` — pattern triggers only | Primes pattern recognition |
| 2 | Complexity table below | Ensures complexity analysis is sharp |
| 3 | Python gotchas below | Prevents dumb syntax errors under stress |
| 4 | Your 3 STAR story titles + measurable outcomes | Behavioral round readiness |
| 5 | LRU/LFU interface signatures: `get(key)`, `put(key, val)` | LLD round readiness |

**Do not open:** DP recurrences, graph algorithm proofs, new files.

---

## Complexity Quick-Reference

### Sorting
| Algorithm | Best | Average | Worst | Space | Stable? |
|-----------|------|---------|-------|-------|---------|
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Tim Sort (Python) | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n+k) | Yes |

### Data Structures
| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
| Stack / Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Map | O(1) avg | O(1) avg | O(1) avg | O(1) avg | O(n) |
| Binary Search Tree | O(log n) avg | O(log n) avg | O(log n) avg | O(log n) avg | O(n) |
| AVL / Red-Black Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| Binary Heap | O(n) | O(n) | O(log n) | O(log n) | O(n) |
| Trie | — | O(m) | O(m) | O(m) | O(alphabet × n) |
| Segment Tree | — | O(log n) | O(log n) | O(log n) | O(n) |

### Graph Algorithms
| Algorithm | Time | Space | Use case |
|-----------|------|-------|---------|
| BFS | O(V+E) | O(V) | Shortest path (unweighted), level-order |
| DFS | O(V+E) | O(V) | Path existence, cycle detection, topological sort |
| Topological Sort (Kahn's) | O(V+E) | O(V) | Dependency ordering |
| Dijkstra (min-heap) | O((V+E) log V) | O(V) | Shortest path (non-negative weights) |
| Bellman-Ford | O(VE) | O(V) | Shortest path (negative weights, detect negative cycles) |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
| Prim's (MST) | O(E log V) | O(V) | Minimum spanning tree |
| Kruskal's (MST) | O(E log E) | O(V) | Minimum spanning tree |
| Union-Find (path compress + rank) | O(α(n)) ≈ O(1) | O(n) | Dynamic connectivity |

### Algorithm Techniques
| Technique | Time | Space |
|-----------|------|-------|
| Binary Search | O(log n) | O(1) |
| Two Pointers | O(n) | O(1) |
| Sliding Window | O(n) | O(window size) |
| Prefix Sum | O(n) build, O(1) query | O(n) |
| Merge Sort / Divide & Conquer | O(n log n) | O(n) |
| Backtracking (permutations) | O(n!) | O(n) |
| Backtracking (subsets) | O(2^n) | O(n) |
| DP (memoization) | O(states × transition) | O(states) |
| KMP string matching | O(n+m) | O(m) |

---

## Python Syntax Gotchas

### Integer Division
```python
7 // 2       # 3  (floor division)
7 / 2        # 3.5 (float division)
-7 // 2      # -4  (floors toward negative infinity — caution!)
-((-7) // 2) # 4   (ceiling division trick: -(-a//b))
import math
math.ceil(7/2)    # 4
```

### List Slicing
```python
arr = [1, 2, 3, 4, 5]
arr[1:3]    # [2, 3]       — indices 1, 2 (not 3)
arr[-1]     # 5            — last element
arr[::-1]   # [5,4,3,2,1] — reverse
arr[::2]    # [1, 3, 5]   — every other
arr[:]      # shallow copy
```

### dict.get() and defaultdict
```python
d = {}
d.get('key', 0)            # returns 0 if 'key' missing (no KeyError)
d['key'] = d.get('key', 0) + 1   # safe increment

from collections import defaultdict
dd = defaultdict(int)      # missing key → 0
dd = defaultdict(list)     # missing key → []
dd = defaultdict(set)      # missing key → set()
```

### heapq — Min-Heap (Python default)
```python
import heapq
h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappop(h)           # 1 (minimum)

# Max-heap: negate values
heapq.heappush(h, -val)
-heapq.heappop(h)          # gives max

# Heapify in-place
arr = [3, 1, 2]
heapq.heapify(arr)         # O(n)

# Push then pop (more efficient than two ops)
heapq.heappushpop(h, val)

# Top K largest
heapq.nlargest(k, arr)     # O(n log k)
heapq.nsmallest(k, arr)    # O(n log k)
```

### collections.deque
```python
from collections import deque
dq = deque()
dq.append(1)               # add to right
dq.appendleft(0)           # add to left
dq.pop()                   # remove from right — O(1)
dq.popleft()               # remove from left — O(1)
# list.pop(0) is O(n) — always use deque for queue/BFS
```

### Counter
```python
from collections import Counter
c = Counter("abracadabra")
c.most_common(2)           # [('a', 5), ('r', 2)]
c['z']                     # 0 (no KeyError)
c.update("aaa")            # add counts
c.subtract("aa")           # subtract counts (can go negative)
```

### Sorting Key Tricks
```python
arr.sort()                          # in-place, returns None
sorted(arr)                         # returns new list
arr.sort(key=lambda x: -x)          # descending
arr.sort(key=lambda x: (x[1], x[0])) # sort by second element, then first
arr.sort(key=lambda x: x.lower())   # case-insensitive string sort
```

### Common Traps
```python
# Mutable default argument — DON'T
def foo(arr=[]):  # arr is shared across all calls!
    arr.append(1)

# Correct
def foo(arr=None):
    if arr is None: arr = []

# String concatenation in loop — O(n²)
s = ""
for c in chars:
    s += c    # DON'T — creates new string each time

# Correct — O(n)
s = "".join(chars)

# Integer identity vs equality
a = 300
b = 300
a is b    # False — use == for value comparison, is only for None/True/False

# Unpacking with *
first, *rest = [1, 2, 3, 4]   # first=1, rest=[2,3,4]
*init, last = [1, 2, 3, 4]    # init=[1,2,3], last=4
```
