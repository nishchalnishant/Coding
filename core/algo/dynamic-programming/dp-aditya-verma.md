# Dynamic Programming — Aditya Verma Pattern Playbook

Pattern-first DP: name the pattern, write the recurrence, code bottom-up, optimize space. For the main SDE-3 DP guide see [README.md](README.md).

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

**Transition direction:** Bottom-up fills small subproblems first. Choose loop order so when you compute `dp[i][w]`, every value on the right-hand side is already filled.

---

## Pattern Map — Choose in 30 Seconds

| What the problem asks | Pattern |
| :--- | :--- |
| Pick items (each once) to hit capacity / sum | **0/1 Knapsack** |
| Pick items (unlimited copies) to hit capacity | **Unbounded Knapsack** |
| `dp[i]` depends on `dp[i-1]`, `dp[i-2]` | **Fibonacci / Linear** |
| Two sequences — align and match | **LCS family** |
| One sequence — longest increasing / longest chain | **LIS** |
| Best subarray ending at `i` | **Kadane** |
| Split interval `[i,j]` at every `k` | **MCM / Interval DP** |
| Subtree answers combined at root | **DP on Trees** |
| Node + extra state (mask, moves) | **DP on Graphs / Bitmask** |

---

## Pattern 1 — 0/1 Knapsack

### Theory

**Core idea:** Each item has a binary choice — include it once or skip it. Taking an item reduces remaining capacity; skipping does not.

**State:** `dp[i][w]` = maximum value achievable using only the first `i` items with capacity exactly `w`.

**Recurrence:**
```
dp[i][w] = dp[i-1][w]                               # skip item i
          if weight[i-1] <= w:
              dp[i][w] = max(dp[i][w],
                             value[i-1] + dp[i-1][w - weight[i-1]])  # take item i
```

**Base case:** `dp[0][w] = 0` for all `w` (no items → zero value).

**Space optimization:** Collapse to 1D `dp[w]`. Iterate `w` from **high → low** so that `dp[w - weight[i]]` still refers to the *previous item's* row (not the current item being added).

```python
def knapsack_01(weights: list[int], values: list[int], W: int) -> int:
    n = len(weights)
    # 2D — easier to derive
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i-1][w]                           # skip
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                               values[i-1] + dp[i-1][w - weights[i-1]])  # take
    return dp[n][W]

def knapsack_01_space(weights: list[int], values: list[int], W: int) -> int:
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):              # BACKWARD — 0/1 invariant
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]
```

> [!CAUTION]
> **Backward vs Forward loop:** In 1D, iterating `w` backward (high → low) ensures each item is used at most once. Iterating forward (low → high) allows the same item to be picked multiple times — that is the unbounded knapsack. Getting this backwards is the #1 knapsack bug.

**Reconstruction (which items were picked):**
```python
def knapsack_reconstruct(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], values[i-1] + dp[i-1][w - weights[i-1]])
    # Traceback
    items, w = [], W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:   # item i was taken
            items.append(i - 1)
            w -= weights[i - 1]
    return dp[n][W], items[::-1]
```

### Variations & Interview Problems

| Problem | Transform | Key Insight |
| :--- | :--- | :--- |
| **Subset Sum** | Boolean knapsack; `dp[sum]` = True/False | `dp[0] = True`; iterate sum descending |
| **Partition Equal Subset Sum** | Subset sum to `total // 2` | Odd total → impossible immediately |
| **Target Sum (±assign)** | Count subsets with sum `(total + target) / 2` | Parity check first; count, not max |
| **Count Subsets with Given Sum** | Add ways: `dp[w] += dp[w - weight]` | `dp[0] = 1` (empty subset = one way) |
| **Last Stone Weight II** | Partition to minimize `|S1 - S2|` = `total - 2 * max_S1_leq_half` | Subset sum variant |
| **Ones and Zeroes** | 2D knapsack: capacity is `(m zeros, n ones)` | `dp[i][j]` = max strings using ≤ i zeros, ≤ j ones |

---

## Pattern 2 — Unbounded Knapsack

### Theory

