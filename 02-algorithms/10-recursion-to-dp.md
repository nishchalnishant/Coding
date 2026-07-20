# Recursion → DP — The Conversion Bridge

> [!abstract] L3 Google Interview — Tier Legend
> `⚡ T1` — **TIER 1 · Must Master**: High-yield Google L3 favorites. These appear in nearly every loop.
> `🎯 T2` — **TIER 2 · Build Fluidity**: This file is core Tier 2 material. Know patterns cold; skip niche edge cases.
> `💤 T3` — **TIER 3 · Skim or Skip**: Overkill for L3. Conceptual awareness only.


**Companion files:** [recursion.md](./09-recursion.md) (write the recurrence) · [dynamic-programming.md](./15-dynamic-programming.md) (pattern catalog + bugs)

Use this file when you can write recursion but suspect repeated subproblems. The interview workflow:

```
Recursive brute force  →  memo (top-down)  →  tabulate (bottom-up)  →  compress space
     define state              cache state         fix fill order         drop unused rows
```

If you can execute those four moves on demand, most classic DP questions become engineering — not memorization.




---

## First-Principles Map

```
WHY this bridge exists
├── Plain recursion is the easiest way to define a correct recurrence
├── Overlapping subproblems make the recursion tree exponential
└── DP = same recurrence + each state computed once

WHAT changes at each stage
├── Recursion:  state = function args; no cache
├── Memo:       state → result map; same call tree, pruned
├── Bottom-up:  state → table cell; explicit dependency order
└── Space-opt:  keep only rows/columns the transition still needs

HOW to convert (never skip step 1)
├── Step 1 — Write recursive solution with correct base cases
├── Step 2 — Name the state: minimum args that uniquely identify a subproblem
├── Step 3 — Prove overlap: same state reached from different paths
├── Step 4 — Memoize OR tabulate (pick based on table shape)
└── Step 5 — Compress if transition only reads i-1, i-2, or one prior row

WHEN overlap appears (signals)
├── Same index pair (i, j) visited twice
├── Same remaining amount / capacity recomputed
├── Exponential tree depth with small input range (n ≤ 500, 2^n TLE)
└── "Count / min / max ways" + choice at each step

WHAT breaks the conversion
├── Wrong state (missing a dimension) → wrong memo key → wrong table
├── Wrong fill order → read uninitialized cells
├── 0/1 knapsack with forward w-loop → item used twice
└── Passing a list as memo key → TypeError; key on `(i, j, …)` only
```

---

## Quick Revision Triggers

| Stage | One-line test |
|-------|----------------|
| **State** | Can two different call paths produce the same `(args)`? → those args are your memo key |
| **Memo** | Recurrence unchanged; cache state in a `dict` (check key, store before return) |
| **Tabulate** | Reverse the recursion direction: if `f(i)` calls `f(i+1)`, fill `i` from high → low |
| **1D space** | Transition uses only `dp[i-1]` / `dp[i-2]` → two variables |
| **2D → 1 row** | Transition uses only row `i+1` → rolling array |
| **0/1 knapsack** | Loop `w` **backward** (high → low) |
| **Unbounded** | Loop `w` **forward** (low → high) |
| **Interval DP** | Outer loop = interval **length**; inner = left endpoint |

---

## Overlap in One Picture (Climbing Stairs)

```
                    f(5)
                   /    \
               f(4)      f(3)        ← f(3) computed twice
              /   \      /   \
           f(3)  f(2)  f(2) f(1)     ← f(2) computed three times
          /  \
       f(2) f(1)
```

- **Recursion:** `O(2^n)` — revisits nodes.
- **Memo on `n`:** `O(n)` time, `O(n)` stack + cache.
- **Bottom-up:** `O(n)` time, `O(n)` table → `O(1)` with two variables.

---

## Iteration Order Cheat Sheet

The #1 bottom-up bug is filling a cell before its dependencies exist. Use this table:

