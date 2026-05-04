# DP Questions Bank — Tiered Drill Sheet

70 questions organized by difficulty. Each entry includes: pattern tag, LeetCode number, hint, and key gotcha. Use this for timed drilling. For theory see [README.md](README.md) and the pattern-specific files.

---

## How to Use This Bank

1. **Timed drill:** Set a timer (Easy: 15 min, Medium: 25 min, Hard: 40 min).
2. **Pattern-first:** State the pattern before coding — if you can't, re-read the pattern file.
3. **Recurrence-first:** Write the recurrence on paper before touching code.
4. **Space optimize last:** Get the O(N²) or O(N×W) solution working, then optimize.

---

## Easy (20 Questions)

| # | Problem | LC # | Pattern | Hint | Key Gotcha |
| :--- | :--- | :--- | :--- | :--- | :--- |
| E1 | **Fibonacci Number** | 509 | Linear | `dp[i] = dp[i-1] + dp[i-2]` | Space optimize: use 2 vars |
| E2 | **Climbing Stairs** | 70 | Linear | Same as Fibonacci | Base: `dp[1]=1, dp[2]=2` |
| E3 | **Min Cost Climbing Stairs** | 746 | Linear | `dp[i] = cost[i] + min(dp[i-1], dp[i-2])` | Can start at step 0 OR 1 |
| E4 | **House Robber** | 198 | Linear | `dp[i] = max(dp[i-1], nums[i]+dp[i-2])` | Space: 2 rolling vars |
| E5 | **Pascal's Triangle** | 118 | Linear | `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` | Row edges = 1 always |
| E6 | **Is Subsequence** | 392 | 2-pointer / linear | Two-pointer, not DP | DP overkill for single query; use for multiple queries |
| E7 | **N-th Tribonacci Number** | 1137 | Linear | 3-variable rolling | Base: T0=0, T1=1, T2=1 |
| E8 | **Divisor Game** | 1025 | Game Theory | Alice wins iff N is even | Math: always pick factor 1; parity flips |
| E9 | **Unique Paths** | 62 | Grid | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` | Math: C(m+n-2, m-1) is O(1) |
| E10 | **Best Time to Buy/Sell I** | 121 | Greedy / DP | Track running minimum | Answer = max(price - min_so_far) |
| E11 | **Maximum Subarray** | 53 | Kadane | `end_here = max(x, end_here + x)` | Start fresh when extending worsens |
| E12 | **Range Sum Query (Immutable)** | 303 | Prefix sum | `prefix[i] = prefix[i-1] + nums[i-1]` | Not strictly DP — prefix sum pattern |
| E13 | **Jump Game** | 55 | Greedy / linear | Track max reachable index | DP is O(N²); greedy is O(N) |
| E14 | **Counting Bits** | 338 | Linear | `dp[i] = dp[i >> 1] + (i & 1)` | Right-shift halves, LSB is the parity |
| E15 | **Longest Continuous Increasing Subsequence** | 674 | Linear | Reset on non-increase | Contiguous — do not carry over across breaks |
| E16 | **Largest Divisible Subset** (basic warm-up) | 368 | LIS variant | Sort first; LIS condition = divisibility | Track parent[] for reconstruction |
| E17 | **Delete and Earn** | 740 | Linear (House Robber) | `earn[v] = v * count(v)`; adjacent values conflict | Sort, build earn array, run House Robber |
| E18 | **Minimum Path Sum** | 64 | Grid | `dp[i][j] = grid[i][j] + min(up, left)` | In-place saves O(N) space |
| E19 | **Maximal Square** | 221 | Grid / Region | `dp[i][j] = min(3 neighbors) + 1` | Answer = `max_side²` |
| E20 | **Get Maximum in Generated Array** | 1646 | Linear | `a[2i] = a[i]`; `a[2i+1] = a[i]+a[i+1]` | Track max during generation |

---

## Medium (30 Questions)

| # | Problem | LC # | Pattern | Hint | Key Gotcha |
| :--- | :--- | :--- | :--- | :--- | :--- |
| M1 | **Coin Change I (min coins)** | 322 | Unbounded Knapsack | `dp[w] = min(dp[w], 1 + dp[w-c])` | Init to `inf`; return -1 if still `inf` |
| M2 | **Coin Change II (count ways)** | 518 | Unbounded Knapsack | Coins outer → combinations | `dp[0] = 1`; forward loop |
| M3 | **Partition Equal Subset Sum** | 416 | 0/1 Knapsack | Target = `sum // 2`; bool DP | Odd sum → impossible immediately |
| M4 | **Target Sum** | 494 | 0/1 Knapsack | Count subsets with sum `(total+target)/2` | Parity check: `(total+target)` must be even |
| M5 | **Word Break** | 139 | Linear DP + set | `dp[i]` = can segment `s[:i]` | Use a set for O(1) word lookup |
| M6 | **Decode Ways** | 91 | Linear | One-digit + two-digit branches | `'0'` alone invalid; `'06'` invalid |
| M7 | **Longest Increasing Subsequence** | 300 | LIS | O(N log N) patience sort | `bisect_left` for strict LIS; `tails` ≠ actual LIS |
| M8 | **House Robber II (circle)** | 213 | Linear | Two passes: exclude first OR last | Can't rob both first and last |
| M9 | **Maximum Product Subarray** | 152 | Kadane | Track both `cur_max` and `cur_min` | Negative × negative = large positive |
| M10 | **Jump Game II (min jumps)** | 45 | Greedy / linear | Track current and next reach | Greedy O(N) beats DP O(N²) |
| M11 | **Unique Paths II (obstacles)** | 63 | Grid | Reset blocked cells to 0 | Blocked start cell → always 0 |
| M12 | **Longest Common Subsequence** | 1143 | LCS | `match → dp[i-1][j-1]+1`; else `max(up,left)` | 1-indexed; `dp[0][*]=dp[*][0]=0` |
| M13 | **Edit Distance** | 72 | LCS | Replace=diag+1; insert/delete=axis+1 | Initialize `dp[i][0]=i`, `dp[0][j]=j` |
| M14 | **Palindromic Substrings** | 647 | Palindrome | Expand around 2n-1 centers | Both odd and even centers |
| M15 | **Longest Palindromic Subsequence** | 516 | Interval DP | `LCS(s, rev(s))` | `dp[i][i]=1`; fill by length |
| M16 | **Triangle Minimum Path** | 120 | Grid | Bottom-up; `dp[j] = triangle[i][j] + min(dp[j], dp[j+1])` | Work bottom-up to avoid width management |
| M17 | **Russian Doll Envelopes** | 354 | LIS (2D) | Sort (w asc, h desc); LIS on h | Descending h prevents same-width stacking |
| M18 | **Interleaving String** | 97 | 2D string DP | `dp[i][j]` can form `s3[:i+j]` | Check `m+n == len(s3)` first |
| M19 | **Distinct Subsequences** | 115 | 2D string DP | Add ways (not max) | `dp[i][0] = 1`; empty t always subseq |
| M20 | **Stock Buy/Sell with Cooldown** | 309 | State machine | 3 states: `hold, sold, rest` | Use `prev_sold` to avoid same-iteration update |
| M21 | **Stock Buy/Sell with Fee** | 714 | State machine | 2 states; subtract fee on sell | Subtract fee at sell OR buy — not both |
| M22 | **Best Time III (2 transactions)** | 123 | State machine | 4 states: `buy1, sell1, buy2, sell2` | Chain `sell1` into `buy2` |
| M23 | **Counting Subsets Equal Sum** | — | 0/1 Knapsack | `dp[w] += dp[w-num]`; backward | `dp[0]=1`; backward prevents reuse |
| M24 | **Last Stone Weight II** | 1049 | 0/1 Knapsack | Minimize `|S1-S2|` = total-2*max_S1_leq_half | Subset sum to `total//2` |
| M25 | **Ones and Zeroes** | 474 | 2D Knapsack | `dp[i][j]` = max strings with ≤ i zeros, ≤ j ones | Backward 2D loop for 0/1 |
| M26 | **Perfect Squares** | 279 | Unbounded Knapsack | Coins = 1,4,9,16…; min count to sum N | Same as coin change |
| M27 | **Integer Break** | 343 | Unbounded Knapsack | `dp[i] = max(j*(i-j), j*dp[i-j])` | Greedy: use 3s (AM-GM); DP is safe |
| M28 | **Maximal Rectangle** | 85 | Histogram + Stack | Build heights row by row; stack for histogram | Not pure DP; stack inner loop |
| M29 | **Longest Common Substring** | — | 2D DP | Reset to 0 on mismatch | Track global max — answer ≠ `dp[m][n]` |
| M30 | **Stone Game III** | 1406 | Minimax | `dp[i] = max over k=1,2,3 of (sum_k − dp[i+k])` | dp[i] = score advantage; >0 → Alice wins |