**Core idea:** Each item type can be picked **unlimited** times. After taking one copy of item `i`, you can pick item `i` again — so recurse on the same index `i`, not `i-1`.

**Recurrence:**
```
dp[i][w] = dp[i-1][w]                               # skip item i entirely
          if weight[i-1] <= w:
              dp[i][w] = max(dp[i][w],
                             value[i-1] + dp[i][w - weight[i-1]])   # take, stay at i
```

**Space optimization:** 1D, iterate `w` from **low → high** (forward). Because we stay at row `i` when taking, `dp[w - weight[i]]` should already include the current item — forward iteration provides this.

```python
def knapsack_unbounded(weights: list[int], values: list[int], W: int) -> int:
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(weights[i], W + 1):           # FORWARD — unbounded invariant
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
> **Combinations vs Permutations:** `coins` outer, `amount` inner → counts combinations (unordered). `amount` outer, `coins` inner → counts permutations (ordered). The problem "Coin Change 2" wants combinations.

### Variations & Interview Problems

| Problem | Loop Order | Key Insight |
| :--- | :--- | :--- |
| **Coin Change I** (min coins) | Coins outer, amount forward | `dp[0]=0`, rest `inf`; take `min` |
| **Coin Change II** (count ways) | Coins outer, amount forward | `dp[0]=1`; takes `+= ` not `max` |
| **Rod Cutting** (max value) | Lengths outer, capacity forward | Identical to unbounded knapsack; length = weight |
| **Integer Break** (max product) | Split 1…n; `dp[i] = max(j*(i-j), j*dp[i-j])` | Greedy: break into 3s (AM-GM), but DP is safe |
| **Perfect Squares** (min count) | Squares outer, amount forward | Same as coin change with coins = 1,4,9,16… |

---

## Pattern 3 — Fibonacci / Linear DP

### Theory

**Core idea:** `dp[i]` depends on a **fixed small window** of previous values (`dp[i-1]`, `dp[i-2]`, …). No item-weight two-dimensional state; the dimension is purely **position**.

**Signature recurrence:**
```
dp[i] = f(dp[i-1], dp[i-2], nums[i])
```

**Space optimization:** Almost always reducible to O(1) or O(k) variables (two-variable rolling).

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def house_robber(nums: list[int]) -> int:
    prev2, prev1 = 0, 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

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

def house_robber_ii(nums: list[int]) -> int:
    def rob_linear(arr):
        prev2, prev1 = 0, 0
        for x in arr:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
    if len(nums) == 1:
        return nums[0]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))  # exclude first or last
```

> [!TIP]
> **House Robber II (circle):** Run the linear robber twice — once on `nums[:-1]` and once on `nums[1:]`. Take the max. The circle constraint means you can't rob both first and last house; excluding one end from each run handles it.

### Variations

| Problem | Recurrence | Note |
| :--- | :--- | :--- |
| **Climbing Stairs** | `dp[i] = dp[i-1] + dp[i-2]` | Fibonacci exactly |
| **Min Cost Climbing Stairs** | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` | Can start at step 0 or 1 |
| **Decode Ways** | One + two digit branches | `'0'` as first digit kills branch |
| **House Robber I** | `dp[i] = max(dp[i-1], nums[i]+dp[i-2])` | — |
| **House Robber II** | Two linear passes, exclude ends | Classic circle trick |
| **Paint Fence / Paint House** | Track last-color state | Add dimension for color constraint |

---

## Pattern 4 — LCS Family

### Theory

**Core idea:** Two sequences `s1[0..m]` and `s2[0..n]`. At each position pair `(i, j)`, either the characters **match** (extend the common subsequence) or you **skip** one side (take the better of advancing `i` or advancing `j`).

**State:** `dp[i][j]` = LCS length of `s1[:i]` and `s2[:j]`.

**Recurrence:**
```
if s1[i-1] == s2[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]      # characters match — extend
else:
    dp[i][j] = max(dp[i-1][j],        # skip s1[i]
                   dp[i][j-1])         # skip s2[j]
