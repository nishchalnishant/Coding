# Recursion → Memoization → Tabulation

The mechanical three-step bridge from naive recursion to optimized DP. For every problem: write the recursive solution first, then memoize, then convert to bottom-up tabulation. For pattern theory see [README.md](README.md).

---

## The Three-Step Conversion

```
Step 1 — RECURSIVE (brute force, correct, exponential)
         Write the recursive solution that matches the problem's natural structure.
         Identify what parameters uniquely define each subproblem.

Step 2 — MEMOIZED (top-down DP, polynomial)
         Add a cache (dict or @lru_cache) keyed on the function parameters.
         Check cache at entry; store result at exit.

Step 3 — TABULATED (bottom-up DP, polynomial, no recursion overhead)
         Define a dp table of the same shape as the cache.
         Fill base cases first; fill larger subproblems using smaller ones.
         Optional: space-optimize the table to a 1D rolling array.
```

> [!IMPORTANT]
> The **state** in the recursive version directly becomes the **dp table dimensions**. If the recursion is `solve(i, w)`, your table is `dp[i][w]`. This mapping is the key insight — never skip to the table without first writing the recursion.

---

## Problem 1 — Fibonacci

### Step 1: Recursive O(2^N)
```python
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

### Step 2: Memoized O(N)
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

### Step 3: Tabulated O(N) time, O(N) space
```python
def fib(n: int) -> int:
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

### Step 4: Space-Optimized O(1) space
```python
def fib(n: int) -> int:
    if n <= 1: return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
```

> [!TIP]
> Space optimize whenever `dp[i]` only reads `dp[i-1]` and `dp[i-2]`. Replace the array with two rolling variables.

---

## Problem 2 — 0/1 Knapsack

**Problem:** N items with `weight[i]` and `value[i]`. Capacity W. Maximize value without exceeding weight.

### Step 1: Recursive
```python
def knapsack(weights, values, i, w):
    if i == 0 or w == 0:
        return 0
    if weights[i-1] > w:
        return knapsack(weights, values, i-1, w)       # can't take
    return max(
        knapsack(weights, values, i-1, w),             # skip
        values[i-1] + knapsack(weights, values, i-1, w - weights[i-1])  # take
    )
```

**State:** `(i, w)` — item index and remaining capacity. Total unique states: O(N × W).

### Step 2: Memoized
```python
from functools import lru_cache

def knapsack_memo(weights, values, W):
    @lru_cache(maxsize=None)
    def solve(i, w):
        if i == 0 or w == 0: return 0
        if weights[i-1] > w:
            return solve(i-1, w)
        return max(solve(i-1, w),
                   values[i-1] + solve(i-1, w - weights[i-1]))
    return solve(len(weights), W)
```

### Step 3: Tabulated O(N×W) time and space
```python
def knapsack_dp(weights, values, W):
    n = len(weights)
    dp = [[0] * (W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(W+1):
            dp[i][w] = dp[i-1][w]                         # skip
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                               values[i-1] + dp[i-1][w - weights[i-1]])  # take
    return dp[n][W]
```

### Step 4: Space-Optimized O(W) space
```python
def knapsack_1d(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i]-1, -1):   # BACKWARD — 0/1 invariant
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]
```

> [!CAUTION]
> The backward loop in the 1D version is critical. Forward iteration would let you pick the same item multiple times (unbounded knapsack). This is the #1 knapsack bug.

---

## Problem 3 — Longest Common Subsequence (LCS)

### Step 1: Recursive O(2^(M+N))
```python
def lcs(s1, s2, i, j):
    if i == 0 or j == 0:
        return 0
    if s1[i-1] == s2[j-1]:
        return 1 + lcs(s1, s2, i-1, j-1)
    return max(lcs(s1, s2, i-1, j), lcs(s1, s2, i, j-1))
```

### Step 2: Memoized O(M×N)
```python
from functools import lru_cache

def lcs_memo(s1, s2):
    @lru_cache(maxsize=None)
    def solve(i, j):
        if i == 0 or j == 0: return 0
        if s1[i-1] == s2[j-1]:
            return 1 + solve(i-1, j-1)
        return max(solve(i-1, j), solve(i, j-1))
    return solve(len(s1), len(s2))
```

