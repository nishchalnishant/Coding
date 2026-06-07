# Dynamic Programming — Complete Guide

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.





---

## First-Principles Map

```
WHY Dynamic Programming exists
├── Overlapping subproblems make brute recursion exponential
│   ├── Same sub-problem re-solved from different call paths
│   └── Naive recursion has O(2^n) or O(n!) time for many choices
WHAT it is
├── Optimization over exhaustive recursion via memoization or tabulation
│   ├── Key property: optimal substructure — optimal global answer built from optimal sub-answers
│   └── Key property: overlapping subproblems — same (i, state) pair appears multiple times
HOW it works
├── Core mechanism: fix a state signature, store results, avoid recomputation
│   ├── Step 1 — write recursive brute-force with correct base cases
│   ├── Step 2 — add a memo table keyed on all recursion arguments
│   ├── Step 3 — invert to bottom-up: fill table in dependency order
│   └── Step 4 — compress table dimensions that are only needed one step back
WHEN to use
├── "count / max / min ways" + choice at each step → DP (not greedy)
├── Two sequences to align → LCS / Edit Distance family
├── Splitting an interval optimally → MCM / Interval DP
├── Items with weight + value, limited capacity → Knapsack family
└── Subtree aggregation needed → DP on Trees
WHAT can go wrong
├── Wrong state: missing a dimension that changes the subproblem identity
├── Wrong base case: uninitialized cells propagate garbage values
└── Wrong iteration order (bottom-up): computing dp[i] before dp[i-1] is ready
DECISION
└── If you see "choice + optimal over all choices" → try DP; "always take the local best" → try greedy first
```

**First-Principles Breakdown:**
- **Root problem:** Brute-force enumeration of all choices is exponential; DP prunes it by caching repeated sub-answers.
- **Core insight:** Any optimal solution can be decomposed into optimal solutions to its sub-problems (optimal substructure).
- **Invariant:** When `dp[i][w]` is computed, every sub-problem it depends on is already computed and correct.
- **Why it works:** Memoization converts an exponential recursion tree into a DAG where each node is solved exactly once.
- **Where it breaks:** Greedy counter-examples exist whenever a locally optimal choice forecloses a globally better path.

---

## The Universal DP Recipe

Every DP problem follows this four-step build order. Never skip to code before step 2.

```
Step 1 — Recursive solution (brute force, correct)
Step 2 — Add memoization (top-down DP)
Step 3 — Convert to bottom-up table (tabulation)
Step 4 — Optimize space (rolling array / two variables)
```

**Identify DP:** At each step you have a **choice** (take/skip, split, match/skip) **and** the problem asks for optimal (max/min/count). If there's no choice — it's greedy or math.

**State naming rule:** State = the minimum set of parameters that uniquely defines a subproblem. If recursion has signature `f(i, w)`, your table is `dp[i][w]`.

**Transition direction:** Bottom-up fills small subproblems first. Choose loop order so when you compute `dp[i][w]`, every value on the RHS is already filled.

---

## SDE-3 Gold Standard Mental Map

```
DP
├── Linear 1D: dp[i] from dp[i-1..i-k]
│   ├── Fibonacci, Climbing Stairs, Decode Ways
│   └── House Robber, Word Break, Paint Fence
├── 0/1 Knapsack: dp[i][w], iterate w BACKWARD in 1D
│   ├── Subset Sum, Partition, Target Sum
│   └── Ones and Zeroes (2D capacity)
├── Unbounded Knapsack: same but iterate w FORWARD
│   ├── Coin Change, Rod Cutting, Perfect Squares
│   └── Combination Sum IV
├── 2D String DP (LCS family): dp[i][j] = prefix match
│   ├── LCS → SCS, LPS, Edit Distance
│   └── Distinct Subsequences, Interleaving String
├── Interval DP: dp[i][j] by length; k = split point
│   └── Strange Printer, Zuma, Optimal BST
├── Grid DP: dp[r][c]; sometimes reverse fill
│   ├── Unique Paths, Min Path Sum, Triangle
│   ├── Dungeon (reverse), Maximal Square
│   └── Cherry Pickup (2 travelers = 4D)
├── Tree DP: post-order DFS, return tuple
│   ├── House Robber III, Max Path Sum, Cameras
│   └── Diameter, Largest BST Subtree
├── Bitmask DP: dp[mask][node] for N ≤ 20
│   ├── TSP, Shortest Path All Nodes
│   └── Smallest Sufficient Team, Stickers
│   ├── Count integers in [L,R] with property
│   └── Monotone digits, No consecutive same
├── Stock State Machine: dp[i][k][holding]
│   ├── Single/unlimited/k-transaction variants
│   └── Cooldown (3 states), Fee
└── Advanced: CHT, D&C DP, Knuth, SOS, Slope Trick
```

---

## Pattern Map — Choose in 30 Seconds

| What the problem asks | Pattern |
| :--- | :--- |
| Pick items (each once) to hit capacity / sum | **0/1 Knapsack** |
| Pick items (unlimited copies) to hit capacity | **Unbounded Knapsack** |
| `dp[i]` depends on `dp[i-1]`, `dp[i-2]` | **Fibonacci / Linear** |
| Two sequences — align and match | **LCS family** |
| One sequence — longest increasing / longest chain | **LIS `🎯 T2`** |
| Best subarray ending at `i` | **Kadane** |
| Split interval `[i,j]` at every `k` | **MCM / Interval DP** |
| Subtree answers combined at root | **DP on Trees** |
| Node + extra state (mask, moves) | **DP on Graphs / Bitmask** |
| Count strings / sequences with constraints | **Counting / Probability DP** |

---

## Signal → Pattern Quick Reference

| Signal in problem | Pattern |
| :--- | :--- |
| "Each item at most once" + capacity constraint | 0/1 Knapsack (backward loop) |
| "Unlimited copies" + capacity constraint | Unbounded Knapsack (forward loop) |
| "Number of ways" + items/coins | Unbounded count — `dp[0]=1`, add not max |
| `dp[i]` from `dp[i-1]` and `dp[i-2]` only | Fibonacci / Linear |
| Two strings, "common", "match", "align" | LCS family |
| One array, "longest increasing" | LIS (`bisect_left` for strict) |
| "Best subarray", "contiguous", "max/min sum" | Kadane |
| "Interval `[i,j]`", "split at `k`", "optimal order" | MCM / Interval DP |
| Tree problem with "rob/skip", "path through root" | Tree DP (post-order DFS, return pair) |
| N ≤ 20, "visit all nodes", "assign items" | Bitmask DP |
| "Count integers in [L,R] with digit-level property" | "Probability", "expected value" | Probability / Expected Value DP |
| "Optimal play", "both players optimal" | Game / Minimax DP |

