# Dynamic Programming — SDE-3 Gold Standard

Solve optimization problems by breaking them into **overlapping subproblems** with **optimal substructure**; store solutions to avoid recomputation. SDE-3 expects: recurrence derivation from scratch, space optimization, and knowing when DP is wrong.

---

## Theory & Mental Models

**What it is.** Dynamic Programming solves problems with overlapping subproblems by storing subproblem results — trading space for time to avoid recomputation. Core invariant: two properties must hold — **optimal substructure** (the optimal solution contains optimal sub-solutions) and **overlapping subproblems** (the same subproblems arise from multiple distinct recursive calls).

**Why it exists.** Naive recursion on problems with overlapping subproblems is exponential (Fibonacci: O(2^N)); DP reduces this to polynomial by solving each unique subproblem exactly once. DP is "careful brute force" — enumerate all possibilities, but cache intermediate results.

**The mental model.** DP is careful brute force: enumerate all possibilities but cache intermediate results so each subproblem is solved only once. Two approaches: top-down (memoization: recursion + cache) and bottom-up (tabulation: fill a table iteratively from base cases). Top-down is easier to derive; bottom-up is cache-friendlier and avoids recursion limits.

**Complexity at a glance.**

| DP Type | Typical States | Typical Transition | Space Optimization |
| :--- | :--- | :--- | :--- |
| Linear 1D | O(N) | O(1) per state | O(1) with two variables |
| 2D grid / string | O(N × M) | O(1) per state | O(min(N, M)) rolling array |
| Knapsack | O(N × W) | O(1) per state | O(W) single row |
| Interval DP | O(N²) | O(N) per state (try all k) | Rarely reducible |
| Bitmask DP (N ≤ 20) | O(2^N × N) | O(N) per state | Rarely reducible |

**When to reach for it.**
- "Count ways", "minimum / maximum cost", "is it possible" — classic DP signals.
- Sequences with choices at each step: knapsack, LCS, edit distance, coin change.
- Game theory: optimal play by both players.
- Any problem where brute-force recursion revisits the same `(args)` multiple times.

**When NOT to use it.**
- Greedy works — if the greedy choice property holds, DP is slower and unnecessary.
- State space is too large — bitmask DP requires N ≤ 20; 2D DP on N = 10^4 × M = 10^4 is infeasible.
- Subproblems don't overlap — use divide and conquer instead.

**Common mistakes.**
- Wrong state definition — missing a dimension (e.g., forgetting the "number of items used" dimension in bounded knapsack).
- Incorrect base case — one wrong base case cascades to all subsequent states.
- Confusing 0-indexed vs 1-indexed DP table — causes off-by-one on string indexing.
- Not recognizing that O(N²) DP can be optimized to O(N log N) (e.g., LIS via patience sort with bisect).
- Forgetting to take modulo in count problems — results overflow silently.

---

## 1. The Four-Step Framework

> [!IMPORTANT]
> **Before writing a single line of code, answer all four questions out loud. Interviewers at Google evaluate whether you can derive a recurrence — not just recall one.**

1. **Define the state**: What does `dp[i]` (or `dp[i][j]`) represent? Be explicit. E.g., "dp[i] = maximum profit using items 0..i".
2. **Write the recurrence**: How does `dp[i]` depend on previous states? The recurrence *is* the algorithm.
3. **Identify base cases**: The smallest subproblems that need no recursion (e.g., `dp[0] = 0`).
4. **Choose traversal order**: Must you fill left-to-right, bottom-up, or can states be computed independently?

```
State → Recurrence → Base Cases → Order → Space Optimize
```

---

## 2. Core Patterns & Click Moments

### Linear DP (1D)

> [!IMPORTANT]
> **The Click Moment**: "Ways to reach N" — OR — "max gain using items in sequence" — OR — "dependency on the **previous 1 or 2 states** only". If you can express `dp[i]` using only `dp[i-1]` and `dp[i-2]`, you can always space-optimize to O(1) using two variables.

