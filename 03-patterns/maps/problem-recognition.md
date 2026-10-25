---
module: striver-a2z
topic: Interview problem recognition mind map
 tags: [mind-map, problem-solving, interview, dsa]
---
# Problem Recognition Mind Map

← [Striver course map](../../striver-a2z/README.md) · [Pattern triggers](pattern-triggers.md) · [Problem index](../../striver-a2z/PROBLEM_INDEX.md)

Use this as a routing guide, not a list of rigid rules. First identify the input shape and the operation being repeated; then pick a candidate pattern, state its invariant, and test it against a small example. If more than one pattern fits, compare complexity and implementation risk.

## Quick triage

| Prompt signal / shape | First patterns to consider | Core move |
|---|---|---|
| Need membership, counts, or duplicates | Hash map / set | Store what was seen or its frequency |
| Contiguous range or subarray | Prefix sums, sliding window, monotonic deque | Use prefix differences, or maintain a valid moving window |
| Sorted data or monotone yes/no condition | Binary search / two pointers | Find a boundary or shrink a feasible interval |
| Next greater/smaller, nearest boundary | Monotonic stack | Keep candidates in sorted order; pop dominated values |
| Top K, repeatedly choose smallest/largest | Heap | Keep only K candidates or the next best item |
| All combinations, arrangements, paths | Backtracking | Choose, recurse, undo; prune impossible branches |
| Choices with repeated subproblems | Dynamic programming | Define state, recurrence, base case, evaluation order |
| Reachability, dependencies, shortest route | Graph traversal / topo / shortest path | Model nodes and edges; choose by edge/weight structure |
| Merge connectivity or answer dynamic components | DSU | Union groups and query representatives |
| Prefix lookup or bitwise maximum XOR | Trie | Walk a shared prefix or greedily choose opposite bits |
| Many range queries / point changes | Prefix/Fenwick/segment tree | Pick structure by update/query operations |
| Intervals overlap or events occur over time | Sort + sweep / heap | Process endpoints in order while maintaining active set |
| Design an API or stateful object | Data-structure composition / OOD | Define invariants, operations, and complexity |
| Scale, availability, storage, async work | System design | Clarify requirements, model traffic/data, then trace bottlenecks |

## 1. Arrays, hashing, and prefix techniques

### Arrays and in-place transformations

- **Find, count, or transform each element:** linear scan; maintain the needed best-so-far value or write pointer. See [Arrays](../../striver-a2z/14-arrays/README.md).
- **Sorted array, remove duplicates, merge, or compact:** two pointers; one pointer reads, another writes the next retained value.
- **Rotate, reverse, or rearrange in place:** reversal blocks, cyclic placement, or index mapping; check whether extra space is allowed.
- **Find a pair/triple with target relation:** hash lookup when order is arbitrary; sort plus two pointers when output needs unique combinations.
- **Subarray sum equals K:** prefix sum + frequency map; add the count of prior prefix values `current-K`.
- **Longest subarray with sum K:** prefix sum + earliest index; for nonnegative values, a sliding window may suffice.
- **Maximum contiguous sum:** Kadane; at each position choose extend-current or restart.
- **Majority / frequent values:** Boyer–Moore candidate selection, then verify; use a map if arbitrary frequency ranking is needed.
- **Merge-sort counting:** inversions, reverse pairs, or cross-half counts; count while merging sorted halves.
- **Matrix transformation / traversal:** choose row/column scans, boundary shrinking, or in-place transpose + reverse. For sorted matrix search, use binary search or staircase elimination.

### Hashing and frequency

- **Anagram, isomorphism, duplicate detection:** frequency vector/map or last-seen map; normalize keys consistently.
- **Longest consecutive run:** set; only start a run at values with no predecessor.
- **Count subarrays with a sum/XOR:** running prefix state + frequency map; seed the empty prefix.
- **Group strings by signature:** canonical key such as sorted characters or frequency counts.

## 2. Two pointers and sliding windows

See [Sliding Window / 2 Pointer](../../striver-a2z/22-sliding-window-and-2-pointer/README.md).

