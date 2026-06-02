# Recursion to DP: From Brute Force to Bottom-Up

This guide is for the exact interview moment where you can see recursion, but you also suspect the recursion is repeating work. The goal is to learn the full progression:

1. Write the recursive brute-force solution correctly.
2. Identify the subproblem state.
3. Add memoization to avoid repeated work.
4. Convert the recurrence into a bottom-up table.
5. Optimize space when the dependency window is small.

If you can do those five steps cleanly, you can solve most classic DP interview questions without memorizing every pattern.

---

## First-Principles Thinking

### What recursion is really doing

Recursion is not the final solution. It is a way to describe the problem in terms of smaller versions of itself.

The first question to ask is:

> “If I already knew the answer to smaller subproblems, how would I build the answer for the current one?”

That sentence is the DP transition.

### Why recursion becomes DP

DP appears when two things are true:

1. The problem has **optimal substructure** or a counting structure built from smaller states.
2. The same subproblem appears again and again in the recursion tree.

When that happens:

- plain recursion recomputes the same work many times,
- memoization saves the result the first time,
- bottom-up computes the same answers in dependency order.

### The mental model

Think in this order:

- **Recursion:** “What are my choices?”
- **Memoization:** “Have I solved this state before?”
- **Bottom-up:** “In what order should I fill states so dependencies already exist?”

That is the entire bridge from recursion to DP.

---

## The Universal Progression

### Step 1: Write the recursive state

Define the smallest input that uniquely identifies a subproblem.

Examples:

- `f(i)` for position-based problems
- `f(i, sum)` for subset/capacity problems
- `f(i, j)` for two-string or grid problems
- `f(i, j, k)` for interval or game problems

If your state is wrong, everything after that is wrong.

### Step 2: Write the recurrence

For each state, write:

- what choices you can make,
- how each choice changes the state,
- what the base case is.

This is where most interview solutions start to emerge.

### Step 3: Detect overlap

If the same `(state)` is reached through different paths, you have overlapping subproblems.

Common signs:

- repeated recursion on the same index pair,
- same suffix/prefix subproblem appears multiple times,
- exponential tree with duplicate states.

### Step 4: Add memoization

Store the answer for each state the first time you compute it.

That turns exponential recursion into polynomial-time DP.

### Step 5: Convert to bottom-up

Once the recurrence is clear, ask:

> “Which states must be computed before this one?”

Then fill the table in that dependency order.

### Step 6: Compress space

If each state only needs:

- the previous 1 row,
- the previous 2 rows,
- or a sliding window,

then compress the DP table.

---

## Bottom-Up Translation Checklist

Before coding tabulation, answer these in order:

1. What is the state?
2. What is the transition?
3. What are the base cases?
4. What is the iteration order?
5. What dimensions can be compressed?

If you can answer those five, the code is usually straightforward.

---

## Template You Should Memorize

### Top-down memoized recursion

```python
from functools import lru_cache

@lru_cache(None)
def solve(state1, state2):
    if base_case:
        return base_value

    best = initial_value
    for choice in choices:
        best = combine(best, solve(next_state))
    return best
```

### Bottom-up tabulation

```python
dp = initialize_table()
for state in valid_order:
    dp[state] = transition_from_smaller_states()
return dp[answer_state]
```

### Space optimization

```python
prev = ...
curr = ...
for state in order:
    curr = compute_using_prev()
    prev = curr
```

---

## Worked Examples: Recursion → Memo → Bottom-Up

These examples are the real bridge from recursion to DP. Read them as transformations, not as separate solutions.

### 1. Climbing Stairs

#### Step A: Recursive brute force

```python
def climb_stairs_recursive(n: int) -> int:
    if n <= 2:
        return n
    return climb_stairs_recursive(n - 1) + climb_stairs_recursive(n - 2)
```

Why this works:

- To reach step `n`, your last move must come from `n-1` or `n-2`.
- That means the answer is the sum of the answers to those smaller states.

Why this is slow:

