# Topic Questions — Logic, Patterns, and Trickiness

This guide lists **canonical interview questions** by topic, **why** they appear, the **core solution logic**, and **what makes them tricky** (gotchas, wrong turns, follow-ups). Use with the full topic files in [data-structures/](data-structures/README.md) and [algorithms/](algorithms/README.md).

**Per-file detail:** Each markdown file in `foundations/` (data structures, algorithms, supplements) has an **Interview Questions — Logic & Trickiness** section with a table: **Question** | **Core logic** | **Trickiness & details** (follow-ups, edge cases, wrong answers, complexity notes). This document stays a **cross-topic index** with shorter rows; open the specific topic file for the **full** expanded table and the rest of the notes (concept, code, strategy, revision).

---

## Arrays, two pointers, sliding window, prefix sum

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Two Sum](../google-sde2/PROBLEM_DETAILS.md#two-sum)** | "Find target sum" in unsorted array | Complement map `target - x` | Duplicates; return indices vs pairs. |
| **[3Sum](../google-sde2/PROBLEM_DETAILS.md#3sum)** | "Sum of three = 0" + "Unique triplets" | Sort + Two Pointers (fixed `i`) | **Skip duplicates** at all 3 levels. |
| **[Subarray Sum Equals K](../google-sde2/PROBLEM_DETAILS.md#subarray-sum-equals-k)** | "Subarray" + "Sum = K" + **Negatives allowed** | Prefix sum + freq map | `count[0]=1` for start-of-array case. |
| **[Longest Substring Without Repeating](../google-sde2/PROBLEM_DETAILS.md#longest-substring-without-repeating)** | "Longest" + "Unique chars" | Sliding window + map | Window valid while unique; jump `i` to `last+1`. |
| **[Minimum Window Substring](../google-sde2/PROBLEM_DETAILS.md#minimum-window-substring)** | "Shortest" + "Contains all chars of T" | Sliding window + counter | Track `formed` vs `required` for O(1) check. |
| **[Trapping Rain Water](../google-sde2/PROBLEM_DETAILS.md#trapping-rain-water)** | "Height array" + "Collect water" | Two pointers or Monotonic Stack | Why move smaller side? Smaller side caps water. |
| **[Merge Intervals](../google-sde2/PROBLEM_DETAILS.md#merge-intervals)** | "Ranges" + "Overlapping" | Sort by start; merge if `curr.s <= prev.e` | Unsorted input; touching intervals `[1,4][4,5]`. |
| **[Product of Array Except Self](../google-sde2/PROBLEM_DETAILS.md#product-of-array-except-self)** | "Product" + **No division allowed** | Prefix products * Suffix products | Zeros (one vs multiple). |
| **[Median of Two Sorted Arrays](../google-sde2/PROBLEM_DETAILS.md#median-of-two-sorted-arrays)** | "Two sorted" + "Median" + O(log(M+N)) | Binary search on partition | Even/odd total length; empty array edges. |

---

## Hashing & frequency

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Group Anagrams](../google-sde2/PROBLEM_DETAILS.md#group-anagrams)** | "Anagrams" + "Group together" | Key = sorted string or 26-count tuple | Unicode chars; O(N*K log K) vs O(N*K). |
| **[Longest Consecutive Sequence](../google-sde2/PROBLEM_DETAILS.md#longest-consecutive-sequence)** | "Consecutive" + **O(N) time** | HashSet; only start if `x-1` missing | O(N) constraint (can't sort). |
| **[LRU Cache](../google-sde2/PROBLEM_DETAILS.md#lru-cache)** | "Design" + "O(1) access" + "Eviction" | HashMap + Doubly Linked List (DLL) | Dummy Head/Tail; thread safety (L5+). |
| **[Top K Frequent Elements](../google-sde2/PROBLEM_DETAILS.md#top-k-frequent-elements)** | "Top K" + "Most frequent" | Min-heap size K OR Bucket Sort | Bucket sort is O(N) if freqs are bounded. |

---

## Linked lists

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Reverse Linked List](../google-sde2/PROBLEM_DETAILS.md#reverse-linked-list)** | "Reverse" + O(1) space | `prev, curr, next` rewiring | Recursive uses O(N) stack. |
| **[Merge Two Sorted Lists](../google-sde2/PROBLEM_DETAILS.md#merge-two-sorted-lists)** | "Two sorted" + "Combine" | Dummy node + pointer compare | In-place vs new nodes. |
| **[Linked List Cycle II](../google-sde2/PROBLEM_DETAILS.md#linked-list-cycle-ii)** | "Cycle" + "Entry point" | Fast/Slow meet; reset one to head | Math proof (2(d+k) = d+k+nC). |
| **[Merge k Sorted Lists](../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists)** | "K sorted" + "Merge" | Min-Heap of (val, list_id, node) | Tie-break on list_id for stability. |
| **[Copy List with Random Pointer](../google-sde2/PROBLEM_DETAILS.md#copy-list-with-random-pointer)** | "Cloning" + "Arbitrary pointers" | Pass 1: Map old->new; Pass 2: Wire | O(1) space trick (interleave nodes). |

---

## Stack & queue

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Valid Parentheses](../google-sde2/PROBLEM_DETAILS.md#valid-parentheses)** | "Balanced" + "Order matters" | Stack of open brackets | Empty stack at end; type mismatch. |
| **[Daily Temperatures](../google-sde2/PROBLEM_DETAILS.md#daily-temperatures)** | "Next warmer" / "Distance to greater" | Monotonic Decr Stack of **indices** | Store indices, not values. |
| **[Largest Rectangle in Histogram](../google-sde2/PROBLEM_DETAILS.md#largest-rectangle-in-histogram)** | "Heights" + "Max area" | Monotonic Stack; pop when height drops | Sentinel 0 at end to flush stack. |
| **[Sliding Window Maximum](../google-sde2/PROBLEM_DETAILS.md#sliding-window-maximum)** | "Window size K" + "Maximum at each" | Monotonic Deque (descending) | Remove front if index out of window. |
| **[Decode String](../google-sde2/PROBLEM_DETAILS.md#decode-string)** | "Nested" + "3[a2[b]]" | Stack of (string, repeat_count) | Multi-digit numbers `100[a]`. |

---

## Trees & BST

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[LCA (BST)](../google-sde2/PROBLEM_DETAILS.md#lowest-common-ancestor-bst)** | "BST" + "Ancestor" | If both `p,q` < root → Left; else Root | LCA can be `p` or `q` itself. |
| **[LCA (binary tree)](../google-sde2/PROBLEM_DETAILS.md#lca-binary-tree)** | "Binary Tree" (Not BST) | Recursive; if Left and Right non-null | Assumes `p,q` both exist. |
| **[Serialize / Deserialize](../google-sde2/PROBLEM_DETAILS.md#serialize-deserialize-binary-tree)** | "Store/Rebuild" + "N-ary/Binary" | Preorder with null markers + Queue | Delimiters; handling negative values. |
| **[Max Path Sum](../google-sde2/PROBLEM_DETAILS.md#binary-tree-maximum-path-sum)** | "Path" + "Any node to any node" | Postorder: `local_max = l+r+val` | Return `max(0, val + max(l, r))` up. |
| **[Validate BST](../google-sde2/PROBLEM_DETAILS.md#validate-bst)** | "Is it a BST?" | Inorder must be strictly increasing | Left < Root < Right for **all** descendants. |

---

## Heap & priority queue

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Merge K Sorted Lists](../google-sde2/PROBLEM_DETAILS.md#merge-k-sorted-lists)** | "K sorted" + "Combine" | Min-Heap size K | Empty lists; stability. |
| **[Median from Data Stream](../google-sde2/PROBLEM_DETAILS.md#find-median-from-data-stream)** | "Dynamic" + "Median" | Max-heap (small half), Min-heap (large) | Rebalance to keep size diff ≤ 1. |
| **[Task Scheduler](../google-sde2/PROBLEM_DETAILS.md#task-scheduler)** | "Cooldown" + "Min time" | Greedy math: `(max_f-1)*(n+1) + num_max` | If tasks > idle slots, result is `len(tasks)`. |

---

## Binary search

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Rotated Array](../google-sde2/PROBLEM_DETAILS.md#search-in-rotated-sorted-array)** | "Sorted" + "Rotated" | Compare `mid` with `left` to find sorted half | Duplicates `nums[l]==nums[m]==nums[r]` → O(N). |
| **[Koko Eating Bananas](../google-sde2/PROBLEM_DETAILS.md#koko-eating-bananas)** | "Min speed" + "Maximize/Minimize" | BS on Answer; `range=[1, max(piles)]` | Ceiling division `(p+k-1)//k`. |
| **[Split Array Max Sum](../google-sde2/PROBLEM_DETAILS.md#split-array-largest-sum)** | "Minimize max sum" + "M subarrays" | BS on Answer; Greedy feasibility check | Lower bound = `max(nums)`, Upper = `sum(nums)`. |

---

## Graphs

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Number of Islands](../google-sde2/PROBLEM_DETAILS.md#number-of-islands)** | "Grid" + "Connected components" | DFS/BFS on grid; mark visited | Mutate grid vs visited set. |
| **[Course Schedule](../google-sde2/PROBLEM_DETAILS.md#course-schedule)** | "Prerequisites" + "Cycle detection" | Topological Sort (Kahn's or DFS 3-color) | Edge direction `[a, b]` (a depends on b). |
| **[Alien Dictionary](../google-sde2/PROBLEM_DETAILS.md#alien-dictionary)** | "Custom alphabet" + "Order" | Compare adj words → Topo Sort | Cycle = Invalid; Prefix order `"ab", "a"` = Invalid. |
| **[Word Ladder](../google-sde2/PROBLEM_DETAILS.md#word-ladder)** | "Shortest transformation" | BFS (Level-order) | Use Set for wordList; Bi-directional BFS for speed. |
| **[Cheapest Flights](../google-sde2/PROBLEM_DETAILS.md#cheapest-flights-within-k-stops)** | "Shortest path" + "Constraint (K stops)" | BFS or Dijkstra with state `(cost, node, stops)` | Stop constraint = `K+1` edges. |

---

## Dynamic programming

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Coin Change](../google-sde2/PROBLEM_DETAILS.md#coin-change)** | "Fewest coins" + "Infinite supply" | Unbounded Knapsack: `dp[w] = min(dp[w], 1+dp[w-c])` | Impossible = `inf`; Amount 0 = 0. |
| **[LIS](../google-sde2/PROBLEM_DETAILS.md#longest-increasing-subsequence)** | "Increasing" + "Subsequence" | Patience Sorting (Binary Search) O(N log N) | `tails` array stores smallest tail for len `i+1`. |
| **[LCS](../google-sde2/PROBLEM_DETAILS.md#longest-common-subsequence)** | "Two strings" + "Common order" | 2D DP: Match → `1+dp[i-1][j-1]`; else `max(up, left)` | Space O(min(M, N)). |
| **[Edit Distance](../google-sde2/PROBLEM_DETAILS.md#edit-distance)** | "Min operations" (Ins/Del/Replace) | 2D DP: min(insert, delete, replace) | Replace cost only if chars differ. |
| **[Word Break](../google-sde2/PROBLEM_DETAILS.md#word-break)** | "Partition string" + "Dictionary" | Linear DP: `dp[i]` = can segment `s[:i]` | Trie optimization; word length bounds. |
| **[Burst Balloons](../google-sde2/PROBLEM_DETAILS.md#burst-balloons)** | "Interval" + "Multiply surroundings" | Interval DP: try last balloon `k` in `(i, j)` | Multiply `nums[i]*nums[k]*nums[j]`. |

---

## Greedy

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Jump Game II](../google-sde2/PROBLEM_DETAILS.md#jump-game-ii)** | "Minimum jumps" | Greedy: extend `furthest` in current range | Increment jumps when `i == end`. |
| **[Non-overlapping](../google-sde2/PROBLEM_DETAILS.md#non-overlapping-intervals)** | "Min removals" to fix intervals | Sort by **End Time**; count overlaps | Greedy choice: earliest finishing interval. |
| **[Gas Station](../google-sde2/PROBLEM_DETAILS.md#gas-station)** | "Circular" + "Can I finish?" | Total gas ≥ cost → unique start exists | Reset start when `tank < 0`. |

---

## Backtracking

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Permutations](../google-sde2/PROBLEM_DETAILS.md#permutations)** | "All orderings" | DFS + `used` array OR swap-in-place | Duplicates: Sort + skip same at same level. |
| **[Combination Sum](../google-sde2/PROBLEM_DETAILS.md#combination-sum)** | "Sum = target" + "Can reuse" | DFS + `start` index (no reuse means `i+1`) | `i` not `i+1` for reuse. |
| **[Subsets II](../google-sde2/PROBLEM_DETAILS.md#subsets-ii)** | "All subsets" + "Duplicates in input" | Sort; skip `if i > start and nums[i] == nums[i-1]` | Same level skip. |
| **[Word Search](../google-sde2/PROBLEM_DETAILS.md#word-search)** | "Grid" + "Path of letters" | DFS + mark visited; Backtrack after return | Unmark visited before return. |

---

## Bit manipulation

| Question | Click Moment | Core logic | Trickiness / Gotchas |
|----------|----------------|------------|------------|
| **[Single Number](../google-sde2/PROBLEM_DETAILS.md#single-number)** | "Pairs" + "One unique" | XOR all: `x ^ x = 0` | Bit counts mod 3 for Single Number II. |
| **[Max XOR of Two](../google-sde2/PROBLEM_DETAILS.md#maximum-xor-of-two-numbers)** | "Max XOR" | Binary Trie (Prefix Tree) of bits | Trie depth 31; greedily pick opposite bit. |

---

## Strings (beyond array)

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **[Implement strStr / KMP](../google-sde2/PROBLEM_DETAILS.md#implement-strstr-kmp)** | LPS, no backtrack on text | Build `lps` from pattern; match with `lps` fallback | **Off-by-one** in `lps` build; **empty** pattern. |
| **[Minimum Window Substring](../google-sde2/PROBLEM_DETAILS.md#minimum-window-substring)** | See arrays | Same as sliding window hard | — |

---

## Design / system-style (often L5+)

| Question | What it tests | Core logic | Trickiness |
|----------|----------------|------------|------------|
| **[LRU Cache](../google-sde2/PROBLEM_DETAILS.md#lru-cache)** | HashMap + DLL | O(1) get/put | **Eviction** order; **capacity** 1 edge case. |
| **[LFU Cache](../google-sde2/PROBLEM_DETAILS.md#lfu-cache)** | freq + LRU within freq | **min_freq** tracking; **lists** per frequency | **Tie** LRU — **second** priority; **O(1)** requires careful structure. |
| **[Rate Limiter](../google-sde2/PROBLEM_DETAILS.md#rate-limiter)** | Token bucket / sliding window | Refill + consume tokens | **Thread** safety; **distributed** follow-up. |

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