### Step 3: Tabulated
```python
def lcs_dp(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

### Step 4: Space-Optimized O(N) space
```python
def lcs_opt(s1, s2):
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0           # holds dp[i-1][j-1] (diagonal)
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev = temp
    return dp[n]
```

---

## Problem 4 — Edit Distance

**Problem:** Minimum operations (insert, delete, replace) to convert `word1` to `word2`.

### Step 1: Recursive
```python
def edit(w1, w2, i, j):
    if i == 0: return j       # insert all of w2
    if j == 0: return i       # delete all of w1
    if w1[i-1] == w2[j-1]:
        return edit(w1, w2, i-1, j-1)
    return 1 + min(
        edit(w1, w2, i-1, j),    # delete from w1
        edit(w1, w2, i, j-1),    # insert into w1
        edit(w1, w2, i-1, j-1)   # replace
    )
```

### Step 2: Memoized
```python
from functools import lru_cache

def edit_distance(w1, w2):
    @lru_cache(maxsize=None)
    def solve(i, j):
        if i == 0: return j
        if j == 0: return i
        if w1[i-1] == w2[j-1]: return solve(i-1, j-1)
        return 1 + min(solve(i-1, j), solve(i, j-1), solve(i-1, j-1))
    return solve(len(w1), len(w2))
```

### Step 3: Tabulated + Space-Optimized O(N) space
```python
def edit_distance_opt(w1, w2):
    m, n = len(w1), len(w2)
    dp = list(range(n + 1))    # base case: dp[0][j] = j
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i              # base case: dp[i][0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if w1[i-1] == w2[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])
            prev = temp
    return dp[n]
```

> [!TIP]
> `prev` stores `dp[i-1][j-1]` (diagonal) before it's overwritten. This is the key trick for 1D space optimization when the recurrence needs the diagonal.

---

## Problem 5 — Coin Change (Minimum Coins)

### Step 1: Recursive O(S^N) where S = amount
```python
def coin_change_rec(coins, amount):
    if amount == 0: return 0
    if amount < 0: return float('inf')
    return 1 + min(coin_change_rec(coins, amount - c) for c in coins)
```

### Step 2: Memoized
```python
from functools import lru_cache

def coin_change_memo(coins, amount):
    @lru_cache(maxsize=None)
    def solve(rem):
        if rem == 0: return 0
        if rem < 0: return float('inf')
        return 1 + min(solve(rem - c) for c in coins)
    result = solve(amount)
    return result if result != float('inf') else -1
