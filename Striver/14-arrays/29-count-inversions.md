---
module: striver/14-arrays
lesson: 29
topic: Count Inversions
difficulty: Hard
source: https://takeuforward.org/learning/dsa/count-inversions?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, merge-sort, divide-and-conquer]
---
# 29. Count Inversions

← [Find the Repeating and Missing Number](28-repeating-and-missing.md) · [Part 14 index](README.md) · Next → [Reverse Pairs](30-reverse-pairs.md)

> [!abstract] Problem at a glance
> **Task:** Count pairs `(i, j)` with `i < j` and `nums[i] > nums[j]`.
> **Key insight:** Piggyback on merge sort. When merging, if `right[j] < left[i]`, then `right[j]` is smaller than *every* remaining element of the left half (it's sorted), so add `mid − i + 1` in one step. Total O(n log n).
> **Difficulty:** Hard · **Pattern:** Merge sort counting · **Also on:** GfG Count Inversions
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-inversions?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All pairs](#3-all-pairs) · [4. Merge sort with counting](#4-merge-sort-with-counting) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the number of inversions: pairs `(i, j)` with `i < j` and `nums[i] > nums[j]`.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 3, 7, 1, 3, 5]` | `5` | (2,1) (3,1) (7,1) (7,3) (7,5) |
| `nums = [-10, -5, 6, 11, 15, 17]` | `0` | sorted |

**Constraints:** `1 ≤ n ≤ 10⁵`. The count can reach n(n − 1)/2 ≈ 5·10⁹, which needs 64-bit.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All pairs | nested loops | O(n²) | O(1) |
| Merge sort with counting | cross inversions += mid − i + 1 when right wins | O(n log n) | O(n) |

> [!tip] Interview angle
> Say why the count can be done during the merge: inversions split into left-only, right-only and cross pairs, and the cross ones are counted cheaply only once both halves are sorted.

---

## 3. All pairs

**Intuition.** Count `nums[i] > nums[j]` over every `i < j`.

```python
def inversions_brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] > nums[j])
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Merge sort with counting

**Intuition.** `inv(arr) = inv(left) + inv(right) + cross(left, right)`. With both halves sorted, during the merge, each time an element from the right half is placed before `left[i]`, it forms an inversion with `left[i..mid]`, all `mid − i + 1` of them. Equal values must not count, so take from the left on `<=`.

**Dry run** — merge `[2 3 7]` + `[1 3 5]`: 1 < 2 → +3; 2 ≤ 3; 3 ≤ 3 (left first); 7 > 3 → +1; 7 > 5 → +1. Cross = 5.

**Inversion count = number of swaps bubble sort makes** = the minimum adjacent swaps to sort the array. Also solvable with a Fenwick tree over compressed values (O(n log n)).

**C++**
```cpp
long long mergeCount(vector<int>& a, int l, int m, int r) {
    vector<int> tmp;
    int i = l, j = m + 1;
    long long cnt = 0;
    while (i <= m && j <= r) {
        if (a[i] <= a[j]) tmp.push_back(a[i++]);
        else { cnt += m - i + 1; tmp.push_back(a[j++]); }
    }
    while (i <= m) tmp.push_back(a[i++]);
    while (j <= r) tmp.push_back(a[j++]);
    for (int k = l; k <= r; k++) a[k] = tmp[k - l];
    return cnt;
}
long long sortCount(vector<int>& a, int l, int r) {
    if (l >= r) return 0;
    int m = l + (r - l) / 2;
    return sortCount(a, l, m) + sortCount(a, m + 1, r) + mergeCount(a, l, m, r);
}
long long countInversions(vector<int>& nums) {
    vector<int> a = nums;   // don't destroy the caller's array
    return sortCount(a, 0, (int)a.size() - 1);
}
```

**Java**
```java
static long mergeCount(int[] a, int l, int m, int r) {
    int[] tmp = new int[r - l + 1];
    int i = l, j = m + 1, k = 0;
    long cnt = 0;
    while (i <= m && j <= r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else { cnt += m - i + 1; tmp[k++] = a[j++]; }
    }
    while (i <= m) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    System.arraycopy(tmp, 0, a, l, tmp.length);
    return cnt;
}
static long sortCount(int[] a, int l, int r) {
    if (l >= r) return 0;
    int m = l + (r - l) / 2;
    return sortCount(a, l, m) + sortCount(a, m + 1, r) + mergeCount(a, l, m, r);
}
static long countInversions(int[] nums) {
    int[] a = nums.clone();
    return sortCount(a, 0, a.length - 1);
}
```

**Python**
```python
def count_inversions(nums):
    a = list(nums)

    def sort_count(l, r):
        if l >= r:
            return 0
        m = (l + r) // 2
        cnt = sort_count(l, m) + sort_count(m + 1, r)
        tmp, i, j = [], l, m + 1
        while i <= m and j <= r:
            if a[i] <= a[j]:
                tmp.append(a[i]); i += 1
            else:
                cnt += m - i + 1
                tmp.append(a[j]); j += 1
        tmp += a[i:m + 1] + a[j:r + 1]
        a[l:r + 1] = tmp
        return cnt

    return sort_count(0, len(a) - 1)
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## Edge cases

- Sorted → 0; reverse sorted → n(n − 1)/2.
- Duplicates (equal pairs aren't inversions).
- Count overflows 32 bits for n ≈ 10⁵.

---

## Common mistakes

1. `<` instead of `<=` in the merge → equal pairs counted.
2. Adding 1 instead of `mid − i + 1`.
3. `int` counter.
4. Mutating the input without telling the interviewer.

---

## Follow-ups

1. Reverse pairs: nums[i] > 2·nums[j].
2. Count of smaller numbers after self (LC 315).
3. Minimum adjacent swaps to sort.

<details><summary>Answer sketches</summary>

**#1:** Count with a separate two-pointer pass before each merge: [Reverse Pairs](30-reverse-pairs.md).

**#2:** Merge sort on indices, adding the right-side count to each left element; or a Fenwick tree.

**#3:** That's exactly the inversion count.
</details>

---

## Flashcards

**Count inversions in O(n log n)?** #flashcard
Merge sort; when right[j] < left[i], add mid − i + 1.

**Why mid − i + 1?** #flashcard
The left half is sorted, so every remaining left element exceeds right[j].

**Inversions equal what in bubble sort?** #flashcard
The number of swaps.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
