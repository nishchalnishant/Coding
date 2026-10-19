---
module: striver/28-dynamic-programming
lesson: 17
topic: Best time to buy and sell stock IV
difficulty: Hard
source: https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-iv?category=dp-on-stocks&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, stocks, state-machine]
---
# 17. Best time to buy and sell stock IV

← [Best time to buy and sell stock III](16-best-time-to-buy-and-sell-stock-iii.md) · [Part 28 index](README.md) · Next → [Best time to buy and sell stock with transaction fees](18-best-time-to-buy-and-sell-stock-with-transaction-fee.md)

> [!abstract] Problem at a glance
> **Task:** At most `k` transactions. Maximise profit.
> **Key insight:** Generalise Stock III: `buy[j] = max(buy[j], sell[j−1] − p)`, `sell[j] = max(sell[j], buy[j] + p)` for `j = 1..k`. Equivalently, number the actions: `(i, t)` with `t ∈ [0, 2k)`, where even `t` means buy and odd `t` means sell. If `k ≥ n/2` the cap never binds, so fall back to Stock II.
> **Difficulty:** Hard · **Pattern:** Stock state machine with k cap · **Also on:** LC 188
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-iv?category=dp-on-stocks&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized (i, transaction number)](#3-memoized-i-transaction-number) · [4. Forward buy[]/sell[] arrays](#4-forward-buysell-arrays) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `k` and `prices`, return the maximum profit with at most `k` transactions.

| Input | Output | Why |
|---|---|---|
| `k = 2, prices = [2,4,1]` | `2` | buy 2 sell 4 |
| `k = 2, prices = [3,2,6,5,0,3]` | `7` | (6−2) + (3−0) |

**Constraints:** `1 ≤ k ≤ 100`, `1 ≤ n ≤ 1000`, `0 ≤ prices[i] ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized (i, transaction number) | t even = buy, t odd = sell | O(n·2k) | O(n·2k) |
| Forward buy[]/sell[] arrays | k copies of the Stock III chain | O(n·k) | O(k) |

> [!tip] Interview angle
> Mention the `k ≥ n/2 → unlimited` shortcut. It turns an O(n·k) DP into O(n) when `k` is huge (e.g. 10⁹), and older versions of this problem test it.

---

## 3. Memoized (i, transaction number)

**Intuition.** `f(i, t)`: if `i == n` or `t == 2k`, return 0. Even `t`: `max(−p[i] + f(i+1, t+1), f(i+1, t))`. Odd `t`: `max(p[i] + f(i+1, t+1), f(i+1, t))`.

```python
def stock4_memo(k, p):
    n = len(p)
    from functools import lru_cache
    @lru_cache(None)
    def f(i, t):
        if i == n or t == 2 * k:
            return 0
        sign = -1 if t % 2 == 0 else 1
        return max(sign * p[i] + f(i + 1, t + 1), f(i + 1, t))
    return f(0, 0)
```

**Complexity:** time **O(n·2k)**, space **O(n·2k)**.

---

## 4. Forward buy[]/sell[] arrays

**Intuition.** `buy[j]` = best cash after the j-th buy, `sell[j]` = after the j-th sell, with `sell[0] = 0`. Update `j = 1..k` per day.

**Algorithm**

1. `buy[1..k] = −∞`, `sell[0..k] = 0`.
2. For each price `x`, for `j = 1..k`: `buy[j] = max(buy[j], sell[j−1] − x)`; `sell[j] = max(sell[j], buy[j] + x)`.
3. Return `sell[k]`.

**Dry run** — k = 2, [3,2,6,5,0,3]: sell[1] reaches 4 at price 6; buy[2] = 4 − 0 = 4 at price 0; sell[2] = 7.

**C++**
```cpp
int maxProfit(int k, vector<int>& p) {
    vector<int> buy(k + 1, INT_MIN), sell(k + 1, 0);
    for (int x : p)
        for (int j = 1; j <= k; j++) {
            buy[j] = max(buy[j], sell[j - 1] - x);
            sell[j] = max(sell[j], buy[j] + x);
        }
    return sell[k];
}
```

**Java**
```java
static int maxProfit(int k, int[] p) {
    int[] buy = new int[k + 1], sell = new int[k + 1];
    Arrays.fill(buy, Integer.MIN_VALUE);
    for (int x : p)
        for (int j = 1; j <= k; j++) {
            buy[j] = Math.max(buy[j], sell[j - 1] - x);
            sell[j] = Math.max(sell[j], buy[j] + x);
        }
    return sell[k];
}
```

**Python**
```python
def max_profit_iv(k, p):
    buy = [float("-inf")] * (k + 1)
    sell = [0] * (k + 1)
    for x in p:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - x)
            sell[j] = max(sell[j], buy[j] + x)
    return sell[k]
```

**Complexity:** time **O(n·k)**, space **O(k)** — n days × k transactions, O(k) memory.

---

## Edge cases

- `k ≥ n/2`: equivalent to unlimited (Stock II).
- Decreasing prices: 0.

---

## Common mistakes

1. Allocating `n × k` memory when k is huge without the shortcut.
2. Reading `buy[j]` from the previous day vs today: both are correct here because a same-day buy and sell nets 0.

---

## Follow-ups

1. Stock IV with cooldown or fee?
2. k up to 10⁹?

<details><summary>Answer sketches</summary>

**#1:** Add the same tweaks to the `(i, t)` DP.

**#2:** If `2k ≥ n`, return the Stock II answer.
</details>

---

## Flashcards

**Stock IV state?** #flashcard
(day, transaction number t < 2k), even = buy, odd = sell.

**Stock IV shortcut?** #flashcard
`k ≥ n/2` → unlimited transactions.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