```

**Base case:** `dp[0][j] = dp[i][0] = 0` (empty prefix has no common characters).

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

def shortest_common_supersequence(s1: str, s2: str) -> str:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    # Reconstruct SCS
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

def edit_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i     # delete all of word1
    for j in range(n + 1): dp[0][j] = j     # insert all of word2
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # delete from word1
                                    dp[i][j-1],    # insert into word1
                                    dp[i-1][j-1])  # replace
    return dp[m][n]

def longest_palindromic_subsequence(s: str) -> int:
    return lcs(s, s[::-1])           # LPS = LCS(s, reverse(s))
```

### LCS-Family Derivations

| Problem | Formula / Derivation |
| :--- | :--- |
| **LCS length** | `dp[i][j]` directly |
| **Print LCS** | Traceback: match → diagonal; else → max of up/left |
| **Shortest Common Supersequence** | Length = `m + n - LCS`; reconstruct by merging |
| **Min insertions to make palindrome** | `len(s) - LPS(s)` |
| **Min deletions to make palindrome** | `len(s) - LPS(s)` |
| **Edit distance** | Replace = diagonal + 1; insert/delete = +1 on axis |
| **Distinct subsequences** | Count ways `s` contains `t` as subseq: add, don't max |
| **Longest Common Substring** | Same grid but reset to 0 on mismatch; track global max |
| **Interleaving Strings** | `dp[i][j]` = can `s1[:i]+s2[:j]` form `s3[:i+j]` |

---

## Pattern 5 — LIS (Longest Increasing Subsequence)

### Theory

**Core idea:** One array; find the length of the longest strictly increasing subsequence. Two approaches with different trade-offs.

**O(N²) DP:**
```
dp[i] = length of LIS ending at index i
dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])
```

**O(N log N) Patience Sorting:**
Maintain `tails[]` where `tails[k]` = smallest tail value of any increasing subsequence of length `k+1`. Binary search to find where to place each new element.

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
        pos = bisect.bisect_left(tails, x)   # strict LIS: bisect_left
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)

def lis_nlogn_non_decreasing(nums: list[int]) -> int:
    tails = []
    for x in nums:
        pos = bisect.bisect_right(tails, x)  # non-strict: bisect_right
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

### LIS-Family Problems

| Problem | Key Transform |
| :--- | :--- |
| **LIS (strict)** | `bisect_left` in patience sort |
| **LIS (non-decreasing)** | `bisect_right` in patience sort |
| **Count LIS** | O(N²): track both `dp[i]` (length) and `cnt[i]` (count) |
| **Longest Chain of Pairs** | Sort by second element; LIS on first element where pairs don't overlap |
| **Russian Doll Envelopes** | Sort (w asc, h desc); LIS on h |
| **Number of Longest Increasing Subsequences** | Two arrays: `length[i]` and `count[i]`; aggregate at end |

---

## Pattern 6 — Kadane (Best Subarray Ending at i)

### Theory

**Core idea:** The globally optimal subarray can be found by tracking the best subarray that **ends** at each position. At position `i`, either extend the previous best subarray or start fresh from `i`.

**Recurrence:**
```
ending_here[i] = max(nums[i], ending_here[i-1] + nums[i])
global_max = max(global_max, ending_here[i])
```

**Space:** O(1) — just two variables.

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
    # Case 1: subarray doesn't wrap → standard Kadane
    # Case 2: subarray wraps → total - min_subarray
    total = sum(nums)
    max_straight = max_subarray(nums)
    # Invert signs to find min subarray
    min_sub = max_subarray([-x for x in nums])  # min_subarray = -max(-nums)
    max_wrap = total + min_sub                    # total - min_subarray
    # Edge case: all negative → max_wrap = 0 (empty), which is wrong; use max_straight
    return max(max_straight, max_wrap) if max_wrap != 0 else max_straight
