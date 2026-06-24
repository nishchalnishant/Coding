---
tags: [coding, sde3, dsa, completeness, audit]
topic: SDE-3 DSA Completeness Addendum
difficulty: reference
---

# SDE-3 DSA Completeness Addendum

This note is the audit companion for the repo. The core material already covers the interview staples; this page fills the gaps that matter when the bar moves from "solve the problem" to "solve it cleanly, prove it, and know the right variant to use".

> [!important] SDE-3 bar for DSA
> You are expected to do more than recall templates. You should:
> - pick the correct family of algorithms from the constraints,
> - state the invariant before coding,
> - prove correctness at a high level,
> - compare alternatives honestly,
> - and know the harder follow-up variant if the interviewer pushes.

---

## What the repo already covers well

- Core data structures: arrays, strings, linked lists, stacks, queues, heaps, hash maps, trees, tries, graphs, segment trees.
- Core algorithms: recursion, backtracking, binary search, greedy, divide-and-conquer, DP, graph algorithms, bit manipulation, union-find, string matching.
- Interview framing: complexity, Google-specific communication, and problem pattern recognition.

## What is often still missing at SDE-3 level

### Advanced graph depth

- **Tarjan articulation points**: not just bridges, but the node version of the same low-link idea.
- **Strongly connected components**: SCC condensation graph, reverse topological reasoning, and when Kosaraju vs Tarjan is simpler.
- **Eulerian path / Hierholzer**: itinerary-style problems where every edge must be used exactly once.
- **0-1 BFS**: the shortest-path trick when edge weights are only `0` and `1`.
- **Bidirectional BFS**: massive reduction for shortest-path-in-unweighted-graph problems.
- **Shortest path on DAGs**: topological ordering plus relaxation.
- **Floyd-Warshall**: dense-all-pairs shortest path and transitive closure.

### Advanced data structure depth

- **Fenwick tree variants**: range update + point query, point update + range query, and the idea of two BITs for range update + range query.
- **Persistent segment tree**: immutable versions for order statistics and historical queries.
- **Order statistic tree / Treap**: ranked lookup, k-th smallest, and dynamic sorted order.
- **Interval tree / sweep-line structures**: overlap queries, calendar booking, and event intersection problems.
- **Bloom filter**: probabilistic membership test when false positives are acceptable.
- **Skip list**: randomized ordered structure that behaves like a simpler balanced tree.

### Advanced string depth

- **Aho-Corasick**: multi-pattern matching at scale.
- **Suffix array / LCP**: all-substring reasoning, repeated substring questions, and lexicographic suffix order.
- **Suffix automaton**: compact representation for substring problems.
- **Rolling hash details**: double hashing, collision awareness, and substring equality.

### Advanced bit / DP depth

- **Bitmask DP**: subset states, traveling-salesman style transitions, and small-`n` exponential solutions.
- **Submask enumeration**: the `sub = (sub - 1) & mask` trick.
- **XOR basis**: stronger than XOR tricks when the question asks for linear independence over bits.

---

## Canonical SDE-3 follow-up questions to be able to answer

### Graphs

1. Can you detect a bridge and explain `low[]` vs `disc[]`?
2. Can you find articulation points and explain why the root case is special?
3. Can you decompose a directed graph into SCCs and explain the condensation graph?
4. Can you solve shortest path with `0/1` weights without a heap?
5. Can you do shortest path on a DAG in linear time after topological sort?

### Data structures

1. Can you support range updates and range queries efficiently?
2. Can you explain when BIT is simpler than a segment tree?
3. Can you use a persistent tree for versioned queries?
4. Can you maintain sorted order with insert/delete and rank queries?
5. Can you explain the tradeoff between skip list, BST, and treap?

### Strings

1. Can you match many patterns against one text in one pass?
2. Can you reason about suffix order and repeated substrings?
3. Can you explain why rolling hash is probabilistic and how to reduce collisions?

### Bit / combinatorics

1. Can you enumerate all subsets and all submasks without extra memory?
2. Can you recognize bitmask DP when `n <= 20`?
3. Can you explain why some XOR problems need a basis instead of a simple trick?

---

## Missing-content checklist for revision

- Know the invariant first; code second.
- State the asymptotic cost of every operation, not just the headline complexity.
- Be able to compare at least two alternatives for every topic.
- Know the edge cases: empty input, duplicates, disconnected graphs, skewed trees, overflow, and negative values.
- Be able to explain why the "easy" solution fails to scale.
- Be able to say when a problem is actually a disguised version of a known pattern.

---

## Where to read next in this repo

- `coding/data-structures/advanced.md`
- `coding/data-structures/graph.md`
- `coding/data-structures/trie.md`
- `coding/algorithms/graph-algorithms.md`
- `coding/algorithms/bit-manipulation.md`
- `coding/algorithms/string-algorithms.md`
- `coding/algorithms/dynamic-programming.md`
- `coding/complexity-cheatsheet.md`

## Final bar

If you can explain the invariant, prove correctness, derive complexity, and handle the obvious follow-up variant without panic, you are at the right DSA level for a Google / Meta / Amazon / Microsoft SDE-3 loop.