---

# Pattern 1 — Linear / Fibonacci DP

## Theory

- **Core idea:** `dp[i]` depends on a fixed small window of previous values. Dimension is purely position.
- **State:** `dp[i]` = answer for problem of size `i`.
- **Recurrence:** `dp[i] = f(dp[i-1], dp[i-2])`.
- **Space optimization:** O(1) using two variables.

## Implementations

```python
def climb_stairs(n: int) -> int:
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def house_robber(nums: list[int]) -> int:
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

def house_robber_ii(nums: list[int]) -> int:
    def rob_linear(arr):
        prev2, prev1 = 0, 0
        for x in arr:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
    if len(nums) == 1:
        return nums[0]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

def decode_ways(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 0 if s[0] == '0' else 1
    for i in range(2, n + 1):
        one_digit = int(s[i-1])
        two_digit = int(s[i-2:i])
        if one_digit >= 1:
            dp[i] += dp[i-1]
        if 10 <= two_digit <= 26:
            dp[i] += dp[i-2]
    return dp[n]
```

> [!TIP]
> **House Robber II (circle): `🎯 T2`** Run the linear robber twice — once on `nums[:-1]` and once on `nums[1:]`. Take the max. The circle constraint means you can't rob both first and last house.

## Variations

| Problem | Recurrence | Note |
| :--- | :--- | :--- |
| **Climbing Stairs `🎯 T2`** | `dp[i] = dp[i-1] + dp[i-2]` | Fibonacci exactly |
| **Min Cost Climbing Stairs** | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` | Can start at step 0 or 1 |
| **Decode Ways `🎯 T2`** | One + two digit branches | `'0'` as first digit kills branch |
| **House Robber I `🎯 T2`** | `dp[i] = max(dp[i-1], nums[i]+dp[i-2])` | — |
| **House Robber II `🎯 T2`** | Two linear passes, exclude ends | Classic circle trick |

---

# Pattern 2 — 0/1 Knapsack

## Theory

- **Core idea:** Each item has a binary choice — include it once or skip it.
- **State:** `dp[i][w]` = maximum value achievable using only the first `i` items with capacity `w`.
- **Recurrence:** `dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])`.
- **Space optimization:** 1D `dp[w]` by iterating `w` from **high → low**.

## Implementations

```python
def knapsack_01(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], values[i-1] + dp[i-1][w - weights[i-1]])
    return dp[n][W]

def knapsack_01_space(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):   # BACKWARD — 0/1 invariant
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]

def knapsack_reconstruct(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], values[i-1] + dp[i-1][w - weights[i-1]])
    items, w = [], W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            items.append(i - 1)
            w -= weights[i - 1]
    return dp[n][W], items[::-1]
```

> [!CAUTION]
> **Backward vs Forward loop:** In 1D, iterating `w` backward (high → low) ensures each item is used at most once. Iterating forward (low → high) allows the same item to be picked multiple times — that is the unbounded knapsack. Getting this backwards is the #1 knapsack bug.

## Knapsack → Subset Sum Reductions

| Formulation | `dp` meaning | Base | Transition |
| :--- | :--- | :--- | :--- |
| Max value ≤ W | `dp[w]` = max value | `dp[0] = 0` | `dp[w] = max(dp[w], v + dp[w-wt])` |
| Is sum T achievable? | `dp[w]` = True/False | `dp[0] = True` | `dp[w] \|= dp[w - num]` |
| Count subsets summing to T | `dp[w]` = # ways | `dp[0] = 1` | `dp[w] += dp[w - num]` |
| Min items summing to T | `dp[w]` = min items | `dp[0]=0`, rest `inf` | `dp[w] = min(dp[w], 1 + dp[w-num])` |

**Identification checklist:**
- [ ] Each item picked at most once → 0/1 Knapsack (backward loop)
- [ ] Items picked unlimited → Unbounded Knapsack (forward loop)
- [ ] Ask is "max/min/count" not "which" → DP (reconstruction is a follow-up)
- [ ] Reduce sum problems: "subset sum to T" = knapsack with `value[i] = weight[i]`

## Variations

| Problem | Transform | Key Insight |
| :--- | :--- | :--- |
| **Subset Sum `🎯 T2`** | Boolean knapsack; `dp[sum]` = True/False | `dp[0] = True`; iterate sum descending |
| **Partition Equal Subset Sum `🎯 T2`** | Subset sum to `total // 2` | Odd total → impossible immediately |
| **Target Sum (±assign) `🎯 T2`** | Count subsets with sum `(total + target) / 2` | Parity check first; count, not max |
| **Count Subsets with Given Sum** | Add ways: `dp[w] += dp[w - weight]` | `dp[0] = 1` (empty subset = one way) |
| **Last Stone Weight II** | Partition to minimize `\|S1 - S2\|` | Subset sum variant |
| **Ones and Zeroes** | 2D knapsack: capacity is `(m zeros, n ones)` | `dp[i][j]` = max strings using ≤ i zeros, ≤ j ones |

---

# Pattern 3 — Unbounded Knapsack

## Theory

- **Core idea:** Each item type can be picked **unlimited** times.
- **Recurrence:** `dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i][w - weights[i-1]])` (stay at `i`).
- **Space optimization:** 1D `dp[w]` with **forward** iteration (low → high).

## Implementations

```python
def knapsack_unbounded(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(weights[i], W + 1):   # FORWARD — unbounded invariant
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]

def coin_change_min(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for w in range(coin, amount + 1):            # forward = unbounded
            dp[w] = min(dp[w], 1 + dp[w - coin])
    return dp[amount] if dp[amount] != float('inf') else -1

def coin_change_ways(coins: list[int], amount: int) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1                                        # one way to make 0: pick nothing
    for coin in coins:                               # coins outer = combinations (no order overcount)
        for w in range(coin, amount + 1):
            dp[w] += dp[w - coin]
    return dp[amount]
```

> [!TIP]
> **Combinations vs Permutations:** `coins` outer, `amount` inner → counts combinations (unordered). `amount` outer, `coins` inner → counts permutations (ordered). Coin Change 2 wants combinations.

## Variations

