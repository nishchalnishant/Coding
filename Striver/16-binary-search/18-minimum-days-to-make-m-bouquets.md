---
module: striver/16-binary-search
lesson: 18
topic: Minimum Days to Make M Bouquets
difficulty: Medium
source: https://takeuforward.org/learning/dsa/minimum-days-to-make-m-bouquets?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer]
---
# 18. Minimum Days to Make M Bouquets

← [Koko Eating Bananas](17-koko-eating-bananas.md) · [Part 16 index](README.md) · Next → [Capacity to Ship Packages Within D Days](19-ship-within-days.md)

> [!abstract] Problem at a glance
> **Task:** Each bouquet needs `k` adjacent bloomed flowers; flower `i` blooms on `bloomDay[i]`. Return the minimum day to make `m` bouquets, or −1.
> **Key insight:** By day `d` the bloomed set only grows, so `bouquets(d)` is non-decreasing. Binary search `d ∈ [min, max]` of bloomDay; check counts runs of consecutive bloomed flowers, adding `run / k`.
> **Difficulty:** Medium · **Pattern:** Binary search on answer — min feasible · **Also on:** [LC 1482](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimum-days-to-make-m-bouquets?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every distinct day](#3-try-every-distinct-day) · [4. Binary search on day](#4-binary-search-on-day) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `bloomDay` (length `n`), and integers `m` and `k`: to make a bouquet you need `k` **adjacent** flowers, each used in at most one bouquet. Return the minimum number of days to wait to make `m` bouquets, or `-1` if impossible.

| Input | Output | Why |
|---|---|---|
| `bloomDay = [1, 10, 3, 10, 2], m = 3, k = 1` | `3` |  |
| `bloomDay = [1, 10, 3, 10, 2], m = 3, k = 2` | `-1` | need 6 flowers, have 5 |
| `bloomDay = [7, 7, 7, 7, 12, 7, 7], m = 2, k = 3` | `12` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ bloomDay[i] ≤ 10⁹`, `1 ≤ m ≤ 10⁶`, `1 ≤ k ≤ n`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every distinct day | sorted unique bloom days, first feasible | O(n²) | O(n) |
| Binary search on day | impossible if m·k > n; else first d in [min, max] with bouquets(d) ≥ m | O(n log(max − min)) | O(1) |

---

## 3. Try every distinct day

**Intuition.** The answer is always one of the bloom days. Check each in increasing order.

```python
def min_days_linear(bloom, m, k):
    if m * k > len(bloom):
        return -1
    for d in sorted(set(bloom)):
        run = cnt = 0
        for b in bloom:
            run = run + 1 if b <= d else 0
            if run == k:
                cnt, run = cnt + 1, 0
        if cnt >= m:
            return d
    return -1
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Binary search on day

**Intuition.** Quick reject: if `m · k > n` there aren't enough flowers. Otherwise day `max(bloomDay)` always works. The check walks the array keeping the length of the current bloomed run; every time it reaches `k`, count a bouquet and reset.

**Dry run** — `[7 7 7 7 12 7 7]`, m 2, k 3: lo 7 hi 12. mid 9: runs 4 | 2 → 1 bouquet ✗ → lo 10. mid 11 ✗ → lo 12. mid 12: run of 7 → 2 bouquets ✓ → 12.

**Overflow:** `m · k` can reach 10¹¹ — compute in 64-bit.

**C++**
```cpp
int minDays(vector<int>& bloomDay, int m, int k) {
    int n = bloomDay.size();
    if ((long long)m * k > n) return -1;
    int lo = *min_element(bloomDay.begin(), bloomDay.end());
    int hi = *max_element(bloomDay.begin(), bloomDay.end()), ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, run = 0, cnt = 0;
        for (int b : bloomDay) {
            run = b <= mid ? run + 1 : 0;
            if (run == k) { cnt++; run = 0; }
        }
        if (cnt >= m) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Java**
```java
static int minDays(int[] bloomDay, int m, int k) {
    int n = bloomDay.length;
    if ((long) m * k > n) return -1;
    int lo = Integer.MAX_VALUE, hi = 0;
    for (int b : bloomDay) { lo = Math.min(lo, b); hi = Math.max(hi, b); }
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2, run = 0, cnt = 0;
        for (int b : bloomDay) {
            run = b <= mid ? run + 1 : 0;
            if (run == k) { cnt++; run = 0; }
        }
        if (cnt >= m) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return ans;
}
```

**Python**
```python
def min_days(bloom_day, m, k):
    if m * k > len(bloom_day):
        return -1
    def bouquets(d):
        run = cnt = 0
        for b in bloom_day:
            run = run + 1 if b <= d else 0
            if run == k:
                cnt, run = cnt + 1, 0
        return cnt
    lo, hi = min(bloom_day), max(bloom_day)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if bouquets(mid) >= m:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(n log(max − min))**, space **O(1)** — log(range) checks of O(n).

---

## Edge cases

- m · k > n → −1 immediately.
- k = 1 → m-th smallest bloom day.

---

## Common mistakes

1. Not resetting `run` after forming a bouquet (flowers reused).
2. `m * k` overflow.
3. Counting total bloomed flowers instead of adjacent runs.

---

## Follow-ups

1. Flowers needn't be adjacent.
2. Return which flowers form the bouquets.

<details><summary>Answer sketches</summary>

**#1:** Answer = (m·k)-th smallest bloom day — quickselect, no binary search.

**#2:** Re-run the check at the answer day and record run endpoints.
</details>

---

## Flashcards

**m bouquets — check(d)?** #flashcard
Count runs of bloomed flowers; each k-run gives a bouquet, reset after.

**m bouquets — instant −1?** #flashcard
m · k > n (64-bit).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
