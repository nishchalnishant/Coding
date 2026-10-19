---
module: striver/21-greedy-algorithms
lesson: 3
topic: Lemonade Change
difficulty: Easy
source: https://takeuforward.org/learning/dsa/lemonade-change?category=easy&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, simulation]
---
# 3. Lemonade Change

← [Assign Cookies](02-assign-cookies.md) · [Part 21 index](README.md) · Next → [Fractional Knapsack](04-fractional-knapsack.md)

> [!abstract] Problem at a glance
> **Task:** Customers pay $5, $10 or $20 for a $5 lemonade in order; starting with no money, can you always give correct change?
> **Key insight:** Only $5 and $10 bills are useful as change. For $20, prefer giving $10 + $5 over $5 × 3, because $5 bills are strictly more flexible (they're needed for $10 customers too).
> **Difficulty:** Easy · **Pattern:** Greedy with counters (keep the most flexible resource) · **Also on:** [LC 860](https://leetcode.com/problems/lemonade-change/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/lemonade-change?category=easy&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Counters with greedy change](#3-counters-with-greedy-change) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Each lemonade costs $5. Customers queue and pay one bill each from `bills` (5, 10 or 20). You start with no change. Return `true` if you can give every customer correct change.

| Input | Output | Why |
|---|---|---|
| `bills = [5,5,5,10,20]` | `true` | 20 → 10 + 5 |
| `bills = [5,5,10,10,20]` | `false` | no 5 left after two 10s… for the 20 |

**Constraints:** `1 ≤ bills.length ≤ 10⁵`, `bills[i] ∈ {5, 10, 20}`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Counters with greedy change | track #5 and #10; for 20 use 10+5 first | O(n) | O(1) |

> [!tip] Interview angle
> A simulation question with one real decision. State why `10 + 5` is the right change for 20: it preserves $5s, which every change-giving case needs.

---

## 3. Counters with greedy change

**Intuition.** Keep counts of $5 and $10 (a $20 is never usable as change). On 5: `five++`. On 10: need one 5. On 20: use `10 + 5` if possible, else `5 + 5 + 5`, else fail.

**Dry run** — [5,5,10,10,20]: five=2 → 10: five=1,ten=1 → 10: five=0,ten=2 → 20: need 10+5 but five=0, 5×3 impossible → false.

**C++**
```cpp
bool lemonadeChange(vector<int>& bills) {
    int five = 0, ten = 0;
    for (int b : bills) {
        if (b == 5) five++;
        else if (b == 10) {
            if (!five) return false;
            five--; ten++;
        } else {
            if (ten && five) { ten--; five--; }
            else if (five >= 3) five -= 3;
            else return false;
        }
    }
    return true;
}
```

**Java**
```java
static boolean lemonadeChange(int[] bills) {
    int five = 0, ten = 0;
    for (int b : bills) {
        if (b == 5) five++;
        else if (b == 10) {
            if (five == 0) return false;
            five--; ten++;
        } else {
            if (ten > 0 && five > 0) { ten--; five--; }
            else if (five >= 3) five -= 3;
            else return false;
        }
    }
    return true;
}
```

**Python**
```python
def lemonade_change(bills):
    five = ten = 0
    for b in bills:
        if b == 5:
            five += 1
        elif b == 10:
            if not five:
                return False
            five -= 1; ten += 1
        else:
            if ten and five:
                ten -= 1; five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, two counters.

---

## Edge cases

- First customer pays 10 or 20 → false immediately.
- Only $5 bills → true.

---

## Common mistakes

1. Giving 5 + 5 + 5 for 20 before trying 10 + 5.
2. Counting $20 bills as usable change.
3. Not checking `five ≥ 1` along with `ten ≥ 1`.

---

## Follow-ups

1. Arbitrary denominations.
2. Customers can be reordered.

<details><summary>Answer sketches</summary>

**#1:** Greedy change-making isn't always optimal for arbitrary coin systems (e.g. {1, 3, 4} for 6); use DP.

**#2:** Serve all $5 customers first, then $10, then $20 — maximises available change.
</details>

---

## Flashcards

**Lemonade Change: change for $20?** #flashcard
Prefer $10 + $5; fall back to 3 × $5 — keeps the flexible $5s.

**Why are $20s never tracked?** #flashcard
No price makes a $20 usable as change.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../coding/algorithms/16-greedy.md)
