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

## 🎙️ The Coach's Dialogue: Bridging the "What" and the "How"

**Student:** "Coach, I see two different lists of patterns. The [README.md](README.md) has 8 patterns, but this playbook has 11. Which one should I follow?"

**Coach:** "Think of the [README.md](README.md) as the **Syllabus** and this playbook as the **Step-by-Step Training Manual**. The README tells you *what* exists in the world of SDE-3 DP; this file shows you *how* to implement the most common variants using the Aditya Verma 'Pattern-First' approach."

### 🔗 Master Pattern Mapping

| Main README Pattern | This Playbook (Aditya Verma) | High-Yield Variants |
| :--- | :--- | :--- |
| **Linear DP (1D)** | **Pattern 3 — Fibonacci / Linear** | Climbing Stairs, House Robber, Decode Ways |
| **Knapsack — 0/1** | **Pattern 1 — 0/1 Knapsack** | Subset Sum, Target Sum, Stone Weight |
| **Knapsack — Unbounded** | **Pattern 2 — Unbounded Knapsack** | Coin Change, Rod Cutting, Perfect Squares |
| **LCS (2D String DP)** | **Pattern 4 — LCS Family** | Edit Distance, SCS, LPS, Palindrome Deletions |
| **Interval DP** | **Pattern 7 — MCM / Interval DP** | Burst Balloons, Matrix Chain, Palindrome Cuts |
| **Bitmask DP** | **Pattern 9 — Bitmask / DP on Graphs** | TSP, Assignment, Smallest Sufficient Team |
| **Tree DP** | **Pattern 8 — DP on Trees** | House Robber III, Max Path Sum, Cameras |
| **Stock Trading** | **Pattern 10 — Stock Trading Machine** | Cooldown, Fee, K-Transactions |
| *(In Codebank)* | **Pattern 5 — LIS** | Russian Doll Envelopes, Longest Pair Chain |
| *(In Codebank)* | **Pattern 6 — Kadane** | Max Subarray, Max Product, Circular Subarray |
| *(In Codebank)* | **Pattern 11 — Palindrome DP** | Palindromic Substrings, Min Insertions |

---

## Pattern 1 — 0/1 Knapsack

### Theory

- **Core idea:** Each item has a binary choice — include it once or skip it. Taking an item reduces remaining capacity; skipping does not.
- **State:** `dp[i][w]` = maximum value achievable using only the first `i` items with capacity exactly `w`.
- **Recurrence:** `dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])` (if weight fits).
- **Base case:** `dp[0][w] = 0` for all `w`.
- **Space optimization:** Collapse to 1D `dp[w]` by iterating `w` from **high → low**.

### The 4-Step Build

- **Step 1 — Recursion (brute force)**
    - **Code:**
        ```python
        def knapsack_rec(weights, values, W, i):
            if i == 0 or W == 0: return 0
            if weights[i-1] > W: return knapsack_rec(weights, values, W, i-1)
            return max(knapsack_rec(weights, values, W, i-1),
                       values[i-1] + knapsack_rec(weights, values, W - weights[i-1], i-1))
        ```
    - **Language & Logic:** "For every item, we have two choices: take it or leave it. If we take it, we gain its value but lose its weight from our remaining capacity."
    - **Complexity:** O(2^n) — overlapping subproblems make this slow.

- **Step 2 — Memoization (top-down)**
    - **Code:**
        ```python
        def knapsack_memo(weights, values, W, i, memo={}):
            if (i, W) in memo: return memo[(i, W)]
            if i == 0 or W == 0: return 0
            if weights[i-1] > W:
                res = knapsack_memo(weights, values, W, i-1, memo)
            else:
                res = max(knapsack_memo(weights, values, W, i-1, memo),
                          values[i-1] + knapsack_memo(weights, values, W - weights[i-1], i-1, memo))
            memo[(i, W)] = res
            return res
        ```
    - **Language & Logic:** "We carry a notebook (`memo`) and write down the answer the first time we see a pair `(i, W)`. Next time, we just look it up."
    - **Complexity:** O(n\*W) time, O(n\*W) space.

