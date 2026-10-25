---
module: striver-a2z/28-dynamic-programming
lesson: 28
topic: Coin change II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/coin-change-ii?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, knapsack, unbounded, counting]
---
# 28. Coin change II

← [Target sum](27-target-sum.md) · [Part 28 index](README.md) · Next → [Unbounded knapsack](29-unbounded-knapsack.md)

> [!abstract] Problem at a glance
> **Task:** Count the combinations (not permutations) of coins (unlimited) that make `amount`.
> **Key insight:** Loop **coins outside, amount inside (ascending)**: `dp[t] += dp[t − c]`. Fixing the coin order means each multiset is counted once. Swapping the loops counts ordered sequences (permutations), which is Combination Sum IV (LC 377).
> **Difficulty:** Medium · **Pattern:** Unbounded knapsack (count) · **Also on:** LC 518
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/coin-change-ii?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized (i, target)](#3-memoized-i-target) · [4. 1D tabulation, coins outer](#4-1d-tabulation-coins-outer) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `amount` and `coins` (unlimited supply), return the number of combinations that make up `amount`. The answer fits in a signed 32-bit integer.

| Input | Output | Why |
|---|---|---|
| `amount = 5, coins = [1,2,5]` | `4` | 5, 2+2+1, 2+1+1+1, 1×5 |
| `amount = 3, coins = [2]` | `0` |  |
| `amount = 10, coins = [10]` | `1` |  |

**Constraints:** `1 ≤ coins.length ≤ 300`, `1 ≤ coins[i] ≤ 5000`, `0 ≤ amount ≤ 5000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized (i, target) | take stays at i; skip goes to i−1 | O(n·amount) | O(n·amount) |
| 1D tabulation, coins outer | dp[t] += dp[t − c], t ascending | O(n·amount) | O(amount) |

> [!tip] Interview angle
> Expect the question "Why is this combinations and not permutations?" Answer: the outer loop over coins means every combination is built in coin-index order, exactly once.

---

## 3. Memoized (i, target)

**Intuition.** `f(i, t)`: at `i == 0`, return 1 if `t % c0 == 0`. Otherwise `f(i−1, t) + f(i, t − c_i)` when `c_i ≤ t`.

```python
def change_memo(amount, coins):
    from functools import lru_cache
    @lru_cache(None)
    def f(i, t):
        if i == 0:
            return 1 if t % coins[0] == 0 else 0
        r = f(i - 1, t)
        if coins[i] <= t:
            r += f(i, t - coins[i])
        return r
    return f(len(coins) - 1, amount)
```

**Complexity:** time **O(n·amount)**, space **O(n·amount)**.

---

## 4. 1D tabulation, coins outer

**Intuition.** `dp[0] = 1`. Processing coins one by one and sweeping `t` upward allows reuse of the current coin, but never of an earlier coin after a later one.

**Algorithm**

1. `dp = [1, 0, …]`.
2. For each `c`: for `t = c..amount`: `dp[t] += dp[t − c]`.
3. Return `dp[amount]`.

**Dry run** — amount 5, [1,2,5]: after 1 → [1,1,1,1,1,1]; after 2 → [1,1,2,2,3,3]; after 5 → dp[5] = 4.

**C++**
```cpp
int change(int amount, vector<int>& coins) {
    vector<unsigned long long> dp(amount + 1, 0);
    dp[0] = 1;
    for (int c : coins)
        for (int t = c; t <= amount; t++)
            dp[t] += dp[t - c];
    return (int)dp[amount];
}
```

**Java**
```java
static int change(int amount, int[] coins) {
    long[] dp = new long[amount + 1];
    dp[0] = 1;
    for (int c : coins)
        for (int t = c; t <= amount; t++)
            dp[t] += dp[t - c];
    return (int) dp[amount];
}
```

**Python**
```python
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:
        for t in range(c, amount + 1):
            dp[t] += dp[t - c]
    return dp[amount]
```

**Complexity:** time **O(n·amount)**, space **O(amount)** — n × amount; intermediate cells can exceed int even when the answer doesn't, hence the 64-bit array.

---

## Edge cases

- `amount = 0`: 1 (the empty combination).
- No coin divides the amount: 0.

---

## Common mistakes

1. Amount loop outside, which counts permutations.
2. 32-bit overflow in intermediate cells (LC tests hit it).

---

## Follow-ups

1. Count ordered sequences (LC 377)?
2. Limited supply of each coin?

<details><summary>Answer sketches</summary>

**#1:** Swap the loops: amount outer, coins inner.

**#2:** Bounded knapsack: binary-split the counts into 0/1 items, or use a sliding window per residue.
</details>

---

## Flashcards

**Combinations vs permutations loop order?** #flashcard
Coins outer → combinations; amount outer → permutations.

**Coin change II base?** #flashcard
dp[0] = 1.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