- **Examples**: Fibonacci, Climbing Stairs, House Robber.

```python
def house_robber(nums: list[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev2, prev1 = 0, 0
    for val in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + val)
    return prev1

#### Common Variants & Twists
1. **Decode Ways**:
   - **What (The Problem & Goal):** Given a digit string, count the number of ways to decode it (A=1..Z=26).
   - **How (Intuition & Mental Model):** This is a Fibonacci variant. `dp[i]` depends on `dp[i-1]` (if `s[i]` is valid) and `dp[i-2]` (if `s[i-1:i+1]` is valid). Handle the '0' cases (leading zero or solo zero) carefully.
2. **Min Cost For Tickets**:
   - **What (The Problem & Goal):** Given travel days and costs for 1-day, 7-day, and 30-day passes, find the minimum cost to travel all days.
   - **How (Intuition & Mental Model):** `dp[i] = min(dp[i-1] + cost[1d], dp[i-7] + cost[7d], dp[i-30] + cost[30d])`. If `i` is not a travel day, `dp[i] = dp[i-1]`.
```

> [!TIP]
> Space optimization rule: if `dp[i]` depends only on `dp[i-1]` and `dp[i-2]`, replace the entire array with two variables. If it depends on `dp[i-1][j]` for all j (2D), replace the full 2D table with a single 1D rolling array.

---

### Knapsack — 0/1 and Unbounded

> [!IMPORTANT]
> **The Click Moment**: "Limited **capacity** or **budget**" — AND — "choose which items to take". **0/1**: each item used at most once. **Unbounded**: each item can be used infinitely. The only difference in code is iteration order: for 0/1, iterate `capacity` **backwards**; for unbounded, iterate **forwards**.

```python
def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):  # backwards: prevents reuse
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]

def coin_change_min(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for c in range(coin, amount + 1):  # forwards: allows reuse
            dp[c] = min(dp[c], dp[c - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

#### Common Variants & Twists
1. **Target Sum**:
   - **What (The Problem & Goal):** Given an array and a target, assign `+/-` signs to each number so they sum to the target.
   - **How (Intuition & Mental Model):** Let `P` be the sum of positive-assigned numbers and `N` be the sum of negative ones. `P - N = target` and `P + N = total_sum`. Thus, `2P = target + total_sum`. We need to find if a subset sums to `(target + total_sum) / 2`. This reduces to 0/1 Knapsack.
2. **Partition to K Equal Sum Subsets**:
   - **What (The Problem & Goal):** Partition array into `k` subsets with equal sum.
   - **How (Intuition & Mental Model):** This is NP-Hard. For small `N`, use Bitmask DP or Backtracking with pruning. `dp[mask]` stores the current sum of the mask mod `target`.
```

> [!CAUTION]
> The **iteration direction** is the single most common knapsack bug. Iterating forwards over capacity in a 0/1 problem allows using the same item multiple times (turns it into unbounded). Nail this distinction; interviewers probe it directly.

---

### Longest Common Subsequence (LCS) — 2D String DP

> [!IMPORTANT]
> **The Click Moment**: "Compare **two strings or sequences**" — OR — "minimum edits to transform one string to another" — OR — "longest shared subsequence / pattern". Any problem involving pairwise comparison of two sequences maps to a 2D DP grid.

```python
def lcs_length(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

def edit_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))  # space-optimized: single row
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]

#### Common Variants & Twists
1. **Shortest Common Supersequence**:
   - **What (The Problem & Goal):** Find the shortest string that has both `s1` and `s2` as subsequences.
   - **How (Intuition & Mental Model):** The length is `len(s1) + len(s2) - LCS(s1, s2)`. To reconstruct the string, backtrack through the LCS table.
2. **Minimum ASCII Delete Sum for Two Strings**:
   - **What (The Problem & Goal):** Minimum ASCII sum of deleted characters to make two strings equal.
   - **How (Intuition & Mental Model):** Similar to Edit Distance/LCS. If characters match, cost is 0. If they don't, choose to delete from `s1` (cost `ord(s1[i])`) or `s2` (cost `ord(s2[j])`).
```