| Problem | Loop Order | Key Insight |
| :--- | :--- | :--- |
| **Coin Change I `🎯 T2`** (min coins) | Coins outer, amount forward | `dp[0]=0`, rest `inf`; take `min` |
| **Coin Change II `🎯 T2`** (count ways) | Coins outer, amount forward | `dp[0]=1`; takes `+=` not `max` |
| **Rod Cutting** (max value) | Lengths outer, capacity forward | Identical to unbounded knapsack |
| **Integer Break** (max product) | Split 1…n; `dp[i] = max(j*(i-j), j*dp[i-j])` | Greedy: break into 3s (AM-GM) |
| **Perfect Squares** (min count) | Squares outer, amount forward | Same as coin change with coins = 1,4,9,16… |

---

# Pattern 4 — LCS Family (2D String DP)

## Theory

- **Core idea:** Two sequences. Match characters or skip one side.
- **State:** `dp[i][j]` = LCS of `s1[:i]` and `s2[:j]`.
- **Recurrence:** `Match ? 1 + dp[i-1][j-1] : max(up, left)`.
- **Space optimization:** O(min(m, n)) using two rows.

## Implementations

```python
def lcs(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def edit_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # delete
                                    dp[i][j-1],    # insert
                                    dp[i-1][j-1])  # replace
    return dp[m][n]

def shortest_common_supersequence(s1: str, s2: str) -> str:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    result, i, j = [], m, n
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result.append(s1[i-1]); i -= 1; j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            result.append(s1[i-1]); i -= 1
        else:
            result.append(s2[j-1]); j -= 1
    result.extend(reversed(s1[:i]))
    result.extend(reversed(s2[:j]))
    return ''.join(reversed(result))

def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j]
            if s[i-1] == t[j-1]:
                dp[i][j] += dp[i-1][j-1]
    return dp[m][n]

def is_interleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3): return False
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or \
                       (dp[i][j-1] and s2[j-1] == s3[i+j-1])
    return dp[m][n]
```

## LCS-Family Derivations

| Problem | Formula / Derivation |
| :--- | :--- |
| **LCS length** | `dp[i][j]` directly |
| **Print LCS** | Traceback: match → diagonal; else → max of up/left |
| **Shortest Common Supersequence** | Length = `m + n - LCS`; reconstruct by merging |
| **Min insertions to make palindrome** | `len(s) - LPS(s)` |
| **Min deletions to make palindrome** | `len(s) - LPS(s)` |
| **Edit distance `🎯 T2`** | Replace = diagonal + 1; insert/delete = +1 on axis |
| **Distinct subsequences `🎯 T2`** | Count ways `s` contains `t` as subseq: add, don't max |
| **Longest Common Substring** | Reset to 0 on mismatch; track global max |
| **Interleaving Strings `🎯 T2`** | `dp[i][j]` = can `s1[:i]+s2[:j]` form `s3[:i+j]` |

## Key Differences: Substring vs Subsequence

| Property | Substring | Subsequence |
| :--- | :--- | :--- |
| Contiguous? | Yes | No |
| DP reset on mismatch? | Yes (`dp[i][j] = 0`) | No (`dp[i][j] = max(up, left)`) |
| Answer | `max over all dp[i][j]` | `dp[m][n]` |

---

# Pattern 5 — LIS (Longest Increasing Subsequence)

## Theory

- **State (O(N²)):** `dp[i]` = length of LIS ending at index `i`.
- **Recurrence:** `dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])`.
- **O(N log N) alternative:** Patience sorting with `tails[]` and binary search.

## Implementations

```python
def lis_n2(nums: list[int]) -> int:
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

import bisect

def lis_nlogn(nums: list[int]) -> int:
    tails = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)   # strict LIS
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)

def lis_nlogn_non_decreasing(nums: list[int]) -> int:
    tails = []
    for x in nums:
        pos = bisect.bisect_right(tails, x)  # non-strict
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)
```

> [!CAUTION]
> `tails` is NOT the actual LIS — it's a bookkeeping structure for length only. To reconstruct the actual subsequence, store `parent[]` pointers in the O(N²) approach.

> [!TIP]
> **Russian Doll Envelopes = 2D LIS:** Sort by width ascending; for ties sort height **descending**. Then run LIS on heights only. Descending height on ties prevents picking two envelopes with the same width.

## LIS-Family Problems

| Problem | Key Transform |
| :--- | :--- |
| **LIS (strict) `🎯 T2`** | `bisect_left` in patience sort |
| **LIS (non-decreasing) `🎯 T2`** | `bisect_right` in patience sort |
| **Count LIS** | O(N²): track both `dp[i]` (length) and `cnt[i]` (count) |
| **Longest Chain of Pairs** | Sort by second element; LIS on first where pairs don't overlap |
| **Russian Doll Envelopes** | Sort (w asc, h desc); LIS on h |

---

# Pattern 6 — Kadane (Best Subarray)

## Theory

- **State:** `dp[i]` = best subarray sum ending at index `i`.
- **Recurrence:** `dp[i] = max(nums[i], dp[i-1] + nums[i])`.
- **Space optimization:** O(1) — only the previous value needed.

## Implementations

```python
def max_subarray(nums: list[int]) -> int:
    ending_here = global_max = nums[0]
    for x in nums[1:]:
        ending_here = max(x, ending_here + x)
        global_max = max(global_max, ending_here)
    return global_max

def max_subarray_with_indices(nums: list[int]) -> tuple[int, int, int]:
    best_sum = cur_sum = nums[0]
    best_start = best_end = cur_start = 0
    for i in range(1, len(nums)):
        if nums[i] > cur_sum + nums[i]:
            cur_sum = nums[i]
            cur_start = i
        else:
            cur_sum += nums[i]
        if cur_sum > best_sum:
            best_sum = cur_sum
            best_start, best_end = cur_start, i
    return best_sum, best_start, best_end

def max_product_subarray(nums: list[int]) -> int:
    cur_max = cur_min = global_max = nums[0]
    for x in nums[1:]:
        candidates = (x, cur_max * x, cur_min * x)
        cur_max, cur_min = max(candidates), min(candidates)
        global_max = max(global_max, cur_max)
    return global_max

def max_circular_subarray(nums: list[int]) -> int:
    total = sum(nums)
    max_straight = max_subarray(nums)
    min_sub = max_subarray([-x for x in nums])
    max_wrap = total + min_sub
    return max(max_straight, max_wrap) if max_wrap != 0 else max_straight
```

