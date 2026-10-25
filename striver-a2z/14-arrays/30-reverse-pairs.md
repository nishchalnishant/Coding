---
module: striver-a2z/14-arrays
lesson: 30
topic: Reverse Pairs
difficulty: Hard
source: https://takeuforward.org/learning/dsa/reverse-pairs?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, merge-sort, divide-and-conquer]
---
# 30. Reverse Pairs

← [Count Inversions](29-count-inversions.md) · [Part 14 index](README.md) · Next → [Maximum Product Subarray](31-maximum-product-subarray.md)

> [!abstract] Problem at a glance
> **Task:** Count pairs `(i, j)` with `i < j` and `nums[i] > 2 · nums[j]`.
> **Key insight:** Merge-sort counting again, but the condition isn't the merge's comparison. So before each merge, count with a separate two-pointer pass over the two sorted halves (`j` only moves forward), then merge normally. Use 64-bit for `2 · nums[j]`.
> **Difficulty:** Hard · **Pattern:** Merge sort counting · **Also on:** [LC 493](https://leetcode.com/problems/reverse-pairs/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-pairs?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All pairs](#3-all-pairs) · [4. Merge sort + separate counting pass](#4-merge-sort--separate-counting-pass) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the number of reverse pairs: pairs `(i, j)` with `0 ≤ i < j < n` and `nums[i] > 2 · nums[j]`.

| Input | Output | Why |
|---|---|---|
| `nums = [6, 4, 1, 2, 7]` | `3` | (6,1) (6,2) (4,1) |
| `nums = [5, 4, 4, 3, 3]` | `0` |  |

**Constraints:** `1 ≤ n ≤ 5·10⁴`, `−2³¹ ≤ nums[i] ≤ 2³¹ − 1`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All pairs | nested loops | O(n²) | O(1) |
| Merge sort + separate counting pass | for each left i, advance j while left[i] > 2·right[j] | O(n log n) | O(n) |

---

## 3. All pairs

**Intuition.** Check the condition for every `i < j`.

```python
def reverse_pairs_brute(nums):
    n = len(nums)
    return sum(1 for i in range(n) for j in range(i + 1, n) if nums[i] > 2 * nums[j])
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Merge sort + separate counting pass

**Intuition.** With both halves sorted, as `i` moves right in the left half `nums[i]` grows, so the set of right elements with `nums[i] > 2·nums[j]` only grows. One pointer `j` that never moves back counts all cross pairs in O(n). Counting must happen before merging, because the merge interleaves the halves.

**Algorithm**

1. Recurse on `[l, m]` and `[m + 1, r]`.
2. `j = m + 1`; for `i` in `l..m`: while `j <= r and nums[i] > 2·nums[j]`: `j++`. Add `j − (m + 1)`.
3. Merge the halves normally.

**C++**
```cpp
void mergeHalves(vector<int>& a, int l, int m, int r) {
    vector<int> tmp;
    int i = l, j = m + 1;
    while (i <= m && j <= r) tmp.push_back(a[i] <= a[j] ? a[i++] : a[j++]);
    while (i <= m) tmp.push_back(a[i++]);
    while (j <= r) tmp.push_back(a[j++]);
    for (int k = l; k <= r; k++) a[k] = tmp[k - l];
}
int countCross(vector<int>& a, int l, int m, int r) {
    int cnt = 0, j = m + 1;
    for (int i = l; i <= m; i++) {
        while (j <= r && (long long)a[i] > 2LL * a[j]) j++;
        cnt += j - (m + 1);
    }
    return cnt;
}
int sortCountRP(vector<int>& a, int l, int r) {
    if (l >= r) return 0;
    int m = l + (r - l) / 2;
    int cnt = sortCountRP(a, l, m) + sortCountRP(a, m + 1, r) + countCross(a, l, m, r);
    mergeHalves(a, l, m, r);
    return cnt;
}
int reversePairs(vector<int>& nums) {
    vector<int> a = nums;
    return sortCountRP(a, 0, (int)a.size() - 1);
}
```

**Java**
```java
static void mergeHalves(int[] a, int l, int m, int r) {
    int[] tmp = new int[r - l + 1];
    int i = l, j = m + 1, k = 0;
    while (i <= m && j <= r) tmp[k++] = a[i] <= a[j] ? a[i++] : a[j++];
    while (i <= m) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    System.arraycopy(tmp, 0, a, l, tmp.length);
}
static int countCross(int[] a, int l, int m, int r) {
    int cnt = 0, j = m + 1;
    for (int i = l; i <= m; i++) {
        while (j <= r && (long) a[i] > 2L * a[j]) j++;
        cnt += j - (m + 1);
    }
    return cnt;
}
static int sortCountRP(int[] a, int l, int r) {
    if (l >= r) return 0;
    int m = l + (r - l) / 2;
    int cnt = sortCountRP(a, l, m) + sortCountRP(a, m + 1, r) + countCross(a, l, m, r);
    mergeHalves(a, l, m, r);
    return cnt;
}
static int reversePairs(int[] nums) {
    int[] a = nums.clone();
    return sortCountRP(a, 0, a.length - 1);
}
```

**Python**
```python
def reverse_pairs(nums):
    a = list(nums)

    def sort_count(l, r):
        if l >= r:
            return 0
        m = (l + r) // 2
        cnt = sort_count(l, m) + sort_count(m + 1, r)
        j = m + 1
        for i in range(l, m + 1):
            while j <= r and a[i] > 2 * a[j]:
                j += 1
            cnt += j - (m + 1)
        a[l:r + 1] = sorted(a[l:r + 1])   # or a linear merge
        return cnt

    return sort_count(0, len(a) - 1)
```

**Complexity:** time **O(n log n)**, space **O(n)**.

---

## Edge cases

- Negative numbers (−5 > 2·(−5) = −10 is a pair).
- INT_MAX: `2 · nums[j]` overflows 32 bits.
- n = 1.

---

## Common mistakes

1. Counting inside the merge loop with the merge's comparison (that counts inversions, not reverse pairs).
2. Resetting `j` for each `i` → O(n²) per level.
3. 32-bit `2 * nums[j]`.

---

## Follow-ups

1. Count pairs with nums[i] > k · nums[j] for any k.
2. Count range sums in [lo, hi] (LC 327).
3. Alternative data structure.

<details><summary>Answer sketches</summary>

**#1:** Same counting pass with `k · nums[j]`.

**#2:** Merge sort on prefix sums with two forward pointers.

**#3:** Fenwick / BIT over coordinate-compressed values of `nums` and `2·nums`.
</details>

---

## Flashcards

**Reverse pairs approach?** #flashcard
Merge sort; separate two-pointer count before each merge.

**Why count separately from the merge?** #flashcard
The condition (> 2·x) differs from the merge order (≤).

**Reverse pairs overflow?** #flashcard
2 · nums[j] needs 64-bit.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
