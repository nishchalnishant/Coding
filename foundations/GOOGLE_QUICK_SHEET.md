# Google Interview — One-Page Quick Sheet

Print or keep on a second screen during **last-minute** review (not during the interview). For full context see [GOOGLE_INTERVIEW_REVISION.md](GOOGLE_INTERVIEW_REVISION.md).

---

## Patterns → action

| Pattern | When | Core idea | Time |
|---------|------|-----------|------|
| Hash map | Two sum, frequency, grouping | Key → count or index | O(n) avg |
| Prefix + map | Subarray sum = K | Count of `prefix - K` | O(n) |
| Sliding window | Longest/shortest substring/subarray with constraint | Expand j, shrink i while invalid | O(n) |
| Two pointers | Sorted array, pair/triplet | left/right or slow/fast | O(n) or O(n²) |
| Kadane | Max subarray sum | `cur = max(x, cur+x)` | O(n) |
| BFS | Shortest path unweighted, level order | Queue + visited | O(V+E) |
| DFS | Components, cycle, topo | Stack/recursion + visited | O(V+E) |
| Topo sort | Dependencies, DAG | Kahn (in-degree) or DFS post | O(V+E) |
| Dijkstra | Weighted, non-negative | Min-heap of (dist, node) | O((V+E)log V) |
| Union-Find | Connectivity, Kruskal | find + union | ~O(1) amortized |
| Heap | Top K, merge K lists | Size-K min-heap or push all heads | O(n log k) |
| Binary search on answer | Minimize max, feasibility | `valid(mid)` + search range | O(n log range) |
| Monotonic stack | Next greater, histogram | Pop while smaller | O(n) |
| Tree DP | Max path through node | Postorder, return up value | O(n) |
| 2D DP | LCS, edit distance | `dp[i][j]` from three neighbors | O(nm) |

---

## Must-state edge cases

- Empty / null; length 1; duplicates; negative numbers; integer overflow.
- Graph: disconnected; single node; repeated edges (if relevant).

---

## Complexity sound bites

- “We visit each node/edge at most once → O(V+E).”
- “Sorting dominates → O(n log n).”
- “Hash map gives O(1) average lookup, so overall O(n).”
- “Binary search on answer: O(n) check per mid × O(log range) mids.”

---

## Open with

1. Repeat problem in your words.  
2. Ask: size limits? duplicates? can we modify input?

---

## Close with

1. Time and space.  
2. Two test cases (normal + edge).  
3. Possible follow-up (e.g. stream, huge n).

---

## Full notes

For explanations and practice lists, use [GOOGLE_INTERVIEW_REVISION.md](GOOGLE_INTERVIEW_REVISION.md) and the topic files under [data-structures/](data-structures/README.md) and [algorithms/](algorithms/README.md).
