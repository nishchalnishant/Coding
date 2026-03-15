# SDE-3 DSA Practice Roadmap

A structured plan to use this repository for SDE-3 level DSA interview preparation: problem order, difficulty progression, weekly plan, and mock strategy.

---

## 1. Recommended Problem Order (By Topic)

Follow this order within each topic so that patterns build on each other.

### Arrays & Two Pointers
1. Two Sum → 3Sum → 4Sum (hash / two pointers)
2. Best Time to Buy/Sell Stock → Trapping Rain Water (two pointers / state)
3. Subarray Sum Equals K (prefix + map) → Maximum Product Subarray (Kadane variant)
4. Merge Intervals → Insert Interval → Non-overlapping Intervals (sort + scan)
5. Median of Two Sorted Arrays (binary search)

### Binary Search
1. Binary Search → Search Insert Position → First/Last Position
2. Search in Rotated Sorted Array → Search in Rotated II
3. Koko Eating Bananas → Split Array Largest Sum → Aggressive Cows (BS on answer)
4. Median of Two Sorted Arrays

### Linked List
1. Reverse Linked List → Reverse in K-Group
2. Middle / Cycle detection → Cycle entry
3. Merge Two Sorted Lists → Merge K Sorted Lists (heap)
4. Copy List with Random Pointer → LRU Cache (design)

### Stack & Queue
1. Valid Parentheses → Min Stack → Implement Queue using Stacks
2. Next Greater Element I/II → Daily Temperatures (monotonic stack)
3. Largest Rectangle in Histogram → Trapping Rain Water (stack variant)
4. Sliding Window Maximum (monotonic deque)

### Trees & BST
1. Max Depth, Invert, Same Tree → Symmetric Tree
2. Level order → Right Side View
3. Construct from Preorder+Inorder → Validate BST → Kth Smallest in BST
4. LCA (BST and general) → Max Path Sum (tree DP)
5. Serialize and Deserialize

### Graphs
1. Number of Islands → Flood Fill → Rotting Oranges (BFS)
2. Course Schedule I/II (topo) → Alien Dictionary (topo)
3. Clone Graph → Shortest path (BFS) → Dijkstra
4. Word Ladder → Cheapest Flights Within K Stops
5. Critical Connections (Tarjan bridges) — advanced

### Dynamic Programming
1. Climbing Stairs, House Robber, Max Subarray (Kadane)
2. Coin Change (unbounded) → 0/1 Knapsack → Partition Equal Subset
3. LIS → LCS → Edit Distance
4. Unique Paths → Min Path Sum
5. Longest Palindromic Substring → Burst Balloons (interval DP)
6. House Robber III (tree DP) → Max Path Sum
7. TSP (bitmask) — optional for SDE-3

### Greedy
1. Jump Game I/II → Gas Station
2. Merge Intervals → Non-overlapping → Min Arrows to Burst Balloons
3. Task Scheduler → Partition Labels
4. Candy (two passes)

### Backtracking
1. Subsets → Permutations → Combinations
2. Combination Sum I/II/III
3. Word Search → Word Search II (Trie + backtrack)
4. N-Queens → Sudoku Solver
5. Remove Invalid Parentheses

### Hashing
1. Two Sum, Group Anagrams, Longest Consecutive Sequence
2. Subarray Sum Equals K → LRU Cache
3. Minimum Window Substring

### Heap
1. Kth Largest in Stream → Top K Frequent → K Closest Points
2. Merge K Sorted Lists → Find Median from Data Stream (two heaps)
3. Task Scheduler → IPO

### Tries & Advanced
1. Implement Trie → Word Search II
2. Maximum XOR of Two Numbers (binary trie)
3. Segment Tree / Fenwick (range sum) — if company asks

### Union Find
1. Number of Connected Components → Redundant Connection
2. Accounts Merge → Kruskal’s MST

---

## 2. Difficulty Progression

- **Weeks 1–2**: One topic per week (e.g., Arrays + Binary Search). Focus Easy + selected Medium. Read concept and pattern sections in this repo before solving.
- **Weeks 3–4**: Two topics per week; mix Easy and Medium; add 1–2 Hard per topic.
- **Weeks 5–6**: Cross-topic (DP + Graph, Trie + Backtrack). Emphasize Medium and Hard. Time yourself (30–40 min per problem).
- **Weeks 7–8**: Mock-heavy. Do 2–3 mocks per week; revisit weak topics from audit (see DSA_REPO_AUDIT.md).

