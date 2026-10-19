---
module: striver/09-basic-arrays
lesson: 2
topic: Count of Odd Numbers in Array
difficulty: Easy
source: https://takeuforward.org/learning/dsa/count-of-odd-numbers-in-array?category=basic-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, basic-arrays, arrays, parity]
---
# 2. Count of Odd Numbers in Array

← [Sum of Array Elements](01-sum-of-array-elements.md) · [Part 9 index](README.md) · Next → [Check if the Array is Sorted](03-check-if-the-array-is-sorted.md)

> [!abstract] Problem at a glance
> **Task:** Count the elements of `nums` that are odd.
> **Key insight:** `x & 1` is 1 for odd `x`, including negatives in two's complement, so `cnt += x & 1` needs no branch.
> **Difficulty:** Easy · **Pattern:** Single-pass accumulator
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-of-odd-numbers-in-array?category=basic-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — filter](#3-brute--filter) · [4. Optimal — bit test](#4-optimal--bit-test) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return how many elements are odd.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3, 4, 5]` | `3` | 1, 3, 5 |
| `nums = [2, 4, 6]` | `0` |  |
| `nums = [-3, -2]` | `1` | -3 is odd |

**Constraints:** `1 ≤ n ≤ 10⁵`, `-10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — filter | build the odd list, take its length | O(n) | O(n) |
| Optimal — bit test | `cnt += x & 1` | O(n) | O(1) |

---

## 3. Brute — filter

**Intuition.** Filter the odd elements into a new list and return its length. This allocates memory it doesn't need.

```python
def count_odd_filter(nums):
    return len([x for x in nums if x % 2 != 0])
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Optimal — bit test

**Intuition.** The lowest bit decides parity. In two's complement an odd negative still has its low bit set, so `& 1` is correct for every int. `% 2 == 1` is not, because in C++ and Java `-3 % 2 == -1`.

**Algorithm**

1. `cnt = 0`.
2. For each `x`: `cnt += x & 1`.
3. Return `cnt`.

**Dry run** — `[1, 2, 3, 4, 5]` → low bits 1 0 1 0 1 → **3**.

**C++**
```cpp
int countOdd(vector<int>& nums) {
    int cnt = 0;
    for (int x : nums) cnt += x & 1;
    return cnt;
}
```

**Java**
```java
static int countOdd(int[] nums) {
    int cnt = 0;
    for (int x : nums) cnt += x & 1;
    return cnt;
}
```

**Python**
```python
def count_odd(nums):
    cnt = 0
    for x in nums:
        cnt += x & 1
    return cnt
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Negative odds such as `-3`.
- `0` is even.
- Empty array → 0.

---

## Common mistakes

1. `x % 2 == 1` in C++/Java, which misses negative odds.
2. Counting evens by accident (`!(x & 1)`).

---

## Follow-ups

1. Count the subarrays with exactly k odd numbers (LC 1248).
2. Move all odds before evens in place.

<details><summary>Answer sketches</summary>

**#1:** Map each element to `x & 1` and count subarrays with sum k using prefix sums plus a hashmap, or `atMost(k) − atMost(k−1)` with a sliding window.

**#2:** Two pointers (a Dutch-flag style partition): `l` finds an even from the left, `r` finds an odd from the right, swap.
</details>

---

## Flashcards

**Parity test that's safe for negatives?** #flashcard
`x & 1` (or `x % 2 != 0`).

**Why does `-3 % 2 == 1` fail in Java?** #flashcard
Java's `%` keeps the dividend's sign, so `-3 % 2 == -1`.

**Interview track →** [Arrays deep-dive](../../01-data-structures/01-array.md) · [Two pointers](../../02-algorithms/03-two-pointers.md) · [Concept: basic arrays](../07-concept-basics/02-basic-arrays.md)