- **Step 3 — Bottom-up tabulation**
    - **Code:**
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
        ```
    - **Language & Logic:** "We fill a physical table row-by-row. Each cell `dp[i][w]` is calculated using only values from the row above it."
    - **Complexity:** O(n\*W) time, O(n\*W) space.

- **Step 4 — Space optimization (1D rolling array)**
    - **Code:**
        ```python
        def knapsack_01_space(weights, values, W):
            dp = [0] * (W + 1)
            for i in range(len(weights)):
                for w in range(W, weights[i] - 1, -1):   # BACKWARD — 0/1 invariant
                    dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
            return dp[W]
        ```
    - **Language & Logic:** "We update a single row in place. We go **backward** to ensure `dp[w - weight]` still refers to the previous item's row, so we don't use the same item twice."
    - **Complexity:** O(n\*W) time, O(W) space.

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
    items, w = [], W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
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
| **Last Stone Weight II** | Partition to minimize `\|S1 - S2\|` = `total - 2 * max_S1_leq_half` | Subset sum variant |
| **Ones and Zeroes** | 2D knapsack: capacity is `(m zeros, n ones)` | `dp[i][j]` = max strings using ≤ i zeros, ≤ j ones |

---

## Pattern 2 — Unbounded Knapsack

### Theory

- **Core idea:** Each item type can be picked **unlimited** times. After taking one copy of item `i`, you can pick item `i` again.
- **State:** `dp[i][w]` = max value using items up to `i` with capacity `w`.
- **Recurrence:** `dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i][w - weights[i-1]])` (stay at `i`).
- **Base case:** `dp[0][w] = 0`.
- **Space optimization:** 1D `dp[w]` with **forward** iteration (low → high).

### The 4-Step Build

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def unbounded_rec(weights, values, W, i):
            if i == 0 or W == 0: return 0
            if weights[i-1] > W: return unbounded_rec(weights, values, W, i-1)
            return max(unbounded_rec(weights, values, W, i-1),
                       values[i-1] + unbounded_rec(weights, values, W - weights[i-1], i))
        ```
    - **Language & Logic:** "Same as 0/1, but if we take an item, we **stay at the same index `i`** because we can pick it again. We only move to `i-1` when we decide we're done with item `i`."
    - **Complexity:** O(2^n).

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        def unbounded_memo(weights, values, W):
            @lru_cache(maxsize=None)
            def dp(i, w):
                if i == 0 or w == 0: return 0
                if weights[i-1] > w: return dp(i-1, w)
                return max(dp(i-1, w), values[i-1] + dp(i, w - weights[i-1]))
            return dp(len(weights), W)
        ```
    - **Language & Logic:** "We cache the results of `dp(i, w)` to avoid redundant calculations. The state space remains `n*W`."
    - **Complexity:** O(n\*W) time and space.

- **Step 3 — Bottom-up tabulation**
    - **Code:**
        ```python
        def knapsack_unbounded_2d(weights, values, W):
            n = len(weights)
            dp = [[0] * (W + 1) for _ in range(n + 1)]
            for i in range(1, n + 1):
                for w in range(W + 1):
                    dp[i][w] = dp[i-1][w]
                    if weights[i-1] <= w:
                        dp[i][w] = max(dp[i][w], values[i-1] + dp[i][w - weights[i-1]])
            return dp[n][W]
        ```
    - **Language & Logic:** "When filling the table, notice that taking an item refers to `dp[i][w-wt]` — the **current row**. This allows re-picking."
    - **Complexity:** O(n\*W) time and space.

- **Step 4 — Space optimization (1D, forward)**
    - **Code:**
        ```python
        def knapsack_unbounded(weights, values, W):
            dp = [0] * (W + 1)
            for i in range(len(weights)):
                for w in range(weights[i], W + 1):   # FORWARD — unbounded invariant
                    dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
            return dp[W]
        ```
    - **Language & Logic:** "Because we need `dp[w - weight]` to already include the current item (same row), we iterate **forward**. This is exactly how unbounded pick works."
    - **Complexity:** O(n\*W) time, O(W) space.

> [!TIP]
> **Combinations vs Permutations:** `coins` outer, `amount` inner → counts combinations (unordered). `amount` outer, `coins` inner → counts permutations (ordered). The problem "Coin Change 2" wants combinations.

**Common Unbounded variants:**

```python
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

