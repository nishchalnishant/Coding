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