---

## Hard (20 Questions)

| # | Problem | LC # | Pattern | Hint | Key Gotcha |
| :--- | :--- | :--- | :--- | :--- | :--- |
| H1 | **Burst Balloons** | 312 | Interval DP | `k` = LAST balloon to burst in `(i,j)` | k is last, not first — makes subproblems non-overlapping |
| H2 | **Regular Expression Matching** | 10 | 2D string DP | `*` = zero or more of PRECEDING char | `dp[0][j] = dp[0][j-2]` for leading `a*` patterns |
| H3 | **Wildcard Matching** | 44 | 2D string DP | `*` = any sequence (standalone) | `dp[i][j] = dp[i-1][j] or dp[i][j-1]` for `*` |
| H4 | **Super Egg Drop** | 887 | Inverted DP | `dp[m][k]` = max floors with m moves, k eggs | Inverted DP O(K log N); standard is O(KN²) |
| H5 | **Palindrome Partitioning II** | 132 | Interval + linear | Precompute `is_pal`; `cut[i] = min(cut[j-1]+1)` | `is_pal[0][i]` → `cut[i] = 0` |
| H6 | **Strange Printer** | 664 | Interval DP | If `s[i]==s[j]`: `dp[i][j] = dp[i][j-1]` | Merge when endpoints match — one free print |
| H7 | **Minimum Window Subsequence** | 727 | 2D DP | `dp[i][j]` = start pos in s for t[:j] ending at s[i] | Slide window starting position after each match |
| H8 | **Edit Distance** | 72 | LCS | Replace=diag+1; insert/delete=axis+1 | Space optimize to 1D with `prev` scalar for diagonal |
| H9 | **Shortest Common Supersequence** | 1092 | LCS | Length = `m+n-LCS`; reconstruct by merge | Traceback: on match — take char; else take from longer side |
| H10 | **Travelling Salesman (All Nodes)** | 847 | Bitmask DP | `dp[mask][node]`; BFS for pairwise distances | Multi-source BFS start; goal = `dp[FULL][any]` |
| H11 | **Smallest Sufficient Team** | 1125 | Bitmask DP | `dp[skill_mask]` = min team to cover | OR bitmasks for coverage; 2^26 is too large — use only relevant skills |
| H12 | **Cherry Pickup** | 741 | 3D DP (2 trips) | Two simultaneous forward trips; `dp[t][r1][r2]` | Use `r1 <= r2` symmetry to halve states |
| H13 | **Dungeon Game** | 174 | Reverse Grid DP | Work backward from goal | Forward DP cannot determine min HP — must reverse |
| H14 | **Stone Game V** | 1563 | Interval DP | Split array; keep the side with smaller sum | `dp[i][j] = max gain when array = piles[i..j]` |
| H15 | **Palindrome Partitioning III** | 1278 | 2D DP + cost | `dp[i][k]` = min changes, prefix `i`, `k` parts | `cost(l,r)` = chars to fix; memoize separately |
| H16 | **Paint House III** | 1473 | 3D DP | `dp[house][color][neighborhood]` | 3 dimensions; initialize with `inf` for impossible states |
| H17 | **Stock Buy/Sell IV (K transactions)** | 188 | State machine DP | `dp[k][0/1]`; backward k-loop | `2k >= n` → unlimited (greedy) |
| H18 | **Concatenated Words** | 472 | Word Break variant | DFS + memo; each word = word break of itself? | A word cannot be formed by itself alone (add exclusion) |
| H19 | **Jump Game IV** | 1345 | BFS (not DP) | BFS with value-grouped jumps | DP overkill; multi-source BFS is optimal |
| H20 | **Tallest Billboard** | 956 | DP with difference | `dp[diff]` = max height sum where `|s1 - s2| = diff` | Key: maximize `min(s1, s2)` not `s1+s2` |

