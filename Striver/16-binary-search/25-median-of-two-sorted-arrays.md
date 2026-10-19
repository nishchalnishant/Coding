---
module: striver/16-binary-search
lesson: 25
topic: Median of 2 Sorted Arrays
difficulty: Hard
source: https://takeuforward.org/learning/dsa/median-of-2-sorted-arrays?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, partition]
---
# 25. Median of 2 Sorted Arrays

← [Find Peak Element](24-find-peak-element.md) · [Part 16 index](README.md) · Next → [Kth Element of 2 Sorted Arrays](26-kth-element-of-two-sorted-arrays.md)

> [!abstract] Problem at a glance
> **Task:** Return the median of two sorted arrays in O(log(min(n₁, n₂))).
> **Key insight:** Binary search how many elements `c1` the **left half** takes from the smaller array; `c2 = half − c1` come from the other. The split is correct when `l1 ≤ r2` and `l2 ≤ r1`. Median comes from `max(l1, l2)` and `min(r1, r2)`.
> **Difficulty:** Hard · **Pattern:** Binary search on partition · **Also on:** [LC 4](https://leetcode.com/problems/median-of-two-sorted-arrays/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/median-of-2-sorted-arrays?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 35 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Merge](#3-merge) · [4. Binary search the partition](#4-binary-search-the-partition) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given sorted arrays `a` (size `n₁`) and `b` (size `n₂`), return the median of the combined multiset. Target O(log(n₁ + n₂)).

| Input | Output | Why |
|---|---|---|
| `a = [1, 3], b = [2]` | `2.0` |  |
| `a = [1, 2], b = [3, 4]` | `2.5` | (2 + 3) / 2 |

**Constraints:** `0 ≤ n₁, n₂ ≤ 1000`, `1 ≤ n₁ + n₂ ≤ 2000`, `|values| ≤ 10⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Merge | two-pointer merge, read the middle | O(n₁ + n₂) | O(n₁ + n₂) |
| Binary search the partition | search c1 in smaller array; valid when l1 ≤ r2 and l2 ≤ r1 | O(log min(n₁, n₂)) | O(1) |

> [!tip] Interview angle
> Hardest standard binary search question. Present it in three steps: (1) merge → O(n) baseline, (2) "the median is fixed by a cut that puts half the elements on the left", (3) search that cut in the smaller array. Use ±∞ sentinels so there are no special cases at the edges.

---

## 3. Merge

**Intuition.** Merge like merge sort. Can be done in O(1) space by only walking to the middle and tracking the last two values.

```python
def median_merge(a, b):
    m, i, j = [], 0, 0
    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            m.append(a[i]); i += 1
        else:
            m.append(b[j]); j += 1
    n = len(m)
    return float(m[n // 2]) if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2
```

**Complexity:** time **O(n₁ + n₂)**, space **O(n₁ + n₂)**.

---

## 4. Binary search the partition

**Intuition.** Let `half = (n₁ + n₂ + 1) / 2` — the left half size (one bigger when the total is odd). Pick `c1` from the smaller array `a`, so `c2 = half − c1` from `b`. Boundary values:

- `l1 = a[c1 − 1]`, `r1 = a[c1]`, `l2 = b[c2 − 1]`, `r2 = b[c2]`, with −∞/+∞ when out of range.

The cut is valid iff `l1 ≤ r2` and `l2 ≤ r1` (everything left ≤ everything right). If `l1 > r2`, too many from `a` → `hi = c1 − 1`. Else `lo = c1 + 1`.

**Dry run** — a `[1 3]`, b `[2]` → swap so a = `[2]`, b = `[1 3]`; half 2. lo 0 hi 1 c1 0 c2 2: l1 −∞ r1 2 l2 3 r2 +∞ → l2 > r1 → lo 1; c1 1 c2 1: l1 2 r1 +∞ l2 1 r2 3 ✓ → odd → max(2, 1) = 2.

**Why search the smaller array:** it keeps `c2 = half − c1` within `[0, n₂]` for every `c1 ∈ [0, n₁]`, and makes the complexity log(min).

**C++**
```cpp
double findMedianSortedArrays(vector<int>& a, vector<int>& b) {
    if (a.size() > b.size()) return findMedianSortedArrays(b, a);
    int n1 = a.size(), n2 = b.size(), half = (n1 + n2 + 1) / 2;
    int lo = 0, hi = n1;
    while (lo <= hi) {
        int c1 = (lo + hi) / 2, c2 = half - c1;
        int l1 = c1 > 0 ? a[c1 - 1] : INT_MIN, r1 = c1 < n1 ? a[c1] : INT_MAX;
        int l2 = c2 > 0 ? b[c2 - 1] : INT_MIN, r2 = c2 < n2 ? b[c2] : INT_MAX;
        if (l1 <= r2 && l2 <= r1) {
            if ((n1 + n2) % 2) return max(l1, l2);
            return (max(l1, l2) + (double)min(r1, r2)) / 2.0;
        }
        if (l1 > r2) hi = c1 - 1;
        else lo = c1 + 1;
    }
    return 0.0;
}
```

**Java**
```java
static double findMedianSortedArrays(int[] a, int[] b) {
    if (a.length > b.length) return findMedianSortedArrays(b, a);
    int n1 = a.length, n2 = b.length, half = (n1 + n2 + 1) / 2;
    int lo = 0, hi = n1;
    while (lo <= hi) {
        int c1 = (lo + hi) / 2, c2 = half - c1;
        int l1 = c1 > 0 ? a[c1 - 1] : Integer.MIN_VALUE, r1 = c1 < n1 ? a[c1] : Integer.MAX_VALUE;
        int l2 = c2 > 0 ? b[c2 - 1] : Integer.MIN_VALUE, r2 = c2 < n2 ? b[c2] : Integer.MAX_VALUE;
        if (l1 <= r2 && l2 <= r1) {
            if ((n1 + n2) % 2 == 1) return Math.max(l1, l2);
            return (Math.max(l1, l2) + (double) Math.min(r1, r2)) / 2.0;
        }
        if (l1 > r2) hi = c1 - 1;
        else lo = c1 + 1;
    }
    return 0.0;
}
```

**Python**
```python
def find_median_sorted_arrays(a, b):
    if len(a) > len(b):
        a, b = b, a
    n1, n2 = len(a), len(b)
    half = (n1 + n2 + 1) // 2
    lo, hi = 0, n1
    inf = float("inf")
    while lo <= hi:
        c1 = (lo + hi) // 2
        c2 = half - c1
        l1 = a[c1 - 1] if c1 > 0 else -inf
        r1 = a[c1] if c1 < n1 else inf
        l2 = b[c2 - 1] if c2 > 0 else -inf
        r2 = b[c2] if c2 < n2 else inf
        if l1 <= r2 and l2 <= r1:
            if (n1 + n2) % 2:
                return float(max(l1, l2))
            return (max(l1, l2) + min(r1, r2)) / 2
        if l1 > r2:
            hi = c1 - 1
        else:
            lo = c1 + 1
    return 0.0
```

**Complexity:** time **O(log min(n₁, n₂))**, space **O(1)** — binary search over n₁ + 1 cut positions of the smaller array.

---

## Edge cases

- One array empty.
- All of `a` smaller than all of `b`.
- Duplicates across arrays.

---

## Common mistakes

1. Searching the larger array → `c2` goes negative.
2. `(l + r) / 2` in int before converting to double.
3. `hi = n1 − 1` instead of `n1` (c1 can take all of a).

---

## Follow-ups

1. k-th smallest of two sorted arrays.
2. Median of k sorted arrays.

<details><summary>Answer sketches</summary>

**#1:** Next problem: same partition with half = k.

**#2:** Binary search on value + count ≤ x with upper_bound in each array: O(k log n log range).
</details>

---

## Flashcards

**Median of two arrays — what do you binary search?** #flashcard
How many elements the left half takes from the smaller array.

**Valid partition condition?** #flashcard
l1 ≤ r2 and l2 ≤ r1.

**Left half size?** #flashcard
(n₁ + n₂ + 1) / 2.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