```

> [!TIP]
> **Max Product Subarray:** Track both `cur_max` and `cur_min` at each step because a large negative × negative = large positive. All three candidates `(x, cur_max*x, cur_min*x)` must be evaluated on every step.

### Kadane Variations

| Problem | Twist |
| :--- | :--- |
| **Standard max subarray** | Base Kadane |
| **Max product subarray** | Track min and max (negatives flip sign) |
| **Circular subarray max** | `max(straight, total - min_subarray)` |
| **Return indices** | Track `cur_start`; update `best_start/end` on improvement |
| **At most K** | Prefix sums + sorted set (TreeMap); not pure Kadane |

---

## Pattern 7 — MCM / Interval DP

### Theory

**Core idea:** The problem is defined on a contiguous interval `[i, j]`. The optimal split point `k` divides the interval into `[i, k]` and `[k+1, j]`; you try all valid `k` and combine.

**State:** `dp[i][j]` = optimal cost/value for the interval `[i..j]`.

**Fill order:** By **increasing length** — `len = 2, 3, …, n`. For each length, iterate all starting positions `i`; `j = i + len - 1`.

**Recurrence:**
```
dp[i][j] = min over k in [i, j-1] of:
                dp[i][k] + dp[k+1][j] + cost(i, j, k)
```

```python
def matrix_chain_multiplication(dims: list[int]) -> int:
    # dims[i-1] x dims[i] = dimensions of matrix i (1-indexed)
    n = len(dims) - 1                       # number of matrices
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):          # fill by increasing length
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):           # try every split point
                cost = dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j]
                dp[i][j] = min(dp[i][j], cost)
    return dp[1][n]

def burst_balloons(nums: list[int]) -> int:
    # Add imaginary 1 at both ends
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):              # intervals of increasing length
        for i in range(0, n - length):
            j = i + length
            for k in range(i + 1, j):      # k = LAST balloon to burst in (i, j)
                coins = nums[i] * nums[k] * nums[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + coins + dp[k][j])
    return dp[0][n - 1]

def palindrome_partition_min_cuts(s: str) -> int:
    n = len(s)
    # Precompute palindrome table
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True
    # Min cuts
    dp = list(range(n))                     # dp[i] = min cuts for s[:i+1]
    for i in range(1, n):
        if is_pal[0][i]:
            dp[i] = 0
            continue
        for j in range(1, i + 1):
            if is_pal[j][i]:
                dp[i] = min(dp[i], dp[j-1] + 1)
    return dp[n - 1]
```

> [!CAUTION]
> **Burst Balloons gotcha:** `k` is the **last** balloon to burst within `(i, j)`, not the first. When `k` bursts, `nums[i]` and `nums[j]` are still present (they are boundaries, not yet burst), so the coins = `nums[i] * nums[k] * nums[j]`. Thinking of `k` as first burst gives wrong boundaries.

### Interval DP Variations

| Problem | Cost at split | State |
| :--- | :--- | :--- |
| **Matrix Chain Multiplication** | `dims[i-1]*dims[k]*dims[j]` | `dp[i][j]` = min multiplications |
| **Burst Balloons** | `nums[i]*nums[k]*nums[j]` | `k` = last to burst in open interval `(i,j)` |
| **Palindrome Partitioning II** | `1` if `s[j..i]` is palindrome | `dp[i]` = min cuts for prefix |
| **Strange Printer** | Reuse or overwrite | `dp[i][j]` = min turns to print `s[i..j]` |
| **Zuma Game** | Burst groups optimally | Interval DP with frequency tracking |
| **Optimal BST** | Key search probabilities | `dp[i][j]` = min expected search cost |

---

## Pattern 8 — DP on Trees

### Theory

**Core idea:** Subtrees are independent subproblems. Process in **DFS post-order** — children before parent. Return a tuple or pair representing different choices at each node (e.g., `(rob_this_node, skip_this_node)`).

**Pattern:** Define `dfs(node) → (state_A, state_B)` where states represent discrete choices. Parent combines children's states to compute its own.

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
        rob   = node.val + l_skip + r_skip       # take this node; skip children
        skip  = max(l_rob, l_skip) + max(r_rob, r_skip)  # skip this; children free to choose
        return rob, skip
    return max(dfs(root))

def max_path_sum(root: Optional[TreeNode]) -> int:
    best = [float('-inf')]
    def dfs(node) -> int:                        # returns best downward chain from node
        if not node:
            return 0
        left  = max(dfs(node.left), 0)           # ignore negative subtrees
        right = max(dfs(node.right), 0)
        best[0] = max(best[0], node.val + left + right)   # path through this node
        return node.val + max(left, right)        # best single chain upward
    dfs(root)
    return best[0]

def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    diameter = [0]
    def dfs(node) -> int:                        # returns depth of subtree
        if not node:
            return 0
        left, right = dfs(node.left), dfs(node.right)
        diameter[0] = max(diameter[0], left + right)
        return 1 + max(left, right)
    dfs(root)
    return diameter[0]

def binary_tree_cameras(root: Optional[TreeNode]) -> int:
    cameras = [0]
    COVERED, HAS_CAMERA, NOT_COVERED = 0, 1, 2
    def dfs(node) -> int:
        if not node:
            return COVERED
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
```