> [!TIP]
> **Max Product Subarray:** Track both `cur_max` and `cur_min` at each step because a large negative × negative = large positive. All three candidates `(x, cur_max*x, cur_min*x)` must be evaluated on every step.

## Kadane Variations

| Problem | Twist |
| :--- | :--- |
| **Standard max subarray** | Base Kadane |
| **Max product subarray** | Track min and max (negatives flip sign) |
| **Circular subarray max** | `max(straight, total - min_subarray)` |
| **Return indices** | Track `cur_start`; update `best_start/end` on improvement |

---

# Pattern 7 — Interval DP (MCM)

## Theory

- **Core idea:** Optimal solution for interval `[i, j]` depends on splitting at `[i, k]` and `[k+1, j]`.
- **State:** `dp[i][j]` = optimal cost/value for the interval `[i..j]`.
- **Fill order:** By **increasing length** — `len = 2, 3, …, n`.
- **Base case:** `dp[i][i] = 0` (interval of size 1).

## Implementations

```python
def matrix_chain_multiplication(dims: list[int]) -> int:
    n = len(dims) - 1
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j]
                dp[i][j] = min(dp[i][j], cost)
    return dp[1][n]


def palindrome_partition_min_cuts(s: str) -> int:
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True
    dp = list(range(n))
    for i in range(1, n):
        if is_pal[0][i]:
            dp[i] = 0
            continue
        for j in range(1, i + 1):
            if is_pal[j][i]:
                dp[i] = min(dp[i], dp[j-1] + 1)
    return dp[n - 1]
```

## Interval DP Variations

| Problem | Cost at split | State |
| :--- | :--- | :--- |
| **Palindrome Partitioning II `🎯 T2`** | `1` if `s[j..i]` is palindrome | `dp[i]` = min cuts for prefix |
| **Strange Printer** | Reuse or overwrite | `dp[i][j]` = min turns to print `s[i..j]` |
| **Optimal BST** | Key search probabilities | `dp[i][j]` = min expected search cost |

---

# Pattern 8 — Grid DP

## Theory & Mental Model

**Grid DP:** State is `dp[r][c]`, typically filled left-to-right, top-to-bottom. For problems requiring reverse (e.g., Dungeon), fill bottom-to-top.

**Two travelers:** When two agents traverse simultaneously, use `dp[r1][c1][r2][c2]` compressed to `dp[step][r1][r2]` since `c2 = step - r2`, `c1 = step - r1`.

## Implementations

```python
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[m-1][n-1]

def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1 if grid[0][0] == 0 else 0
    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0: continue
            if grid[r][c] == 1:
                dp[r][c] = 0
            else:
                dp[r][c] = (dp[r-1][c] if r > 0 else 0) + (dp[r][c-1] if c > 0 else 0)
    return dp[m-1][n-1]

def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0]*n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for c in range(1, n): dp[0][c] = dp[0][c-1] + grid[0][c]
    for r in range(1, m): dp[r][0] = dp[r-1][0] + grid[r][0]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])
    return dp[m-1][n-1]

def minimum_total(triangle: list[list[int]]) -> int:
    n = len(triangle)
    dp = triangle[-1][:]
    for row in range(n - 2, -1, -1):
        for col in range(row + 1):
            dp[col] = triangle[row][col] + min(dp[col], dp[col + 1])
    return dp[0]

def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    m, n = len(dungeon), len(dungeon[0])
    dp = [[0]*n for _ in range(m)]
    dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
    for c in range(n-2, -1, -1):
        dp[m-1][c] = max(1, dp[m-1][c+1] - dungeon[m-1][c])
    for r in range(m-2, -1, -1):
        dp[r][n-1] = max(1, dp[r+1][n-1] - dungeon[r][n-1])
    for r in range(m-2, -1, -1):
        for c in range(n-2, -1, -1):
            min_next = min(dp[r+1][c], dp[r][c+1])
            dp[r][c] = max(1, min_next - dungeon[r][c])
    return dp[0][0]

def maximal_square(matrix: list[list[str]]) -> int:
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0]*n for _ in range(m)]
    max_side = 0
    for r in range(m):
        for c in range(n):
            if matrix[r][c] == '1':
                dp[r][c] = 1 if r == 0 or c == 0 else min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) + 1
                max_side = max(max_side, dp[r][c])
    return max_side * max_side

def cherry_pickup_ii(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(row, c1, c2):
        if row == m: return 0
        cherries = grid[row][c1] + (grid[row][c2] if c2 != c1 else 0)
        best = 0
        for dc1 in [-1, 0, 1]:
            for dc2 in [-1, 0, 1]:
                nc1, nc2 = c1 + dc1, c2 + dc2
                if 0 <= nc1 < n and 0 <= nc2 < n:
                    best = max(best, dp(row + 1, nc1, nc2))
        return cherries + best
    return dp(0, 0, n - 1)

def find_paths(m: int, n: int, max_move: int, start_row: int, start_col: int) -> int:
    MOD = 10**9 + 7
    dp = [[0]*n for _ in range(m)]
    dp[start_row][start_col] = 1
    ans = 0
    for _ in range(max_move):
        ndp = [[0]*n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < m and 0 <= nc < n:
                        ndp[nr][nc] = (ndp[nr][nc] + dp[r][c]) % MOD
                    else:
                        ans = (ans + dp[r][c]) % MOD
        dp = ndp
    return ans
```

## Space Optimization Rules

| Pattern | Original | Optimized |
| :--- | :--- | :--- |
| Unique Paths / Min Path Sum | O(M×N) | O(N) single row |
| Triangle bottom-up | O(N²) | O(N) `dp = last row` |
| Maximal Square | O(M×N) | O(N) + one scalar `prev` |
| Dungeon (reverse fill) | O(M×N) | O(N) one row, fill R→L |

## Grid DP Interview Questions

| Problem | LC # | Pattern | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Unique Paths `🎯 T2`** | 62 | Forward DP | `dp[r][c] = dp[r-1][c] + dp[r][c-1]` | Base row/col = all 1s |
| **Unique Paths II `🎯 T2`** | 63 | Forward DP with obstacles | Set `dp[r][c] = 0` when obstacle | Re-check first row/col early |
| **Min Path Sum** | 64 | Forward DP | Grid values as cost; minimize | Init top row and left col first |
| **Triangle** | 120 | Bottom-up reverse | Start from last row, merge upward | Can reuse last row as `dp` |
| **Dungeon Game** | 174 | **Reverse DP** | Min HP needed works backward only | Forward DP is impossible here |
| **Maximal Square `🎯 T2`** | 221 | `min(3 neighbors)+1` | Extend bottom-right corner | `matrix` is `str`, cast to int |
| **Cherry Pickup II** | 1463 | Two travelers 3D→2D | Both start top; symmetric start helps | c1 ≤ c2 invariant halves states |
| **Out of Boundary Paths** | 576 | Forward probability | Count steps exiting the grid | Don't re-enter; mod at every step |