### Variations & Interview Problems

| Problem | Loop Order | Key Insight |
| :--- | :--- | :--- |
| **Coin Change I** (min coins) | Coins outer, amount forward | `dp[0]=0`, rest `inf`; take `min` |
| **Coin Change II** (count ways) | Coins outer, amount forward | `dp[0]=1`; takes `+=` not `max` |
| **Rod Cutting** (max value) | Lengths outer, capacity forward | Identical to unbounded knapsack; length = weight |
| **Integer Break** (max product) | Split 1…n; `dp[i] = max(j*(i-j), j*dp[i-j])` | Greedy: break into 3s (AM-GM), but DP is safe |
| **Perfect Squares** (min count) | Squares outer, amount forward | Same as coin change with coins = 1,4,9,16… |

---

## Pattern 3 — Fibonacci / Linear DP

### Theory

- **Core idea:** `dp[i]` depends on a fixed small window of previous values (`dp[i-1]`, `dp[i-2]`). Dimension is purely position.
- **State:** `dp[i]` = answer for problem of size `i`.
- **Recurrence:** `dp[i] = f(dp[i-1], dp[i-2])`.
- **Base case:** Problem-specific (e.g., `dp[1]=1, dp[2]=2` for stairs).
- **Space optimization:** Reduces to O(1) using two variables.

### The 4-Step Build (Climbing Stairs)

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def climb_rec(n):
            if n <= 2: return n
            return climb_rec(n-1) + climb_rec(n-2)
        ```
    - **Language & Logic:** "To reach step `n`, you must have come from either `n-1` or `n-2`. The total ways is the sum of both."
    - **Complexity:** O(2^n).

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        @lru_cache(maxsize=None)
        def climb_memo(n):
            if n <= 2: return n
            return climb_memo(n-1) + climb_memo(n-2)
        ```
    - **Language & Logic:** "We cache the results to turn an exponential tree into a linear chain."
    - **Complexity:** O(n) time and space.

- **Step 3 — Bottom-up tabulation**
    - **Code:**
        ```python
        def climb_dp(n):
            dp = [0] * (n + 1)
            dp[1], dp[2] = 1, 2
            for i in range(3, n + 1):
                dp[i] = dp[i-1] + dp[i-2]
            return dp[n]
        ```
    - **Language & Logic:** "We fill an array from step 1 up to `n`."
    - **Complexity:** O(n) time and space.

- **Step 4 — Space optimization (two variables)**
    - **Code:**
        ```python
        def climb_stairs(n):
            if n <= 2: return n
            a, b = 1, 2
            for _ in range(3, n + 1):
                a, b = b, a + b
            return b
        ```
    - **Language & Logic:** "We only ever need the last two values. Sliding variables save O(N) space."
    - **Complexity:** O(n) time, O(1) space.

> [!TIP]
> **House Robber II (circle):** Run the linear robber twice — once on `nums[:-1]` and once on `nums[1:]`. Take the max. The circle constraint means you can't rob both first and last house; excluding one end from each run handles it.

**Other linear DP variants:**

```python
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
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
```

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

- **Core idea:** Two sequences. Match characters or skip one side.
- **State:** `dp[i][j]` = LCS of `s1[:i]` and `s2[:j]`.
- **Recurrence:** `Match ? 1 + dp[i-1][j-1] : max(up, left)`.
- **Base case:** `dp[0][j] = dp[i][0] = 0`.
- **Space optimization:** O(min(m, n)) using two rows.

### The 4-Step Build

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def lcs_rec(s1, s2, i, j):
            if i == 0 or j == 0: return 0
            if s1[i-1] == s2[j-1]: return 1 + lcs_rec(s1, s2, i-1, j-1)
            return max(lcs_rec(s1, s2, i-1, j), lcs_rec(s1, s2, i, j-1))
        ```
    - **Language & Logic:** "For a mismatch, try skipping from either string and take the better result."
    - **Complexity:** O(2^(m+n)).

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        def lcs_memo(s1, s2):
            @lru_cache(maxsize=None)
            def dp(i, j):
                if i == 0 or j == 0: return 0
                if s1[i-1] == s2[j-1]: return 1 + dp(i-1, j-1)
                return max(dp(i-1, j), dp(i, j-1))
            return dp(len(s1), len(s2))
        ```
    - **Language & Logic:** "Cache results for `(i, j)` prefix pairs."
    - **Complexity:** O(m\*n) time and space.

