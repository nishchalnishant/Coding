---
module: 03-patterns
topic: Topic Questions Logic And Tricks
tags: [patterns, topic-questions-logic-and-tricks]
---
# Topic Questions — Logic, Patterns, and Trickiness

> [!note] L3 Reference Document
> This file is a **reference / meta document** — read it once, then use it as a lookup.
> It is NOT a coding practice file. Do not deep-study it like a topic file.

This guide lists **canonical interview questions** by topic, **why** they appear, the **core solution logic**, and **what makes them tricky** (gotchas, wrong turns, follow-ups). Use with the full topic files in [data-structures/](../01-data-structures/README.md) and [algorithms/](../02-algorithms/README.md).

**Per-file detail:** Each file in `01-data-structures/` and `02-algorithms/` has an **Interview Questions — Logic & Trickiness** section with a table: **Question** | **Core logic** | **Trickiness & details** (follow-ups, edge cases, wrong answers, complexity notes). This document stays a **cross-topic index** with shorter rows; open the specific topic file for the **full** expanded table and the rest of the notes (concept, code, strategy, revision).

**How to read each section:** the first table gives the full logic + trickiness breakdown for the highest-yield problems. The **More canonical problems** table that follows gives one-line key insights for the rest — if you can state the key insight cold, you know the problem.

---

## Arrays, two pointers, sliding window, prefix sum

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Two Sum** | Hash map vs sort + two pointers | Complement map `target - x` or sort then converge `left/right` | Unsorted → hash O(n); sorted → two pointers O(n). Duplicates: don’t reuse same index. Return indices vs pairs. |
| **3Sum** | Avoid O(n³), dedupe | Sort; fix `i`, two-sum on `i+1..n-1` with `left/right`; skip equal `nums[i]` and equal `nums[left]` after move | **Skip duplicates** at all three levels or you output duplicates. Don’t forget `i < n-2`. |
| **Subarray Sum Equals K** | Prefix sum + frequency | `count[prefix]`; add `count[prefix - K]` each step; `count[0]=1` | **Prefix 0** means subarray from start. **Negative numbers** → prefix sum still works; no sliding window for “exactly K” with negatives. |
| **Longest Substring Without Repeating** | Sliding window + set/map | Expand `j`, shrink `i` while `s[j]` in window | **Window is “valid”** while unique; use `last` index map for O(1) jump of `i`. |
| **Minimum Window Substring** | Hard sliding window | Need counts for `t`; `window` valid when all chars satisfied; shrink while valid | **“Valid”** check is expensive if naive — track `formed` vs `required`. **Order** of chars irrelevant — frequency only. |
| **Trapping Rain Water** | Two pointers or stack | Water at `i` = min(left_max, right_max) - height[i]; move smaller side | **Why move smaller side?** — smaller side caps water; **stack** variant for “next greater” mindset. |
| **Merge Intervals** | Sort + sweep | Sort by start; merge if `curr.start <= prev.end` | **Unsorted input** — must sort first. **Touching** intervals `[1,4][4,5]` — clarify if merge (usually yes). |
| **Product of Array Except Self** | Prefix/suffix without division | Left products `i`, right products `i`, multiply | **Zeros** — one zero → all zero except that index; two zeros → all zero. **No division** constraint. |
| **Median of Two Sorted Arrays** | Binary search on partition | Partition smaller array so left sizes balance and `max(left) <= min(right)` | **Indices** vs lengths; **even/odd** total length; **empty** one array. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Best Time to Buy/Sell Stock | Easy | Kadane variant | Track running min; profit = price - min_so_far |
| Maximum Subarray | Easy | Kadane's | Reset to 0 when prefix goes negative |
| Maximum Product Subarray | Medium | DP | Track both max and min (negatives flip sign) |
| Container With Most Water | Medium | Two Pointers | Move the shorter side — taller side can never improve by moving |
| Subarray Sums Divisible by K | Medium | Prefix Sum Modulo | Frequency map of prefix sum mod K; normalize negative remainder with `(prefix_sum % k + k) % k` |
| Subarrays with K Different Integers | Hard | Sliding Window | Exactly K distinct = At Most K - At Most K-1; subtraction makes non-monotonic window linear |
| Range Sum Query 2D - Immutable | Medium | 2D Prefix Sum | Precompute 2D prefix array; answer queries in O(1) via standard 2D inclusion-exclusion subtraction |

