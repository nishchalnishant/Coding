---
module: striver-a2z/16-binary-search
lesson: 27
topic: Minimize Max Distance to Gas Station
difficulty: Hard
source: https://takeuforward.org/learning/dsa/minimise-max-distance-to-gas-stations?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, heap]
---
# 27. Minimize Max Distance to Gas Station

← [Kth Element of 2 Sorted Arrays](26-kth-element-of-two-sorted-arrays.md) · [Part 16 index](README.md) · Next → [Split Array — Largest Sum](28-split-array-largest-sum.md)

> [!abstract] Problem at a glance
> **Task:** Add `k` new stations anywhere on the line to minimise the largest gap between adjacent stations. Return that gap (real number).
> **Key insight:** Binary search on a **real** answer `d`: a gap `g` needs `⌈g / d⌉ − 1` new stations to bring every piece ≤ d. Total needed is non-increasing in `d`. Iterate a fixed number of times (≈100) instead of comparing with an epsilon.
> **Difficulty:** Hard · **Pattern:** Binary search on real-valued answer · **Also on:** [LC 774](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) (premium)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/minimise-max-distance-to-gas-stations?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Max-heap of piece lengths](#3-max-heap-of-piece-lengths) · [4. Binary search on the answer (reals)](#4-binary-search-on-the-answer-reals) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given sorted positions `arr` of `n` gas stations and an integer `k`, add `k` new stations at any real positions. Return the smallest possible value of the maximum distance between adjacent stations. Answers within 10⁻⁶ are accepted.

| Input | Output | Why |
|---|---|---|
| `arr = [1, 2, 3, 4, 5], k = 4` | `0.5` | one station in each gap |
| `arr = [1, 13, 17, 23], k = 5` | `3.0` | 3 in the 12-gap, 1 in the 4-gap, 1 in the 6-gap |

**Constraints:** `2 ≤ n ≤ 10⁵`, `0 ≤ arr[i] ≤ 10⁸` sorted, `1 ≤ k ≤ 10⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Max-heap of piece lengths | k times: pop largest gap/(cnt+1), give it one more station | O(n + k log n) | O(n) |
| Binary search on the answer (reals) | need(d) = Σ (⌈g/d⌉ − 1) ≤ k → hi = d else lo = d; 100 iterations | O(n · 100) | O(1) |

> [!tip] Interview angle
> Show the progression: O(k·n) brute → O(k log n) heap (always split the currently largest *piece*) → O(n log(range/ε)) binary search. Name why the heap stores `gap / (placed + 1)`: placing stations evenly in a gap is optimal.

---

## 3. Max-heap of piece lengths

**Intuition.** Greedy: each new station goes into the gap whose current piece length is largest. With `c` stations in gap `g` placed evenly, the piece is `g / (c + 1)`.

```python
def gas_station_heap(arr, k):
    import heapq
    gaps = [arr[i + 1] - arr[i] for i in range(len(arr) - 1)]
    cnt = [0] * len(gaps)
    h = [(-g, i) for i, g in enumerate(gaps)]
    heapq.heapify(h)
    for _ in range(k):
        _, i = heapq.heappop(h)
        cnt[i] += 1
        heapq.heappush(h, (-gaps[i] / (cnt[i] + 1), i))
    return float(-h[0][0])
```

**Complexity:** time **O(n + k log n)**, space **O(n)**.

---

## 4. Binary search on the answer (reals)

**Intuition.** For a candidate `d`, count stations needed: `c = ⌊g / d⌋`, minus one if `g` is an exact multiple of `d` (that's `⌈g/d⌉ − 1`). Feasible → shrink `hi`; else raise `lo`. 100 halvings of a range ≤ 10⁸ reaches double precision.

**Why fixed iterations, not `while hi − lo > 1e−6`:** epsilon loops can spin forever when the range is large and doubles can't represent the gap; a fixed count always terminates and is precise enough.

**C++**
```cpp
double minimiseMaxDistance(vector<int>& arr, int k) {
    int n = arr.size();
    double lo = 0, hi = 0;
    for (int i = 0; i + 1 < n; i++) hi = max(hi, (double)(arr[i + 1] - arr[i]));
    for (int it = 0; it < 100; it++) {
        double mid = (lo + hi) / 2;
        long long need = 0;
        for (int i = 0; i + 1 < n; i++) {
            double g = arr[i + 1] - arr[i];
            long long c = (long long)(g / mid);
            if (c * mid == g) c--;
            need += c;
        }
        if (need <= k) hi = mid;
        else lo = mid;
    }
    return hi;
}
```

**Java**
```java
static double minimiseMaxDistance(int[] arr, int k) {
    int n = arr.length;
    double lo = 0, hi = 0;
    for (int i = 0; i + 1 < n; i++) hi = Math.max(hi, arr[i + 1] - arr[i]);
    for (int it = 0; it < 100; it++) {
        double mid = (lo + hi) / 2;
        long need = 0;
        for (int i = 0; i + 1 < n; i++) {
            double g = arr[i + 1] - arr[i];
            long c = (long) (g / mid);
            if (c * mid == g) c--;
            need += c;
        }
        if (need <= k) hi = mid;
        else lo = mid;
    }
    return hi;
}
```

**Python**
```python
def minimise_max_distance(arr, k):
    gaps = [arr[i + 1] - arr[i] for i in range(len(arr) - 1)]
    lo, hi = 0.0, float(max(gaps))
    for _ in range(100):
        mid = (lo + hi) / 2
        need = 0
        for g in gaps:
            c = int(g / mid)
            if c * mid == g:
                c -= 1
            need += c
        if need <= k:
            hi = mid
        else:
            lo = mid
    return hi
```

**Complexity:** time **O(n · 100)**, space **O(1)** — constant 100 iterations × O(n) check.

---

## Edge cases

- All gaps equal.
- k = 0 → max gap (not allowed here, but the search returns it).
- Exact multiples: g / d integer → one fewer station.

---

## Common mistakes

1. Using `g / d` stations instead of `⌈g/d⌉ − 1`.
2. Epsilon loop that never ends.
3. Integer division in the check.

---

## Follow-ups

1. Integer positions only.
2. Return the station positions.

<details><summary>Answer sketches</summary>

**#1:** Integer binary search with need = ⌈g/d⌉ − 1.

**#2:** At the answer, place c evenly spaced points in each gap.
</details>

---

## Flashcards

**Stations needed to cut gap g into pieces ≤ d?** #flashcard
⌈g / d⌉ − 1.

**Real-valued binary search — loop condition?** #flashcard
Fixed ~100 iterations.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
