---
module: striver/28-dynamic-programming
lesson: 16
topic: Best time to buy and sell stock III
difficulty: Hard
source: https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-iii?category=dp-on-stocks&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, stocks, state-machine]
---
# 16. Best time to buy and sell stock III

← [Best time to buy and sell stock II](15-best-time-to-buy-and-sell-stock-ii.md) · [Part 28 index](README.md) · Next → [Best time to buy and sell stock IV](17-best-time-to-buy-and-sell-stock-iv.md)

> [!abstract] Problem at a glance
> **Task:** At most **two** transactions. Maximise profit.
> **Key insight:** Add a transaction counter to the state: `(i, canBuy, capLeft)`. A transaction is consumed on **sell**, and `cap = 0` returns 0. Equivalently, four rolling variables (`buy1, sell1, buy2, sell2`) run forward in one pass.
> **Difficulty:** Hard · **Pattern:** Stock state machine with cap · **Also on:** LC 123
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-iii?category=dp-on-stocks&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized (i, canBuy, cap)](#3-memoized-i-canbuy-cap) · [4. Four forward variables](#4-four-forward-variables) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Find the maximum profit with at most two transactions (sell before buying again).

| Input | Output | Why |
|---|---|---|
| `[3,3,5,0,0,3,1,4]` | `6` | (3−0) + (4−1) |
| `[1,2,3,4,5]` | `4` | one transaction suffices |
| `[7,6,4,3,1]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ prices[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized (i, canBuy, cap) | cap decremented on sell | O(n·2·3) | O(n·2·3) |
| Four forward variables | buy1, sell1, buy2, sell2 | O(n) | O(1) |

> [!tip] Interview angle
> Present the 3D memo first, then show the four-variable forward version and explain each: `buy1` = best cash after the first buy, `sell1` = after the first sell, and so on. Each one feeds the next on the same day, which is safe because buying and selling on one day gains nothing.

---

## 3. Memoized (i, canBuy, cap)

**Intuition.** `f(i, buy, cap)`: `cap == 0` or `i == n` → 0. Buying: `max(−p + f(i+1, 0, cap), f(i+1, 1, cap))`. Selling: `max(p + f(i+1, 1, cap−1), f(i+1, 0, cap))`.

```python
def stock3_memo(p):
    n = len(p)
    dp = {}
    def f(i, buy, cap):
        if i == n or cap == 0:
            return 0
        key = (i, buy, cap)
        if key not in dp:
            if buy:
                dp[key] = max(-p[i] + f(i + 1, 0, cap), f(i + 1, 1, cap))
            else:
                dp[key] = max(p[i] + f(i + 1, 1, cap - 1), f(i + 1, 0, cap))
        return dp[key]
    return f(0, 1, 2)
```

**Complexity:** time **O(n·2·3)**, space **O(n·2·3)**.

---

## 4. Four forward variables

**Intuition.** `buy1 = max(buy1, −p)`, `sell1 = max(sell1, buy1 + p)`, `buy2 = max(buy2, sell1 − p)`, `sell2 = max(sell2, buy2 + p)`. `sell2` is the answer, since it is at least `sell1`.

**Algorithm**

1. `buy1 = buy2 = −∞`, `sell1 = sell2 = 0`.
2. For each price `x`: update `buy1, sell1, buy2, sell2` in that order.
3. Return `sell2`.

**Dry run** — [3,3,5,0,0,3,1,4]: after day 3 (price 0): buy1 = 0, sell1 = 2, buy2 = 2. Final: sell1 = 4, sell2 = 6.

**C++**
```cpp
int maxProfit(vector<int>& p) {
    int buy1 = INT_MIN, sell1 = 0, buy2 = INT_MIN, sell2 = 0;
    for (int x : p) {
        buy1 = max(buy1, -x);
        sell1 = max(sell1, buy1 + x);
        buy2 = max(buy2, sell1 - x);
        sell2 = max(sell2, buy2 + x);
    }
    return sell2;
}
```

**Java**
```java
static int maxProfit(int[] p) {
    int buy1 = Integer.MIN_VALUE, sell1 = 0, buy2 = Integer.MIN_VALUE, sell2 = 0;
    for (int x : p) {
        buy1 = Math.max(buy1, -x);
        sell1 = Math.max(sell1, buy1 + x);
        buy2 = Math.max(buy2, sell1 - x);
        sell2 = Math.max(sell2, buy2 + x);
    }
    return sell2;
}
```

**Python**
```python
def max_profit_iii(p):
    buy1 = buy2 = float("-inf")
    sell1 = sell2 = 0
    for x in p:
        buy1 = max(buy1, -x)
        sell1 = max(sell1, buy1 + x)
        buy2 = max(buy2, sell1 - x)
        sell2 = max(sell2, buy2 + x)
    return sell2
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, four states; `buy1` is set before `sell1` reads it, so `INT_MIN + x` never overflows.

---

## Edge cases

- Fewer than 2 profitable runs: the answer equals Stock I.
- One day: 0.

---

## Common mistakes

1. Decrementing the cap on buy **and** on sell.
2. Initialising `buy1` to 0 (that means a free share).

---

## Follow-ups

1. At most k transactions?
2. Prefix/suffix approach?

<details><summary>Answer sketches</summary>

**#1:** Next problem: arrays `buy[1..k]`, `sell[1..k]`, or the `(i, transactionNo)` 2D state.

**#2:** `left[i]` = best single trade in `[0..i]`, `right[i]` = best in `[i..n−1]`; answer `max(left[i] + right[i])`.
</details>

---

## Flashcards

**Stock III state?** #flashcard
(day, canBuy, capLeft ∈ {0,1,2}).

**Four-variable update order?** #flashcard
buy1 → sell1 → buy2 → sell2.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
