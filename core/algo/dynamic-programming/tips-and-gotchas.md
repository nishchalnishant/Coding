# DP Tips & Gotchas — Master Cheatsheet

Quick-reference for the 30-second pattern recognition, the 12 most common bugs, and the SDE-3 interview communication framework. For full pattern details see [README.md](README.md).

---

## Part 1 — Pattern Recognition (30-Second Triggers)

Read the problem statement and match against these signals before writing any code.

### Signal → Pattern Map

| Problem Says... | Pattern | Key State |
| :--- | :--- | :--- |
| "Count ways to reach N", "N stairs (1 or 2 steps)", "decode string" | **Linear / Fibonacci** | `dp[i]` from `dp[i-1]`, `dp[i-2]` |
| "Max/min with no adjacent selection", "rob houses", "delete and earn" | **Linear (House Robber)** | `dp[i] = max(dp[i-1], dp[i-2]+val)` |
| "Each item at most once" + weight/capacity limit | **0/1 Knapsack** | `dp[w]` backward loop |
| "Unlimited copies" + reach a target sum/amount | **Unbounded Knapsack** | `dp[w]` forward loop |
| "Count subsets with sum K", "number of ways to partition" | **0/1 Knapsack (count)** | `dp[w] += dp[w-num]`; `dp[0]=1` |
| "Best contiguous subarray", "max/min subarray sum/product" | **Kadane** | `end_here = max(x, end_here+x)` |
| "Two strings: align, match, edit, longest common" | **LCS family** | `dp[i][j]` on 2 string prefixes |
| "One array: longest strictly increasing sequence" | **LIS** | `bisect_left` on `tails[]` |
| "Grid, right/down moves, count/optimize paths" | **Grid DP** | `dp[i][j]` from `dp[i-1][j]`, `dp[i][j-1]` |
| "Optimal split of interval [i,j], try all k" | **Interval / MCM** | `dp[i][j]` filled by increasing length |
| "Palindrome structure, min cuts, min insertions" | **Palindrome DP** | `dp[i][j]` for `s[i..j]` |
| "Buy/sell stock, K transactions, cooldown, fee" | **Stock State Machine** | `dp[k][holding]` |
| "N ≤ 20, visit all nodes, assign tasks to items" | **Bitmask DP** | `dp[mask][node]` |
| "Count integers in [L,R] with digit property" | **Digit DP** | `dp[pos][tight][started][state]` |
| "DP on tree, subtree optimization, independent set" | **Tree DP** | Postorder DFS; return pair/tuple |
| "Expected value, probability, dice, knight path" | **Probability DP** | `dp[state]` = probability |
| "Minimax, optimal play by both players" | **Game Theory DP** | `dp[state]` = score difference |

---

## Part 2 — The 12 Most Common DP Bugs

### Bug 1: Wrong Loop Direction in 1D Knapsack

```python
# 0/1 Knapsack — WRONG (forward = allows reuse = unbounded)
for item in items:
    for w in range(item.weight, W+1):  # ❌ BUG
        dp[w] = max(dp[w], item.value + dp[w - item.weight])

# 0/1 Knapsack — CORRECT (backward = each item used once)
for item in items:
    for w in range(W, item.weight-1, -1):  # ✅
        dp[w] = max(dp[w], item.value + dp[w - item.weight])
```

**Rule:** Unbounded = forward. 0/1 = backward. Getting this wrong silently produces wrong answers.

---

### Bug 2: Wrong Base Case for Count Problems

```python
# Counting ways — WRONG
dp = [0] * (target + 1)   # dp[0] = 0 → nothing can be formed from empty set
# ❌: Every dp[w] will stay 0

# CORRECT
dp = [0] * (target + 1)
dp[0] = 1    # ✅: empty selection = one valid way to achieve sum 0
```

**Rule:** For count DP, `dp[0] = 1`. For min-cost DP, `dp[0] = 0`, rest `= inf`.

---

### Bug 3: Missing Modulo in Count Problems

```python
# Count subsequences — WRONG
dp[i][j] = dp[i-1][j-1] + dp[i-1][j]   # can overflow silently in Python? No, but in C++ yes

# Always modulo for problems that say "return answer mod 10^9+7"
MOD = 10**9 + 7
dp[i][j] = (dp[i-1][j-1] + dp[i-1][j]) % MOD   # ✅
```

---

### Bug 4: Off-by-One in 1-Indexed DP Tables

```python
# LCS with 1-indexed table — common off-by-one
for i in range(1, m+1):
    for j in range(1, n+1):
        if s1[i-1] == s2[j-1]:   # ✅ i,j are 1-indexed; string is 0-indexed
            dp[i][j] = dp[i-1][j-1] + 1
```

**Rule:** When using a `(m+1) × (n+1)` DP table for strings of length `m` and `n`, always access `s[i-1]` (not `s[i]`) inside the loop.

---

### Bug 5: Wrong Interval DP Fill Order

