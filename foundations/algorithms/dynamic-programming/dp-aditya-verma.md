# Dynamic Programming — Aditya Verma Style (Supplement)

Notes on the **choice diagram** and **0/1 knapsack** way of building DP. For the main SDE-3 DP guide see [README.md](README.md) and [patterns/dp-advanced.md](../../../patterns/dp-advanced.md).

---

## What is DP here?

- **DP = recursion + storage** — Same subproblems computed many times → cache results.
- **When:** Choices at each step (take / not take, split, match) **and** optimal substructure (max/min/count).
- **Steps:** Write correct **recursive** solution → add **memo** (top-down) or **table** (bottom-up) → **space optimize** when only previous row/column needed.

---

## Parent patterns (overview)

These are the **families** Aditya Verma-style notes organize around: each has a recognizable **choice** or **transition**, a **state**, and a **recurrence**. In an interview, name the pattern first, then write states.

| Pattern | One-line idea |
|---------|----------------|
| **0/1 Knapsack** | Each item at most once — two branches (take / skip). |
| **Unbounded Knapsack** | Unlimited copies — inner loop order differs from 0/1. |
| **Fibonacci / linear** | `dp[i]` from a **fixed window** of earlier indices. |
| **LCS / LIS** | Two sequences aligned, or one sequence + patience / patience-like DP. |
| **Kadane** | Best subarray **ending** at `i` (global max over `i`). |
| **MCM / interval** | Split interval `[i,j]` at `k`; combine left + right + cost at `k`. |
| **DP on trees** | Subtree answer from children (post-order). |
| **DP on graphs** | Often DAG: topo order + relax; or state = `(node, extra)`. |

---

### 0/1 Knapsack

- **Idea:** At each item you make a **binary choice**: use this item once or not. Past decisions change **remaining capacity** (or remaining sum budget). This is the classic **choice diagram** — two branches, then max/min/sum/count over them.
- **How to solve:** Define `dp[i][w]` = optimal answer using **only the first `i` items** with knapsack capacity `w` (or: first `i` items summing to at most `w`, depending on formulation). Recurrence: `max(skip, take)` with index `i-1` when you take (so each item is used at most once). Bottom-up fills the table; **1D optimization:** single array `dp[w]`, loop `w` from **high to low** when processing each item.
- **Why it works:** Optimal substructure — best use of first `i` items for capacity `w` builds from best of first `i-1` items with strictly smaller subproblems. Overlapping subproblems — same `(i,w)` recomputed in naive recursion.
- **Question variations (interview):**
  - **Subset sum / partition equal subset sum** — boolean or max value to hit exact `T`.
  - **Target sum with ±** — count ways; often rephrase as subset-sum on transformed total.
  - **Count subsets with given sum** — add ways instead of max.
  - **Bounded knapsack** (fixed counts per item) — binary split into 0/1 items, or specialized deque per residue class.
  - **Follow-ups:** space-only `O(W)`, reconstruct which items picked, bitset speedup for subset sum.

---

### Unbounded Knapsack

- **Idea:** Each **type** of item can be taken **any number of times** (still subject to capacity). The “choice” is often: **how many of this type** in one shot, or equivalently: after taking one copy, you may **stay on the same item index** (unlike 0/1 where you always move to `i-1` after taking).
- **How to solve:** `dp[w] = max over items of (value + dp[w - weight])` or nested loops **for each item, for w from weight to W forward**. Forward `w` in 1D means the same item can contribute again in the same iteration — that is exactly “unbounded.” **Coin change (min coins)** and **rod cutting** are the same skeleton with min instead of max.
- **Why it differs from 0/1:** In 1D DP, **backward** `w` for item `i` = each weight state updated from a row that **did not** include `i` yet (0/1). **Forward** `w` = state can include **multiple** uses of `i` in one pass.
- **Question variations:**
  - **Coin change I / II** — min coins vs **number of combinations** (loop order: coins outer vs amount outer).
  - **Rod cutting, unbounded max profit.**
  - **Integer break** (multiply) — multiplicative variant; greedy proof exists but DP is safe.
  - **Follow-up:** count ways modulo prime; print one optimal multiset.

