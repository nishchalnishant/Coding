# Data Structures — SDE-3 Gold Standard

Core data structures for senior-level engineering interviews. This repository has been rigorously audited and structured as a **"Truth Source" for SDE-3 / Staff** candidates. It goes beyond SDE-2 problem-solving by injecting canonical implementations, concurrency considerations, memory layout implications, and system design scalability metrics.

**Twin-Track Architecture:**
Use [../../../reference/quick-sheets/revision-guide.md](../../../reference/quick-sheets/revision-guide.md) (topic priority) and [../../../reference/quick-sheets/quick-recall.md](../../../reference/quick-sheets/quick-recall.md) (one-page patterns) alongside the files below.

Each topic module contains:
1. **Theory & Mental Models**: Memory layout, caching implications, and invariants.
2. **Core Algorithms & Click Moments**: SDE-3 canonical code templates.
3. **SDE-3 Deep Dives**: Thread-safety, lock-free structures, and distributed scalability.
4. **Interview Questions — Logic & Trickiness**: Distilled wisdom on boundaries and traps.

## Topic files

| Topic | File | Highlights |
|-------|------|------------|
| **Array** | [array.md](array.md) | Boyer-Moore, Floyd's cycle, prefix sum, Kadane, stream scaling. |
| **Linked List** | [linked-list.md](linked-list.md) | In-place reversal, cycle detection, LRU Cache DLL, Lock-free design. |
| **Stack** | [stack.md](stack.md) | Monotonic stack, Asteroid collision, expression evaluation. |
| **Queue** | [queue.md](queue.md) | BFS, monotonic deque, ring buffer bit-masking, LMAX disruptor. |
| **Tree** | [tree.md](tree.md) | 1-Stack Postorder, LCA, tree DP, max path sum, serialization. |
| **Heap** | [heap.md](heap.md) | Custom `__lt__` objects, top-K, K-way merge, Two Heaps (median). |
| **Hashing** | [hashing.md](hashing.md) | Rabin-Karp, subarray sums, consistent hashing, bloom filters. |
| **Graphs** | [graphs.md](graphs.md) | Bidirectional BFS, multi-source BFS, topological sort, flood fill. |
| **Trie** | [trie.md](trie.md) | Prefix tree, autocomplete, Word Search II pruning, XOR Trie. |

## How to use

- **Learn a topic:** Open the topic file; read Concept Overview → Core Algorithms → Pattern Recognition → Interview Strategy → Quick Revision.
- **Before interviews:** Use each file’s **Quick Revision** and **Interview Strategy** sections.
- **Patterns:** See also [patterns/two-pointers-sliding-window.md](../../patterns/two-pointers-sliding-window.md) and [patterns/leetcode-patterns.md](../../patterns/leetcode-patterns.md).

## Cross-links

- **Graph algorithms** (Dijkstra, topo, MST): [../algorithms/graph.md](../algorithms/graph.md)  
- **Union Find** (connectivity, Kruskal): [../algorithms/union-find.md](../algorithms/union-find.md)
