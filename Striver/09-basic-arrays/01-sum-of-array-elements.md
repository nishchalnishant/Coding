---
module: striver/09-basic-arrays
lesson: 1
topic: Sum of Array Elements
difficulty: Easy
source: https://takeuforward.org/learning/dsa/sum-of-array-elements?category=basic-arrays&source=strivers-a2z-dsa-sheet
tags: [striver, basic-arrays, arrays]
---
# 1. Sum of Array Elements

← [Part 9 index](README.md) · Next → [Count of Odd Numbers in Array](02-count-of-odd-numbers-in-array.md)

> [!abstract] Problem at a glance
> **Task:** Return the sum of all elements of `nums`.
> **Key insight:** One pass with an accumulator that starts at 0. Use 64-bit if `n · max|x|` can exceed 2³¹.
> **Difficulty:** Easy · **Pattern:** Single-pass accumulator
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/sum-of-array-elements?category=basic-arrays&source=strivers-a2z-dsa-sheet) · **Time:** 5 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute — recursion](#3-brute--recursion) · [4. Optimal — accumulator](#4-optimal--accumulator) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the sum of its elements.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3]` | `6` |  |
| `nums = [-1, 2, -3, 1]` | `-1` | negatives are fine |
| `nums = [5]` | `5` |  |

**Constraints:** `1 ≤ n ≤ 10⁵`, `-10⁴ ≤ nums[i] ≤ 10⁴`. The worst-case sum is ±10⁹, which fits in 32 bits. With values up to 10⁹ it would not.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute — recursion | `nums[0] + sum(nums[1:])` | O(n²) with slicing | O(n) stack |
| Optimal — accumulator | `s += x` | O(n) | O(1) |

---

## 3. Brute — recursion

**Intuition.** The recursive definition is fine as a thought, but in Python each slice copies the rest of the list (O(n²) total) and n = 10⁵ blows the default recursion limit. It's shown only as a contrast.

```python
def sum_rec(nums):
    return 0 if not nums else nums[0] + sum_rec(nums[1:])
```

**Complexity:** time **O(n²) with slicing**, space **O(n) stack**.

---

## 4. Optimal — accumulator

**Intuition.** Start at the additive identity 0 and add each element once.

**Algorithm**

1. `s = 0`.
2. For each `x` in `nums`: `s += x`.
3. Return `s`.

**Dry run** — `[1, 2, 3]`: 0 → 1 → 3 → 6.

**Library:** Python `sum(nums)`; C++ `accumulate(nums.begin(), nums.end(), 0LL)`. The `0LL` sets the accumulator type: passing `0` sums in `int` even if you store the result in a `long long`. Java: `Arrays.stream(nums).asLongStream().sum()`.

**C++**
```cpp
long long sumOfArray(vector<int>& nums) {
    long long s = 0;
    for (int x : nums) s += x;
    return s;
}
```

**Java**
```java
static long sumOfArray(int[] nums) {
    long s = 0;
    for (int x : nums) s += x;
    return s;
}
```

**Python**
```python
def sum_of_array(nums):
    s = 0
    for x in nums:
        s += x
    return s
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Empty array → 0.
- Large values: `3 × 10⁹` overflows `int`, so the test above needs 64-bit.
- All negatives → a negative sum, so don't initialise from a max/min.

---

## Common mistakes

1. `accumulate(..., 0)` in C++. The `int` init makes the whole sum `int`.
2. Starting `s = nums[0]` and looping from index 0, which counts the first element twice.

---

## Follow-ups

1. Prefix sums for range-sum queries (LC 303).
2. Sum modulo 10⁹+7.

<details><summary>Answer sketches</summary>

**#1:** `pre[i+1] = pre[i] + nums[i]`; `sum(l..r) = pre[r+1] − pre[l]`. O(n) build, O(1) per query.

**#2:** `s = (s + x) % MOD`. With negatives, add MOD before the final `%`.
</details>

---

## Flashcards

**C++ accumulate overflow trap?** #flashcard
The init value fixes the type: use `0LL`, not `0`.

**Range sum in O(1)?** #flashcard
Prefix sums: pre[r+1] − pre[l].

**Interview track →** [Arrays deep-dive](../../01-data-structures/01-array.md) · [Two pointers](../../02-algorithms/03-two-pointers.md) · [Concept: basic arrays](../07-concept-basics/02-basic-arrays.md)
