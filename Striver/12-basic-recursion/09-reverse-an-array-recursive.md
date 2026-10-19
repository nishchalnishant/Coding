---
module: striver/12-basic-recursion
lesson: 9
topic: Reverse an Array (Recursive)
difficulty: Easy
source: https://takeuforward.org/learning/dsa/reverse-an-array-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet
tags: [striver, basic-recursion, recursion, arrays, two-pointers]
---
# 9. Reverse an Array (Recursive)

← [Check if a Number is Prime or Not](08-check-if-a-number-is-prime.md) · [Part 12 index](README.md) · Next → [Check if the Array is Sorted](10-check-if-the-array-is-sorted-recursive.md)

> [!abstract] Problem at a glance
> **Task:** Reverse `nums` in place, using recursion.
> **Key insight:** The same two-ended recursion as the string: swap `nums[l]` and `nums[r]`, then call `f(l + 1, r − 1)`. A single-index version is `f(i)` swapping `i` with `n − 1 − i` until `i ≥ n/2`.
> **Difficulty:** Easy · **Pattern:** Two-ended recursion
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-an-array-ii?category=basic-recursion&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Two indices (l, r)](#3-two-indices-l-r) · [4. Single index i](#4-single-index-i) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums`, reverse it in place using recursion.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 4, 5]` | `[5, 4, 3, 2, 1]` |  |
| `nums = [1, 2]` | `[2, 1]` |  |
| `nums = [7]` | `[7]` |  |

**Constraints:** `1 ≤ n ≤ 10³`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Two indices (l, r) | swap(l, r); f(l + 1, r − 1) | O(n) | O(n) stack |
| Single index i | swap(i, n−1−i); f(i + 1) | O(n) | O(n) stack |

---

## 3. Two indices (l, r)

**Intuition.** Mirrors the iterative two-pointer.

```python
def rev_lr(nums, l=0, r=None):
    if r is None:
        r = len(nums) - 1
    if l >= r:
        return
    nums[l], nums[r] = nums[r], nums[l]
    rev_lr(nums, l + 1, r - 1)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## 4. Single index i

**Intuition.** The right pointer is always `n − 1 − i`, so it doesn't need to be a parameter. Stop at `i ≥ n/2`.

**Algorithm**

1. `f(i)`: if `i >= n / 2` return.
2. Swap `nums[i]` and `nums[n − 1 − i]`.
3. `f(i + 1)`.

**Dry run** — `[1 2 3 4 5]`, n/2 = 2: i = 0 → `5 2 3 4 1`; i = 1 → `5 4 3 2 1`; i = 2 stop.

**C++**
```cpp
void revFrom(vector<int>& nums, int i) {
    int n = nums.size();
    if (i >= n / 2) return;
    swap(nums[i], nums[n - 1 - i]);
    revFrom(nums, i + 1);
}
void reverseArray(vector<int>& nums) { revFrom(nums, 0); }
```

**Java**
```java
static void revFrom(int[] nums, int i) {
    int n = nums.length;
    if (i >= n / 2) return;
    int t = nums[i]; nums[i] = nums[n - 1 - i]; nums[n - 1 - i] = t;
    revFrom(nums, i + 1);
}
static void reverseArray(int[] nums) { revFrom(nums, 0); }
```

**Python**
```python
def reverse_array(nums, i=0):
    n = len(nums)
    if i >= n // 2:
        return
    nums[i], nums[n - 1 - i] = nums[n - 1 - i], nums[i]
    reverse_array(nums, i + 1)
```

**Complexity:** time **O(n)**, space **O(n) stack**.

---

## Edge cases

- n = 1: zero swaps.
- Even n: the last swap is at `i = n/2 − 1`.

---

## Common mistakes

1. Stopping at `i >= n` instead of `n/2`: it swaps everything twice and leaves the array unchanged.
2. Returning a new array when the task is in place.

---

## Follow-ups

1. Reverse a subarray `[a, b]`.
2. Rotate an array by k (LC 189).

<details><summary>Answer sketches</summary>

**#1:** Call the `(l, r)` version with `(a, b)`.

**#2:** Three reversals: the whole array, then `[0, k−1]`, then `[k, n−1]` ([Part 14](../14-arrays/README.md)).
</details>

---

## Flashcards

**Single-index array reverse stop condition?** #flashcard
i >= n/2.

**What happens if you swap up to i < n?** #flashcard
Each pair is swapped twice, so the array is unchanged.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md)