- `f(n-1)` and `f(n-2)` both compute `f(n-3)`, `f(n-4)`, and so on.
- The recursion tree repeats the same work exponentially.

#### Step B: Memoized recursion

```python
from functools import lru_cache

@lru_cache(None)
def climb_stairs_memo(n: int) -> int:
    if n <= 2:
        return n
    return climb_stairs_memo(n - 1) + climb_stairs_memo(n - 2)
```

What changed:

- The recurrence did not change.
- Only the repeated work was cached.

#### Step C: Bottom-up tabulation

```python
def climb_stairs_bottom_up(n: int) -> int:
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

#### Step D: Space optimization

```python
def climb_stairs_optimized(n: int) -> int:
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
```

Main lesson:

- If a state depends only on the previous two states, you do not need the whole table.

---

### 2. House Robber

#### Step A: Recursive brute force

```python
def house_robber_recursive(nums: list[int], i: int = 0) -> int:
    if i >= len(nums):
        return 0
    take = nums[i] + house_robber_recursive(nums, i + 2)
    skip = house_robber_recursive(nums, i + 1)
    return max(take, skip)
```

Why this works:

- At house `i`, you either rob it and skip the next house, or skip it and move to the next house.

Why this is a DP problem:

- The same index `i` is computed from multiple paths.
- That makes memoization useful.

#### Step B: Memoized recursion

```python
from functools import lru_cache

@lru_cache(None)
def house_robber_memo(nums_tuple: tuple[int, ...], i: int = 0) -> int:
    if i >= len(nums_tuple):
        return 0
    take = nums_tuple[i] + house_robber_memo(nums_tuple, i + 2)
    skip = house_robber_memo(nums_tuple, i + 1)
    return max(take, skip)
```

Note:

- For caching, the input array must be hashable if included in the memoized signature.
- In interviews, it is cleaner to store `nums` externally and memoize only on `i`.

Cleaner memo version:

```python
def house_robber_memo_clean(nums: list[int]) -> int:
    from functools import lru_cache

    @lru_cache(None)
    def solve(i: int) -> int:
        if i >= len(nums):
            return 0
        return max(nums[i] + solve(i + 2), solve(i + 1))

    return solve(0)
```

#### Step C: Bottom-up tabulation

```python
def house_robber_bottom_up(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]

    dp = [0] * (n + 1)
    dp[n] = 0
    dp[n - 1] = nums[n - 1]

    for i in range(n - 2, -1, -1):
        dp[i] = max(nums[i] + dp[i + 2], dp[i + 1])
    return dp[0]
```

#### Step D: Space optimization

```python
def house_robber_optimized(nums: list[int]) -> int:
    next1 = 0
    next2 = 0
    for i in range(len(nums) - 1, -1, -1):
        current = max(nums[i] + next2, next1)
        next2 = next1
        next1 = current
    return next1
```

Main lesson:

- The recursive state is not “how many houses exist”; it is “what is the best answer starting from index `i`”.

---

### 3. Coin Change (minimum coins)

#### Step A: Recursive brute force

```python
def coin_change_recursive(coins: list[int], amount: int) -> int:
    if amount == 0:
        return 0
    if amount < 0:
        return float("inf")

    best = float("inf")
    for coin in coins:
        candidate = coin_change_recursive(coins, amount - coin)
        if candidate != float("inf"):
            best = min(best, 1 + candidate)
    return best
```

Why this works:

- For the remaining amount, try every coin.
- The best result over all choices is the answer.

Why memoization matters:

- The same `amount` value gets recomputed many times.

#### Step B: Memoized recursion

```python
def coin_change_memo(coins: list[int], amount: int) -> int:
    from functools import lru_cache

    @lru_cache(None)
    def solve(rem: int) -> int:
        if rem == 0:
            return 0
        if rem < 0:
            return float("inf")

        best = float("inf")
        for coin in coins:
            candidate = solve(rem - coin)
            if candidate != float("inf"):
                best = min(best, 1 + candidate)
        return best

    answer = solve(amount)
    return -1 if answer == float("inf") else answer