---

## Hashing & frequency

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Group Anagrams** | Canonical key for string | Key = sorted string OR tuple of 26 counts | **Unicode** — not 26 buckets if arbitrary chars; use **Counter** or sort. |
| **Longest Consecutive Sequence** | O(n) expected, not sort | Put all in set; for each `x`, only start sequence if `x-1` not in set | **O(n)** only if you don’t sort; **inner while** looks O(n²) but each number visited once across all sequences. |
| **LRU Cache** | HashMap + DLL | `get`: move to head; `put`: insert at head, evict tail if over capacity | **Doubly linked** for O(1) remove; **dummy head/tail** simplifies edges. Thread-safety follow-up at senior level. |
| **Top K Frequent Elements** | Bucket vs heap | Count freq → min-heap of size K **or** bucket by frequency | **Heap** is O(n log k); **bucket sort** can be O(n) if frequencies bounded. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Valid Anagram | Easy | Frequency Map | Counter(s) == Counter(t) |

---

## Linked lists

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Reverse Linked List** | Pointer rewiring | `prev, curr, next`; iterative or recursive | **Recursive** uses O(n) stack; **null** head. |
| **Merge Two Sorted Lists** | Dummy node | Dummy → compare `l1`/`l2`, append smaller | **In-place** vs new list; **dummy** avoids null head cases. |
| **Linked List Cycle II** | Floyd + math | Fast/slow meet; reset one to head; **same speed** to entry | **Why entry?** — length algebra; **wrong**: restarting only fast from meet. |
| **Merge k Sorted Lists** | Heap | Min-heap of (val, list_id, node); pop min, push next | **O(N log k)** vs **compare all k** each step O(kN). **Tie-break** on list id for stability. |
| **Copy List with Random Pointer** | Old→new map | Two passes: create clones, wire `next`/`random` using map | **O(n)** space; **O(1)** space trick exists (interleave nodes) — bonus for senior. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Linked List Cycle | Easy | Fast/Slow Pointers | Cycle if fast == slow |
| Reorder List | Medium | Fast/Slow + Reverse | Find mid, reverse second half, interleave |
| Remove Nth from End | Medium | Two Pointers | Advance fast n steps; then move both |

---

## Stack & queue

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Valid Parentheses** | Stack matching | Push opens; on close, pop and match | **Order** matters; **only one type** of bracket in simpler variants. |
| **Daily Temperatures** | Monotonic stack | Decreasing stack of indices; **warmer** pop and assign | **Indices** on stack, not values; **end** of array — sentinel or second pass. |
| **Largest Rectangle in Histogram** | Monotonic stack | Bars as heights; pop when lower; width = `i - new_top - 1` | **Sentinel 0** at end to flush stack; **width** formula when stack empty. |
| **Sliding Window Maximum** | Monotonic deque | Deque of indices, decreasing values; pop back while `nums[back] < nums[i]` | **Front** out of window — remove while `<= i-k`; **indices** not values for width. |
| **Decode String** | Nested structure | Stack of (current_string, repeat_count) or recursive | **Nested** `a2[b3[c]]` — stack per `[`; **digit** can be multi-digit `100[`. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Min Stack | Easy | Two Stacks | Track running min alongside main stack |
| Next Greater Element | Medium | Monotonic Stack | Same pattern as Daily Temperatures; map result by value |
| Car Fleet | Medium | Monotonic Stack | Sort by position; car merges fleet if it arrives before or same time |

---