```python
# Interval DP — WRONG: filling by start position
for i in range(n-1, -1, -1):
    for j in range(i+1, n):
        ...  # dp[i][j] depends on dp[i][k] and dp[k+1][j] which may not be filled

# CORRECT: fill by INCREASING LENGTH
for length in range(2, n+1):
    for i in range(n - length + 1):
        j = i + length - 1
        for k in range(i, j):
            dp[i][j] = ...  # ✅ shorter intervals already filled
```

---

### Bug 6: Burst Balloons — k is Last, Not First

```python
# Burst Balloons — WRONG: k = first to burst
# coins = balloons[k-1] * balloons[k] * balloons[k+1]  # ❌ neighbors may already be gone

# CORRECT: k = LAST to burst in (left, right)
coins = balloons[left] * balloons[k] * balloons[right]   # ✅ left & right still present
```

---

### Bug 7: Regex `*` Handling — Zero Occurrences

```python
# Regex matching — WRONG: forgetting zero-occurrence case
if p[j-1] == '*':
    if p[j-2] == s[i-1] or p[j-2] == '.':
        dp[i][j] = dp[i-1][j]   # ❌ forgot zero-occurrence: skip p[j-2] and '*'

# CORRECT
if p[j-1] == '*':
    dp[i][j] = dp[i][j-2]       # ✅ zero occurrences: skip both p[j-2] and '*'
    if p[j-2] == '.' or p[j-2] == s[i-1]:
        dp[i][j] = dp[i][j] or dp[i-1][j]  # ✅ one or more occurrences
```

---

### Bug 8: Not Initializing `dp[i][0]` and `dp[0][j]` for Edit Distance

```python
# Edit Distance — WRONG: forgetting base cases
dp = [[0]*(n+1) for _ in range(m+1)]
# ❌ dp[i][0] = 0 means "0 ops to make empty string from word1[:i]" — wrong

# CORRECT
for i in range(m+1): dp[i][0] = i   # delete i chars from word1
for j in range(n+1): dp[0][j] = j   # insert j chars to form word2
```

---

### Bug 9: Digit DP Cache Not Cleared Between Calls

```python
# WRONG: calling f(R) then f(L-1) with same cached dp
result = count_up_to(R) - count_up_to(L - 1)  # ❌ if dp not cleared

# CORRECT
def count_up_to(limit):
    ...
    result = dp(0, True, False, 0)
    dp.cache_clear()   # ✅ clear before returning
    return result
```

---

### Bug 10: Dungeon Game — Forward DP is Impossible

```python
# Dungeon Game — WRONG: trying to go forward
# dp[i][j] = min HP when LEAVING cell (i,j) — but what HP do you need to ENTER?
# Forward DP cannot determine entry HP without knowing the future path.

# CORRECT: work BACKWARD from bottom-right
dp[m-1][n-1] = max(1 - dungeon[m-1][n-1], 1)
# Fill right-to-left, bottom-to-top ✅
```

---

### Bug 11: Stock Trading — Using `sold` in Same Iteration (Cooldown)

```python
# Stock Cooldown — WRONG
for p in prices:
    sold = hold + p
    hold = max(hold, rest - p)
    rest = max(rest, sold)   # ❌ uses TODAY's sold, not yesterday's

# CORRECT: save prev_sold before updating
for p in prices:
    prev_sold = sold
    sold = hold + p
    hold = max(hold, rest - p)
    rest = max(rest, prev_sold)   # ✅ yesterday's sold
```

---

### Bug 12: LIS — `tails` is NOT the Actual LIS

```python
def lis_nlogn(nums):
    tails = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails): tails.append(x)
        else: tails[pos] = x
    return len(tails)   # ✅ length is correct

# WRONG: treating tails as the actual subsequence
# tails = [2, 3, 5] for [3, 5, 2, 8] — this is NOT an LIS; it's a bookkeeping artifact
# To get the actual LIS, use parent[] tracking in the O(N²) approach
```

---

## Part 3 — Space Optimization Decision Tree

```
Does dp[i] depend only on dp[i-1]?
  ├─ Yes, and dp[i-1] only → Use 1 scalar (rolling variable)
  └─ Yes, and dp[i-1] and dp[i-2] → Use 2 variables (prev2, prev1)

Does dp[i][j] depend only on dp[i-1][*]?
  └─ Use 1D rolling array; process in correct direction

Does dp[i][j] use diagonal dp[i-1][j-1]?
  └─ Use 1D array + `prev` scalar to hold diagonal before overwrite

Does dp[i][j] depend on dp[i+1][*] or dp[i][j+1]?
  └─ Fill from bottom-right; still 1D rolling possible

Is the state space sparse (most states unreachable)?
  └─ Use dict-memo (@lru_cache or explicit dict) instead of full array
```

---

## Part 4 — Iteration Direction Rules

| DP Type | Outer Loop | Inner Loop | Direction | Reason |
| :--- | :--- | :--- | :--- | :--- |
| 0/1 Knapsack | Items | Capacity | **Backward** (W→0) | Prevents reusing same item |
| Unbounded Knapsack | Items | Capacity | **Forward** (0→W) | Allows reusing same item |
| Coin Change Count (combos) | Coins outer | Amount forward | Forward | Coins outer = combinations |
| Coin Change Count (perms) | Amount outer | Coins inner | Forward | Amount outer = permutations |
| LCS / Edit Distance | Row by row | Left → right | Forward | Reads from `dp[i-1]` (done) |
| Interval DP | By length | By start | Ascending length | Short intervals needed first |
| Palindrome DP | By length | By start | Ascending length | Shorter substring checked first |
| Grid DP | Row by row | Left → right | Forward | Top-left dependencies |
| Reverse Grid DP (Dungeon) | Row by row | Right → left | Backward | Bottom-right dependencies |

