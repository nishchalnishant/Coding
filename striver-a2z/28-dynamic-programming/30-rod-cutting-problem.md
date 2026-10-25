---
module: striver-a2z/28-dynamic-programming
lesson: 30
topic: Rod cutting problem
difficulty: Medium
source: https://takeuforward.org/learning/dsa/rod-cutting-problem?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, knapsack, unbounded]
---
# 30. Rod cutting problem

← [Unbounded knapsack](29-unbounded-knapsack.md) · [Part 28 index](README.md) · Next → [Longest increasing subsequence](31-longest-increasing-subsequence.md)

> [!abstract] Problem at a glance
> **Task:** Cut a rod of length `n` into integer pieces; a piece of length `L` sells for `price[L−1]`. Maximise revenue.
> **Key insight:** Every piece length `1..n` is an item with weight `L` and value `price[L−1]`, usable any number of times, with capacity `n`. **Rod cutting is unbounded knapsack.** Equivalently, `dp[L] = max over first cut c of price[c−1] + dp[L − c]`.
> **Difficulty:** Medium · **Pattern:** Unbounded knapsack (reframing)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/rod-cutting-problem?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized first-cut recursion](#3-memoized-first-cut-recursion) · [4. Unbounded knapsack table](#4-unbounded-knapsack-table) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `price[0..n−1]` where `price[i]` is the price of a piece of length `i + 1`, and the rod length `n`, return the maximum obtainable value by cutting the rod (or not cutting it).

| Input | Output | Why |
|---|---|---|
| `price = [2,5,7,8,10], n = 5` | `12` | 2 + 2 + 1 → 5 + 5 + 2 |
| `price = [3,5,8,9,10,17,17,20], n = 8` | `24` | eight pieces of length 1 |
| `price = [1,5,8,9,10,17,17,20], n = 8` | `22` | 2 + 6 → 5 + 17 |

**Constraints:** `1 ≤ n ≤ 10³`, `1 ≤ price[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized first-cut recursion | f(L) = max_c price[c−1] + f(L − c) | O(n²) | O(n) |
| Unbounded knapsack table | items = lengths, capacity = n | O(n²) | O(n) |

> [!tip] Interview angle
> Say the mapping explicitly: "length = weight, price = value, rod length = capacity, unlimited pieces → unbounded knapsack." Recognising reductions is the skill being tested here.

---

## 3. Memoized first-cut recursion

**Intuition.** Choose the length of the first piece, recurse on the remainder. `f(0) = 0`.

```python
def rod_memo(price, n):
    from functools import lru_cache
    @lru_cache(None)
    def f(L):
        if L == 0:
            return 0
        return max(price[c - 1] + f(L - c) for c in range(1, L + 1))
    return f(n)
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Unbounded knapsack table

**Intuition.** For each piece length `L`, sweep capacity upward: `dp[c] = max(dp[c], price[L−1] + dp[c − L])`.

**Algorithm**

1. `dp = [0]*(n+1)`.
2. For `L = 1..n`: for `c = L..n`: `dp[c] = max(dp[c], price[L−1] + dp[c − L])`.
3. Return `dp[n]`.

**Dry run** — [2,5,7,8,10], n 5: after L=1 → dp[c] = 2c; after L=2 → dp[4] = 10, dp[5] = 12; longer lengths don't help → 12.

**C++**
```cpp
int cutRod(vector<int>& price, int n) {
    vector<int> dp(n + 1, 0);
    for (int L = 1; L <= n; L++)
        for (int c = L; c <= n; c++)
            dp[c] = max(dp[c], price[L - 1] + dp[c - L]);
    return dp[n];
}
```

**Java**
```java
static int cutRod(int[] price, int n) {
    int[] dp = new int[n + 1];
    for (int L = 1; L <= n; L++)
        for (int c = L; c <= n; c++)
            dp[c] = Math.max(dp[c], price[L - 1] + dp[c - L]);
    return dp[n];
}
```

**Python**
```python
def cut_rod(price, n):
    dp = [0] * (n + 1)
    for L in range(1, n + 1):
        for c in range(L, n + 1):
            dp[c] = max(dp[c], price[L - 1] + dp[c - L])
    return dp[n]
```

**Complexity:** time **O(n²)**, space **O(n)** — n lengths × n capacities.

---

## Edge cases

- `n = 1`: `price[0]`.
- An uncut rod can be optimal (when `price[n−1]` is large).

---

## Common mistakes

1. Off-by-one between length `L` and `price[L−1]`.
2. Treating each length as usable once (0/1).

---

## Follow-ups

1. Cost per cut?
2. Return the cut lengths.

<details><summary>Answer sketches</summary>

**#1:** Subtract the cut cost whenever a piece is shorter than the remaining rod.

**#2:** Store the best first cut per length and follow it.
</details>

---

## Flashcards

**Rod cutting = ?** #flashcard
Unbounded knapsack with weight = length, value = price.

**Rod cutting recurrence?** #flashcard
`dp[L] = max_c price[c−1] + dp[L−c]`.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