| State shape | Recursive direction | Bottom-up fill order | Depends on |
|-------------|--------------------|-----------------------|------------|
| `f(i)` suffix from `i` | calls `f(i+1)`, `f(i+2)` | `i` from **n → 0** | future indices |
| `f(i)` prefix to `i` | calls `f(i-1)`, `f(i-2)` | `i` from **0 → n** | past indices |
| `f(amount)` unbounded | `amount - coin` | `amount` from **0 → target** | smaller amounts |
| `f(i, w)` 0/1 knapsack | `i+1`, same `w` or `w-wt` | outer `i`, inner `w`; 1D: **w backward** | previous item row |
| `f(i, j)` two strings | `i+1`, `j+1` | `i` **m→0**, `j` **n→0** (or row-major) | suffixes / larger indices |
| `f(l, r)` interval | split at `k` | outer **length**, inner `l` | strictly smaller intervals |
| `f(r, c)` grid paths | `r+1`, `c+1` | `r` **0→m**, `c` **0→n** | top and left neighbors |

**Rule:** List what `dp[state]` reads on the RHS. Those cells must already be filled when you write `state`.

---

## Top-Down vs Bottom-Up — When to Use Which

| Use **memo (top-down)** | Use **bottom-up** |
|-------------------------|-------------------|
| State space is sparse (hash map stays small) | State space is dense array — table is natural |
| You want fastest path to correct code in interview | Recursion depth may overflow stack (`n > 10^4`) |
| Interval / tree DP — order is awkward to explain | Space optimization (rolling row) matters |
| Proving recurrence before committing to dimensions | Interviewer asks for iterative solution |

Both are `O(states × work per state)` when done correctly. Pick the one you can explain cleanly; convert after.

---

## Templates

### Top-down (memo dict)

Use a plain dict in interviews — easy to say “cache each subproblem by its state.” (`@lru_cache` is Python-only sugar; `maxsize=None` just means unlimited cache.)

```python
def solve(nums):
    memo = {}

    def dfs(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        if base_case:
            return base_value
        best = initial_value
        for choice in choices:
            best = combine(best, dfs(next_i, next_j))
        memo[(i, j)] = best
        return best

    return dfs(start_i, start_j)
```

**Interview tip:** Keep `nums` / strings in the outer scope; memo keys are only `(i, j, …)` — never the whole array.

### Bottom-up

```python
dp = initialize_table(base_cases)
for state in dependency_order:          # see cheat sheet above
    dp[state] = transition_from_smaller_states(dp)
return dp[answer_state]
```

### Space compression

```python
prev, curr = base, base
for state in order:
    curr = compute_using(prev)         # or prev2, prev1 for Fibonacci-style
    prev = curr
return prev
```

---

## Worked Examples — Full Pipeline

Each example follows: **state → recurrence → brute → memo → tabulate → (optional) space-opt**.

Complexity: **R** = recursive, **M** = memo, **B** = bottom-up, **S** = space-opt.

---

### 1. Climbing Stairs — linear / Fibonacci

**State:** `f(i)` = number of ways to reach step `i`.  
**Recurrence:** `f(i) = f(i-1) + f(i-2)` · base: `f(1)=1, f(2)=2`.

| Stage | Code idea | Time | Space |
|-------|-----------|------|-------|
| R | `return f(n-1)+f(n-2)` | O(2^n) | O(n) stack |
| M | `memo[n]` dict | O(n) | O(n) |
| B | `dp[i] = dp[i-1]+dp[i-2]`, `i: 3..n` | O(n) | O(n) |
| S | `prev2, prev1` rolling | O(n) | O(1) |

```python
# B — bottom-up
def climb(n: int) -> int:
    if n <= 2: return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**Lesson:** One-dimensional state depending on two prior values → rolling variables.

---

### 2. House Robber — take / skip

**State:** `f(i)` = max loot from houses `i..n-1` (suffix formulation).  
**Recurrence:** `f(i) = max(nums[i] + f(i+2), f(i+1))` · base: `f(n)=0`.

| Stage | Time | Space |
|-------|------|-------|
| R | O(2^n) | O(n) |
| M | O(n) | O(n) |
| B | O(n) | O(n) |
| S | O(n) | O(1) |

```python
# M — memo on index; nums in closure
def rob(nums):
    memo = {}

    def f(i):
        if i in memo:
            return memo[i]
        if i >= len(nums):
            return 0
        memo[i] = max(nums[i] + f(i + 2), f(i + 1))
        return memo[i]

    return f(0)

# B — fill suffix: i from n-1 down to 0
def rob_tab(nums: list[int]) -> int:
    n = len(nums)
    dp = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        dp[i] = max(nums[i] + dp[i + 2], dp[i + 1])
    return dp[0]