- **Step 3 — Bottom-up tabulation**
    - **Code:**
        ```python
        def lcs(s1, s2):
            m, n = len(s1), len(s2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if s1[i-1] == s2[j-1]:
                        dp[i][j] = 1 + dp[i-1][j-1]
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            return dp[m][n]
        ```
    - **Language & Logic:** "Fill table row-by-row. Each cell reads from the row above and the left column."
    - **Complexity:** O(m\*n) time and space.

- **Step 4 — Space optimization (two rows)**
    - **Code:**
        ```python
        def lcs_space(s1, s2):
            m, n = len(s1), len(s2)
            prev = [0] * (n + 1)
            for i in range(1, m + 1):
                curr = [0] * (n + 1)
                for j in range(1, n + 1):
                    if s1[i-1] == s2[j-1]:
                        curr[j] = 1 + prev[j-1]
                    else:
                        curr[j] = max(prev[j], curr[j-1])
                prev = curr
            return prev[n]
        ```
    - **Language & Logic:** "Only the previous row is needed. Note: can't reduce to O(1) because `dp[i][j]` reads `dp[i-1][j-1]`, `dp[i-1][j]`, and `dp[i][j-1]`."
    - **Complexity:** O(m\*n) time, O(n) space.

**Common LCS-family implementations:**

```python
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

- **Core idea:** One array; find the length of the longest strictly increasing subsequence. Two approaches with different trade-offs.
- **State (O(N²)):** `dp[i]` = length of LIS ending at index `i`.
- **Recurrence:** `dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])`.
- **O(N log N) alternative:** Patience sorting with `tails[]` array and binary search.
- **Space optimization:** O(N log N) approach already uses O(N) space with no further reduction.

### The 4-Step Build

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def lis_rec(nums, i, prev_idx):
            if i == len(nums): return 0
            skip = lis_rec(nums, i+1, prev_idx)
            take = 0
            if prev_idx == -1 or nums[i] > nums[prev_idx]:
                take = 1 + lis_rec(nums, i+1, i)
            return max(skip, take)
        # Call: lis_rec(nums, 0, -1)
        ```
    - **Language & Logic:** "At each index, either skip it or take it (if it's greater than the last taken). State = current index + index of last chosen element."
    - **Complexity:** O(2^n).

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        def lis_memo(nums):
            @lru_cache(maxsize=None)
            def dp(i, prev_idx):
                if i == len(nums): return 0
                skip = dp(i+1, prev_idx)
                take = 0
                if prev_idx == -1 or nums[i] > nums[prev_idx]:
                    take = 1 + dp(i+1, i)
                return max(skip, take)
            return dp(0, -1)
        ```
    - **Language & Logic:** "Cache `(i, prev_idx)` pairs — there are O(n²) unique states."
    - **Complexity:** O(n²) time and space.

- **Step 3 — Bottom-up O(N²) tabulation**
    - **Code:**
        ```python
        def lis_n2(nums: list[int]) -> int:
            n = len(nums)
            dp = [1] * n
            for i in range(1, n):
                for j in range(i):
                    if nums[j] < nums[i]:
                        dp[i] = max(dp[i], dp[j] + 1)
            return max(dp)
        ```
    - **Language & Logic:** "Fill `dp[i]` by looking back at all `j < i`. Answer = `max(dp)`, not `dp[n-1]`."
    - **Complexity:** O(n²) time, O(n) space.

- **Step 4 — O(N log N) via patience sorting (structural improvement)**
    - **Code:**
        ```python
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
    - **Language & Logic:** "Maintain `tails[k]` = smallest tail of any IS of length `k+1`. Binary search to place each element. `tails` is NOT the actual LIS — only its length is correct."
    - **Complexity:** O(n log n) time, O(n) space.

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

