---
module: striver-a2z/32-beyond-the-sheet
lesson: 2
topic: Advanced DP — bitmask DP (TSP, assignment), digit DP, tree DP and rerooting, DP on intervals recap, probability/expected value DP, state-compression and optimisation tricks
source: beyond the A2Z sheet (enrichment)
tags: [striver, beyond-sheet, theory, dp, bitmask-dp, digit-dp, tree-dp, rerooting]
---
# 2. Advanced DP

← [Range queries](01-range-queries-theory.md) · [Part 32 index](README.md) · Next → [Advanced trees and graphs](03-advanced-trees-and-graphs-theory.md)

> [!abstract] What this covers
> **Core idea:** Every advanced DP keeps the same recipe as [Part 28](../28-dynamic-programming/README.md): state, transition, base case, order. What changes is the **state encoding**. A subset becomes a bitmask, a number becomes its digit position plus a tight flag, and a tree gives each node a subtree value (then, for rerooting, a value from outside the subtree).
> **You'll be able to:** spot bitmask DP from n ≤ 20; write the digit-DP template with `tight`/`started`; solve "answer for every root" with two DFS passes; and apply the standard optimisations (rolling arrays, prefix sums over transitions, monotonic deque).
> **Source:** not in the A2Z sheet. These are the most common "hard DP" families in Google/LeetCode hard rounds. · **Time:** 75 min