---

### Fibonacci / linear

- **Idea:** `dp[i]` depends only on **O(1)** or **O(k)** previous values — climbing stairs, house robber (linear), decode ways. This is **not** knapsack; the state is usually **position** along one sequence or time.
- **How to solve:** Write `dp[i] = f(dp[i-1], dp[i-2], …)` from the problem statement; reduce to **two variables** if only last two (or last `k`) entries matter. Matrix exponentiation for **very large `n`** with linear recurrence (rare in interviews but good to mention).
- **Question variations:**
  - **Climbing stairs, tribonacci, min cost climbing stairs.**
  - **House robber I** — `dp[i] = max(dp[i-1], nums[i] + dp[i-2])`.
  - **Decode ways** — branching on one or two digits; handle leading zero.
  - **Paint house / fence** — last few colors constrained.
  - **Follow-up:** **House robber II** (circle) — run twice (exclude first or last house).

---

### LCS / LIS

- **Idea — LCS:** Two strings; at each `(i,j)` you **match** `s1[i]` with `s2[j]` or **skip** one side — three-way recurrence. **Idea — LIS:** One array; either **O(n²)** `dp[i]` = LIS ending at `i`, or **O(n log n)** **patience sorting** (binary search on tails).
- **How to solve:** **LCS:** `dp[i][j]` longest common subsequence of prefixes. **LIS:** for each `i`, scan `j<i` with `nums[j]<nums[i]` and take `1+dp[j]`, or maintain `tails[]` where `tails[k]` = smallest ending value of an increasing subsequence of length `k+1`.
- **Question variations:**
  - **LCS, LCS print, shortest common supersequence** (length = `m+n-LCS`).
  - **Edit distance** — similar grid; insert/delete/replace costs.
  - **Longest palindromic subsequence** = LCS(s, reverse(s)).
  - **LIS:** count LIS, longest chain of pairs, Russian dolls envelopes (sort + LIS).
  - **Follow-up:** **DLIS** (decreasing), **non-decreasing** vs **strict** (binary search `lower_bound` vs `upper_bound`).

---

### Kadane

- **Idea:** Global maximum subarray equals the max over **all ending positions** of “best sum of a subarray that **ends** at `i`.” That local quantity satisfies a **simple recurrence** — no interval split table.
- **How to solve:** `ending_here = max(nums[i], nums[i] + ending_here_prev)`; `global = max(global, ending_here)`. One pass **O(n)**, **O(1)** space. Same spirit: **max product subarray** (track min and max because of negatives).
- **Question variations:**
  - **Standard max sum subarray; circular array** (total − min subarray or two cases).
  - **Shortest subarray with sum ≥ K** (prefix + deque — not pure Kadane).
  - **Follow-up:** return **indices** of max subarray; 2D Kadane for max rectangle in matrix (compress columns).

---

### MCM / Interval DP

- **Idea:** Optimal solution on `[i,j]` is often **split** at `k` (`i ≤ k < j`): solve `[i,k]` and `[k+1,j]` independently, pay a **merge/cost** at `k`. Matrix chain multiplication is the textbook example; **burst balloons** and **palindrome partitioning II** use the same **interval** state.
- **How to solve:** `dp[i][j] = min/max over k of dp[i][k] + dp[k+1][j] + cost(i,j,k)`. Fill by **increasing length** `len = 2..n`. **O(n³)** for many problems unless structure reduces `k` range.
- **Question variations:**
  - **Matrix chain multiplication** — cost = product of dimensions at split.
  - **Burst balloons** — add imaginary 1 at ends; value at `k` when last to burst in `(i,j)`.
  - **Palindrome partitioning II** — min cuts; **optimal BST** (search cost) — similar split flavor.
  - **Scramble string** — recursive structure with pruning.
  - **Follow-up:** **optimal triangulation** of polygon (same interval DP shape).

