# Question Bank (Google SDE-2)

Canonical questions by topic, with the **trick** (what usually goes wrong) and where to find the reference code.

Use this to build mock sets: pick 1–2 from 2–3 topics per session. Cross-index with [PROBLEM_SET.md](PROBLEM_SET.md) and the **14-day** schedule in [TWO_WEEK_REVISION.md](TWO_WEEK_REVISION.md) if you are on a short timeline.

---

## Arrays / Prefix sums

- [Two Sum](PROBLEM_DETAILS.md#two-sum) — trick: duplicates + return indices. Code: `snippets/python/arrays.py`
- [Subarray Sum Equals K](PROBLEM_DETAILS.md#subarray-sum-equals-k) — trick: negatives break sliding window; need prefix-count map. Code: `snippets/python/arrays.py`
- [Product of Array Except Self](PROBLEM_DETAILS.md#product-of-array-except-self) — trick: zeros; two-pass prefix/suffix. Code: `snippets/python/arrays.py`
- [Merge Intervals](PROBLEM_DETAILS.md#merge-intervals) — trick: sort by start; merge by end. Code: `snippets/python/arrays.py`
- [Maximum Subarray](PROBLEM_DETAILS.md#maximum-subarray) — trick: all negatives; Kadane init. Code: `snippets/python/arrays.py`

## Two pointers / Sliding window

- [Longest Substring Without Repeating](PROBLEM_DETAILS.md#longest-substring-without-repeating) — trick: jump `left` using last index. Code: `snippets/python/two_pointers_window.py`
- [Minimum Window Substring](PROBLEM_DETAILS.md#minimum-window-substring) — trick: `formed==required`; shrink while valid. Code: `snippets/python/two_pointers_window.py`
- [Sliding Window Maximum](PROBLEM_DETAILS.md#sliding-window-maximum) — trick: store indices in deque; expire by index. Code: `snippets/python/two_pointers_window.py`

## Binary search

- [Lower/Upper bound](PROBLEM_DETAILS.md#lower-upper-bound) — trick: loop invariants (`lo<hi`). Code: `snippets/python/binary_search.py`
- [Search in Rotated Sorted Array](PROBLEM_DETAILS.md#search-in-rotated-sorted-array) — trick: pick sorted half correctly. Code: `snippets/python/binary_search.py`
- “Search on answer” (Koko / split array) — trick: monotonic predicate. Code: `snippets/python/binary_search.py`

## Linked list

- [Reverse Linked List](PROBLEM_DETAILS.md#reverse-linked-list) — trick: save `next` before rewiring. Code: `snippets/python/linked_list.py`
- [Remove Nth From End](PROBLEM_DETAILS.md#remove-nth-from-end) — trick: dummy head; move fast n steps. Code: `snippets/python/linked_list.py`
- [Cycle II](PROBLEM_DETAILS.md#cycle-ii) — trick: meet then head+meet step 1 to entry. Code: `snippets/python/linked_list.py`
- [Merge Two Sorted Lists](PROBLEM_DETAILS.md#merge-two-sorted-lists) — trick: dummy head; attach remainder. Code: `snippets/python/linked_list.py`

## Stack / Queue

- [Valid Parentheses](PROBLEM_DETAILS.md#valid-parentheses) — trick: early close when stack empty. Code: `snippets/python/stack_queue.py`
- [Daily Temperatures](PROBLEM_DETAILS.md#daily-temperatures) — trick: monotonic stack of indices. Code: `snippets/python/stack_queue.py`
- [Largest Rectangle Histogram](PROBLEM_DETAILS.md#largest-rectangle-histogram) — trick: sentinel flush + width formula. Code: `snippets/python/stack_queue.py`

## Trees

- [Validate BST](PROBLEM_DETAILS.md#validate-bst) — trick: use min/max bounds, not parent-only checks. Code: `snippets/python/trees.py`
- [LCA (binary tree)](PROBLEM_DETAILS.md#lca-binary-tree) — trick: return node when matches p/q. Code: `snippets/python/trees.py`
- [Max Path Sum](PROBLEM_DETAILS.md#max-path-sum) — trick: return “gain” and update global with left+right. Code: `snippets/python/trees.py`
- [Serialize/Deserialize](PROBLEM_DETAILS.md#serialize-deserialize) — trick: delimiter + null markers. Code: `snippets/python/trees.py`

## Graphs

- [Number of Islands](PROBLEM_DETAILS.md#number-of-islands) — trick: mark visited early; iterative if deep. Code: `snippets/python/graphs.py`
- [Rotting Oranges](PROBLEM_DETAILS.md#rotting-oranges) — trick: multi-source BFS + minutes by levels. Code: `snippets/python/graphs.py`
- [Course Schedule](PROBLEM_DETAILS.md#course-schedule) — trick: edge direction `prereq -> course`; cycle if topo short. Code: `snippets/python/graphs.py`
- [Clone Graph](PROBLEM_DETAILS.md#clone-graph) — trick: map old→copy to handle cycles. Code: `snippets/python/graphs.py`
- [Dijkstra](PROBLEM_DETAILS.md#dijkstra) (stretch) — trick: skip stale heap entries. Code: `snippets/python/graphs.py`

## Dynamic programming

- [House Robber](PROBLEM_DETAILS.md#house-robber) — trick: `take/skip` vars. Code: `snippets/python/dp.py`
- [Coin Change](PROBLEM_DETAILS.md#coin-change) (min) — trick: impossible → -1; beware INF. Code: `snippets/python/dp.py`
- [LIS](PROBLEM_DETAILS.md#lis) — trick: `tails` uses lower_bound; length only. Code: `snippets/python/dp.py`
- [LCS / Edit Distance](PROBLEM_DETAILS.md#lcs-edit-distance) (stretch) — trick: 2D recurrence; 1-row optimization. Code: `snippets/python/dp.py`
- [Word Break](PROBLEM_DETAILS.md#word-break) — trick: dp on prefix positions; dictionary membership. Code: `snippets/python/dp.py`

## Backtracking

- [Subsets](PROBLEM_DETAILS.md#subsets) — trick: include/exclude; copy path. Code: `snippets/python/backtracking.py`
- [Permutations](PROBLEM_DETAILS.md#permutations) — trick: used[]; undo. Code: `snippets/python/backtracking.py`
- [Combination Sum](PROBLEM_DETAILS.md#combination-sum) — trick: reuse index (unbounded) vs i+1 variant. Code: `snippets/python/backtracking.py`

## Union-Find

- [Redundant Connection](PROBLEM_DETAILS.md#redundant-connection) — trick: union returns false when cycle edge. Code: `snippets/python/union_find.py`

## Bit manipulation

- [Single Number](PROBLEM_DETAILS.md#single-number) — trick: XOR cancels pairs. Code: `snippets/python/bit.py`
- [Counting Bits](PROBLEM_DETAILS.md#counting-bits) — trick: dp[i>>1] + (i&1). Code: `snippets/python/bit.py`
- [Total Hamming Distance](PROBLEM_DETAILS.md#total-hamming-distance) — trick: per-bit contribution, not pairwise. Code: `snippets/python/bit.py`
- [Maximum XOR Pair](PROBLEM_DETAILS.md#maximum-xor-pair) — trick: greedy bit prefixes (or trie). Code: `snippets/python/bit.py`

## Greedy

- [Jump Game II](PROBLEM_DETAILS.md#jump-game-ii) — trick: “BFS levels” with `end/furthest`. Code: `snippets/python/greedy.py`
- [Gas Station](PROBLEM_DETAILS.md#gas-station) — trick: sum check + reset start when tank < 0. Code: `snippets/python/greedy.py`
- [Non-overlapping intervals](PROBLEM_DETAILS.md#non-overlapping-intervals) — trick: sort by end. Code: `snippets/python/greedy.py`

## Maths

- [GCD/LCM](PROBLEM_DETAILS.md#gcd-lcm) — trick: divide first to avoid overflow in other languages. Code: `snippets/python/maths.py`
- [Count Primes](PROBLEM_DETAILS.md#count-primes) — trick: mark from p*p. Code: `snippets/python/maths.py`
- [Trailing Zeroes](PROBLEM_DETAILS.md#trailing-zeroes) — trick: count factors of 5. Code: `snippets/python/maths.py`

## Sorting

- [Kth Largest](PROBLEM_DETAILS.md#kth-largest) — trick: quickselect index `n-k`, randomized pivot. Code: `snippets/python/sorting.py`