### Tree DP Variations

| Problem | States returned | Combination |
| :--- | :--- | :--- |
| **House Robber III** | `(rob, skip)` | Parent: `rob=val+l_skip+r_skip`; `skip=max(l)+max(r)` |
| **Max Path Sum** | Best downward chain | Global max updated through node |
| **Diameter** | Depth | `diameter = max(l_depth + r_depth)` |
| **Binary Tree Cameras** | `covered/has_camera/not_covered` | Greedy from leaves; place camera if child uncovered |
| **Largest BST Subtree** | `(min, max, size, is_bst)` | Check BST property at each node |
| **Tree DP for Independent Set** | `(with_node, without_node)` | Without: children free; With: children must be without |

---

## Pattern 9 — Bitmask / DP on Graphs

### Theory

**Core idea:** When the graph is small (N ≤ 20), encode the set of visited nodes as a bitmask integer. State = `(current_node, visited_mask)`. This allows O(2^N × N) DP over all subsets.

**State:** `dp[mask][v]` = cost/distance to reach node `v` having visited exactly the nodes in `mask`.

**Classic application:** Travelling Salesman Problem (TSP), Hamiltonian path, collecting all keys.

```python
def shortest_path_all_nodes(graph: list[list[int]]) -> int:
    n = len(graph)
    INF = float('inf')
    # BFS to precompute pairwise distances
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
    # Bitmask DP
    FULL = (1 << n) - 1
    dp = [[INF] * n for _ in range(1 << n)]
    for i in range(n):
        dp[1 << i][i] = 0               # start from any single node
    for mask in range(1, 1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask >> u & 1):
                continue
            for v in range(n):
                if mask >> v & 1:
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])
    return min(dp[FULL])

def minimum_xor_sum(nums1: list[int], nums2: list[int]) -> int:
    n = len(nums1)
    dp = [float('inf')] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        i = bin(mask).count('1')        # how many of nums2 assigned so far
        if i >= n:
            continue
        for j in range(n):
            if mask >> j & 1:
                continue                # nums2[j] already assigned
            dp[mask | (1 << j)] = min(dp[mask | (1 << j)],
                                       dp[mask] + (nums1[i] ^ nums2[j]))
    return dp[(1 << n) - 1]
```

> [!TIP]
> **Subset enumeration trick:** To iterate over all subsets of a mask `m`, use `sub = m; while sub > 0: process(sub); sub = (sub - 1) & m`. This runs in O(3^N) total over all masks — crucial for subset-sum style bitmask DP.

### Bitmask DP Problems

| Problem | State | N limit |
| :--- | :--- | :--- |
| **Travelling Salesman** | `dp[mask][city]` | N ≤ 20 |
| **Shortest Path Visiting All Nodes** | BFS with `(node, visited_mask)` | N ≤ 12 |
| **Minimum XOR Sum (assignment)** | `dp[mask]` = cost assigning first `popcount(mask)` of nums1 | N ≤ 14 |
| **Smallest Sufficient Team** | `dp[skill_mask]` = min team to cover skills | skills ≤ 26 |
| **Stickers to Spell Word** | `dp[mask]` = min stickers to cover chars in mask | word ≤ 15 |

---

## Pattern 10 — Stock Trading State Machine

### Theory

