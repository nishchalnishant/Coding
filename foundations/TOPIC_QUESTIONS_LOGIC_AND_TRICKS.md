# Topic Questions — Logic, Patterns, and Trickiness

This guide lists **canonical interview questions** by topic, **why** they appear, the **core solution logic**, and **what makes them tricky** (gotchas, wrong turns, follow-ups). Use with the full topic files in [data-structures/](data-structures/README.md) and [algorithms/](algorithms/README.md).

**Per-file detail:** Each markdown file in `foundations/` (data structures, algorithms, supplements) has an **Interview Questions — Logic & Trickiness** section with a table: **Question** | **Core logic** | **Trickiness & details** (follow-ups, edge cases, wrong answers, complexity notes). This document stays a **cross-topic index** with shorter rows; open the specific topic file for the **full** expanded table and the rest of the notes (concept, code, strategy, revision).

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

---

## Hashing & frequency

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Group Anagrams** | Canonical key for string | Key = sorted string OR tuple of 26 counts | **Unicode** — not 26 buckets if arbitrary chars; use **Counter** or sort. |
| **Longest Consecutive Sequence** | O(n) expected, not sort | Put all in set; for each `x`, only start sequence if `x-1` not in set | **O(n)** only if you don’t sort; **inner while** looks O(n²) but each number visited once across all sequences. |
| **LRU Cache** | HashMap + DLL | `get`: move to head; `put`: insert at head, evict tail if over capacity | **Doubly linked** for O(1) remove; **dummy head/tail** simplifies edges. Thread-safety follow-up at senior level. |
| **Top K Frequent Elements** | Bucket vs heap | Count freq → min-heap of size K **or** bucket by frequency | **Heap** is O(n log k); **bucket sort** can be O(n) if frequencies bounded. |

---

## Linked lists

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Reverse Linked List** | Pointer rewiring | `prev, curr, next`; iterative or recursive | **Recursive** uses O(n) stack; **null** head. |
| **Merge Two Sorted Lists** | Dummy node | Dummy → compare `l1`/`l2`, append smaller | **In-place** vs new list; **dummy** avoids null head cases. |
| **Linked List Cycle II** | Floyd + math | Fast/slow meet; reset one to head; **same speed** to entry | **Why entry?** — length algebra; **wrong**: restarting only fast from meet. |
| **Merge k Sorted Lists** | Heap | Min-heap of (val, list_id, node); pop min, push next | **O(N log k)** vs **compare all k** each step O(kN). **Tie-break** on list id for stability. |
| **Copy List with Random Pointer** | Old→new map | Two passes: create clones, wire `next`/`random` using map | **O(n)** space; **O(1)** space trick exists (interleave nodes) — bonus for senior. |

---

## Stack & queue

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Valid Parentheses** | Stack matching | Push opens; on close, pop and match | **Order** matters; **only one type** of bracket in simpler variants. |
| **Daily Temperatures** | Monotonic stack | Decreasing stack of indices; **warmer** pop and assign | **Indices** on stack, not values; **end** of array — sentinel or second pass. |
| **Largest Rectangle in Histogram** | Monotonic stack | Bars as heights; pop when lower; width = `i - new_top - 1` | **Sentinel 0** at end to flush stack; **width** formula when stack empty. |
| **Sliding Window Maximum** | Monotonic deque | Deque of indices, decreasing values; pop back while `nums[back] < nums[i]` | **Front** out of window — remove while `<= i-k`; **indices** not values for width. |
| **Decode String** | Nested structure | Stack of (current_string, repeat_count) or recursive | **Nested** `a2[b3[c]]` — stack per `[`; **digit** can be multi-digit `100[`. |

---

## Trees & BST

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Lowest Common Ancestor (BST)** | BST property | `p,q < root` → left; both > → right; else root | **LCA can be p or q**; **values** not nodes if duplicates policy unclear. |
| **LCA (binary tree)** | Recursion | If left and right return non-null → root; else return non-null child | **Assumption** `p,q` exist in tree; **not BST** — can’t use value compare. |
| **Serialize / Deserialize Binary Tree** | Design + traversal | Preorder with null markers + queue rebuild; or level-order | **One string** representation; **delimiter** for multi-digit values; **empty** tree. |
| **Binary Tree Maximum Path Sum** | Tree DP | Postorder: return max chain up; `global = max(global, left+right+val)` | **Path** may not pass root; **negative** nodes — use `max(0, child)`. |
| **Validate BST** | Inorder or bounds | Inorder must be strictly increasing **or** `node` in `(min,max)` | **BST** = left < root < right for **all** descendants — not just immediate children. |

---

## Heap & priority queue

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Merge K Sorted Lists** | K-way merge | Min-heap of size K (first node of each list) | Same as linked list section; **empty** lists in heap. |
| **Find Median from Data Stream** | Two heaps | `max` heap (lower half), `min` heap (upper half); balance sizes | **Rebalance** after each insert; **even** median = average of two tops. |
| **Task Scheduler** | Math + greedy | `(max_count-1)*(n+1) + num_max_tasks` | **Idle slots** formula; **cap** at `len(tasks)` if enough tasks fill gaps. |

