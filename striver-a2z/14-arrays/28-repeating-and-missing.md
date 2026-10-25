---
module: striver-a2z/14-arrays
lesson: 28
topic: Find the Repeating and Missing Number
difficulty: Hard
source: https://takeuforward.org/learning/dsa/find-the-repeating-and-missing-number?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, math, xor, bit-manipulation]
---
# 28. Find the Repeating and Missing Number

← [Majority Element II](27-majority-element-ii.md) · [Part 14 index](README.md) · Next → [Count Inversions](29-count-inversions.md)

> [!abstract] Problem at a glance
> **Task:** `nums` holds 1..n with one value repeated and one missing; return `[repeating, missing]`.
> **Key insight:** Two equations in `x` (repeating) and `y` (missing): `S − Sₙ = x − y` and `S₂ − S₂ₙ = x² − y²`. Dividing gives `x + y`, and two linear equations solve it in O(n)/O(1). The XOR split is the overflow-free alternative.
> **Difficulty:** Hard · **Pattern:** Math equations / XOR split · **Also on:** GfG Find Missing and Repeating
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/find-the-repeating-and-missing-number?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Frequency array](#3-frequency-array) · [4. XOR split](#4-xor-split) · [5. Sum and sum-of-squares equations](#5-sum-and-sum-of-squares-equations) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of size `n` containing each number in `[1, n]` exactly once, except one number `A` that appears twice and one number `B` that's missing, return `[A, B]`.

| Input | Output | Why |
|---|---|---|
| `nums = [3, 5, 4, 1, 1]` | `[1, 2]` |  |
| `nums = [1, 2, 3, 6, 7, 5, 7]` | `[7, 4]` |  |

**Constraints:** `2 ≤ n ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Frequency array | count each value; count 2 → repeating, 0 → missing | O(n) | O(n) |
| XOR split | XOR gives x ^ y; split by a set bit; identify which is which | O(n) | O(1) |
| Sum and sum-of-squares equations | x − y and x² − y² → x + y | O(n) | O(1) |

> [!tip] Interview angle
> Offer the hash version first, then the math version, then mention XOR. Call out the overflow in the sum of squares (n² · n ≈ 10¹⁵, so use 64-bit).

---

## 3. Frequency array

**Intuition.** A count array of size `n + 1`. The value with count 2 is repeating, the one with count 0 is missing.

```python
def rep_miss_hash(nums):
    n = len(nums)
    cnt = [0] * (n + 1)
    for x in nums:
        cnt[x] += 1
    rep = miss = -1
    for v in range(1, n + 1):
        if cnt[v] == 2:
            rep = v
        elif cnt[v] == 0:
            miss = v
    return [rep, miss]
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. XOR split

**Intuition.** XOR of all elements and 1..n gives `x ^ y` (everything else cancels). Its lowest set bit separates `x` and `y` into different groups; XOR each group (array and range) to get the two values. A final scan decides which one appears in the array, i.e. is the repeating one.

```python
def rep_miss_xor(nums):
    n, xr = len(nums), 0
    for i, v in enumerate(nums):
        xr ^= v ^ (i + 1)
    bit = xr & -xr
    a = b = 0
    for i, v in enumerate(nums):
        if v & bit: a ^= v
        else: b ^= v
        if (i + 1) & bit: a ^= i + 1
        else: b ^= i + 1
    return [a, b] if a in nums else [b, a]
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 5. Sum and sum-of-squares equations

**Intuition.** Let `x` = repeating, `y` = missing. With `S = Σ nums`, `Sₙ = n(n + 1)/2`: `S − Sₙ = x − y`. With `S₂ = Σ nums²`, `S₂ₙ = n(n + 1)(2n + 1)/6`: `S₂ − S₂ₙ = x² − y² = (x − y)(x + y)`. So `x + y = (S₂ − S₂ₙ) / (x − y)`, and `x = ((x − y) + (x + y)) / 2`. `x − y` is never 0, because they're different values.

**Dry run** — `[3 5 4 1 1]`, n = 5: S = 14, Sₙ = 15 → x − y = −1. S₂ = 52, S₂ₙ = 55 → x² − y² = −3 → x + y = 3. x = (−1 + 3)/2 = 1, y = 2.

**C++**
```cpp
vector<int> findMissingRepeatingNumbers(vector<int>& nums) {
    long long n = nums.size();
    long long sn = n * (n + 1) / 2, s2n = n * (n + 1) * (2 * n + 1) / 6;
    long long s = 0, s2 = 0;
    for (int v : nums) { s += v; s2 += (long long)v * v; }
    long long diff = s - sn;            // x - y
    long long sum = (s2 - s2n) / diff;  // x + y
    long long x = (diff + sum) / 2, y = x - diff;
    return {(int)x, (int)y};
}
```

**Java**
```java
static int[] findMissingRepeatingNumbers(int[] nums) {
    long n = nums.length;
    long sn = n * (n + 1) / 2, s2n = n * (n + 1) * (2 * n + 1) / 6;
    long s = 0, s2 = 0;
    for (int v : nums) { s += v; s2 += (long) v * v; }
    long diff = s - sn;            // x - y
    long sum = (s2 - s2n) / diff;  // x + y
    long x = (diff + sum) / 2, y = x - diff;
    return new int[]{(int) x, (int) y};
}
```

**Python**
```python
def find_missing_repeating(nums):
    n = len(nums)
    diff = sum(nums) - n * (n + 1) // 2                                  # x - y
    total = (sum(v * v for v in nums) - n * (n + 1) * (2 * n + 1) // 6) // diff  # x + y
    x = (diff + total) // 2
    return [x, x - diff]
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Missing is 1 or n.
- n = 2.
- Large n: Σv² up to ~3·10¹⁴.

---

## Common mistakes

1. `int` for sums of squares → overflow.
2. Mixing up the order: the problem asks for [repeating, missing].
3. XOR method: forgetting the final scan to tell which of the two values is the repeating one.

---

## Follow-ups

1. Cyclic sort / in-place marking (array may be modified).
2. Find all duplicates in 1..n (LC 442).
3. Duplicate number without modifying the array (LC 287).

<details><summary>Answer sketches</summary>

**#1:** Negate `nums[|v| − 1]`; seeing it already negative → repeating; the positive index left → missing.

**#2:** The same sign-marking trick.

**#3:** Floyd's cycle detection on i → nums[i] ([Part 19](../19-linked-list/README.md)).
</details>

---

## Flashcards

**Repeating/missing via math?** #flashcard
x − y from sums, x² − y² from squares; divide → x + y.

**Repeating/missing via XOR?** #flashcard
XOR all with 1..n → x ^ y; split by the lowest set bit.

**Sum of squares 1..n?** #flashcard
n(n + 1)(2n + 1)/6.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