```

#### Step C: Bottom-up tabulation

```python
def coin_change_bottom_up(coins: list[int], amount: int) -> int:
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for current in range(1, amount + 1):
        for coin in coins:
            if current - coin >= 0 and dp[current - coin] != float("inf"):
                dp[current] = min(dp[current], dp[current - coin] + 1)

    return -1 if dp[amount] == float("inf") else dp[amount]
```

Main lesson:

- This is an unbounded DP because you may use each coin many times.
- That is why amount increases from `0` to target.

---

### 4. Longest Common Subsequence

#### Step A: Recursive brute force

```python
def lcs_recursive(a: str, b: str, i: int = 0, j: int = 0) -> int:
    if i == len(a) or j == len(b):
        return 0
    if a[i] == b[j]:
        return 1 + lcs_recursive(a, b, i + 1, j + 1)
    return max(
        lcs_recursive(a, b, i + 1, j),
        lcs_recursive(a, b, i, j + 1),
    )
```

Why this works:

- If the characters match, keep them and move diagonally.
- If not, drop one from either side and try again.

#### Step B: Memoized recursion

```python
def lcs_memo(a: str, b: str) -> int:
    from functools import lru_cache

    @lru_cache(None)
    def solve(i: int, j: int) -> int:
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + solve(i + 1, j + 1)
        return max(solve(i + 1, j), solve(i, j + 1))

    return solve(0, 0)
```

#### Step C: Bottom-up tabulation

```python
def lcs_bottom_up(a: str, b: str) -> int:
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

Main lesson:

- For two-string DP, the table often represents suffixes when built bottom-up from the end.

---

### 5. Unique Paths

#### Step A: Recursive brute force

```python
def unique_paths_recursive(m: int, n: int, r: int = 0, c: int = 0) -> int:
    if r == m - 1 and c == n - 1:
        return 1
    if r >= m or c >= n:
        return 0
    return unique_paths_recursive(m, n, r + 1, c) + unique_paths_recursive(m, n, r, c + 1)
```

#### Step B: Memoized recursion

```python
def unique_paths_memo(m: int, n: int) -> int:
    from functools import lru_cache

    @lru_cache(None)
    def solve(r: int, c: int) -> int:
        if r == m - 1 and c == n - 1:
            return 1
        if r >= m or c >= n:
            return 0
        return solve(r + 1, c) + solve(r, c + 1)

    return solve(0, 0)
```

#### Step C: Bottom-up tabulation

```python
def unique_paths_bottom_up(m: int, n: int) -> int:
    dp = [[0] * n for _ in range(m)]
    for r in range(m):
        dp[r][0] = 1
    for c in range(n):
        dp[0][c] = 1

    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[m - 1][n - 1]
```

Main lesson:

- Grid DP usually becomes easy once you decide which two directions feed the current cell.

---

### 6. Burst Balloons

#### Step A: Recursive brute force

```python
def burst_balloons_recursive(nums: list[int], left: int, right: int) -> int:
    if left + 1 == right:
        return 0

    best = 0
    for k in range(left + 1, right):
        best = max(
            best,
            nums[left] * nums[k] * nums[right]
            + burst_balloons_recursive(nums, left, k)
            + burst_balloons_recursive(nums, k, right),
        )
    return best
```

Why this is tricky:

- You do not choose the first balloon to burst.
- You choose the last balloon to burst inside an interval.
- That makes the neighbors of the chosen balloon fixed.

#### Step B: Memoized recursion

```python
def burst_balloons_memo(nums: list[int]) -> int:
    from functools import lru_cache

    arr = [1] + nums + [1]

    @lru_cache(None)
    def solve(left: int, right: int) -> int:
        if left + 1 == right:
            return 0
        best = 0
        for k in range(left + 1, right):
            best = max(
                best,
                arr[left] * arr[k] * arr[right] + solve(left, k) + solve(k, right),
            )
        return best

    return solve(0, len(arr) - 1)
```