> [!TIP]
> **Space-optimize 2D LCS/Edit Distance**: You only ever read `dp[i-1][j]`, `dp[i][j-1]`, and `dp[i-1][j-1]`. Use a single 1D array and a `prev` variable for the diagonal. Reduces O(M×N) space to O(N).

---

### Interval DP

> [!IMPORTANT]
> **The Click Moment**: "Optimal way to **merge or split a range [i, j]**" — OR — "the **last operation** happens at some index k between i and j". You don't know which k is optimal, so you try all k and take the best. Iteration order: by **length** of the interval, from short to long.

```python
def burst_balloons(nums: list[int]) -> int:
    # Add sentinel balloons of value 1 at both ends
    balloons = [1] + nums + [1]
    n = len(balloons)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):  # interval length
        for left in range(n - length):
            right = left + length
            for k in range(left + 1, right):  # k is the LAST balloon to burst
                coins = balloons[left] * balloons[k] * balloons[right]
                dp[left][right] = max(dp[left][right],
                                      dp[left][k] + coins + dp[k][right])
    return dp[0][n - 1]

#### Common Variants & Twists
1. **Matrix Chain Multiplication**:
   - **What (The Problem & Goal):** Find the minimum scalar multiplications to multiply a chain of matrices.
   - **How (Intuition & Mental Model):** Standard interval DP. `dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost_to_multiply(i, k, j))`.
2. **Minimum Score Triangulation of Polygon**:
   - **What (The Problem & Goal):** Divide a polygon into triangles to minimize the sum of products of vertices of each triangle.
   - **How (Intuition & Mental Model):** An edge `(i, j)` belongs to exactly one triangle with some vertex `k`. Split the range `[i, j]` at `k`.
```

> [!CAUTION]
> **Burst Balloons key insight**: `k` is the **last** balloon to burst in `[left, right]`, not the first. This makes the subproblems independent because `balloons[left]` and `balloons[right]` are still present when `k` is burst. Thinking of k as the first balloon to burst leads to overlapping subproblem boundaries.

---

### Bitmask DP — Subset State Tracking

> [!IMPORTANT]
> **The Click Moment**: "N ≤ 20" — AND — "need to track **which elements have been used**". State `dp[mask]` encodes the set of used elements as a bitmask. See [Bit Manipulation](../bit-manipulation.md) for the subset enumeration loop.

---

### Digit DP — Count Numbers in a Range

> [!IMPORTANT]
> **The Click Moment**: "Count integers in `[L, R]` with a specific **digit-level property**" (sum of digits = K, no consecutive same digits, etc.). The key insight: count `f(R) - f(L-1)` where `f(X)` = count of valid numbers in `[0, X]`. Build numbers digit-by-digit with a `tight` flag.

**State:** `dp[pos][tight][started][extra]`
- `pos` — current digit position
- `tight` — still bounded by the limit digit?
- `started` — has a non-zero digit been placed? (handles leading zeros)
- `extra` — problem-specific: digit sum, last digit, remainder mod K, bitmask of used digits…

```python
from functools import lru_cache

def count_up_to(limit: int, K: int) -> int:
    digits = str(limit)
    n = len(digits)

    @lru_cache(maxsize=None)
    def dp(pos: int, tight: bool, started: bool, curr_sum: int) -> int:
        if curr_sum > K: return 0          # prune
        if pos == n: return 1 if started and curr_sum == K else 0
        max_d = int(digits[pos]) if tight else 9
        total = 0
        for d in range(0, max_d + 1):
            new_started = started or d != 0
            new_sum = (curr_sum + d) if new_started else 0
            total += dp(pos+1, tight and d==max_d, new_started, new_sum)
        return total

    result = dp(0, True, False, 0)
    dp.cache_clear()   # ← critical: clear before next call
    return result

def count_digit_sum_in_range(L: int, R: int, K: int) -> int:
    return count_up_to(R, K) - count_up_to(L - 1, K)

#### Common Variants & Twists
1. **Numbers At Most N Given Digit Set**:
   - **What (The Problem & Goal):** Given a set of digits, count how many numbers up to `N` can be formed.
   - **How (Intuition & Mental Model):** Standard Digit DP where the available digits are restricted to the given set.
2. **Non-negative Integers without Consecutive Ones**:
   - **What (The Problem & Goal):** Count integers up to `N` whose binary representation doesn't have `11`.
   - **How (Intuition & Mental Model):** Use binary representation in Digit DP. State includes `last_digit`.
```

