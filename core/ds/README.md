# The Data Structures Library: A Guided Tour

Welcome to the toolkit. As an SDE-3, you don't just "use" a data structure; you choose it based on its memory footprint, concurrency safety, and cache locality. 

In this section, we're not just going to talk about how to push to a stack. We're going to talk about **why** a Monotonic Stack is the gold standard for "Next Greater Element" and how to implement an **LRU Cache** that won't fail under high-concurrency pressure.

### Our Approach:
1.  **Theory & Mental Models**: We'll talk about the "Click Moment" for each structure.
2.  **Core Algorithms**: SDE-3 canonical code templates that you can write in your sleep.
3.  **SDE-3 Deep Dives**: The "Staff-level" stuff—lock-free designs and distributed scalability.
4.  **The Dialogue**: Tips on how to explain your choices to an interviewer.

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
| **Advanced** | [advanced-structures.md](advanced-structures.md) | Segment Trees, Fenwick Trees, Sparse Tables, Disjoint Set variants. |
| **Tree Index** | [ds_tree.md](ds_tree.md) | Master hierarchical index of all DS patterns and variants. |

## How to use

- **Learn a topic:** Open the topic file; read Concept Overview → Core Algorithms → Pattern Recognition → Interview Strategy → Quick Revision.
- **Before interviews:** Use each file’s **Quick Revision** and **Interview Strategy** sections.
- **Patterns:** See also [../../reference/patterns/patterns-master.md](../../reference/patterns/patterns-master.md).

## Cross-links

- **Graph algorithms** (Dijkstra, topo, MST): [../algo/graph.md](../algo/graph.md)  
- **Union Find** (connectivity, Kruskal): [../algo/union-find.md](../algo/union-find.md)
