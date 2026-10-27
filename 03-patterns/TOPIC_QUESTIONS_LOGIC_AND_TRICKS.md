---
module: 03-patterns
topic: Topic Questions Logic And Tricks
tags: [patterns, topic-questions-logic-and-tricks]
---
# Topic Questions — Logic, Patterns, and Trickiness

## What this covers

> [!abstract] In this file
> **Covers:** Canonical questions for every topic, why they're asked, the core logic, the trap in each — plus a variants table showing how each classic problem mutates.
> **You'll be able to:** Recall the key insight and gotcha for any canonical problem in seconds, and recognise a 'new' problem as a variant of one you know.
> **Prereqs:** Lecture files · **Pair with:** [Questions index](../04-practice/README.md) · **Time:** 2 h (lookup afterwards)
> **How to use:** reference — read once, then use as a lookup.
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Arrays, two pointers, sliding window, prefix sum](#arrays-two-pointers-sliding-window-prefix-sum) · [Hashing & frequency](#hashing--frequency) · [Linked lists](#linked-lists) · [Stack & queue](#stack--queue) · [Trees & BST](#trees--bst) · [Heap & priority queue](#heap--priority-queue) · [Binary search](#binary-search) · [Graphs](#graphs) · [Disjoint Set Union (DSU)](#disjoint-set-union-dsu) · [Dynamic programming](#dynamic-programming) · [Greedy](#greedy) · [Backtracking](#backtracking) · [Trie](#trie) · [Bit manipulation](#bit-manipulation) · [Math & number theory](#math--number-theory) · [Strings (beyond array)](#strings-beyond-array) · [Variants Playbook](#variants-playbook) · [See also](#see-also)

---

Cross-topic index: each section's first table gives logic + trap for the highest-yield problems; **More canonical problems** gives one-line key insights for the rest. If you can state the key insight cold, you know the problem. Full expanded tables live in each [data-structures](../01-data-structures/README.md) / [algorithms](../02-algorithms/README.md) file under **Interview Questions — Logic & Trickiness**.

**In the interview:**
1. **Name the pattern** in 30 s: "Subarray sum equals K — prefix sum with a map of prefix counts."
2. **State the trick** before coding: "Skip duplicates in 3Sum at `i`, `left`, and `right`."
3. **Name the trap** out loud: "Naive is O(n²) over all subarrays; a map makes it O(n)."

Range queries with updates (segment tree / Fenwick) are out of scope — name them, don't code them. Count of Smaller Numbers After Self is solvable with merge-sort counting.

---

## Arrays, two pointers, sliding window, prefix sum

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Two Sum** `⚡ T1` | Hash map vs sort + two pointers | Complement map `target - x` or sort then converge `left/right` | Unsorted → hash O(n); sorted → two pointers O(n). Duplicates: don’t reuse same index. Return indices vs pairs. |
| **3Sum** `⚡ T1` | Avoid O(n³), dedupe | Sort; fix `i`, two-sum on `i+1..n-1` with `left/right`; skip equal `nums[i]` and equal `nums[left]` after move | **Skip duplicates** at all three levels or you output duplicates. Don’t forget `i < n-2`. |
| **Subarray Sum Equals K** `⚡ T1` | Prefix sum + frequency | `count[prefix]`; add `count[prefix - K]` each step; `count[0]=1` | **Prefix 0** means subarray from start. **Negative numbers** → prefix sum still works; no sliding window for “exactly K” with negatives. |
| **Longest Substring Without Repeating** `⚡ T1` | Sliding window + set/map | Expand `j`, shrink `i` while `s[j]` in window | **Window is “valid”** while unique; use `last` index map for O(1) jump of `i`. |
| **Minimum Window Substring** `⚡ T1` | Hard sliding window | Need counts for `t`; `window` valid when all chars satisfied; shrink while valid | **“Valid”** check is expensive if naive — track `formed` vs `required`. **Order** of chars irrelevant — frequency only. |
| **Trapping Rain Water** `⚡ T1` | Two pointers or stack | Water at `i` = min(left_max, right_max) - height[i]; move smaller side | **Why move smaller side?** — smaller side caps water; **stack** variant for “next greater” mindset. |
| **Merge Intervals** `🎯 T2` | Sort + sweep | Sort by start; merge if `curr.start <= prev.end` | **Unsorted input** — must sort first. **Touching** intervals `[1,4][4,5]` — clarify if merge (usually yes). |
| **Product of Array Except Self** `🎯 T2` | Prefix/suffix without division | Left products `i`, right products `i`, multiply | **Zeros** — one zero → all zero except that index; two zeros → all zero. **No division** constraint. |
| **Median of Two Sorted Arrays** `⚡ T1` | Binary search on partition | Partition smaller array so left sizes balance and `max(left) <= min(right)` | **Indices** vs lengths; **even/odd** total length; **empty** one array. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Best Time to Buy/Sell Stock `⚡ T1` | Easy | Kadane variant | Track running min; profit = price - min_so_far |
| Maximum Subarray `🎯 T2` | Medium | Kadane's | Running sum resets to 0 when it goes negative (or `cur = max(x, cur + x)`) |
| Maximum Product Subarray `🎯 T2` | Medium | DP | Track both max and min (negatives flip sign) |
| Container With Most Water `⚡ T1` | Medium | Two Pointers | Move the shorter side — taller side can never improve by moving |
| Subarray Sums Divisible by K `⚡ T1` | Medium | Prefix Sum Modulo | Frequency map of prefix sum mod K; normalize negative remainder with `(prefix_sum % k + k) % k` |
| Subarrays with K Different Integers `⚡ T1` | Hard | Sliding Window | Exactly K distinct = At Most K - At Most K-1; subtraction makes non-monotonic window linear |
| Range Sum Query 2D - Immutable `🎯 T2` | Medium | 2D Prefix Sum | Precompute 2D prefix array; answer queries in O(1) via standard 2D inclusion-exclusion subtraction |

---

## Hashing & frequency

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Group Anagrams** `⚡ T1` | Canonical key for string | Key = sorted string OR tuple of 26 counts | **Unicode** — not 26 buckets if arbitrary chars; use **Counter** or sort. |
| **Longest Consecutive Sequence** `⚡ T1` | O(n) expected, not sort | Put all in set; for each `x`, only start sequence if `x-1` not in set | **O(n)** only if you don’t sort; **inner while** looks O(n²) but each number visited once across all sequences. |
| **LRU Cache** `🎯 T2` | HashMap + DLL | `get`: move to head; `put`: insert at head, evict tail if over capacity | **Doubly linked** for O(1) remove; **dummy head/tail** simplifies edges. Thread-safety follow-up at senior level. |
| **Top K Frequent Elements** `⚡ T1` | Bucket vs heap | Count freq → min-heap of size K **or** bucket by frequency | **Heap** is O(n log k); **bucket sort** can be O(n) if frequencies bounded. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Valid Anagram `🎯 T2` | Easy | Frequency Map | Counter(s) == Counter(t) |

---

## Linked lists

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Reverse Linked List** `🎯 T2` | Pointer rewiring | `prev, curr, next`; iterative or recursive | **Recursive** uses O(n) stack; **null** head. |
| **Merge Two Sorted Lists** `🎯 T2` | Dummy node | Dummy → compare `l1`/`l2`, append smaller | **In-place** vs new list; **dummy** avoids null head cases. |
| **Linked List Cycle II** `🎯 T2` | Floyd + math | Fast/slow meet; reset one to head; **same speed** to entry | **Why entry?** — length algebra; **wrong**: restarting only fast from meet. |
| **Merge k Sorted Lists** `⚡ T1` | Heap | Min-heap of (val, list_id, node); pop min, push next | **O(N log k)** vs **compare all k** each step O(kN). **Tie-break** on list id for stability. |
| **Copy List with Random Pointer** `🎯 T2` | Old→new map | Two passes: create clones, wire `next`/`random` using map | **O(n)** space; **O(1)** space trick exists (interleave nodes) — bonus for senior. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Linked List Cycle `🎯 T2` | Easy | Fast/Slow Pointers | Cycle if fast == slow |
| Reorder List `🎯 T2` | Medium | Fast/Slow + Reverse | Find mid, reverse second half, interleave |
| Remove Nth from End `⚡ T1` | Medium | Two Pointers | Advance fast n steps; then move both |

---

## Stack & queue

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Valid Parentheses** `🎯 T2` | Stack matching | Push opens; on close, pop and match | **Order** matters; **only one type** of bracket in simpler variants. |
| **Daily Temperatures** `🎯 T2` | Monotonic stack | Decreasing stack of indices; **warmer** pop and assign | **Indices** on stack, not values; **end** of array — sentinel or second pass. |
| **Largest Rectangle in Histogram** `🎯 T2` | Monotonic stack | Bars as heights; pop when lower; width = `i - new_top - 1` | **Sentinel 0** at end to flush stack; **width** formula when stack empty. |
| **Sliding Window Maximum** `⚡ T1` | Monotonic deque | Deque of indices, decreasing values; pop back while `nums[back] < nums[i]` | **Front** out of window — remove while `<= i-k`; **indices** not values for width. |
| **Decode String** `🎯 T2` | Nested structure | Stack of (current_string, repeat_count) or recursive | **Nested** `a2[b3[c]]` — stack per `[`; **digit** can be multi-digit `100[`. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Min Stack `🎯 T2` | Easy | Two Stacks | Track running min alongside main stack |
| Next Greater Element `⚡ T1` | Medium | Monotonic Stack | Same pattern as Daily Temperatures; map result by value |
| Car Fleet `🎯 T2` | Medium | Monotonic Stack | Sort by position; car merges fleet if it arrives before or same time |

---

## Trees & BST

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Lowest Common Ancestor (BST)** `⚡ T1` | BST property | `p,q < root` → left; both > → right; else root | **LCA can be p or q**; **values** not nodes if duplicates policy unclear. |
| **LCA (binary tree)** `⚡ T1` | Recursion | If left and right return non-null → root; else return non-null child | **Assumption** `p,q` exist in tree; **not BST** — can’t use value compare. |
| **Serialize / Deserialize Binary Tree** `🎯 T2` | Design + traversal | Preorder with null markers + queue rebuild; or level-order | **One string** representation; **delimiter** for multi-digit values; **empty** tree. |
| **Binary Tree Maximum Path Sum** `🎯 T2` | Tree DP | Postorder: return max chain up; `global = max(global, left+right+val)` | **Path** may not pass root; **negative** nodes — use `max(0, child)`. |
| **Validate BST** `⚡ T1` | Inorder or bounds | Inorder must be strictly increasing **or** `node` in `(min,max)` | **BST** = left < root < right for **all** descendants — not just immediate children. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Invert Binary Tree `🎯 T2` | Easy | DFS | Swap left/right at each node recursively |
| Maximum Depth `⚡ T1` | Easy | DFS | 1 + max(left_depth, right_depth) |
| Same Tree `⚡ T1` | Easy | DFS | Recurse both trees simultaneously |
| Subtree of Another Tree `⚡ T1` | Easy | DFS | At each node, check if trees match |
| Kth Smallest in BST `⚡ T1` | Medium | In-order DFS | In-order gives sorted; count down to k |
| Path Sum II `🎯 T2` | Medium | DFS backtrack | Add to path, recurse, remove from path |
| Path Sum III `🎯 T2` | Medium | DFS + Prefix Sum | Track running prefix sum frequency in map during DFS; lookup `current_sum - target` to count paths; decrement counts on backtrack |
| Level Order Traversal `⚡ T1` | Medium | BFS | Deque; record len at start of each level |
| Right Side View `⚡ T1` | Medium | BFS | Last node at each BFS level |
| Count Good Nodes `🎯 T2` | Medium | DFS | Pass max_so_far down; count if node >= max |
| Construct from Pre+Inorder `🎯 T2` | Medium | DFS + Index Map | Preorder[0] = root; find in inorder to split |
| Step-By-Step Directions `🎯 T2` | Medium | LCA + Path Generation | Find path from root to start and root to dest; LCA is the last common node; start-to-LCA becomes all 'U's, LCA-to-dest is appended |

---

## Heap & priority queue

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Merge K Sorted Lists** `⚡ T1` | K-way merge | Min-heap of size K (first node of each list) | Same as linked list section; **empty** lists in heap. |
| **Find Median from Data Stream** `⚡ T1` | Two heaps | `max` heap (lower half), `min` heap (upper half); balance sizes | **Rebalance** after each insert; **even** median = average of two tops. |
| **Task Scheduler** `⚡ T1` | Math + greedy | `(max_count-1)*(n+1) + num_max_tasks` | **Idle slots** formula; **cap** at `len(tasks)` if enough tasks fill gaps. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Kth Largest Element `⚡ T1` | Medium | Min-Heap size K | Push all; pop until size K; heap[0] is answer |

---

## Binary search

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Search in Rotated Sorted Array** `⚡ T1` | Find sorted half | Compare `mid` with `left`/`right` to decide which half is sorted, then target in range? | **Duplicates** in `nums[left]==nums[mid]==nums[right]` — **worst case O(n)**. |
| **Koko Eating Bananas** `⚡ T1` | BS on answer | `min=1`, `max=max(piles)`; `valid(k)` = hours ≤ h; minimize k | **Ceiling** division per pile: `(p + k - 1) // k`. |
| **Split Array Largest Sum** `⚡ T1` | Minimize largest sum | BS on answer: `valid(mid)` = can split into ≤ m subarrays with sum ≤ mid | **Greedy** check for feasibility—**count splits** when sum exceeds mid. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Binary Search `⚡ T1` | Easy | Standard | lo=0, hi=n-1; mid=(lo+hi)//2 |
| Search a 2D Matrix `⚡ T1` | Medium | BS on 1D index | Treat as 1D: row=mid//cols, col=mid%cols |
| Find Minimum in Rotated Array `⚡ T1` | Medium | Binary Search | Left-biased: if arr[mid] > arr[hi], pivot in right half |
| Time-Based Key-Value Store `🎯 T2` | Medium | BS on timestamps | bisect_right on sorted timestamps per key |

---

## Graphs

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Number of Islands** `⚡ T1` | DFS/BFS on grid | Mark visited; flood 4-dir from each `1` | **Mutate** grid vs `visited` set; **8-dir** if problem says so. |
| **Course Schedule** `⚡ T1` | Cycle in directed graph | Topo sort: Kahn or DFS 3-color | **Edge direction** `a,b` means `b` before `a` — **build graph** correctly. |
| **Alien Dictionary** `⚡ T1` | Topo + ordering | Compare adjacent words, first diff → edge; topo all letters | **Invalid** if cycle; **prefix** order — `"ab"` before `"abc"` gives no edge between words; **all letters** as nodes. |
| **Word Ladder** `⚡ T1` | BFS on implicit graph | BFS from `beginWord`; neighbors = one-letter diff in wordList | **WordList** as set for O(1) lookup; **length** of path = BFS level; **bidirectional** BFS follow-up. |
| **Cheapest Flights Within K Stops** `⚡ T1` | Bellman-Ford / relax k times | `dist[v]` relax all edges `k+1` rounds or **min-heap** state `(cost, node, stops)` | **K stops** = at most `K+1` edges; **negative** edges not allowed in Dijkstra variant. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Clone Graph `⚡ T1` | Medium | BFS + HashMap | Map original→clone; BFS to copy edges |
| Pacific Atlantic Water Flow `⚡ T1` | Medium | Reverse BFS | BFS from both coasts; answer = intersection |
| Course Schedule II `⚡ T1` | Medium | Topo Sort (Kahn's) | Return topo order; empty if cycle exists |
| Number of Connected Components `⚡ T1` | Medium | Union-Find / DFS | Count distinct roots |
| Graph Valid Tree `⚡ T1` | Medium | Union-Find | n nodes, n-1 edges, no cycle = valid tree |
| Network Delay Time `🎯 T2` | Medium | Dijkstra | Single-source shortest path; return max dist |
| Swim in Rising Water `⚡ T1` | Hard | Binary Search + BFS / Dijkstra | Min time = min max-height path from (0,0) to (n-1,n-1) |
| Is Graph Bipartite? `⚡ T1` | Medium | 2-Coloring DFS/BFS | Alternate coloring nodes 0 and 1; a same-color conflict between neighbors means not bipartite |
| Redundant Connection `⚡ T1` | Medium | Union-Find | The edge that connects two vertices already in the same Union-Find set is redundant |

---

## Disjoint Set Union (DSU)

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Redundant Connection II `⚡ T1` | Hard | Directed DSU + Cycle | Track two parent pointers to find node with two parents; check cycle; remove correct edge to restore tree |
| Accounts Merge `⚡ T1` | Medium | DSU Connected Components | Treat emails as nodes, map to parent email; run DSU; group emails by absolute component root |
| Number of Good Paths `💤 T3` | Hard | DSU + Sorted Nodes | Sort nodes by value; union components starting from smallest; size of equal values within component determines paths |

---

## Dynamic programming

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Coin Change** `🎯 T2` | Unbounded knapsack | `dp[w] = min(dp[w], 1+dp[w-coin])` | **order** of coins doesn’t matter; **0** amount = 0 coins; **impossible** = inf. |
| **Longest Increasing Subsequence** `⚡ T1` | LIS O(n log n) | `tails` array; binary search position to replace | **Strictly** increasing vs **non-decreasing** changes binary search. |
| **Longest Common Subsequence** `🎯 T2` | 2D DP | Match → `1+dp[i-1][j-1]`; else `max(dp[i-1][j], dp[i][j-1])` | **Space** O(min(m,n)) possible; **empty** string base. |
| **Edit Distance** `🎯 T2` | 2D DP | Insert/delete/replace costs | **Indels** symmetric; **follow-up** one-row space. |
| **Word Break** `🎯 T2` | Partition + memo | `dp[i]` = can segment `s[i:]`; try each word prefix | **Word length** bound can optimize; **Trie** for multiple lookups. |
| **Burst Balloons** `🎯 T2` | Interval DP | `dp[i][j]` = max coins in open interval `(i,j)`; try last balloon `k` | **Multiply** `nums[i]*nums[k]*nums[j]` — **add** boundary 1s as sentinels. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Climbing Stairs `🎯 T2` | Easy | 1D DP | dp[i] = dp[i-1] + dp[i-2]; Fibonacci |
| House Robber `🎯 T2` | Medium | 1D DP | dp[i] = max(dp[i-1], dp[i-2] + nums[i]) |
| House Robber II (circular) `🎯 T2` | Medium | 1D DP | Run twice: [0..n-2] and [1..n-1]; take max |
| Longest Palindromic Subsequence `🎯 T2` | Medium | 2D DP (interval) | dp[i][j] = 2+dp[i+1][j-1] if match else max(dp[i+1][j], dp[i][j-1]) |
| Coin Change II (ways) `🎯 T2` | Medium | Unbounded Knapsack | dp[i] += dp[i-coin]; order: coin outer, amount inner |
| 0-1 Knapsack `⚡ T1` | Medium | 2D DP | dp[i][w] = max(skip, take if weight fits) |
| Partition Equal Subset Sum `🎯 T2` | Medium | 0-1 Knapsack | Can we reach sum/2? Subset sum DP |
| Unique Paths `⚡ T1` | Medium | Grid DP | dp[i][j] = dp[i-1][j] + dp[i][j-1] |
| Regular Expression Matching `🎯 T2` | Hard | 2D DP | Handle '*': match 0 times (dp[i][j-2]) or 1+ times (dp[i-1][j]) |

---

## Greedy

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Jump Game II** `🎯 T2` | Min jumps | Greedy: extend `furthest` in current jump range; increment jumps when `i` reaches `end` | **O(n)** single pass; **Jump Game I** is only reachability (different). |
| **Non-overlapping Intervals** `🎯 T2` | Min removals | Sort by end; **count** overlap when `start < last_end` | **Sort by end** not start — **counterexample** if start sort. |
| **Gas Station** `🎯 T2` | Circular greedy | If total gas ≥ total cost, unique start exists; track `tank`, reset start when `tank < 0` | **Proof** — if sum ≥ 0 solution exists; **O(n)** single pass. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Jump Game `🎯 T2` | Medium | Greedy | Track max reachable index; fail if current > max_reach |
| Candy `🎯 T2` | Hard | Two-pass Greedy | Left-to-right pass satisfying left neighbors, right-to-left pass satisfying right neighbors; merge via max |

---

## Backtracking

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Permutations** `🎯 T2` | All orderings | DFS + `used` or swap | **Duplicates** in `nums` — sort + skip same at same level. |
| **Combination Sum** `🎯 T2` | Sum with reuse | `start` index to avoid duplicate combinations | **Reuse** same element — next recursion starts at `i` not `i+1`. |
| **Subsets II** `🎯 T2` | Subsets with dupes | Sort; skip `nums[i]` if `i>start` and `nums[i]==nums[i-1]` | **Same level** skip vs **different** branch. |
| **Word Search** `⚡ T1` | Grid DFS | DFS + mark visited; backtrack | **Reuse** cell — **unmark** after return; **prune** with Trie in Word Search II. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Subsets `🎯 T2` | Medium | Choose/Skip | For each element: include or exclude |
| Permutations II (duplicates) `🎯 T2` | Medium | Sorted + Skip | Skip if used[i] or (same as prev and prev not used) |
| Combination Sum II `🎯 T2` | Medium | Sorted + Skip | Cannot reuse; skip duplicates at same depth |
| N-Queens `🎯 T2` | Hard | Row-by-row | Track col, diag1, diag2 as sets |
| Palindrome Partitioning `🎯 T2` | Medium | Backtrack + precompute | Precompute is_palindrome[i][j]; then backtrack |

---

## Trie

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Implement Trie `⚡ T1` | Medium | Prefix Tree | Dictionary-based children map plus end-of-word boolean marker |
| Word Search II `⚡ T1` | Hard | Trie + Backtracking DFS | Build Trie of search words; DFS on grid pruning paths immediately when prefix is absent in Trie |
| Design Add and Search Words `🎯 T2` | Medium | Trie + DFS Wildcard | Use recursion on Trie children for wildcard '.' characters; standard lookup for normal characters |
| Prefix and Suffix Search `💤 T3` | Hard | Trie of wrapped words | Insert wrapped words `suffix + '#' + word` into Trie; search prefix is resolved as `suffix + '#' + prefix` |

---

## Bit manipulation

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Single Number** `⚡ T1` | XOR | XOR all — pairs cancel | **General** to **Single Number II** (mod 3) — bit counts. |
| **Maximum XOR of Two Numbers** `⚡ T1` | Binary trie | Insert bits; for each number try opposite bit path | **Trie** depth 31 or 32 for signed ints; **leading** zeros. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Single Number II `🎯 T2` | Medium | Bit counting modulo 3 | Count set bits at each of 32 positions modulo 3; or use state machine masks `ones` and `twos` |
| Counting Bits `🎯 T2` | Easy | Bit DP | `dp[i] = dp[i >> 1] + (i & 1)`; the bit count of `i` is the count of its right shift plus its last bit |
| Sum of Two Integers `💤 T3` | Medium | Bit addition | Simulate half-adder: `a ^ b` computes sum without carry, `(a & b) << 1` computes carry; repeat until carry is zero |

---

## Math & number theory

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Happy Number `⚡ T1` | Easy | Floyd's Cycle Detection | Sequence of digit-square sums eventually loops; use fast/slow pointers on values instead of linked list |
| Pow(x, n) `🎯 T2` | Medium | Binary Exponentiation | `O(log N)` reduction: `pow(x, n) = pow(x*x, n//2)` for even, `x * pow(x, n-1)` for odd. Handle negative bounds |
| Sieve of Eratosthenes `🎯 T2` | Easy | Prime Sieving | Incrementally mark multiples of discovered primes as composite up to `sqrt(N)`; count unmarked |

---

## Strings (beyond array)

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Implement strStr / KMP** `🎯 T2` | LPS, no backtrack on text | Build `lps` from pattern; match with `lps` fallback | **Off-by-one** in `lps` build; **empty** pattern. |

**More canonical problems:**

| Problem | Difficulty | Pattern | Key Insight |
|---------|-----------|---------|-------------|
| Valid Palindrome `🎯 T2` | Easy | Two Pointers | Skip non-alphanumeric; compare lowercased |
| Longest Repeating Character Replacement `⚡ T1` | Medium | Sliding Window | Window valid if len - max_freq ≤ k |
| Find All Anagrams `⚡ T1` | Medium | Sliding Window (fixed) | Fixed window; compare freq maps |
| Longest Palindromic Substring `⚡ T1` | Medium | Expand Around Center | Try both odd and even expansions at each index |
| Palindromic Substrings (count) `⚡ T1` | Medium | Expand Around Center | Count each successful expansion |
| Encode and Decode Strings `🎯 T2` | Medium | Delimiter | Length-prefix format: "4#word" handles all delimiters |

---

## Variants Playbook

Pick the base pattern via [patterns-master § Quick Decision Trees](patterns-master.md#quick-decision-trees); then ask *"which invariant did they change?"* and use the matching section below.

### How Variants Work

- **Core insight:** a variant changes **one invariant** of a base problem — find which one shifted, re-derive only that part, keep the rest of the algorithm.
- **Four mutation types:**

| Mutation | Example | What changes |
|---|---|---|
| Constraint relaxed / tightened | remove "distinct"; add "at most k distinct" | duplicate handling; add a freq map to the window |
| Output changed | count → list all / path | bookkeeping (parents, choices); count→all usually O(n) → O(2ⁿ) |
| Input shape changed | sorted input; 1D → 2D; circular | hash → two pointers; 2D indexing; double the array / mod index |
| Online / updates | static → stream of queries | precompute, incremental state, or versioning |

- **Reusable tricks:** "exactly k" = atMost(k) − atMost(k−1); sorted input ⇒ two pointers beat hashing on space; "k stops/k uses" ⇒ add k to the state.
- **Where it breaks:** a disguised *different* problem ("Two Sum on a graph" is graph traversal) — re-check the pattern trigger before reusing the base.
- Interview follow-ups by transformation → [HOW_TO_THINK § escalation grammar](HOW_TO_THINK.md#the-escalation-grammar-what-follow-ups-will-be); per-family chains → [patterns-master § Follow-Up Chains](patterns-master.md#follow-up-chains--interview-progression--t1).

---

### Variant table

Base problem → the one invariant each variant changes → the fix. Tier and difficulty are for the base problem.

| Base (tier · diff) | Core move | Variant → what changes |
|---|---|---|
| [LIS](https://leetcode.com/problems/longest-increasing-subsequence/) `🎯 T2` · M | O(n²) "which chain can I extend?"; O(n log n) patience sort: `tails` array + `bisect_left` | **Number of LIS** → carry `(len, count)` per index · **Russian Doll Envelopes** → sort width ↑, height ↓ on ties, LIS on height · **Longest Bitonic / Mountain** → LIS from left + LIS from right, peak = max(L+R−1) |
| [Coin Change](https://leetcode.com/problems/coin-change/) `⚡ T1` · M | Unbounded knapsack: `dp[a] = min(dp[a − c] + 1)` | **Coin Change II** (combinations) → `+=`, coins outer loop · **Combination Sum IV** (order matters) → amount outer loop · **Min Cost for Tickets** → subtract pass length in days |
| [House Robber](https://leetcode.com/problems/house-robber/) `⚡ T1` · M | `dp[i] = max(dp[i−1], dp[i−2] + x)`, two rolling vars | **Circular** → run on `[0..n−2]` and `[1..n−1]` · **Tree** → postorder returns `(rob, skip)` · **Delete and Earn** → bucket values into `sum[v]`, then House Robber |
| [Permutations](https://leetcode.com/problems/permutations/) `⚡ T1` · M | Choose unused → recurse → undo | **With duplicates** → sort; skip `i` if `a[i] == a[i−1]` and `a[i−1]` unused · **Next Permutation** → no recursion: rightmost dip, swap with next larger on right, reverse suffix |
| [Word Search](https://leetcode.com/problems/word-search/) `⚡ T1` · M | DFS, mark `#`, restore on return | **Word Search II** (many words) → Trie of words, walk grid and Trie together, prune dead branches and remove found words |
| [Longest Substring w/o Repeat](https://leetcode.com/problems/longest-substring-without-repeating-characters/) `⚡ T1` · M | Window; `left = max(left, last[c] + 1)` | **Replace k chars** → valid while `len − maxFreq ≤ k` (maxFreq need not shrink) · **Min Window Substring** → expand until `need == 0`, shrink while valid · **Exactly k distinct** → atMost(k) − atMost(k−1) |
| [Course Schedule](https://leetcode.com/problems/course-schedule/) `⚡ T1` · M | Kahn's: pop in-degree 0; processed < n ⇒ cycle | **Course Schedule II** → return pop order · **Alien Dictionary** → edge from first differing char of adjacent words; prefix longer-before-shorter ⇒ invalid |
| [Subarray Sum = K](https://leetcode.com/problems/subarray-sum-equals-k/) `⚡ T1` · M | Prefix sum + count map seeded `{0: 1}`; window fails on negatives | **Contiguous Array** (equal 0/1) → map 0 → −1, store *first* index per prefix · **Path Sum III** (tree) → same map during DFS, decrement on backtrack · **Divisible by K** → key `prefix % k` (normalise negatives) |
| [3Sum](https://leetcode.com/problems/3sum/) `⚡ T1` · M | Sort; fix `i`, converge `l, r`; skip duplicates at all three | **4Sum** → two fixed loops + two pointers · **3Sum Closest** → track min `|sum − target|` · **3Sum Smaller** → when `sum < t`, add `r − l` at once |
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) `⚡ T1` · M | Move the shorter wall — the taller can't help while the short one bounds area | **Trapping Rain Water** → water at i = `min(maxL, maxR) − h[i]`; move the side with the smaller max, O(1) space |
| [Find Peak Element](https://leetcode.com/problems/find-peak-element/) `🎯 T2` · M | BS on slope: `a[mid] < a[mid+1]` ⇒ peak on right | **Peak in 2D** → BS on columns, take max row of mid column · **Koko / Ship Packages** → BS on answer with a greedy `feasible(x)` |
| [Search in Rotated Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) `⚡ T1` · M | One half is sorted; check if target lies in it | **With duplicates** → `a[l] == a[mid] == a[r]` ⇒ shrink both ends, worst O(n) · **Find minimum** → compare `a[mid]` with `a[r]` |
| [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) `🎯 T2` · M | Floyd; after meeting, reset one to head, step both by 1 → entry | **Middle** → `while fast and fast.next` · **k-th from end** → lead pointer k ahead · **Find Duplicate Number** → array as `i → a[i]` linked list, same Floyd |
| [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) `⚡ T1` · H | Min-heap of heads `(val, i, node)`; O(N log k) | **No heap** → pairwise divide-and-conquer merge, same O(N log k) · **Smallest Range Covering K Lists** → heap + track current max |
| [LCA of Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) `⚡ T1` · M | Return p/q/null; both sides non-null ⇒ this node | **BST** → walk from root: both smaller go left, both larger go right, else here · **Parent pointers** → two-pointer like list intersection · **Many queries** → binary lifting `💤 T3` |
| [Max Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) `🎯 T2` · H | Postorder; gain = `max(0, child)`; global = `val + L + R`; return `val + max(L, R)` | **Diameter** → same shape with depths · **Longest Univalue Path** → gain only if child value matches |
| [Serialize / Deserialize](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) `🎯 T2` · H | Preorder with `#` for null; rebuild from an iterator | **BST** → no null markers needed: preorder + bounds `(lo, hi)` rebuild in O(n) · **N-ary** → write child count after each value |
| [Merge Intervals](https://leetcode.com/problems/merge-intervals/) `🎯 T2` · M | Sort by start; merge while `start ≤ cur_end` | **Insert Interval** → three phases: before, overlapping, after · **Meeting Rooms II** → min-heap of end times · **Non-overlapping** (min removals) → sort by end, greedy keep |
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) `⚡ T1` · M | DFS/BFS from each unvisited land, count launches | **Max Area** → return size · **Pacific Atlantic** → reverse BFS from each ocean's border, intersect · **01 Matrix / Rotting Oranges** → multi-source BFS · **Islands II** (online adds) → Union-Find |
| [Unique Paths](https://leetcode.com/problems/unique-paths/) `⚡ T1` · M | `dp[i][j] = up + left`, 1D row | **Obstacles** → `dp = 0` on blocked cells · **Min Path Sum** → `min` + cell · **Dungeon Game** → DP from bottom-right (min HP needed going forward) |
| [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) `⚡ T1` · M | Decreasing stack of indices; pop resolves the popped index | **Largest Rectangle** → increasing stack; pop gives height, width from new top · **Remove K Digits** → pop larger digits while k > 0, strip leading zeros · **Circular NGE** → iterate 2n with `i % n` |
| [Top K Frequent](https://leetcode.com/problems/top-k-frequent-elements/) `⚡ T1` · M | Count map + min-heap of size k, O(n log k) | **O(n)** → bucket sort by frequency · **Kth Largest in Stream** → min-heap size k, top is answer · **Median of Stream** → two heaps, sizes differ ≤ 1 |
| [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) `⚡ T1` · M | Node = children map + `is_end`; walk/create | **Add and Search Words** → DFS all children at `.` · **Replace Words** → stop at first `is_end` on the walk · **Max XOR Pair** `🎯 T2` → bitwise trie, greedy opposite bit |
| [Single Number](https://leetcode.com/problems/single-number/) `⚡ T1` · E | XOR all; pairs cancel | **Single Number II** → per-bit count mod 3 · **Single Number III** → split by lowest set bit of total XOR · **Missing Number** → XOR indices and values (or Gauss sum) |
| [Happy Number](https://leetcode.com/problems/happy-number/) `🎯 T2` · E | Floyd on the implicit sequence `n → digit-square-sum(n)` | **Pow(x, n)** → binary exponentiation; negate `n` safely (Python fine, Java use `long`) · **Excel Column Number** → base 26, 1-indexed (`A = 1`) |

---

## See also

- [patterns-master.md](patterns-master.md) — full pattern catalog, decision trees, gotchas
- [INTERVIEW_JUDGMENT.md](INTERVIEW_JUDGMENT.md#round-cheatsheet-one-page) — round cheatsheet + revision schedule
- [HOW_TO_THINK.md](HOW_TO_THINK.md) — derive the pattern instead of recalling it
