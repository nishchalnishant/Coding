---
module: striver-a2z/14-arrays
lesson: 9
topic: Find Missing Number
difficulty: Easy
source: https://takeuforward.org/learning/dsa/find-missing-number?category=logic-building&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, math, xor, bit-manipulation]
---
# 9. Find Missing Number

← [Remove Duplicates from Sorted Array](08-remove-duplicates-from-sorted-array.md) · [Part 14 index](README.md) · Next → [Union of Two Sorted Arrays](10-union-of-two-sorted-arrays.md)

> [!abstract] Problem at a glance
> **Task:** `nums` holds `n` distinct numbers from `0..n`; return the one that's missing.
> **Key insight:** The expected total is `n(n + 1)/2`, so the missing number is that minus `sum(nums)`. The XOR version, `XOR(0..n) ^ XOR(nums)`, cancels every present value and can't overflow.
> **Difficulty:** Easy · **Pattern:** Math / XOR cancellation · **Also on:** [LC 268](https://leetcode.com/problems/missing-number/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-missing-number?category=logic-building&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Check each candidate](#3-check-each-candidate) · [4. Presence array](#4-presence-array) · [5. Sum formula](#5-sum-formula) · [6. XOR](#6-xor) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of `n` distinct integers in the range `[0, n]`, return the only number in the range that is missing.

| Input | Output | Why |
|---|---|---|
| `nums = [0, 2, 3, 1, 4]` | `5` | n = 5, range 0..5 |
| `nums = [0, 1, 2, 4, 5, 6]` | `3` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`, distinct values in `[0, n]`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Check each candidate | for v in 0..n, linear search | O(n²) | O(1) |
| Presence array | mark seen[v], find the unmarked | O(n) | O(n) |
| Sum formula | n(n+1)/2 − sum | O(n) | O(1) |
| XOR | XOR of 0..n and all nums | O(n) | O(1) |

---

## 3. Check each candidate

**Intuition.** For every candidate, scan the array. It's the obvious brute force.

```python
def missing_brute(nums):
    for v in range(len(nums) + 1):
        if v not in nums:
            return v
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Presence array

**Intuition.** A boolean array of size `n + 1`. Mark each value, then the first unmarked index is the answer.

```python
def missing_hash(nums):
    seen = [False] * (len(nums) + 1)
    for x in nums:
        seen[x] = True
    return seen.index(False)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. Sum formula

**Intuition.** The sum of `0..n` minus the sum of the array is exactly the missing value. In C++/Java, use `long` for large `n`.

```python
def missing_sum(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 6. XOR

**Intuition.** `x ^ x = 0` and `x ^ 0 = x`. XOR together every index `0..n` and every element: each present value appears twice and cancels, leaving the missing one. No overflow risk.

**Dry run** — `[0 2 3 1 4]`: (0^1^2^3^4^5) ^ (0^2^3^1^4) = 5.

**Cyclic sort** is a third O(1)-space method that also finds *several* missing numbers: place each `v` at index `v`, then scan for `nums[i] != i`. See [Repeating and Missing](#).

**C++**
```cpp
int missingNumber(vector<int>& nums) {
    int n = nums.size(), x = n;
    for (int i = 0; i < n; i++) x ^= i ^ nums[i];
    return x;
}
```

**Java**
```java
static int missingNumber(int[] nums) {
    int n = nums.length, x = n;
    for (int i = 0; i < n; i++) x ^= i ^ nums[i];
    return x;
}
```

**Python**
```python
def missing_number(nums):
    x = len(nums)
    for i, v in enumerate(nums):
        x ^= i ^ v
    return x
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Missing 0.
- Missing n (all of 0..n−1 present).
- n = 1.

---

## Common mistakes

1. Using `n = len + 1` when the range is `0..n` (it's `1..n` in some variants; read the statement).
2. `int` overflow in the sum formula for big n in C++/Java.
3. Sorting first: correct but O(n log n).

---

## Follow-ups

1. Range is 1..n, one missing.
2. Two numbers missing.
3. One missing and one repeating.

<details><summary>Answer sketches</summary>

**#1:** Expected sum n(n + 1)/2 with n = len + 1, or XOR 1..n.

**#2:** XOR gives a ^ b; split by its lowest set bit into two groups and XOR each group ([Part 20](../20-bit-manipulation/README.md)).

**#3:** Sum and sum-of-squares equations, or XOR split ([Hard section](#)).
</details>

---

## Flashcards

**Missing number via XOR?** #flashcard
XOR all indices 0..n with all elements; duplicates cancel.

**Why XOR over the sum formula?** #flashcard
No overflow; same O(n)/O(1).

**x ^ x and x ^ 0?** #flashcard
0 and x.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
