---
module: striver/21-greedy-algorithms
lesson: 16
topic: Minimum coins (greedy, canonical denominations)
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-minimum-number-of-coins?category=easy&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, easy]
---
# 16. Minimum coins (greedy, canonical denominations)

← [Jump Game II](15-jump-game-ii.md) · [Part 21 index](README.md) · Next → [Part 22: Sliding Window / 2 Pointer](../22-sliding-window-and-2-pointer/README.md)

> [!abstract] Problem at a glance
> **Task:** Using Indian currency {1, 2, 5, 10, 20, 50, 100, 500, 1000}, return the coins making `V` with the fewest coins.
> **Key insight:** For **canonical** coin systems like real currencies, always taking the largest coin `≤` the remaining amount is optimal. Greedy is **not** optimal for arbitrary denominations: with {1, 3, 4} and V = 6, greedy gives 4 + 1 + 1, but 3 + 3 is better. In that case use DP (coin change, Part 28). Always state the condition before using greedy.
> **Difficulty:** Easy · **Pattern:** Greedy — largest first · **Also on:** [GfG — Minimum number of coins](https://www.geeksforgeeks.org/problems/-minimum-number-of-coins4426/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-minimum-number-of-coins?category=easy&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Greedy, repeated subtraction](#3-greedy-repeated-subtraction) · [4. Greedy with division](#4-greedy-with-division) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a value `V` and an unlimited supply of coins/notes {1, 2, 5, 10, 20, 50, 100, 500, 1000}, return the list of denominations (largest first) using the minimum number of coins that sum to `V`.

| Input | Output | Why |
|---|---|---|
| `V = 49` | `[20, 20, 5, 2, 2]` |  |
| `V = 121` | `[100, 20, 1]` |  |
| `V = 0` | `[]` |  |

**Constraints:** `0 ≤ V ≤ 10⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Greedy, repeated subtraction | for each coin desc: while V ≥ c take c | O(V/min + k) | O(answer) |
| Greedy with division | take V // c copies of each coin | O(k + answer) | O(answer) |

> [!tip] Interview angle
> Give the greedy answer immediately, then say *why* it is only correct here: the denomination system is canonical. Offer the {1, 3, 4} counterexample unprompted, and name DP coin change as the general solution, O(V · k). A strong extra point: you can check whether a system is canonical by comparing greedy and DP for every amount below the sum of the two largest coins.

---

## 3. Greedy, repeated subtraction

**Intuition.** Scan denominations from largest to smallest and subtract while possible.

```python
def min_coins_loop(v):
    res = []
    for c in [1000, 500, 100, 50, 20, 10, 5, 2, 1]:
        while v >= c:
            res.append(c)
            v -= c
    return res
```

**Complexity:** time **O(V/min + k)**, space **O(answer)**.

---

## 4. Greedy with division

**Intuition.** The number of copies of coin `c` is `V / c`. Then `V %= c`.

**Algorithm**

1. Denominations in descending order.
2. For each `c`: append `V / c` copies, `V %= c`.
3. Return the list.

**Dry run** — V = 49: 1000/500/100/50 → 0; 20 → 2 copies, V = 9; 10 → 0; 5 → 1, V = 4; 2 → 2, V = 0. Result [20, 20, 5, 2, 2].

**C++**
```cpp
vector<int> minCoins(int v) {
    int d[] = {1000, 500, 100, 50, 20, 10, 5, 2, 1};
    vector<int> res;
    for (int c : d) {
        for (int k = v / c; k > 0; k--) res.push_back(c);
        v %= c;
    }
    return res;
}
```

**Java**
```java
static List<Integer> minCoins(int v) {
    int[] d = {1000, 500, 100, 50, 20, 10, 5, 2, 1};
    List<Integer> res = new ArrayList<>();
    for (int c : d) {
        for (int k = v / c; k > 0; k--) res.add(c);
        v %= c;
    }
    return res;
}
```

**Python**
```python
def min_coins(v):
    res = []
    for c in [1000, 500, 100, 50, 20, 10, 5, 2, 1]:
        res += [c] * (v // c)
        v %= c
    return res
```

**Complexity:** time **O(k + answer)**, space **O(answer)** — Exchange argument for this system: an optimal solution uses at most 1 one, 2 twos, 1 five, and so on, because otherwise a group of them could be swapped for fewer larger coins. Those bounds force exactly the greedy choice at each step.

---

## Edge cases

- V = 0 → empty.
- V equal to one denomination.
- Large V (many 1000s).

---

## Common mistakes

1. Using greedy on non-canonical coin sets (e.g. {1, 3, 4}).
2. Iterating denominations in ascending order.
3. Returning the count when the list is asked for, or the other way round.

---

## Follow-ups

1. Arbitrary denominations?
2. Limited supply of each coin?

<details><summary>Answer sketches</summary>

**#1:** DP coin change: dp[v] = 1 + min dp[v − c], O(V·k) (Part 28).

**#2:** Bounded knapsack DP; greedy breaks.
</details>

---

## Flashcards

**When is greedy coin change optimal?** #flashcard
Only for canonical systems (real currencies). Counterexample {1,3,4}, V=6.

**General coin change?** #flashcard
DP O(V·k).

**Interview track →** 