---

# Pattern 9 — Tree DP

## Theory

- **Core idea:** Subtrees are independent subproblems. Process in **DFS post-order** — children before parent.
- **Pattern:** Define `dfs(node) → (state_A, state_B)`. Parent combines children's states.
- **Space:** O(h) call stack only — no table needed.

## Implementations

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def house_robber_iii(root: Optional[TreeNode]) -> int:
    def dfs(node):
        if not node:
            return 0, 0         # (rob_node, skip_node)
        l_rob, l_skip = dfs(node.left)
        r_rob, r_skip = dfs(node.right)
        rob  = node.val + l_skip + r_skip
        skip = max(l_rob, l_skip) + max(r_rob, r_skip)
        return rob, skip
    return max(dfs(root))

def max_path_sum(root: Optional[TreeNode]) -> int:
    best = [float('-inf')]
    def dfs(node) -> int:
        if not node: return 0
        left  = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)
        best[0] = max(best[0], node.val + left + right)
        return node.val + max(left, right)
    dfs(root)
    return best[0]

def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    diameter = [0]
    def dfs(node) -> int:
        if not node: return 0
        left, right = dfs(node.left), dfs(node.right)
        diameter[0] = max(diameter[0], left + right)
        return 1 + max(left, right)
    dfs(root)
    return diameter[0]

def binary_tree_cameras(root: Optional[TreeNode]) -> int:
    cameras = [0]
    COVERED, HAS_CAMERA, NOT_COVERED = 0, 1, 2
    def dfs(node) -> int:
        if not node: return COVERED
        left, right = dfs(node.left), dfs(node.right)
        if left == NOT_COVERED or right == NOT_COVERED:
            cameras[0] += 1
            return HAS_CAMERA
        if left == HAS_CAMERA or right == HAS_CAMERA:
            return COVERED
        return NOT_COVERED
    if dfs(root) == NOT_COVERED:
        cameras[0] += 1
    return cameras[0]

def rob_house_tree(root: Optional[TreeNode]) -> int:
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def dp(node):
        if not node: return 0
        rob = node.val
        if node.left:
            rob += dp(node.left.left) + dp(node.left.right)
        if node.right:
            rob += dp(node.right.left) + dp(node.right.right)
        skip = dp(node.left) + dp(node.right)
        return max(rob, skip)
    return dp(root)
```

## Tree DP Variations

| Problem | States returned | Combination |
| :--- | :--- | :--- |
| **House Robber III `🎯 T2`** | `(rob, skip)` | `rob=val+l_skip+r_skip`; `skip=max(l)+max(r)` |
| **Max Path Sum `🎯 T2`** | Best downward chain | Global max updated through node |
| **Diameter `🎯 T2`** | Depth | `diameter = max(l_depth + r_depth)` |
| **Binary Tree Cameras `🎯 T2`** | `covered/has_camera/not_covered` | Greedy from leaves; place camera if child uncovered |
| **Largest BST Subtree** | `(min, max, size, is_bst)` | Check BST property at each node |

---

# Pattern 10 — Bitmask DP

## Theory

- **Core idea:** When graph is small (N ≤ 20), encode visited nodes as bitmask integer.
- **State:** `dp[mask][v]` = cost to reach node `v` having visited exactly nodes in `mask`.

## Implementations

```python
def tsp_memo(dist):
    from functools import lru_cache
    n = len(dist)
    @lru_cache(maxsize=None)
    def dp(visited, curr):
        if visited == (1 << n) - 1:
            return dist[curr][0]
        best = float('inf')
        for nxt in range(n):
            if not (visited >> nxt & 1):
                best = min(best, dist[curr][nxt] + dp(visited | (1 << nxt), nxt))
        return best
    return dp(1, 0)

def shortest_path_all_nodes(graph: list[list[int]]) -> int:
    n = len(graph)
    INF = float('inf')
    from collections import deque
    dist = [[INF] * n for _ in range(n)]
    for src in range(n):
        dist[src][src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if dist[src][v] == INF:
                    dist[src][v] = dist[src][u] + 1
                    q.append(v)
    FULL = (1 << n) - 1
    dp = [[INF] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 0
    for mask in range(1, 1 << n):
        for u in range(n):
            if dp[mask][u] == INF or not (mask >> u & 1): continue
            for v in range(n):
                if mask >> v & 1: continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])
    return min(dp[FULL])

def minimum_xor_sum(nums1: list[int], nums2: list[int]) -> int:
    n = len(nums1)
    dp = [float('inf')] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        i = bin(mask).count('1')
        if i >= n: continue
        for j in range(n):
            if mask >> j & 1: continue
            dp[mask | (1 << j)] = min(dp[mask | (1 << j)],
                                       dp[mask] + (nums1[i] ^ nums2[j]))
    return dp[(1 << n) - 1]
```

> [!TIP]
> **Subset enumeration trick:** To iterate over all subsets of a mask `m`, use `sub = m; while sub > 0: process(sub); sub = (sub - 1) & m`. This runs in O(3^N) total over all masks.

## Bitmask DP Problems

| Problem | State | N limit |
| :--- | :--- | :--- |
| **Travelling Salesman** | `dp[mask][city]` | N ≤ 20 |
| **Minimum XOR Sum (assignment)** | `dp[mask]` = cost assigning first `popcount(mask)` | N ≤ 14 |
| **Stickers to Spell Word** | `dp[mask]` = min stickers to cover chars in mask | word ≤ 15 |

---

# Pattern 11 — Stock Trading State Machine

## Theory

All 6 stock variants share the same `dp[i][k][holding]` state machine.

- **State:** `dp[i][k][holding]` = max profit on day `i` with `k` transactions remaining and `holding` (0/1).
- **Key rule:** Decrement `k` on **buy** (not sell).

## Implementations

```python
def max_profit_1(prices: list[int]) -> int:
    min_price, max_profit = float('inf'), 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return max_profit

def max_profit_2(prices: list[int]) -> int:
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free

