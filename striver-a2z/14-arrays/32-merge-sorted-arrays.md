---
module: striver-a2z/14-arrays
lesson: 32
topic: Merge Two Sorted Arrays Without Extra Space
difficulty: Medium
source: https://takeuforward.org/learning/dsa/merge-two-sorted-arrays-without-extra-space?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, two-pointers, merge, in-place]
---
# 32. Merge Two Sorted Arrays Without Extra Space

← [Maximum Product Subarray](31-maximum-product-subarray.md) · [Part 14 index](README.md) · Next → [Check if array is sorted and rotated](33-check-if-array-is-sorted-and-rotated.md)

> [!abstract] Problem at a glance
> **Task:** Merge sorted `nums2` (length `n`) into sorted `nums1`, whose first `m` slots hold data and the last `n` are zeros, in place.
> **Key insight:** Fill `nums1` from the back. The largest remaining element of either array goes to position `k = m + n − 1`, then `k−−`. Writing from the back never overwrites an unread element of `nums1`. Leftover `nums1` elements are already in place.
> **Difficulty:** Medium · **Pattern:** Two pointers from the end · **Also on:** [LC 88](https://leetcode.com/problems/merge-sorted-array/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/merge-two-sorted-arrays-without-extra-space?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Extra array merge](#3-extra-array-merge) · [4. Swap from the ends + sort (Striver's optimal 1)](#4-swap-from-the-ends--sort-strivers-optimal-1) · [5. Gap method (Striver's optimal 2)](#5-gap-method-strivers-optimal-2) · [6. Three pointers from the back (LC 88)](#6-three-pointers-from-the-back-lc-88) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums1` of length `m + n`, whose first `m` elements are sorted and whose last `n` are 0, and sorted `nums2` of length `n`, merge `nums2` into `nums1` so that `nums1` is sorted. Don't return anything.

| Input | Output | Why |
|---|---|---|
| `nums1 = [-5, -2, 4, 5, 0, 0, 0], m = 4, nums2 = [-3, 1, 8], n = 3` | `[-5, -3, -2, 1, 4, 5, 8]` |  |
| `nums1 = [0, 2, 7, 8, 0, 0, 0], m = 4, nums2 = [-7, -3, -1], n = 3` | `[-7, -3, -1, 0, 2, 7, 8]` |  |

**Constraints:** `0 ≤ m, n ≤ 200`, `1 ≤ m + n`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Extra array merge | standard merge into temp, copy back | O(m + n) | O(m + n) |
| Swap from the ends + sort (Striver's optimal 1) | swap nums1's largest with nums2's smallest while out of order; sort both | O(min(m, n) + m log m + n log n) | O(1) |
| Gap method (Striver's optimal 2) | Shell-sort gaps ⌈len/2⌉ down to 1 across both arrays | O((m + n) log(m + n)) | O(1) |
| Three pointers from the back (LC 88) | largest of nums1[i], nums2[j] goes to k; k−− | O(m + n) | O(1) |

> [!tip] Interview angle
> Striver also covers the version where both arrays are full (`nums1` of size m, `nums2` of size n, the result split across them). Mention it: the answers are swap-from-the-ends plus sorting, or the gap method (Shell-sort style) in O((m + n) log(m + n)) with O(1) space.

---

## 3. Extra array merge

**Intuition.** Merge the two sorted prefixes into a new array and copy it into `nums1`. Uses the extra space the title forbids.

```python
def merge_extra(nums1, m, nums2, n):
    tmp, i, j = [], 0, 0
    while i < m and j < n:
        if nums1[i] <= nums2[j]:
            tmp.append(nums1[i]); i += 1
        else:
            tmp.append(nums2[j]); j += 1
    tmp += nums1[i:m] + nums2[j:n]
    nums1[:] = tmp
```

**Complexity:** time **O(m + n)**, space **O(m + n)**.

---

## 4. Swap from the ends + sort (Striver's optimal 1)

**Intuition.** For the two-arrays version: compare `nums1[m − 1 − t]` with `nums2[t]`. While the left one is bigger, swap them. Afterwards every element of `nums1` is ≤ every element of `nums2`, but each array needs sorting. Here we then copy `nums2` into the tail of `nums1`.

```python
def merge_swap_sort(nums1, m, nums2, n):
    a, b = nums1[:m], list(nums2)
    l, r = m - 1, 0
    while l >= 0 and r < n and a[l] > b[r]:
        a[l], b[r] = b[r], a[l]
        l -= 1; r += 1
    a.sort(); b.sort()
    nums1[:] = a + b
```

**Complexity:** time **O(min(m, n) + m log m + n log n)**, space **O(1)**.

---

## 5. Gap method (Striver's optimal 2)

**Intuition.** Treat the two arrays as one virtual array of length `L = m + n`. For `gap = ⌈L/2⌉, ⌈gap/2⌉, …, 1`, compare positions `i` and `i + gap` and swap if they're out of order. Each pass is O(L). On the last gap of 1, the array is sorted.

```python
def merge_gap(nums1, m, nums2, n):
    a, b = nums1[:m], list(nums2)
    L = m + n
    def get(k): return a[k] if k < m else b[k - m]
    def put(k, v):
        if k < m: a[k] = v
        else: b[k - m] = v
    gap = (L + 1) // 2
    while gap > 0:
        for i in range(L - gap):
            j = i + gap
            if get(i) > get(j):
                x, y = get(i), get(j)
                put(i, y); put(j, x)
        if gap == 1:
            break
        gap = (gap + 1) // 2
    nums1[:] = a + b
```

**Complexity:** time **O((m + n) log(m + n))**, space **O(1)**.

---

## 6. Three pointers from the back (LC 88)

**Intuition.** Positions `> k` in `nums1` are final. Since `k = i + j + 1 > i`, writing at `k` never clobbers an unread `nums1[i]`. Loop while `j >= 0`: once `nums2` is exhausted, the remaining `nums1[0..i]` are already in place.

**Algorithm**

1. `i = m − 1`, `j = n − 1`, `k = m + n − 1`.
2. While `j >= 0`: if `i >= 0 and nums1[i] > nums2[j]`: `nums1[k−−] = nums1[i−−]`; else `nums1[k−−] = nums2[j−−]`.

**Dry run** — `[−5 −2 4 5 _ _ _]`, `[−3 1 8]`: 8 → k=6; 5 → k=5; 4 → k=4; 1 → k=3; −2 → k=2; −3 → k=1; j < 0, stop. `[−5 −3 −2 1 4 5 8]`.

**C++**
```cpp
void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
    int i = m - 1, j = n - 1, k = m + n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j]) nums1[k--] = nums1[i--];
        else nums1[k--] = nums2[j--];
    }
}
```

**Java**
```java
static void merge(int[] nums1, int m, int[] nums2, int n) {
    int i = m - 1, j = n - 1, k = m + n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j]) nums1[k--] = nums1[i--];
        else nums1[k--] = nums2[j--];
    }
}
```

**Python**
```python
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]; i -= 1
        else:
            nums1[k] = nums2[j]; j -= 1
        k -= 1
```

**Complexity:** time **O(m + n)**, space **O(1)**.

---

## Edge cases

- m = 0 (copy nums2).
- n = 0 (nothing to do).
- All of nums2 smaller / larger than nums1.

---

## Common mistakes

1. Filling from the front → overwrites unread `nums1` elements.
2. Looping while `i >= 0 and j >= 0`, then forgetting to copy the rest of `nums2`.
3. Gap method: `gap = gap // 2` (floor) skips needed passes; use the ceiling and stop after gap 1.

---

## Follow-ups

1. Both arrays full (no buffer); result split across them.
2. Merge k sorted arrays.
3. Median of two sorted arrays (LC 4).

<details><summary>Answer sketches</summary>

**#1:** Swap-from-ends + sort, or the gap method.

**#2:** Min-heap of heads ([Part 26](../26-heaps/README.md)).

**#3:** Binary search on the partition ([Part 16](../16-binary-search/README.md)).
</details>

---

## Flashcards

**LC 88 merge in place: direction?** #flashcard
From the back: largest to index k = m + n − 1.

**LC 88 loop condition?** #flashcard
while j >= 0; leftover nums1 is already in place.

**Gap method next gap?** #flashcard
⌈gap / 2⌉, stopping after gap = 1.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
