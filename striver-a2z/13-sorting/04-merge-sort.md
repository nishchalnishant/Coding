---
module: striver-a2z/13-sorting
lesson: 4
topic: Merge Sort
difficulty: Medium
source: https://takeuforward.org/learning/dsa/merge-sorting?category=algorithms&source=strivers-a2z-dsa-sheet
tags: [striver, algorithms, sorting, merge-sort, divide-and-conquer, recursion]
---
# 4. Merge Sort

← [Insertion Sort](03-insertion-sort.md) · [Part 13 index](README.md) · Next → [Quick Sort](05-quick-sort.md)

> [!abstract] Problem at a glance
> **Task:** Sort `nums` in place using merge sort.
> **Key insight:** Split in half, sort each half recursively, then merge the two sorted halves in O(n) with two pointers. The recursion tree has log n levels and each level does O(n) merge work, so it's O(n log n) in every case.
> **Difficulty:** Medium · **Pattern:** Divide and conquer
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/merge-sorting?category=algorithms&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Top-down recursive merge sort](#3-top-down-recursive-merge-sort) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, sort it in non-decreasing order using merge sort.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 4, 1, 5, 3]` | `[1, 3, 4, 5, 7]` |  |
| `nums = [5, 4, 4, 1, 1]` | `[1, 1, 4, 4, 5]` | duplicates |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁴ ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Top-down recursive merge sort | sort(l, m), sort(m+1, r), merge(l, m, r) | O(n log n) best / avg / worst | O(n) temp + O(log n) stack |

> [!tip] Interview angle
> Write `merge` as its own function; interviewers reuse it for follow-ups (count inversions, reverse pairs, count of smaller numbers after self, sort a linked list). Say "`<=` keeps it stable" as you write it.

---

## 3. Top-down recursive merge sort

**Intuition.** **Divide:** `m = l + (r − l) / 2`. **Conquer:** sort `[l, m]` and `[m + 1, r]`. **Combine:** two pointers over the halves, always taking the smaller head into a temp buffer, then copy the buffer back. A one-element range is already sorted (the base case).

**Algorithm**

1. `ms(l, r)`: if `l >= r` return.
2. `m = (l + r) / 2`; `ms(l, m)`; `ms(m + 1, r)`.
3. `merge(l, m, r)`: `i = l`, `j = m + 1`; push the smaller of `nums[i]`, `nums[j]` (ties → left) into `tmp`; append the leftovers; copy `tmp` into `nums[l..r]`.

**Dry run** — `[7 4 1 5 3]` → split `[7 4 1] [5 3]` → `[7] [4 1]` → `[4 1]` merges to `[1 4]` → `[7] + [1 4]` → `[1 4 7]`; `[5 3]` → `[3 5]`; final merge `[1 4 7] + [3 5]` → `[1 3 4 5 7]`.

**Recurrence:** T(n) = 2T(n/2) + O(n) → O(n log n) (master theorem, case 2). **Bottom-up variant:** merge widths 1, 2, 4, … iteratively, with no recursion stack. It's also the natural sort for linked lists (O(1) extra, [LC 148](https://leetcode.com/problems/sort-list/)).

**C++**
```cpp
void mergeHalves(vector<int>& nums, int l, int m, int r) {
    vector<int> tmp;
    tmp.reserve(r - l + 1);
    int i = l, j = m + 1;
    while (i <= m && j <= r)
        tmp.push_back(nums[i] <= nums[j] ? nums[i++] : nums[j++]);
    while (i <= m) tmp.push_back(nums[i++]);
    while (j <= r) tmp.push_back(nums[j++]);
    for (int k = 0; k < (int)tmp.size(); k++) nums[l + k] = tmp[k];
}
void ms(vector<int>& nums, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    ms(nums, l, m);
    ms(nums, m + 1, r);
    mergeHalves(nums, l, m, r);
}
void mergeSort(vector<int>& nums) { ms(nums, 0, (int)nums.size() - 1); }
```

**Java**
```java
static void mergeHalves(int[] nums, int l, int m, int r) {
    int[] tmp = new int[r - l + 1];
    int i = l, j = m + 1, k = 0;
    while (i <= m && j <= r)
        tmp[k++] = nums[i] <= nums[j] ? nums[i++] : nums[j++];
    while (i <= m) tmp[k++] = nums[i++];
    while (j <= r) tmp[k++] = nums[j++];
    System.arraycopy(tmp, 0, nums, l, tmp.length);
}
static void ms(int[] nums, int l, int r) {
    if (l >= r) return;
    int m = l + (r - l) / 2;
    ms(nums, l, m);
    ms(nums, m + 1, r);
    mergeHalves(nums, l, m, r);
}
static void mergeSort(int[] nums) { ms(nums, 0, nums.length - 1); }
```

**Python**
```python
def merge_sort(nums):
    def merge(l, m, r):
        tmp, i, j = [], l, m + 1
        while i <= m and j <= r:
            if nums[i] <= nums[j]:
                tmp.append(nums[i]); i += 1
            else:
                tmp.append(nums[j]); j += 1
        tmp.extend(nums[i:m + 1])
        tmp.extend(nums[j:r + 1])
        nums[l:r + 1] = tmp

    def ms(l, r):
        if l >= r:
            return
        m = (l + r) // 2
        ms(l, m)
        ms(m + 1, r)
        merge(l, m, r)

    ms(0, len(nums) - 1)
```

**Complexity:** time **O(n log n) best / avg / worst**, space **O(n) temp + O(log n) stack** — log₂ n levels × O(n) merge per level; recursion depth log n.

---

## Edge cases

- n = 1, and n = 2 in either order.
- Already sorted, reverse sorted.
- All equal; duplicates; negatives.
- n = 10⁵: depth is only ~17, so no stack risk.

---

## Common mistakes

1. `<` instead of `<=` in the merge: still sorted, but no longer stable.
2. Forgetting to copy the leftovers of one half.
3. Writing back to `nums[k]` instead of `nums[l + k]`.
4. `m = (l + r) / 2` overflow in C++/Java for huge indices; prefer `l + (r − l) / 2`.
5. Base case `l == r` only: correct here, but `l > r` (empty) must also return, so use `>=`.

---

## Follow-ups

1. Count inversions in O(n log n).
2. Reverse pairs (LC 493): count `i < j` with `nums[i] > 2·nums[j]`.
3. Sort a linked list (LC 148).
4. External sort for data that doesn't fit in RAM.

<details><summary>Answer sketches</summary>

**#1:** During the merge, when `nums[j] < nums[i]`, add `m − i + 1` (every remaining left element is larger).

**#2:** Before each merge, two-pointer count across the halves, then merge normally.

**#3:** Find the middle with slow/fast, split, sort both halves, merge. No random access needed.

**#4:** Sort chunks in memory, write runs to disk, k-way merge with a min-heap.
</details>

---

## Flashcards

**Merge sort recurrence and solution?** #flashcard
T(n) = 2T(n/2) + O(n) → O(n log n).

**What makes merge sort stable?** #flashcard
Taking from the left half on ties (<=).

**Merge sort extra space?** #flashcard
O(n) buffer + O(log n) stack (arrays); O(log n) for linked lists.

**Inversion count via merge?** #flashcard
When a right element goes first, add the number of remaining left elements (m − i + 1).

**Interview track →** [Sorting deep-dive](../../02-algorithms/00-sorting.md) · [Sorting walkthroughs](../../04-practice/algorithms/00-sorting.md)