**Sections:** [1. Recognising the family](#1-recognising-the-family) · [2. Bitmask DP](#2-bitmask-dp) · [3. Digit DP](#3-digit-dp) · [4. Tree DP](#4-tree-dp) · [5. Rerooting](#5-rerooting) · [6. Expected value DP](#6-expected-value-dp) · [7. Optimisation tricks](#7-optimisation-tricks)

---

## 1. Recognising the family

| Signal | Family | State |
|---|---|---|
| n ≤ 15–20, "visit all", "assign each" | Bitmask | `dp[mask][last]` or `dp[mask]` |
| "Count numbers in [L, R] with digit property" with R up to 10¹⁸ | Digit | `dp[pos][tight][started][extra]` |
| Tree, "max/min/count over subtrees" | Tree DP | `dp[v][state]` after DFS |
| "For every node as root" | Rerooting | `down[v]` plus `up[v]` |
| Merge/burst/cut intervals | Interval (Part 28 MCM) | `dp[i][j]` by length |
| Probability, dice, random walk | Expected value | `E[state]` going backwards |
| Big k transitions, linear recurrence | Matrix exponentiation | Vector × matrix^k ([maths](../31-maths/05-modular-arithmetic-and-combinatorics-theory.md)) |

---

## 2. Bitmask DP

Bit i of `mask` is set when item i is used or visited. There are 2ⁿ states.

**Travelling salesman / shortest Hamiltonian path,** O(2ⁿ·n²):

```text
dp[1<<s][s] = 0
for mask in increasing order:
  for last in mask with dp[mask][last] finite:
    for nxt not in mask:
      dp[mask | 1<<nxt][nxt] = min(…, dp[mask][last] + w[last][nxt])
answer = min over last of dp[full][last] (+ w[last][s] for a cycle)
```

| Problem | State | Notes |
|---|---|---|
| Assignment (n workers × n jobs) | `dp[mask]`, where worker = popcount(mask) | O(2ⁿ·n) |
| Shortest path visiting all nodes (LC 847) | BFS over (node, mask) | Unweighted, so use BFS rather than DP |
| Partition into k equal subsets | `dp[mask]` = current bucket fill | O(2ⁿ·n) |
| Minimum incompatibility / groups | Enumerate submasks: `for (s = m; s; s = (s−1) & m)` | Over all masks the total is O(3ⁿ) |
| Smallest sufficient team | `dp[skillMask]` = min people | The mask is over skills |

**Bit idioms** (Part 20):
- `mask & (1 << i)` tests bit i.
- `mask | (1 << i)` sets bit i.
- `__builtin_popcount(mask)` (Java `Integer.bitCount`) counts set bits.

---

## 3. Digit DP

The usual form is: count `x ∈ [0, N]` with property P. Then `ans(L, R) = f(R) − f(L − 1)`.

```text
digits = decimal digits of N
solve(pos, tight, started, s):          // s = extra state (sum mod k, last digit, mask of used digits…)
  if pos == len: return valid(s, started)
  memo on (pos, tight, started, s)       // memoise only when not tight, or include tight in the key
  lim = tight ? digits[pos] : 9
  for d in 0..lim:
    res += solve(pos+1, tight && d == lim, started || d != 0, update(s, d, started))
```

| Problem | Extra state |
|---|---|
| Count numbers with digit sum = k | running sum |
| Numbers with no repeated digit (LC 1012) | 10-bit mask of used digits |
| Count of digit d in 1..N (LC 233) | running count |
| Numbers whose adjacent digits differ by ≥ 2 | last digit |
| Divisible by k | value mod k |

- `started` handles leading zeros, which should not count as used digits.
- The number of states is `len × 2 × 2 × |s|`, which is tiny.

---

## 4. Tree DP

Compute children first (post-order DFS). Then combine.

| Problem | State | Transition |
|---|---|---|
| Diameter | `h[v]` = deepest downward path | `best = max(best, h[c1] + h[c2] + 2)` |
| Max path sum (Part 24) | `gain[v]` = best downward path from v | `max(0, gain[c])` for each child |
| House Robber III | `(take, skip)` | `take = v + Σ skip(c)`, `skip = Σ max(take(c), skip(c))` |
| Min vertex cover | `(in, out)` | `out = Σ in(c)`, `in = 1 + Σ min(in, out)` |
| Binary tree cameras | 3 states: covered, has camera, needs cover | Greedy-like DP |
| Count subtrees / sizes | `sz[v] = 1 + Σ sz[c]` | Used everywhere |
| Tree knapsack (choose k nodes, connected) | `dp[v][k]` | Merging children is O(n²) total with size bounds |

---

## 5. Rerooting

Use this to compute an answer for **every** root in O(n), instead of O(n²).

1. **Down pass:** with root 0, compute `down[v]` from the children (for example the sum of distances within the subtree, and `sz[v]`).
2. **Up pass:** from the parent p to the child c, derive `ans[c]` from `ans[p]` by removing c's contribution and adding the "rest of the tree".

**Sum of distances in tree (LC 834):**
```text
ans[0] = Σ depth (from DFS1)
ans[c] = ans[p] − sz[c] + (n − sz[c])     // the sz[c] nodes get 1 closer, the other n − sz[c] get 1 farther
```

- **Max-type rerooting** (for example the max distance from each node): keep the **top two** child values, so that excluding one child is O(1).

---

## 6. Expected value DP

- **Linearity of expectation:** `E[X + Y] = E[X] + E[Y]`, even when X and Y are dependent.
- **Backward recurrence:** `E[s] = cost + Σ P(s → t)·E[t]`.
  - Knight probability (LC 688): `dp[k][r][c]` holds the probability of still being on the board.
  - New 21 Game (LC 837): this needs a sliding window sum over the last W values to get O(n).
- **Geometric distribution:** with success probability p per trial, the expected number of trials is 1/p.

---

## 7. Optimisation tricks

| Trick | When | Gain |
|---|---|---|
| Rolling array | `dp[i]` depends only on `dp[i−1]` | O(nm) → O(m) space |
| Prefix sums over transitions | `dp[i] = Σ dp[j]` for j in a range | O(n·k) → O(n) |
| Monotonic deque | `dp[i] = max over the window j of dp[j] + c` | O(nk) → O(n) (Constrained Subsequence Sum, LC 1425) |
| Binary search over states | LIS in O(n log n), weighted job scheduling | Transitions in O(log n) |
| Divide and conquer / Knuth / convex hull trick | Cost has a monotonicity or quadrangle property | Competitive-programming level; mention it only at senior level |
| State reduction | Drop a dimension that is derivable (for example, the index from a popcount) | Fewer states |

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Bitmask DP with n = 30 | 2³⁰ × 30 is far too many; think meet in the middle (lesson 4) |
| Memoising digit DP while `tight` is true and not in the key | Put `tight` in the key, or memo only the non-tight states |
| Leading zeros counted as digits | Add a `started` flag |
| Rerooting by running n DFSs | Two passes |
| Tree DP recursion depth 10⁵ (Python) | Iterative post-order or `sys.setrecursionlimit` + threading |

---

## Practice

<details><summary>1. n = 16 cities, find the shortest tour. Complexity?</summary>

O(2¹⁶·16²) ≈ 1.7·10⁷, which is fine.
</details>

<details><summary>2. Count numbers in [1, 10¹⁸] whose digit sum is divisible by 7.</summary>

Digit DP with the state (pos, tight, sum mod 7). Compute f(10¹⁸) − f(0).
</details>

<details><summary>3. House Robber III on root 3 → (2 → 3), (3 → 1). Answer?</summary>

7: take the root (3) and the two grandchildren (3 + 1).
</details>

<details><summary>4. Why does sum of distances reroot with `− sz[c] + (n − sz[c])`?</summary>

Moving the root from p to c brings the sz[c] nodes in c's subtree one step closer and takes the other n − sz[c] nodes one step farther away.
</details>

---

## Key terms

| Term | Meaning |
|---|---|
| Submask enumeration | `s = (s − 1) & m` visits every subset of m |
| Tight | The prefix so far equals N's prefix, so the next digit is bounded |
| Rerooting | Computing every node's answer as if it were the root, reusing the parent's answer |
| Linearity of expectation | E of a sum = sum of the Es |

---

## Flashcards

**Bitmask DP trigger?** #flashcard
n ≤ 20, and the state needs "which items are used".

**Digit DP state?** #flashcard
(pos, tight, started, extra). Answer with f(R) − f(L−1).

**Submask enumeration cost over all masks?** #flashcard
O(3ⁿ).

**Rerooting in two sentences?** #flashcard
DFS1 computes subtree values. DFS2 pushes the parent's full answer down, adjusting for the child's subtree.

**House Robber III state?** #flashcard
(take, skip) per node.

---

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
