# Google Coding Interview — Foundations Revision Guide

Use this document for **focused revision** before your Google interview. It complements the full topic files in [data-structures/](data-structures/README.md) and [algorithms/](algorithms/README.md). Read **Part A** the day before; use **Part B** by topic; follow **Part C** for communication; use **Part D** for timing.

**Per-topic drill:** Every file under `foundations/` now includes an **Interview Questions — Logic & Trickiness** section (canonical problems + core logic + gotchas). Cross-topic index: [canonical-questions.md](../problem-bank/canonical-questions.md).

---

## Part A — One-Page Quick Recall (Cheatsheet)

### What Google looks for (coding round)

- **Problem-solving**: Clarify → brute force → optimize → code → test → complexity.
- **Communication**: Think out loud; state assumptions; ask about constraints (empty input, duplicates, size limits).
- **Code quality**: Clear names, handle edge cases, correct complexity analysis.

### Topic priority (typical frequency)

| Priority | Topics | Patterns to nail |
|----------|--------|------------------|
| **1** | Arrays, Strings, Hashing | Two pointers, sliding window, prefix sum + map, frequency map |
| **2** | Trees, Graphs | BFS/DFS, LCA, topo sort, shortest path (BFS / Dijkstra) |
| **3** | DP | 1D recurrence, 2D (LCS/grid), interval DP basics |
| **4** | Heap, Binary Search | Top-K, merge K lists, BS on answer, rotated array |
| **5** | Stack/Queue | Monotonic stack, monotonic deque |

### Complexity you must state correctly

- BFS/DFS on graph: **O(V + E)** time, **O(V)** space (visited + queue/stack).
- Dijkstra: **O((V + E) log V)** with min-heap.
- Sorting: **O(N log N)**; hash map ops average **O(1)**.
- Sliding window: usually **O(N)** time.

### Edge cases to always mention

- Empty array/string; single element; all same; negative numbers; overflow in sum/product.
- Graph: disconnected; self-loop; 0 or 1 node.
- Tree: empty tree; single node; skewed tree.

### 30-second pattern triggers

| You hear / see | Think |
|----------------|--------|
| Subarray sum = K | Prefix sum + hash map (count of prefix sums) |
| Longest substring with … | Sliding window |
| Sorted + pair / triplet | Two pointers or binary search |
| Dependencies / order | Graph + topological sort |
| K largest / smallest | Heap of size K |
| Max path through node | Tree DP / postorder |
| Minimize maximum / maximize minimum | Binary search on answer |

---

## Part B — Topic-by-Topic Revision (with links)

For each topic, skim the linked file’s **Quick Revision** and **Interview Strategy** sections, then redo **one Medium** problem cold.

### B1. Arrays & two pointers

**Must know:** Two pointers (opposite ends + same direction), sliding window (variable/fixed), prefix sum, Kadane.

- Full notes: [data-structures/array.md](data-structures/array.md)  
- Patterns: [../patterns/two-pointers-sliding-window.md](../patterns/two-pointers-sliding-window.md)

**Practice:** [PROBLEM_SET.md — Arrays, hashing, two pointers, sliding window sections](../../tracks/google-sde2/PROBLEM_SET.md): Two Sum, 3Sum, Subarray Sum Equals K, Longest Substring Without Repeating Characters, Minimum Window Substring, Trapping Rain Water, Merge Intervals, Product of Array Except Self.

**Verbal template:** “I’ll use a hash map for O(N) or two pointers after sort for O(N) with O(1) space trade-off…”

---

### B2. Strings & hashing

**Must know:** Frequency map for anagrams; sliding window; KMP/Rabin-Karp at high level; palindrome (expand from center or DP).

- Full notes: [algorithms/string.md](algorithms/string.md), [data-structures/hashing.md](data-structures/hashing.md)

**Practice:** [PROBLEM_SET.md — Arrays/hashing section](../../tracks/google-sde2/PROBLEM_SET.md): Group Anagrams, Valid Anagram, Longest Palindromic Substring, Find All Anagrams in a String.

---

### B3. Linked lists

**Must know:** Dummy node, fast/slow (middle, cycle), reverse in place, merge two sorted.

- Full notes: [data-structures/linked-list.md](data-structures/linked-list.md)

**Practice:** [PROBLEM_SET.md — Linked list section](../../tracks/google-sde2/PROBLEM_SET.md): Reverse Linked List, Linked List Cycle II, Merge Two Sorted Lists, Remove Nth From End.

---

### B4. Stack & queue

**Must know:** Monotonic stack (next greater, histogram), valid parentheses, monotonic deque (sliding window max).

- Full notes: [data-structures/stack.md](data-structures/stack.md), [data-structures/queue.md](data-structures/queue.md)

**Practice:** [PROBLEM_SET.md — Stack/queue section](../../tracks/google-sde2/PROBLEM_SET.md): Valid Parentheses, Daily Temperatures, Sliding Window Maximum, Largest Rectangle in Histogram.

