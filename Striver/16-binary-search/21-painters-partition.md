---
module: striver/16-binary-search
lesson: 21
topic: Painter's Partition
difficulty: Hard
source: https://takeuforward.org/learning/dsa/painters-partition?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, greedy]
---
# 21. Painter's Partition

← [Kth Missing Positive Number](20-kth-missing-positive-number.md) · [Part 16 index](README.md) · Next → [Aggressive Cows](22-aggressive-cows.md)

> [!abstract] Problem at a glance
> **Task:** Split boards (in order) among `k` painters, each taking a contiguous block; minimise the maximum block sum.
> **Key insight:** Same as shipping packages with `days = k`: binary search the max load in `[max, Σ]`, greedy-count painters needed.
> **Difficulty:** Hard · **Pattern:** Binary search on answer + greedy partition
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/painters-partition?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Linear over max load](#3-linear-over-max-load) · [4. Binary search on max load](#4-binary-search-on-max-load) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given board lengths `boards` and `k` painters (each paints 1 unit per unit time, all start together), each painter paints a **contiguous** set of boards. Return the minimum time to paint all boards — i.e. the minimum possible largest block sum.

| Input | Output | Why |
|---|---|---|
| `boards = [10, 20, 30, 40], k = 2` | `60` | [10 20 30] [40] |
| `boards = [5, 5, 5, 5], k = 2` | `10` |  |
| `boards = [10, 20, 30, 40], k = 1` | `100` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ boards[i] ≤ 10⁵`, `1 ≤ k ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Linear over max load | load = max … Σ, first feasible | O(n · (Σ − max)) | O(1) |
| Binary search on max load | painters_needed(cap) ≤ k → go left | O(n log Σ) | O(1) |

> [!tip] Interview angle
> When asked, say immediately: "This is split-array-largest-sum." If `k > n`, extra painters idle — the answer is `max(boards)`, which the binary search returns naturally since the greedy uses ≤ n painters.

---

## 3. Linear over max load

**Intuition.** Same greedy check, scanned upward.

```python
def painters_linear(boards, k):
    for cap in range(max(boards), sum(boards) + 1):
        p, cur = 1, 0
        for b in boards:
            if cur + b > cap:
                p, cur = p + 1, 0
            cur += b
        if p <= k:
            return cap
```

**Complexity:** time **O(n · (Σ − max))**, space **O(1)**.

---

## 4. Binary search on max load

**Intuition.** Exactly `shipWithinDays` with days → painters. Use 64-bit sums (Σ ≤ 10¹⁰).

**C++**
```cpp
long long paintersPartition(vector<int>& boards, int k) {
    long long lo = 0, hi = 0;
    for (int b : boards) { lo = max(lo, (long long)b); hi += b; }
    long long ans = hi;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2, cur = 0;
        int p = 1;
        for (int b : boards) {
            if (cur + b > mid) { p++; cur = 0; }
            cur += b;
        }
        if (p <= k) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static long paintersPartition(int[] boards, int k) {
    long lo = 0, hi = 0;
    for (int b : boards) { lo = Math.max(lo, b); hi += b; }
    long ans = hi;
    while (lo <= hi) {
        long mid = lo + (hi - lo) / 2, cur = 0;
        int p = 1;
        for (int b : boards) {
            if (cur + b > mid) { p++; cur = 0; }
            cur += b;
        }
        if (p <= k) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def painters_partition(boards, k):
    def need(cap):
        p, cur = 1, 0
        for b in boards:
            if cur + b > cap:
                p, cur = p + 1, 0
            cur += b
        return p
    lo, hi = max(boards), sum(boards)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if need(mid) <= k:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(n log Σ)**, space **O(1)** — log(Σ) greedy checks.

---

## Edge cases

- k ≥ n → max(boards).
- k = 1 → Σ boards.

---

## Common mistakes

1. 32-bit sums.
2. Lower bound below max(boards).

---

## Follow-ups

1. Each painter takes t time per unit.
2. Non-contiguous allowed.

<details><summary>Answer sketches</summary>

**#1:** Multiply the answer by t (mod if required).

**#2:** Multiprocessor scheduling — NP-hard; LPT greedy is a 4/3 approximation.
</details>

---

## Flashcards

**Painter's partition = ?** #flashcard
Split array largest sum / ship within days with k parts.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