---

## Part 5 — SDE-3 Interview Communication Framework

Use this structure for every DP problem in an interview:

```
1. IDENTIFY (30 seconds)
   "This looks like [pattern] because [signal in problem statement]."
   "The subproblems overlap — [which recursive calls repeat]."

2. STATE (1 minute)
   "I'll define dp[i] as [explicit English description]."
   "The state needs [explain why this is the minimum set of parameters]."

3. RECURRENCE (2 minutes)
   "The recurrence is: dp[i] = [formula]."
   "This comes from [choices available at each step]."
   Write it on the whiteboard/IDE before coding.

4. BASE CASES (30 seconds)
   "Base cases: dp[0] = [value] because [reason]."
   Check: does your recurrence work for the smallest valid inputs?

5. ORDER (30 seconds)
   "I'll fill the table [left-to-right / by increasing length / backwards]."
   "This ensures [the RHS values are already computed]."

6. CODE (10-15 minutes)
   Start with 2D if unsure; optimize to 1D after correctness is verified.

7. SPACE OPTIMIZE (2 minutes)
   "Can I reduce from O(N²) to O(N)?"
   Offer the optimization but implement only if time allows.

8. COMPLEXITY
   "Time: O([states] × [transitions per state]) = O([result])."
   "Space: O([table size]) → optimizable to O([reduced])."
```

---

## Part 6 — When NOT to Use DP

> [!CAUTION]
> Applying DP when another approach is better wastes time and produces unnecessarily complex code.

| Scenario | Better Approach | Why DP Is Wrong |
| :--- | :--- | :--- |
| **Activity selection / interval scheduling** | Greedy (sort by end time) | Greedy choice property holds; no overlapping subproblems |
| **Shortest path in graph (no negative cycles)** | Dijkstra / BFS | No overlapping subproblem structure (unless DAG) |
| **Subproblems don't overlap** | Divide & Conquer | Memoization adds overhead with no benefit |
| **Problem has the greedy choice property** | Greedy | DP over-enumerates; greedy is O(N) vs O(N²) |
| **State space is too large** | Math / algebra | Bitmask DP breaks at N>20; 2D DP breaks at N=M=10^4 |
| **Exact reconstruction required (not optimization)** | Backtracking | DP finds optimal value; reconstruction is post-processing |
| **Counting combinations (closed form)** | Math (combinatorics) | `C(n,k)` is O(k) — faster than O(N²) DP |

---

## Part 7 — Complexity Quick Reference

| Pattern | Time | Space | Optimized Space |
| :--- | :--- | :--- | :--- |
| Linear 1D | O(N) | O(N) | O(1) or O(2) |
| 0/1 Knapsack | O(N×W) | O(N×W) | O(W) |
| Unbounded Knapsack | O(N×W) | O(W) | O(W) |
| LCS / Edit Distance | O(M×N) | O(M×N) | O(min(M,N)) |
| LIS O(N²) | O(N²) | O(N) | O(N) |
| LIS O(N log N) | O(N log N) | O(N) | O(N) |
| Interval DP | O(N³) | O(N²) | Rarely reducible |
| Bitmask DP | O(2^N × N) | O(2^N × N) | Rarely reducible |
| Digit DP | O(D × |state|) | O(D × |state|) | Dict memo for sparse |
| Tree DP | O(N) | O(N) | O(depth) for DFS stack |
| Deque-optimized DP | O(N) | O(N) | O(N) |
| CHT | O(N log N) | O(N) | O(N) |

---

## Part 8 — 10 Patterns in One Line Each

```
Linear:     dp[i] from dp[i-1], dp[i-2]; space-optimize to 2 vars
0/1 Knap:   iterate items outer, capacity BACKWARD inner
Unbounded:  iterate items outer, capacity FORWARD inner
Kadane:     end_here = max(x, end_here+x); track global max
LCS:        dp[i][j]: match→diag+1, else max(up,left)
LIS:        patience sort with bisect_left; tails[] is NOT the LIS
Interval:   fill by increasing length; k is the last operation
Grid:       dp[i][j] from top/left; Dungeon reverses direction
Palindrome: is_pal[i][j] = s[i]==s[j] AND is_pal[i+1][j-1]
Bitmask:    dp[mask][node]; enumerate submasks in O(3^N)
```

---

## See also

- [README.md](README.md) — 4-step framework and all patterns
- [dp-aditya-verma.md](dp-aditya-verma.md) — Full code for all 9 patterns
- [questions-bank.md](questions-bank.md) — 70 tiered drill questions
- [advanced-dp-optimizations.md](advanced-dp-optimizations.md) — CHT, D&C, SOS DP
