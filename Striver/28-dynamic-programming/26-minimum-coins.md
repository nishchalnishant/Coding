---
module: striver/28-dynamic-programming
lesson: 26
topic: Minimum coins
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-coins?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, knapsack, unbounded]
---
# 26. Minimum coins

← [0 and 1 Knapsack](25-0-1-knapsack.md) · [Part 28 index](README.md) · Next → [Target sum](27-target-sum.md)

> [!abstract] Problem at a glance
> **Task:** Fewest coins (unlimited supply of each denomination) summing to `amount`; −1 if impossible.
> **Key insight:** Unbounded choice: when you **take** coin `i` you stay at `i`. 1D form: `dp[t] = min over coins c ≤ t of 1 + dp[t − c]`, filled with `t` **ascending**. Use ∞ (e.g. `amount + 1`) for unreachable. Greedy-by-largest fails for coins like `[1, 3, 4]`, amount 6.
> **Difficulty:** Medium · **Pattern:** Unbounded knapsack (min) · **Also on:** LC 322 (Coin Change)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-coins?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized (i, target)](#3-memoized-i-target) · [4. 1D tabulation, target ascending](#4-1d-tabulation-target-ascending) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given coin denominations `coins` (unlimited of each) and `amount`, return the fewest coins that sum to `amount`, or −1 if impossible.

| Input | Output | Why |
|---|---|---|
| `coins = [1,2,5], amount = 11` | `3` | 5+5+1 |
| `coins = [2], amount = 3` | `-1` |  |
| `coins = [1,3,4], amount = 6` | `2` | 3+3 (greedy 4+1+1 = 3 coins) |

**Constraints:** `1 ≤ coins.length ≤ 12`, `1 ≤ coins[i] ≤ 2³¹−1`, `0 ≤ amount ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized (i, target) | take stays at i | O(n·amount) | O(n·amount) |
| 1D tabulation, target ascending | dp[t] = min(dp[t], 1 + dp[t − c]) | O(n·amount) | O(amount) |

> [!tip] Interview angle
> Contrast 0/1 vs unbounded in one line: "take → stay at `i`" in the 2D form, or "loop the target upward" in the 1D form. Use `amount + 1` as infinity to avoid overflow on `1 + INF`.

---

## 3. Memoized (i, target)

**Intuition.** `f(i, t)`: at `i == 0`, return `t / c0` if divisible, else ∞. Otherwise `min(f(i−1, t), 1 + f(i, t − c_i))`.

```python
def coins_memo(coins, amount):
    INF = float("inf")
    from functools import lru_cache
    @lru_cache(None)
    def f(i, t):
        if i == 0:
            return t // coins[0] if t % coins[0] == 0 else INF
        best = f(i - 1, t)
        if coins[i] <= t:
            best = min(best, 1 + f(i, t - coins[i]))
        return best
    r = f(len(coins) - 1, amount)
    return -1 if r == INF else r
```

**Complexity:** time **O(n·amount)**, space **O(n·amount)**.

---

## 4. 1D tabulation, target ascending

**Intuition.** `dp[0] = 0`, others `amount + 1`. For each coin, sweep `t` upward so `dp[t − c]` may already include this coin, which is what allows reuse.

**Algorithm**

1. `dp = [0] + [amount+1]*amount`.
2. For each coin `c`: for `t = c..amount`: `dp[t] = min(dp[t], 1 + dp[t − c])`.
3. Return `dp[amount]` if ≤ amount else −1.

**Dry run** — coins [1,3,4], 6: after 1 → dp[t] = t; after 3 → dp[3] = 1, dp[6] = 2; after 4 → dp[4] = 1, dp[5] = 2, dp[6] = 2.

**C++**
```cpp
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int c : coins)
        for (int t = c; t <= amount; t++)
            dp[t] = min(dp[t], 1 + dp[t - c]);
    return dp[amount] > amount ? -1 : dp[amount];
}
```

**Java**
```java
static int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int c : coins)
        for (int t = c; t <= amount; t++)
            dp[t] = Math.min(dp[t], 1 + dp[t - c]);
    return dp[amount] > amount ? -1 : dp[amount];
}
```

**Python**
```python
def coin_change(coins, amount):
    dp = [0] + [amount + 1] * amount
    for c in coins:
        for t in range(c, amount + 1):
            dp[t] = min(dp[t], 1 + dp[t - c])
    return -1 if dp[amount] > amount else dp[amount]
```

**Complexity:** time **O(n·amount)**, space **O(amount)** — n × amount updates; `amount + 1` as ∞ never overflows.

---

## Edge cases

- `amount = 0`: 0 coins.
- Unreachable amount: −1.
- Huge coin values: the `t = c..amount` loop just never runs.

---

## Common mistakes

1. Greedy by largest coin.
2. `INT_MAX` as infinity, then `1 + INT_MAX` overflows.
3. Descending `t` loop (each coin used at most once).

---

## Follow-ups

1. Count the ways instead?
2. BFS view?

<details><summary>Answer sketches</summary>

**#1:** Coin Change II, two problems ahead.

**#2:** Amounts are nodes, coins are edges; BFS from 0 finds the fewest coins too.
</details>

---

## Flashcards

**Min coins 1D loop direction?** #flashcard
Target ascending (unbounded reuse).

**Safe infinity?** #flashcard
`amount + 1`.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
