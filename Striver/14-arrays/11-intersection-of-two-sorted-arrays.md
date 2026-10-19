---
module: striver/14-arrays
lesson: 11
topic: Intersection of Two Sorted Arrays
difficulty: Easy
source: https://takeuforward.org/learning/dsa/intersection-of-two-sorted-arrays?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, two-pointers]
---
# 11. Intersection of Two Sorted Arrays

← [Union of Two Sorted Arrays](10-union-of-two-sorted-arrays.md) · [Part 14 index](README.md) · Next → [Majority Element I](12-majority-element.md)

> [!abstract] Problem at a glance
> **Task:** Return the elements common to two sorted arrays, each repeated as many times as it appears in *both* (min of the two counts).
> **Key insight:** Two pointers: advance the smaller side; on equality, record the value and advance both. Each match consumes one copy from each array, which is exactly the min-count rule.
> **Difficulty:** Easy · **Pattern:** Two pointers: merge · **Also on:** [LC 350](https://leetcode.com/problems/intersection-of-two-arrays-ii/) (unsorted version)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/intersection-of-two-sorted-arrays?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Visited array](#3-visited-array) · [4. Two pointers](#4-two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given two sorted arrays `nums1` and `nums2`, return their intersection in sorted order. A value that occurs `p` times in `nums1` and `q` times in `nums2` appears `min(p, q)` times.

| Input | Output | Why |
|---|---|---|
| `nums1 = [1, 2, 2, 3, 5], nums2 = [1, 2, 7]` | `[1, 2]` | 2 appears once in nums2 |
| `nums1 = [1, 2, 2, 3], nums2 = [2, 2, 4]` | `[2, 2]` |  |

**Constraints:** `1 ≤ n, m ≤ 10⁵`, both sorted.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Visited array | for each a[i], find an unused equal b[j] | O(n · m) | O(m) |
| Two pointers | advance the smaller; equal → take and advance both | O(n + m) | O(1) beyond the output |

---

## 3. Visited array

**Intuition.** For every element of `a`, scan `b` for an equal element not used yet and mark it. Because `b` is sorted, break as soon as `b[j] > a[i]`.

```python
def intersect_brute(a, b):
    used, res = [False] * len(b), []
    for x in a:
        for j, y in enumerate(b):
            if y == x and not used[j]:
                used[j] = True; res.append(x); break
            if y > x:
                break
    return res
```

**Complexity:** time **O(n · m)**, space **O(m)**.

---

## 4. Two pointers

**Intuition.** If `a[i] < b[j]`, `a[i]` can't match anything at or after `j`, so skip it. Symmetrically for `b`. On a tie, both copies are used up together.

**Distinct intersection (LC 349 style):** additionally skip if the value equals the last appended one.

**C++**
```cpp
vector<int> intersectionArray(vector<int>& a, vector<int>& b) {
    vector<int> res;
    int i = 0, j = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        if (a[i] < b[j]) i++;
        else if (b[j] < a[i]) j++;
        else { res.push_back(a[i]); i++; j++; }
    }
    return res;
}
```

**Java**
```java
static int[] intersectionArray(int[] a, int[] b) {
    ArrayList<Integer> res = new ArrayList<>();
    int i = 0, j = 0;
    while (i < a.length && j < b.length) {
        if (a[i] < b[j]) i++;
        else if (b[j] < a[i]) j++;
        else { res.add(a[i]); i++; j++; }
    }
    int[] out = new int[res.size()];
    for (int k = 0; k < out.length; k++) out[k] = res.get(k);
    return out;
}
```

**Python**
```python
def intersection_array(a, b):
    res, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif b[j] < a[i]:
            j += 1
        else:
            res.append(a[i]); i += 1; j += 1
    return res
```

**Complexity:** time **O(n + m)**, space **O(1) beyond the output**.

---

## Edge cases

- Empty intersection.
- All duplicates.
- One array is a sub-multiset of the other.

---

## Common mistakes

1. Advancing only one pointer on a match → the same element counted repeatedly.
2. Applying distinct-dedupe when min-count semantics are asked (or vice versa). Clarify first.

---

## Follow-ups

1. Unsorted arrays (LC 350).
2. `nums2` is on disk and too big for memory.
3. One array is tiny, the other huge.

<details><summary>Answer sketches</summary>

**#1:** Count the smaller array in a hash map; decrement while scanning the other.

**#2:** Stream it in sorted chunks against an in-memory count map of `nums1`.

**#3:** Binary search each small element in the big one: O(n log m).
</details>

---

## Flashcards

**Intersection of sorted arrays: on a tie?** #flashcard
Record it and advance both pointers.

**Intersection when one array is much smaller?** #flashcard
Binary search each small element in the big array: O(n log m).

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
