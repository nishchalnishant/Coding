# Algorithms — Google L3 Cheat Sheet

> [!NOTE]
> **Tier Legend**
> `⚡ T1` — **TIER 1 · Must Master**: Reflexive recall required. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: Know the core pattern cold; edge cases matter less.
> `💤 T3` — **TIER 3 · Skim or Skip**: Conceptual awareness only for L3.

---

## Index

| Topic | Section | Tier |
| :---- | :------ | :--- |
| Two Pointers & Sliding Window | [Jump](#two-pointers--sliding-window) | `⚡ T1` |
| Binary Search | [Jump](#binary-search) | `⚡ T1` |
| Dynamic Programming | [Jump](#dynamic-programming) | `⚡ T1` |
| Recursion & Backtracking | [Jump](#recursion--backtracking) | `⚡ T1` |
| Graph Algorithms | [Jump](#graph-algorithms) | `⚡ T1` |
| Greedy | [Jump](#greedy) | `🎯 T2` |
| Divide & Conquer / Math | [Jump](#divide--conquer--math) | `🎯 T2` |
| Sorting (reference) | [Jump](#sorting-reference) | `🎯 T2` |
| Advanced Graphs | [Jump](#advanced-graphs) | `🎯 T2` |
| Union-Find (DSU) | [Jump](#union-find-dsu) | `🎯 T2` |
| Bit Manipulation | [Jump](#bit-manipulation) | `🎯 T2` |
| Intervals | [Jump](#intervals) | `🎯 T2` |

---


- [ ] Two Pointers & Sliding Window
    - Alternatives
        - Brute Force O(N²): Two pointers reduces pair-enumeration to O(N) by exploiting sorted or structural monotonicity.
        - Hash Map: For unsorted arrays, a hash map gives O(1) complement lookup — two pointers only beats this when the input is already sorted.
    - Key Techniques
        - **Converging (Opposite Ends):** `lo=0, hi=n-1`; move `lo` up on too-small, `hi` down on too-big. Needs sorted input. Used for: 2Sum, 3Sum, Container With Most Water.
        - **Fast / Slow (Floyd's Tortoise & Hare):** `fast` moves 2 steps, `slow` 1 step. If they meet, a cycle exists. Reset one to head → both advance 1 step until they meet again = cycle start.
        - **Same-Direction (Write Pointer):** `slow` marks the last valid position; `fast` scans. Used for: Remove Duplicates, Move Zeros, Dutch National Flag.
        - **Sliding Window — Fixed Size K:** Build initial window; slide by adding `arr[right]` and removing `arr[right-K]`. O(N).
        - **Sliding Window — Variable Size:** Expand `right` greedily; shrink `left` while constraint violated. `max_len = right - left + 1`. Used for: Longest Substring Without Repeating Chars, Minimum Window Substring.
        - **Exactly K Trick:** `exactly(K) = atMost(K) - atMost(K-1)`. Sliding window for "exactly K distinct" is not monotone — always use this decomposition.
    - Gotchas
        - Converging only works on sorted input — always sort first and note the O(N log N) overhead.
        - Duplicate handling in 3Sum: skip identical values at the anchor AND at both inner pointers.
        - Sliding window with character maps: decrement count on left exit; delete key when count reaches 0.
        - "Exactly K distinct" is NOT handled by a single window — use atMost trick.
    - Questions — Two Pointers `⚡ T1 / 🎯 T2`
        - **Two Sum II (Sorted Array) `⚡ T1`**
            - Description: Given a 1-indexed sorted array, find two numbers that add up to target and return their positions.
            - Pattern: Converging two pointers
            - Key insight: sorted array → complement lives at the other end. Move `lo` if sum too small, `hi` if too large. O(N) O(1).
            - Gotcha: input is 1-indexed in LC 167 — return `[lo+1, hi+1]`.
        - **3Sum `⚡ T1`**
            - Description: Given an integer array, find all unique triplets [a,b,c] such that a + b + c = 0.
            - Pattern: Sort + fix anchor + converging inner pointers
            - Key insight: sort first; fix `nums[i]`, two-pointer on `[i+1..n-1]`. Skip duplicate anchors and duplicate inner values after recording a triplet.
            - Gotcha: skip ALL equal values at each pointer level, not just one.
        - **Container With Most Water `⚡ T1`**
            - Description: Given n vertical lines with heights, find two lines that form a container holding the most water.
            - Pattern: Converging
            - Key insight: `area = min(h[lo], h[hi]) * (hi - lo)`. Always move the shorter side — the taller side can never make the `min()` larger.
            - Gotcha: moving the taller side never improves `min(h[lo], h[hi])`.
        - **Trapping Rain Water `⚡ T1`**
            - Description: Given an elevation map of bar heights, compute how much rainwater can be trapped after rain.
            - Pattern: Converging with running max
            - Key insight: water at `i` = `min(max_left, max_right) - h[i]`. Use two-pointer O(N) O(1): advance the side with the smaller `l_max`/`r_max`.
            - Gotcha: two-pointer is different from the stack solution — both are O(N).
        - **Sort Colors (Dutch National Flag) `⚡ T1`**
            - Description: Given an array with values 0, 1, 2 (red/white/blue), sort it in-place in a single pass without using sort().
            - Pattern: Three pointers `lo, mid, hi`
            - Key insight: `0→swap with lo++`, `1→mid++`, `2→swap with hi--`. Do NOT increment `mid` after swapping with `hi` — newly swapped element is unchecked.
        - **Valid Palindrome II `🎯 T2`**
            - Description: Given string s, return true if it can become a palindrome by removing at most one character.
            - Pattern: Converging with one skip allowed
            - Key insight: on first mismatch, try skipping `left` or skipping `right`, then check if the remaining substring is a palindrome.
        - **Linked List Cycle `🎯 T2`**
            - Description: Given head of a linked list, determine if it contains a cycle. Return true/false.
            - Pattern: Fast/slow — Floyd's
            - Key insight: fast 2 steps, slow 1 step. If they meet, cycle exists. Reset one to head, single-step both → meeting point = cycle entry.
        - **Longest Substring Without Repeating Chars `⚡ T1`**
            - Description: Find the length of the longest substring that contains no repeated characters.
            - Pattern: Variable sliding window
            - Key insight: `seen` dict maps char → last index. On duplicate, jump `left = seen[ch] + 1` (only if char is inside window: `seen[ch] >= left`).
        - **Minimum Window Substring `⚡ T1`**
            - Description: Given strings s and t, find the minimum window in s that contains every character in t (including duplicates).
            - Pattern: Variable sliding window + frequency map
            - Key insight: track `missing` count. Expand right to fulfill need; shrink left while `missing == 0` to minimize window. Record on valid shrink.
        - **Sliding Window Maximum `⚡ T1`**
            - Description: Given an integer array and window size k, return the maximum value in each sliding window of size k.
            - Pattern: Monotonic deque
            - Key insight: deque stores indices in decreasing-value order. Front = max of current window. Pop from front when index is out of window; pop from back when new value is larger.
            - Gotcha: store indices, not values — you need indices to check if front is expired.
        - **Find All Anagrams in a String `⚡ T1`**
            - Description: Given strings s and p, find all starting indices in s where a substring is an anagram of p.
            - Pattern: Fixed sliding window (size = `len(p)`)
            - Key insight: window size is fixed. Use a match-count trick instead of comparing full Counter dicts each step.
        - **Permutation in String `⚡ T1`**
            - Description: Given strings s1 and s2, return true if any permutation of s1 is a substring of s2.
            - Pattern: Fixed sliding window (same as anagram)
            - Key insight: same as anagram check — window = `len(s1)`. Return True if any window matches.
        - **Longest Repeating Character Replacement `🎯 T2`**
            - Description: Given string s and integer k, find the length of the longest substring where you can change at most k characters to all be the same letter.
            - Pattern: Variable sliding window
            - Key insight: window is valid if `(window_len - max_freq) <= k`. Shrink only when this condition is violated. It's OK if `max_freq` doesn't decrease on shrink — the answer only grows.
        - **Subarrays with K Distinct `🎯 T2`**
            - Description: Given an integer array and k, count subarrays with exactly k distinct integers.
            - Pattern: atMost trick
            - Key insight: `exactly(K) = atMost(K) - atMost(K-1)`. A single window cannot handle "exactly" because it's not monotone.

---

- [ ] Binary Search
    - Alternatives
        - Linear Search O(N): Binary search is O(log N) — only applicable when input is sorted OR the answer space is monotone.
        - Two Pointers: If the array is sorted and you need a pair, two pointers is O(N) vs O(N log N) for BS + scan.
    - Key Techniques
        - **Exact Match (`lo <= hi`):** Classic. `lo = mid+1` on too-small, `hi = mid-1` on too-big. Returns -1 if not found.
        - **Lower Bound / Upper Bound (`lo < hi`, `hi = len`):** Use `lo < hi` with `hi` as an exclusive sentinel. `hi = mid` (not `mid-1`) keeps `mid` as candidate. Terminates with `lo == hi == answer`.
        - **Binary Search on Answer:** Answer space `[lo, hi]` is monotone (feasible once → feasible for all larger values). Write a `feasible(mid)` predicate. To minimize: `if feasible(mid): hi = mid else: lo = mid+1`. Upper-mid trick: when doing `lo = mid`, use `mid = lo + (hi - lo + 1) // 2`.
        - **Rotated Sorted Array:** One half is always sorted. Check `if nums[lo] <= nums[mid]` (left sorted). If target in that half, go there; else go to the other.
        - **2D Binary Search (LC 74 — flattened):** Treat m×n matrix as 1D array. `val = matrix[mid // n][mid % n]`.
    - Gotchas
        - `mid = lo + (hi - lo) // 2` avoids integer overflow (critical in Java/C++; safe to skip in Python).
        - `lo = mid` (not `lo = mid+1`) causes infinite loop when `hi = lo + 1` — use upper-mid formula.
        - Rotated with duplicates: when `nums[lo] == nums[mid] == nums[hi]`, can't determine sorted half → `lo++; hi--`. Worst case degrades to O(N).
        - Search 2D Matrix II (LC 240) is NOT binary search — it's O(M+N) staircase starting top-right.
    - Off-By-One Reference Table

        | Goal | `lo` | `hi` | Loop | On `arr[mid] < target` | On `arr[mid] >= target` | Answer |
        |------|------|------|------|------------------------|------------------------|--------|
        | Exact match | 0 | n-1 | `<= ` | `lo = mid+1` | `hi = mid-1` | `mid` or -1 |
        | Lower bound | 0 | n | `< ` | `lo = mid+1` | `hi = mid` | `lo` |
        | Upper bound | 0 | n | `< ` | `lo = mid+1` (≤) | `hi = mid` | `lo` |
        | Minimize answer | lo | hi | `< ` | `lo = mid+1` | `hi = mid` | `lo` |
        | Maximize answer | lo | hi | `< ` | `lo = mid` (upper-mid) | `hi = mid-1` | `lo` |

    - Questions — Binary Search `⚡ T1 / 🎯 T2`
        - **Binary Search `⚡ T1`**
            - Description: Given a sorted array and a target, return the index of target or -1 if not found. Must run in O(log N).
            - Pattern: Exact match
            - Key insight: `lo <= hi`. Return `mid` on match, -1 on exhaustion. The template every other BS variant builds on.
        - **Search in Rotated Sorted Array `⚡ T1`**
            - Description: A sorted array has been rotated at an unknown pivot. Search for a target and return its index, or -1.
            - Pattern: Rotated BS
            - Key insight: Check which half is sorted (`nums[lo] <= nums[mid]`), then check if target falls in that half. Go there; otherwise, go to the other.
        - **Find Minimum in Rotated Sorted Array `⚡ T1`**
            - Description: A sorted array rotated at some pivot. Find and return the minimum element in O(log N).
            - Pattern: Rotated BS, `lo < hi`
            - Key insight: compare `nums[mid]` with `nums[hi]`. If `nums[mid] > nums[hi]`, min is in right half. Else `hi = mid` (mid could be the min).
        - **Koko Eating Bananas `⚡ T1`**
            - Description: Koko has piles of bananas and h hours. Find the minimum eating speed k (bananas/hr) such that she can eat all bananas within h hours.
            - Pattern: BS on answer
            - Key insight: binary search on speed `k ∈ [1, max(piles)]`. `feasible(k)` = `sum(ceil(p/k) for p in piles) <= h`. Ceiling division: `math.ceil(p/k)` or `-((-p)//k)`.
        - **Capacity to Ship Packages Within D Days `🎯 T2`**
            - Description: Given package weights and d days, find the minimum ship capacity to ship all packages in order within d days.
            - Pattern: BS on answer
            - Key insight: binary search on capacity `∈ [max(weights), sum(weights)]`. `feasible(cap)` = greedily simulate days needed; return `days <= D`.
        - **Search a 2D Matrix `⚡ T1`**
            - Description: In an m×n matrix where each row is sorted and each row's first element is greater than the previous row's last, search for a target in O(log(m*n)).
            - Pattern: 2D BS (flattened)
            - Key insight: treat as 1D. `mid // n` = row, `mid % n` = col.
        - **Find Minimum in Rotated Sorted Array II (with duplicates) `🎯 T2`**
            - Description: A sorted array rotated at some pivot. Find and return the minimum element in O(log N).
            - Pattern: Rotated BS with edge case
            - Key insight: same as LC 153 but when `nums[lo] == nums[mid] == nums[hi]`, can't determine sorted half → `lo++; hi--`. Worst case O(N).
        - **Search in Rotated Sorted Array II (with duplicates) `🎯 T2`**
            - Description: A sorted array has been rotated at an unknown pivot. Search for a target and return its index, or -1.
            - Pattern: Rotated BS with edge case
            - Key insight: same as LC 33 but handle `nums[lo] == nums[mid]` → `lo++` to skip ambiguity.
        - **Time Based Key-Value Store `🎯 T2`**
            - Description: Design a key-value store where set(key, value, timestamp) stores a value and get(key, timestamp) returns the value with the largest timestamp <= given timestamp.
            - Pattern: BS on answer (within a sorted list)
            - Key insight: store `(timestamp, value)` pairs per key. On `get(key, timestamp)`, binary search the list for the largest timestamp `<= timestamp`. Use `upper_bound - 1`.

---

- [ ] Dynamic Programming
    - Alternatives
        - Backtracking: DP = backtracking + memoization. If subproblems overlap (same `(i, state)` reached from multiple paths), cache results → DP.
        - Greedy: Greedy makes irrevocable local-optimal choices (O(N log N)). DP considers all choices (O(N²)). If you can construct a counterexample to greedy, use DP.
    - The 4-Step Recipe (Always in this order)
        1. Write the recursive brute-force with correct base cases
        2. Add a memo dict keyed on all recursion arguments → top-down DP
        3. Invert to bottom-up table filled in dependency order
        4. Compress table when `dp[i]` only depends on a fixed window of past values → O(1) space
    - Pattern Map — Pick in 30 seconds

        | Signal | Pattern |
        |--------|---------|
        | Pick items once, hit capacity/sum | **0/1 Knapsack** — backward inner loop |
        | Pick items unlimited times | **Unbounded Knapsack** — forward inner loop |
        | `dp[i]` from `dp[i-1]`, `dp[i-2]` | **Linear/Fibonacci** |
        | Two sequences, align & match | **LCS family** |
        | Best subarray ending at `i` | **Kadane** |
        | Split interval `[i,j]` at every `k` | **Interval DP / MCM** |
        | Grid, move right/down | **Grid DP** |
        | Subtree answers combined at root | **Tree DP (post-order DFS)** |
        | "count ways" with items | `dp[0] = 1`, add not max |

    - Key Knapsack Rule
        - 0/1 Knapsack → iterate `w` **BACKWARD** (high → low) in the 1D array. Ensures each item used at most once.
        - Unbounded Knapsack → iterate `w` **FORWARD** (low → high). Allows re-picking the same item.
        - Getting this backwards is the #1 knapsack bug.
    - Questions — DP `⚡ T1 / 🎯 T2`
        - **Climbing Stairs `🎯 T2`**
            - Description: You can climb 1 or 2 steps at a time. How many distinct ways are there to reach the top of n stairs?
            - Pattern: Linear/Fibonacci
            - Key insight: `dp[i] = dp[i-1] + dp[i-2]`. Space-optimize to two variables `a, b`.
        - **House Robber `🎯 T2`**
            - Description: Houses in a line. You cannot rob adjacent houses. Find the maximum money you can rob tonight.
            - Pattern: Linear
            - Key insight: `dp[i] = max(dp[i-1], nums[i] + dp[i-2])`. O(1) space with `prev2, prev1`.
        - **House Robber II `🎯 T2`**
            - Description: Same as House Robber but houses are arranged in a circle, so first and last are adjacent.
            - Pattern: Linear (circle trick)
            - Key insight: first and last houses are adjacent → can't rob both. Run linear robber twice: on `nums[:-1]` and `nums[1:]`. Take max.
        - **Decode Ways `🎯 T2`**
            - Description: A digit string encodes letters where A=1..Z=26. Count the number of distinct ways to decode it.
            - Pattern: Linear
            - Key insight: at each position, try 1-digit decode (if `s[i] != '0'`) and 2-digit decode (if `10 <= int(s[i-2:i]) <= 26`). A leading `'0'` kills that branch.
        - **Partition Equal Subset Sum `🎯 T2`**
            - Description: Given an integer array, determine if it can be partitioned into two subsets with equal sum.
            - Pattern: 0/1 Knapsack (boolean)
            - Key insight: Can we find a subset summing to `total // 2`? `dp[w] |= dp[w - num]`. Iterate `w` backward.
        - **Target Sum `🎯 T2`**
            - Description: Assign + or - to each element of an array. Count the number of ways the expression evaluates to target.
            - Pattern: 0/1 Knapsack (count)
            - Key insight: split into two subsets `P` and `N`. `P - N = target`, `P + N = total`. → `P = (total + target) / 2`. Count subsets summing to `P`. Parity check first: `(total + target) % 2 != 0` → 0 ways.
        - **Coin Change I `🎯 T2`**
            - Description: Given coin denominations and an amount, find the minimum number of coins needed to make that amount. Return -1 if impossible.
            - Pattern: Unbounded Knapsack (minimize)
            - Key insight: `dp[w] = min(dp[w], 1 + dp[w - coin])`. `dp[0] = 0`, rest `inf`. Iterate coins outer, amount forward.
        - **Coin Change II `🎯 T2`**
            - Description: Given coin denominations and an amount, count the number of distinct combinations of coins that sum to amount.
            - Pattern: Unbounded Knapsack (count combinations)
            - Key insight: `dp[w] += dp[w - coin]`. Coins outer → counts combinations (not permutations). `dp[0] = 1`.
        - **Longest Increasing Subsequence `🎯 T2`**
            - Description: Find the length of the longest strictly increasing subsequence in an integer array.
            - Pattern: LIS
            - Key insight: O(N²): `dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])`. O(N log N): patience sort with `tails[]` and `bisect_left`.
        - **Edit Distance `🎯 T2`**
            - Description: Given two strings, find the minimum number of insert, delete, or replace operations to convert word1 to word2.
            - Pattern: LCS family (2D string DP)
            - Key insight: `dp[i][j]` = min ops to convert `word1[:i]` to `word2[:j]`. Match → `dp[i-1][j-1]`. Else `1 + min(delete, insert, replace)`.
        - **Unique Paths `🎯 T2`**
            - Description: In an m×n grid, count the number of distinct paths from the top-left to the bottom-right, moving only right or down.
            - Pattern: Grid DP
            - Key insight: `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. Base: first row and column all 1s.
        - **Unique Paths II `🎯 T2`**
            - Description: Same as Unique Paths but some cells are blocked (marked 1). Count distinct unobstructed paths.
            - Pattern: Grid DP with obstacles
            - Key insight: same as above but `dp[r][c] = 0` if `grid[r][c] == 1`.
        - **Interleaving String `🎯 T2`**
            - Description: Given s1, s2, and s3, return true if s3 can be formed by interleaving characters of s1 and s2 (preserving relative order of each).
            - Pattern: LCS family
            - Key insight: `dp[i][j] = True` if `s3[:i+j]` is formed by interleaving `s1[:i]` and `s2[:j]`. Check both branches in transition.
        - **House Robber III `🎯 T2`**
            - Description: Houses are nodes in a binary tree. Adjacent parent-child nodes cannot both be robbed. Maximize money robbed.
            - Pattern: Tree DP (post-order DFS)
            - Key insight: `dfs(node)` returns `(rob_node, skip_node)`. Parent combines: `rob = skip_left + skip_right + node.val`, `skip = max(left) + max(right)`.
        - **Palindrome Partitioning II `🎯 T2`**
            - Description: Return the minimum number of cuts to partition a string s so every substring is a palindrome.
            - Pattern: Interval DP
            - Key insight: precompute `is_pal[i][j]` in O(N²). Then `dp[i] = min(dp[j-1] + 1 for all j where s[j:i+1] is palindrome)`.
        - **Best Time to Buy and Sell Stock II `🎯 T2`**
            - Description: You may buy and sell on any day (at most one share at a time, unlimited transactions). Maximize total profit.
            - Pattern: State machine DP
            - Key insight: unlimited transactions. At each day: hold state `max(prev_hold, prev_cash - price)`, cash state `max(prev_cash, prev_hold + price)`.
        - **Best Time to Buy and Sell Stock with Cooldown `🎯 T2`**
            - Description: After selling, you must wait one day before buying again. Maximize profit with unlimited transactions.
            - Pattern: State machine DP (3 states)
            - Key insight: three states: `held`, `sold` (cooldown), `rest`. Transitions: `held = max(held, rest - price)`, `sold = held + price`, `rest = max(rest, sold)`.
        - **Min Cost Climbing Stairs `🎯 T2`**
            - Description: Each step has a cost. You can start at step 0 or 1 and climb 1 or 2 steps. Find minimum cost to reach beyond the top.
            - Pattern: Linear
            - Key insight: `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`. Answer is `min(dp[-1], dp[-2])`. Can start at step 0 or 1.
        - **Last Stone Weight II `🎯 T2`**
            - Description: Repeatedly smash any two stones, keeping the difference. Minimize the weight of the last remaining stone.
            - Pattern: 0/1 Knapsack
            - Key insight: minimize `|S1 - S2|` where `S1 + S2 = total`. Equivalent to subset sum to `total // 2`.
        - **Word Break `⚡ T1`**
            - Description: Given a string s and a dictionary, return true if s can be segmented into one or more dictionary words.
            - Pattern: Linear DP + HashSet
            - Key insight: `dp[i] = True` if any `dp[j]` is True AND `s[j:i]` in word set; O(N²). Top-down DFS+memo cleaner for returning actual word break list.
        - **Maximal Square `⚡ T1`**
            - Description: In a binary matrix of '0's and '1's, find the largest square containing only '1's and return its area.
            - Pattern: Grid DP
            - Key insight: `dp[r][c] = min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) + 1` when cell is `'1'`. The minimum of three neighbors is the bottleneck. Answer = `max(dp)²`.
        - **Longest Common Subsequence `🎯 T2`**
            - Description: Given two strings, find the length of their longest common subsequence (characters don't need to be contiguous).
            - Pattern: LCS 2D string DP (foundation for Edit Distance, SCS, LPS)
            - Key insight: `dp[i][j] = dp[i-1][j-1] + 1` if chars match; else `max(dp[i-1][j], dp[i][j-1])`. Fill row-by-row; O(MN) time, O(N) space.
        - **Longest Palindromic Subsequence `🎯 T2`**
            - Description: Find the length of the longest subsequence of a string that is a palindrome.
            - Pattern: LCS of s and reverse(s); or interval DP
            - Key insight: `dp[i][j] = dp[i+1][j-1] + 2` if `s[i]==s[j]`; else `max(dp[i+1][j], dp[i][j-1])`. Fill by increasing interval length.
        - **Burst Balloons `🎯 T2`**
            - Description: Given n balloons with values, bursting balloon i gives nums[i-1]*nums[i]*nums[i+1] coins. Maximize total coins.
            - Pattern: Interval DP — think "last balloon to burst"
            - Key insight: `dp[i][j]` = max coins bursting all in `(i,j)`. Fix k as the **last** to burst; `coins = nums[i]*nums[k]*nums[j]`. Add padding `nums[-1]=nums[n]=1`. Fill by interval length.
        - **Regular Expression Matching `🎯 T2`**
            - Description: Implement regex matching supporting '.' (any single char) and '*' (zero or more of preceding element). Must match the entire string.
            - Pattern: 2D string DP with `*` lookahead
            - Key insight: `p[j-1]=='*'` → either zero copies (`dp[i][j-2]`) or one+ copies if `p[j-2]` matches `s[i-1]` → `dp[i-1][j]`. `'.'` matches any single char.
        - **Combination Sum IV (Ordered Count) `🎯 T2`**
            - Description: Given an array of distinct integers and a target, count the number of ordered combinations (permutations) that sum to target.
            - Pattern: Unbounded Knapsack — but amount is outer loop
            - Key insight: for **ordered** permutations, loop `amount` outer and `items` inner. This is opposite of Coin Change II (unordered combinations). `dp[0]=1`.

---


- [ ] Recursion & Backtracking
    - Alternatives
        - DP: If the same `(start_index, state)` is reached from multiple paths, subproblems overlap. Add memoization → top-down DP. Classic: Word Break.
        - Iteration: Backtracking explores a decision tree. Iterative version requires an explicit stack — extremely complex. Only convert for very deep trees (Python default recursion limit = 1000).
    - Universal Template
        ```python
        def backtrack(path, start, state):
            if is_goal(path, state):
                results.append(path[:])  # copy — never append `path` directly
                return
            for choice in get_choices(start, state):
                if not is_valid(choice, state):
                    continue
                apply(path, state, choice)   # make choice
                backtrack(path, start, state) # recurse
                undo(path, state, choice)    # ← THE #1 BUG: always undo
        ```
    - Key Patterns
        - **Subsets / Combinations:** Use a `start` index — pass `i+1` to prevent going backward. Prevents `[1,2]` and `[2,1]` from both appearing.
        - **Combination Sum (with reuse):** Pass `i` (not `i+1`) to allow reuse of the same element.
        - **Permutations:** No `start` index. Use a `used[]` boolean array to track which elements are in the current path.
        - **Deduplication:** Sort first. In the loop, skip `if i > start and nums[i] == nums[i-1]: continue`. The `i > start` condition ensures we skip at the same recursion level, not across levels.
        - **Grid DFS:** Mark cell visited in-place (`board[r][c] = '#'`) to avoid a separate set. Restore after the recursive call.
        - **Pruning:** Always check feasibility before recursing. If `remaining_sum > sum(remaining_elements)`, return immediately. This is the difference between passing and TLE.
    - Questions — Backtracking `⚡ T1 / 🎯 T2`
        - **Subsets `🎯 T2`**
            - Description: Given an array of distinct integers, return all possible subsets (the power set), including the empty set.
            - Pattern: Include/exclude with `start` index
            - Key insight: record `path[:]` at every node of the tree (not just leaves). `start` index prevents reverse-order duplicates.
        - **Subsets II (with duplicates) `🎯 T2`**
            - Description: Given an array that may contain duplicates, return all unique subsets.
            - Pattern: Same as Subsets + dedup
            - Key insight: sort first; `if i > start and nums[i] == nums[i-1]: continue` skips duplicate siblings.
        - **Permutations `🎯 T2`**
            - Description: Given an array of distinct integers, return all possible permutations.
            - Pattern: `used[]` array, no `start` index
            - Key insight: at each level, try every element not yet `used`. Record path when `len(path) == n`.
        - **Permutations II (with duplicates) `🎯 T2`**
            - Description: Given an array that may contain duplicates, return all unique permutations.
            - Pattern: `used[]` + duplicate skip
            - Key insight: sort first. Skip `if nums[i] == nums[i-1] and not used[i-1]`. The `not used[i-1]` means the previous identical element was NOT used in this branch — so we're at the same recursion level, causing a duplicate.
        - **Combination Sum `🎯 T2`**
            - Description: Given distinct candidates and a target, find all unique combinations where chosen numbers sum to target. Numbers may be reused.
            - Pattern: Combinations, reuse allowed
            - Key insight: pass `i` (not `i+1`) when recursing to allow picking the same element again. Prune when `remaining < 0`.
        - **Combination Sum II `🎯 T2`**
            - Description: Given candidates (may have duplicates) and a target, find all unique combinations summing to target. Each number used at most once.
            - Pattern: Combinations, no reuse, dedup
            - Key insight: sort + skip. Use `i+1` when recursing (no reuse). Skip `if i > start and nums[i] == nums[i-1]`.
        - **N-Queens `🎯 T2`**
            - Description: Place n queens on an n×n chessboard so no two queens attack each other. Return all valid board configurations.
            - Pattern: Constraint satisfaction, sets
            - Key insight: track `cols`, `diag1 (row+col)`, `diag2 (row-col)` as sets. O(1) validity check per cell. Only one queen per row, so recurse row by row.
        - **Word Search `⚡ T1`**
            - Description: Given a 2D grid of characters and a word, determine if the word exists in the grid via adjacent (up/down/left/right) non-revisiting cells.
            - Pattern: Grid DFS + backtrack
            - Key insight: mark `board[r][c] = '#'` in-place before recursing; restore after. If any direction returns True, bubble it up.
        - **Palindrome Partitioning `🎯 T2`**
            - Description: Given string s, return all possible ways to partition it so every substring in the partition is a palindrome.
            - Pattern: Include/exclude + validity guard
            - Key insight: precompute `is_pal[i][j]` in O(N²) so each check is O(1). Without precompute: O(N³). Never skip the precompute step.
        - **Generate Parentheses `⚡ T1`**
            - Description: Given n, generate all combinations of n pairs of well-formed (balanced) parentheses.
            - Pattern: Decision tree with counts
            - Key insight: track `open` and `close` counts. Add `(` if `open < n`; add `)` if `close < open`. Prune all other branches.
        - **Letter Combinations of a Phone Number `🎯 T2`**
            - Description: Given a digit string (2–9), return all possible letter combinations the digits could represent on a phone keypad.
            - Pattern: Cartesian product DFS
            - Key insight: at each digit, branch over all its mapped letters. Empty `digits` input → return `[]` (not `[""]`).
        - **Combinations `🎯 T2`**
            - Description: Given n and k, return all combinations of k numbers chosen from 1 to n.
            - Pattern: `start` index, fixed path length
            - Key insight: stop recursing when `len(path) == k`. Pruning: `if n - start + 1 < k - len(path)`, not enough elements left.
        - **Target Sum `🎯 T2`**
            - Description: Assign + or - to each element of an array. Count the number of ways the expression evaluates to target.
            - Pattern: Include/exclude → also solvable as 0/1 Knapsack
            - Key insight: assign `+` or `-` to each element. Backtrack by trying both. Or reframe as count-subsets-with-sum `(total + target) / 2` using DP.
        - **Word Break II `🎯 T2`**
            - Description: Given string s and a dictionary, return all ways to segment s into a space-separated sequence of dictionary words.
            - Pattern: DFS + memoization
            - Key insight: memoize `start_index → [list of valid sentences]`. Without memo, exponential re-expansion. This is the bridge pattern from backtracking to top-down DP.
        - **Unique Paths III `🎯 T2`**
            - Description: In a grid, start at cell '1', reach cell '2', stepping on every non-obstacle cell exactly once. Count valid paths.
            - Pattern: Grid backtrack + visited counter
            - Key insight: count all non-obstacle empty squares. Only count a path when you reach the target AND all empty squares are visited. Track `remaining_empty` counter — O(1) check.

---

- [ ] Graph Algorithms
    - Alternatives
        - DFS vs BFS: BFS guarantees the shortest path in unweighted graphs. DFS is better for cycle detection, topological sort, and exhaustive enumeration.
        - Dijkstra vs Bellman-Ford: Dijkstra O((V+E) log V) requires non-negative weights. Bellman-Ford O(VE) handles negative weights and detects negative cycles.
        - Union-Find vs DFS: For static connectivity, both work. Union-Find is better for dynamic edge additions (amortized O(α(N)) per operation).
    - Algorithm Selection Table

        | Goal | Algorithm | Complexity |
        |------|-----------|-----------|
        | Unweighted shortest path | BFS | O(V+E) |
        | Non-negative weighted shortest path | Dijkstra + min-heap | O((V+E) log V) |
        | Negative weights / negative cycle detect | Bellman-Ford | O(VE) |
        | All-pairs shortest path | Floyd-Warshall | O(V³) |
        | 0/1 weight edges | 0-1 BFS (deque) | O(V+E) |
        | Topological order / cycle in directed graph | Kahn's (BFS in-degree) | O(V+E) |
        | Connected components (undirected) | DFS / Union-Find | O(V+E) |
        | Minimum spanning tree | Kruskal (sparse) / Prim (dense) | O(E log E) |

    - Critical Gotchas
        - Mark visited BEFORE pushing to BFS queue (not after popping) — otherwise you push the same node multiple times → TLE.
        - Dijkstra lazy deletion guard: `if d > dist[u]: continue` — without this, stale heap entries corrupt results silently.
        - Dijkstra with negative weights produces silently wrong results (not an error). Use Bellman-Ford.
        - For large graphs, convert recursive DFS to iterative with explicit stack — Python's default limit is 1000.
        - Disconnected graphs: always wrap BFS/DFS in an outer loop over all unvisited nodes.
    - Questions — BFS / DFS `⚡ T1 / 🎯 T2`
        - **Number of Islands `⚡ T1`**
            - Description: Given a 2D grid of '1' (land) and '0' (water), count the number of islands (connected components of land, 4-directional).
            - Pattern: DFS/BFS flood-fill, connected components
            - Key insight: for each unvisited `'1'`, run DFS/BFS marking all connected `'1'`s as `'0'`. Count how many times you start. No separate visited set needed — mark in-place.
        - **Clone Graph `⚡ T1`**
            - Description: Given a reference to a node in an undirected connected graph, return a deep copy (clone) of the entire graph.
            - Pattern: DFS/BFS with old→new node map
            - Key insight: memo map `{old_node: new_node}` before recursing into neighbors to handle cycles. Without memo, infinite loop on any cycle.
        - **Pacific Atlantic Water Flow `⚡ T1`**
            - Description: In an m×n height grid, water flows to 4-adjacent cells of equal or lesser height. Find all cells that can flow to both the Pacific (top/left) and Atlantic (bottom/right) ocean.
            - Pattern: Multi-source BFS from borders
            - Key insight: reverse the direction. BFS from all Pacific border cells; BFS from all Atlantic border cells. Return the intersection — cells in both visited sets.
        - **Course Schedule `⚡ T1`**
            - Description: Given numCourses and a list of [course, prerequisite] pairs, determine if it's possible to finish all courses (i.e., no cycle).
            - Pattern: Kahn's topological sort / cycle detection
            - Key insight: build adjacency list; compute in-degrees. BFS from all 0-in-degree nodes. Cycle exists iff `len(order) < n`.
            - Gotcha: edge direction matters. `prereq → course` means course can be taken after prereq.
        - **Course Schedule II `⚡ T1`**
            - Description: Same as Course Schedule, but return one valid ordering of courses to take. Return [] if impossible.
            - Pattern: Kahn's + return order
            - Key insight: same as Course Schedule. If `len(order) == n`, return `order`; else return `[]`.
        - **Word Ladder `⚡ T1`**
            - Description: Given beginWord, endWord, and a word list, find the length of the shortest transformation sequence where each step changes one letter and every intermediate word is in the list.
            - Pattern: BFS (unweighted shortest path)
            - Key insight: each word is a node; edge = one character difference. BFS level = transformation steps. Remove visited words from the set immediately to prevent revisiting.
        - **All Paths From Source to Target `⚡ T1`**
            - Description: Given a DAG, find all paths from node 0 to node n-1. Return them in any order.
            - Pattern: DFS backtracking in a DAG
            - Key insight: DAG means no cycles — no visited set needed. DFS from source; append to results when target reached. Backtrack by popping from path.
        - **Is Graph Bipartite `⚡ T1`**
            - Description: Given an undirected graph, determine if it can be 2-colored (bipartite) — i.e., no edge connects two same-colored nodes.
            - Pattern: BFS 2-coloring
            - Key insight: alternate colors `1 - current_color` for neighbors. If a neighbor already has the same color → not bipartite. Handle disconnected graphs with outer loop.
        - **Alien Dictionary `⚡ T1`**
            - Description: Given a sorted list of alien-language words, derive the character ordering of the alien alphabet. Return '' if invalid.
            - Pattern: Kahn's topological sort on characters
            - Key insight: compare adjacent words to find the first mismatch → directed edge between those characters. Run Kahn's. Return `""` if cycle detected OR if `word1` is a prefix-violated prefix of `word2`.
        - **Network Delay Time (Dijkstra) `🎯 T2`**
            - Description: Given a directed weighted graph, a source k, and n nodes, find how long it takes for a signal to reach all nodes. Return -1 if unreachable.
            - Pattern: Dijkstra SSSP
            - Key insight: find `max(dist.values())`. If any node unreachable (`dist[v] == inf`), return -1.
        - **Cheapest Flights Within K Stops `🎯 T2`**
            - Description: Given flights with costs, find the cheapest price from src to dst using at most k stops. Return -1 if no route.
            - Pattern: Modified Bellman-Ford (K+1 iterations)
            - Key insight: run exactly K+1 relaxations. Use a COPY of the distance array each iteration — prevents using more edges than allowed in one pass. Standard Dijkstra doesn't work because stop-count must be bounded.
        - **Redundant Connection `🎯 T2`**
            - Description: Given an undirected tree with one extra edge added (creating a cycle), find and return that redundant edge.
            - Pattern: Union-Find
            - Key insight: process edges one by one. The first edge where both endpoints are already in the same component creates the cycle — that's the redundant edge. Return the last one if multiple.
        - **Accounts Merge `🎯 T2`**
            - Description: Given a list of accounts [name, emails...], merge accounts sharing at least one email. Return sorted merged accounts.
            - Pattern: Union-Find on emails
            - Key insight: for each account, union all emails with the first email. After all unions, group emails by their root. Sort each group and prepend the account name.
        - **Graph Valid Tree `🎯 T2`**
            - Description: Given n nodes and a list of undirected edges, determine if the edges form a valid tree (connected, no cycles).
            - Pattern: Union-Find + edge count
            - Key insight: a valid tree has exactly `n-1` edges and no cycles. Check edge count first; then use Union-Find — if any edge creates a cycle, return False.

---

- [ ] Greedy
    - Alternatives
        - DP: Greedy makes irrevocable local choices (O(N log N)). DP considers all choices (O(N²) typical). If you can construct a counterexample for greedy, use DP immediately.
        - Backtracking: Use when no greedy or DP structure exists and all valid configurations are needed.
    - When Greedy is Correct — The Exchange Argument
        - The **Greedy Choice Property** must hold: the locally optimal choice is always part of some globally optimal solution.
        - **Exchange Argument:** Take any optimal solution O that doesn't make the greedy choice at step 1. Show you can swap the greedy choice into O without worsening it. By induction, full greedy solution = optimal.
        - Classic greedy failures: coin change with non-canonical denominations `{1,3,4}` for target 6 — greedy gives 3 coins (`4+1+1`), DP gives 2 (`3+3`). The local choice blocked the global optimum.
    - Key Patterns
        - **Interval Scheduling — Sort by End Time:** Greedily pick the earliest-ending interval. This keeps maximum future slots open. Sorting by start time is wrong — construct a counterexample instantly.
        - **Coverage Problems — Sort by Start, Track Farthest:** Sort by start; always pick the interval that extends coverage the furthest from the current boundary.
        - **Jump Game — Track Farthest Reachable:** Iterate; if `i > farthest`, position is unreachable → return False. Otherwise `farthest = max(farthest, i + nums[i])`.
        - **Gas Station — Circular Feasibility:** If `sum(gas) >= sum(cost)`, a valid start always exists. The valid start = first position after the longest deficit prefix.
        - **Task Scheduler — Formula:** `max((max_freq - 1) * (n + 1) + count_with_max_freq, len(tasks))`. The `max(..., len(tasks))` cap handles when task variety fills all idle slots.
    - Gotchas
        - Interval overlap boundary: "Minimum Arrows" uses strict `>` (touching counts as one shot). "Non-overlapping Intervals" uses `<` (touching is NOT overlapping). One character difference — watch the `>` vs `>=`.
        - Task Scheduler: always apply the `max(formula, len(tasks))` cap — forgetting it fails when there's enough task variety.
        - Gas Station: the problem guarantees a unique valid start only when `sum(gas) >= sum(cost)`.
    - Questions — Greedy `⚡ T1 / 🎯 T2`
        - **Jump Game I `🎯 T2`**
            - Description: Given an array where nums[i] is the max jump from index i, determine if you can reach the last index.
            - Pattern: Single-pass reach tracking
            - Key insight: track `farthest`. If `i > farthest`, current position is unreachable → return False. Update `farthest = max(farthest, i + nums[i])` at each step. O(N).
        - **Jump Game II `🎯 T2`**
            - Description: Given an array where nums[i] is the max jump from index i (always reachable), return the minimum number of jumps to reach the last index.
            - Pattern: Greedy BFS levels
            - Key insight: treat as BFS levels. When `i == current_end`, you must make a jump → `jumps += 1`, `current_end = farthest`. Stop loop at `len(nums) - 2` (no need to jump from last).
        - **Gas Station `🎯 T2`**
            - Description: n gas stations in a circle with gas[i] available and cost[i] to travel to next. Find the starting station index to complete the circuit, or -1.
            - Pattern: Running deficit reset
            - Key insight: if `sum(gas) < sum(cost)`, return -1. Otherwise, reset `start = i + 1` whenever `tank < 0`. The unique valid start is after the last negative prefix.
        - **Task Scheduler `⚡ T1`**
            - Description: Given tasks (letters) and cooldown n (same task needs n intervals gap), find minimum total time to finish all tasks.
            - Pattern: Frequency formula
            - Key insight: `(max_freq - 1) * (n + 1) + count_max`. `max(formula, len(tasks))` handles the case where task variety fills all idle slots.
        - **Partition Labels `🎯 T2`**
            - Description: Partition string s into as many parts as possible so each letter appears in at most one part. Return list of part lengths.
            - Pattern: Last-occurrence greedy sweep
            - Key insight: precompute `last[ch]` = last index of each character. Sweep: `end = max(end, last[ch])`. When `i == end`, cut the partition.
        - **Merge Intervals `⚡ T1`**
            - Description: Given a collection of intervals, merge all overlapping intervals and return the result.
            - Pattern: Sort by start, merge overlapping
            - Key insight: sort by start. If current interval starts before previous end → merge by extending end. Else push current.
        - **Non-overlapping Intervals `🎯 T2`**
            - Description: Given intervals, remove the minimum number of intervals so the rest are non-overlapping.
            - Pattern: Sort by end, count removals
            - Key insight: sort by end. Greedily keep non-overlapping (pick earliest-ending). Removals = total - kept. Return `total - kept`.
        - **Meeting Rooms II `🎯 T2`**
            - Description: Given meeting time intervals, find the minimum number of conference rooms required.
            - Pattern: Min-heap of end times
            - Key insight: sort by start. Use a min-heap of end times of active meetings. If the next meeting starts after the earliest ending meeting, reuse that room (pop and push new end). Else, open a new room. Answer = heap size.
        - **Minimum Arrows to Burst Balloons `🎯 T2`**
            - Description: Balloons are represented by [x_start, x_end]. Find minimum arrows shot straight up (at any x) to burst all balloons.
            - Pattern: Sort by end
            - Key insight: sort balloons by end. Place arrow at `end` of first balloon. A new arrow is needed only when next balloon's `start > current arrow position`. Strict `>`.
        - **3Sum Closest `🎯 T2`**
            - Description: Given an integer array and target, find the triplet whose sum is closest to target. Return the sum.
            - Pattern: Sort + converging two pointers
            - Key insight: sort. Fix anchor `i`; converging inner pointers. Track `abs(sum - target)`. Update best when closer. Move pointers based on sum vs target direction.
        - **IPO (Maximize Capital) `⚡ T1`**
            - Description: Given k projects each with a profit and minimum capital requirement, find max capital starting with w capital after completing at most k projects.
            - Pattern: Two-structure greedy (sorted array + max-heap)
            - Key insight: sort projects by capital. For each of K rounds: unlock all affordable projects into a max-heap of profits. Pop the highest profit. Repeat.

---

- [ ] Divide & Conquer / Math
    - Alternatives
        - Linear DP: Merge Sort / inversions can be solved with D&C in O(N log N) vs O(N²) for DP.
        - Heap: "Merge K sorted lists" is O(N log K) with a heap — same complexity as D&C but simpler to code.
    - Key Techniques
        - **D&C Template:** Split into halves; recurse; merge. The merge step usually does the real work (e.g., count inversions during merge, not split).
        - **Fast Exponentiation:** `x^n` in O(log N). `x^n = (x^(n//2))^2` if n even; `x * x^(n-1)` if odd. Handle `n < 0` by computing `(1/x)^(-n)`.
        - **Modulo Arithmetic:** `(a * b) % MOD` at every step to prevent overflow. `(a + b) % MOD`. For subtraction: `(a - b + MOD) % MOD`.
        - **GCD / LCM:** `gcd(a, b) = gcd(b, a % b)`. `lcm(a, b) = a * b // gcd(a, b)`.
        - **Happy Number:** Sum of squares of digits. Cycle detection → use fast/slow pointers or a set. Terminates at 1 (happy) or enters a cycle (not happy).
    - Questions — D&C / Math `⚡ T1 / 🎯 T2`
        - **Pow(x, n) `🎯 T2`**
            - Description: Implement pow(x, n) — raise x to the power n — efficiently. Handle negative exponents.
            - Pattern: Fast exponentiation
            - Key insight: `x^n = (x^(n//2))^2`. Handle `n < 0`: return `(1/x)^(-n)`. O(log N).
        - **Maximum Subarray `⚡ T1`**
            - Description: Find the contiguous subarray (at least one element) with the largest sum and return its sum.
            - Pattern: Kadane's algorithm (also solvable with D&C)
            - Key insight: `ending_here = max(nums[i], ending_here + nums[i])`. `global_max = max(global_max, ending_here)`. O(N) O(1).
        - **Merge K Sorted Lists `🎯 T2`**
            - Description: Merge k sorted linked lists into one sorted linked list and return it.
            - Pattern: D&C (or heap)
            - Key insight: D&C: pair up lists and merge pairs, repeat. O(N log K). Heap: push first node of each list into a min-heap; always pop the smallest and push its successor.
        - **Happy Number `🎯 T2`**
            - Description: A number is happy if repeatedly replacing it with the sum of squares of its digits eventually reaches 1. Determine if n is happy.
            - Pattern: Cycle detection (fast/slow or set)
            - Key insight: repeatedly replace `n` with sum of squares of its digits. If `n == 1` → happy. If you enter a cycle → not happy. Fastest: use a set to detect revisit.
        - **Reverse Integer `🎯 T2`**
            - Description: Given a 32-bit signed integer, return it with its digits reversed. Return 0 if the reversed integer overflows.
            - Pattern: Math / modulo
            - Key insight: build reversed number via `rev = rev * 10 + digit`. Check overflow at each step (Python: check against `2^31 - 1` range).

---

## Sorting (Reference)

`🎯 T2` — Know complexity and stability. Never implement from scratch in a live interview unless explicitly asked — just call `sorted()` and explain what's happening underneath.

| Algorithm | Best | Average | Worst | Space | Stable? | When to Use |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Merge Sort | O(N log N) | O(N log N) | O(N log N) | O(N) | Yes | LL sort; external sort; stable order needed |
| Quick Sort | O(N log N) | O(N log N) | O(N²) | O(log N) | No | In-place, cache-friendly; avoid if worst-case matters |
| Heap Sort | O(N log N) | O(N log N) | O(N log N) | O(1) | No | In-place O(1) space; not cache-friendly |
| Counting Sort | O(N+K) | O(N+K) | O(N+K) | O(K) | Yes | Integer keys with bounded range K |
| Radix Sort | O(N·d) | O(N·d) | O(N·d) | O(N+K) | Yes | Large integer keys; d = number of digits |
| Tim Sort | O(N) | O(N log N) | O(N log N) | O(N) | Yes | Python/Java default; hybrid merge+insertion |

**Gotchas:**
- `sorted()` in Python uses Tim Sort — stable O(N log N). In-place: `list.sort()`.
- Custom key: `sorted(items, key=lambda x: x[1])` — never compare tuples directly if elements non-comparable.
- Counting sort requires bounded, non-negative integer keys — ask about key range before proposing it.
- Quick sort worst case O(N²) on sorted/reverse-sorted input — mention random pivot or 3-way partition.

### QuickSelect — O(N) Average Kth Order Statistic

**Click Moment**: \"Kth largest/smallest without full sort\" or \"can you do better than O(N log N)?\"

```python
def find_kth_largest(nums, k):
    import random; random.shuffle(nums)  # prevent O(N²) worst case
    target = len(nums) - k  # k-th largest = (n-k)-th smallest (0-indexed)
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        pivot = nums[hi]; i = lo
        for j in range(lo, hi):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]; i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        if i == target: break
        elif i < target: lo = i + 1
        else: hi = i - 1
    return nums[target]
```

> **Gotcha**: QuickSelect mutates the input array. Mention this to the interviewer. O(N) average, O(N²) worst without shuffling.

### Sorting Questions

| Problem | Pattern | Key Insight | Tier |
| :--- | :--- | :--- | :--- |
| **Sort Colors (Dutch National Flag)** | 3-pointer: `lo, mid, hi` | Swap 0→lo++, 1→mid++, 2→hi--; do NOT increment mid after swap with hi | `⚡ T1` |
| **Kth Largest Element in Array** | QuickSelect OR Min-Heap K | QuickSelect O(N) avg; min-heap O(N log K) streaming-safe; mention both | `⚡ T1` |
| **Largest Number** | Custom Comparator | `cmp_to_key(lambda a,b: 1 if a+b < b+a else -1)`; check all-zeros: `[0,0]→"0"` | `🎯 T2` |
| **Russian Doll Envelopes** | Sort w asc + h desc + LIS | Height sort descending prevents same-width stacking; `bisect_left` for O(N log N) LIS | `🎯 T2` |
| **Maximum Gap** | Bucket Sort / Pigeonhole | Gap must cross at least one empty bucket; n-1 buckets of size `ceil((max-min)/(n-1))` | `🎯 T2` |
| **H-Index** | Sort Descending | Find largest i where `citations[i] >= i+1`; or bucket sort O(N) | `🎯 T2` |
| **3Sum Closest** | Sort + Converging Two Pointers | Fix anchor; converging inner pointers; track `abs(sum-target)` | `🎯 T2` |

---

## Advanced Graphs

`🎯 T2` — Algorithms needed when BFS/DFS/Dijkstra are insufficient. Know the trigger; the click moment is more important than memorising the full implementation at L3.

### Algorithm Selection

| Problem Type | Algorithm | Complexity | Trigger |
| :--- | :--- | :--- | :--- |
| Negative edge weights / K-hops bound | Bellman-Ford | O(VE) | \"negative weights\"; \"at most K stops\" |
| All-pairs shortest paths | Floyd-Warshall | O(V³) | \"all pairs\"; N ≤ 500; transitive closure |
| Traverse every edge exactly once | Hierholzer's (Eulerian Path) | O(V+E) | \"use every ticket once\"; \"draw without lifting pen\" |
| Critical edges (network robustness) | Tarjan Bridges | O(V+E) | \"remove one edge, network splits\" |
| Strongly connected components | Kosaraju / Tarjan SCC | O(V+E) | \"groups where every node reaches every other\" |

### Key Techniques

**Bellman-Ford (Bounded Relaxations)**
- Relax all edges exactly K+1 times. Use a **snapshot copy** of the distance array each round — prevents cascading updates within a single round (critical for K-stops problems).
- Negative cycle detection: if Nth round still relaxes → cycle exists. Dijkstra cannot detect this.

**Floyd-Warshall**
- `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])`. K is the **outermost** loop. Init: `dp[i][j] = inf` unless direct edge; `dp[i][i] = 0`. Only for N ≤ 500.

**Hierholzer's Eulerian Path**
- Sort adjacency lists in reverse; use `.pop()` for lexicographic order. Post-order DFS: **add node to result only after all edges exhausted**. Reverse result at end.
- Existence (directed): out−in = +1 (start), in−out = +1 (end), all others balanced.

**Tarjan Bridges**
- Track `disc[]` and `low[]`. Edge `(u,v)` is a bridge when `low[v] > disc[u]`. Multi-edges: track parent **edge index**, not node.

### Gotchas

- **Bellman-Ford copy**: without copying dist each round, updates from the same round cascade → wrong K-stops answer.
- **Floyd-Warshall loop order**: k must be outermost. `dp[i][k]` and `dp[k][j]` must be finalised before computing `dp[i][j]` through k.
- **Hierholzer's post-order**: naive pre-order DFS incorrectly dead-ends. Only post-order (append after while loop) works.
- **Bridges vs undirected back-edge**: always track parent node (or edge index for multi-graphs) to avoid `u→v→u` being counted as a cycle.

### Questions

| Problem | Pattern | Key Insight | Tier |
| :--- | :--- | :--- | :--- |
| **Cheapest Flights Within K Stops** | Bellman-Ford K+1 rounds | Snapshot each round; Dijkstra fails (stop count not respected by greedy expansion) | `⚡ T1` |
| **Reconstruct Itinerary** | Hierholzer's Eulerian Path | Sort reverse + `.pop()`; post-order DFS; reverse result | `⚡ T1` |
| **Word Ladder II** | BFS layered + backtrack | Process full BFS layer before removing words from set; build parent map; DFS backtrack | `⚡ T1` |
| **Evaluate Division** | Weighted directed graph + BFS | Edge weight = ratio; product along DFS/BFS path = answer; -1 if unreachable or unknown var | `⚡ T1` |
| **Critical Connections (Bridges)** | Tarjan bridge DFS | `low[v] > disc[u]` = bridge; multi-edge: track parent edge index not node | `🎯 T2` |
| **Network Delay Time** | Dijkstra SSSP | `max(dist.values())`; -1 if `len(dist) < n` (unreachable nodes) | `🎯 T2` |
| **Swim in Rising Water** | Dijkstra or Binary Search+BFS | `dist[r][c]` = min max-elevation on path; looks like BFS but needs min-of-max | `🎯 T2` |
| **Find the City (Floyd-Warshall)** | All-pairs shortest path | N ≤ 100; count neighbors with `dist ≤ threshold`; prefer Floyd over V×Dijkstra | `🎯 T2` |
| **Path With Minimum Effort** | Dijkstra (minimise max edge) | `dist[node]` = min effort to reach; edge weight = `abs(h1-h2)` | `🎯 T2` |
| **Minimum Cost to Connect All Points** | Kruskal's MST | Generate all N²/2 edges sorted by Manhattan dist; DSU | `🎯 T2` |
| **Detect Negative Cycle** | Bellman-Ford Nth round | If Nth relaxation still updates → negative cycle; Dijkstra cannot detect | `💤 T3` |
| **SCC (Kosaraju/Tarjan)** | Two-pass DFS / disc+low | Directed graph groups where every node reaches every other | `💤 T3` |

---

## Union-Find (DSU)

`🎯 T2` — Disjoint Set Union: O(α(N)) amortized per operation with path compression + union by rank. The go-to for dynamic connectivity, Kruskal's MST, and redundant edge detection.

### Core Implementation

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # already connected — this edge is redundant
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

### Key Patterns

| Pattern | How |
| :--- | :--- |
| **Connected components count** | `uf.components` after all unions |
| **Redundant edge (cycle detection)** | `union()` returns `False` on first cycle-creating edge |
| **Kruskal's MST** | Sort edges by weight; `union(u, v)` if not connected; stop at N-1 edges |
| **Accounts merge / email grouping** | Union all emails in same account; group by root |
| **Grid connectivity (implicit graph)** | Encode `(r, c)` as `r * cols + c`; union 4-dir neighbors |

### Gotchas
- **Always call `find()` for path compression** — accessing `parent[x]` directly bypasses compression and gives O(N) worst case.
- **Union by rank, not arbitrary** — always attach smaller rank tree under larger rank tree to keep tree height O(log N).
- **`union()` returns False on same-component** — use this return value to detect cycles (Redundant Connection).

### Questions

| Problem | Pattern | Key Insight | Tier |
| :--- | :--- | :--- | :--- |
| **Number of Connected Components** | DSU component count | `uf.components` after all `union()` calls | `🎯 T2` |
| **Redundant Connection** | Cycle via DSU | First edge where `union()` returns False = redundant | `⚡ T1` |
| **Graph Valid Tree** | DSU + edge count | Valid tree: exactly N-1 edges AND no cycle (all unions return True) | `🎯 T2` |
| **Accounts Merge** | DSU on emails | Union all emails in same account; group by root; sort+prepend name | `🎯 T2` |
| **Kruskal's MST** | DSU + sort edges | Sort by weight; union if not connected; stop at N-1 edges | `🎯 T2` |
| **Smallest String With Swaps** | DSU on indices | Group indices in same component; sort characters per component; rebuild | `💤 T3` |

---

## Bit Manipulation

`🎯 T2` — Direct binary operations. O(1) per operation. Critical for space optimization, XOR tricks, and mask-based DP.

### Core Operations Reference

| Operation | Python | Use |
| :--- | :--- | :--- |
| Check bit k | `(n >> k) & 1` | Is bit k set? |
| Set bit k | `n \| (1 << k)` | Force bit k to 1 |
| Clear bit k | `n & ~(1 << k)` | Force bit k to 0 |
| Toggle bit k | `n ^ (1 << k)` | Flip bit k |
| Remove lowest set bit | `n & (n - 1)` | Brian Kernighan: count set bits in O(popcount) |
| Isolate lowest set bit | `n & (-n)` | Used in Fenwick Tree (BIT) |
| Check power of 2 | `n > 0 and (n & (n-1)) == 0` | Exactly one bit set |
| Count set bits | `bin(n).count('1')` or `n.bit_count()` | Python 3.10+ |
| XOR all in range [1..n] | Pattern cycles 4: n, 1, n+1, 0 | XOR 1 to N without loop |

### Key Patterns

| Pattern | How |
| :--- | :--- |
| **XOR cancel pairs** | `a ^ a = 0`; XOR all elements — duplicates cancel; single remains | Single Number I |
| **XOR find two singles** | XOR all — get `x ^ y`; isolate any differing bit; partition and XOR each group | Single Number III |
| **Enumerate subsets of mask** | `sub = mask; while sub: ...; sub = (sub-1) & mask` | Bitmask DP over subsets |
| **DP over bitmasks** | State = visited set of nodes encoded as bitmask; O(2^N · N) | TSP, Hamiltonian path |
| **XOR Trie** | Binary Trie on bits MSB→LSB; greedily pick opposite bit to maximize XOR | Maximum XOR pair |

### Gotchas
- **Python integers are arbitrary-precision** — no overflow, but simulate 32-bit with `n & 0xFFFFFFFF` if the problem requires fixed-width behavior.
- **Right shift of negative in Java/C++ is arithmetic** (sign-extended); use `>>>` for logical right shift in Java.
- **`n & (n-1)` removes lowest set bit** — memorize this; it's the building block of Brian Kernighan's bit count.
- **Bitmask DP state space**: 2^N grows fast; only viable for N ≤ 20.

### Questions

| Problem | Pattern | Key Insight | Tier |
| :--- | :--- | :--- | :--- |
| **Single Number I** | XOR cancel | `reduce(xor, nums)` — all duplicates cancel; single remains | `⚡ T1` |
| **Single Number II** | Bit count mod 3 | Count each bit across all numbers; if `bit_count % 3 != 0`, that bit is in the single | `⚡ T1` |
| **Single Number III** | XOR + partition | XOR all to get `x^y`; find any differing bit; partition on it; XOR each group | `🎯 T2` |
| **Number of 1 Bits (Hamming Weight)** | `n & (n-1)` loop | Each iteration removes lowest set bit; count iterations | `🎯 T2` |
| **Counting Bits** | DP + lowest bit | `dp[i] = dp[i >> 1] + (i & 1)` — O(N) | `🎯 T2` |
| **Reverse Bits** | Shift + OR | Shift result left, OR in LSB of n, shift n right; 32 iterations | `🎯 T2` |
| **Missing Number** | XOR or Gauss | XOR `0..n` with all elements; missing is what's left. Or: `n*(n+1)//2 - sum(nums)` | `🎯 T2` |
| **Sum of Two Integers (No +/-)** | XOR + carry | `a ^ b` = sum without carry; `(a & b) << 1` = carry; repeat until carry = 0 | `🎯 T2` |
| **Maximum XOR of Two Numbers** | XOR Trie | Binary trie bits MSB→LSB; greedily choose opposite bit at each level | `⚡ T1` |
| **Subsets via Bitmask** | Enumerate 2^N masks | For each mask in `0..2^N-1`, bit k set = include nums[k] | `🎯 T2` |

---

## Intervals

`🎯 T2` — Sort then sweep. Interval problems are greedy once you sort. The boundary condition (`>` vs `>=`) is the single most common bug.

### Core Patterns

| Pattern | Sort By | Key Decision | Problem |
| :--- | :--- | :--- | :--- |
| **Merge intervals** | Start time | Merge if `curr_start <= prev_end`; extend `prev_end = max(prev_end, curr_end)` | Merge Intervals |
| **Min rooms / resources** | Start time | Min-heap of end times; pop if `heap[0] <= curr_start`; heap size = rooms needed | Meeting Rooms II |
| **Remove fewest for no overlap** | End time | Greedily keep earliest-ending; skip overlapping | Non-overlapping Intervals |
| **Shoot fewest arrows** | End time | Arrow at `curr_end`; new arrow only when `next_start > curr_end` (strict `>`) | Min Arrows to Burst |
| **Insert interval** | — | Find non-overlapping left side, merge overlapping, append right side | Insert Interval |
| **Coverage / jump** | Start time | Sort; track farthest reachable; count jumps when boundary crossed | Jump Game II |

### Gotchas

> [!CAUTION]
> **`>` vs `>=` boundary is the #1 interval bug.** "Non-overlapping Intervals" uses `>=` (touching = overlapping). "Minimum Arrows" uses `>` (touching = same arrow covers both). Verify with one example before coding.

- **Meeting Rooms II**: sort by start; use min-heap of end times. If earliest-ending meeting ends before current starts, reuse that room (pop and push new end). Heap size = answer.
- **Insert Interval**: don't sort — input is already sorted. Three phases: copy all non-overlapping left intervals, merge all overlapping, copy remaining right intervals.
- **Merge Intervals**: sort by start. Extend `prev_end = max(prev_end, curr_end)` (not just `curr_end`) to handle fully contained intervals like `[1,10]` and `[2,3]`.

### Questions

| Problem | Pattern | Key Insight | Tier |
| :--- | :--- | :--- | :--- |
| **Merge Intervals** | Sort by start + sweep | Extend `prev_end = max(prev_end, curr_end)` for contained intervals | `⚡ T1` |
| **Insert Interval** | Three-phase scan | Phase 1: copy non-overlapping left; Phase 2: merge overlapping into new; Phase 3: copy right | `⚡ T1` |
| **Non-overlapping Intervals** | Sort by end, count removals | Greedily keep earliest-ending; `removals = total - kept` | `🎯 T2` |
| **Meeting Rooms I** | Sort by start | If any `intervals[i].start < intervals[i-1].end` → False | `🎯 T2` |
| **Meeting Rooms II** | Sort by start + min-heap | Pop if `heap[0] <= curr.start`; heap size = min rooms | `🎯 T2` |
| **Minimum Arrows to Burst Balloons** | Sort by end, strict `>` | Arrow at `curr_end`; new arrow only when `next_start > curr_end` | `🎯 T2` |
| **Employee Free Time** | Merge all intervals | Collect all intervals; sort; merge; gaps between merged = free time | `💤 T3` |

---

## ⚡ Quick Pattern Triggers — Algorithms

> Read this the morning of your interview. One-line recognition drills.

| If you see... | Algorithm | Critical detail |
| :--- | :--- | :--- |
| "Shortest path" in unweighted graph | BFS | Mark visited before enqueue |
| "Shortest path" weighted, no negatives | Dijkstra | Skip stale: `if d > dist[u]: continue` |
| "Negative edge weights" | Bellman-Ford K+1 rounds | Use copy of dist array each round |
| "Order tasks / prerequisites" | Kahn's Topo Sort | Cycle ⇔ `len(order) < n` |
| "Maximize/minimize with feasibility" | Binary search on answer | Write `feasible(mid)`; min: `hi=mid` on feasible |
| "Partition + pick items once" | 0/1 Knapsack | Inner loop W **backward** |
| "Partition + reuse items" | Unbounded Knapsack | Inner loop W **forward** |
| "Two sequences — align & match" | LCS DP | `dp[i][j] = dp[i-1][j-1] + 1` on match |
| "All valid configurations / subsets" | Backtracking | `undo` after recurse; copy path at goal |
| "Locally optimal = globally optimal" | Greedy | Prove with exchange argument |
| "Sorted array, find target" | Binary Search `lo <= hi` | `mid = lo + (hi-lo)//2` prevents overflow |
| "Connected components / cycle in undirected" | Union-Find | `union()` returns False on first cycle |
| "XOR pair / single number" | XOR + bit trick | `a^a=0`; `a^0=a`; XOR all → singles survive |
| "Touching interval boundary" | Greedy — sort by end | `>` vs `>=` — verify with one example |
| "Count inversions / merge" | Merge Sort D&C | Count during merge step, not split |
| "All paths" in a DAG | DFS backtrack, no visited set | DAG → no cycles → no infinite loops |
| "State machine (hold / sell / cooldown)" | DP with states | Track all states at each step simultaneously |

---

## L3 Must-Solve Problems (algorithms)

Solve these **cold** before your loop.

| # | Problem | Topic | Pattern |
| :- | :--- | :--- | :--- |
| 1 | Two Sum II (Sorted) | Two Pointers | Converging |
| 2 | 3Sum | Two Pointers | Sort + converging + dedup |
| 3 | Container With Most Water | Two Pointers | Move shorter side |
| 4 | Trapping Rain Water | Two Pointers / Stack | Two-pointer or monotonic stack |
| 5 | Minimum Window Substring | Sliding Window | Variable window + freq map |
| 6 | Sliding Window Maximum | Sliding Window | Monotonic deque |
| 7 | Binary Search (exact) | Binary Search | `lo <= hi` template |
| 8 | Search in Rotated Array | Binary Search | Determine sorted half first |
| 9 | Koko Eating Bananas | Binary Search | BS on answer + `feasible()` |
| 10 | Climbing Stairs | DP | Linear / Fibonacci |
| 11 | Coin Change I | DP | Unbounded Knapsack — minimize |
| 12 | Word Break | DP | Linear DP + HashSet |
| 13 | Longest Common Subsequence | DP | LCS 2D table |
| 14 | Maximal Square | DP | Grid DP — `min(up, left, diag) + 1` |
| 15 | Subsets | Backtracking | Include/exclude + `start` index |
| 16 | Combination Sum | Backtracking | Reuse allowed — pass `i` |
| 17 | Word Search | Backtracking | Grid DFS + in-place mark |
| 18 | Generate Parentheses | Backtracking | Count `open`/`close`; prune |
| 19 | N-Queens | Backtracking | Constraint sets `cols, diag1, diag2` |
| 20 | Course Schedule | Graph | Kahn's topo sort |
| 21 | Word Ladder | Graph | BFS on implicit graph |
| 22 | Pacific Atlantic Water Flow | Graph | Reverse BFS from borders |
| 23 | Redundant Connection | Union-Find | First cycle-creating edge |
| 24 | Cheapest Flights K Stops | Advanced Graph | Bellman-Ford K+1 rounds |
| 25 | Merge Intervals | Greedy | Sort + sweep |
| 26 | Insert Interval | Greedy | Three-phase scan |
| 27 | Task Scheduler | Greedy | Freq formula |
| 28 | Maximum Subarray | D&C / Kadane | Reset on negative |

> **Mock cadence:** Weeks 3-4, do **2 timed mocks per week** (35 min, one problem, talk out loud).

---

*See individual topic sections above for full patterns, gotchas, and complexity analysis.*
