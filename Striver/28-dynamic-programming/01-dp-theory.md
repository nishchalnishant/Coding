---
module: striver/28-dynamic-programming
lesson: 1
topic: Dynamic programming from recursion to tabulation — states, recurrences, loop order, space optimisation, and the DP families
source: https://takeuforward.org/learning/dsa/introduction-to-dp?category=introduction&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, memoization, tabulation, theory]
---
# 1. Dynamic Programming: From Recursion to Tabulation

← [Part 28 index](README.md) · Next → [Climbing stairs](02-climbing-stairs.md)

> [!abstract] What this covers
> **Core idea:** DP is recursion that never solves the same subproblem twice.
> - Write the brute-force recursion over a small **state**.
> - Cache it (**memoization**).
> - Flip it into loops (**tabulation**).
> - Keep only the rows you still read (**space optimisation**).
>
> **You'll be able to:** spot when DP applies; define a state from "what do I need to know to finish?"; write the recurrence from "what is the last (or first) choice?"; pick the loop order from the dependency direction; cut a dimension; reconstruct the actual answer; and map a new problem onto one of the eight Striver families.
> **Source:** [Striver: Introduction to DP](https://takeuforward.org/learning/dsa/introduction-to-dp?category=introduction&source=strivers-a2z-dsa-sheet) · **Time:** 75 min

**Sections:** [1. When DP applies](#1-when-dp-applies) · [2. The 4-stage pipeline](#2-the-4-stage-pipeline) · [3. Choosing the state](#3-choosing-the-state) · [4. Writing the recurrence](#4-writing-the-recurrence) · [5. Base cases and sentinels](#5-base-cases-and-sentinels) · [6. Loop order in tabulation](#6-loop-order-in-tabulation) · [7. Space optimisation](#7-space-optimisation) · [8. The DP families](#8-the-dp-families) · [9. Reconstructing the answer](#9-reconstructing-the-answer) · [10. Complexity accounting](#10-complexity-accounting) · [Common mistakes](#common-mistakes) · [Practice](#practice) · [Key terms](#key-terms) · [Flashcards](#flashcards)

---

## 1. When DP applies

DP applies when a problem has both of these properties:

| Property | Meaning | Test |
|---|---|---|
| **Optimal substructure** | The best answer is built from best answers to smaller subproblems. | "If I fix the first/last choice, is the rest the same problem, only smaller?" |
| **Overlapping subproblems** | The same subproblem is reached by many paths. | Draw the recursion tree for small input: do nodes repeat? |

**Trigger phrases:** "count the ways", "minimum/maximum cost", "is it possible", "longest/shortest …", "number of distinct …", each over a sequence of choices.

**Not DP:**
- When **greedy** is provably correct (activity selection, jump game I). DP still works there, only more slowly.
- When subproblems don't overlap (merge sort). That is divide and conquer.
- When the state would need the whole history ("which elements have I used?" on n = 50). That needs a bitmask or a different idea.

---

## 2. The 4-stage pipeline

Striver's method, illustrated on Fibonacci / climbing stairs:

| Stage | Code shape | Time | Space |
|---|---|---|---|
| 1. Recursion | `f(n) = f(n−1) + f(n−2)` | O(2ⁿ) | O(n) stack |
| 2. Memoization (top-down) | `if dp[n] != −1: return dp[n]`, then store | O(n) | O(n) + O(n) stack |
| 3. Tabulation (bottom-up) | `for i in 2..n: dp[i] = dp[i−1] + dp[i−2]` | O(n) | O(n) |
| 4. Space-optimised | `prev2, prev1 = prev1, prev1 + prev2` | O(n) | O(1) |

```python
# 1 → 2: add a cache
def f(n, dp):
    if n <= 1: return 1
    if dp[n] != -1: return dp[n]
    dp[n] = f(n - 1, dp) + f(n - 2, dp)
    return dp[n]

# 2 → 3: base cases become initial cells, recursion becomes a loop in the reverse direction
dp = [0] * (n + 1); dp[0] = dp[1] = 1
for i in range(2, n + 1): dp[i] = dp[i - 1] + dp[i - 2]

# 3 → 4: only the last two cells are read
a, b = 1, 1
for _ in range(2, n + 1): a, b = b, a + b
```

**Rules for each conversion:**
- **Recursion → memo:** one cache dimension per changing parameter. Choose an "unset" value (−1, `None`) that can never be a real answer.
- **Memo → tabulation:**
  - The base cases become initialised cells.
  - Each parameter becomes a loop, running **opposite** to the direction the recursion shrinks. `f(i)` calls `f(i−1)`, so loop `i` upward. `f(i)` calls `f(i+1)`, so loop downward.
  - The recursive body becomes the loop body, unchanged.
- **Tabulation → space:** if row `i` reads only row `i−1` (or `i+1`), keep two rows: `prev`, `cur`. If it reads only `dp[i−1][smaller j]`, a 1D array updated with `j` descending suffices (0/1 knapsack).

In interviews, memoization is usually enough to get credit. Tabulation avoids recursion-depth limits (Python's default is ~1000) and opens the door to space optimisation.

---

## 3. Choosing the state

> **The state is the minimum information needed to solve the rest of the problem.**

Ask: "If I froze the process here, what would someone else need to know to finish optimally?"

| Problem | State | Why |
|---|---|---|
| House robber | `i` | Only the index matters; "did I rob i−1?" is encoded by jumping to `i−2`. |
| Ninja's training | `(day, lastTask)` | Today's choice depends on yesterday's task. |
| Grid paths | `(r, c)` | Position fully determines the future. |
| 0/1 knapsack | `(i, capacityLeft)` | Item index plus remaining capacity. |
| Stocks III/IV | `(i, holding, txLeft)` | Day, whether you hold a share, and the transactions left. |
| LCS / edit distance | `(i, j)` | A prefix (or suffix) of each string. |
| MCM / burst balloons | `(i, j)` | A contiguous interval. |
| Cherry pickup II | `(row, c1, c2)` | Both robots move down together, so one row index suffices. |

**Sanity checks:**
- Count the states: #states × work per state = time. If that's too big, the state is too rich. Look for a dimension that is implied by the others (cherry pickup: both robots share the row).
- Don't put the **answer so far** in the state (`f(i, sumSoFar)` for a max problem). Return it instead: `f(i)` = best achievable from `i` onward. "Sum so far" belongs in the state only when it is a **constraint** (subset-sum target, knapsack capacity).

---

## 4. Writing the recurrence

Three moves, used in every Striver problem:

1. **Express the problem in terms of indices**: `f(i)`, `f(i, j)`, `f(i, j, flag)`.
2. **Do all the choices on that index**: pick/not-pick, move down/right, buy/sell/skip, match/insert/delete, split at `k`.
3. **Combine the choices:**

   | Asked for | Combine with |
   |---|---|
   | Count the ways | `sum` |
   | Best | `min` / `max` |
   | Feasibility | `or` |

Two ways to frame the choice:

| Framing | Form | Used by |
|---|---|---|
| **Last choice** (prefix DP) | `f(i)` = answer for the prefix ending at `i` | LIS, stairs, knapsack, LCS (Striver writes `f(n−1, …)` going down to 0) |
| **First choice** (suffix DP) | `f(i)` = answer for the suffix starting at `i` | Stocks, front partitioning, word break, palindrome partitioning II |
| **Split point** (interval DP) | `f(i, j) = best over k of cost + f(i, k) + f(k+1, j)` | MCM, cut stick, burst balloons (choose the **last** balloon), boolean parenthesisation |

**Pick / not-pick template** (subsequences, knapsack):
```python
def f(i, cap):
    if i == 0: return val[0] if wt[0] <= cap else 0
    skip = f(i - 1, cap)
    take = val[i] + f(i - 1, cap - wt[i]) if wt[i] <= cap else -inf
    return max(skip, take)
```
For **unbounded** items (coin change, rod cutting, unbounded knapsack), `take` stays at the same index: `f(i, cap − wt[i])`.

---

## 5. Base cases and sentinels

- **Base cases come from the smallest valid state.**
  - Index 0: decide directly. In subset sum, `f(0, t) = (arr[0] == t)`.
  - Empty string: LCS with an empty string is 0. Edit distance of `i` chars vs empty is `i`.
- **Out-of-bounds sentinels:** return `+∞` for a min problem or `−∞` for a max problem when a move leaves the grid. Never return 0, which looks like a free path. Use `1e9` rather than `INT_MAX` so that `+ cost` cannot overflow.
- **Shift indices by one** for string DP: `dp[i][j]` describes the prefixes of lengths `i` and `j`. Row 0 and column 0 are then the empty-string base cases, and `s[i−1]` is the current char. This removes every `if i < 0` check.
- **Zeros in subset counting:** if `arr[0] == 0` there are 2 ways to reach target 0 (take it or not). Handle this in the base case, or every count with zeros is off by a factor of 2.

---

## 6. Loop order in tabulation

> **Every cell must be computed before anything that reads it.**

Draw the dependency arrows, then choose loops that respect them:

| Recurrence reads | Loop order |
|---|---|
| `dp[i−1]`, `dp[i−2]` | `i` ascending |
| `dp[i+1][…]` (suffix DP: stocks, word break) | `i` descending |
| `dp[i−1][j]`, `dp[i][j−1]` (grid, LCS) | `i` ascending, `j` ascending |
| `dp[i−1][j−wt]` (0/1 knapsack, 1D) | `j` **descending**, so the old row is still in place |
| `dp[i][j−wt]` (unbounded, 1D) | `j` **ascending**, so the item can be reused |
| `dp[i][k]` and `dp[k+1][j]` (interval) | `i` descending, `j` ascending, or by length `len = 2..n` |
| `dp[i+1][j−1]` (palindromes) | `i` descending, `j` ascending |

**The 1D knapsack direction** comes up all the time. In 0/1 knapsack, a descending `j` reads cells from the previous item. In unbounded knapsack, an ascending `j` reads cells already updated for the current item, which is exactly "take it again".

**Combinations vs permutations (coin change II vs combination sum IV):**
- Coins in the outer loop, amount in the inner loop: each multiset is counted once (**combinations**).
- Amount outer, coins inner: each ordering is counted (**permutations**).

---

## 7. Space optimisation

| Pattern | Keep | Example |
|---|---|---|
| Reads `i−1`, `i−2` | two scalars | stairs, house robber |
| Reads only the previous row | `prev[]`, `cur[]` | grid paths, LCS, edit distance, knapsack |
| Reads the previous row at `j` and `j−w` only | one array, `j` descending | 0/1 knapsack, subset sum |
| Reads only the next day | `ahead[2][k+1]` → `cur` | stocks |
| Interval `dp[i][j]` | usually can't be reduced | MCM, burst balloons |

**Caveats:**
- **Reconstruction needs the full table.** Printing the LCS, LIS or SCS walks back through `dp`, so keep it 2D (or store parent pointers).
- With `prev`/`cur` swapping, reset `cur`'s base cell each row (for example `cur[0] = …`). Otherwise the previous row leaks in.

---

## 8. The DP families

| # | Family | State | Recurrence core | Problems in this part |
|---|---|---|---|---|
| 1 | **1D** | `i` | `f(i) = g(f(i−1), f(i−2), …)` | stairs, frog jump (k), house robber I/II |
| 2 | **2D / multi-choice** | `(i, last)` | `max over choice ≠ last` | ninja's training |
| 3 | **Grids** | `(r, c)` | from up/left (or 3 cells above) | unique paths I/II, min path sum, triangle, falling path, cherry pickup II, count squares |
| 4 | **Subsequences / knapsack** | `(i, target)` | pick / not pick (unbounded: stay at `i`) | subset sum, partitions, count subsets, 0/1 knapsack, coins, target sum, coin change II, rod cutting |
| 5 | **Stocks** | `(i, holding, [txLeft])` | buy / sell / skip | stocks I–IV, fee, cooldown |
| 6 | **LIS** | `i` (+ `prev`) | `dp[i] = 1 + max dp[j]` over `j < i`, `a[j] < a[i]` | LIS (n² + binary search), print LIS, divisible subset, string chain, bitonic, number of LIS |
| 7 | **Two strings** | `(i, j)` | match → diagonal; else combine neighbours | LCS, substring, LPS, insertions, SCS, distinct subsequences, edit distance, wildcard |
| 8 | **Partition (MCM)** | `(i, j)` or front `i` | split over `k` | MCM, cut stick, burst balloons, boolean evaluation, palindrome partitioning II, partition array |

**Family signals:**
- **"Choose a subset with a sum/weight constraint"** → family 4.
- **"Two strings, transform/compare"** → family 7. Many reduce to LCS:
  - LPS = LCS(s, reverse s).
  - Min insertions for a palindrome = n − LPS.
  - Delete/insert A→B = (n − LCS) + (m − LCS).
  - SCS length = n + m − LCS.
- **"Order of operations on a range matters"** → family 8.
- **"State changes over time with constraints"** (holding, cooldown, k transactions) → family 5, a small state machine indexed by day.

---

## 9. Reconstructing the answer

The DP table stores values, not choices. To output the actual object:

1. Keep the full table, or store `parent[state] = choice`.
2. Start from the answer cell and repeat the decision the recurrence made: whichever option produced `dp[state]`.

| Problem | Walk-back rule |
|---|---|
| LCS string | If `s[i−1] == t[j−1]`, take the char and go diagonal. Else move toward the larger of `dp[i−1][j]` and `dp[i][j−1]`. |
| SCS | Like LCS, but also emit the char of the side you step away from; flush the leftovers at the end. |
| LIS | Store `parent[i] = j` for the best `j`; follow it from the argmax. |
| Knapsack items | If `dp[i][c] != dp[i−1][c]`, item `i` was taken: `c −= wt[i]`. |
| MCM brackets | Store `split[i][j]`; print recursively. |

---

## 10. Complexity accounting

**Time = (#states) × (work per state).** **Space = #states**, or the reduced row count.

| Problem | States | Work | Time |
|---|---|---|---|
| House robber | n | O(1) | O(n) |
| Frog jump with k | n | O(k) | O(n·k) |
| Knapsack | n·W | O(1) | O(n·W), **pseudo-polynomial** |
| LIS (DP) | n | O(n) | O(n²); O(n log n) with patience sorting |
| LCS / edit distance | n·m | O(1) | O(n·m) |
| Stocks IV | n·2·k | O(1) | O(n·k) |
| MCM / burst balloons | n² | O(n) | O(n³) |
| Palindrome partitioning II | n | O(n) with an `isPal` table | O(n²) |

**Pseudo-polynomial:** O(n·W) is polynomial in the *value* W but exponential in its bit length. When `W ≈ 10⁹`, knapsack DP is infeasible. Then swap the dimensions (`dp[value] = min weight`) or use a different approach.

**Memo vs tabulation overhead:**
- Memoization visits only the reachable states. That can beat tabulation when most states are unreachable.
- Memoization pays for function calls and recursion depth. For n ≈ 10⁵, tabulate.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Returning 0 for an out-of-grid move in a min problem | Return a large sentinel (`1e9`). |
| Memo "unset" value collides with a real answer (−1 can be valid) | Use `None` or a separate `seen` array. |
| 1D 0/1 knapsack with `j` ascending | That's unbounded knapsack. Iterate `j` descending. |
| Swapping coin/amount loops in coin change II | Coins outer gives combinations; amount outer gives permutations. |
| Base case for `arr[0] == 0` in count subsets | 2 ways for target 0. |
| Putting "best so far" into the state | Return the best from the subproblem instead. |
| Tabulating in the same direction as the recursion | Reverse it: the recursion shrinks toward the base cases, so the loops grow away from them. |
| Overflow when adding cost to `INT_MAX` | Use `1e9` sentinels or 64-bit. |
| Interval DP with `i` ascending | `dp[k+1][j]` isn't ready yet. Use `i` descending or loop by length. |
| Burst balloons choosing the first balloon | Choose the last one, so its neighbours are fixed. |

---

## Practice

<details><summary>1. Climbing stairs with steps {1, 3, 5}. Write the recurrence and the base case.</summary>

`f(n) = f(n−1) + f(n−3) + f(n−5)`, with `f(0) = 1` and `f(<0) = 0`. Time O(n), space O(1) with five rolling values (or O(n) simply).
</details>

<details><summary>2. Grid with obstacles: "min cost from (0,0) to (n−1,m−1), moves right/down". What is the state, the recurrence and the out-of-bounds value?</summary>

State `(r, c)`. `f(r, c) = cost[r][c] + min(f(r−1, c), f(r, c−1))`. An obstacle or out-of-bounds cell returns `1e9`. Base: `f(0, 0) = cost[0][0]`.
</details>

<details><summary>3. You converted 0/1 knapsack to 1D and the answers are too large. What's wrong?</summary>

The capacity loop runs ascending, so each item can be taken several times. Make it descending.
</details>

<details><summary>4. Coins [1, 2], amount 3. How many combinations, and how many ordered sequences?</summary>

Combinations: {1,1,1} and {1,2}, so 2 (coins outer). Ordered sequences: 111, 12, 21, so 3 (amount outer).
</details>

<details><summary>5. Which family is "minimum deletions to make s a palindrome", and what is the formula?</summary>

Two-string DP via LCS: `n − LPS(s)`, where `LPS(s) = LCS(s, reverse(s))`.
</details>

<details><summary>6. Stocks with at most 2 transactions. Give the state and its size.</summary>

`(day, holding ∈ {0,1}, txLeft ∈ {0,1,2})`, so n·2·3 states, O(n) time and O(1) space with a rolling `ahead` table. Equivalently, there are 4 states: buy1, sell1, buy2, sell2.
</details>

<details><summary>7. Is O(n·W) knapsack polynomial? When does it fail?</summary>

It is pseudo-polynomial: it fails when W ≈ 10⁹ even for small n. Then index by value (`dp[v] = min weight`) if the values are small, or use meet-in-the-middle for n ≈ 40.
</details>

<details><summary>8. In which order do you fill dp for "longest palindromic substring" with isPal[i][j] = s[i]==s[j] && isPal[i+1][j−1]?</summary>

`i` descending, `j` ascending from `i`, or by length. The cell reads row `i+1`, so that row must already be filled.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| State | The parameters that uniquely identify a subproblem. |
| Transition / recurrence | How a state's answer is built from smaller states. |
| Memoization | Top-down recursion with a cache. |
| Tabulation | Bottom-up iteration over a table in dependency order. |
| Space optimisation | Keeping only the rows or cells that later states read. |
| Optimal substructure | Optimal solutions contain optimal sub-solutions. |
| Overlapping subproblems | The same state is reached by several paths. |
| Pick / not-pick | A binary choice per element (subsequence DP). |
| Unbounded | An item can be reused; the transition stays at the same index. |
| Interval DP | State `(i, j)` over a contiguous range; transition by split point. |
| Front partition | `f(i)` over suffixes; choose where the first block ends. |
| Pseudo-polynomial | Polynomial in a numeric value, not in input size. |

---

## Flashcards

**Two conditions for DP?** #flashcard
Optimal substructure and overlapping subproblems.

**Striver's three steps for the recurrence?** #flashcard
Express in indices → do all choices on that index → sum / min / max / or over them.

**Memo → tabulation rule?** #flashcard
Base cases become initial cells; loops run opposite to the recursion's direction; the body is copied.

**When can you drop to two rows?** #flashcard
When row i reads only row i−1 (or i+1).

**1D 0/1 knapsack capacity loop direction?** #flashcard
Descending. Ascending gives unbounded knapsack.

**Coin change II: which loop is outer?** #flashcard
Coins outer gives combinations; amount outer gives permutations.

**Out-of-bounds value in a min-path DP?** #flashcard
A large sentinel like 1e9, not 0 or INT_MAX.

**Time of a DP?** #flashcard
#states × work per state.

**Why is O(n·W) knapsack "pseudo-polynomial"?** #flashcard
It's polynomial in the value W, but exponential in W's bit length.

**LPS via LCS?** #flashcard
LPS(s) = LCS(s, reverse(s)).

**SCS length?** #flashcard
n + m − LCS.

**Interval DP fill order?** #flashcard
i descending, j ascending, or by increasing length.

**Burst balloons: first or last?** #flashcard
Last. Its neighbours are then the fixed interval boundaries.

**How do you reconstruct a DP answer?** #flashcard
Keep the table (or parent pointers) and re-trace whichever choice produced each cell.

**Interview track →** [Recursion to DP](../../02-algorithms/10-recursion-to-dp.md) · [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
