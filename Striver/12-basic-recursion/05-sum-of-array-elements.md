---
module: striver/12-basic-recursion
lesson: 5
topic: Sum of Array Elements
difficulty: Easy
source: https://takeuforward.org/learning/dsa/sum-of-array-elements-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, arrays]
---
# 5. Sum of Array Elements

← [Factorial of a Given Number](04-factorial-of-a-given-number.md) · [Part 12 index](README.md) · Next → [Reverse a String (Recursive)](06-reverse-a-string-recursive.md)

> [!abstract] Problem at a glance
> **Task:** Return the sum of `nums` using recursion.
> **Key insight:** Recurse on an **index**, not a slice: `f(i) = nums[i] + f(i + 1)`, `f(n) = 0`. Slicing makes it O(n²).
> **Difficulty:** Easy · **Pattern:** Linear recursion over an index
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-array-elements-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — recursion on slices](#3-brute--recursion-on-slices) · [4. Optimal — recursion on an index](#4-optimal--recursion-on-an-index) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the sum of its elements, recursively.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3]` | `6` |  |
| `nums = [-1, 2, -3, 4]` | `2` |  |
| `nums = [5]` | `5` |  |

**Constraints:** `1 ≤ n ≤ 10³`, `−10⁴ ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — recursion on slices | nums[0] + f(nums[1:]) | O(n²) | O(n²) total copies |
| Optimal — recursion on an index | f(i) = nums[i] + f(i + 1) | O(n) | O(n) stack |

---

## 3. Brute — recursion on slices

**Intuition.** Reads naturally, but each slice copies the rest of the array.

```python
def sum_slice(nums):
    if not nums:
        return 0
    return nums[0] + sum_slice(nums[1:])
```

**Complexity:** time **O(n²)**, space **O(n²) total copies**.

---

## 4. Optimal — recursion on an index

**Intuition.** The index `i` marks the start of the remaining suffix, so nothing is copied. The base `i == n` is the empty suffix with sum 0.

**Algorithm**

1. Helper `f(i)`: if `i == n` return 0.
2. Return `nums[i] + f(i + 1)`.
3. Answer = `f(0)`.

**Dry run** — `[1, 2, 3]`: f(0) = 1 + f(1) = 1 + 2 + f(2) = 1 + 2 + 3 + f(3) = 6.

**C++**
```cpp
int sumFrom(vector<int>& nums, int i) {
    if (i == (int)nums.size()) return 0;
    return nums[i] + sumFrom(nums, i + 1);
}
int arraySum(vector<int>& nums) { return sumFrom(nums, 0); }
```

**Java**
```java
static int sumFrom(int[] nums, int i) {
    if (i == nums.length) return 0;
    return nums[i] + sumFrom(nums, i + 1);
}
static int arraySum(int[] nums) { return sumFrom(nums, 0); }
```

**Python**
```python
def array_sum(nums, i=0):
    if i == len(nums):
        return 0
    return nums[i] + array_sum(nums, i + 1)
```

**Complexity:** time **O(n)**, space **O(n) stack** — in C++, pass the vector by reference or every call copies it.

---

## Edge cases

- Single element.
- Negatives cancel out.

---

## Common mistakes

1. Slicing per call (O(n²)).
2. C++ `vector<int> nums` by value in the helper, which copies at every level.
3. Base `i == n − 1 → nums[i]` crashes on an empty array.

---

## Follow-ups

1. Recursive max of an array.
2. Make the stack depth O(log n).

<details><summary>Answer sketches</summary>

**#1:** `max(nums[i], f(i + 1))`, base `i == n − 1 → nums[i]`.

**#2:** Divide and conquer: `f(l, r) = f(l, m) + f(m + 1, r)`.
</details>

---

## Flashcards

**Why recurse on an index rather than a slice?** #flashcard
A slice copies O(n) per call → O(n²).

**Array-sum recursion base case?** #flashcard
i == n → 0.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