```

**Lesson:** “Take or skip” on a line → suffix index state; fill **right to left**.

---

### 3. Decode Ways — suffix string, forward tabulation

**State:** `f(i)` = ways to decode `s[i:]`.  
**Recurrence:** if `s[i]=='0'` → 0; else `f(i) = f(i+1)` + (optional) `f(i+2)` if two-digit valid.

| Stage | Time | Space |
|-------|------|-------|
| R | O(2^n) | O(n) |
| M | O(n) | O(n) |
| B | O(n) | O(n) |
| S | O(n) | O(1) |

```python
# R
def num_decodings_r(s: str, i: int = 0) -> int:
    if i == len(s): return 1
    if s[i] == '0': return 0
    ways = num_decodings_r(s, i + 1)
    if i + 1 < len(s) and 10 <= int(s[i:i+2]) <= 26:
        ways += num_decodings_r(s, i + 2)
    return ways

# B — prefix formulation: dp[i] = ways for s[:i]; fill left to right
def num_decodings(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 0 if s[0] == '0' else 1
    for i in range(2, n + 1):
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        two = int(s[i - 2:i])
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]
    return dp[n]
```

**Lesson:** Suffix recursion ↔ prefix tabulation. Leading `'0'` is a dead branch — handle in base/transition, not after the fact.

---

### 4. Coin Change (min coins) — unbounded knapsack

**State:** `f(rem)` = min coins to make amount `rem`.  
**Recurrence:** try every coin: `f(rem) = min(1 + f(rem - coin))`.

| Stage | Time | Space |
|-------|------|-------|
| R | O(coins^amount) | O(amount) |
| M | O(amount × coins) | O(amount) |
| B | O(amount × coins) | O(amount) |

```python
# B — increasing amount; each coin reusable → inner coin loop
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for cur in range(1, amount + 1):
        for c in coins:
            if cur >= c and dp[cur - c] != float('inf'):
                dp[cur] = min(dp[cur], dp[cur - c] + 1)
    return -1 if dp[amount] == float('inf') else dp[amount]
```

**Lesson:** Unbounded reuse → iterate amount **forward**; transition reads **smaller** amount.

---

### 5. Subset Sum — 0/1 knapsack (boolean)

**State:** `f(i, target)` = can we hit `target` using items from index `i` onward?  
**Recurrence:** take or skip item `i`.

| Stage | Time | Space |
|-------|------|-------|
| R | O(2^n) | O(n) |
| M | O(n × target) | O(n × target) |
| B | O(n × target) | O(target) with 1D |

```python
# M
def subset_sum_memo(nums, target):
    memo = {}

    def f(i, t):
        if (i, t) in memo:
            return memo[(i, t)]
        if t == 0:
            return True
        if i == len(nums) or t < 0:
            return False
        memo[(i, t)] = f(i + 1, t - nums[i]) or f(i + 1, t)
        return memo[(i, t)]

    return f(0, target)

# B — 1D: dp[w] = achievable?; w goes BACKWARD per item
def subset_sum(nums: list[int], target: int) -> bool:
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for w in range(target, num - 1, -1):   # backward = each item once
            dp[w] = dp[w] or dp[w - num]
    return dp[target]
```

**Lesson:** 0/1 choice → **backward** capacity loop. Partition Equal Subset Sum = subset sum with `target = sum/2`.

---

### 6. Longest Common Subsequence — 2D string DP

**State:** `f(i, j)` = LCS length of `a[i:]` and `b[j:]`.  
**Recurrence:** match → `1 + f(i+1,j+1)`; else `max(f(i+1,j), f(i,j+1))`.

| Stage | Time | Space |
|-------|------|-------|
| R | O(2^(m+n)) | O(m+n) |
| M | O(m × n) | O(m × n) |
| B | O(m × n) | O(m × n) |
| S | O(m × n) | O(min(m,n)) one row |

```python
# B — fill from bottom-right: i m-1..0, j n-1..0
def lcs(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    return dp[0][0]
```

**Lesson:** Two-sequence alignment → 2D table; match moves diagonally. Edit Distance uses the same grid with three operations instead of max.

---

### 7. Edit Distance — 2D with three operations

**State:** `f(i, j)` = min edits to turn `a[i:]` into `b[j:]`.  
**Recurrence:** match → `f(i+1,j+1)`; else `1 + min(delete, insert, replace)`.

```python
# B — same fill order as LCS; base: empty prefix costs
def min_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][n] = m - i
    for j in range(n + 1): dp[m][j] = n - j
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = dp[i + 1][j + 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i + 1][j],      # delete a[i]
                    dp[i][j + 1],      # insert b[j]
                    dp[i + 1][j + 1],  # replace
                )
    return dp[0][0]