#### Step C: Bottom-up tabulation

```python
def burst_balloons_bottom_up(nums: list[int]) -> int:
    arr = [1] + nums + [1]
    n = len(arr)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    arr[left] * arr[k] * arr[right] + dp[left][k] + dp[k][right],
                )
    return dp[0][n - 1]
```

Main lesson:

- Interval DP usually means “choose a split point” and fill by increasing interval length.

---

## 15 Problems That Show the Progression

The table below is the important part. Read it as:

- recursion state,
- memo key,
- bottom-up order,
- and the main lesson you should learn.

| # | Problem | Recursive state | Memo key | Bottom-up order | Main lesson |
|---|---|---|---|---|---|
| 1 | Climbing Stairs | `f(i)` = ways to reach step `i` | `i` | left to right | The simplest Fibonacci-style DP |
| 2 | Min Cost Climbing Stairs | `f(i)` = min cost to reach `i` | `i` | left to right | DP can minimize, not just count |
| 3 | House Robber | `f(i)` = best loot from first `i` houses | `i` | left to right | Each state is “take or skip” |
| 4 | Decode Ways | `f(i)` = ways to decode suffix starting at `i` | `i` | right to left | Base case may live at the end of the string |
| 5 | Coin Change (min coins) | `f(amount)` = min coins for remaining amount | `amount` | increasing amount | Unbounded choice means forward transitions |
| 6 | Coin Change II | `f(i, amount)` = ways using coins from index `i` onward | `(i, amount)` | by coin, then amount | Count DP uses addition, not min/max |
| 7 | Subset Sum | `f(i, target)` = can we make target using first `i` items | `(i, target)` | item by item | Binary choice: take or skip |
| 8 | Partition Equal Subset Sum | Same as subset sum | `(i, target)` | item by item | A “partition” problem is often a subset sum problem |
| 9 | Target Sum | `f(i, sum)` = number of ways to reach sum with first `i` numbers | `(i, sum)` | item by item with offset | Negative sums often need shifting or hashing |
| 10 | Longest Common Subsequence | `f(i, j)` = LCS of prefixes `s1[:i]`, `s2[:j]` | `(i, j)` | row-major / col-major | Two-string alignment is classic 2D DP |
| 11 | Edit Distance | `f(i, j)` = min edits for prefixes `s1[:i]`, `s2[:j]` | `(i, j)` | row-major / col-major | Base rows/cols matter more than the recurrence |
| 12 | Longest Palindromic Subsequence | `f(l, r)` = best in substring `s[l:r+1]` | `(l, r)` | increasing length | Interval DP fills by substring length |
| 13 | Unique Paths | `f(r, c)` = ways to reach cell `(r, c)` | `(r, c)` | top-left to bottom-right | Grid DP is just 2D recursion with boundaries |
| 14 | Minimum Path Sum | `f(r, c)` = min cost to reach cell `(r, c)` | `(r, c)` | top-left to bottom-right | Same structure as Unique Paths, different combine function |
| 15 | Burst Balloons | `f(l, r)` = best score inside interval `(l, r)` | `(l, r)` | increasing interval length | Sometimes the best move is to choose the **last** action, not the first |

---

## How to Think Through Each Stage

### Stage A: Pure recursion

Ask:

- What are my choices?
- What happens if I choose option A?
- What happens if I choose option B?
- What is the base case?

At this stage, do not care about efficiency. Just make the recurrence correct.

### Stage B: Memoization

Ask:

- What combination of parameters uniquely identifies the subproblem?
- Can I use a map or array to cache the answer?
- Are the repeated states obvious from the recursion tree?

Use memoization when:

- the same state appears multiple times,
- the problem is still naturally recursive,
- you want the easiest correctness proof.

### Stage C: Bottom-up

Ask:

- What smaller states does this state depend on?
- Can I reverse the recursion order into an iteration order?
- Do I need one row, two rows, or the whole table?

Use bottom-up when:

