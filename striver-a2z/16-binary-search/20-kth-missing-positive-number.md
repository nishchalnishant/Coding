---
module: striver-a2z/16-binary-search
lesson: 20
topic: Kth Missing Positive Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/kth-missing-positive-number?category=on-answers&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search]
---
# 20. Kth Missing Positive Number

← [Capacity to Ship Packages Within D Days](19-ship-within-days.md) · [Part 16 index](README.md) · Next → [Painter's Partition](21-painters-partition.md)

> [!abstract] Problem at a glance
> **Task:** Given a strictly increasing array of positive ints, return the `k`-th positive integer missing from it.
> **Key insight:** Missing count before index `i` is `arr[i] − (i + 1)`, and it's non-decreasing. Binary search the first index where missing ≥ k; the answer is `lo + k` (with `lo` = that index).
> **Difficulty:** Easy · **Pattern:** Binary search on derived monotone quantity · **Also on:** [LC 1539](https://leetcode.com/problems/kth-missing-positive-number/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/kth-missing-positive-number?category=on-answers&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Walk and bump](#3-walk-and-bump) · [4. Binary search on missing count](#4-binary-search-on-missing-count) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a sorted array `arr` of distinct positive integers and an integer `k`, return the `k`-th positive integer that is missing from `arr`.

| Input | Output | Why |
|---|---|---|
| `arr = [2, 3, 4, 7, 11], k = 5` | `9` | missing: 1 5 6 8 9 … |
| `arr = [1, 2, 3, 4], k = 2` | `6` |  |
| `arr = [5, 6, 7], k = 3` | `3` |  |

**Constraints:** `1 ≤ n ≤ 1000`, `1 ≤ arr[i] ≤ 1000`, `1 ≤ k ≤ 1000`, strictly increasing.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Walk and bump | for x in arr: if x ≤ k: k += 1 | O(n) | O(1) |
| Binary search on missing count | missing(i) = arr[i] − i − 1; first i with missing ≥ k; return lo + k | O(log n) | O(1) |

> [!tip] Interview angle
> Derive `lo + k` aloud: after the loop, `hi = lo − 1` is the last index with fewer than `k` missing. Answer = `arr[hi] + (k − missing(hi))` = `arr[hi] + k − (arr[hi] − hi − 1)` = `hi + 1 + k` = `lo + k`. Interviewers like seeing that algebra.

---

## 3. Walk and bump

**Intuition.** Every array element `≤` the current candidate pushes the k-th missing number one further. Neat O(n) solution.

```python
def kth_missing_linear(arr, k):
    for x in arr:
        if x <= k:
            k += 1
        else:
            break
    return k
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 4. Binary search on missing count

**Intuition.** If the array were `[1, 2, 3, …]`, `arr[i] = i + 1`. Each skipped number raises `arr[i]` by one, so `arr[i] − (i + 1)` is exactly how many positives are missing below `arr[i]`. Search the boundary where that count reaches `k`.

**Dry run** — `[2 3 4 7 11]`, k 5: missing = [1 1 1 3 6]. lo 0 hi 4 mid 2 (1 < 5) lo 3; mid 3 (3 < 5) lo 4; mid 4 (6 ≥ 5) hi 3. lo 4 → 4 + 5 = 9.

**C++**
```cpp
int findKthPositive(vector<int>& arr, int k) {
    int lo = 0, hi = (int)arr.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] - (mid + 1) < k) lo = mid + 1;
        else hi = mid - 1;
    }
    return lo + k;
}
```

**Java**
```java
static int findKthPositive(int[] arr, int k) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] - (mid + 1) < k) lo = mid + 1;
        else hi = mid - 1;
    }
    return lo + k;
}
```

**Python**
```python
def find_kth_positive(arr, k):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) < k:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo + k
```

**Complexity:** time **O(log n)**, space **O(1)** — plain halving over indices.

---

## Edge cases

- All missing numbers before arr[0] (k < arr[0]).
- No gaps (`[1..n]`) → n + k.

---

## Common mistakes

1. Returning `arr[lo] + …` — `lo` may be `n` (out of range).
2. Using `arr[i] − i` (forgot the +1).

---

## Follow-ups

1. Array has duplicates.
2. k-th missing between arr[0] and arr[n−1] (LC 1060).

<details><summary>Answer sketches</summary>

**#1:** Missing count no longer arr[i] − i − 1; dedupe first or count differently.

**#2:** Missing(i) = arr[i] − arr[0] − i; same search.
</details>

---

## Flashcards

**Missing positives below arr[i]?** #flashcard
arr[i] − (i + 1).

**Kth missing — final formula?** #flashcard
lo + k, where lo = first index with missing ≥ k.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../04-practice/algorithms/11-binary-search.md)