- **Core idea:** The globally optimal subarray can be found by tracking the best subarray that **ends** at each position. At position `i`, either extend the previous best or start fresh.
- **State:** `dp[i]` = best subarray sum ending at index `i`.
- **Recurrence:** `dp[i] = max(nums[i], dp[i-1] + nums[i])`.
- **Base case:** `dp[0] = nums[0]`.
- **Space optimization:** O(1) — only the previous value is needed.

### The 4-Step Build

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def kadane_rec(nums, i):
            if i == 0: return nums[0]
            prev = kadane_rec(nums, i-1)
            return max(nums[i], prev + nums[i])
        # Answer: max(kadane_rec(nums, i) for i in range(len(nums)))
        ```
    - **Language & Logic:** "At any index `i`, start a brand new subarray at `i`, or attach `nums[i]` to the best subarray ending at `i-1`. Pick whichever is larger."
    - **Complexity:** O(n) — no branching, linear chain.

- **Step 2 — Memoization**
    - **Note:** Trivially the same as recursion here — no branching, linear chain. Not needed in practice.

- **Step 3 — Bottom-up tabulation**
    - **Code:**
        ```python
        def kadane_dp(nums):
            n = len(nums)
            dp = [0] * n
            dp[0] = nums[0]
            for i in range(1, n):
                dp[i] = max(nums[i], dp[i-1] + nums[i])
            return max(dp)
        ```
    - **Language & Logic:** "Fill a 1D array. `dp[i]` = 'what is the best I can do if I MUST end at `i`?'"
    - **Complexity:** O(n) time, O(n) space.

- **Step 4 — Space optimization (two variables)**
    - **Code:**
        ```python
        def max_subarray(nums: list[int]) -> int:
            ending_here = global_max = nums[0]
            for x in nums[1:]:
                ending_here = max(x, ending_here + x)
                global_max = max(global_max, ending_here)
            return global_max
        ```
    - **Language & Logic:** "Since `dp[i]` only depends on `dp[i-1]`, we don't need the array — just two variables: the running best and the global best."
    - **Complexity:** O(n) time, O(1) space.

> [!TIP]
> **Max Product Subarray:** Track both `cur_max` and `cur_min` at each step because a large negative × negative = large positive. All three candidates `(x, cur_max*x, cur_min*x)` must be evaluated on every step.

**Other Kadane variants:**

```python
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

- **Core idea:** Optimal solution for interval `[i, j]` depends on splitting it into `[i, k]` and `[k+1, j]`.
- **State:** `dp[i][j]` = optimal cost/value for the interval `[i..j]`.
- **Recurrence:** `dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost(i, k, j))` for all `i <= k < j`.
- **Fill order:** By **increasing length** — `len = 2, 3, …, n`.
- **Base case:** `dp[i][i] = 0` (interval of size 1).
- **Space optimization:** Not possible; reads from scattered sub-intervals.

### The 4-Step Build (MCM)

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def mcm_rec(dims, i, j):
            if i == j: return 0
            res = float('inf')
            for k in range(i, j):
                cost = (mcm_rec(dims, i, k) + mcm_rec(dims, k+1, j)
                        + dims[i-1] * dims[k] * dims[j])
                res = min(res, cost)
            return res
        # Call: mcm_rec(dims, 1, n)
        ```
    - **Language & Logic:** "Try every split point `k` and take the minimum. Sub-intervals `[i,k]` and `[k+1,j]` overlap heavily across calls."
    - **Complexity:** O(3^n).

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        def mcm_memo(dims):
            n = len(dims) - 1
            @lru_cache(maxsize=None)
            def dp(i, j):
                if i == j: return 0
                return min(dp(i, k) + dp(k+1, j) + dims[i-1] * dims[k] * dims[j]
                           for k in range(i, j))
            return dp(1, n)
        ```
    - **Language & Logic:** "Cache results for sub-intervals `[i, j]`."
    - **Complexity:** O(n³) time, O(n²) space.