```

**Lesson:** Initialize **border rows/cols** before the double loop — same state shape as LCS, different combine.

---

### 8. Unique Paths — grid DP

**State:** `f(r, c)` = paths from `(0,0)` to `(r,c)`.  
**Recurrence:** `f(r,c) = f(r-1,c) + f(r,c-1)`.

```python
# B — top-left to bottom-right; first row/col = 1
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[m - 1][n - 1]

# S — single row rolling
def unique_paths_opt(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
```

**Lesson:** Dependencies come from **top and left** → fill row-major forward.

---

### 9. Burst Balloons — interval DP (“last choice”)

**State:** `f(l, r)` = max coins bursting all balloons in open interval `(l, r)` (exclusive bounds; pad array with `1`).  
**Recurrence:** pick **last** balloon `k` to burst in `(l,r)` → neighbors `l` and `r` stay fixed.

```python
# M — pad with 1; memo on (left, right)
def max_coins(nums):
    arr = [1] + nums + [1]
    memo = {}

    def f(left, right):
        if (left, right) in memo:
            return memo[(left, right)]
        if left + 1 >= right:
            return 0
        best = 0
        for k in range(left + 1, right):
            best = max(best, arr[left] * arr[k] * arr[right] + f(left, k) + f(k, right))
        memo[(left, right)] = best
        return best

    return f(0, len(arr) - 1)

# B — outer loop: interval length; inner: left endpoint
def max_coins_tab(nums: list[int]) -> int:
    arr = [1] + nums + [1]
    n = len(arr)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for l in range(0, n - length):
            r = l + length
            for k in range(l + 1, r):
                dp[l][r] = max(dp[l][r], arr[l]*arr[k]*arr[r] + dp[l][k] + dp[k][r])
    return dp[0][n - 1]
```

**Lesson:** When “first action” makes neighbors unknown, reframe as **last action** in interval. Fill by **increasing interval length**.

---

## 15-Problem Conversion Reference

One row per problem — use after you can do the nine worked examples above.

| # | Problem | State | Memo key | Fill order | Space-opt | Key lesson |
|---|---------|-------|----------|------------|-----------|------------|
| 1 | Climbing Stairs | `f(i)` ways to step `i` | `i` | `i ↑` | 2 vars | Fibonacci-style |
| 2 | Min Cost Climbing Stairs | `f(i)` min cost to reach `i` | `i` | `i ↑` | 2 vars | Same shape, `min` + cost |
| 3 | House Robber | `f(i)` max from `i..end` | `i` | `i ↓` | 2 vars | Take/skip destroys adjacency |
| 4 | Decode Ways | `f(i)` ways for suffix `i` | `i` | prefix `i ↑` | 2 vars | `'0'` kills branch |
| 5 | Coin Change | `f(amount)` min coins | `amount` | `amount ↑` | 1D array | Unbounded → forward |
| 6 | Coin Change II | `f(i, amt)` ways, coins ≥ i | `(i, amt)` | coin outer, amt inner | 1D | Count = **add**, not min |
| 7 | Subset Sum | `f(i, t)` hit target `t` | `(i, t)` | items outer, **w ↓** | 1D bool | 0/1 → backward |
| 8 | Partition Equal Subset Sum | same as #7 | `(i, t)` | same | 1D | Target = `sum/2` |
| 9 | Target Sum | `f(i, sum)` ways to sum | `(i, sum)` | item + offset shift | map or shifted array | Negative sums need offset |
| 10 | LCS | `f(i, j)` suffix LCS | `(i, j)` | `i ↓`, `j ↓` | 1 row | Match → diagonal |
| 11 | Edit Distance | `f(i, j)` min edits | `(i, j)` | `i ↓`, `j ↓` | 1 row | Border init matters |
| 12 | Longest Palindromic Subseq | `f(l, r)` best in `[l,r]` | `(l, r)` | length ↑ | full table | Interval on one string |
| 13 | Unique Paths | `f(r, c)` paths to cell | `(r, c)` | `r ↑`, `c ↑` | 1 row | Top + left deps |
| 14 | Minimum Path Sum | `f(r, c)` min cost to cell | `(r, c)` | same as #13 | 1 row | Same grid, `min` combine |
| 15 | Burst Balloons | `f(l, r)` max in interval | `(l, r)` | length ↑ | full table | **Last** burst, not first |

**More depth:** [dynamic-programming.md](./15-dynamic-programming.md) — knapsack variants, stock DP, digit DP, bitmask.

---

## Common Conversion Bugs

| Bug | Symptom | Fix |
|-----|---------|-----|
| Wrong fill direction | Random-looking answers | Map recursive calls → dependency order (cheat sheet) |
| 0/1 knapsack forward loop | Same item counted twice | Loop `w` from `target` down to `num` |
| Unbounded knapsack backward | Impossible min coin counts | Loop `w` forward |
| Missing base row/col | Off-by-one on small inputs | Write borders before nested loops (Edit Distance) |
| State includes mutable array | `TypeError: unhashable` | Close over array; memoize `(i, j, …)` only |
| Interval DP wrong loop | Always 0 / wrong max | Outer = **length**, not left endpoint alone |
| Forgetting `inf` sentinel | `min` over empty set wrong | Init unreachable states to `inf`; check before return |

---

## Interview Script (say this out loud)

> “I'll define the recursive state and recurrence first — that's the proof of correctness.  
> The same states repeat, so I'll memoize on `[state keys]`.  
> For bottom-up I'll fill `[order]` because each state depends on `[deps]`.  
> Space can drop to `[O(…)]` because we only need `[prior row / two vars]`.”

That shows you understand **why** DP works, not just the pattern name.

---

## Final Mental Model

```
Recursion  = language for the recurrence
Memo       = cache on the recursion DAG
Bottom-up  = topological sort of that DAG
Space-opt  = drop dimensions no longer on the dependency frontier
```

Define the recursion clearly → everything else is table engineering.

---

## Flashcards

**What is the mechanical rule for deriving bottom-up fill order from a recurrence?** #flashcard
List every cell `dp[state]` reads on its right-hand side; those must already be filled when you write `state`. Recursion calling *forward* (`f(i+1)`) fills **n → 0**; calling *backward* (`f(i-1)`) fills **0 → n**. Interval DP loops outer on **length**, never on the left endpoint alone.

**In 1D knapsack, why does 0/1 loop weight downward while unbounded loops upward?** #flashcard
The 1D array conflates the "previous item" and "current item" rows. Descending `w` reads cells not yet overwritten this round — the previous row — so each item is used at most once. Ascending `w` reads cells already updated with the current item, which is exactly the reuse unbounded knapsack wants. Same array, opposite direction, different problem.

**A memoized solution raises `TypeError: unhashable type: 'list'`. What is the fix?** #flashcard
A mutable argument is in the memo key. Keep only hashable scalars (`i`, `j`, `remaining`) in the key and close over the array in the enclosing scope, or convert with `tuple(nums)`. Never key a cache on a structure that mutates during recursion.

**When should you choose top-down memoization over bottom-up tabulation?** #flashcard
Top-down when the state space is **sparse** (only reachable states get computed), when the fill order is awkward to explain (interval and tree DP), or when you want correct code fastest in an interview. Bottom-up when recursion depth risks a stack overflow (`n > 10^4`), or when space optimization to a rolling row matters. Both are O(states × work per state).

**Your DP returns 0 or a nonsense value on interval problems like Burst Balloons. What is the likely bug?** #flashcard
Iterating the outer loop over the left endpoint instead of over **interval length**. `f(l, r)` depends on strictly smaller intervals, so every shorter span must be complete before any longer one starts. Outer = length, inner = left endpoint.

**Why can a min-cost DP produce a wrong answer without an `inf` sentinel?** #flashcard
Unreachable states initialized to `0` masquerade as free solutions and win the `min`. Initialize unreachable states to `inf`, and check `dp[target] == inf` before returning to convert it to the problem's "impossible" value (typically `-1`).
