---
module: striver/28-dynamic-programming
lesson: 15
topic: Best time to buy and sell stock II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-ii?category=dp-on-stocks&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, stocks, state-machine]
---
# 15. Best time to buy and sell stock II

← [Best time to buy and sell stock](14-best-time-to-buy-and-sell-stock.md) · [Part 28 index](README.md) · Next → [Best time to buy and sell stock III](16-best-time-to-buy-and-sell-stock-iii.md)

> [!abstract] Problem at a glance
> **Task:** Unlimited transactions (hold at most one share at a time). Maximise profit.
> **Key insight:** State `(i, holding)`. Not holding: skip or buy (`−p[i] + f(i+1, hold)`). Holding: skip or sell (`+p[i] + f(i+1, free)`). This **buy/sell state machine** is the template for all the stock problems, which only change the state. Here it collapses to summing every positive daily difference.
> **Difficulty:** Medium · **Pattern:** Stock state machine (unlimited) · **Also on:** LC 122
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-ii?category=dp-on-stocks&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized state machine](#3-memoized-state-machine) · [4. Greedy: sum of rises](#4-greedy-sum-of-rises) · [5. Tabulated state machine, O(1)](#5-tabulated-state-machine-o1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`prices[i]` is the price on day `i`. You may complete as many buy/sell transactions as you like, but you must sell before buying again. Return the maximum profit.

| Input | Output | Why |
|---|---|---|
| `[7,1,5,3,6,4]` | `7` | (5−1) + (6−3) |
| `[1,2,3,4,5]` | `4` | buy 1 sell 5, or every daily gain |
| `[7,6,4,3,1]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 3·10⁴`, `0 ≤ prices[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized state machine | f(i, buy) over buy/sell/skip | O(n·2) | O(n·2) |
| Greedy: sum of rises | Σ max(0, p[i] − p[i−1]) | O(n) | O(1) |
| Tabulated state machine, O(1) | aheadBuy, aheadSell rolled backward | O(n) | O(1) |

> [!tip] Interview angle
> Code the state machine even though the greedy is shorter. It extends directly to cooldown, fees and k transactions, and the interviewer will usually ask for one of those next.

---

## 3. Memoized state machine

**Intuition.** `f(i, canBuy)`: if `canBuy`, `max(−p[i] + f(i+1, 0), f(i+1, 1))`; else `max(p[i] + f(i+1, 1), f(i+1, 0))`. `f(n, ·) = 0`.

```python
def stock2_memo(p):
    n = len(p)
    dp = [[-1, -1] for _ in range(n)]
    def f(i, can_buy):
        if i == n:
            return 0
        if dp[i][can_buy] == -1:
            if can_buy:
                dp[i][can_buy] = max(-p[i] + f(i + 1, 0), f(i + 1, 1))
            else:
                dp[i][can_buy] = max(p[i] + f(i + 1, 1), f(i + 1, 0))
        return dp[i][can_buy]
    return f(0, 1)
```

**Complexity:** time **O(n·2)**, space **O(n·2)**.

---

## 4. Greedy: sum of rises

**Intuition.** Any profitable hold from `a` to `b` equals the sum of its daily differences, so collecting every positive difference is optimal.

```python
def stock2_greedy(p):
    return sum(max(0, p[i] - p[i - 1]) for i in range(1, len(p)))
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 5. Tabulated state machine, O(1)

**Intuition.** Fill from `i = n−1` down. `aheadBuy`/`aheadNotBuy` are `f(i+1, 1)` / `f(i+1, 0)`. Two variables replace the table.

**Algorithm**

1. `aheadBuy = aheadSell = 0` (day n).
2. For `i = n−1..0`: `curBuy = max(−p[i] + aheadSell, aheadBuy)`; `curSell = max(p[i] + aheadBuy, aheadSell)`.
3. Shift and return `aheadBuy`.

**Dry run** — [1,2,3]: i=2 → buy 0, sell 3; i=1 → buy max(−2+3, 0) = 1, sell max(2+0, 3) = 3; i=0 → buy max(−1+3, 1) = 2.

**C++**
```cpp
int maxProfit(vector<int>& p) {
    int aheadBuy = 0, aheadSell = 0;
    for (int i = (int)p.size() - 1; i >= 0; i--) {
        int curBuy = max(-p[i] + aheadSell, aheadBuy);
        int curSell = max(p[i] + aheadBuy, aheadSell);
        aheadBuy = curBuy;
        aheadSell = curSell;
    }
    return aheadBuy;
}
```

**Java**
```java
static int maxProfit(int[] p) {
    int aheadBuy = 0, aheadSell = 0;
    for (int i = p.length - 1; i >= 0; i--) {
        int curBuy = Math.max(-p[i] + aheadSell, aheadBuy);
        int curSell = Math.max(p[i] + aheadBuy, aheadSell);
        aheadBuy = curBuy;
        aheadSell = curSell;
    }
    return aheadBuy;
}
```

**Python**
```python
def max_profit_ii(p):
    ahead_buy = ahead_sell = 0
    for x in reversed(p):
        ahead_buy, ahead_sell = max(-x + ahead_sell, ahead_buy), max(x + ahead_buy, ahead_sell)
    return ahead_buy
```

**Complexity:** time **O(n)**, space **O(1)** — 2 states per day, constant memory; the same skeleton serves the rest of the stock family.

---

## Edge cases

- Flat prices: 0.
- One day: 0.

---

## Common mistakes

1. Updating `aheadBuy` before computing `curSell` from the old value (use temporaries).
2. Allowing buy-buy (holding two shares).

---

## Follow-ups

1. Cooldown after selling?
2. Fee per transaction?

<details><summary>Answer sketches</summary>

**#1:** A sell jumps to `i + 2` (LC 309).

**#2:** Subtract the fee on sell (LC 714).
</details>

---

## Flashcards

**Stock state machine state?** #flashcard
(day, canBuy) plus a transaction cap when limited.

**Stock II greedy?** #flashcard
Sum all positive consecutive differences.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