- **Pair in sorted input / compare ends:** move the pointer whose choice cannot lead to a valid answer.
- **Longest substring/subarray satisfying a constraint:** expand right; while invalid, move left and update counts. State exactly what makes the window valid.
- **At most K distinct / no duplicates:** frequency map plus shrink loop.
- **Exactly K distinct or exactly K odd values:** compute `atMost(K) - atMost(K-1)` when the predicate is monotone by K.
- **Minimum window covering required counts:** expand until covered, then shrink while coverage remains.
- **Fixed-size window:** add entering item and remove leaving item; maintain aggregate incrementally.
- **When window does not work:** negative values often break monotonicity; consider prefix sums, a deque, or ordered data structure instead.

## 3. Binary search and sorted structure

See [Binary Search](../../striver-a2z/16-binary-search/README.md).

- **Find value / first or last occurrence:** lower/upper-bound templates; define the interval and invariant before coding.
- **Rotated sorted array / peak / single element:** compare mid with a neighbor or sorted half to discard one side.
- **Minimum feasible capacity/time/speed:** binary search on the answer if feasibility changes monotonically; write a greedy feasibility check.
- **Kth element / median of two sorted arrays:** binary search a partition; verify left max ≤ right min.
- **2D row/column sorted matrix:** flattened binary search if globally sorted; staircase search if rows and columns are independently sorted.
- **Floating-point answer:** fixed iteration count or precision-based loop; define stopping condition and rounding needs.

## 4. Stack, queue, and monotonic structures

See [Stack / Queues](../../striver-a2z/23-stack-and-queues/README.md).

- **Balanced delimiters / expression evaluation:** stack; track nesting or operator precedence.
- **Next greater/smaller element, stock span:** monotonic stack of unresolved indices; resolve items when a better boundary arrives.
- **Largest rectangle / contribution of each value:** nearest smaller boundaries; handle equal values consistently.
- **Sliding-window maximum/minimum:** monotonic deque of indices; remove expired and dominated entries.
- **Min stack / max stack:** store auxiliary extrema or encoded state so each operation stays O(1).
- **Queue/stack implementation questions:** choose two stacks, linked nodes, or array ring buffer; state amortized versus worst-case cost.
- **LRU cache:** hash map + doubly linked list. **LFU cache:** key map + frequency buckets + recency order within each bucket.

## 5. Linked lists

See [Linked List](../../striver-a2z/19-linked-list/README.md).

- **Middle, cycle, cycle start:** slow/fast pointers; prove meeting and offset logic.
- **Reverse list / reverse in groups:** pointer rewiring; keep previous/current/next or use a dummy node.
- **Nth from end / intersection:** two pointers with a fixed gap or pointer switching.
- **Merge sorted lists / sort list:** dummy head for merge; merge sort for O(n log n) list sorting.
- **Palindrome / reorder:** find midpoint, reverse half, compare or weave.
- **Random pointer clone:** hash map or interleave copied nodes, then separate.
- **Pointer-heavy operations:** draw a 3–5 node example and track every link before writing code.

## 6. Trees and BSTs

See [Binary Trees](../../striver-a2z/24-binary-trees/README.md) and [Binary Search Trees](../../striver-a2z/25-binary-search-trees/README.md).

- **Visit every node in a requested order:** DFS recursion/stack or BFS queue.
- **Height, balance, diameter, path maximum:** postorder; return the information the parent needs and update a global answer if needed.
- **Path to target / root-to-leaf constraints:** DFS carrying path/state; backtrack path after each branch.
- **Level, vertical, boundary, top/bottom view:** BFS with depth/column metadata; define tie-breaking explicitly.
- **Lowest common ancestor:** recursive split for general tree; exploit ordering in BST.
- **Build/serialize/flatten tree:** encode traversal ranges or explicit null markers; verify shape with a small tree.
- **BST range / predecessor / successor / kth:** use ordering to prune; inorder gives sorted sequence.
- **Subtree or ancestor query at scale:** Euler tour + range structure or binary lifting; see [advanced trees and graphs](../../striver-a2z/32-beyond-the-sheet/03-advanced-trees-and-graphs-theory.md).

## 7. Heaps and ordering

See [Heaps](../../striver-a2z/26-heaps/README.md).

- **Top K largest/smallest:** keep a heap of size K, or full heap when K is large.
- **Merge K sorted streams/lists:** heap stores each source's current head and source index.
- **Running median:** max-heap for lower half + min-heap for upper half; rebalance sizes.
- **Scheduling by next available time:** min-heap keyed by end time / release time.
- **Repeatedly combine cheapest/lightest items:** min-heap; each operation adds a newly combined candidate.
- **Sort nearly sorted data:** heap of about K+1 next candidates.

