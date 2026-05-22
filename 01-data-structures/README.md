## First-Principles Map

```text
WHY data structures exist
├── Different problems demand different access patterns
│   ├── Lookup by key           → need O(1) average access           → HashMap / HashSet
│   ├── Ordered traversal       → need sorted, dynamic insert        → BST / TreeMap
│   ├── Priority access         → need min/max always available      → Heap (PriorityQueue)
│   ├── Hierarchical data       → parent-child relationships         → Tree / Trie
│   ├── Pairwise connections    → arbitrary edges, cycles            → Graph (adj list/matrix)
│   ├── Range queries           → aggregate over sub-arrays          → Segment Tree / BIT
│   └── Sequential access       → LIFO / FIFO discipline             → Stack / Queue / Deque
│
WHAT the core structures are
├── Array         — contiguous memory, O(1) index, O(n) insert/delete
├── Linked List   — O(1) insert at known node, O(n) search, no random access
├── Stack         — LIFO; DFS, undo, monotonic problems
├── Queue/Deque   — FIFO / both-ends; BFS, sliding window max
├── Hash Map/Set  — O(1) amortized lookup, insert, delete; unordered
├── BST/TreeMap   — O(log n) ordered ops; floor/ceil/rank
├── Heap          — O(log n) push/pop, O(1) peek; top-k, median
├── Trie          — O(L) prefix ops; autocomplete, word search
├── Graph         — adjacency list O(V+E); matrix O(V²); traversal, shortest path
└── Segment Tree  — O(log n) range query + point update; sum, min, max, GCD
│
HOW to pick the right one (access pattern → DS)
├── "Find in O(1)"                    → HashMap
├── "Maintain sorted + dynamic"       → TreeMap / SortedList
├── "Always need min or max"          → Min-Heap / Max-Heap
├── "Two extremes of a sequence"      → Deque
├── "Prefix match / word existence"   → Trie
├── "Range sum / range min"           → Segment Tree / BIT
├── "Shortest path / connectivity"    → Graph + BFS/Dijkstra/Union-Find
└── "Undo / balanced parens / NGE"    → Stack
│
WHEN each structure excels
├── HashMap      — frequency counts, anagrams, two-sum, memoization
├── Heap         — k-th largest, merge k sorted, median of stream
├── Trie         — longest common prefix, word break, autocomplete
├── Segment Tree — range min/max/sum with updates, sliding queries
├── Graph        — network flow, island count, topological sort, cycle detection
├── Deque        — sliding window maximum, monotonic deque, BFS level order
└── Stack        — next greater element, valid parentheses, inorder iterative
│
WHAT CAN GO WRONG
├── Using array where hash needed      → O(n) lookup bottleneck
├── Using BST where heap needed        → can't peek min/max in O(1)
├── Using adjacency matrix on V=10^5   → O(V²) space blowup
├── Missing Trie, using set of strings → O(L·N) vs O(L) per query
├── Segment Tree when prefix sum works → over-engineering, wasted time
└── Wrong DS choice locks wrong complexity → no amount of algo cleverness fixes it
│
DECISION — access pattern → DS
├── O(1) lookup by key          → HashMap / HashSet
├── O(1) both ends              → Deque
├── O(log n) min/max            → Heap
├── O(log n) ordered ops        → BST / TreeMap
├── O(L) prefix ops             → Trie
├── O(log n) range query+update → Segment Tree / BIT
├── Hierarchy / parent-child    → Tree
└── Arbitrary connectivity      → Graph (adj list)
```

## First-Principles Breakdown

- **Root problem:** Different problems expose different bottlenecks — lookup, ordering, range, hierarchy, connectivity — and no single structure solves all efficiently.
- **Core insight:** Every DS is a trade-off: hash maps sacrifice order for O(1) lookup; heaps sacrifice arbitrary access for O(1) extremum; tries sacrifice space for O(L) prefix ops.
- **Invariant:** The access pattern of the dominant operation determines the optimal DS; everything else is secondary.
- **Why it works:** Each DS encodes a structural guarantee (heap property, BST ordering, trie prefix path) that makes its target operation cheap by construction.
- **Where it breaks:** When the wrong DS is chosen upfront, no algorithmic optimization on top can recover the lost complexity — you must change the structure, not the algorithm.

