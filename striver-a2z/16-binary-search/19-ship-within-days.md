---
module: striver-a2z/16-binary-search
lesson: 19
topic: Capacity to Ship Packages Within D Days
difficulty: Medium
source: https://takeuforward.org/learning/dsa/capacity-to-ship-packages-within-d-days?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, greedy]
---
# 19. Capacity to Ship Packages Within D Days

← [Minimum Days to Make M Bouquets](18-minimum-days-to-make-m-bouquets.md) · [Part 16 index](README.md) · Next → [Kth Missing Positive Number](20-kth-missing-positive-number.md)

> [!abstract] Problem at a glance
> **Task:** Packages must ship in order; find the least ship capacity that ships them all in `days` days.
> **Key insight:** Range `[max(w), Σw]`: below max a package never fits, at Σw it all ships in one day. Check = greedy: fill the current day until the next package overflows, then start a new day. Days needed is non-increasing in capacity.
> **Difficulty:** Medium · **Pattern:** Binary search on answer + greedy partition · **Also on:** [LC 1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/capacity-to-ship-packages-within-d-days?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every capacity](#3-try-every-capacity) · [4. Binary search on capacity](#4-binary-search-on-capacity) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `weights` of packages that must be shipped **in the given order** and an integer `days`, return the least ship capacity such that all packages ship within `days` days. Each day the ship loads a contiguous run of the remaining packages whose total weight ≤ capacity.

| Input | Output | Why |
|---|---|---|
| `weights = [1..10], days = 5` | `15` | [1-5] [6,7] [8] [9] [10] |
| `weights = [3, 2, 2, 4, 1, 4], days = 3` | `6` | [3,2] [2,4] [1,4] |
| `weights = [1, 2, 3, 1, 1], days = 4` | `3` |  |

**Constraints:** `1 ≤ days ≤ n ≤ 5·10⁴`, `1 ≤ weights[i] ≤ 500`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every capacity | cap = max … sum, first feasible | O(n · (Σ − max)) | O(1) |
| Binary search on capacity | days_needed(cap) ≤ days → go left; greedy check | O(n log Σw) | O(1) |

> [!tip] Interview angle
> This is the "split a sequence into ≤ k contiguous parts minimising the maximum part" pattern — the same code solves Book Allocation, Painter's Partition and Split Array Largest Sum (all later in this part). Learn it once.

---

## 3. Try every capacity

**Intuition.** Linear version of the same check.

```python
def ship_linear(weights, days):
    for cap in range(max(weights), sum(weights) + 1):
        d, load = 1, 0
        for w in weights:
            if load + w > cap:
                d, load = d + 1, 0
            load += w
        if d <= days:
            return cap
```

**Complexity:** time **O(n · (Σ − max))**, space **O(1)**.

---

## 4. Binary search on capacity

**Intuition.** **Why greedy is optimal for the check:** loading as much as possible on each day never hurts — any valid schedule can be shifted so earlier days are fuller without adding days. So `days_needed(cap)` is exact, and it only decreases as `cap` grows.

**Dry run** — `[3 2 2 4 1 4]`, days 3: lo 4 hi 16 mid 10 → [3 2 2] [4 1 4] = 2 ✓ hi 9; mid 6 → [3 2] [2 4] [1 4] = 3 ✓ hi 5; mid 4 → [3] [2 2] [4] [1] [4] = 5 ✗ lo 5; mid 5 → [3 2] [2] [4 1] [4] = 4 ✗ lo 6 → 6.

**C++**
```cpp
int shipWithinDays(vector<int>& weights, int days) {
    int lo = 0, hi = 0;
    for (int w : weights) { lo = max(lo, w); hi += w; }
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, d = 1, load = 0;
        for (int w : weights) {
            if (load + w > mid) { d++; load = 0; }
            load += w;
        }
        if (d <= days) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int shipWithinDays(int[] weights, int days) {
    int lo = 0, hi = 0;
    for (int w : weights) { lo = Math.max(lo, w); hi += w; }
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, d = 1, load = 0;
        for (int w : weights) {
            if (load + w > mid) { d++; load = 0; }
            load += w;
        }
        if (d <= days) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def ship_within_days(weights, days):
    def need(cap):
        d, load = 1, 0
        for w in weights:
            if load + w > cap:
                d, load = d + 1, 0
            load += w
        return d
    lo, hi = max(weights), sum(weights)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if need(mid) <= days:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(n log Σw)**, space **O(1)** — log(Σ) checks of O(n).

---

## Edge cases

- days = n → max(weights).
- days = 1 → Σ weights.

---

## Common mistakes

1. Lower bound 1 instead of max(weights) — the check then loops forever or miscounts (a package heavier than cap never fits).
2. Starting `d = 0` instead of 1.

---

## Follow-ups

1. Order doesn't matter.
2. Output the split points.

<details><summary>Answer sketches</summary>

**#1:** Becomes bin packing — NP-hard; no binary search shortcut.

**#2:** Run the greedy at the answer capacity and record where days break.
</details>

---

## Flashcards

**Ship packages — search range?** #flashcard
[max(w), Σw].

**Ship packages — check?** #flashcard
Greedy fill each day; count days ≤ D.

**Same template solves…** #flashcard
Book allocation, painter's partition, split array largest sum.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