> [!CAUTION]
> **Always call `dp.cache_clear()` between `f(R)` and `f(L-1)`.** The `digits` string lives in the closure — cached results for `f(R)` are wrong for `f(L-1)`. Also: do NOT update state (`curr_sum`, `mask`, `rem`) when `started=False` — leading zeros must not pollute state.

See [digit-dp.md](digit-dp.md) for 8+ full problem implementations.

---

### Tree DP — Postorder State Propagation

> [!IMPORTANT]
> **The Click Moment**: "Optimal selection on a **tree**" — OR — "each node's value depends on its children's choices" — OR — "cannot select two adjacent nodes in a tree". Process children first (postorder); aggregate into parent.

```python
def rob_house_tree(root) -> int:
    def dfs(node):
        if not node:
            return 0, 0  # (with_node, without_node)
        left_with, left_without = dfs(node.left)
        right_with, right_without = dfs(node.right)
        with_node = node.val + left_without + right_without
        without_node = max(left_with, left_without) + max(right_with, right_without)
        return with_node, without_node

    return max(dfs(root))

#### Common Variants & Twists
1. **Binary Tree Maximum Path Sum**:
   - **What (The Problem & Goal):** Find the max path sum between any two nodes.
   - **How (Intuition & Mental Model):** For each node, the max path passing *through* it is `node.val + max(0, left_gain) + max(0, right_gain)`. Update a global max and return `node.val + max(0, left_gain, right_gain)` to the parent.
2. **House Robber III**:
   - **What (The Problem & Goal):** Maximum robbery in a tree without robbing two adjacent nodes.
   - **How (Intuition & Mental Model):** For each node, return two values: `(rob_it, skip_it)`. `rob_it = node.val + left.skip_it + right.skip_it`. `skip_it = max(left) + max(right)`.
```

---

### Stock Trading — State Machine DP

> [!IMPORTANT]
> **The Click Moment**: "Buy and sell stock with constraints" — K transactions, cooldown, fee. Unify all 6 variants under one state machine: `dp[i][k][holding]` where `holding = 0` (not holding) or `1` (holding stock).

```python
# Best Time to Buy and Sell Stock II — unlimited transactions
def max_profit_unlimited(prices: list[int]) -> int:
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free

# With cooldown (3-state machine)
def max_profit_cooldown(prices: list[int]) -> int:
    hold, sold, rest = float('-inf'), 0, 0
    for p in prices:
        prev_sold = sold          # save before overwrite
        sold = hold + p           # sell today
        hold = max(hold, rest - p)  # buy from rest only
        rest = max(rest, prev_sold) # rest or post-cooldown
    return max(sold, rest)

# With fee
def max_profit_fee(prices: list[int], fee: int) -> int:
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold = max(hold, free - p)
        free = max(free, hold + p - fee)  # subtract fee on sell
    return free

#### Common Variants & Twists
1. **Stock with Transaction Fee (Optimized)**:
   - **What (The Problem & Goal):** Unlimited transactions but each sale has a fixed fee.
   - **How (Intuition & Mental Model):** 2 states: `buy` (max profit ending in a buy) and `sell` (max profit ending in a sell). `buy = max(buy, sell - price)`, `sell = max(sell, buy + price - fee)`. This avoids the complex `dp[k]` state when transactions are unlimited.
```