---

### B5. Trees & BST

**Must know:** Pre/in/post/level order; LCA (BST vs general); validate BST; tree DP (max path sum); serialize/deserialize idea.

- Full notes: [data-structures/tree.md](data-structures/tree.md)

**Practice:** [PROBLEM_SET.md — Trees/BST section](../../tracks/google-sde2/PROBLEM_SET.md): Maximum Depth, Level Order Traversal, LCA (general + BST), Validate BST, Max Path Sum, Serialize/Deserialize.

---

### B6. Heaps

**Must know:** Min-heap for “K largest” (heap size K); merge K sorted lists; two heaps for median.

- Full notes: [data-structures/heap.md](data-structures/heap.md)

**Practice:** [PROBLEM_SET.md — Heaps section](../../tracks/google-sde2/PROBLEM_SET.md): Top K Frequent Elements, Merge K Sorted Lists, Find Median from Data Stream.

---

### B7. Binary search

**Must know:** Lower/upper bound; binary search on answer (minimize max, etc.); rotated sorted array.

- Full notes: [algorithms/searching.md](algorithms/searching.md)

**Practice:** [PROBLEM_SET.md — Binary search section](../../tracks/google-sde2/PROBLEM_SET.md): Find First and Last Position, Search in Rotated Sorted Array, Find Minimum in Rotated Sorted Array, Koko Eating Bananas.

---

### B8. Graphs

**Must know:** Adjacency list; BFS shortest path (unweighted); DFS for components/cycle; topological sort (Kahn / DFS); Dijkstra (non-negative weights); when to use Union-Find.

- Full notes: [algorithms/graph.md](algorithms/graph.md), [data-structures/graphs.md](data-structures/graphs.md)  
- Union-Find: [algorithms/union-find.md](algorithms/union-find.md)  
- Advanced (if L5+): [../advanced-dsa/advanced-graphs.md](../advanced-dsa/advanced-graphs.md)

**Practice:** [PROBLEM_SET.md — Graphs section](../../tracks/google-sde2/PROBLEM_SET.md): Number of Islands, Course Schedule, Rotting Oranges, Clone Graph, Network Delay Time (Dijkstra), Word Ladder (stretch).

---

### B9. Dynamic programming

**Must know:** Define state; recurrence; base case; space optimization when only previous row/column needed.

- Full notes: [algorithms/dynamic-programming/README.md](algorithms/dynamic-programming/README.md)  
- 16 patterns: [../patterns/dp-advanced.md](../patterns/dp-advanced.md)

**Practice:** [PROBLEM_SET.md — DP section](../../tracks/google-sde2/PROBLEM_SET.md): House Robber, Coin Change, LIS (O(n log n) variant), LCS, Word Break, Edit Distance (stretch).

---

### B10. Greedy & backtracking

**Must know:** Sort + greedy for intervals; backtracking template (choose, recurse, undo).

- Full notes: [algorithms/greedy.md](algorithms/greedy.md), [algorithms/backtracking.md](algorithms/backtracking.md)

**Practice:** [PROBLEM_SET.md — Backtracking + Greedy sections](../../tracks/google-sde2/PROBLEM_SET.md): Subsets, Permutations, Combination Sum, Non-overlapping Intervals, Jump Game II.

---

### B11. Bit manipulation

**Must know:** XOR for single number; n & (n-1) clears lowest bit; bitmask for subsets when N small.

- Full notes: [algorithms/bit-manipulation.md](algorithms/bit-manipulation.md)

---

### B12. Maths & sorting

**Must know:** GCD, modular arithmetic basics; merge/quick sort complexity; when counting sort applies.

- Full notes: [algorithms/maths.md](algorithms/maths.md), [algorithms/sorting.md](algorithms/sorting.md)

---

## Part C — Communication (how to sound clear at Google)

1. **Start:** “Let me restate the problem and confirm constraints: can the array be empty? Are numbers non-negative?”
2. **Brute force:** “A naive approach would be O(…) because …”
3. **Optimize:** “We can improve by … which brings it to O(…) because …”
4. **While coding:** Narrate non-obvious indices and invariants (“`left` is always the start of the valid window”).
5. **End:** “Time is O(…), space is O(…). Edge cases: empty input, single element, …”

If stuck: “I’m considering BFS vs DFS — for shortest path in an unweighted graph I’ll use BFS because each level guarantees minimum distance.”

**Example dialogue — Two Sum:**
> “So we need to find two indices that sum to target. Let me confirm: can indices be the same? Is there always exactly one answer? [Wait.] Brute force is O(n²) — check all pairs. We can do better: scan once, storing each value in a hash map keyed by the complement target-x. When we see a value whose complement is already in the map, we return both indices. This is O(n) time, O(n) space. Edge case: same element can’t be used twice, so I’ll check the index stored in the map isn’t the current index.”

---

## Part D — Revision schedules

### If you have 7 days

