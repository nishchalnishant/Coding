---
module: striver/28-dynamic-programming
lesson: 19
topic: Best time to buy and sell stock with cooldown
difficulty: Medium
source: https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-with-cooldown?category=dp-on-stocks&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, stocks, state-machine]
---
# 19. Best time to buy and sell stock with cooldown

← [Best time to buy and sell stock with transaction fees](18-best-time-to-buy-and-sell-stock-with-transaction-fee.md) · [Part 28 index](README.md) · Next → [Subset sum equals to target](20-subset-sum-equals-to-target.md)

> [!abstract] Problem at a glance
> **Task:** Unlimited transactions, but after a sale you must wait one day before buying.
> **Key insight:** In the backward state machine, selling on day `i` jumps to `f(i + 2, canBuy)` instead of `f(i + 1, …)`. In the tabulated version you therefore need `ahead` **and** `ahead2` rows, i.e. one more rolling variable.
> **Difficulty:** Medium · **Pattern:** Stock state machine with cooldown · **Also on:** LC 309
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-with-cooldown?category=dp-on-stocks&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized state machine](#3-memoized-state-machine) · [4. Backward tabulation with two look-ahead rows](#4-backward-tabulation-with-two-look-ahead-rows) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Find the maximum profit with unlimited transactions where, after selling, you cannot buy on the next day.

| Input | Output | Why |
|---|---|---|
| `[1,2,3,0,2]` | `3` | buy, sell, cooldown, buy, sell |
| `[1]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 5000`, `0 ≤ prices[i] ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized state machine | sell → f(i+2, 1) | O(n) | O(n) |
| Backward tabulation with two look-ahead rows | front1, front2 | O(n) | O(1) |

> [!tip] Interview angle
> Show the one-line change from Stock II (`i + 1 → i + 2` on sell). Mention the alternative three-state forward machine (`hold`, `sold`, `rest`), which some interviewers prefer.

---

## 3. Memoized state machine

**Intuition.** Same as Stock II, but the sale skips the next day. `f(i ≥ n) = 0`.

```python
def cool_memo(p):
    n = len(p)
    dp = {}
    def f(i, can_buy):
        if i >= n:
            return 0
        if (i, can_buy) not in dp:
            if can_buy:
                dp[(i, can_buy)] = max(-p[i] + f(i + 1, 0), f(i + 1, 1))
            else:
                dp[(i, can_buy)] = max(p[i] + f(i + 2, 1), f(i + 1, 0))
        return dp[(i, can_buy)]
    return f(0, 1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Backward tabulation with two look-ahead rows

**Intuition.** Track `front1Buy, front1Sell` (day i+1) and `front2Buy` (day i+2). Sell reads `front2Buy`.

**Algorithm**

1. All zeros (days n and n+1).
2. For `i = n−1..0`: `curBuy = max(−p + front1Sell, front1Buy)`; `curSell = max(p + front2Buy, front1Sell)`.
3. `front2Buy = front1Buy`; `front1 = cur`. Return `front1Buy`.

**Dry run** — [1,2,3,0,2] → 3.

**C++**
```cpp
int maxProfit(vector<int>& p) {
    int f1Buy = 0, f1Sell = 0, f2Buy = 0;
    for (int i = (int)p.size() - 1; i >= 0; i--) {
        int curBuy = max(-p[i] + f1Sell, f1Buy);
        int curSell = max(p[i] + f2Buy, f1Sell);
        f2Buy = f1Buy;
        f1Buy = curBuy;
        f1Sell = curSell;
    }
    return f1Buy;
}
```

**Java**
```java
static int maxProfit(int[] p) {
    int f1Buy = 0, f1Sell = 0, f2Buy = 0;
    for (int i = p.length - 1; i >= 0; i--) {
        int curBuy = Math.max(-p[i] + f1Sell, f1Buy);
        int curSell = Math.max(p[i] + f2Buy, f1Sell);
        f2Buy = f1Buy;
        f1Buy = curBuy;
        f1Sell = curSell;
    }
    return f1Buy;
}
```

**Python**
```python
def max_profit_cooldown(p):
    f1_buy = f1_sell = f2_buy = 0
    for x in reversed(p):
        cur_buy = max(-x + f1_sell, f1_buy)
        cur_sell = max(x + f2_buy, f1_sell)
        f2_buy, f1_buy, f1_sell = f1_buy, cur_buy, cur_sell
    return f1_buy
```

**Complexity:** time **O(n)**, space **O(1)** — O(1) rolling look-ahead of two days.

---

## Edge cases

- One day: 0.
- Selling on the last day: `i + 2` is past the end, which returns 0.

---

## Common mistakes

1. Applying the cooldown after a buy instead of after a sell.
2. Losing `front2Buy` by shifting in the wrong order.

---

## Follow-ups

1. Cooldown of `c` days?
2. Three-state forward form?

<details><summary>Answer sketches</summary>

**#1:** Sell jumps to `i + c + 1`; keep `c + 1` look-ahead values.

**#2:** `hold = max(hold, rest − p)`, `sold = hold + p`, `rest = max(rest, sold_prev)`.
</details>

---

## Flashcards

**Cooldown change vs Stock II?** #flashcard
Sell transitions to `i + 2`.

**Space for cooldown tabulation?** #flashcard
Two look-ahead days → 3 rolling variables.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