| Variant | k | Extra | Code Strategy |
| :--- | :--- | :--- | :--- |
| I | 1 | None | Greedy: track `min_price` |
| II | ∞ | None | 2 states: `hold, free` |
| III | 2 | None | 4 states: `buy1, sell1, buy2, sell2` |
| IV | K | None | `dp[k][0/1]`; backward k-loop |
| Cooldown | ∞ | 1-day wait | 3 states: `hold, sold, rest`; use `prev_sold` |
| Fee | ∞ | Fee per tx | 2 states; `- fee` on sell |

See [stock-trading-dp.md](stock-trading-dp.md) for all 6 variants with full code.

---

## 3. SDE-3 Deep Dives

### Scalability: Large State Spaces & Selective Memoization

> [!TIP]
> For very large state spaces (e.g., Digit DP with large N), use a **dictionary-based memo** (`@functools.lru_cache` or explicit dict) instead of a full 2D array. This stores only **reachable states** and avoids allocating O(N²) memory when most cells are never visited.

```python
from functools import lru_cache

def count_valid_numbers(limit: str) -> int:
    n = len(limit)

    @lru_cache(maxsize=None)
    def dp(pos: int, tight: bool, started: bool) -> int:
        if pos == n:
            return 1 if started else 0
        max_digit = int(limit[pos]) if tight else 9
        total = 0
        for digit in range(0, max_digit + 1):
            is_tight = tight and (digit == max_digit)
            is_started = started or (digit != 0)
            total += dp(pos + 1, is_tight, is_started)
        return total

    return dp(0, True, False)
```

> [!CAUTION]
> `@lru_cache` uses **unhashable** arguments restriction — lists and dicts cannot be cache keys. Convert mutable state to tuples before passing. For very deep recursion (N > 10,000), increase `sys.setrecursionlimit` or rewrite iteratively.

### Scalability: Space Optimization Patterns

| Original DP | Optimized To | How |
| :--- | :--- | :--- |
| `dp[i]` uses `dp[i-1]` only | 1 variable | Rolling scalar |
| `dp[i]` uses `dp[i-1]` and `dp[i-2]` | 2 variables | `prev2, prev1` |
| `dp[i][j]` uses `dp[i-1][j*]` | 1D array | Process row i, overwrite with i+1 |
| `dp[i][j]` uses diagonal `dp[i-1][j-1]` | 1D array + `prev` scalar | Track previous diagonal value |

### Concurrency: Parallelizing DP

> [!TIP]
> Most DP problems have data dependencies that prevent naive parallelization. However:
> - **Embarrassingly parallel states**: In interval DP, all intervals of the same length are independent — each length layer can be computed in parallel.
> - **Wavefront parallelism**: In 2D grid DP, all cells on the same anti-diagonal (`i + j = constant`) are independent.
> - In practice: Python's GIL blocks CPU parallelism in threads; use `multiprocessing` or `numpy` vectorization for bulk DP transitions.

### When DP is the Wrong Tool

> [!CAUTION]
> DP requires **optimal substructure** (the global optimum contains local optima) and **overlapping subproblems** (the same subproblems are solved repeatedly). If either is absent, DP is wrong:
> - **Greedy** works when local optimal choices always lead to the global optimum (e.g., Activity Selection, Huffman).
> - **Divide and conquer** works when subproblems don't overlap (e.g., standard Merge Sort).
> - **Backtracking** is needed when you can't define a useful state or when constraints invalidate memoization.

### Trade-offs: Top-Down vs. Bottom-Up

| Dimension | Top-Down (Memoization) | Bottom-Up (Tabulation) |
| :--- | :--- | :--- |
| Code style | Natural recursion; easier to derive | Requires explicit iteration order |
| Space | Stack depth + memo table | Memo table only; no stack risk |
| Cache efficiency | Cache misses on sparse access | Sequential memory access = cache-friendly |
| Partial computation | Only computes reachable states | Fills entire table regardless |
| When to prefer | Complex state transitions; large sparse space | Tight space constraints; no recursion limit risk |