def max_profit_3(prices: list[int]) -> int:
    buy1 = buy2 = float('-inf')
    sell1 = sell2 = 0
    for p in prices:
        buy1  = max(buy1, -p)
        sell1 = max(sell1, buy1 + p)
        buy2  = max(buy2, sell1 - p)
        sell2 = max(sell2, buy2 + p)
    return sell2

def max_profit_4(k: int, prices: list[int]) -> int:
    n = len(prices)
    if k >= n // 2:
        return sum(max(0, prices[i]-prices[i-1]) for i in range(1, n))
    dp = [[0, float('-inf')] for _ in range(k + 1)]
    for p in prices:
        for j in range(k, 0, -1):   # backward prevents reuse
            dp[j][0] = max(dp[j][0], dp[j][1] + p)
            dp[j][1] = max(dp[j][1], dp[j-1][0] - p)
    return dp[k][0]

def max_profit_cooldown(prices: list[int]) -> int:
    hold, sold, rest = float('-inf'), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
    return max(sold, rest)

def max_profit_with_fee(prices: list[int], fee: int) -> int:
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold = max(hold, free - p)
        free = max(free, hold + p - fee)
    return free
```

## Stock Variants Table

| Variant | k | Extra | States | Key Bug to Avoid |
| :--- | :--- | :--- | :--- | :--- |
| **I** (LC 121) | 1 | None | Greedy | Forgetting edge case: empty array |
| **II** (LC 122) | ∞ | None | `hold, free` | Buying same day as selling = 0 gain |
| **III** (LC 123) | 2 | None | `buy1, sell1, buy2, sell2` | Not chaining `sell1` into `buy2` |
| **IV** (LC 188) | K | None | `dp[k][0/1]` | Forward k-loop causes reuse (must go backward) |
| **Cooldown** (LC 309) | ∞ | 1-day wait | `hold, sold, rest` | Using `sold` in same iteration (use `prev_sold`) |
| **Fee** (LC 714) | ∞ | Fee per tx | `hold, free` | Applying fee at both buy and sell |

---

# Pattern 12 — String & Palindrome DP

## Theory

**Two flavors:**
1. **Single-string palindrome DP** — `dp[i][j]` represents a property of `s[i..j]`. Fill by increasing length.
2. **Two-string matching DP** — `dp[i][j]` represents matching/transforming `s1[:i]` and `s2[:j]`. Fill row by row.

**Palindrome key insight:** `s[i..j]` is a palindrome iff `s[i] == s[j]` AND `s[i+1..j-1]` is a palindrome.

## Part A — Palindrome Problems

```python
def longest_palindromic_substring_expand(s: str) -> str:
    def expand(l: int, r: int) -> tuple:
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return l + 1, r - 1
    start, end = 0, 0
    for i in range(len(s)):
        l1, r1 = expand(i, i)
        l2, r2 = expand(i, i + 1)
        if r1 - l1 > end - start: start, end = l1, r1
        if r2 - l2 > end - start: start, end = l2, r2
    return s[start:end+1]

def longest_palindromic_subsequence(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i+1][j-1] if length > 2 else 0)
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1]

def min_insertions_palindrome(s: str) -> int:
    return len(s) - longest_palindromic_subsequence(s)

def count_substrings(s: str) -> int:
    n = len(s)
    count = 0
    def expand_count(l: int, r: int) -> int:
        cnt = 0
        while l >= 0 and r < n and s[l] == s[r]:
            cnt += 1; l -= 1; r += 1
        return cnt
    for i in range(n):
        count += expand_count(i, i)
        count += expand_count(i, i+1)
    return count

def min_cut(s: str) -> int:
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = (s[i] == s[j]) and (j - i < 2 or is_pal[i+1][j-1])
    cut = list(range(n))
    for i in range(1, n):
        if is_pal[0][i]:
            cut[i] = 0
            continue
        for j in range(1, i + 1):
            if is_pal[j][i]:
                cut[i] = min(cut[i], cut[j-1] + 1)
    return cut[n-1]

def palindrome_partition_iii(s: str, k: int) -> int:
    n = len(s)
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def cost(l: int, r: int) -> int:
        changes = 0
        while l < r:
            if s[l] != s[r]: changes += 1
            l += 1; r -= 1
        return changes
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            for m in range(j - 1, i):
                dp[i][j] = min(dp[i][j], dp[m][j-1] + cost(m, i-1))
    return dp[n][k]
```

> [!TIP]
> **Manacher's Algorithm** finds all palindromes in O(N). For interviews, mention it as the optimal solution but implement expand-around-center (O(N²) time, O(1) space) unless asked for optimal.

> [!TIP]
> Both insertion and deletion to make a palindrome have the same minimum count = `len(s) - LPS(s)`.

## Part B — Pattern Matching DP

```python
def is_match_regex(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i][j-2]
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    return dp[m][n]

