---
module: striver-a2z/14-arrays
lesson: 33
topic: Check if array is sorted and rotated
difficulty: Easy
source: https://takeuforward.org/learning/dsa/check-if-the-array-is-sorted?category=easy&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, easy]
---
# 33. Check if array is sorted and rotated

← [Merge Two Sorted Arrays Without Extra Space](32-merge-sorted-arrays.md) · [Part 14 index](README.md) · Next → [Part 15: Hashing](../15-hashing/README.md)

> [!abstract] Problem at a glance
> **Task:** Return true if `nums` is a non-decreasing array rotated by some amount (0 counts).
> **Key insight:** Walk the array circularly and count the **drops**, places where `a[i] > a[(i+1) % n]`. A sorted array has 0 drops in a straight walk. A sorted array that was rotated has exactly one drop around the circle, at the rotation point, and the wrap from last to first has to be a non-drop. So the answer is `drops ≤ 1`. The plain "is it sorted" check is the same loop without the wrap, requiring `drops == 0`.
> **Difficulty:** Easy · **Pattern:** Single pass / circular scan · **Also on:** [LC 1752](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/check-if-the-array-is-sorted?category=easy&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Try every rotation](#3-try-every-rotation) · [4. Count circular drops](#4-count-circular-drops) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums`, return `true` if it was originally sorted in non-decreasing order and then rotated some number of positions (including zero). Duplicates are allowed.

| Input | Output | Why |
|---|---|---|
| `[3, 4, 5, 1, 2]` | `true` | rotation of [1, 2, 3, 4, 5] |
| `[2, 1, 3, 4]` | `false` | two drops: 2→1 and 4→2 (wrap) |
| `[1, 2, 3]` | `true` | rotation by 0 |

**Constraints:** `1 ≤ n ≤ 100`, `1 ≤ nums[i] ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Try every rotation | compare each rotation with sorted(nums) | O(n²) | O(n) |
| Count circular drops | drops where a[i] > a[(i+1)%n]; answer drops ≤ 1 | O(n) | O(1) |

> [!tip] Interview angle
> Start with the plain sorted check (`a[i-1] ≤ a[i]` for all i). Then extend it: try all n rotations against the sorted copy, which is O(n²). Then give the drop-count argument in one pass. Spell out the wrap-around comparison, because it is what catches `[2, 1, 3, 4]`.

---

## 3. Try every rotation

**Intuition.** Sort a copy. For each `k`, check whether `nums[k:] + nums[:k]` equals it.

```python
def check_brute(nums):
    s = sorted(nums)
    return any(nums[k:] + nums[:k] == s for k in range(len(nums)))
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. Count circular drops

**Intuition.** A non-decreasing circle that has been cut at one point has at most one descent, the cut. Count the descents, including the wrap from last to first.

**Algorithm**

1. `drops = 0`.
2. For `i` in `0..n-1`: if `a[i] > a[(i + 1) % n]`, `drops++`.
3. Return `drops ≤ 1`.

**Dry run** — [3,4,5,1,2]: 3≤4, 4≤5, 5>1 (drop 1), 1≤2, wrap 2≤3, so drops = 1 → true. [2,1,3,4]: 2>1 (1), 1≤3, 3≤4, wrap 4>2 (2), so drops = 2 → false.

**C++**
```cpp
bool check(vector<int>& nums) {
    int n = nums.size(), drops = 0;
    for (int i = 0; i < n; i++)
        if (nums[i] > nums[(i + 1) % n]) drops++;
    return drops <= 1;
}
```

**Java**
```java
static boolean check(int[] nums) {
    int n = nums.length, drops = 0;
    for (int i = 0; i < n; i++)
        if (nums[i] > nums[(i + 1) % n]) drops++;
    return drops <= 1;
}
```

**Python**
```python
def check(nums):
    n = len(nums)
    drops = sum(nums[i] > nums[(i + 1) % n] for i in range(n))
    return drops <= 1
```

**Complexity:** time **O(n)**, space **O(1)** — A rotation of a sorted array is two sorted runs `B A` with `last(A) ≤ first(B)`. Going around the circle, the only descent is between the end of `B` and the start of `A`. Conversely, if there is at most one descent, cutting the circle just after it gives a sorted array.

---

## Edge cases

- Single element: true.
- All equal: 0 drops, true.
- Duplicates around the cut, e.g. [6, 10, 6]: use `>` not `≥`.
- Two elements: always true.

---

## Common mistakes

1. Forgetting the wrap comparison: [2, 1, 3, 4] has one internal drop and would wrongly pass.
2. Counting `≥` as a drop, which breaks on duplicates.
3. Finding the minimum and checking from there: this fails with duplicates, e.g. [1, 1, 2, 1].

---

## Follow-ups

1. Return the rotation amount?
2. Strictly increasing required?

<details><summary>Answer sketches</summary>

**#1:** It is the index just after the single drop, or 0 if there is no drop.

**#2:** Count `≥` as a drop instead.
</details>

---

## Flashcards

**Sorted-and-rotated test?** #flashcard
Count circular drops a[i] > a[(i+1)%n]; true iff ≤ 1.

**Why include the wrap pair?** #flashcard
Without it, [2,1,3,4] looks like a valid rotation.

**Interview track →** 