---

## Binary search

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Search in Rotated Sorted Array** | Find sorted half | Compare `mid` with `left`/`right` to decide which half is sorted, then target in range? | **Duplicates** in `nums[left]==nums[mid]==nums[right]` — **worst case O(n)**. |
| **Koko Eating Bananas** | BS on answer | `min=1`, `max=max(piles)`; `valid(k)` = hours ≤ h; minimize k | **Ceiling** division per pile: `(p + k - 1) // k`. |
| **Split Array Largest Sum** | Minimize largest sum | BS on answer: `valid(mid)` = can split into ≤ m subarrays with sum ≤ mid | **Greedy** check for feasibility—**count splits** when sum exceeds mid. |

---

## Graphs

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Number of Islands** | DFS/BFS on grid | Mark visited; flood 4-dir from each `1` | **Mutate** grid vs `visited` set; **8-dir** if problem says so. |
| **Course Schedule** | Cycle in directed graph | Topo sort: Kahn or DFS 3-color | **Edge direction** `a,b` means `b` before `a` — **build graph** correctly. |
| **Alien Dictionary** | Topo + ordering | Compare adjacent words, first diff → edge; topo all letters | **Invalid** if cycle; **prefix** order — `"ab"` before `"abc"` gives no edge between words; **all letters** as nodes. |
| **Word Ladder** | BFS on implicit graph | BFS from `beginWord`; neighbors = one-letter diff in wordList | **WordList** as set for O(1) lookup; **length** of path = BFS level; **bidirectional** BFS follow-up. |
| **Cheapest Flights Within K Stops** | Bellman-Ford / relax k times | `dist[v]` relax all edges `k+1` rounds or **min-heap** state `(cost, node, stops)` | **K stops** = at most `K+1` edges; **negative** edges not allowed in Dijkstra variant. |

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

---

## Greedy

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Jump Game II** | Min jumps | Greedy: extend `furthest` in current jump range; increment jumps when `i` reaches `end` | **O(n)** single pass; **Jump Game I** is only reachability (different). |
| **Non-overlapping Intervals** | Min removals | Sort by end; **count** overlap when `start < last_end` | **Sort by end** not start — **counterexample** if start sort. |
| **Gas Station** | Circular greedy | If total gas ≥ total cost, unique start exists; track `tank`, reset start when `tank < 0` | **Proof** — if sum ≥ 0 solution exists; **O(n)** single pass. |

---

## Backtracking

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Permutations** | All orderings | DFS + `used` or swap | **Duplicates** in `nums` — sort + skip same at same level. |
| **Combination Sum** | Sum with reuse | `start` index to avoid duplicate combinations | **Reuse** same element — next recursion starts at `i` not `i+1`. |
| **Subsets II** | Subsets with dupes | Sort; skip `nums[i]` if `i>start` and `nums[i]==nums[i-1]` | **Same level** skip vs **different** branch. |
| **Word Search** | Grid DFS | DFS + mark visited; backtrack | **Reuse** cell — **unmark** after return; **prune** with Trie in Word Search II. |

---

## Bit manipulation

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Single Number** | XOR** | XOR all — pairs cancel | **General** to **Single Number II** (mod 3) — bit counts. |
| **Maximum XOR of Two Numbers** | Binary trie | Insert bits; for each number try opposite bit path | **Trie** depth 31 or 32 for signed ints; **leading** zeros. |

---

## Strings (beyond array)

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **Implement strStr / KMP** | LPS, no backtrack on text | Build `lps` from pattern; match with `lps` fallback | **Off-by-one** in `lps` build; **empty** pattern. |
| **Minimum Window Substring** | See arrays | Same as sliding window hard | — |

---

## Design / system-style (often L5+)

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **LRU Cache** | HashMap + DLL | O(1) get/put | **Eviction** order; **capacity** 1 edge case. |
| **LFU Cache** | freq + LRU within freq | **min_freq** tracking; **lists** per frequency | **Tie** LRU — **second** priority; **O(1)** requires careful structure. |
| **Rate Limiter** | Token bucket / sliding window | Refill + consume tokens | **Thread** safety; **distributed** follow-up. |

---

## How to use this in interviews

1. **Name the pattern** in 30 seconds: “This is subarray sum equals K — prefix sum with a map of prefix counts.”
2. **State the trick** before coding: “I need to skip duplicates in 3-sum at `i`, `left`, and `right`.”
3. **Fail** the obvious trap out loud: “Naive would be O(n²) checking all subarrays; I’ll use a map instead.”

---

## See also

- [GOOGLE_INTERVIEW_REVISION.md](GOOGLE_INTERVIEW_REVISION.md) — revision schedule  
- [patterns/leetcode-patterns.md](../patterns/leetcode-patterns.md) — pattern catalog  
- [sde-3-guide/sde-3-guide.md](../sde-3-guide/sde-3-guide.md) — Top 20 curated problems  