def is_match_wildcard(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
            elif p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    return dp[m][n]
```

> [!CAUTION]
> **`*` in regex means zero OR MORE of the PRECEDING char.** Always look at `p[j-2]` when `p[j-1] == '*'`. The "zero occurrences" case (`dp[i][j-2]`) skips both `*` AND the preceding char.

> [!TIP]
> **Regex vs Wildcard:** In regex, `*` requires a preceding char to repeat. In wildcard, `*` is standalone and matches any sequence. Transitions differ: regex checks `p[j-2]`; wildcard uses `dp[i-1][j] or dp[i][j-1]`.

## String & Palindrome DP Interview Questions

| Problem | LC # | Pattern | Click Moment | Gotcha |
| :--- | :--- | :--- | :--- | :--- |
| **Longest Palindromic Substring `🎯 T2`** | 5 | Expand center | `is_pal[i][j]` filled by length | Expand-around-center is O(1) space |
| **Longest Palindromic Subsequence `🎯 T2`** | 516 | Interval DP | `LCS(s, rev(s))` shortcut | Single chars: `dp[i][i] = 1` base case |
| **Min Insertions for Palindrome** | 1312 | LPS reduction | `len - LPS` | Equivalent to min deletions |
| **Count Palindromic Substrings** | 647 | Expand-center | Count from each center | 2n-1 centers |
| **Palindrome Partitioning II `🎯 T2`** | 132 | Interval + linear | Precompute `is_pal`; linear `cut[]` | If `is_pal[0][i]`, no cut needed |
| **Palindrome Partitioning III `🎯 T2`** | 1278 | 2D DP + cost | `cost(l, r)` = chars to fix | `cost` function is O(N) per call; memoize |
| **Regular Expression Matching** | 10 | 2D string DP | `*` = zero-or-more of PRECEDING char | Base case: leading `a*b*` matches `""` |
| **Wildcard Matching** | 44 | 2D string DP | `*` = any sequence | `dp[i-1][j]`: `*` matches s[i]; `dp[i][j-1]`: `*` empty |
| **Distinct Subsequences `🎯 T2`** | 115 | 2D DP, counting | Add ways when chars match | `dp[i][0] = 1` (empty t always subseq) |
| **Interleaving String `🎯 T2`** | 97 | 2D DP, bool | Two sources for each `s3` char | Check `m+n == len(s3)` first |

---

# Common DP Bugs — The 12

> [!CAUTION]
> These are the 12 most common DP bugs in interviews.

1. **Backward vs Forward in knapsack 1D** — 0/1 needs backward; unbounded needs forward.
2. **Wrong base case for count problems** — `dp[0] = 1` (empty = one way), not 0.
3. **Missing modulo** — In counting problems, mod every `+=` and `*` operation.
4. **Off-by-one in 1-indexed tables** — `dp[i]` corresponds to `arr[i-1]`; base cases at row/col 0.
5. **Wrong interval DP fill order** — Always fill by increasing interval length, not by row.
6. **Regex `*` zero-occurrence** — `dp[i][j-2]` skips both `*` and the preceding element.
7. **Edit distance base cases `🎯 T2`** — `dp[0][j] = j` and `dp[i][0] = i` (full insert/delete cost).
9. **Dungeon forward DP is impossible** — Forward doesn't know minimum HP required; must fill backwards.
10. **Stock cooldown uses prev_sold** — Save `prev_sold = sold` before updating `sold`; else uses same-day value.
11. **LIS tails ≠ actual LIS** — `tails` array only gives correct length; to reconstruct, use `parent[]` in O(N²).

---

## Space Optimization Patterns

| DP Type | Original | Optimized | Note |
| :--- | :--- | :--- | :--- |
| Linear 1D | O(N) array | O(1) two variables | Only when dp[i] uses dp[i-1] only |
| 0/1 Knapsack | O(N×W) table | O(W) single row | Iterate w backward |
| Unbounded Knapsack | O(N×W) table | O(W) single row | Iterate w forward |
| LCS / Edit Distance | O(M×N) table | O(N) two rows | prev row + curr row |
| LPS / Interval DP | O(N²) | Not possible | Needs diagonal access |
| Grid (Min Path, Unique Paths) | O(M×N) | O(N) one row | Update in place |
| Maximal Square | O(M×N) | O(N) + 1 scalar `prev` | `prev` = `dp[r-1][c-1]` |

### Iteration Direction Rules

| DP Type | Inner Loop Direction | Why |
| :--- | :--- | :--- |
| 0/1 Knapsack | `w` from high to low | Prevent same item reuse |
| Unbounded Knapsack | `w` from low to high | Allow same item reuse |
| LCS / Edit | Row by row (any direction) | Reads from top/left only |
| Interval DP | Outer: length asc; Inner: `i` asc | Short intervals before long |
| Palindrome table | `i` from high to low, `j` from `i` to `n` | `dp[i+1][j-1]` must exist first |
| Dungeon | Bottom-right to top-left | Need successor values |
| Stock Cooldown | Forward (day by day) | State machine, save `prev_sold` |

---

## SDE-3 Interview Communication Framework (8-Step)

When given a DP problem in an interview:

1. **Restate:** Confirm what you're minimizing/maximizing/counting.
2. **Identify pattern:** Name the pattern (knapsack, interval, bitmask…) — do this out loud.
3. **Define state:** Write `dp[i][j] = ...` in one sentence.
4. **Write recurrence:** Two cases: match/take vs skip/split.
5. **Identify base cases:** Boundaries where recursion stops.
6. **Determine fill order:** Which loop goes outside; which inside.
6. **Code bottom-up:** Skip memoization unless interviewer asks for top-down first.
7. **Space optimize:** Always offer to reduce space; don't apply until base solution is correct.

---

## When NOT to Use DP

| Situation | Better Approach |
| :--- | :--- |
| Always take the locally best option | Greedy (interval scheduling, fractional knapsack) |
| Subproblems are independent (no overlap) | Divide & Conquer |
| Problem has no optimal substructure | Brute force / backtracking |
| Need to find an actual path, not just optimal | BFS / Dijkstra |
| Constraints too large for state space | Math / combinatorics formula |

---

## Complexity Quick Reference

| Pattern | Time | Space (optimized) |
| :--- | :--- | :--- |
| Linear DP | O(N) | O(1) |
| 0/1 / Unbounded Knapsack | O(N×W) | O(W) |
| LCS / Edit Distance | O(M×N) | O(N) |
| LIS O(N²) | O(N²) | O(N) |
| LIS O(N log N) | O(N log N) | O(N) |
| Interval DP | O(N³) | O(N²) |
| Grid DP | O(M×N) | O(N) |
| Tree DP | O(N) | O(h) |
| Bitmask DP | O(2^N × N²) | O(2^N × N) |
| Probability DP | O(states × transitions) | O(states) |

---

## Interview Questions Bank

### Level 1 — Foundation (Pattern Recognition)

| Problem | Pattern | Key Insight |
| :--- | :--- | :--- |
| **Climbing Stairs `🎯 T2`** | Linear DP | Fibonacci: `dp[i] = dp[i-1] + dp[i-2]` |
| **Min Cost Climbing Stairs** | Linear DP | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` |
| **Subset Sum Problem `🎯 T2`** | 0/1 Knapsack | `dp[i][j]` = is sum `j` possible with first `i` items? |
| **Coin Change (Min Coins) `🎯 T2`** | Unbounded Knapsack | `dp[i] = 1 + min(dp[i - coin])` |
| **Longest Common Subsequence `🎯 T2`** | LCS | `s1[i] == s2[j] ? 1 + diag : max(top, left)` |
| **Maximum Subarray (Kadane) `🎯 T2`** | Kadane | `best = max(x, best + x)` |

### Level 2 — SDE-2 Standard

| Problem | Pattern | The Twist |
| :--- | :--- | :--- |
| **Partition Equal Subset Sum `🎯 T2`** | 0/1 Knapsack | Target = `total_sum / 2` |
| **Target Sum `🎯 T2`** | 0/1 Knapsack | Math: `P - N = target` → `2P = target + total` |
| **Coin Change II (Total Ways) `🎯 T2`** | Unbounded Knapsack | `dp[i] += dp[i - coin]` (coins outer = combinations) |
| **Edit Distance `🎯 T2`** | LCS Family | Three choices: insert, delete, replace |
| **Longest Palindromic Subsequence `🎯 T2`** | LCS Family | `LCS(s, reverse(s))` |
| **House Robber II `🎯 T2`** | Linear DP | Circular constraint: two passes exclude ends |
| **Maximal Square `🎯 T2`** | Grid DP | `min(3 neighbors) + 1` |
| **Word Break `🎯 T2`** | Linear DP | `dp[i] = any(dp[j] and s[j:i] in dict)` |
| **LIS `🎯 T2`** | LIS | O(N log N) with patience sort |
| **Russian Doll Envelopes** | LIS | Sort (w asc, h desc); LIS on h |

### Level 3 — SDE-3 / Staff Level

| Problem | Pattern | Complexity / Optimization |
| :--- | :--- | :--- |
| **Numbers At Most N Given Digit Set** | **Binary Tree Maximum Path Sum `🎯 T2`** | Tree DP | Single-arm gain vs full-path through node |
| **Stock with Cooldown** | State Machine | 3 states: `hold`, `sold`, `rest` |
| **Cherry Pickup II** | Grid DP | Two travelers 3D→2D compression |
| **Palindrome Partitioning III `🎯 T2`** | 2D DP + cost | Cost function `cost(l,r)` memoized |
| **Stone Game III** | Minimax DP | `dp[i]` = score advantage; Alice/Bob generalized |
| **Jump Game VI `🎯 T2`** | Deque Optimization | Monotonic deque; O(N) |

---

## All-Pattern Interview Questions Table

| Question | Pattern | Core Logic | Trickiness |
| :--- | :--- | :--- | :--- |
| **0/1 Knapsack** | 0/1 Knapsack | `dp[i][w] = max(skip, take)` | Backward inner loop in 1D |
| **Subset Sum `🎯 T2`** | 0/1 Knapsack | Boolean `dp[sum]` | `dp[0] = True`; empty subset valid |
| **Partition Equal Subset `🎯 T2`** | 0/1 Knapsack | Subset sum to `total//2` | Odd total → False immediately |
| **Target Sum (±) `🎯 T2`** | 0/1 Knapsack | Count subsets to `(total+target)//2` | Parity + impossibility check |
| **Coin Change I `🎯 T2`** | Unbounded | `dp[w] = min(dp[w], 1 + dp[w-c])` | Forward loop; init rest to `inf` |
| **Coin Change II `🎯 T2`** | Unbounded | `dp[w] += dp[w-c]`; coins outer | Coin outer = combinations |
| **Climbing Stairs `🎯 T2`** | Fibonacci | `dp[i] = dp[i-1] + dp[i-2]` | Base: `dp[1]=1, dp[2]=2` |
| **House Robber `🎯 T2`** | Fibonacci | `dp[i] = max(dp[i-1], nums[i]+dp[i-2])` | Two-variable rolling |
| **House Robber II `🎯 T2`** | Fibonacci | Two passes: exclude first or last | Only one of first/last can be robbed |
| **Decode Ways `🎯 T2`** | Fibonacci | One-digit + two-digit branches | `'0'` alone invalid |
| **LCS `🎯 T2`** | LCS | Match → `dp[i-1][j-1]+1`; else `max` | 1-indexed table |
| **Edit Distance `🎯 T2`** | LCS | Replace=diagonal+1; insert/delete=axis+1 | All three ops; full base case |
| **LPS** | LCS | `LCS(s, reversed(s))` | Elegant reduction |
| **LIS O(N²)** | LIS | `dp[i] = 1 + max(dp[j])` | Answer = `max(dp)` not `dp[n-1]` |
| **LIS O(N log N)** | LIS (patience) | `bisect_left` on `tails` | `tails` ≠ actual LIS |
| **Russian Doll Envelopes** | LIS | Sort (w asc, h desc); LIS on h | Descending h prevents same-width |
| **Max Subarray (Kadane)** | Kadane | `end_here = max(x, end_here+x)` | Start fresh when extending worse |
| **Max Product Subarray** | Kadane | Track `cur_max` and `cur_min` | Negative × negative = positive |
| **Circular Subarray Max** | Kadane | `max(straight, total - min_subarray)` | All-negative edge case |
| **Palindrome Partitioning II `🎯 T2`** | Interval DP | Precompute palindrome table first | `is_pal[0][i]` → no cut needed |
| **Unique Paths `🎯 T2`** | Grid DP | `dp[r][c] = dp[r-1][c] + dp[r][c-1]` | Init row 0 and col 0 to 1 |
| **Min Path Sum** | Grid DP | Accumulate costs | Init first row/col explicitly |
| **Dungeon Game** | Grid DP | Reverse fill: need successor values | Forward is impossible |
| **Maximal Square `🎯 T2`** | Grid DP | `min(left, top, diag) + 1` | Entry is a string; cast to int |
| **House Robber III `🎯 T2`** | Tree DP | `dfs → (rob, skip)` | Return pair from DFS |
| **Max Path Sum `🎯 T2`** | Tree DP | Ignore negative subtrees | Global max updated per node |
| **Binary Tree Cameras `🎯 T2`** | Tree DP | 3 states: covered/has_camera/not_covered | Root NOT_COVERED needs +1 |
| **Stock I** | State Machine | Greedy: track min price | Edge case: empty array |
| **Stock II** | State Machine | `hold, free` two states | Unlimited transactions |
| **Stock III** | State Machine | `buy1, sell1, buy2, sell2` | Chain sell1 into buy2 |
| **Stock IV** | State Machine | `dp[k][0/1]` backward k-loop | Forward k causes reuse |
| **Stock Cooldown** | State Machine | 3 states; save `prev_sold` | Same-iteration update bug |
| **Egg Drop** | Inverted DP | `dp[m][k] = dp[m-1][k-1]+1+dp[m-1][k]` | Invert: max floors per moves |
| **Knight Probability** | Probability DP | Propagate forward | Off-board just discarded |
| **Stone Game III** | Game / Minimax | Advantage DP | Take 1/2/3; score − opponent |
| **Jump Game VI `🎯 T2`** | Deque Opt | Monotonic deque for window max | Pop front when expired |