| Day | Focus | Action |
|-----|--------|--------|
| 1 | Arrays + hashing | Review [array](data-structures/array.md) + [hashing](data-structures/hashing.md); 4 problems |
| 2 | Strings + two pointers | [string](algorithms/string.md) + sliding window pattern; 4 problems |
| 3 | Trees + BST | [tree](data-structures/tree.md); 3 problems |
| 4 | Graphs | [graph](algorithms/graph.md); BFS/DFS/topo; 4 problems |
| 5 | DP | [DP README](algorithms/dynamic-programming/README.md) + [dp-advanced](../patterns/dp-advanced.md); 4 problems |
| 6 | Heap + binary search + stack | [heap](data-structures/heap.md), [searching](algorithms/searching.md), [stack](data-structures/stack.md); 4 problems |
| 7 | Mixed mock | 2 timed problems (45 min each) + review mistakes |

### If you have 48 hours

- **Hour 0–4:** Part A (this doc) + redo 2 Medium problems you failed recently.
- **Hour 4–12:** Skim Quick Revision in: array, tree, graph, DP README, heap, searching.
- **Hour 12–24:** One full mock (2 problems); note gaps only.
- **Hour 24–36:** Only gaps + Union-Find + topo sort if weak.
- **Hour 36–48:** Sleep, light review of Part A, no new problems.

---

## Part E — 30-Minute High-Intensity Revision Blitz

Use this in the final 30 minutes before your interview. Do NOT solve new problems. Just recall these "Click Logic" triggers.

### E1. The "Click" Logic (Fastest Recall)

| If you see this... | Your brain should go... |
| :--- | :--- |
| **Subarray Sum = K** | Prefix Sum + Map of `{sum: frequency}` |
| **Next Greater Element** | Monotonic Stack (Store indices) |
| **Shortest Path (Weighted)** | Dijkstra (Min-Heap) |
| **Shortest Path (Unweighted)** | BFS (Queue) |
| **Dependencies / Order** | Topological Sort (Kahn's) |
| **Top K / Frequent** | Min-Heap of size K |
| **Maximize the Min / Min the Max** | Binary Search on Answer |
| **"Contiguous"** | Sliding Window |
| **"Subsequence"** | DP (Take or Skip) |
| **Small N (N <= 20)** | Backtracking or Bitmask DP |

### E2. Critical Gotchas (Last Check)

1. **Duplicates?** Skip them in 3-sum, subsets, and permutations (`if i > start and nums[i] == nums[i-1] continue`).
2. **Negatives?** Simple Sliding Window doesn't work for "Sum = K" with negatives; use Prefix Sum + Map.
3. **Empty Input?** Always handle `if not root:` or `if not nums:` first.
4. **Overflow?** Use `low + (high - low) // 2` for binary search mid.
5. **Circular?** Connect end to start or double the array (`nums + nums`).

### E3. Communication Checklist
- [ ] **Restate** the problem.
- [ ] **Clarify** constraints (sorted? unique? memory?).
- [ ] **State** complexity BEFORE coding.
- [ ] **Test** with a small edge case manually.

---

## Part F — After the interview

- Jot down problems you saw (titles only) while memory is fresh — helps if you have future rounds.
- Regardless of outcome, note **one** pattern to drill next time.

---

## Related repo resources

- [../google-sde2/README.md](../google-sde2/README.md) — **Google SDE-2 (L4)** track: loop variants, file index  
- [../google-sde2/TWO_WEEK_REVISION.md](../google-sde2/TWO_WEEK_REVISION.md) — **14-day** plan, **2× DSA** (virtual + on-site) + **AI-ML** when applicable  
- [SDE3_DSA_ROADMAP.md](../SDE3_DSA_ROADMAP.md) — longer problem order and weekly plan  
- [sde-3-guide/sde-3-guide.md](../sde-3-guide/sde-3-guide.md) — Top 20 curated problems  
- [patterns/leetcode-patterns.md](../patterns/leetcode-patterns.md) — condensed patterns  

**Good luck.** You’ve already done the hard work building this repo — use Part A + one full mock in the last 48 hours to walk in confident.

---

## Document map (foundations)

| Need | File |
|------|------|
| **One-page patterns** | [quick-recall.md](quick-recall.md) |
| **Arrays / two pointers** | [data-structures/array.md](../../tracks/foundations/data-structures/array.md) |
| **Graphs (traversal + topo)** | [data-structures/graphs.md](../../tracks/foundations/data-structures/graphs.md) |
| **Graphs (Dijkstra, Bellman-Ford, MST)** | [algorithms/graph.md](../../tracks/foundations/algorithms/graph.md) |
| **DP** | [algorithms/dynamic-programming/README.md](../../tracks/foundations/algorithms/dynamic-programming/README.md) |
| **Full topic index** | [data-structures/](../../tracks/foundations/data-structures/), [algorithms/](../../tracks/foundations/algorithms/) |