- **Step 3 — Bottom-up tabulation (fill by increasing length)**
    - **Code:**
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
        ```
    - **Language & Logic:** "Fill table by increasing interval length. Smaller intervals must be filled before larger ones that depend on them."
    - **Complexity:** O(n³) time, O(n²) space.

- **Step 4 — Space optimization: Not Possible**
    - **Language & Logic:** "Requires access to arbitrary smaller intervals; cannot reduce below O(n²)."

> [!CAUTION]
> **Burst Balloons gotcha:** `k` is the **last** balloon to burst within `(i, j)`, not the first. When `k` bursts, `nums[i]` and `nums[j]` are still present (boundaries), so the coins = `nums[i] * nums[k] * nums[j]`.

**Other Interval DP implementations:**

```python
def burst_balloons(nums: list[int]) -> int:
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(0, n - length):
            j = i + length
            for k in range(i + 1, j):      # k = LAST balloon to burst in (i, j)
                coins = nums[i] * nums[k] * nums[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + coins + dp[k][j])
    return dp[0][n - 1]

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

- **Core idea:** Subtrees are independent subproblems. Process in **DFS post-order** — children before parent.
- **Pattern:** Define `dfs(node) → (state_A, state_B)` where states represent discrete choices. Parent combines children's states to compute its own.
- **Space:** O(h) call stack only — no table needed. "Bottom-up" = post-order DFS returning a tuple.

### The 4-Step Build (House Robber III)

- **Step 1 — Recursion (exponential, recomputes subtrees)**
    - **Code:**
        ```python
        def rob_rec(node):
            if not node: return 0
            rob = node.val
            if node.left:
                rob += rob_rec(node.left.left) + rob_rec(node.left.right)
            if node.right:
                rob += rob_rec(node.right.left) + rob_rec(node.right.right)
            skip = rob_rec(node.left) + rob_rec(node.right)
            return max(rob, skip)
        ```
    - **Language & Logic:** "Either rob this node (skip children, allow grandchildren) or skip it (children free to choose). Grandchildren get recomputed for every rob branch."
    - **Complexity:** O(2^n).

- **Step 2 — Memoization**
    - **Code:**
        ```python
        def rob_memo(node, memo={}):
            if not node: return 0
            if node in memo: return memo[node]
            rob = node.val
            if node.left:
                rob += rob_memo(node.left.left, memo) + rob_memo(node.left.right, memo)
            if node.right:
                rob += rob_memo(node.right.left, memo) + rob_memo(node.right.right, memo)
            skip = rob_memo(node.left, memo) + rob_memo(node.right, memo)
            memo[node] = max(rob, skip)
            return memo[node]
        ```
    - **Language & Logic:** "Store the best result per node object. Each node processed exactly once."
    - **Complexity:** O(n) time, O(n) memo + O(h) call stack.

- **Step 3+4 — Bottom-up (post-order DFS returning both states)**
    - **Note:** Trees don't use a 2D table. Post-order DFS returning a tuple is both Step 3 and Step 4: each node computes from already-computed children, O(n) time, O(h) space.
    - **Code:**
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
        ```

**Other tree DP implementations:**

```python
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

- **Core idea:** When the graph is small (N ≤ 20), encode the set of visited nodes as a bitmask integer. State = `(current_node, visited_mask)`.
- **State:** `dp[mask][v]` = cost/distance to reach node `v` having visited exactly the nodes in `mask`.
- **Classic application:** TSP, Hamiltonian path, collecting all keys.
- **Space optimization:** Not possible — full `dp[2^n][n]` table is needed.

### The 4-Step Build (TSP)

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def tsp_rec(dist, visited, curr, n):
            if visited == (1 << n) - 1:
                return dist[curr][0]             # return to start
            best = float('inf')
            for nxt in range(n):
                if not (visited >> nxt & 1):
                    cost = dist[curr][nxt] + tsp_rec(dist, visited | (1 << nxt), nxt, n)
                    best = min(best, cost)
            return best
        # Call: tsp_rec(dist, 1, 0, n)
        ```
    - **Language & Logic:** "From the current node, try visiting every unvisited neighbor. 'Visited' is encoded as a bitmask (e.g., `1011` means nodes 0, 1, and 3 are done)."
    - **Complexity:** O(n!) — exponential; `(visited, curr)` subproblems repeat heavily.

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        def tsp_memo(dist):
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
        ```
    - **Language & Logic:** "There are only 2^N subsets × N current positions = O(2^N × N) unique states. We cache this `(mask, curr)` pair."
    - **Complexity:** O(2^n × n²) time, O(2^n × n) space.

