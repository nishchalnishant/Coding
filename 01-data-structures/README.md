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
