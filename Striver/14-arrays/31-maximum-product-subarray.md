---
module: striver/14-arrays
lesson: 31
topic: Maximum Product Subarray
difficulty: Medium
source: https://takeuforward.org/learning/dsa/maximum-product-subarray-in-an-array?category=faqs-hard&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, dp, kadane]
---
# 31. Maximum Product Subarray

← [Reverse Pairs](30-reverse-pairs.md) · [Part 14 index](README.md) · Next → [Merge Two Sorted Arrays Without Extra Space](32-merge-sorted-arrays.md)

> [!abstract] Problem at a glance
> **Task:** Return the largest product of a non-empty contiguous subarray.
> **Key insight:** A negative number turns the smallest product into the largest. So track both `maxEnd` and `minEnd` (the max/min product ending here) and update `max(x, x·maxEnd, x·minEnd)`. Equivalently: the answer is the best prefix or suffix product, restarting after zeros.
> **Difficulty:** Medium · **Pattern:** Kadane variant (max/min) · **Also on:** [LC 152](https://leetcode.com/problems/maximum-product-subarray/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-product-subarray-in-an-array?category=faqs-hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All subarrays](#3-all-subarrays) · [4. Prefix and suffix products (Striver's optimal)](#4-prefix-and-suffix-products-strivers-optimal) · [5. Max/min ending here](#5-maxmin-ending-here) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, find a contiguous non-empty subarray with the largest product, and return that product. The answer fits in a 32-bit integer.

| Input | Output | Why |
|---|---|---|
| `nums = [4, 5, 3, 7, 1, 2]` | `840` | whole array |
| `nums = [-5, 0, -2]` | `0` |  |
| `nums = [2, 3, -2, 4]` | `6` | [2, 3] |

**Constraints:** `1 ≤ n ≤ 2·10⁴`, `−10 ≤ nums[i] ≤ 10`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All subarrays | fix start, extend end, running product | O(n²) | O(1) |
| Prefix and suffix products (Striver's optimal) | best of all prefix/suffix products, reset on 0 | O(n) | O(1) |
| Max/min ending here | hi, lo = max/min(x, x·hi, x·lo) | O(n) | O(1) |

---

## 3. All subarrays

**Intuition.** For each `i`, multiply forward and track the max.

```python
def max_product_brute(nums):
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Prefix and suffix products (Striver's optimal)

**Intuition.** Without zeros, the optimal subarray drops either a prefix ending at some negative or a suffix starting at one. With an even count of negatives, the whole array is optimal. With an odd count, drop everything up to the first negative or from the last one onwards. Both are a prefix or suffix product. A zero splits the array, so restart the product at 1 after it.

```python
def max_product_prefix_suffix(nums):
    n, best, pre, suf = len(nums), float("-inf"), 1, 1
    for i in range(n):
        pre = pre * nums[i] if pre else nums[i]
        suf = suf * nums[n - 1 - i] if suf else nums[n - 1 - i]
        best = max(best, pre, suf)
    return best
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 5. Max/min ending here

**Intuition.** `hi` = max product of a subarray ending at `i`, `lo` = min. A new element `x` either starts fresh or extends one of them, and multiplying by a negative swaps their roles, so compute both from the old values at the same time.

**Dry run** — `[2 3 −2 4]`: (hi, lo) = (2, 2) → (6, 3) → (−2, −12) → (4, −48); best = 6.

**C++**
```cpp
int maxProduct(vector<int>& nums) {
    int hi = nums[0], lo = nums[0], best = nums[0];
    for (int i = 1; i < (int)nums.size(); i++) {
        int x = nums[i];
        if (x < 0) swap(hi, lo);
        hi = max(x, hi * x);
        lo = min(x, lo * x);
        best = max(best, hi);
    }
    return best;
}
```

**Java**
```java
static int maxProduct(int[] nums) {
    int hi = nums[0], lo = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        if (x < 0) { int t = hi; hi = lo; lo = t; }
        hi = Math.max(x, hi * x);
        lo = Math.min(x, lo * x);
        best = Math.max(best, hi);
    }
    return best;
}
```

**Python**
```python
def max_product(nums):
    hi = lo = best = nums[0]
    for x in nums[1:]:
        if x < 0:
            hi, lo = lo, hi
        hi = max(x, hi * x)
        lo = min(x, lo * x)
        best = max(best, hi)
    return best
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Zeros split the array.
- Single negative → itself.
- Odd number of negatives.
- All negatives.

---

## Common mistakes

1. Tracking only the max (misses negative × negative).
2. Updating `hi` and then using the new `hi` to compute `lo` (without the swap trick, save the old value).
3. Seeding `best` with 0 or 1.

---

## Follow-ups

1. Return the subarray.
2. Overflow on longer inputs or larger values.
3. Maximum product of three numbers (LC 628).

<details><summary>Answer sketches</summary>

**#1:** Track start indices with the prefix/suffix version: restart on zero.

**#2:** Use 64-bit or doubles; with log sums, compare log|product| with sign tracking.

**#3:** Sort, or track the top 3 and bottom 2: max(a·b·c, min1·min2·max1).
</details>

---

## Flashcards

**Max product subarray state?** #flashcard
Both the max and min product ending here.

**Why track the min product?** #flashcard
A negative x turns the min into the max.

**Prefix/suffix trick for max product?** #flashcard
Best of all prefix and suffix products, resetting after a zero.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