- **Step 3 — Bottom-up tabulation**
    - **Note:** Fill by increasing `popcount(mask)` so smaller subproblems (fewer nodes visited) come before larger ones.
    - **Code:**
        ```python
        def tsp_bottom_up(dist):
            n = len(dist)
            INF = float('inf')
            FULL = (1 << n) - 1
            dp = [[INF] * n for _ in range(1 << n)]
            dp[1][0] = 0                         # start at node 0, only node 0 visited
            for mask in range(1, 1 << n):
                for u in range(n):
                    if dp[mask][u] == INF or not (mask >> u & 1):
                        continue
                    for v in range(n):
                        if mask >> v & 1: continue
                        new_mask = mask | (1 << v)
                        dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])
            return min(dp[FULL][u] + dist[u][0] for u in range(n))
        ```
    - **Complexity:** O(2^n × n²) time, O(2^n × n) space.

- **Step 4 — Space optimization: Not Possible**
    - **Language & Logic:** "`dp[mask][v]` reads from `dp[mask ^ (1<<v)][u]` for all `u`; the full table is needed."

> [!TIP]
> **Subset enumeration trick:** To iterate over all subsets of a mask `m`, use `sub = m; while sub > 0: process(sub); sub = (sub - 1) & m`. This runs in O(3^N) total over all masks.

**Other bitmask DP implementations:**

```python
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

- **Core idea:** All variants share the same `dp[i][k][state]` state machine.
- **State:** `dp[i][k][holding]` = max profit on day `i` with `k` transactions remaining and `holding` (0/1).
- **Recurrence:** `Buy: -prices[i] + dp[i+1][k-1][1]`; `Sell: prices[i] + dp[i+1][k][0]`.
- **Key rule:** Decrement `k` on **buy** (not sell). This tracks remaining complete transactions.
- **Base case:** `dp[len][*][*] = 0` or `dp[*][0][*] = 0`.
- **Space optimization:** O(K) variables or rolling row.

### The 4-Step Build (K-transactions)

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def stock_rec(prices, i, k, holding):
            if i == len(prices) or k == 0: return 0
            if holding:
                return max(prices[i] + stock_rec(prices, i+1, k, 0),
                           stock_rec(prices, i+1, k, 1))
            return max(-prices[i] + stock_rec(prices, i+1, k-1, 1),
                       stock_rec(prices, i+1, k, 0))
        # Call: stock_rec(prices, 0, k, 0)
        ```
    - **Language & Logic:** "On any day: Buy, Sell, or Do Nothing. Buy starts a transaction; Sell finishes it."
    - **Complexity:** O(2^n).

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        def stock_memo(prices, k):
            @lru_cache(maxsize=None)
            def dp(i, k, holding):
                if i == len(prices) or k == 0: return 0
                if holding:
                    return max(prices[i] + dp(i+1, k, 0), dp(i+1, k, 1))
                return max(-prices[i] + dp(i+1, k-1, 1), dp(i+1, k, 0))
            return dp(0, k, 0)
        ```
    - **Language & Logic:** "Cache results for `(day, k, holding)` states."
    - **Complexity:** O(n\*k\*2) time and space.

- **Step 3 — Bottom-up tabulation**
    - **Code:**
        ```python
        # Fill 3D table: iterate days forward; k and holding as table dimensions
        # dp[i][j][0/1] = max profit starting from day i with j transactions left, holding state
        ```
    - **Language & Logic:** "Fill day-by-day. Each state reads the next day's values (forward recursion → backward fill)."
    - **Complexity:** O(n\*k\*2).

- **Step 4 — Space optimization (rolling row — keep only current k state)**
    - **Code:**
        ```python
        def max_profit_iv(k: int, prices: list[int]) -> int:
            n = len(prices)
            if k >= n // 2:
                return sum(max(0, prices[i]-prices[i-1]) for i in range(1, n))
            dp = [[0, float('-inf')] for _ in range(k + 1)]
            for p in prices:
                for j in range(k, 0, -1):   # backward prevents reuse of updated values
                    dp[j][0] = max(dp[j][0], dp[j][1] + p)
                    dp[j][1] = max(dp[j][1], dp[j-1][0] - p)
            return dp[k][0]
        ```
    - **Language & Logic:** "Use only the previous day's state and iterate `k` backward to prevent using updated values in the same pass."
    - **Complexity:** O(n\*k) time, O(k) space.

**Common stock variants:**

```python
def max_profit_ii(prices: list[int]) -> int:
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free

