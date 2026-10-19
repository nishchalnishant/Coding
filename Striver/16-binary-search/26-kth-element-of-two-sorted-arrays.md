---
module: striver/16-binary-search
lesson: 26
topic: Kth Element of 2 Sorted Arrays
difficulty: Medium
source: https://takeuforward.org/learning/dsa/kth-element-of-2-sorted-arrays?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, partition]
---
# 26. Kth Element of 2 Sorted Arrays

← [Median of 2 Sorted Arrays](25-median-of-two-sorted-arrays.md) · [Part 16 index](README.md) · Next → [Minimize Max Distance to Gas Station](27-minimise-max-distance-to-gas-station.md)

> [!abstract] Problem at a glance
> **Task:** Return the k-th smallest element (1-indexed) of the union of two sorted arrays.
> **Key insight:** Same partition search as the median, with left-half size `k`. Bound `c1 ∈ [max(0, k − n₂), min(k, n₁)]` so `c2 = k − c1` stays valid. Answer = `max(l1, l2)`.
> **Difficulty:** Medium · **Pattern:** Binary search on partition
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/kth-element-of-2-sorted-arrays?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Merge to k](#3-merge-to-k) · [4. Binary search the partition](#4-binary-search-the-partition) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two sorted arrays `a` and `b` and an integer `k` (`1 ≤ k ≤ n₁ + n₂`), return the element that would be at position `k` in the merged sorted array.

| Input | Output | Why |
|---|---|---|
| `a = [2, 3, 6, 7, 9], b = [1, 4, 8, 10], k = 5` | `6` | merged 1 2 3 4 6 … |
| `a = [100, 112, 256, 349, 770], b = [72, 86, 113, 119, 265, 445, 892], k = 7` | `256` |  |

**Constraints:** `0 ≤ n₁, n₂ ≤ 10⁶`, `1 ≤ k ≤ n₁ + n₂`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Merge to k | two pointers, stop at the k-th pick | O(k) | O(1) |
| Binary search the partition | c1 ∈ [max(0, k − n₂), min(k, n₁)]; valid cut → max(l1, l2) | O(log min(n₁, n₂)) | O(1) |

---

## 3. Merge to k

**Intuition.** Walk both arrays taking the smaller head; the k-th one taken is the answer.

```python
def kth_merge(a, b, k):
    i = j = 0
    while True:
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            x, i = a[i], i + 1
        else:
            x, j = b[j], j + 1
        k -= 1
        if k == 0:
            return x
```

**Complexity:** time **O(k)**, space **O(1)**.

---

## 4. Binary search the partition

**Intuition.** The left part must hold exactly `k` elements. `c1` can't exceed `min(k, n₁)`, and must be at least `k − n₂` (b can't supply more than n₂).

**Dry run** — a `[1 2]`, b `[3 4]`, k 1: lo 0 hi 1 c1 0 c2 1: l1 −∞ r1 1 l2 3 r2 4 → l2 > r1 → lo 1; c1 1 c2 0: l1 1 r1 2 l2 −∞ r2 3 ✓ → 1.

**C++**
```cpp
int kthElement(vector<int>& a, vector<int>& b, int k) {
    if (a.size() > b.size()) return kthElement(b, a, k);
    int n1 = a.size(), n2 = b.size();
    int lo = max(0, k - n2), hi = min(k, n1);
    while (lo <= hi) {
        int c1 = (lo + hi) / 2, c2 = k - c1;
        int l1 = c1 > 0 ? a[c1 - 1] : INT_MIN, r1 = c1 < n1 ? a[c1] : INT_MAX;
        int l2 = c2 > 0 ? b[c2 - 1] : INT_MIN, r2 = c2 < n2 ? b[c2] : INT_MAX;
        if (l1 <= r2 && l2 <= r1) return max(l1, l2);
        if (l1 > r2) hi = c1 - 1;
        else lo = c1 + 1;
    }
    return -1;
}
```

**Java**
```java
static int kthElement(int[] a, int[] b, int k) {
    if (a.length > b.length) return kthElement(b, a, k);
    int n1 = a.length, n2 = b.length;
    int lo = Math.max(0, k - n2), hi = Math.min(k, n1);
    while (lo <= hi) {
        int c1 = (lo + hi) / 2, c2 = k - c1;
        int l1 = c1 > 0 ? a[c1 - 1] : Integer.MIN_VALUE, r1 = c1 < n1 ? a[c1] : Integer.MAX_VALUE;
        int l2 = c2 > 0 ? b[c2 - 1] : Integer.MIN_VALUE, r2 = c2 < n2 ? b[c2] : Integer.MAX_VALUE;
        if (l1 <= r2 && l2 <= r1) return Math.max(l1, l2);
        if (l1 > r2) hi = c1 - 1;
        else lo = c1 + 1;
    }
    return -1;
}
```

**Python**
```python
def kth_element(a, b, k):
    if len(a) > len(b):
        a, b = b, a
    n1, n2 = len(a), len(b)
    lo, hi = max(0, k - n2), min(k, n1)
    inf = float("inf")
    while lo <= hi:
        c1 = (lo + hi) // 2
        c2 = k - c1
        l1 = a[c1 - 1] if c1 > 0 else -inf
        r1 = a[c1] if c1 < n1 else inf
        l2 = b[c2 - 1] if c2 > 0 else -inf
        r2 = b[c2] if c2 < n2 else inf
        if l1 <= r2 and l2 <= r1:
            return max(l1, l2)
        if l1 > r2:
            hi = c1 - 1
        else:
            lo = c1 + 1
    return -1
```

**Complexity:** time **O(log min(n₁, n₂))**, space **O(1)** — log of the smaller array's size.

---

## Edge cases

- k = 1 or k = n₁ + n₂.
- One array empty.
- k > n₂ forces c1 ≥ k − n₂.

---

## Common mistakes

1. Range `[0, n1]` without the k bounds → c2 out of range.
2. Off-by-one: k is 1-indexed, the cut size is k.

---

## Follow-ups

1. Median as a special case.
2. Recursive O(log k) elimination.

<details><summary>Answer sketches</summary>

**#1:** k = (n₁ + n₂ + 1) / 2 (and k + 1 for even totals).

**#2:** Compare a[k/2 − 1] and b[k/2 − 1]; drop k/2 elements from the smaller side.
</details>

---

## Flashcards

**Kth of two arrays — c1 bounds?** #flashcard
[max(0, k − n₂), min(k, n₁)].

**Kth of two arrays — answer at valid cut?** #flashcard
max(l1, l2).

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
