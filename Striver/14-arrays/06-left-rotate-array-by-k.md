---
module: striver/14-arrays
lesson: 6
topic: Left Rotate Array by K Places
difficulty: Easy
source: https://takeuforward.org/learning/dsa/left-rotate-array?category=fundamentals&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, rotation, reversal, in-place]
---
# 6. Left Rotate Array by K Places

← [Left Rotate Array by One](05-left-rotate-array-by-one.md) · [Part 14 index](README.md) · Next → [Move Zeros to End](07-move-zeros-to-end.md)

> [!abstract] Problem at a glance
> **Task:** Rotate `nums` left by `k` positions in place.
> **Key insight:** Reduce `k %= n`. Then reverse `[0, k)`, reverse `[k, n)`, reverse the whole array. Three reversals give O(n) time with O(1) extra space.
> **Difficulty:** Easy · **Pattern:** Reversal trick · **Also on:** [LC 189](https://leetcode.com/problems/rotate-array/) (right rotation)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/left-rotate-array?category=fundamentals&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Rotate by one, k times](#3-rotate-by-one-k-times) · [4. Temp array (Striver's brute)](#4-temp-array-strivers-brute) · [5. Three reversals](#5-three-reversals) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` and a non-negative integer `k`, rotate the array to the left by `k` steps in place. `k` may be larger than `n`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 4, 5, 6], k = 2` | `[3, 4, 5, 6, 1, 2]` |  |
| `nums = [3, 4, 1, 5], k = 6` | `[1, 5, 3, 4]` | 6 % 4 = 2 |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ k ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Rotate by one, k times | repeat the previous problem | O(n · k) | O(1) |
| Temp array (Striver's brute) | copy first k, shift rest, paste | O(n) | O(k) |
| Three reversals | rev(0,k−1), rev(k,n−1), rev(0,n−1) | O(n) | O(1) |

---

## 3. Rotate by one, k times

**Intuition.** Correct after `k %= n`, but O(n²) in the worst case.

```python
def rotate_k_naive(nums, k):
    n = len(nums)
    for _ in range(k % n):
        first = nums[0]
        for i in range(1, n):
            nums[i - 1] = nums[i]
        nums[-1] = first
```

**Complexity:** time **O(n · k)**, space **O(1)**.

---

## 4. Temp array (Striver's brute)

**Intuition.** Save `nums[0..k)` in `temp`, move `nums[k..n)` to the front, then copy `temp` into the last `k` slots.

```python
def rotate_k_temp(nums, k):
    n = len(nums)
    k %= n
    temp = nums[:k]
    for i in range(k, n):
        nums[i - k] = nums[i]
    for i in range(k):
        nums[n - k + i] = temp[i]
```

**Complexity:** time **O(n)**, space **O(k)**.

---

## 5. Three reversals

**Intuition.** Write the array as `A B` with `|A| = k`. We want `B A`. Reversing each part gives `Aᴿ Bᴿ`; reversing the whole gives `(Aᴿ Bᴿ)ᴿ = B A`. Each element is swapped about twice.

**Algorithm**

1. `k %= n`.
2. Reverse `nums[0 .. k − 1]`.
3. Reverse `nums[k .. n − 1]`.
4. Reverse `nums[0 .. n − 1]`.

**Dry run** — `[1 2 3 4 5 6]`, k = 2 → `[2 1 | 6 5 4 3]` → reverse all → `[3 4 5 6 1 2]`.

**Right rotation (LC 189)** is the mirror: reverse all, then `[0, k)`, then `[k, n)`. Or left-rotate by `n − k`. **Juggling (GCD) algorithm** also gives O(n)/O(1) by following gcd(n, k) cycles, but it's harder to get right in an interview.

**C++**
```cpp
void reverseRange(vector<int>& a, int l, int r) {
    while (l < r) swap(a[l++], a[r--]);
}
void rotateArray(vector<int>& nums, int k) {
    int n = nums.size();
    k %= n;
    reverseRange(nums, 0, k - 1);
    reverseRange(nums, k, n - 1);
    reverseRange(nums, 0, n - 1);
}
```

**Java**
```java
static void reverseRange(int[] a, int l, int r) {
    while (l < r) { int t = a[l]; a[l++] = a[r]; a[r--] = t; }
}
static void rotateArray(int[] nums, int k) {
    int n = nums.length;
    k %= n;
    reverseRange(nums, 0, k - 1);
    reverseRange(nums, k, n - 1);
    reverseRange(nums, 0, n - 1);
}
```

**Python**
```python
def rotate_left(nums, k):
    def rev(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1

    n = len(nums)
    k %= n
    rev(0, k - 1)
    rev(k, n - 1)
    rev(0, n - 1)
```

**Complexity:** time **O(n)**, space **O(1)** — three linear passes, swaps only.

---

## Edge cases

- k = 0, k = n, k a multiple of n → unchanged.
- k > n → reduce first.
- n = 1.

---

## Common mistakes

1. Forgetting `k %= n` → out-of-range indices.
2. Mixing up left and right rotation order of the reversals.
3. Python: `nums = nums[k:] + nums[:k]` rebinds a local; the caller's list is unchanged. Use `nums[:] = …`.

---

## Follow-ups

1. Rotate right by k (LC 189).
2. Rotate a string / check if one string is a rotation of another.
3. Rotate a linked list by k (LC 61).

<details><summary>Answer sketches</summary>

**#1:** Reverse all, reverse `[0, k)`, reverse `[k, n)`.

**#2:** `goal in s + s` with equal lengths ([Part 11](../11-basic-strings/README.md)).

**#3:** Make it circular, then break at `n − k % n`.
</details>

---

## Flashcards

**Left rotate by k with O(1) space?** #flashcard
rev(0, k−1), rev(k, n−1), rev(0, n−1) after k %= n.

**Why do three reversals work?** #flashcard
(Aᴿ Bᴿ)ᴿ = B A.

**First step of any rotate-by-k?** #flashcard
k %= n.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
