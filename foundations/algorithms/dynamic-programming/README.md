# Dynamic Programming — SDE-2+ Level

Optimization via overlapping subproblems and optimal substructure; store solutions (memo or table). SDE-3 expects recurrence derivation, space optimization, and pattern recognition (see [dp-advanced.md](../../patterns/dp-advanced.md)).

---

## 1. Concept Overview

SDE-2 reference implementations (Python): `../../../google-sde2/snippets/python/dp.py`.

**When to use**: Choices at each step; maximize/minimize/count; overlapping subproblems. If greedy doesn't apply and state space is manageable, try DP.

**Two approaches**: Top-down (recurse + memo; only needed states) vs bottom-up (table; often space-optimizable). State definition and recurrence are key.

---

## 2. Core Patterns (Summary)

- **1D**: Fibonacci, Climbing Stairs, House Robber, Decode Ways — dp[i] from dp[i-1], dp[i-2].
- **0/1 Knapsack**: Pick or skip; dp[i][w] = max( dp[i-1][w], val[i] + dp[i-1][w-wt[i]] ). Space → 1D backward loop.
- **Unbounded Knapsack**: Same item repeatable; dp[w] from dp[w-wt[i]].
- **[LIS](../../../google-sde2/PROBLEM_DETAILS.md#lis)**: dp[i] = 1 + max dp[j] for j < i and arr[j] < arr[i]; or O(N log N) with binary search + tails.
- **LCS**: 2D; match → 1+dp[i-1][j-1]; else max(dp[i-1][j], dp[i][j-1]).
- **Kadane**: dp[i] = max(arr[i], arr[i]+dp[i-1]); O(1) space.
- **Interval DP**: dp[i][j] from split k in [i,j]; Burst Balloons, MCM.
- **Tree DP**: Post-order; parent state from children (e.g., max path sum, House Robber III).
- **Bitmask DP**: state = mask (subset); TSP, partition; N ≤ ~20.
- **Digit DP**: state = (position, tight, ...); count numbers in [L,R] with property.

---

## 3. Interview Flow

1. **Define state**: What does dp[i] or dp[i][j] represent?
2. **Recurrence**: How does state depend on smaller states? Base cases?
3. **Order**: Bottom-up order so dependencies are computed first.
4. **Space**: If dp[i] only needs dp[i-1] (and maybe dp[i-2]), use 1D and overwrite or use few variables.

---

## 4. Common SDE-3 DP Problems

**Easy**: Climbing Stairs, House Robber, Maximum Subarray.  
**Medium**: Coin Change, LIS, LCS, Unique Paths, Longest Palindromic Substring.  
**Hard**: Edit Distance, Burst Balloons, TSP (bitmask), Tree DP (Max Path Sum), Digit DP.

See [dp-advanced.md](../../patterns/dp-advanced.md) for 16 patterns and examples.

---

## 5. Pattern Recognition (DP Patterns)

- **Linear 1D**: Fibonacci, House Robber — previous states only.
- **0/1 Knapsack**: Pick/skip; weight dimension.
- **[LIS](../../../google-sde2/PROBLEM_DETAILS.md#lis)**: End at i; binary search for O(N log N).
- **[LCS/Edit distance](../../../google-sde2/PROBLEM_DETAILS.md#lcs-edit-distance)**: Two sequences; 2D.
- **Interval**: Break at k; MCM, Burst Balloons.
- **Tree**: Post-order; return multiple values (e.g., with/without node).
- **Bitmask**: Subset as integer; TSP, partition.
- **Digit**: Position, tight, sum/count.

---

## 6. Trade-offs & Scaling (optional)

- **Trade-offs**: Top-down easier to write; bottom-up faster and easier to optimize space. Recursion depth vs table size.
- **Scalability**: State space must be feasible (e.g., bitmask 2^n for n≤20). For huge state, consider approximate or greedy.

---

## 7. Interview Strategy

- **Identify**: "Choices", "optimal", "count ways" → DP. Define state and recurrence first.
- **Common mistakes**: Wrong state (missing dimension); wrong order in bottom-up; forgetting base case; integer overflow in count problems.

---

## 8. Quick Revision

- **Recurrence**: State = f(smaller states). Base = known values.
- **Space**: 1D often → 2 variables (current, prev); 2D → 1D row if row i only needs row i-1.
- **Pattern tip**: "Max/min/count with choices" → state + recurrence; "interval" → split k; "subset" small n → bitmask.

---

## Interview Questions — Logic & Trickiness

| Question | Core logic | Trickiness & details |
|----------|------------|----------------------|
| **[House Robber](../../../google-sde2/PROBLEM_DETAILS.md#house-robber)** | `dp[i] = max(dp[i-1], nums[i]+dp[i-2])`; space to **two vars** `take/skip`. | **House Robber II:** rob `[0..n-2]` or `[1..n-1]`—can’t take both ends. **III** tree DP. |
| **Coin Change (min coins)** | `dp[amt] = 1 + min(dp[amt-c])` for coins `c`; unbounded forward loop. | **Impossible** → -1; **order** of loops matters for **combinations** vs permutations in counting variants. |
| **Coin Change 2 (ways)** | Unbounded **combinations:** outer loop **coins**, inner **amount** to avoid duplicate order. | **Permutation** count uses outer amount, inner coins—different problem. |
| **Target Sum** | Count subsets with `sum(P) - sum(N) = target` → subset sum with offset; or **2D DP** on index and sum. | **Sum bounds** shrink state space; **memo** `(i, curr_sum)`. |
| **[Longest Increasing Subsequence](../../../google-sde2/PROBLEM_DETAILS.md#longest-increasing-subsequence)** | **O(n²):** `dp[i]` = best ending at `i`. **O(n log n):** patience sorting with **binary search** on tails. | **Strictly** vs **non-decreasing** changes `lower_bound` vs `upper_bound`. |
| **[Longest Common Subsequence](../../../google-sde2/PROBLEM_DETAILS.md#longest-common-subsequence)** | `dp[i][j]` from char match or max skip; classic 2D table. | **Space** one row if only length needed; **print** LCS needs backtrack. |
| **Longest Palindromic Substring** | Expand centers **O(n²)** or **Manacher** O(n). | **DP** `isPal[i][j]` for LPS **subsequence** differs from substring. |
| **Unique Paths** | `dp[i][j] = dp[i-1][j] + dp[i][j-1]`; obstacles → `0` if blocked. | **Mod** result; **start** blocked edge case. |
| **[Edit Distance](../../../google-sde2/PROBLEM_DETAILS.md#edit-distance)** | Insert/delete/replace recurrence on prefixes. | **One-row** optimization; **delete-only** variant simpler. |
| **[Burst Balloons](../../../google-sde2/PROBLEM_DETAILS.md#burst-balloons)** | Interval DP: add **imaginary** 1 balloons at ends; split at last balloon `k` in `(i,j)`. | **O(n³)**; **index** shift for closed interval `[i,j]`. |
| **[Word Break](../../../google-sde2/PROBLEM_DETAILS.md#word-break)** | `dp[i]` = can segment `s[0:i)`; try all dict words ending at `i`. | **Trie** speeds prefix checks; **Word Break II** all sentences → backtrack + memo. |
| **Decode Ways** | `dp[i]` from `dp[i-1]` (one digit) and `dp[i-2]` (two digits if 10–26). | **Leading zero** invalid; **`*`** wildcard variant harder. |

---

## See also

- [dp-aditya-verma.md](dp-aditya-verma.md) — choice diagram / knapsack style  
- [patterns/dp-advanced.md](../../../patterns/dp-advanced.md) — 16 patterns  
- [Backtracking](../backtracking.md) — when to memoize into DP
