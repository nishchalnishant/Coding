# Data Structures — Start Here

Deep-dive notes for **Amazon SDE-2** coding interviews. Each topic file is self-contained; this page is your **navigation hub** — use it to pick what to read and in what order.

**Repo hub:** [00-start-here/README.md](../00-start-here/README.md) · **Patterns (when to use what):** [03-patterns/patterns-master.md](../03-patterns/patterns-master.md) · **Algorithms (techniques):** [02-algorithms/README.md](../02-algorithms/README.md) · **Problem walkthroughs:** [02-algorithms/problem-deep-dives.md](../02-algorithms/problem-deep-dives.md)

---

## Pick your path

| If you… | Do this |
|---------|---------|
| **Have ~2 weeks** (Amazon SDE-2 loop) | Follow **Must-nail for SDE-2** below → one topic/day → **Quick Revision Triggers** on final days. |
| **Are learning a topic for the first time** | Open the topic file → skim **First-Principles Map** → read **Core Algorithms & Click Moments** → do 2–3 problems from **Interview Questions** table. |
| **Are revising before a mock** | Read **Quick Revision Triggers** + **Interview Questions — Logic & Trickiness** only (skip theory). |
| **Stuck on “which DS?”** | Open [ds_tree.md](./ds_tree.md) — decision tree + pattern → structure mapping. |

---

## Topic index

| Topic | Difficulty | Key patterns | File |
|-------|------------|--------------|------|
| **Arrays** | Easy–Hard | Two pointers, sliding window, prefix sum, Kadane | [array.md](./array.md) |
| **Strings** | Easy–Hard | Sliding window, frequency map, KMP / Rabin-Karp | [string.md](./string.md) |
| **Linked lists** | Easy–Med | Fast/slow, dummy node, reverse in place | [linked-list.md](./linked-list.md) |
| **Stacks** | Easy–Med | Monotonic stack, brackets, next greater | [stack.md](./stack.md) |
| **Queues / deque** | Easy–Med | BFS, monotonic deque, sliding window max | [queue.md](./queue.md) |
| **Trees / BST** | Med–Hard | DFS/BFS, LCA, validate BST, tree DP | [tree.md](./tree.md) |
| **Heaps** | Med–Hard | Top-K, merge K sorted, two-heap median | [heap.md](./heap.md) |
| **Hash maps** | Easy–Med | Frequency, two sum, grouping, prefix + map | [hashing.md](./hashing.md) |
| **Tries** | Med | Prefix search, word break, XOR trie | [trie.md](./trie.md) |
| **Graphs** | Med–Hard | BFS/DFS, topo, union-find; weighted → [graph.md](../02-algorithms/graph.md) | [graphs.md](./graphs.md) |
| **Segment trees** | Hard — awareness only | Range query/update — not tested at SDE-2 | [segment-tree.md](./segment-tree.md) |
| **Advanced** | Varies | LRU/LFU (must know), Bloom filter (awareness), skip list (awareness) | [advanced-structures.md](./advanced-structures.md) |
| **DS decision tree** | — | “Which structure for this constraint?” | [ds_tree.md](./ds_tree.md) |

---

## How every topic file is organized

Read top-to-bottom on first pass; on revision, jump to the **bold** sections.

| Section | When to read |
|---------|----------------|
| **First-Principles Map** + **Breakdown** | First visit — *why* this DS exists and when it breaks |
| **Concept Overview** / **Core Algorithms** | Learn implementations and “click moments” |
| **SDE-3 Deep Dives** | Optional stretch; skip until L4 set is solid |
| **Common Interview Problems** | Problem list with one-line hints |
| **Interview Questions — Logic & Trickiness** | **High yield** — pattern, logic, gotchas in one table |
| **Quick Revision Triggers** | **Day-before / mock prep** — phrase → technique |
| **See also** | Cross-links to algorithms + patterns |
| **Flashcards** | Obsidian / spaced repetition (`#flashcard` tags) |

---

## Study progression (beginner → advanced)

**Foundation (~week 1)**  
1. [array.md](./array.md) — prefix sum, two-pointer, sliding window  
2. [hashing.md](./hashing.md) — frequency maps, two sum  
3. [string.md](./string.md) — treat as char arrays + windows  
4. [linked-list.md](./linked-list.md) — dummy node, fast/slow  

**Core L4 (~week 1–2)**  
5. [stack.md](./stack.md) — monotonic stack  
6. [queue.md](./queue.md) — BFS + monotonic deque  
7. [tree.md](./tree.md) — traversals, LCA, BST  
8. [graphs.md](./graphs.md) — BFS/DFS, topo, grids  

**Differentiators (~week 3+)**  
9. [heap.md](./heap.md) — top-K, merge K, median stream  
10. [trie.md](./trie.md) — prefix / dictionary problems  
11. Union-find — [union-find.md](../02-algorithms/union-find.md)  

**Awareness only (do not spend implementation time)**  
[segment-tree.md](./segment-tree.md) — know it exists, what problem it solves; not tested at SDE-2.  
[advanced-structures.md](./advanced-structures.md) — LRU/LFU must know; Bloom filter, skip list: know what they are.

---

## Must-nail for Amazon SDE-2

| Priority | Topics |
|----------|--------|
| **Very high** | Arrays, hashing, trees, graphs, strings |
| **High** | Stacks, heaps, linked lists |
| **Medium** | Tries, queues, union-find |
| **Awareness only** | Segment trees, Fenwick trees, persistent/exotic structures — not expected at SDE-2 |

---

## DS selection cheat sheet

Full decision tree: [ds_tree.md](./ds_tree.md).

| You need… | Reach for… |
|-----------|------------|
| O(1) lookup by key | Hash map / hash set |
| Sorted order + dynamic insert | BST / TreeMap |
| Min or max always available | Heap |
| Prefix on strings | Trie |
| Range sum, **static** data | Prefix sum |
| Range query + **updates** | Segment tree / BIT |
| Next greater / histogram | Monotonic stack |
| Sliding window max | Monotonic deque |
| Shortest path (unweighted) | BFS on graph |
| Connectivity / components | DFS or union-find |

---

## First-principles map (compact)

```text
WHY → different access patterns need different structures
WHAT → array, list, stack, queue, hash, tree, heap, trie, graph, segment tree
HOW  → match dominant operation (lookup / order / range / hierarchy / connectivity)
WHEN → see table above and ds_tree.md
RISK → wrong DS caps complexity no matter how clever the algorithm
```

For the expanded ASCII map (same content as before), see the top of [ds_tree.md](./ds_tree.md).