---

## Pattern Quick-Reference Index

| Pattern | Easy | Medium | Hard |
| :--- | :--- | :--- | :--- |
| **Linear / Fibonacci** | E1–E3, E7, E14, E20 | M5, M6, M8 | — |
| **Kadane** | E11 | M9 | — |
| **0/1 Knapsack** | E17 | M3, M4, M23, M24, M25 | — |
| **Unbounded Knapsack** | — | M1, M2, M26, M27 | — |
| **Grid DP** | E9, E18, E19 | M11, M16, M28 | H13 |
| **LCS / String** | — | M12, M13, M18, M19, M29 | H7, H8, H9 |
| **LIS** | — | M7, M17 | — |
| **Interval DP** | — | M14, M15 | H1, H6, H14, H15 |
| **Stock / State Machine** | E10 | M20, M21, M22 | H17 |
| **Bitmask DP** | — | — | H10, H11 |
| **Tree DP** | — | — | — |
| **Game Theory** | E8 | M30 | H4 |
| **Palindrome** | — | M14, M15 | H5, H15 |
| **Regex / Wildcard** | — | — | H2, H3 |

---

## Drill Schedules

### 1-Week Blitz (Interview in 7 days)

| Day | Focus | Questions |
| :--- | :--- | :--- |
| 1 | Linear + Kadane | E1–E12, M9 |
| 2 | Knapsack family | M1–M4, M23–M27 |
| 3 | LCS + String | M12, M13, M18, M19, M29 |
| 4 | Grid DP + Palindrome | E9, E18, E19, M14, M15, H5 |
| 5 | LIS + Interval | M7, M15, M17, H1, H6 |
| 6 | Stock + Bitmask | M20–M22, H17, H10, H11 |
| 7 | Hard review | H2, H3, H4, H8, H12 |

### 2-Day Emergency Revision (Google-style)

| Session | Questions | Time Budget |
| :--- | :--- | :--- |
| AM | E1, E2, E4, E11, M1, M3, M7, M12 | 90 min |
| PM | M13, M20, H1, H2, H4, H5 | 90 min |

---

## See also

- [README.md](README.md) — Theory and 4-step framework
- [dp-aditya-verma.md](dp-aditya-verma.md) — Full pattern playbook with code
- [tips-and-gotchas.md](tips-and-gotchas.md) — Master cheatsheet for bugs and recognition
- [digit-dp.md](digit-dp.md) | [grid-dp.md](grid-dp.md) | [stock-trading-dp.md](stock-trading-dp.md) | [string-palindrome-dp.md](string-palindrome-dp.md)
