---
module: striver-a2z/14-arrays
lesson: 5
topic: Left Rotate Array by One
difficulty: Easy
source: https://takeuforward.org/learning/dsa/left-rotate-array-by-one?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, rotation, in-place]
---
# 5. Left Rotate Array by One

← [Maximum Consecutive Ones](04-maximum-consecutive-ones.md) · [Part 14 index](README.md) · Next → [Left Rotate Array by K Places](06-left-rotate-array-by-k.md)

> [!abstract] Problem at a glance
> **Task:** Shift every element of `nums` one place left, in place; the first element moves to the end.
> **Key insight:** Save `nums[0]`, shift `nums[1..n−1]` left by one, put the saved value at `n − 1`. One temporary, O(n).
> **Difficulty:** Easy · **Pattern:** In-place array shifting
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/left-rotate-array-by-one?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Save first, shift, place](#3-save-first-shift-place) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, rotate it left by one position in place.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 4, 5]` | `[2, 3, 4, 5, 1]` |  |
| `nums = [-1, 0, 3, 6]` | `[0, 3, 6, -1]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Save first, shift, place | temp = nums[0]; shift left; nums[n−1] = temp | O(n) | O(1) |

---

## 3. Save first, shift, place

**Intuition.** Shifting left overwrites `nums[0]` first, so save it before the loop. The loop must go left to right; going right to left would smear one value across the array.

**C++**
```cpp
void rotateArrayByOne(vector<int>& nums) {
    int n = nums.size(), first = nums[0];
    for (int i = 1; i < n; i++) nums[i - 1] = nums[i];
    nums[n - 1] = first;
}
```

**Java**
```java
static void rotateArrayByOne(int[] nums) {
    int n = nums.length, first = nums[0];
    for (int i = 1; i < n; i++) nums[i - 1] = nums[i];
    nums[n - 1] = first;
}
```

**Python**
```python
def rotate_by_one(nums):
    first = nums[0]
    for i in range(1, len(nums)):
        nums[i - 1] = nums[i]
    nums[-1] = first
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- n = 1: unchanged.

---

## Common mistakes

1. Not saving `nums[0]` before overwriting it.
2. Iterating right to left when shifting left.

---

## Follow-ups

1. Right rotate by one?
2. Python one-liner (not in place)?

<details><summary>Answer sketches</summary>

**#1:** Save `nums[n − 1]`, shift right going right to left, put it at index 0.

**#2:** `nums[:] = nums[1:] + nums[:1]`, which is O(n) extra space.
</details>

---

## Flashcards

**Left rotate by one: what do you save?** #flashcard
nums[0], placed at n − 1 after the shift.

**Shift-left loop direction?** #flashcard
Left to right (i = 1 .. n − 1: nums[i − 1] = nums[i]).

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