```

### Step 3: Tabulated O(S×N) time, O(S) space
```python
def coin_change_dp(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for c in coins:
        for w in range(c, amount + 1):   # forward = unbounded (reuse allowed)
            dp[w] = min(dp[w], 1 + dp[w - c])
    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## Problem 6 — Longest Palindromic Subsequence

**State:** `solve(i, j)` = LPS length of `s[i..j]`.

### Step 1: Recursive
```python
def lps_rec(s, i, j):
    if i == j: return 1
    if i > j: return 0
    if s[i] == s[j]:
        return 2 + lps_rec(s, i+1, j-1)
    return max(lps_rec(s, i+1, j), lps_rec(s, i, j-1))
```

### Step 2: Memoized
```python
from functools import lru_cache

def lps(s):
    @lru_cache(maxsize=None)
    def solve(i, j):
        if i == j: return 1
        if i > j: return 0
        if s[i] == s[j]: return 2 + solve(i+1, j-1)
        return max(solve(i+1, j), solve(i, j-1))
    return solve(0, len(s)-1)
```

### Step 3: Tabulated (fill by increasing interval length)
```python
def lps_dp(s):
    n = len(s)
    dp = [[0]*n for _ in range(n)]
    for i in range(n): dp[i][i] = 1
    for length in range(2, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i+1][j-1] if length > 2 else 0)
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1]
```

> [!TIP]
> Interval DP (like LPS, MCM) must be filled by **increasing length** — base cases are single characters (length=1), then pairs (length=2), and so on. You cannot fill row-by-row because `dp[i+1][j-1]` comes from a shorter interval, not a previous row.

---

## Problem 7 — Matrix Chain Multiplication

**Problem:** Parenthesize a chain of matrices to minimize total scalar multiplications.

### Step 1: Recursive (state = interval [i, j])
```python
def mcm_rec(dims, i, j):
    if i == j: return 0
    min_cost = float('inf')
    for k in range(i, j):
        cost = (mcm_rec(dims, i, k) +
                mcm_rec(dims, k+1, j) +
                dims[i-1] * dims[k] * dims[j])
        min_cost = min(min_cost, cost)
    return min_cost
```

### Step 2: Memoized
```python
from functools import lru_cache

def mcm_memo(dims):
    @lru_cache(maxsize=None)
    def solve(i, j):
        if i == j: return 0
        return min(
            solve(i, k) + solve(k+1, j) + dims[i-1]*dims[k]*dims[j]
            for k in range(i, j)
        )
    n = len(dims) - 1
    return solve(1, n)
```

### Step 3: Tabulated
```python
def mcm_dp(dims):
    n = len(dims) - 1
    dp = [[0]*( n+1) for _ in range(n+1)]
    for length in range(2, n+1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i-1]*dims[k]*dims[j]
                dp[i][j] = min(dp[i][j], cost)
    return dp[1][n]
```

---

## Problem 8 — Word Break

**Problem:** Can string `s` be segmented into words from `word_dict`?

### Step 1: Recursive
```python
def word_break_rec(s, words, i):
    if i == len(s): return True
    for j in range(i+1, len(s)+1):
        if s[i:j] in words and word_break_rec(s, words, j):
            return True
    return False
```

### Step 2: Memoized (True/False result)
```python
from functools import lru_cache

def word_break(s, word_dict):
    words = frozenset(word_dict)
    @lru_cache(maxsize=None)
    def solve(i):
        if i == len(s): return True
        return any(s[i:j] in words and solve(j)
                   for j in range(i+1, len(s)+1))
    return solve(0)
```

### Step 3: Tabulated
```python
def word_break_dp(s, word_dict):
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True               # empty string is always segmentable
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]
```

> [!CAUTION]
> Without memoization, `word_break_rec` is O(2^N) on strings like `"aaaaab"` with `words=["a","aa","aaa"]` — every prefix is valid, generating an exponential tree. The memo reduces this to O(N²).

---

## Conversion Cheatsheet

| Step | Action | Complexity Change |
| :--- | :--- | :--- |
| Recursive | Write naturally; identify state params | O(branches^depth) |
| + Cache check at entry | `if state in memo: return memo[state]` | O(states × transition) |
| + Store at exit | `memo[state] = result` | Same |
| Bottom-up table | Fill dp[state] from base → larger | Same; avoids stack |
| Space optimize | Replace full table with rolling row/vars | Reduce space dimension |

## State → Table Mapping

| Recursive signature | Table dimensions | Fill order |
| :--- | :--- | :--- |
| `f(i)` | `dp[n+1]` | `i` from 0 to n |
| `f(i, j)` for two-string | `dp[m+1][n+1]` | row by row, left to right |
| `f(i, j)` for interval | `dp[n][n]` | by increasing `j - i` (length) |
| `f(i, w)` for knapsack | `dp[n+1][W+1]` | row by row; 1D: backward |
| `f(i, j)` for palindrome | `dp[n][n]` | by increasing length |

---

## See also

- [README.md](README.md) — Recursion types and memoized recursion pattern
- [aditya-verma.md](aditya-verma.md) — Pattern 8: Recursion→Memo Bridge with more examples
- [../dynamic-programming/README.md](../dynamic-programming/README.md) — Full DP guide
- [../dynamic-programming/dp-aditya-verma.md](../dynamic-programming/dp-aditya-verma.md) — All DP patterns with tabulation
