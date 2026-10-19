---
module: striver/09-basic-arrays
lesson: 4
topic: Reverse an Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/reverse-an-array?category=basic-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, basic-arrays, arrays, two-pointers]
---
# 4. Reverse an Array

← [Check if the Array is Sorted](03-check-if-the-array-is-sorted.md) · [Part 9 index](README.md) · Next → [Part 10: Basic Hashing](../10-basic-hashing/README.md)

> [!abstract] Problem at a glance
> **Task:** Reverse `nums` in place.
> **Key insight:** Swap `a[l]` and `a[r]` and move both pointers inward until they meet. Each element moves once, using O(1) extra space.
> **Difficulty:** Easy · **Pattern:** Two pointers (opposite ends)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/reverse-an-array?category=basic-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — copy backwards](#3-brute--copy-backwards) · [4. Optimal — two pointers](#4-optimal--two-pointers) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums`, reverse it in place. Element `i` should end up at index `n − 1 − i`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 4, 5]` | `[5, 4, 3, 2, 1]` | middle stays |
| `nums = [1, 2, 1, 1, 5, 1]` | `[1, 5, 1, 1, 2, 1]` |  |
| `nums = [1, 2]` | `[2, 1]` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`. Modify `nums`; return nothing.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — copy backwards | fill a new array from the end | O(n) | O(n) |
| Optimal — two pointers | swap ends, move inward | O(n) | O(1) |

> [!tip] Interview angle
> Say "in place, two pointers, stop when `l ≥ r`". The common follow-up is rotating by k, which is three reverses, so this function gets reused.

---

## 3. Brute — copy backwards

**Intuition.** Write `nums[n-1-i]` into `tmp[i]`, then copy back. Correct, but it uses a full extra array.

```python
def reverse_copy(nums):
    tmp = [nums[len(nums) - 1 - i] for i in range(len(nums))]
    nums[:] = tmp
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Optimal — two pointers

**Intuition.** The element at index `l` and the one at `r = n − 1 − l` swap places. Do it for every `l < r`. When `l == r` (odd n) the middle element is already in place.

**Algorithm**

1. `l = 0`, `r = n - 1`.
2. While `l < r`: swap `nums[l]`, `nums[r]`; `l += 1`; `r -= 1`.

**Dry run** — `[1, 2, 3, 4, 5]`

| l | r | array |
|---|---|---|
| 0 | 4 | 5 2 3 4 1 |
| 1 | 3 | 5 4 3 2 1 |
| 2 | 2 | stop |

**Library:** C++ `std::reverse(v.begin(), v.end())`; Python `nums.reverse()` (in place) or `nums[::-1]` (copy); Java has no `Arrays.reverse` for primitives, so write the loop, or use `Collections.reverse` on a `List`.

**C++**
```cpp
void reverseArray(vector<int>& nums) {
    int l = 0, r = (int)nums.size() - 1;
    while (l < r) swap(nums[l++], nums[r--]);
}
```

**Java**
```java
static void reverseArray(int[] nums) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int t = nums[l];
        nums[l++] = nums[r];
        nums[r--] = t;
    }
}
```

**Python**
```python
def reverse_array(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1
```

**Complexity:** time **O(n)**, space **O(1)** — n/2 swaps.

---

## Edge cases

- Odd n: the middle element is untouched.
- Even n: the pointers cross with no shared middle.
- `n = 0` in C++: cast `size()` to int before subtracting 1, or `r` becomes huge.

---

## Common mistakes

1. Looping `i` over the whole array and swapping `i` with `n-1-i`, which reverses twice and restores the original.
2. Using `l <= r`. Harmless (it swaps the middle with itself), but sloppy.
3. `size_t r = nums.size() - 1` on an empty vector underflows.

---

## Follow-ups

1. Rotate an array right by k (LC 189).
2. Reverse a subarray `[i, j]`.
3. Reverse the words in a string (LC 151).

<details><summary>Answer sketches</summary>

**#1:** Reverse all, reverse the first k, reverse the rest, with `k %= n` first. O(n), O(1).

**#2:** Same loop with `l = i`, `r = j`.

**#3:** Reverse the whole char array, then reverse each word.
</details>

---

## Flashcards

**In-place reverse loop condition?** #flashcard
`while l < r` — swap and move both inward.

**Rotate right by k with reverses?** #flashcard
reverse(all), reverse(0..k-1), reverse(k..n-1), with k %= n.

**How many swaps does reversing take?** #flashcard
⌊n/2⌋.

**Interview track →** [Arrays deep-dive](../../01-data-structures/01-array.md) · [Two pointers](../../02-algorithms/03-two-pointers.md) · [Concept: basic arrays](../07-concept-basics/02-basic-arrays.md)
