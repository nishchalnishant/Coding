---
module: striver-a2z/28-dynamic-programming
lesson: 14
topic: Best time to buy and sell stock
difficulty: Easy
source: https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock?category=dp-on-stocks&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, stocks, array]
---
# 14. Best time to buy and sell stock

← [Count Square Submatrices with All Ones](13-count-square-submatrices-with-all-ones.md) · [Part 28 index](README.md) · Next → [Best time to buy and sell stock II](15-best-time-to-buy-and-sell-stock-ii.md)

> [!abstract] Problem at a glance
> **Task:** Make at most one buy and a later sell to maximise profit.
> **Key insight:** If you sell on day `i`, the best buy is the minimum price before `i`. One pass tracking `minSoFar` gives `max(prices[i] − minSoFar)`. It is the simplest DP: the state is just "cheapest so far".
> **Difficulty:** Easy · **Pattern:** Running min (prefix DP) · **Also on:** LC 121
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/best-time-to-buy-and-sell-stock?category=dp-on-stocks&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All pairs](#3-all-pairs) · [4. Running minimum](#4-running-minimum) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`prices[i]` is the price on day `i`. Choose one day to buy and a later day to sell. Return the maximum profit, or 0 if no profit is possible.

| Input | Output | Why |
|---|---|---|
| `[7,1,5,3,6,4]` | `5` | buy at 1, sell at 6 |
| `[7,6,4,3,1]` | `0` | prices only fall |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ prices[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All pairs | try every (buy, sell) | O(n²) | O(1) |
| Running minimum | profit = price − min so far | O(n) | O(1) |

> [!tip] Interview angle
> State the invariant: "`mini` is the cheapest price strictly before today." Update the profit before updating `mini`, or update `mini` first; both work here because selling the same day gives 0.

---

## 3. All pairs

**Intuition.** Check every `i < j` and keep the largest `prices[j] − prices[i]`.

```python
def stock1_brute(p):
    best = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            best = max(best, p[j] - p[i])
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Running minimum

**Intuition.** Scan once. For each day, the best sale today is `price − mini`, then fold today into `mini`.

**Algorithm**

1. `mini = prices[0]`, `best = 0`.
2. For each later price `x`: `best = max(best, x − mini)`; `mini = min(mini, x)`.
3. Return `best`.

**Dry run** — [7,1,5,3,6,4]: mini 7→1; profits 0, 4, 2, 5, 3 → 5.

**C++**
```cpp
int maxProfit(vector<int>& p) {
    int mini = p[0], best = 0;
    for (int x : p) {
        best = max(best, x - mini);
        mini = min(mini, x);
    }
    return best;
}
```

**Java**
```java
static int maxProfit(int[] p) {
    int mini = p[0], best = 0;
    for (int x : p) {
        best = Math.max(best, x - mini);
        mini = Math.min(mini, x);
    }
    return best;
}
```

**Python**
```python
def max_profit(p):
    mini, best = p[0], 0
    for x in p:
        best = max(best, x - mini)
        mini = min(mini, x)
    return best
```

**Complexity:** time **O(n)**, space **O(1)** — single pass, two variables.

---

## Edge cases

- One day: 0.
- Strictly decreasing prices: 0.
- Minimum on the last day: never used as a buy.

---

## Common mistakes

1. Returning `max − min` overall (the max may come before the min).
2. Returning a negative profit instead of 0.

---

## Follow-ups

1. Return the days.
2. Kadane connection?

<details><summary>Answer sketches</summary>

**#1:** Store the index of `mini` when it updates and the pair when `best` improves.

**#2:** The profit equals the max subarray sum of daily differences `p[i] − p[i−1]`.
</details>

---

## Flashcards

**Stock I one-liner?** #flashcard
`best = max(best, x − minSoFar)`.

**Stock I as Kadane?** #flashcard
Max subarray of consecutive differences.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