---

## 4. Common Interview Problems

### Easy
- **Climbing Stairs** — Fibonacci; `dp[i] = dp[i-1] + dp[i-2]`; space-optimize to 2 vars.
- **Min Cost Climbing Stairs** — Can start at step 0 or 1; `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`.
- **Maximum Subarray** — Kadane; `end_here = max(x, end_here + x)`.
- **Best Time to Buy/Sell I** — Greedy; track running minimum; answer = max(price - min_seen).
- **Delete and Earn** — House Robber on `earn[v] = v × count(v)` array.

### Medium
- [House Robber](../../../google-sde2/PROBLEM_DETAILS.md#house-robber) — Linear DP; space-optimize to O(1).
- [Longest Increasing Subsequence](../../../google-sde2/PROBLEM_DETAILS.md#longest-increasing-subsequence) — O(N²) DP or O(N log N) patience sort (binary search).
- [Coin Change](../../../google-sde2/PROBLEM_DETAILS.md#coin-change) — Unbounded knapsack; forward iteration.
- [Word Break](../../../google-sde2/PROBLEM_DETAILS.md#word-break) — Linear DP with set lookup; `dp[i]` = can s[:i] be segmented.
- **Partition Equal Subset Sum** — 0/1 knapsack; `dp[target]` = is subset-sum `target` achievable?
- **Longest Palindromic Subsequence** — LCS of string with its reverse.
- **Jump Game II** — Greedy O(N) beats DP O(N²); mention both.
- **Stock with Cooldown** — 3-state machine: `hold, sold, rest`. Use `prev_sold`.
- **Unique Paths II** — Grid DP; blocked cells → `dp[i][j] = 0`.
- **Longest Common Substring** — Grid DP; reset on mismatch (unlike LCS).
- **Interleaving String** — 2D DP; two sources for each char of s3.
- **Maximal Square** — `dp[i][j] = min(3 neighbors) + 1`; answer = `max_side²`.

### Hard
- [Edit Distance](../../../google-sde2/PROBLEM_DETAILS.md#edit-distance) — 2D LCS variant; space-optimize to O(N).
- [Burst Balloons](../../../google-sde2/PROBLEM_DETAILS.md#burst-balloons) — Interval DP; k = last balloon burst.
- **Palindrome Partitioning II** — Precompute `is_pal[i][j]`; linear `cut[]` array.
- **Regular Expression Matching** — 2D DP; `*` = zero OR more of preceding char.
- **Wildcard Matching** — 2D DP; `*` = any sequence (standalone, not preceding).
- **Strange Printer** — Interval DP; merge when `s[i] == s[j]`.
- **Super Egg Drop** — Invert DP: `dp[moves][eggs]` = max floors. O(K log N).
- **Dungeon Game** — Reverse grid DP; forward DP is impossible here.
- **Cherry Pickup** — Simulate 2 simultaneous forward trips: `dp[t][r1][r2]`.
- **Shortest Path Visiting All Nodes** — Bitmask BFS; `(mask, node)` state.

---

## Interview Questions — Logic & Trickiness

| Question | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- |
| **[House Robber](../../../google-sde2/PROBLEM_DETAILS.md#house-robber)** | "No adjacent selection" | `dp[i] = max(dp[i-1], val + dp[i-2])` | Space-optimize to 2 vars; handle `len=1` separately. |
| **[LIS](../../../google-sde2/PROBLEM_DETAILS.md#longest-increasing-subsequence)** | "Strictly increasing order" | O(N²) DP or O(N log N) patience sort | **O(N log N)** is often expected at SDE-3; patience sort uses `bisect_left`. |
| **[Word Break](../../../google-sde2/PROBLEM_DETAILS.md#word-break)** | "Partition string into dictionary words" | `dp[i]` = can segment `s[:i]` | Use a **set** for O(1) lookup; nested loop is O(N²) without it. |
| **[Edit Distance](../../../google-sde2/PROBLEM_DETAILS.md#edit-distance)** | "Transform string via ops" | 2D DP on prefix pairs | Initialize `dp[0][j]=j` and `dp[i][0]=i`; space-optimize to 1D. |
| **Coin Change** | "Min coins for amount" | Unbounded knapsack; forward iteration | Init dp with `inf`, not 0; return -1 if `dp[amount]` stays `inf`. |
| **Partition Equal Subset** | "Split into two equal halves" | 0/1 knapsack to `sum//2` | Only possible if total sum is even; check first. |
| **[Burst Balloons](../../../google-sde2/PROBLEM_DETAILS.md#burst-balloons)** | "Last operation in range" | Interval DP; k = last to burst | k is the **last** balloon, not first — this is what makes subproblems non-overlapping. |
| **LPS (Longest Palindromic Subseq)** | "Palindromic structure in one string" | LCS of `s` and `reversed(s)` | Classic LCS reduction; easy to miss this framing. |
| **Egg Drop** | "Min trials in worst case" | Interval DP or binary search + DP | State `dp[eggs][floors]`; can be inverted: "how many floors with k eggs and t trials?" |
| **Regular Expression** | "Pattern match with `*` and `.`" | 2D DP; `*` = zero or more of prev char | `*` can mean zero occurrences of the preceding char — handle separately. |
| **Climbing Stairs** [E] | "Ways to climb N stairs (1 or 2 steps at a time)" | `dp[i] = dp[i-1] + dp[i-2]`; base cases `dp[1]=1, dp[2]=2` | This is Fibonacci — space-optimize to two variables. Generalize to K step sizes as follow-up. |
| **Min Cost Climbing Stairs** [E] | "Min cost to reach top; each step costs `cost[i]`" | `dp[i] = min(dp[i-1], dp[i-2]) + cost[i]`; answer = `min(dp[n-1], dp[n-2])` | Can start from index 0 or 1 — both are valid starting positions. |
| **Unique Paths** [E] | "Count paths in m×n grid moving only right/down" | `dp[i][j] = dp[i-1][j] + dp[i][j-1]`; base row/col all 1s | Space-optimize to 1D by reusing row array. Math formula: `C(m+n-2, m-1)`. |
| **Maximum Product Subarray** [M] | "Max product of contiguous subarray" | Track both `max_prod` and `min_prod` (negatives flip on multiplication) | Negative × negative = positive max — must track minimum as well. Reset on 0. |
| **Decode Ways** [M] | "Number of ways to decode digit string (A=1..Z=26)" | `dp[i]` from `dp[i-1]` (single char) + `dp[i-2]` (two chars if 10-26) | `'0'` alone is invalid; `'06'` is invalid (leading zero); handle these edge cases. |
| **Triangle** [M] | "Min path sum from top to bottom of triangle" | Bottom-up; `dp[j] = min(dp[j], dp[j+1]) + triangle[i][j]` | Work bottom-up to avoid managing indices for variable-width rows. |
| **Counting Subsets Equal to Sum** [M] | "Number of subsets summing to target" | 0/1 knapsack counting variant; `dp[w] += dp[w - num]`; backward iteration | Init `dp[0] = 1`; backward loop so each item counted at most once (unlike unbounded). |
| **Longest Common Substring** [M] | "Contiguous common substring (not subsequence)" | `dp[i][j] = dp[i-1][j-1] + 1` if chars match, else 0 | Reset to 0 on mismatch (contiguous); max over all `dp[i][j]` is answer. LCS keeps value on mismatch — know the difference. |
| **Minimum Path Sum** [M] | "Grid path with min cost, right/down only" | `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])` | Initialize top row and left column as prefix sums. O(1) space: modify grid in place. |
| **Maximal Square** [M] | "Largest square of 1s in binary matrix" | `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1` | Answer = `max(dp[i][j])²`; the min of three neighbors is the key insight. |
| **Interleaving String** [M] | "Can s3 be formed by interleaving s1 and s2?" | `dp[i][j]` = can form `s3[:i+j]` using `s1[:i]` and `s2[:j]` | Two sources for each `s3[i+j-1]` position; transitions from both dimensions. |
| **Super Egg Drop** [H] | "Min moves in worst case with K eggs and N floors" | Invert problem: `dp[moves][eggs]` = max floors checkable | Direct `dp[eggs][floors]` is O(KN²); inverted is O(KN log N) with binary search. |
| **Palindrome Partitioning II** [H] | "Min cuts to make all parts palindromes" | `cut[i]` = min cuts for `s[:i+1]`; precompute palindrome table | Combine palindrome expansion + cut DP in one pass for O(N²). |
| **Strange Printer** [H] | "Min print operations to print string" | Interval DP; if `s[i] == s[j]`, `dp[i][j] = dp[i][j-1]` (extend last turn) | Diagonal order; merge intervals when endpoints match — reduces prints by 1. |

---

## Quick Revision Triggers

- "Overlapping subproblems + optimal substructure" → DP; memoize or tabulate.
- "Recursive solution has exponential branches with repeated arguments" → add `@lru_cache`; done.
- "Count ways / min cost / max profit over a sequence" → 1D DP on index; define `dp[i]` as answer for prefix ending at `i`.
- "Two sequences (strings, arrays): align / match / edit" → 2D DP on `(i, j)`; LCS / edit distance template.
- "Subset sum / knapsack: include or exclude each item" → 1D DP iterating items then capacity (backwards for 0/1 knapsack).
- "Optimal split of a contiguous segment (matrix chain, burst balloons)" → interval DP `dp[l][r]`; try all split points k.
- "State space encodes a subset of N items (N ≤ 20)" → bitmask DP `dp[mask]`; enumerate submasks in O(3^N).
- "Count integers in [L, R] with digit property (digit sum, no repeats, divisible by K)" → digit DP `f(R) - f(L-1)` with `(pos, tight, started, extra)` state.
- "Buy/sell stock with K transactions / cooldown / fee" → state machine DP; `hold` and `free` states.
- "Grid, paths right/down, count or minimize" → grid DP `dp[i][j]`; top row and left column as base.
- "Palindrome structure, min cuts, min insertions" → palindrome DP `is_pal[i][j]`; fill by increasing interval length.
- "Match pattern with `*` and `.`" → 2D string DP; regex `*` = zero-or-more of PRECEDING char.
- "Optimal play by two players, both play optimally" → minimax DP; `dp[state]` = score difference.
- "Expected value, probability, dice rolls, knight path" → forward probability propagation DP.

---

## See also

**DP Sub-files (this folder):**
- [dp-aditya-verma.md](dp-aditya-verma.md) — Full pattern playbook: 9 patterns with complete code
- [digit-dp.md](digit-dp.md) — Digit DP: count numbers in ranges with digit properties
- [grid-dp.md](grid-dp.md) — 2D grid DP: unique paths, min path sum, cherry pickup, dungeon
- [stock-trading-dp.md](stock-trading-dp.md) — All 6 stock variants with unified state machine
- [string-palindrome-dp.md](string-palindrome-dp.md) — Palindromes, regex, wildcard, interleaving
- [advanced-dp-optimizations.md](advanced-dp-optimizations.md) — CHT, deque opt, D&C opt, SOS DP
- [probability-combinatorics-dp.md](probability-combinatorics-dp.md) — Expected value, games, egg drop
- [questions-bank.md](questions-bank.md) — 70 tiered drill questions (Easy / Medium / Hard)
- [tips-and-gotchas.md](tips-and-gotchas.md) — 12 common bugs, recognition triggers, interview framework

**Related files:**
- [Patterns Master](../../../../reference/patterns/patterns-master.md) — 16 DP pattern recognition triggers
- [Bit Manipulation](../bit-manipulation.md) — bitmask DP for subset problems
- [Backtracking](../backtracking.md) — when to use backtracking vs. memoizing into DP
- [Binary Search](../binary-search.md) — O(N log N) LIS via patience sort