## 8. Graphs

See [Graphs](../../striver-a2z/27-graphs/README.md).

- **Reachability / connected components / grid regions:** BFS or DFS; mark when enqueued/entered.
- **Shortest path, unweighted edges:** BFS.
- **Shortest path, nonnegative weights:** Dijkstra; discard stale heap entries.
- **Negative weights / detect negative cycle:** Bellman–Ford.
- **All-pairs shortest distances:** Floyd–Warshall for small/dense graphs; otherwise repeated appropriate single-source runs.
- **Prerequisites / dependency order:** topological sort; if not all vertices process, a cycle exists.
- **Dynamic connectivity / components merge:** DSU with path compression and union by size/rank.
- **Minimum spanning tree:** Kruskal + DSU or Prim + heap.
- **Bipartite / two-color constraints:** BFS/DFS coloring.
- **Bridge / articulation point:** Tarjan discovery and low-link times.
- **State-expanded shortest path:** node plus state (keys, stops, mask, parity); choose BFS/Dijkstra based on transition weights.
- **Grid with 0/1 transition costs:** 0-1 BFS using deque; for general nonnegative cost, Dijkstra.

## 9. Recursion, backtracking, and combinatorics

See [Recursion](../../striver-a2z/18-recursion/README.md).

- **Generate subsets / subsequences:** include/exclude decisions; O(2^n) output-sensitive enumeration.
- **Permutations:** choose an unused element at each position; swap-in-place or used-marker approach.
- **Combination sum / choose K under constraints:** recurse over candidates; sort and prune when the remaining target cannot be met.
- **Duplicate input with unique outputs:** sort, then skip equal choices at the same recursion depth.
- **Constraint satisfaction (N-Queens, Sudoku, coloring):** choose a variable, try legal candidates, undo; prune immediately on constraint violation.
- **Grid word/path search:** mark current cell, explore neighbors, unmark on return; prevent revisiting per path.
- **Count vs list all solutions:** counting may allow memoization; enumeration has output-size lower bounds.

## 10. Dynamic programming

See [Dynamic Programming](../../striver-a2z/28-dynamic-programming/README.md) and [Advanced DP](../../striver-a2z/32-beyond-the-sheet/02-advanced-dp-theory.md).

Start with: **state** (what decisions/history matter?), **transition** (last choice), **base cases**, **answer state**, then memoize or tabulate.

- **One-dimensional take/skip:** house robber, non-adjacent sum; state by prefix/index and whether previous choice constrains it.
- **Grid path / min or max cost:** state `(row, col)`; transition from legal predecessors; add obstacles/boundaries to base cases.
- **Subset sum / knapsack:** state `(item index, remaining capacity/sum)`; choose take/skip; compress dimension only with correct iteration direction.
- **Unbounded choices / coin change:** reuse current item; distinguish counting combinations from permutations by loop order.
- **String alignment / subsequence:** state `(i,j)`; match or skip; examples include LCS, edit distance, wildcard matching.
- **Longest increasing subsequence:** O(n²) DP or patience-sorting tails for length; reconstruct with predecessor indices if needed.
- **Stock state machine:** day + holding/transactions/cooldown state.
- **Interval DP:** choose the final split/operation in interval `[l,r]` (MCM, burst balloons).
- **Tree DP / rerooting:** combine child states; reroot when each node needs an answer as root.
- **Bitmask DP:** small number of entities and subset state; typical n around 20 or below.
- **Digit DP:** count bounded integers by position, tightness, and relevant digit properties.
- **Common pitfall:** do not force DP where a greedy invariant or graph shortest path is simpler. Define state before coding.

## 11. Greedy algorithms and intervals

See [Greedy Algorithms](../../striver-a2z/21-greedy-algorithms/README.md).

- **Select maximum compatible intervals:** sort by finishing time; prove earliest finish leaves the most room.
- **Merge or insert intervals:** sort by start and merge while ranges overlap.
- **Minimum resources for overlaps:** sort starts/ends or use a min-heap of active end times.
- **Jump/reachability:** maintain farthest reachable boundary; for minimum jumps, advance by BFS-like layers.
- **Deadline scheduling:** order by deadline/profit structure; verify the exchange argument or use heap.
- **Greedy suspicion check:** construct a counterexample to the tempting local choice; if one exists, consider DP, heap, or sorting plus proof.

