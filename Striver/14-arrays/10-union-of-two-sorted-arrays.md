---
module: striver/14-arrays
lesson: 10
topic: Union of Two Sorted Arrays
difficulty: Easy
source: https://takeuforward.org/learning/dsa/union-of-two-sorted-arrays?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, two-pointers, merge]
---
# 10. Union of Two Sorted Arrays

← [Find Missing Number](09-find-missing-number.md) · [Part 14 index](README.md) · Next → [Intersection of Two Sorted Arrays](11-intersection-of-two-sorted-arrays.md)

> [!abstract] Problem at a glance
> **Task:** Return the sorted list of distinct values present in either of two sorted arrays.
> **Key insight:** Merge with two pointers like merge sort, but append a value only if it differs from the last value appended. That handles duplicates inside and across both arrays in O(n + m).
> **Difficulty:** Easy · **Pattern:** Two pointers: merge · **Also on:** GfG Union of Two Sorted Arrays
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/union-of-two-sorted-arrays?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Ordered set](#3-ordered-set) · [4. Two-pointer merge with dedupe](#4-two-pointer-merge-with-dedupe) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two arrays `nums1` and `nums2`, each sorted in non-decreasing order, return their union: every distinct element present in either array, in sorted order.

| Input | Output | Why |
|---|---|---|
| `nums1 = [1, 2, 3, 4, 5], nums2 = [1, 2, 7]` | `[1, 2, 3, 4, 5, 7]` |  |
| `nums1 = [3, 4, 6, 7, 9, 9], nums2 = [1, 5, 7, 8, 8]` | `[1, 3, 4, 5, 6, 7, 8, 9]` |  |

**Constraints:** `1 ≤ n, m ≤ 10⁵`, both sorted.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Ordered set | insert everything into a set | O((n + m) log(n + m)) | O(n + m) |
| Two-pointer merge with dedupe | take the smaller head; skip if equal to the last output | O(n + m) | O(1) beyond the output |

---

## 3. Ordered set

**Intuition.** An ordered set dedupes and sorts. Correct, but it ignores that the inputs are sorted.

```python
def union_set(a, b):
    return sorted(set(a) | set(b))
```

**Complexity:** time **O((n + m) log(n + m))**, space **O(n + m)**.

---

## 4. Two-pointer merge with dedupe

**Intuition.** At each step take the smaller of `a[i]`, `b[j]` (on a tie, take one and advance both). Append only if the output is empty or its last value differs. Then drain the leftovers with the same check.

**Algorithm**

1. `i = j = 0`, `res = []`.
2. While both remain: `v = min(a[i], b[j])`; advance whichever pointer(s) equal `v`; push `v` if `res` is empty or `res.back() != v`.
3. Drain `a` then `b` with the same push rule.

**C++**
```cpp
vector<int> unionArray(vector<int>& a, vector<int>& b) {
    vector<int> res;
    int i = 0, j = 0, n = a.size(), m = b.size();
    auto push = [&](int v) { if (res.empty() || res.back() != v) res.push_back(v); };
    while (i < n && j < m) {
        if (a[i] < b[j]) push(a[i++]);
        else if (b[j] < a[i]) push(b[j++]);
        else { push(a[i]); i++; j++; }
    }
    while (i < n) push(a[i++]);
    while (j < m) push(b[j++]);
    return res;
}
```

**Java**
```java
static int[] unionArray(int[] a, int[] b) {
    ArrayList<Integer> res = new ArrayList<>();
    int i = 0, j = 0, n = a.length, m = b.length;
    while (i < n || j < m) {
        int v;
        if (j == m || (i < n && a[i] < b[j])) v = a[i++];
        else if (i == n || b[j] < a[i]) v = b[j++];
        else { v = a[i]; i++; j++; }
        if (res.isEmpty() || res.get(res.size() - 1) != v) res.add(v);
    }
    int[] out = new int[res.size()];
    for (int k = 0; k < out.length; k++) out[k] = res.get(k);
    return out;
}
```

**Python**
```python
def union_array(a, b):
    res, i, j = [], 0, 0
    def push(v):
        if not res or res[-1] != v:
            res.append(v)
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            push(a[i]); i += 1
        elif b[j] < a[i]:
            push(b[j]); j += 1
        else:
            push(a[i]); i += 1; j += 1
    for v in a[i:]:
        push(v)
    for v in b[j:]:
        push(v)
    return res
```

**Complexity:** time **O(n + m)**, space **O(1) beyond the output**.

---

## Edge cases

- Duplicates inside one array.
- Disjoint ranges.
- One array exhausted early.
- Identical arrays.

---

## Common mistakes

1. Forgetting to dedupe the leftover tail.
2. Java `Integer` comparison with `!=` above 127: compare `int` values (here `v` is unboxed, `res.get(...)` auto-unboxes because `v` is `int`).
3. Using `<=` without handling the tie → equal values from both arrays both appended.

---

## Follow-ups

1. Union of unsorted arrays.
2. Union of k sorted arrays.

<details><summary>Answer sketches</summary>

**#1:** Hash set: O(n + m) average, then sort if sorted output is required.

**#2:** Min-heap of k heads: O(N log k).
</details>

---

## Flashcards

**Union of sorted arrays: dedupe rule?** #flashcard
Append v only if the output is empty or its last value ≠ v.

**Union of sorted arrays complexity?** #flashcard
O(n + m) time, O(1) besides the output.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
