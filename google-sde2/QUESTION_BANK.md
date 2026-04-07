# Question Bank (Google SDE-2)

Canonical questions by topic, with the **trick** (what usually goes wrong) and where to find the reference code.

Use this to build mock sets: pick 1–2 from 2–3 topics per session.

---

## Arrays / Prefix sums

- Two Sum — trick: duplicates + return indices. Code: `snippets/python/arrays.py`
- Subarray Sum Equals K — trick: negatives break sliding window; need prefix-count map. Code: `snippets/python/arrays.py`
- Product of Array Except Self — trick: zeros; two-pass prefix/suffix. Code: `snippets/python/arrays.py`
- Merge Intervals — trick: sort by start; merge by end. Code: `snippets/python/arrays.py`
- Maximum Subarray — trick: all negatives; Kadane init. Code: `snippets/python/arrays.py`

## Two pointers / Sliding window

- Longest Substring Without Repeating — trick: jump `left` using last index. Code: `snippets/python/two_pointers_window.py`
- Minimum Window Substring — trick: `formed==required`; shrink while valid. Code: `snippets/python/two_pointers_window.py`
- Sliding Window Maximum — trick: store indices in deque; expire by index. Code: `snippets/python/two_pointers_window.py`

## Binary search

- Lower/Upper bound — trick: loop invariants (`lo<hi`). Code: `snippets/python/binary_search.py`
- Search in Rotated Sorted Array — trick: pick sorted half correctly. Code: `snippets/python/binary_search.py`
- “Search on answer” (Koko / split array) — trick: monotonic predicate. Code: `snippets/python/binary_search.py`

## Linked list

- Reverse Linked List — trick: save `next` before rewiring. Code: `snippets/python/linked_list.py`
- Remove Nth From End — trick: dummy head; move fast n steps. Code: `snippets/python/linked_list.py`
- Cycle II — trick: meet then head+meet step 1 to entry. Code: `snippets/python/linked_list.py`
- Merge Two Sorted Lists — trick: dummy head; attach remainder. Code: `snippets/python/linked_list.py`

## Stack / Queue

- Valid Parentheses — trick: early close when stack empty. Code: `snippets/python/stack_queue.py`
- Daily Temperatures — trick: monotonic stack of indices. Code: `snippets/python/stack_queue.py`
- Largest Rectangle Histogram — trick: sentinel flush + width formula. Code: `snippets/python/stack_queue.py`

## Trees

- Validate BST — trick: use min/max bounds, not parent-only checks. Code: `snippets/python/trees.py`
- LCA (binary tree) — trick: return node when matches p/q. Code: `snippets/python/trees.py`
- Max Path Sum — trick: return “gain” and update global with left+right. Code: `snippets/python/trees.py`
- Serialize/Deserialize — trick: delimiter + null markers. Code: `snippets/python/trees.py`

## Graphs

- Number of Islands — trick: mark visited early; iterative if deep. Code: `snippets/python/graphs.py`
- Rotting Oranges — trick: multi-source BFS + minutes by levels. Code: `snippets/python/graphs.py`
- Course Schedule — trick: edge direction `prereq -> course`; cycle if topo short. Code: `snippets/python/graphs.py`
- Clone Graph — trick: map old→copy to handle cycles. Code: `snippets/python/graphs.py`
- Dijkstra (stretch) — trick: skip stale heap entries. Code: `snippets/python/graphs.py`

## Dynamic programming

- House Robber — trick: `take/skip` vars. Code: `snippets/python/dp.py`
- Coin Change (min) — trick: impossible → -1; beware INF. Code: `snippets/python/dp.py`
- LIS — trick: `tails` uses lower_bound; length only. Code: `snippets/python/dp.py`
- LCS / Edit Distance (stretch) — trick: 2D recurrence; 1-row optimization. Code: `snippets/python/dp.py`
- Word Break — trick: dp on prefix positions; dictionary membership. Code: `snippets/python/dp.py`

## Backtracking

- Subsets — trick: include/exclude; copy path. Code: `snippets/python/backtracking.py`
- Permutations — trick: used[]; undo. Code: `snippets/python/backtracking.py`
- Combination Sum — trick: reuse index (unbounded) vs i+1 variant. Code: `snippets/python/backtracking.py`

## Union-Find

- Redundant Connection — trick: union returns false when cycle edge. Code: `snippets/python/union_find.py`

## Bit manipulation

- Single Number — trick: XOR cancels pairs. Code: `snippets/python/bit.py`
- Counting Bits — trick: dp[i>>1] + (i&1). Code: `snippets/python/bit.py`
- Total Hamming Distance — trick: per-bit contribution, not pairwise. Code: `snippets/python/bit.py`
- Maximum XOR Pair — trick: greedy bit prefixes (or trie). Code: `snippets/python/bit.py`

## Greedy

- Jump Game II — trick: “BFS levels” with `end/furthest`. Code: `snippets/python/greedy.py`
- Gas Station — trick: sum check + reset start when tank < 0. Code: `snippets/python/greedy.py`
- Non-overlapping intervals — trick: sort by end. Code: `snippets/python/greedy.py`

## Maths

- GCD/LCM — trick: divide first to avoid overflow in other languages. Code: `snippets/python/maths.py`
- Count Primes — trick: mark from p*p. Code: `snippets/python/maths.py`
- Trailing Zeroes — trick: count factors of 5. Code: `snippets/python/maths.py`

## Sorting

- Kth Largest — trick: quickselect index `n-k`, randomized pivot. Code: `snippets/python/sorting.py`

