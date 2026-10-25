---
module: striver-a2z/28-dynamic-programming
lesson: 18
topic: Best time to buy and sell stock with transaction fees
difficulty: Medium
source: https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-with-cooldown-and-transaction-fees?category=dp-on-stocks&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, stocks, state-machine]
---
# 18. Best time to buy and sell stock with transaction fees

← [Best time to buy and sell stock IV](17-best-time-to-buy-and-sell-stock-iv.md) · [Part 28 index](README.md) · Next → [Best time to buy and sell stock with cooldown](19-best-time-to-buy-and-sell-stock-with-cooldown.md)

> [!abstract] Problem at a glance
> **Task:** Unlimited transactions, but each sale costs `fee`. Maximise profit.
> **Key insight:** This is the Stock II state machine with `−fee` on the sell transition (or on buy, not both). Fees break the "sum of rises" greedy, because many small trades now cost more than one long hold.
> **Difficulty:** Medium · **Pattern:** Stock state machine with fee · **Also on:** LC 714
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock-with-cooldown-and-transaction-fees?category=dp-on-stocks&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized state machine](#3-memoized-state-machine) · [4. Forward hold / cash](#4-forward-hold--cash) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `prices` and a non-negative `fee`, return the maximum profit with unlimited non-overlapping transactions when every completed transaction pays `fee`.

| Input | Output | Why |
|---|---|---|
| `prices = [1,3,2,8,4,9], fee = 2` | `8` | (8−1−2) + (9−4−2) |
| `prices = [1,3,7,5,10,3], fee = 3` | `6` | (10−1−3) |

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `1 ≤ prices[i] < 5·10⁴`, `0 ≤ fee < 5·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized state machine | sell: +p − fee | O(n) | O(n) |
| Forward hold / cash | cash = max(cash, hold + p − fee) | O(n) | O(1) |

> [!tip] Interview angle
> Say that the fee is charged once per transaction: "I'll subtract it at sell time." This is a one-line change to Stock II, which is the point of learning the state machine.

---

## 3. Memoized state machine

**Intuition.** `f(i, canBuy)` as Stock II, with `p[i] − fee` on a sell.

```python
def fee_memo(p, fee):
    n = len(p)
    dp = [[None, None] for _ in range(n)]
    def f(i, can_buy):
        if i == n:
            return 0
        if dp[i][can_buy] is None:
            if can_buy:
                dp[i][can_buy] = max(-p[i] + f(i + 1, 0), f(i + 1, 1))
            else:
                dp[i][can_buy] = max(p[i] - fee + f(i + 1, 1), f(i + 1, 0))
        return dp[i][can_buy]
    return f(0, 1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Forward hold / cash

**Intuition.** `hold` = best balance while owning a share, `cash` = best balance without one.

**Algorithm**

1. `hold = −p[0]`, `cash = 0`.
2. For each `x`: `cash = max(cash, hold + x − fee)`; `hold = max(hold, cash − x)`.
3. Return `cash`.

**Dry run** — [1,3,2,8,4,9], fee 2: cash 0,0,0,5,5,8; hold −1,−1,−1,−1,1,1 → 8.

**C++**
```cpp
int maxProfit(vector<int>& p, int fee) {
    int hold = -p[0], cash = 0;
    for (int x : p) {
        cash = max(cash, hold + x - fee);
        hold = max(hold, cash - x);
    }
    return cash;
}
```

**Java**
```java
static int maxProfit(int[] p, int fee) {
    int hold = -p[0], cash = 0;
    for (int x : p) {
        cash = Math.max(cash, hold + x - fee);
        hold = Math.max(hold, cash - x);
    }
    return cash;
}
```

**Python**
```python
def max_profit_fee(p, fee):
    hold, cash = -p[0], 0
    for x in p:
        cash = max(cash, hold + x - fee)
        hold = max(hold, cash - x)
    return cash
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, two states.

---

## Edge cases

- `fee = 0`: same as Stock II.
- Fee larger than every rise: 0.

---

## Common mistakes

1. Charging the fee on both buy and sell.
2. Applying the Stock II greedy.

---

## Follow-ups

1. Fee and cooldown together?
2. Fee as a percentage?

<details><summary>Answer sketches</summary>

**#1:** Sell jumps to `i + 2` and subtracts the fee.

**#2:** Multiply instead of subtract; the same state machine.
</details>

---

## Flashcards

**Stock with fee change vs Stock II?** #flashcard
Subtract the fee on the sell transition.

**hold / cash update?** #flashcard
`cash = max(cash, hold + p − fee)`, `hold = max(hold, cash − p)`.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