## Trees & BST

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Lowest Common Ancestor (BST)** | BST property | `p,q < root` → left; both > → right; else root | **LCA can be p or q**; **values** not nodes if duplicates policy unclear. |
| **LCA (binary tree)** | Recursion | If left and right return non-null → root; else return non-null child | **Assumption** `p,q` exist in tree; **not BST** — can’t use value compare. |
| **Serialize / Deserialize Binary Tree** | Design + traversal | Preorder with null markers + queue rebuild; or level-order | **One string** representation; **delimiter** for multi-digit values; **empty** tree. |
| **Binary Tree Maximum Path Sum** | Tree DP | Postorder: return max chain up; `global = max(global, left+right+val)` | **Path** may not pass root; **negative** nodes — use `max(0, child)`. |
| **Validate BST** | Inorder or bounds | Inorder must be strictly increasing **or** `node` in `(min,max)` | **BST** = left < root < right for **all** descendants — not just immediate children. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Invert Binary Tree | Easy | DFS | Swap left/right at each node recursively |
| Maximum Depth | Easy | DFS | 1 + max(left_depth, right_depth) |
| Same Tree | Easy | DFS | Recurse both trees simultaneously |
| Subtree of Another Tree | Easy | DFS | At each node, check if trees match |
| Kth Smallest in BST | Medium | In-order DFS | In-order gives sorted; count down to k |
| Path Sum II | Medium | DFS backtrack | Add to path, recurse, remove from path |
| Path Sum III | Medium | DFS + Prefix Sum | Track running prefix sum frequency in map during DFS; lookup `current_sum - target` to count paths; decrement counts on backtrack |
| Level Order Traversal | Medium | BFS | Deque; record len at start of each level |
| Right Side View | Medium | BFS | Last node at each BFS level |
| Count Good Nodes | Medium | DFS | Pass max_so_far down; count if node >= max |
| Construct from Pre+Inorder | Medium | DFS + Index Map | Preorder[0] = root; find in inorder to split |
| Step-By-Step Directions | Medium | LCA + Path Generation | Find path from root to start and root to dest; LCA is the last common node; start-to-LCA becomes all 'U's, LCA-to-dest is appended |

---

## Heap & priority queue

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Merge K Sorted Lists** | K-way merge | Min-heap of size K (first node of each list) | Same as linked list section; **empty** lists in heap. |
| **Find Median from Data Stream** | Two heaps | `max` heap (lower half), `min` heap (upper half); balance sizes | **Rebalance** after each insert; **even** median = average of two tops. |
| **Task Scheduler** | Math + greedy | `(max_count-1)*(n+1) + num_max_tasks` | **Idle slots** formula; **cap** at `len(tasks)` if enough tasks fill gaps. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Kth Largest Element | Medium | Min-Heap size K | Push all; pop until size K; heap[0] is answer |

---

## Binary search

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Search in Rotated Sorted Array** | Find sorted half | Compare `mid` with `left`/`right` to decide which half is sorted, then target in range? | **Duplicates** in `nums[left]==nums[mid]==nums[right]` — **worst case O(n)**. |
| **Koko Eating Bananas** | BS on answer | `min=1`, `max=max(piles)`; `valid(k)` = hours ≤ h; minimize k | **Ceiling** division per pile: `(p + k - 1) // k`. |
| **Split Array Largest Sum** | Minimize largest sum | BS on answer: `valid(mid)` = can split into ≤ m subarrays with sum ≤ mid | **Greedy** check for feasibility—**count splits** when sum exceeds mid. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Binary Search | Easy | Standard | lo=0, hi=n-1; mid=(lo+hi)//2 |
| Search a 2D Matrix | Medium | BS on 1D index | Treat as 1D: row=mid//cols, col=mid%cols |
| Find Minimum in Rotated Array | Medium | Binary Search | Left-biased: if arr[mid] > arr[hi], pivot in right half |
| Time-Based Key-Value Store | Medium | BS on timestamps | bisect_right on sorted timestamps per key |