# Data Structures — Index

Deep-dive files live in `01-data-structures/`. This file is the navigation index.

---

## Topic Table

| Topic | Difficulty | Key Patterns | File |
|-------|-----------|--------------|------|
| **Arrays** | Easy–Hard | Two Pointers, Sliding Window, Prefix Sum, Kadane's | [`array.md`](./array.md) |
| **Strings** | Easy–Hard | Sliding Window, KMP, Rabin-Karp, Anagram/Frequency Map | [`string.md`](../02-algorithms/string.md) |
| **Linked Lists** | Easy–Med | Fast/Slow Pointers, Dummy Node, Reverse In-Place | [`linked-list.md`](./linked-list.md) |
| **Stacks** | Easy–Med | Monotonic Stack, Bracket Matching, Next Greater Element | [`stack.md`](./stack.md) |
| **Queues** | Easy–Med | BFS, Sliding Window Max (Monotonic Deque) | [`queue.md`](./queue.md) |
| **Trees / BST** | Med–Hard | DFS (pre/in/post), BFS, LCA, Path Sum, Morris Traversal | [`tree.md`](./tree.md) |
| **Heaps** | Med–Hard | Top-K, Merge K Sorted, Two-Heap (Median), Dijkstra | [`heap.md`](./heap.md) |
| **Hash Maps** | Easy–Med | Frequency Count, Two Sum, Grouping, Rolling Hash | [`hashing.md`](./hashing.md) |
| **Tries** | Med | Prefix Search, Word Break, Autocomplete, XOR Max | [`trie.md`](./trie.md) |
| **Graphs** | Med–Hard | BFS, DFS, Topological Sort, Union-Find, Dijkstra, Bellman-Ford | [`graphs.md`](./graphs.md) |
| **Segment Trees** | Hard | Range Query, Range Update, Lazy Propagation | [`segment-tree.md`](./segment-tree.md) |
| **Advanced** | Hard | Bloom Filter, Skip List, Fenwick Tree, Disjoint Set | [`advanced-structures.md`](./advanced-structures.md) |

Also see: [`ds_tree.md`](./ds_tree.md) — DS taxonomy / decision tree.

---

## Study Progression (Beginner → Advanced)

**Foundation (start here, ~Week 1)**
1. Arrays — know prefix sum, two-pointer, sliding window cold
2. Hash Maps — frequency maps, two-sum pattern, O(1) lookup
3. Strings — treat as array of chars; sliding window + frequency map
4. Linked Lists — master pointer manipulation; dummy node pattern

**Core (must-nail for L4, ~Week 1–2)**
5. Stacks — monotonic stack is an L4 staple
6. Queues + Deque — BFS backbone; monotonic deque for window max/min
7. Trees + BST — every L4 loop gets at least one tree problem
8. Graphs — BFS/DFS, topological sort, connected components

**Advanced (differentiators, ~Week 3–4)**
9. Heaps — median maintenance, top-K; know heapq API cold
10. Tries — prefix problems, word dictionary, XOR tricks
11. Union-Find — Kruskal's, dynamic connectivity
12. Segment Trees — range queries; understand concept even if you don't code from scratch

**"Good to know" (only if time permits)**
- Advanced structures (Bloom filter, Skip list) — unlikely to be asked to implement, but know the use case

---

## Must-Nail for L4 (Frequency at Google)

**Very High:** Arrays, Hash Maps, Trees, Graphs, Strings  
**High:** Stacks, Heaps, Linked Lists  
**Medium:** Tries, Union-Find, Queues  
**Lower:** Segment Trees, Advanced Structures (but know *what* they solve)