def max_profit_cooldown(prices: list[int]) -> int:
    hold, sold, rest = float('-inf'), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
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

- **Core idea:** `s[i..j]` is a palindrome if `s[i] == s[j]` and middle is a palindrome.
- **State:** `dp[i][j]` = True if `s[i..j]` is a palindrome.
- **Recurrence:** `dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]`.
- **Base case:** `dp[i][i] = True`, `dp[i][i+1] = (s[i] == s[i+1])`.
- **Fill order:** `i` from high to low, `j` from `i` to high (so `dp[i+1][j-1]` is already filled).
- **Space optimization:** Not possible for range queries; full table required.

### The 4-Step Build (Palindrome Table)

- **Step 1 — Recursion**
    - **Code:**
        ```python
        def is_pal_rec(s, i, j):
            if i >= j: return True
            return s[i] == s[j] and is_pal_rec(s, i+1, j-1)
        ```
    - **Language & Logic:** "Check ends and recurse inward. Same `(i, j)` pairs get recomputed across different outer problems."
    - **Complexity:** O(2^n) without memo.

- **Step 2 — Memoization**
    - **Code:**
        ```python
        from functools import lru_cache
        def count_palindromes_memo(s):
            @lru_cache(maxsize=None)
            def is_pal(i, j):
                if i >= j: return True
                return s[i] == s[j] and is_pal(i+1, j-1)
            return sum(is_pal(i, j) for i in range(len(s)) for j in range(i, len(s)))
        ```
    - **Language & Logic:** "Cache results for `(i, j)` intervals."
    - **Complexity:** O(n²) time and space.

- **Step 3 — Bottom-up tabulation**
    - **Code:**
        ```python
        def build_palindrome_table(s: str) -> list[list[bool]]:
            n = len(s)
            is_pal = [[False] * n for _ in range(n)]
            for i in range(n - 1, -1, -1):
                for j in range(i, n):
                    is_pal[i][j] = (s[i] == s[j]) and (j - i < 2 or is_pal[i+1][j-1])
            return is_pal
        ```
    - **Language & Logic:** "Fill outer-in: `i` from high to low ensures `is_pal[i+1][j-1]` is always computed before `is_pal[i][j]`."
    - **Complexity:** O(n²) time and space.

- **Step 4 — Space optimization: Not Possible**
    - **Language & Logic:** "Access to diagonal `[i+1, j-1]` requires the full table. Min-cut and partition problems read arbitrary `is_pal[l][r]` ranges."

**Common palindrome DP implementations:**

```python
def longest_palindromic_subsequence(s: str) -> int:
    t = s[::-1]
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j-1] + 1 if s[i-1] == t[j-1] else max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def min_cut_palindrome(s: str) -> int:
    n = len(s)
    is_pal = build_palindrome_table(s)
    cut = list(range(n))
    for i in range(1, n):
        if is_pal[0][i]:
            cut[i] = 0
            continue
        for j in range(1, i + 1):
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

## Knapsack Identification Checklist

**Identification checklist:**
- [ ] Each item picked at most once → 0/1 Knapsack (backward loop)
- [ ] Items picked unlimited → Unbounded Knapsack (forward loop)
- [ ] Ask is "max/min/count" not "which" → DP (reconstruction is a follow-up)
- [ ] Reduce sum problems: "subset sum to T" = knapsack with `value[i] = weight[i]`

### Knapsack → Subset Sum Reductions

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
