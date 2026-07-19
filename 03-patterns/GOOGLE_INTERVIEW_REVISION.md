---
module: 03-patterns
topic: Google Interview Revision
subtopic: 
status: unread
tags: [patterns, google-interview-revision]
---

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, then use it as a lookup.
> It is NOT a coding practice file. Do not deep-study it like a topic file.


## First-Principles Breakdown

- **Root problem:** Pre-interview time is finite and anxiety-amplified; without a plan, effort concentrates on comfortable topics instead of high-signal gaps.
- **Core insight:** Revision is about retrieval practice (can I solve cold?), not re-reading — the metric is cold solve speed, not familiarity.
- **Invariant:** Tier 1 topics must be fully solid before touching Tier 3; frequency-weighted priority always dominates recency bias.
- **Why it works:** A fixed schedule eliminates decision fatigue ("what do I study today?") — that cognitive budget goes to actual problem solving.
- **Where it breaks:** If mock feedback isn't incorporated daily, the plan becomes a reading exercise rather than a performance calibration loop.

---

# Google Coding Interview — Foundations Revision Guide

Use this document for **focused revision** before your Google interview. It complements the full topic files in [01-data-structures](../01-data-structures/README.md) and [02-algorithms](../02-algorithms/README.md). Read **Part A** the day before; use **Part B** by topic; follow **Part C** for communication; use **Part D** for timing.

**Per-topic drill:** Every file under `01-data-structures/` and `02-algorithms/` includes an **Interview Questions — Logic & Trickiness** section (canonical problems + core logic + gotchas). Cross-topic index: [TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md](TOPIC_QUESTIONS_LOGIC_AND_TRICKS.md).

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

Sound bites — say them exactly like this:

- “We visit each node/edge at most once → **O(V + E)**” (BFS/DFS); Dijkstra: **O((V + E) log V)** with min-heap.
- “Sorting dominates → **O(N log N)**.”
- “Hash map gives O(1) average lookup, so overall **O(N)**.”
- “Binary search on answer: O(N) check per mid × O(log range) mids → **O(N log range)**.”
- Sliding window: usually **O(N)** time.

### Edge cases to always mention

- Empty array/string; single element; all same; negative numbers; overflow in sum/product.
- Graph: disconnected; self-loop; 0 or 1 node.
- Tree: empty tree; single node; skewed tree.

### Patterns → action (30-second triggers)

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

### Open with / Close with

**Open:** repeat the problem in your words; ask — size limits? duplicates? can we modify input?
**Close:** state time and space; run two test cases (normal + edge); name a follow-up (stream, huge n).

---

## Part B — Topic-by-Topic Revision (with links)

For each topic, skim the linked file’s **Quick Revision** and **Interview Strategy** sections, then redo **one Medium** problem cold.

### B1. Arrays & two pointers

**Must know:** Two pointers (opposite ends + same direction), sliding window (variable/fixed), prefix sum, Kadane.

- Full notes: [../01-data-structures/array.md](../01-data-structures/01-array.md)  
- Patterns: `02-algorithms/03-two-pointers.md`, `02-algorithms/04-sliding-window.md`

**Google-style practice (names only — use your platform):** Two Sum, 3Sum, Subarray Sum Equals K, Longest Substring Without Repeating Characters, Minimum Window Substring, Trapping Rain Water, Merge Intervals, Product of Array Except Self.

**Verbal template:** “I’ll use a hash map for O(N) or two pointers after sort for O(N) with O(1) space trade-off…”

---

### B2. Strings & hashing

**Must know:** Frequency map for anagrams; sliding window; KMP/Rabin-Karp at high level; palindrome (expand from center or DP).

- Full notes: [string.md](../01-data-structures/03-string.md) (DS + windows); [string algorithms](../01-data-structures/03-string.md) (KMP, Rabin-Karp), [hashing.md](../01-data-structures/02-hashing.md)

**Practice:** Group Anagrams, Valid Anagram, Longest Palindromic Substring, Minimum Window Substring, Find All Anagrams in a String.

---

### B3. Linked lists

**Must know:** Dummy node, fast/slow (middle, cycle), reverse in place, merge two sorted.

- Full notes: [data-structures/linked-list.md](../01-data-structures/07-linked-list.md)

**Practice:** Reverse Linked List, Linked List Cycle II, Merge Two Sorted Lists, Remove Nth From End.

---

### B4. Stack & queue

**Must know:** Monotonic stack (next greater, histogram), valid parentheses, monotonic deque (sliding window max).

- Full notes: [data-structures/stack.md](../01-data-structures/05-stack.md), [data-structures/queue.md](../01-data-structures/06-queue.md)

**Practice:** Daily Temperatures, Largest Rectangle in Histogram, Sliding Window Maximum, Valid Parentheses.

---

### B5. Trees & BST

**Must know:** Pre/in/post/level order; LCA (BST vs general); validate BST; tree DP (max path sum); serialize/deserialize idea.

- Full notes: [data-structures/tree.md](../01-data-structures/08-tree.md)

**Practice:** Lowest Common Ancestor, Validate BST, Binary Tree Maximum Path Sum, Serialize and Deserialize Binary Tree, Kth Smallest in BST.

---

### B6. Heaps

**Must know:** Min-heap for “K largest” (heap size K); merge K sorted lists; two heaps for median.

- Full notes: [data-structures/heap.md](../01-data-structures/10-heap.md)

**Practice:** Merge K Sorted Lists, Top K Frequent Elements, Find Median from Data Stream.

---

### B7. Binary search