---

### DP on trees

- **Idea:** Each subtree has a well-defined answer **from its children**; combine at the root. Often **two states per node**: rob/skip (house robber III), white/black (tree coloring), min vertex cover.
- **How to solve:** DFS post-order; `return` a struct or pair `(take, skip)` or `(with_root, without_root)`. For **counting** or **paths through root**, keep a global max or return both best **downward chain** and best **path in subtree**.
- **Question variations:**
  - **House robber III, max path sum binary tree, diameter, largest BST subtree.**
  - **Binary tree cameras** — states per node (has camera / covered / not).
  - **Follow-up:** **N-ary tree**, **weighted** edges, **rerooting** DP (advanced — rare in phone screen).

---

### DP on graphs

- **Idea:** State = **(node, …)** where `…` might be bitmask (small graph), remaining moves, or collected items. On a **DAG**, process nodes in **topological order** and relax edges like shortest path. **Cycles** need more state (e.g. number of edges used) or Bellman-Ford / Floyd-Warshall style.
- **How to solve:** **Topo order + DP:** `dp[v] = aggregate of dp[u] + edge(u,v)` over incoming edges. **Shortest/longest path in DAG** is linear in `V+E` with topo sort. **Bitmask DP on graph:** Hamiltonian path, TSP-like, `n ≤ ~20`.
- **Question variations:**
  - **Longest path in DAG** (project scheduling, critical path).
  - **Cheapest flights within K stops** — state `(city, edges_used)` or Bellman-Ford `K` rounds.
  - **Travelling salesman** (bitmask), **collect all keys** (state = position + key mask).
  - **Follow-up:** **0-1 BFS** / **Dijkstra** when weights non-negative — not always labeled “DP” but same “relax in order” idea.

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

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **0/1 Knapsack** | `dp[i][w] = max(skip, take if weight fits)`; 1D: iterate `w` **downward** so each item used once. | **Backward** inner loop is the 0/1 invariant; **forward** would allow reuse (unbounded bug). |
| **Subset Sum** | Boolean `dp[sum]` = achievable using subset; update `sum` descending for 0/1. | **Space** one bitset possible; **empty** sum always true. |
| **Partition Equal Subset Sum** | If `sum` odd → false; else subset sum to `sum/2`. | **Bitset** `bits \| (bits<<x)` optimization; **overflow** if sum huge—use boolean array. |
| **Target Sum (±)** | Transform to: find subset with sum `(total+target)/2` if parity works; **count** ways. | **Impossible** if `(total+target)` odd or target unreachable; map to **count subset sums**. |
| **Coin Change (unbounded, min coins)** | `dp[amt] = 1 + min(dp[amt-c])`; inner loop **forward** over `amt` for each coin **or** coins outer loop. | **vs 0/1:** forward pass; **order** for counting **combinations** vs permutations. |
| **Coin Change 2 (unbounded, count)** | Nested loops: **for coin in coins: for amt** to count **combinations** without order overcount. | **Permutation** count reverses loop order (amount outer). |
| **Rod Cutting** | Same as unbounded knapsack—maximize value with length “weights”. | **Cut** at each position—interval variant is different (MCM). |
| **Bounded Knapsack** | Multiple copies with **limits**—binary split items into 0/1 items or deque optimization per remainder class. | **Naive** copy each item `count` times may be too many—**binary** decomposition O(log count) each. |

---

## See also

- [README.md](README.md) — SDE-3 DP overview and interview flow  
- [patterns/dp-advanced.md](../../../patterns/dp-advanced.md) — 16 patterns  
- [greedy.md](../greedy.md) — when greedy replaces DP (fractional knapsack)