**Core idea:** All 6 stock variants share the same `dp[i][k][holding]` state machine. `holding = 0` (not holding) or `1` (holding). Constraints (k transactions, cooldown, fee) simply modify the transition rules.

**Key rule:** Decrement `k` on **buy** (not sell). This tracks remaining complete transactions.

```python
# Unlimited transactions — 2 states
def max_profit_ii(prices: list[int]) -> int:
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free

# K transactions — 2D DP with backward k-loop
def max_profit_iv(k: int, prices: list[int]) -> int:
    n = len(prices)
    if k >= n // 2:   # unlimited case
        return sum(max(0, prices[i]-prices[i-1]) for i in range(1, n))
    dp = [[0, float('-inf')] for _ in range(k + 1)]
    for p in prices:
        for j in range(k, 0, -1):   # backward prevents reuse of updated values
            dp[j][0] = max(dp[j][0], dp[j][1] + p)
            dp[j][1] = max(dp[j][1], dp[j-1][0] - p)
    return dp[k][0]

# Cooldown — 3 states
def max_profit_cooldown(prices: list[int]) -> int:
    hold, sold, rest = float('-inf'), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)   # prev_sold: can't buy same day as sell
    return max(sold, rest)
```

### Stock Variants Table

| Variant | k | Extra | States | Key Bug to Avoid |
| :--- | :--- | :--- | :--- | :--- |
| **I** | 1 | None | Greedy | Forgetting edge case: empty array |
| **II** | ∞ | None | `hold, free` | Buying same day as selling = 0 gain (allowed) |
| **III** | 2 | None | `buy1, sell1, buy2, sell2` | Not chaining `sell1` into `buy2` |
| **IV** | K | None | `dp[k][0/1]` | Forward k-loop causes reuse (must go backward) |
| **Cooldown** | ∞ | 1-day wait | `hold, sold, rest` | Using `sold` in same iteration (use `prev_sold`) |
| **Fee** | ∞ | Fee per tx | `hold, free` | Applying fee at both buy and sell |

See [stock-trading-dp.md](stock-trading-dp.md) for all 6 variants with full code.

---

## Pattern 11 — Palindrome DP

### Theory

**Core idea:** `s[i..j]` is a palindrome iff `s[i] == s[j]` AND `s[i+1..j-1]` is a palindrome. Fill `is_pal[i][j]` by increasing length. Then use it for:
- Counting palindromic substrings
- Longest palindromic subsequence (LCS shortcut)
- Minimum cuts to partition into palindromes

```python
def build_palindrome_table(s: str) -> list[list[bool]]:
    n = len(s)
    is_pal = [[False]*n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            is_pal[i][j] = (s[i] == s[j]) and (j - i < 2 or is_pal[i+1][j-1])
    return is_pal

def longest_palindromic_subsequence(s: str) -> int:
    """LCS(s, reverse(s)) — clean O(N²) reduction."""
    t = s[::-1]
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = dp[i-1][j-1]+1 if s[i-1]==t[j-1] else max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def min_cut_palindrome(s: str) -> int:
    n = len(s)
    is_pal = build_palindrome_table(s)
    cut = list(range(n))          # worst case: n-1 cuts
    for i in range(1, n):
        if is_pal[0][i]: cut[i] = 0; continue
        for j in range(1, i+1):
            if is_pal[j][i]:
                cut[i] = min(cut[i], cut[j-1] + 1)
    return cut[n-1]
```

### Palindrome DP Variations

| Problem | Formula | Notes |
| :--- | :--- | :--- |
| **Longest Palindromic Substring** | Expand around center O(1) space | DP table is O(N²) space; expand is better |
| **Longest Palindromic Subsequence** | `LCS(s, rev(s))` | Elegant reduction to LCS |
| **Count Palindromic Substrings** | 2n-1 expand-around-centers | Track both odd and even centers |
| **Min Insertions for Palindrome** | `len(s) - LPS(s)` | Same count as min deletions |
| **Min Cuts for Palindrome Partition** | Precompute `is_pal`; linear `cut[]` | If `is_pal[0][i]`: no cut needed for prefix |
| **Palindrome Partitioning III (K parts)** | 2D DP + `cost(l,r)` function | `cost` = chars to change to make palindrome |