---

## Graphs

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Number of Islands** | DFS/BFS on grid | Mark visited; flood 4-dir from each `1` | **Mutate** grid vs `visited` set; **8-dir** if problem says so. |
| **Course Schedule** | Cycle in directed graph | Topo sort: Kahn or DFS 3-color | **Edge direction** `a,b` means `b` before `a` — **build graph** correctly. |
| **Alien Dictionary** | Topo + ordering | Compare adjacent words, first diff → edge; topo all letters | **Invalid** if cycle; **prefix** order — `"ab"` before `"abc"` gives no edge between words; **all letters** as nodes. |
| **Word Ladder** | BFS on implicit graph | BFS from `beginWord`; neighbors = one-letter diff in wordList | **WordList** as set for O(1) lookup; **length** of path = BFS level; **bidirectional** BFS follow-up. |
| **Cheapest Flights Within K Stops** | Bellman-Ford / relax k times | `dist[v]` relax all edges `k+1` rounds or **min-heap** state `(cost, node, stops)` | **K stops** = at most `K+1` edges; **negative** edges not allowed in Dijkstra variant. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Clone Graph | Medium | BFS + HashMap | Map original→clone; BFS to copy edges |
| Pacific Atlantic Water Flow | Medium | Reverse BFS | BFS from both coasts; answer = intersection |
| Course Schedule II | Medium | Topo Sort (Kahn's) | Return topo order; empty if cycle exists |
| Number of Connected Components | Medium | Union-Find / DFS | Count distinct roots |
| Graph Valid Tree | Medium | Union-Find | n nodes, n-1 edges, no cycle = valid tree |
| Network Delay Time | Medium | Dijkstra | Single-source shortest path; return max dist |
| Swim in Rising Water | Hard | Binary Search + BFS / Dijkstra | Min time = min max-height path from (0,0) to (n-1,n-1) |
| Is Graph Bipartite? | Medium | 2-Coloring DFS/BFS | Alternate coloring nodes 0 and 1; a same-color conflict between neighbors means not bipartite |
| Redundant Connection | Medium | Union-Find | The edge that connects two vertices already in the same Union-Find set is redundant |

---

## Disjoint Set Union (DSU)

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Redundant Connection II | Hard | Directed DSU + Cycle | Track two parent pointers to find node with two parents; check cycle; remove correct edge to restore tree |
| Accounts Merge | Medium | DSU Connected Components | Treat emails as nodes, map to parent email; run DSU; group emails by absolute component root |
| Number of Good Paths | Hard | DSU + Sorted Nodes | Sort nodes by value; union components starting from smallest; size of equal values within component determines paths |

---

## Dynamic programming

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Coin Change** | Unbounded knapsack | `dp[w] = min(dp[w], 1+dp[w-coin])` | **order** of coins doesn’t matter; **0** amount = 0 coins; **impossible** = inf. |
| **Longest Increasing Subsequence** | LIS O(n log n) | `tails` array; binary search position to replace | **Strictly** increasing vs **non-decreasing** changes binary search. |
| **Longest Common Subsequence** | 2D DP | Match → `1+dp[i-1][j-1]`; else `max(dp[i-1][j], dp[i][j-1])` | **Space** O(min(m,n)) possible; **empty** string base. |
| **Edit Distance** | 2D DP | Insert/delete/replace costs | **Indels** symmetric; **follow-up** one-row space. |
| **Word Break** | Partition + memo | `dp[i]` = can segment `s[i:]`; try each word prefix | **Word length** bound can optimize; **Trie** for multiple lookups. |
| **Burst Balloons** | Interval DP | `dp[i][j]` = max coins in open interval `(i,j)`; try last balloon `k` | **Multiply** `nums[i]*nums[k]*nums[j]` — **add** boundary 1s as sentinels. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Climbing Stairs | Easy | 1D DP | dp[i] = dp[i-1] + dp[i-2]; Fibonacci |
| House Robber | Medium | 1D DP | dp[i] = max(dp[i-1], dp[i-2] + nums[i]) |
| House Robber II (circular) | Medium | 1D DP | Run twice: [0..n-2] and [1..n-1]; take max |
| Longest Palindromic Subsequence | Medium | 2D DP (interval) | dp[i][j] = 2+dp[i+1][j-1] if match else max(dp[i+1][j], dp[i][j-1]) |
| Coin Change II (ways) | Medium | Unbounded Knapsack | dp[i] += dp[i-coin]; order: coin outer, amount inner |
| 0-1 Knapsack | Medium | 2D DP | dp[i][w] = max(skip, take if weight fits) |
| Partition Equal Subset Sum | Medium | 0-1 Knapsack | Can we reach sum/2? Subset sum DP |
| Unique Paths | Medium | Grid DP | dp[i][j] = dp[i-1][j] + dp[i][j-1] |
| Regular Expression Matching | Hard | 2D DP | Handle '*': match 0 times (dp[i][j-2]) or 1+ times (dp[i-1][j]) |

---

## Greedy

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Jump Game II** | Min jumps | Greedy: extend `furthest` in current jump range; increment jumps when `i` reaches `end` | **O(n)** single pass; **Jump Game I** is only reachability (different). |
| **Non-overlapping Intervals** | Min removals | Sort by end; **count** overlap when `start < last_end` | **Sort by end** not start — **counterexample** if start sort. |
| **Gas Station** | Circular greedy | If total gas ≥ total cost, unique start exists; track `tank`, reset start when `tank < 0` | **Proof** — if sum ≥ 0 solution exists; **O(n)** single pass. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Jump Game | Medium | Greedy | Track max reachable index; fail if current > max_reach |
| Candy | Hard | Two-pass Greedy | Left-to-right pass satisfying left neighbors, right-to-left pass satisfying right neighbors; merge via max |

---

## Backtracking

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Permutations** | All orderings | DFS + `used` or swap | **Duplicates** in `nums` — sort + skip same at same level. |
| **Combination Sum** | Sum with reuse | `start` index to avoid duplicate combinations | **Reuse** same element — next recursion starts at `i` not `i+1`. |
| **Subsets II** | Subsets with dupes | Sort; skip `nums[i]` if `i>start` and `nums[i]==nums[i-1]` | **Same level** skip vs **different** branch. |
| **Word Search** | Grid DFS | DFS + mark visited; backtrack | **Reuse** cell — **unmark** after return; **prune** with Trie in Word Search II. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Subsets | Medium | Choose/Skip | For each element: include or exclude |
| Permutations II (duplicates) | Medium | Sorted + Skip | Skip if used[i] or (same as prev and prev not used) |
| Combination Sum II | Medium | Sorted + Skip | Cannot reuse; skip duplicates at same depth |
| N-Queens | Hard | Row-by-row | Track col, diag1, diag2 as sets |
| Palindrome Partitioning | Medium | Backtrack + precompute | Precompute is_palindrome[i][j]; then backtrack |

---

## Trie

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Implement Trie | Medium | Prefix Tree | Dictionary-based children map plus end-of-word boolean marker |
| Word Search II | Hard | Trie + Backtracking DFS | Build Trie of search words; DFS on grid pruning paths immediately when prefix is absent in Trie |
| Design Add and Search Words | Medium | Trie + DFS Wildcard | Use recursion on Trie children for wildcard '.' characters; standard lookup for normal characters |
| Prefix and Suffix Search | Hard | Trie of wrapped words | Insert wrapped words `suffix + '#' + word` into Trie; search prefix is resolved as `suffix + '#' + prefix` |

---

## Bit manipulation

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Single Number** | XOR | XOR all — pairs cancel | **General** to **Single Number II** (mod 3) — bit counts. |
| **Maximum XOR of Two Numbers** | Binary trie | Insert bits; for each number try opposite bit path | **Trie** depth 31 or 32 for signed ints; **leading** zeros. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Single Number II | Medium | Bit counting modulo 3 | Count set bits at each of 32 positions modulo 3; or use state machine masks `ones` and `twos` |
| Counting Bits | Easy | Bit DP | `dp[i] = dp[i >> 1] + (i & 1)`; the bit count of `i` is the count of its right shift plus its last bit |
| Sum of Two Integers | Medium | Bit addition | Simulate half-adder: `a ^ b` computes sum without carry, `(a & b) << 1` computes carry; repeat until carry is zero |

---

## Math & number theory

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Happy Number | Easy | Floyd's Cycle Detection | Sequence of digit-square sums eventually loops; use fast/slow pointers on values instead of linked list |
| Pow(x, n) | Medium | Binary Exponentiation | `O(log N)` reduction: `pow(x, n) = pow(x*x, n//2)` for even, `x * pow(x, n-1)` for odd. Handle negative bounds |
| Sieve of Eratosthenes | Easy | Prime Sieving | Incrementally mark multiples of discovered primes as composite up to `sqrt(N)`; count unmarked |

---

## Strings (beyond array)

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Implement strStr / KMP** | LPS, no backtrack on text | Build `lps` from pattern; match with `lps` fallback | **Off-by-one** in `lps` build; **empty** pattern. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Valid Palindrome | Easy | Two Pointers | Skip non-alphanumeric; compare lowercased |
| Longest Repeating Character Replacement | Medium | Sliding Window | Window valid if len - max_freq ≤ k |
| Find All Anagrams | Medium | Sliding Window (fixed) | Fixed window; compare freq maps |
| Longest Palindromic Substring | Medium | Expand Around Center | Try both odd and even expansions at each index |
| Palindromic Substrings (count) | Medium | Expand Around Center | Count each successful expansion |
| Encode and Decode Strings | Medium | Delimiter | Length-prefix format: "4#word" handles all delimiters |

---

## Design / system-style (often L5+)

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **LRU Cache** | HashMap + DLL | O(1) get/put | **Eviction** order; **capacity** 1 edge case. |
| **LFU Cache** | freq + LRU within freq | **min_freq** tracking; **lists** per frequency | **Tie** LRU — **second** priority; **O(1)** requires careful structure. |
| **Rate Limiter** | Token bucket / sliding window | Refill + consume tokens | **Thread** safety; **distributed** follow-up. |

---

## Segment Tree & Fenwick Tree `💤 T3` — out of L3 scope

> Skip for L3 — see [What to Skip](../00-L3-EXECUTION-META/L3_CHEATSHEET.md). Kept here only for reference.

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Range Sum Query - Mutable | Medium | Segment Tree / Fenwick | Segment Tree for O(log N) point update and range query, or Fenwick Tree for space-optimized prefix sums |
| Range Sum Query 2D - Mutable | Hard | 2D Fenwick / QuadTree | Generalize Fenwick Tree to 2D; point update and prefix range queries are O(log R * log C) |
| Count of Smaller Numbers After Self | Hard | Fenwick / Merge Sort | Traverse array right-to-left; query smaller count, then update Fenwick with current number's frequency |

---

## How to use this in interviews

1. **Name the pattern** in 30 seconds: “This is subarray sum equals K — prefix sum with a map of prefix counts.”
2. **State the trick** before coding: “I need to skip duplicates in 3-sum at `i`, `left`, and `right`.”
3. **Fail** the obvious trap out loud: “Naive would be O(n²) checking all subarrays; I’ll use a map instead.”

---

## See also

- [patterns-master.md](patterns-master.md) — full pattern catalog, decision trees, gotchas  
- [GOOGLE_INTERVIEW_REVISION.md](GOOGLE_INTERVIEW_REVISION.md) — quick sheet + revision schedule  
- [HOW_TO_THINK.md](HOW_TO_THINK.md) — derive the pattern instead of recalling it  
