# Data Structures

Core data structures for coding interviews. These notes are written to be sufficient for **Google SDE-2 (L4)**, with optional deeper sections that also help for SDE-3: concept overview, algorithms, patterns, code, interview strategy, and quick revision.

**Google interview:** Use [../GOOGLE_INTERVIEW_REVISION.md](../GOOGLE_INTERVIEW_REVISION.md) (topic priority + practice lists) and [../GOOGLE_QUICK_SHEET.md](../GOOGLE_QUICK_SHEET.md) (one-page patterns) alongside the files below.
For an end-to-end SDE-2 plan (coding + system design + behavioral), start with: [../../google-sde2/README.md](../../google-sde2/README.md).

Each topic file below includes **Interview Questions — Logic & Trickiness** (canonical problems, solution logic, and trickiness for that structure).

## Topic files

| Topic | File | Highlights |
|-------|------|------------|
| **Array** | [array.md](array.md) | Two pointers, sliding window, prefix sum, Kadane; edge cases, SDE-3 trade-offs. |
| **Linked List** | [linked-list.md](linked-list.md) | Dummy node, fast/slow, in-place reversal, cycle detection; LRU (design). |
| **Stack** | [stack.md](stack.md) | Monotonic stack, next greater element, largest rectangle in histogram. |
| **Queue** | [queue.md](queue.md) | BFS, monotonic deque, sliding window maximum, circular queue. |
| **Tree** | [tree.md](tree.md) | Traversals, LCA, tree DP, BST, max path sum, serialize/deserialize. |
| **Heap** | [heap.md](heap.md) | Top-K, K-way merge, two heaps (median), implementations. |
| **Hashing** | [hashing.md](hashing.md) | Collision handling, subarray sum = K, consistent hashing, bloom filter. |
| **Graphs** | [graphs.md](graphs.md) | BFS/DFS, islands, flood fill, rotten oranges, course schedule, alien dictionary; terminology, algorithms, question lists. |

## How to use

- **Learn a topic:** Open the topic file; read Concept Overview → Core Algorithms → Pattern Recognition → Interview Strategy → Quick Revision.
- **Before interviews:** Use each file’s **Quick Revision** and **Interview Strategy** sections.
- **Patterns:** See also [patterns/two-pointers-sliding-window.md](../../patterns/two-pointers-sliding-window.md) and [patterns/leetcode-patterns.md](../../patterns/leetcode-patterns.md).

## Cross-links

- **Graph algorithms** (Dijkstra, topo, MST): [../algorithms/graph.md](../algorithms/graph.md)  
- **Union Find** (connectivity, Kruskal): [../algorithms/union-find.md](../algorithms/union-find.md)
