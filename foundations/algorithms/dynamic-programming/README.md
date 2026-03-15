# Dynamic Programming — SDE-3 Level

Optimization via overlapping subproblems and optimal substructure; store solutions (memo or table). SDE-3 expects recurrence derivation, space optimization, and pattern recognition (see [dp-advanced.md](../../patterns/dp-advanced.md)).

---

## 1. Concept Overview

**When to use**: Choices at each step; maximize/minimize/count; overlapping subproblems. If greedy doesn't apply and state space is manageable, try DP.

**Two approaches**: Top-down (recurse + memo; only needed states) vs bottom-up (table; often space-optimizable). State definition and recurrence are key.

---

## 2. Core Patterns (Summary)

- **1D**: Fibonacci, Climbing Stairs, House Robber, Decode Ways — dp[i] from dp[i-1], dp[i-2].
- **0/1 Knapsack**: Pick or skip; dp[i][w] = max( dp[i-1][w], val[i] + dp[i-1][w-wt[i]] ). Space → 1D backward loop.
- **Unbounded Knapsack**: Same item repeatable; dp[w] from dp[w-wt[i]].
- **LIS**: dp[i] = 1 + max dp[j] for j < i and arr[j] < arr[i]; or O(N log N) with binary search + tails.
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
- **LIS**: End at i; binary search for O(N log N).
- **LCS/Edit distance**: Two sequences; 2D.
- **Interval**: Break at k; MCM, Burst Balloons.
- **Tree**: Post-order; return multiple values (e.g., with/without node).
- **Bitmask**: Subset as integer; TSP, partition.
- **Digit**: Position, tight, sum/count.

---

## 6. SDE-3 Level Thinking

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
