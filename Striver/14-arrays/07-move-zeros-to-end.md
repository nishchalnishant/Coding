---
module: striver/14-arrays
lesson: 7
topic: Move Zeros to End
difficulty: Easy
source: https://takeuforward.org/learning/dsa/move-zeros-to-end?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, two-pointers, in-place]
---
# 7. Move Zeros to End

← [Left Rotate Array by K Places](06-left-rotate-array-by-k.md) · [Part 14 index](README.md) · Next → [Remove Duplicates from Sorted Array](08-remove-duplicates-from-sorted-array.md)

> [!abstract] Problem at a glance
> **Task:** Move all zeros to the end of `nums` in place, keeping the relative order of the non-zero elements.
> **Key insight:** Two pointers: `j` marks where the next non-zero belongs. For each non-zero at `i`, swap it into `j` and advance `j`. Order is preserved and the zeros collect at the back.
> **Difficulty:** Easy · **Pattern:** Two pointers: read/write · **Also on:** [LC 283](https://leetcode.com/problems/move-zeroes/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/move-zeros-to-end?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Temp array](#3-temp-array) · [4. Two pointers (write index)](#4-two-pointers-write-index) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, move all `0`s to the end while maintaining the relative order of the non-zero elements. Do it in place.

| Input | Output | Why |
|---|---|---|
| `nums = [0, 1, 4, 0, 5, 2]` | `[1, 4, 5, 2, 0, 0]` |  |
| `nums = [0, 0, 1]` | `[1, 0, 0]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Temp array | collect non-zeros, then pad with zeros | O(n) | O(n) |
| Two pointers (write index) | swap each non-zero into position j | O(n) | O(1) |

---

## 3. Temp array

**Intuition.** Copy the non-zero values into `temp`, write them back to the front, and fill the rest with 0.

```python
def move_zeros_temp(nums):
    temp = [x for x in nums if x != 0]
    for i in range(len(nums)):
        nums[i] = temp[i] if i < len(temp) else 0
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Two pointers (write index)

**Intuition.** Invariant: `nums[0..j)` holds the non-zeros seen so far, in order, and `nums[j..i)` is all zeros. When `nums[i] != 0`, swapping it with `nums[j]` extends the non-zero prefix and moves a zero right. This is the same read/write pattern as [Remove Duplicates](#).

**Dry run** — `[0 1 4 0 5 2]`: i=1 swap(0,1) → `[1 0 4 0 5 2]` j=1; i=2 swap → `[1 4 0 0 5 2]` j=2; i=4 → `[1 4 5 0 0 2]` j=3; i=5 → `[1 4 5 2 0 0]`.

**Fewer writes variant:** copy each non-zero to `nums[j++]` (no swap), then zero-fill `[j, n)`. Same O(n), and simpler to reason about.

**C++**
```cpp
void moveZeroes(vector<int>& nums) {
    int j = 0;
    for (int i = 0; i < (int)nums.size(); i++)
        if (nums[i] != 0) swap(nums[i], nums[j++]);
}
```

**Java**
```java
static void moveZeroes(int[] nums) {
    int j = 0;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] != 0) {
            int t = nums[i]; nums[i] = nums[j]; nums[j] = t;
            j++;
        }
    }
}
```

**Python**
```python
def move_zeroes(nums):
    j = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[i], nums[j] = nums[j], nums[i]
            j += 1
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- No zeros / all zeros.
- Single element.
- Negative values (only 0 is special).

---

## Common mistakes

1. Swapping zeros with the *next* non-zero using nested loops → O(n²).
2. Comparing `nums[j] == 0` instead of tracking the write index.
3. Breaking the relative order with a two-ends approach (only fine if order doesn't matter).

---

## Follow-ups

1. Move zeros to the front instead?
2. Order doesn't matter: fewest writes?
3. Partition into negatives then non-negatives, stable?

<details><summary>Answer sketches</summary>

**#1:** Iterate from the right with the write index starting at n − 1.

**#2:** Two pointers from both ends: swap a left zero with a right non-zero.

**#3:** Not O(1) space stable in O(n); use extra space, or accept O(n log n) stable partition.
</details>

---

## Flashcards

**Move zeros pattern?** #flashcard
Write index j; swap each non-zero into j, j++.

**Move zeros invariant?** #flashcard
nums[0..j) non-zeros in order; nums[j..i) zeros.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
