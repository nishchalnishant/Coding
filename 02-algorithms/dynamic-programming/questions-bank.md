---
module: 02-algorithms
topic: Dynamic Programming
subtopic: Questions Bank
status: unread
tags: [algorithms, dynamic-programming]
---
## First-Principles Map

```text
WHY dynamic programming exists
├── Recursive solutions recompute identical subproblems exponentially many times
│   ├── Fibonacci naive: O(2^n) calls; with memo: O(n) calls, O(n) space
│   └── Overlapping subproblems + optimal substructure = DP applicability test
WHAT it is
├── Memoization (top-down): cache recursive call results; natural problem decomposition
├── Tabulation (bottom-up): fill table in dependency order; no call-stack overhead
│   ├── 1-D table: single-index state (Fibonacci, coin change, house robber)
│   ├── 2-D table: two-index state (LCS, edit distance, 0/1 knapsack)
│   └── Interval DP: dp[i][j] depends on dp[i][k] + dp[k+1][j] (matrix chain, burst balloons)
HOW it works
├── Identify state: minimum variables that fully describe a subproblem
├── Write recurrence: dp[state] = f(dp[smaller states])
├── Determine base cases: smallest states solvable without recursion
├── Determine evaluation order: ensure dp[smaller] is computed before dp[larger]
│   └── For intervals: outer loop on length, inner on start index
├── Space optimization: if dp[i] depends only on dp[i-1], use two variables instead of array
WHEN to use
├── "count ways to reach X" → additive recurrence, bottom-up 1-D
├── "minimum cost / maximum value with capacity constraint" → 0/1 knapsack 2-D dp
├── "longest common subsequence / edit distance" → 2-D string DP
├── "optimal way to split/merge intervals" → interval DP on dp[i][j]
├── "decisions affect future choices" (stock cooldown, house robber II) → state machine DP
└── "palindrome / substring structure" → expand-around-center or dp[i][j] for substring
WHAT can go wrong
├── State is under-specified → multiple distinct subproblems map to same key → wrong answers
├── Wrong evaluation order → reading dp[larger] before it's computed
└── Space optimization applied too early → lose states needed for reconstruction
DECISION
└── Overlapping subproblems + optimal substructure confirmed → DP; if state space is a DAG → topological tabulation; if state too large → BFS/greedy alternative
```

## First-Principles Breakdown

- **Root problem**: Naive recursion solves the same subproblem O(2^n) times; DP caches results so each unique subproblem is solved exactly once.
- **Core insight**: Define a state that uniquely identifies a subproblem, write a recurrence expressing the optimal state in terms of strictly smaller states, then fill in dependency order.
- **Invariant**: When computing dp[i] (or dp[i][j]), all states it depends on are already finalized.
- **Why it works**: Optimal substructure guarantees that combining optimal sub-solutions gives the global optimum; overlapping subproblems guarantees memoization pays off.
- **Where it breaks**: Insufficient state definition (missing a dimension like index, capacity, or previous choice) causes different subproblems to collide on the same cache key.

---

# Dynamic Programming Question Bank — Tiered Drill

Standardize your intuition by solving these 70 problems. Every problem here maps to one of the 11 patterns in the [Aditya Verma Playbook](dp-aditya-verma.md).

---

## 🟢 Level 1: Foundation (Pattern Recognition)

| Problem | Pattern | Key Insight |
| :--- | :--- | :--- |
| **Climbing Stairs** | Linear DP | Fibonacci: `dp[i] = dp[i-1] + dp[i-2]` |
| **Min Cost Climbing Stairs** | Linear DP | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` |
| **Subset Sum Problem** | 0/1 Knapsack | `dp[i][j]` = is sum `j` possible with first `i` items? |
| **Coin Change (Min Coins)** | Unbounded Knapsack | `dp[i] = 1 + min(dp[i - coin])` |
| **Longest Common Subsequence** | LCS | `s1[i] == s2[j] ? 1 + diag : max(top, left)` |
| **Maximum Subarray (Kadane)** | Kadane | `best = max(x, best + x)` |

---

## 🟡 Level 2: SDE-2 Standard (The "Twist")

| Problem | Pattern | The Twist |
| :--- | :--- | :--- |
| **Partition Equal Subset Sum** | 0/1 Knapsack | Target = `total_sum / 2` |
| **Target Sum** | 0/1 Knapsack | Math: `P - N = target` → `2P = target + total` |
| **Coin Change II (Total Ways)** | Unbounded Knapsack | `dp[i] += dp[i - coin]` (order matters for combinations) |
| **Edit Distance** | LCS Family | Three choices: insert, delete, replace |
| **Longest Palindromic Subsequence** | LCS Family | `LCS(s, reverse(s))` |
| **House Robber II** | Linear DP | Circular constraint: `max(rob(0..n-2), rob(1..n-1))` |
| **Maximal Square** | Grid DP | `min(3 neighbors) + 1` |
| **Word Break** | Linear DP | `dp[i] = any(dp[j] and s[j:i] in dict)` |

---

## 🔴 Level 3: SDE-3 / Staff Level (Deep Logic)

| Problem | Pattern | Complexity / Optimization |
| :--- | :--- | :--- |
| **Burst Balloons** | Interval DP | `k` is the **last** balloon to burst |
| **Super Egg Drop** | Optimization | Binary search + DP or Inverted DP `dp[moves][eggs]` |
| **Shortest Path Visiting All Nodes** | Bitmask DP | `(mask, last_node)` state in BFS |
| **Numbers At Most N Given Digit Set** | Digit DP | `tight` constraint tracking |
| **Binary Tree Maximum Path Sum** | Tree DP | Single-arm gain vs. full-path through node |
| **Stock with Cooldown** | State Machine | 3 states: `hold`, `sold`, `rest` |
| **Minimum Window Subsequence** | LCS / Two Pointers | 2D DP to find start of best match |

---

## 🛠️ Drill Instructions

1.  **Don't jump to code.** Draw the choice diagram first.
2.  **Identify the state.** If you can't name `dp[i][j]` in one sentence, you haven't understood the problem.
3.  **Space optimize.** If you've solved it with 2D, try to reduce it to 1D before moving on.
4.  **Trace the Base Case.** 90% of DP bugs are off-by-one errors in initialization.

---

## See also

- [Aditya Verma Playbook](dp-aditya-verma.md) — Step-by-step build for these patterns.
- [DP README](README.md) — Theoretical foundations and complexity map.