- recursion depth is too high,
- iterative filling is easier to explain,
- or space optimization is important.

---

## Problem-by-Problem Progression Notes

### 1. Climbing Stairs

- Recursion: `f(n) = f(n-1) + f(n-2)`
- Memoization: cache `n`
- Bottom-up: left to right from `1` to `n`
- Key idea: this is Fibonacci with a story.

### 2. Min Cost Climbing Stairs

- Recursion: minimum cost to reach step `i`
- Memoization: cache step index
- Bottom-up: compute from lower steps upward
- Key idea: same recursion as climbing stairs, but combine with `min` and cost.

### 3. House Robber

- Recursion: at each house, take or skip
- Memoization: cache index
- Bottom-up: `dp[i]` depends on `i-1` and `i-2`
- Key idea: one choice destroys adjacency, so only two prior states matter.

### 4. Decode Ways

- Recursion: decode one digit or two digits if valid
- Memoization: cache suffix index
- Bottom-up: right to left
- Key idea: base case on the empty suffix is crucial.

### 5. Coin Change (min coins)

- Recursion: choose any coin and reduce remaining amount
- Memoization: cache amount
- Bottom-up: amount increasing from `0` to target
- Key idea: unbounded reuse means forward iteration is natural.

### 6. Coin Change II

- Recursion: count ways, not minimum
- Memoization: cache `(i, amount)`
- Bottom-up: coins outer loop, amount inner loop
- Key idea: counting DP adds ways; it does not minimize them.

### 7. Subset Sum

- Recursion: take or skip the current item
- Memoization: cache `(i, target)`
- Bottom-up: item by item
- Key idea: this pattern becomes many other partition problems.

### 8. Partition Equal Subset Sum

- Recursion: same as subset sum with target = total / 2
- Memoization: same state
- Bottom-up: same as subset sum
- Key idea: many “partition” questions are disguised subset sum.

### 9. Target Sum

- Recursion: add or subtract each number
- Memoization: cache `(i, running_sum)`
- Bottom-up: offset-based 2D table or hashmap
- Key idea: negative states often require shifting or sparse storage.

### 10. LCS

- Recursion: compare suffixes of two strings
- Memoization: cache `(i, j)`
- Bottom-up: fill from small prefixes to larger prefixes
- Key idea: if characters match, move diagonally; otherwise choose best of two sides.

### 11. Edit Distance

- Recursion: insert, delete, replace
- Memoization: cache `(i, j)`
- Bottom-up: row/column DP
- Key idea: the three operations are the recurrence.

### 12. Longest Palindromic Subsequence

- Recursion: solve inside substring `[l, r]`
- Memoization: cache `(l, r)`
- Bottom-up: increasing substring length
- Key idea: interval DP almost always fills by length.

### 13. Unique Paths

- Recursion: move down or right
- Memoization: cache cell
- Bottom-up: fill row-major
- Key idea: grid boundaries are the base cases.

### 14. Minimum Path Sum

- Recursion: same movement as Unique Paths
- Memoization: cache cell
- Bottom-up: same order
- Key idea: same state shape, different combine function (`min` instead of count).

### 15. Burst Balloons

- Recursion: choose the **last** balloon to burst in an interval
- Memoization: cache interval `(l, r)`
- Bottom-up: increasing interval length
- Key idea: interval DP often becomes easy once you shift from “first choice” to “last choice.”

---

## How to Explain This in an Interview

When you’re asked a DP question, say this out loud:

> “I’ll first write the recursive version to define the state and recurrence.  
> Then I’ll check whether states repeat and memoize them.  
> After that I’ll convert the recurrence into bottom-up order and see whether space can be optimized.”

That answer tells the interviewer:

- you know the workflow,
- you understand the reason behind DP,
- and you can move from recursion to tabulation without guessing.

---

## Final Mental Model

Recursion is the language.
Memoization is the cache.
Bottom-up is the execution order.

If you can clearly define the recursion, the rest of DP is usually just engineering.
