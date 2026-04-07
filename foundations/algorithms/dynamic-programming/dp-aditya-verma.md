# Dynamic Programming — Aditya Verma Style (Supplement)

Notes on the **choice diagram** and **0/1 knapsack** way of building DP. For the main SDE-3 DP guide see [README.md](README.md) and [patterns/dp-advanced.md](../../../patterns/dp-advanced.md).

---

## What is DP here?

- **DP = recursion + storage** — Same subproblems computed many times → cache results.
- **When:** Choices at each step (take / not take, split, match) **and** optimal substructure (max/min/count).
- **Steps:** Write correct **recursive** solution → add **memo** (top-down) or **table** (bottom-up) → **space optimize** when only previous row/column needed.

---

## Parent patterns (overview)

| Pattern | Idea |
|---------|------|
| 0/1 Knapsack | Each item at most once — two branches per item. |
| Unbounded Knapsack | Unlimited copies of each item. |
| Fibonacci / linear | `dp[i]` from previous indices. |
| LCS / LIS | Two sequences or patience sorting. |
| Kadane | Max subarray ending at `i`. |
| MCM / Interval | Split `[i,j]` at `k`. |
| DP on trees | Post-order; combine children. |
| DP on graphs | Often topo order + relax. |

---

## 0/1 Knapsack — classic formulation

**Problem:** `n` items with `weight[i]` and `value[i]`, capacity `W`. Maximize sum of values without exceeding `W`.

**Choices per item:** Include item `i` (if weight fits) or skip.

**Recursive (conceptual):**

```text
knapsack(i, w) = max(
    knapsack(i-1, w),                                    # skip i
    value[i-1] + knapsack(i-1, w - weight[i-1])         # take i, if w >= weight[i-1]
)
```

Base: `i == 0` or `w == 0` → `0` (adjust indices to your 0/1-based convention).

**Memo dimensions:** `(i, w)` — at most `(n+1)*(W+1)` states.

**Bottom-up:** `dp[i][w]` = max value using first `i` items with capacity `w`. Space-optimize to **1D** `dp[w]` iterating **backwards** over `w` when copying from `i-1` row.

**Identification:** “Subset with given sum”, “partition equal subset”, “target sum” — often reduce to knapsack or subset-sum variant.

---

## Unbounded knapsack

Same items can be picked multiple times — inner loop can iterate **forward** over capacity when using 1D DP (unlike 0/1 backward loop).

---

## Original notes (fractional vs 0/1 vs unbounded)

- **Fractional knapsack** — Greedy by value/weight ratio (not DP).
- **0/1 knapsack** — Each item once; DP.
- **Unbounded** — Unlimited copies; DP with different inner loop order.

After reading the problem, check: **choice** (pick/skip) + **optimal** (max/min) → write recurrence → memo/table.

---

## Interview Questions — Logic & Trickiness (knapsack family)

| Question | Core logic | Trickiness |
|----------|------------|------------|
| **Subset Sum** | 0/1 pick to reach target | DP[i][sum] |
| **Partition Equal Subset Sum** | Target = sum/2; odd sum → false | Bitset optimization follow-up |
| **Target Sum** | Count ways with +/- signs | Offset array or two-DP |
| **Coin Change (unbounded)** | Min coins; inner loop forward on weight | vs 0/1 backward inner loop |
| **Rod Cutting** | Unbounded max value | Same as unbounded knapsack |

---

## See also

- [README.md](README.md) — SDE-3 DP overview and interview flow  
- [patterns/dp-advanced.md](../../../patterns/dp-advanced.md) — 16 patterns  
- [greedy.md](../greedy.md) — when greedy replaces DP (fractional knapsack)
