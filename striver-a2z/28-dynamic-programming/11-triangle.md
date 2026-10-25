---
module: striver-a2z/28-dynamic-programming
lesson: 11
topic: Triangle
difficulty: Medium
source: https://takeuforward.org/learning/dsa/triangle?category=dp-on-grids&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, grid]
---
# 11. Triangle

← [Minimum Falling Path Sum](10-minimum-falling-path-sum.md) · [Part 28 index](README.md) · Next → [Cherry pickup II](12-cherry-pickup-ii.md)

> [!abstract] Problem at a glance
> **Task:** Find the minimum top-to-bottom path sum in a triangle, moving to index `j` or `j+1` of the next row.
> **Key insight:** Going **bottom-up** removes the variable-end problem: start with the last row as `dp`, then `dp[j] = t[i][j] + min(dp[j], dp[j+1])` moving upward. `dp[0]` is the answer, with no final min, no ∞ checks and O(n) extra space.
> **Difficulty:** Medium · **Pattern:** Grid DP, bottom-up to fix the start · **Also on:** LC 120
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/triangle?category=dp-on-grids&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized recursion from the top](#3-memoized-recursion-from-the-top) · [4. Bottom-up with one row](#4-bottom-up-with-one-row) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a triangle where row `i` has `i + 1` numbers, start at the top and move each step to the adjacent index `j` or `j+1` in the row below. Return the minimum path sum to the bottom.

| Input | Output | Why |
|---|---|---|
| `[[2],[3,4],[6,5,7],[4,1,8,3]]` | `11` | 2 + 3 + 5 + 1 |
| `[[-10]]` | `-10` | single cell |

**Constraints:** `1 ≤ rows ≤ 200`, `−10⁴ ≤ t[i][j] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized recursion from the top | f(i,j) = t[i][j] + min(f(i+1,j), f(i+1,j+1)) | O(n²) | O(n²) |
| Bottom-up with one row | dp = last row; move up | O(n²) | O(n) |

> [!tip] Interview angle
> This is the canonical "fixed start, variable end → reverse the direction" trick. The top-down version needs `min` of the last row plus edge checks, while bottom-up has neither. Mention the follow-up of using O(n) extra space without modifying the input.

---

## 3. Memoized recursion from the top

**Intuition.** `f(i, j)` = cheapest path from `(i, j)` to the bottom. The last row returns its own value. The answer is `f(0, 0)`.

```python
def tri_memo(t):
    n = len(t)
    dp = [[None] * (i + 1) for i in range(n)]
    def f(i, j):
        if i == n - 1:
            return t[i][j]
        if dp[i][j] is None:
            dp[i][j] = t[i][j] + min(f(i + 1, j), f(i + 1, j + 1))
        return dp[i][j]
    return f(0, 0)
```

**Complexity:** time **O(n²)**, space **O(n²)**.

---

## 4. Bottom-up with one row

**Intuition.** `dp[j]` holds the best path from `(i+1, j)` downward. Processing `j` left to right is safe, because `dp[j]` and `dp[j+1]` are both from the row below until `dp[j]` is overwritten, and later cells read only `dp[j+1..]`.

**Algorithm**

1. `dp = copy(t[n−1])`.
2. For `i = n−2` down to 0, for `j = 0..i`: `dp[j] = t[i][j] + min(dp[j], dp[j+1])`.
3. Return `dp[0]`.

**Dry run** — [[2],[3,4],[6,5,7],[4,1,8,3]]: dp = [4,1,8,3] → [7,6,10] → [9,10] → [11].

**C++**
```cpp
int minimumTotal(vector<vector<int>>& t) {
    int n = t.size();
    vector<int> dp = t[n - 1];
    for (int i = n - 2; i >= 0; i--)
        for (int j = 0; j <= i; j++)
            dp[j] = t[i][j] + min(dp[j], dp[j + 1]);
    return dp[0];
}
```

**Java**
```java
static int minimumTotal(int[][] t) {
    int n = t.length;
    int[] dp = t[n - 1].clone();
    for (int i = n - 2; i >= 0; i--)
        for (int j = 0; j <= i; j++)
            dp[j] = t[i][j] + Math.min(dp[j], dp[j + 1]);
    return dp[0];
}
```

**Python**
```python
def minimum_total(t):
    dp = list(t[-1])
    for i in range(len(t) - 2, -1, -1):
        for j in range(i + 1):
            dp[j] = t[i][j] + min(dp[j], dp[j + 1])
    return dp[0]
```

**Complexity:** time **O(n²)**, space **O(n)** — each of the ~n²/2 cells once.

---

## Edge cases

- One row: the single value.
- Negative values: no special case in the bottom-up version.

---

## Common mistakes

1. Greedy smaller child at each step.
2. Top-down without taking the min of the whole last row.

---

## Follow-ups

1. Return the path itself.
2. Maximum path sum (Project Euler 18)?

<details><summary>Answer sketches</summary>

**#1:** Keep a `choice[i][j]` of which child won, then walk from the top.

**#2:** Swap min for max.
</details>

---

## Flashcards

**Triangle: why go bottom-up?** #flashcard
Fixed start, variable end: reversing makes the start the single answer cell.

**Triangle bottom-up update?** #flashcard
`dp[j] = t[i][j] + min(dp[j], dp[j+1])`.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