## 12. Strings, tries, and bit operations

See [Strings](../../striver-a2z/17-strings-basic-medium/README.md), [Advanced strings](../../striver-a2z/30-strings-advanced/README.md), [Tries](../../striver-a2z/29-tries/README.md), and [Bit manipulation](../../striver-a2z/20-bit-manipulation/README.md).

- **Substring with constraints:** sliding window if validity can be repaired monotonically; otherwise prefix/state DP.
- **Pattern matching:** KMP for linear matching with prefix reuse; Z algorithm for prefix matches; rolling hash for fingerprints (verify collisions where correctness requires).
- **Prefix dictionary / many starts-with queries:** trie; store terminal/count metadata as needed.
- **Maximum XOR:** binary trie greedily follows opposite bits; be clear about signed versus unsigned ranges.
- **Odd/even, subsets, flags, powers of two:** bit masks and bit operations; check width and signedness.
- **Single number among pairs/triples:** XOR or bit counts based on multiplicity guarantees.
- **Parentheses/string parsing:** stack or finite-state scan; state transitions often beat regex.

## 13. Math, number theory, and advanced range queries

See [Maths](../../striver-a2z/31-maths/README.md) and [Range Queries](../../striver-a2z/32-beyond-the-sheet/01-range-queries-theory.md).

- **Prime tests / many prime queries:** trial division for one small value; sieve for a range; segmented sieve for large interval with manageable width.
- **GCD / divisibility / modular powers:** Euclid, gcd normalization, fast exponentiation; avoid multiplication overflow in modular arithmetic.
- **Static range sum:** prefix sums. **Static idempotent min/max:** sparse table. **Point updates + range aggregate:** Fenwick or segment tree. **Range updates:** difference array offline or lazy segment tree online.
- **Many offline queries / sorted thresholds:** sort queries with events and process in order; coordinate-compress values if only ordering matters.
- **Large n around 40 and subset constraints:** meet in the middle.
- **Overlapping time intervals:** sweep line; process event ordering carefully at equal endpoints.

## 14. Design and engineering interview problem types

See [SDE 2 interview preparation](../../striver-a2z/33-sde2-interview-prep/README.md).

### Low-level / object design

- **Stateful object with strict operation costs:** combine data structures (LRU, LFU, min stack); state invariants and complexity.
- **Domain model with interchangeable policies:** define small interfaces; use composition/Strategy where actual variation exists.
- **Scheduling / allocation / reservation:** model lifecycle and state transitions; handle conflicts and concurrency.
- **API-heavy design:** clarify contracts, error cases, pagination, idempotency, and versioning.

### High-level / system design

- **Large read-heavy product (feed, catalog):** access patterns, caching, precompute versus on-demand fanout.
- **Event or notification delivery:** queues, retries, deduplication, ordering, rate limits, dead-letter handling.
- **Search or nearby lookup:** indexing, partitioning, candidate generation, ranking, freshness.
- **File/media storage:** metadata versus blob storage, upload/download flow, permissions, lifecycle and replication.
- **Realtime communication:** persistent connections, presence, delivery state, offline queues, fanout.
- **Rate limiting / metrics ingestion:** key partitioning, approximate counters, aggregation, bounded memory.

For any system prompt: clarify core use cases and scale; propose APIs and data model; draw a simple architecture; trace one write and one read; find the bottleneck; discuss failure, consistency, security, monitoring, and trade-offs.

## 15. Interview execution and behavioral prompts

See [Interview execution](../../striver-a2z/33-sde2-interview-prep/01-interview-execution.md) and [Behavioral stories](../../striver-a2z/33-sde2-interview-prep/05-behavioral-and-project-stories.md).

- **Coding round:** clarify → examples → baseline → optimize → implement → test → complexity.
- **Debug/review round:** find a smallest counterexample; identify violated invariant; patch and add a regression case.
- **Project deep dive:** problem → role → design choices → launch/operation → measured outcome → learning.
- **Behavioral question:** prepare a true, specific story; distinguish your actions from team actions; include result and reflection.

## If two patterns seem plausible

1. Write the brute-force solution and identify the repeated work.
2. Name the invariant a faster solution would maintain.
3. Check whether the prompt's constraints make that invariant valid (for example, negative numbers invalidate many sliding-window sum approaches).
4. Compare time, space, and implementation complexity.
5. Dry-run duplicates, boundaries, and a case designed to break the assumption.