See [string-palindrome-dp.md](string-palindrome-dp.md) for regex and wildcard matching too.

---


```text
Items: weight[1..n], value[1..n], capacity W

knapsack(i, w):
  if i == 0 or w == 0: return 0
  if weight[i] > w: return knapsack(i-1, w)        # can't take — forced skip
  return max(
    knapsack(i-1, w),                               # skip
    value[i] + knapsack(i-1, w - weight[i])         # take
  )

Bottom-up: dp[0..n][0..W], fill row by row
Space-optimized: dp[0..W], iterate w from W down to weight[i]
```

**Identification checklist:**
- [ ] Each item picked at most once → 0/1
- [ ] Items picked unlimited → Unbounded (forward loop)
- [ ] Ask is "max/min/count" not "which" → DP (reconstruction is a follow-up)
- [ ] Reduce sum problems: "subset sum to T" = knapsack with `value[i] = weight[i]`

---

## Knapsack → Subset Sum Reductions

| Formulation | `dp` meaning | Base | Transition |
| :--- | :--- | :--- | :--- |
| Max value ≤ W | `dp[w]` = max value | `dp[0] = 0` | `dp[w] = max(dp[w], v + dp[w-wt])` |
| Is sum T achievable? | `dp[w]` = True/False | `dp[0] = True` | `dp[w] \|= dp[w - num]` |
| Count subsets summing to T | `dp[w]` = # ways | `dp[0] = 1` | `dp[w] += dp[w - num]` |
| Min items summing to T | `dp[w]` = min items | `dp[0]=0`, rest `inf` | `dp[w] = min(dp[w], 1 + dp[w-num])` |

---

## Interview Questions — All Patterns

| Question | Pattern | Core Logic | Trickiness |
| :--- | :--- | :--- | :--- |
| **0/1 Knapsack** | 0/1 Knapsack | `dp[i][w] = max(skip, take)` | Backward inner loop in 1D — forward = unbounded bug |
| **Subset Sum** | 0/1 Knapsack | Boolean `dp[sum]` | `dp[0] = True`; empty subset always valid |
| **Partition Equal Subset Sum** | 0/1 Knapsack | Subset sum to `total//2` | Odd total → False immediately |
| **Target Sum (±)** | 0/1 Knapsack | Count subsets summing to `(total+target)//2` | Parity + impossibility check first |
| **Coin Change I** | Unbounded | `dp[w] = min(dp[w], 1 + dp[w-c])` | Forward loop; init rest to `inf`, `dp[0]=0` |
| **Coin Change II** | Unbounded | `dp[w] += dp[w-c]`; coins outer | Coin outer = combinations; amount outer = permutations |
| **Climbing Stairs** | Fibonacci | `dp[i] = dp[i-1] + dp[i-2]` | Base case: `dp[1]=1, dp[2]=2` |
| **House Robber** | Fibonacci | `dp[i] = max(dp[i-1], nums[i]+dp[i-2])` | Two-variable rolling; no array needed |
| **House Robber II** | Fibonacci | Two passes: exclude first or last | Only one of first/last can be robbed |
| **Decode Ways** | Fibonacci | One-digit + two-digit branches | `'0'` alone invalid; `'0x'` for x≥7 invalid |
| **LCS** | LCS | Match → `dp[i-1][j-1]+1`; else `max(up, left)` | 1-indexed table; `dp[0][*]=dp[*][0]=0` |
| **Edit Distance** | LCS | Replace=diagonal+1; insert/delete=axis+1 | All three ops; base case = full insert/delete |
| **LPS (Longest Palindromic Subsequence)** | LCS | `LCS(s, reversed(s))` | Elegant reduction; no new recurrence |
| **LIS O(N²)** | LIS | `dp[i] = 1 + max(dp[j]) for j<i, nums[j]<nums[i]` | Answer = `max(dp)` not `dp[n-1]` |
| **LIS O(N log N)** | LIS (patience) | `bisect_left` on `tails`; replace or append | `tails` ≠ actual LIS; only its length is correct |
| **Russian Doll Envelopes** | LIS | Sort (w asc, h desc); LIS on h | Descending h prevents same-width stacking |
| **Max Subarray (Kadane)** | Kadane | `end_here = max(x, end_here+x)` | Start fresh when extending is worse |
| **Max Product Subarray** | Kadane | Track `cur_max` and `cur_min` | Negative × negative = positive; must track both |
| **Circular Subarray Max** | Kadane | `max(straight, total - min_subarray)` | All-negative edge case: use straight only |
| **Burst Balloons** | Interval DP | `k` = last burst; `nums[i]*nums[k]*nums[j]` | `k` is last, not first; boundaries `i,j` still present |
| **Matrix Chain Multiplication** | Interval DP | `dp[i][j] = min over k of cost(i,k,j)` | Fill by increasing length; `cost = dims[i-1]*dims[k]*dims[j]` |
| **Palindrome Partitioning II** | Interval DP | Precompute palindrome table; `dp[i] = min(dp[j-1]+1)` | Precompute `is_pal[i][j]` in O(N²) first |
| **House Robber III** | Tree DP | `dfs → (rob, skip)`; parent combines | Return pair; parent not forced to take max of child |
| **Max Path Sum** | Tree DP | Ignore negative subtrees; path through node | Global max updated per node; return only single chain up |
| **Binary Tree Cameras** | Tree DP | 3 states: covered/has_camera/not_covered | Greedy from leaves; root NOT_COVERED needs one more camera |
| **TSP / Shortest Path All Nodes** | Bitmask DP | `dp[mask][node]`; BFS pairwise distances first | Multi-source BFS start; `FULL = (1<<n)-1` is goal |
| **Smallest Sufficient Team** | Bitmask DP | `dp[skill_mask]` = min team | Subset of required skills; OR masks for coverage |