---

## 3. Weekly Practice Plan (8-Week SDE-3 Focus)

| Week | Topics | Focus | Problems (approx) |
|------|--------|--------|--------------------|
| 1 | Arrays, Two Pointers, Prefix Sum, Sliding Window | Concept + patterns | 8 Easy, 6 Medium |
| 2 | Binary Search (index + on answer), Linked List, Stack, Queue | Monotonic stack/deque | 6 Easy, 8 Medium |
| 3 | Trees, BST, Tree DP | LCA, serialize, max path sum | 6 Easy, 8 Medium, 2 Hard |
| 4 | Graphs (BFS, DFS, Topo, Dijkstra), Union Find | Multi-source BFS, topo, MST | 4 Easy, 10 Medium, 2 Hard |
| 5 | DP (1D, 2D, Knapsack, LIS, LCS, Interval) | Recurrence + space opt | 4 Easy, 10 Medium, 2 Hard |
| 6 | Greedy, Backtracking, Hashing, Heap | Proof intuition, pruning | 4 Easy, 10 Medium, 2 Hard |
| 7 | Tries, Bit Manipulation, Advanced (Tarjan, Segment Tree) | Word Search II, XOR trie, bridges | 2 Easy, 6 Medium, 4 Hard |
| 8 | Mocks + weak areas, System design algorithms | Rate limit, consistent hashing, full mocks | 4–6 mocks, 2–3 problems/day review |

---

## 4. Mock Interview Preparation Strategy

### Before Each Mock
- **Day before**: Review Quick Revision sections for 2–3 topics you’ll focus on; re-solve one Medium from each.
- **1 hour before**: Skim Pattern Recognition and Interview Strategy for Arrays, DP, Graphs (most common).
- **During**: Read problem → clarify → brute force → optimize → code → test edge cases. State time/space complexity.

### Mock Structure (45–60 min)
- **Problem 1 (20–25 min)**: Often array/string/DP or tree. Aim for optimal solution + code.
- **Problem 2 (20–25 min)**: Graph, design (LRU/cache), or second array/DP. If time, discuss follow-ups (e.g., scale, concurrency).
- **Last 5–10 min**: Ask interviewer questions; note feedback.

### After Each Mock
- Note problems you couldn’t identify (pattern) or couldn’t optimize (revisit that topic’s “Interview Strategy” and “Pattern Recognition”).
- Re-solve the mock problems within 24 hours without help; then compare with solutions in this repo or official editorials.
- Update a personal “weak list” and dedicate 1–2 days before next mock to those topics.

### SDE-3 Specific
- **Explain trade-offs**: e.g., “We could use a hash map for O(N) or sort for O(N log N) with O(1) space.”
- **Edge cases**: Empty, single element, duplicates, overflow, negative numbers.
- **Scale/concurrency**: If asked, tie to “SDE-3 Level Thinking” in each topic (e.g., rate limiting, consistent hashing in system-design-algorithms.md).

---

## 5. How to Use This Repository With the Roadmap

1. **Start with DSA_REPO_AUDIT.md** — know which topics are strong vs weak.
2. **For each topic**: Read Concept Overview → Core Algorithms → Pattern Recognition → Interview Strategy → Quick Revision. Then do the recommended problems in order (above).
3. **When stuck**: Check “Common Interview Problems” and “Code Implementations” in the topic file; then “Advanced Variations” and “Common mistakes” in Interview Strategy.
4. **Before mocks**: Use Quick Revision + Interview Strategy across 4–5 topics; re-solve 2–3 Medium/Hard from the curated list in [sde-3-guide](sde-3-guide/sde-3-guide.md) (Top 20 problems).
5. **System design + coding**: Combine [concurrency](concurrency/concurrency-patterns.md) and [advanced-dsa/system-design-algorithms.md](advanced-dsa/system-design-algorithms.md) when practicing “design + implement” rounds.

---

## 6. Checklist Before Interview

- [ ] All “Quick Revision” sections reviewed for Arrays, DP, Graphs, Trees, Binary Search.
- [ ] At least 1 problem from each Hard list done (or 2 per topic you’re weak in).
- [ ] Top 20 SDE-3 problems from sde-3-guide attempted (or 15/20).
- [ ] 4+ full mocks completed with feedback incorporated.
- [ ] Union Find, Trie, and one advanced graph (Tarjan or bridges) practiced if target company asks them.
- [ ] Rate limiting or consistent hashing can be implemented or explained (system-design-algorithms.md).
