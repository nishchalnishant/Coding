# Question Bank (Google SDE-2)

Canonical questions by topic, with the **trick** (what usually goes wrong) and where to find the reference code.

Use this to build mock sets: pick 1–2 from 2–3 topics per session. Cross-index with [PROBLEM_SET.md](PROBLEM_SET.md) and the **14-day** schedule in [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) if you are on a short timeline.

---

## Arrays / Prefix sums

- [E] [Two Sum](PROBLEM_DETAILS.md#two-sum) — trick: duplicates + return indices, not values. Use `enumerate` to get both. Code: `snippets/python/arrays.py`
- [M] [Subarray Sum Equals K](PROBLEM_DETAILS.md#subarray-sum-equals-k) — trick: negatives break sliding window; use prefix-count map `{0:1}` initialized. Code: `snippets/python/arrays.py`
- [M] [Product of Array Except Self](PROBLEM_DETAILS.md#product-of-array-except-self) — trick: zeros cause division failure; two-pass prefix/suffix avoids division entirely. Code: `snippets/python/arrays.py`
- [M] [Merge Intervals](PROBLEM_DETAILS.md#merge-intervals) — trick: sort by start; new interval overlaps if `curr[0] <= last[1]`; extend end with `max`. Code: `snippets/python/arrays.py`
- [M] [Maximum Subarray](PROBLEM_DETAILS.md#maximum-subarray) — trick: all-negative case; Kadane init = `nums[0]`, not 0. Code: `snippets/python/arrays.py`

## Two pointers / Sliding window

- [M] [Longest Substring Without Repeating](PROBLEM_DETAILS.md#longest-substring-without-repeating) — trick: jump `left` to `last_seen[c]+1`, not `left+1`; update seen after checking. Code: `snippets/python/two_pointers_window.py`
- [H] [Minimum Window Substring](PROBLEM_DETAILS.md#minimum-window-substring) — trick: `formed==required` to detect valid; shrink while valid; track window with indices not copy. Code: `snippets/python/two_pointers_window.py`
- [H] [Sliding Window Maximum](PROBLEM_DETAILS.md#sliding-window-maximum) — trick: deque stores indices; pop front when `dq[0] < i - k + 1`; pop back while `nums[dq[-1]] < nums[i]`. Code: `snippets/python/two_pointers_window.py`

## Binary search

- [E] [Lower/Upper bound](PROBLEM_DETAILS.md#lower-upper-bound) — trick: use `lo < hi` (not `<=`); `lo = mid+1` vs `hi = mid` is the only difference between variants. Code: `snippets/python/binary_search.py`
- [M] [Search in Rotated Sorted Array](PROBLEM_DETAILS.md#search-in-rotated-sorted-array) — trick: check which half is sorted first (`a[lo] <= a[mid]`), then decide which side target falls in. Code: `snippets/python/binary_search.py`
- [M] Search on answer (Koko / split array) — trick: define a monotonic `feasible(mid)` predicate; `lo=min, hi=max`; return `lo` at end. Code: `snippets/python/binary_search.py`

## Linked list

- [E] [Reverse Linked List](PROBLEM_DETAILS.md#reverse-linked-list) — trick: save `next = curr.next` before rewiring `curr.next = prev`. Code: `snippets/python/linked_list.py`
- [M] [Remove Nth From End](PROBLEM_DETAILS.md#remove-nth-from-end) — trick: dummy head avoids null checks; advance `fast` by n+1 so `slow` lands before target. Code: `snippets/python/linked_list.py`
- [M] [Cycle II](PROBLEM_DETAILS.md#cycle-ii) — trick: after fast+slow meet, move one pointer to head; both move 1 step → meet at cycle entry. Code: `snippets/python/linked_list.py`
- [E] [Merge Two Sorted Lists](PROBLEM_DETAILS.md#merge-two-sorted-lists) — trick: dummy head; attach non-null remainder after loop. Code: `snippets/python/linked_list.py`

## Stack / Queue

- [E] [Valid Parentheses](PROBLEM_DETAILS.md#valid-parentheses) — trick: check `stack` is non-empty before popping; check `len(stack)==0` at end. Code: `snippets/python/stack_queue.py`
- [M] [Daily Temperatures](PROBLEM_DETAILS.md#daily-temperatures) — trick: monotonic stack of indices (decreasing temps); answer is `i - stack.pop()`. Code: `snippets/python/stack_queue.py`
- [H] [Largest Rectangle Histogram](PROBLEM_DETAILS.md#largest-rectangle-histogram) — trick: append sentinel `0`; width = `i - stack[-1] - 1` after pop (using index of previous shorter bar). Code: `snippets/python/stack_queue.py`

## Trees

- [M] [Validate BST](PROBLEM_DETAILS.md#validate-bst) — trick: pass `(min_val, max_val)` bounds down, not just parent; `node.val` must satisfy `min < val < max`. Code: `snippets/python/trees.py`
- [M] [LCA (binary tree)](PROBLEM_DETAILS.md#lca-binary-tree) — trick: return node when it matches `p` or `q`; LCA is first node with non-null from both sides. Code: `snippets/python/trees.py`
- [H] [Max Path Sum](PROBLEM_DETAILS.md#max-path-sum) — trick: helper returns single-branch gain (`max(0, left) + val`); global is updated with `left + right + val`. Code: `snippets/python/trees.py`
- [H] [Serialize/Deserialize](PROBLEM_DETAILS.md#serialize-deserialize) — trick: preorder with null markers; use `deque` for deserialize so `popleft` is O(1). Code: `snippets/python/trees.py`

## Graphs

- [M] [Number of Islands](PROBLEM_DETAILS.md#number-of-islands) — trick: mark `grid[r][c]='0'` immediately on enqueue (not dequeue) to prevent re-visit; use BFS to avoid recursion depth issues. Code: `snippets/python/graphs.py`
- [M] [Rotting Oranges](PROBLEM_DETAILS.md#rotting-oranges) — trick: multi-source BFS — seed all rotten oranges at minute 0; count fresh before BFS, not after. Code: `snippets/python/graphs.py`
- [M] [Course Schedule](PROBLEM_DETAILS.md#course-schedule) — trick: edge is `prereq → course`; has cycle if `len(order) != n` after Kahn's. Code: `snippets/python/graphs.py`
- [M] [Clone Graph](PROBLEM_DETAILS.md#clone-graph) — trick: `old_to_new` map prevents infinite loops on cycles; BFS processes each node exactly once. Code: `snippets/python/graphs.py`
- [M] [Dijkstra](PROBLEM_DETAILS.md#dijkstra) (stretch) — trick: skip stale heap entries with `if dist > recorded: continue`. Code: `snippets/python/graphs.py`

## Dynamic programming

- [M] [House Robber](PROBLEM_DETAILS.md#house-robber) — trick: two variables `prev, curr` suffice; `new_curr = max(curr, prev + nums[i])`. Code: `snippets/python/dp.py`
- [M] [Coin Change](PROBLEM_DETAILS.md#coin-change) (min) — trick: init `dp = [inf] * (amount+1)`, `dp[0]=0`; return -1 if `dp[amount]` is still inf. Code: `snippets/python/dp.py`
- [M/H] [LIS](PROBLEM_DETAILS.md#lis) — trick: `tails` array + `bisect_left` (lower bound); `tails` values are not the actual sequence, just length matters. Code: `snippets/python/dp.py`
- [H] [LCS / Edit Distance](PROBLEM_DETAILS.md#lcs-edit-distance) (stretch) — trick: 2D recurrence `dp[i][j] = dp[i-1][j-1]+1` (match) or `1+min(...)` (edit); 1-row optimization possible. Code: `snippets/python/dp.py`
- [M] [Word Break](PROBLEM_DETAILS.md#word-break) — trick: `dp[i]` = True if any `dp[j]` and `s[j:i] in word_set`; avoid O(n²×L) by bounding inner loop by max word length. Code: `snippets/python/dp.py`

## Backtracking

- [M] [Subsets](PROBLEM_DETAILS.md#subsets) — trick: include/exclude pattern OR loop-from-start; `path.copy()` before appending to results. Code: `snippets/python/backtracking.py`
- [M] [Permutations](PROBLEM_DETAILS.md#permutations) — trick: `used[]` boolean array; backtrack by setting `used[i]=False` after recurse. Code: `snippets/python/backtracking.py`
- [M] [Combination Sum](PROBLEM_DETAILS.md#combination-sum) — trick: unbounded = reuse same index `start=i`; 1-use = `start=i+1`; skip duplicate candidates by checking `i > start and nums[i] == nums[i-1]`. Code: `snippets/python/backtracking.py`

## Union-Find

- [M] [Redundant Connection](PROBLEM_DETAILS.md#redundant-connection) — trick: `union(u,v)` returns False when already in same component → that edge is the answer. Code: `snippets/python/union_find.py`
- [M] Number of Provinces — same DSU template; count distinct roots at end. Code: `snippets/python/union_find.py`

## Bit manipulation

- [E] [Single Number](PROBLEM_DETAILS.md#single-number) — trick: XOR cancels duplicate pairs; `a^a=0`, `a^0=a`. Code: `snippets/python/bit.py`
- [E] [Counting Bits](PROBLEM_DETAILS.md#counting-bits) — trick: `dp[i] = dp[i>>1] + (i&1)`; right shift removes LSB, add it back. Code: `snippets/python/bit.py`
- [M] [Total Hamming Distance](PROBLEM_DETAILS.md#total-hamming-distance) — trick: per-bit: count 1s (`ones`) and 0s (`n-ones`); contribution = `ones * (n-ones)`. Code: `snippets/python/bit.py`
- [H] [Maximum XOR Pair](PROBLEM_DETAILS.md#maximum-xor-pair) — trick: greedy bit-by-bit with prefix set; at each bit try to set it by checking if `prefix ^ (1<<bit)` exists. Code: `snippets/python/bit.py`

## Greedy

- [M] [Jump Game II](PROBLEM_DETAILS.md#jump-game-ii) — trick: track `end` (current BFS level boundary) and `furthest`; increment jumps when `i == end`; update `end = furthest`. Code: `snippets/python/greedy.py`
- [M] [Gas Station](PROBLEM_DETAILS.md#gas-station) — trick: if total sum >= 0 a solution exists; reset `start = i+1` when running tank < 0. Code: `snippets/python/greedy.py`
- [M] [Non-overlapping intervals](PROBLEM_DETAILS.md#non-overlapping-intervals) — trick: sort by end; greedily keep intervals with earliest end; remove (not keep) overlapping ones. Code: `snippets/python/greedy.py`

## Maths

- [E] [GCD/LCM](PROBLEM_DETAILS.md#gcd-lcm) — trick: `gcd(a,b) = gcd(b, a%b)`; `lcm = a*b // gcd(a,b)` — divide first to avoid overflow. Code: `snippets/python/maths.py`
- [M] [Count Primes](PROBLEM_DETAILS.md#count-primes) — trick: sieve; start marking from `p*p` (not `2p`); inner loop: `for j in range(p*p, n, p)`. Code: `snippets/python/maths.py`
- [E] [Trailing Zeroes](PROBLEM_DETAILS.md#trailing-zeroes) — trick: count factors of 5 only (5s are limiting); `n//5 + n//25 + n//125 + ...`. Code: `snippets/python/maths.py`

## Sorting

- [M] [Kth Largest](PROBLEM_DETAILS.md#kth-largest) — trick: quickselect targets index `n-k`; randomize pivot to avoid O(n²) worst case. Code: `snippets/python/sorting.py`