---

## Quick Pattern Recognition

| Signal in problem | Pattern to reach for |
| :--- | :--- |
| "Each item at most once" + capacity constraint | 0/1 Knapsack |
| "Unlimited copies" + capacity constraint | Unbounded Knapsack |
| "Number of ways" + items/coins | Unbounded (count) — `dp[0]=1`, add not max |
| `dp[i]` from `dp[i-1]` and `dp[i-2]` only | Fibonacci / Linear |
| Two strings, "common", "match", "align" | LCS family |
| One array, "longest increasing" | LIS (`bisect_left` for strict) |
| "Best subarray", "contiguous", "max/min sum" | Kadane |
| "Interval `[i,j]`", "split at `k`", "optimal order" | MCM / Interval DP |
| Tree problem with "rob/skip", "path through root" | Tree DP (post-order DFS, return pair) |
| N ≤ 20, "visit all nodes", "assign items" | Bitmask DP |

---

---

## See also

**DP Sub-files (this folder):**
- [README.md](README.md) — SDE-3 DP overview and interview flow
- [digit-dp.md](digit-dp.md) — Digit DP with 8+ problems
- [grid-dp.md](grid-dp.md) — 2D grid DP: paths, Dungeon, Cherry Pickup
- [stock-trading-dp.md](stock-trading-dp.md) — All 6 stock variants (Pattern 10)
- [string-palindrome-dp.md](string-palindrome-dp.md) — Palindromes, regex, wildcard (Pattern 11)
- [advanced-dp-optimizations.md](advanced-dp-optimizations.md) — CHT, deque, D&C, SOS DP
- [probability-combinatorics-dp.md](probability-combinatorics-dp.md) — Game theory, egg drop, Catalan
- [questions-bank.md](questions-bank.md) — 70 tiered drill questions
- [tips-and-gotchas.md](tips-and-gotchas.md) — 12 common bugs, 30+ recognition triggers

**Related files:**
- [Patterns Master](../../../../reference/patterns/patterns-master.md) — 16 patterns with recognition triggers
- [greedy.md](../greedy.md) — when greedy replaces DP (fractional knapsack, interval scheduling)
- [divide-and-conquer.md](../divide-and-conquer.md) — independent subproblems vs overlapping (DP)