**Must know:** Lower/upper bound; binary search on answer (minimize max, etc.); rotated sorted array.

- Full notes: [algorithms/11-binary-search.md](../02-algorithms/11-binary-search.md)

**Practice:** Search in Rotated Sorted Array, Find First and Last Position, Koko Eating Bananas (or similar BS-on-answer).

---

### B8. Graphs

**Must know:** Adjacency list; BFS shortest path (unweighted); DFS for components/cycle; topological sort (Kahn / DFS); Dijkstra (non-negative weights); when to use Union-Find.

- Full notes: [algorithms/graph.md](../01-data-structures/13-graphs.md), [data-structures/graphs.md](../01-data-structures/13-graphs.md)  
- Union-Find: [algorithms/union-find.md](../02-algorithms/14-union-find.md)

**Practice:** Number of Islands, Course Schedule, Rotting Oranges, Clone Graph, Word Ladder (BFS), Network Delay Time (Dijkstra).

---

### B9. Dynamic programming

**Must know:** Define state; recurrence; base case; space optimization when only previous row/column needed.

- Full notes: [15-dynamic-programming.md](../02-algorithms/15-dynamic-programming.md) · [recursion-to-dp.md](../02-algorithms/10-recursion-to-dp.md)

**Practice:** Coin Change, House Robber, Longest Increasing Subsequence, Longest Common Subsequence, Unique Paths, Edit Distance, Word Break.

---

### B10. Greedy & backtracking

**Must know:** Sort + greedy for intervals; backtracking template (choose, recurse, undo).

- Full notes: [algorithms/greedy.md](../02-algorithms/16-greedy.md), [algorithms/backtracking.md](../02-algorithms/12-backtracking.md)

**Practice:** Jump Game, Merge Intervals / Non-overlapping Intervals, Permutations, Combination Sum, Word Search.

---

### B11. Sorting (reference)

**Must know:** Merge/quick sort O(n log n); when sort enables greedy or two pointers.

- Full notes: [00-sorting.md](../02-algorithms/00-sorting.md)

---

## Part C — Communication (how to sound clear at Google)

1. **Start:** “Let me restate the problem and confirm constraints: can the array be empty? Are numbers non-negative?”
2. **Brute force:** “A naive approach would be O(…) because …”
3. **Optimize:** “We can improve by … which brings it to O(…) because …”
4. **While coding:** Narrate non-obvious indices and invariants (“`left` is always the start of the valid window”).
5. **End:** “Time is O(…), space is O(…). Edge cases: empty input, single element, …”

If stuck: “I’m considering BFS vs DFS — for shortest path in an unweighted graph I’ll use BFS because…”

---

## Part D — Revision schedules

### If you have 7 days

| Day | Focus | Action |
|-----|--------|--------|
| 1 | Arrays + hashing | Review [array](../01-data-structures/01-array.md) + [hashing](../01-data-structures/02-hashing.md); 4 problems |
| 2 | Strings + two pointers | [string](../01-data-structures/03-string.md) + sliding window pattern; 4 problems |
| 3 | Trees + BST | [tree](../01-data-structures/08-tree.md); 3 problems |
| 4 | Graphs | [graph](../01-data-structures/13-graphs.md); BFS/DFS/topo; 4 problems |
| 5 | DP | [15-dynamic-programming.md](../02-algorithms/15-dynamic-programming.md) + [recursion-to-dp.md](../02-algorithms/10-recursion-to-dp.md); 4 problems |
| 6 | Heap + binary search + stack | [heap](../01-data-structures/10-heap.md), [binary search](../02-algorithms/11-binary-search.md), [stack](../01-data-structures/05-stack.md); 4 problems |
| 7 | Mixed mock | 2 timed problems (45 min each) + review mistakes |

### If you have 48 hours

- **Hour 0–4:** Part A (this doc) + redo 2 Medium problems you failed recently.
- **Hour 4–12:** Skim Quick Revision in: array, tree, graph, DP, heap, binary search.
- **Hour 12–24:** One full mock (2 problems); note gaps only.
- **Hour 24–36:** Only gaps + Union-Find + topo sort if weak.
- **Hour 36–48:** Sleep, light review of Part A, no new problems.

### Night before

- Skim **Part A** and **edge cases**.
- Do **not** cram new topics; review **one** problem per weak area only.
- Prepare 2–3 questions for your interviewers (team, code review, on-call).

---

## Part E — After the interview

- Jot down problems you saw (titles only) while memory is fresh — helps if you have future rounds.
- Regardless of outcome, note **one** pattern to drill next time.

---

## Related repo resources

- [coding/l3-google-roadmap.md](../coding/l3-google-roadmap.md) — 4-week L3 study schedule  
- [03-patterns/patterns-master.md](patterns-master.md) — condensed patterns with triggers  

**Good luck.** You’ve already done the hard work building this repo — use Part A + one full mock in the last 48 hours to walk in confident.

---

## Document map (foundations)

| Need | File |
|------|------|
| **One-page patterns** | Part A above · [patterns-master.md](patterns-master.md) |
| **Arrays / two pointers** | [../01-data-structures/array.md](../01-data-structures/01-array.md) |
| **Graphs (compact)** | [algorithms/graph.md](../01-data-structures/13-graphs.md) |
| **Graphs (long examples)** | [data-structures/graphs.md](../01-data-structures/13-graphs.md) |
| **DP** | [../02-algorithms/15-dynamic-programming.md](../02-algorithms/15-dynamic-programming.md) |
| **Full topic index** | [01-data-structures](../01-data-structures/README.md), [02-algorithms](../02-algorithms/README.md) |
