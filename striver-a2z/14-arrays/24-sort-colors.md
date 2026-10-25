---
module: striver-a2z/14-arrays
lesson: 24
topic: Sort an Array of 0s, 1s and 2s
difficulty: Medium
source: https://takeuforward.org/learning/dsa/sort-an-array-of-0's-1's-and-2's?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, dutch-national-flag, two-pointers, in-place]
---
# 24. Sort an Array of 0s, 1s and 2s

← [4 Sum](23-4-sum.md) · [Part 14 index](README.md) · Next → [Kadane's Algorithm: Maximum Subarray Sum](25-kadanes-algorithm.md)

> [!abstract] Problem at a glance
> **Task:** Sort an array containing only 0, 1, 2 in place, in one pass.
> **Key insight:** Dutch National Flag: three pointers `low`, `mid`, `high`. `[0, low)` holds 0s, `[low, mid)` 1s, `(high, n)` 2s, and `[mid, high]` is unknown. A 0 at `mid` swaps to `low` (both advance), a 1 just advances `mid`, a 2 swaps to `high` (only `high` moves, because the swapped-in value is unexamined).
> **Difficulty:** Medium · **Pattern:** Dutch National Flag · **Also on:** [LC 75](https://leetcode.com/problems/sort-colors/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sort-an-array-of-0's-1's-and-2's?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Library sort](#3-library-sort) · [4. Counting](#4-counting) · [5. Dutch National Flag](#5-dutch-national-flag) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of 0s, 1s and 2s, sort it in place so equal values are adjacent in the order 0, 1, 2, without a library sort.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 0, 2, 1, 0]` | `[0, 0, 1, 1, 2]` |  |
| `nums = [2, 0, 1]` | `[0, 1, 2]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `nums[i] ∈ {0, 1, 2}`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Library sort | sort | O(n log n) | O(1)–O(n) |
| Counting | count 0/1/2, overwrite | O(n), two passes | O(1) |
| Dutch National Flag | low/mid/high; 0 → swap low, 1 → skip, 2 → swap high | O(n), one pass | O(1) |

---

## 3. Library sort

**Intuition.** Works, but ignores the three-value structure and is explicitly disallowed.

```python
def sort_colors_lib(nums):
    nums.sort()
```

**Complexity:** time **O(n log n)**, space **O(1)–O(n)**.

---

## 4. Counting

**Intuition.** Count each value, then write that many 0s, 1s and 2s. Fine, but the follow-up asks for one pass.

```python
def sort_colors_count(nums):
    c = [nums.count(v) for v in range(3)]
    nums[:] = [0] * c[0] + [1] * c[1] + [2] * c[2]
```

**Complexity:** time **O(n), two passes**, space **O(1)**.

---

## 5. Dutch National Flag

**Intuition.** Each step shrinks the unknown region `[mid, high]` by one. Swapping with `low` brings back a value known to be 1 (or `mid == low`), so `mid` may advance. Swapping with `high` brings back an unknown value, so `mid` must stay and examine it.

**Dry run** — `[1 0 2 1 0]` l=0 m=0 h=4: 1 → m=1; 0 → swap(0,1) `[0 1 2 1 0]` l=1 m=2; 2 → swap(2,4) `[0 1 0 1 2]` h=3; 0 → swap(1,2) `[0 0 1 1 2]` l=2 m=3; 1 → m=4 > h. Done.

Same partition idea as 3-way quicksort (Dijkstra's), which handles many duplicate keys in O(n) per level.

**C++**
```cpp
void sortColors(vector<int>& nums) {
    int low = 0, mid = 0, high = nums.size() - 1;
    while (mid <= high) {
        if (nums[mid] == 0) swap(nums[low++], nums[mid++]);
        else if (nums[mid] == 1) mid++;
        else swap(nums[mid], nums[high--]);
    }
}
```

**Java**
```java
static void sortColors(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            int t = nums[low]; nums[low++] = nums[mid]; nums[mid++] = t;
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            int t = nums[high]; nums[high--] = nums[mid]; nums[mid] = t;
        }
    }
}
```

**Python**
```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

**Complexity:** time **O(n), one pass**, space **O(1)**.

---

## Edge cases

- All one value.
- Already sorted / reverse sorted.
- n = 1.

---

## Common mistakes

1. `mid++` after swapping with `high` → the swapped-in 2 or 0 is never examined.
2. Loop condition `mid < high` → misses the last unknown element.
3. Counting sort is accepted only if two passes are allowed.

---

## Follow-ups

1. Sort k colours (LintCode 143).
2. Partition around a pivot into <, =, >.

<details><summary>Answer sketches</summary>

**#1:** Counting O(n + k), or recursive partitioning by colour range O(n log k).

**#2:** The same three pointers, comparing with the pivot.
</details>

---

## Flashcards

**Dutch flag pointers and regions?** #flashcard
[0, low) 0s · [low, mid) 1s · [mid, high] unknown · (high, n) 2s.

**Dutch flag: why doesn't mid advance on a 2?** #flashcard
The value swapped in from high is unexamined.

**Dutch flag loop condition?** #flashcard
while mid <= high.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
