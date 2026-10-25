---
module: striver-a2z/14-arrays
lesson: 25
topic: Kadane's Algorithm: Maximum Subarray Sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/kadane's-algorithm?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, dp, kadane]
---
# 25. Kadane's Algorithm: Maximum Subarray Sum

← [Sort an Array of 0s, 1s and 2s](24-sort-colors.md) · [Part 14 index](README.md) · Next → [Next Permutation](26-next-permutation.md)

> [!abstract] Problem at a glance
> **Task:** Return the largest sum of a non-empty contiguous subarray.
> **Key insight:** At each index, either extend the best subarray ending at `i − 1` or start fresh: `cur = max(x, cur + x)`. Equivalently, drop a negative running sum. The answer is the max `cur` seen.
> **Difficulty:** Medium · **Pattern:** Kadane / DP on suffix · **Also on:** [LC 53](https://leetcode.com/problems/maximum-subarray/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/kadane's-algorithm?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All subarrays](#3-all-subarrays) · [4. Kadane](#4-kadane) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, find the contiguous non-empty subarray with the largest sum, and return that sum.

| Input | Output | Why |
|---|---|---|
| `nums = [2, 3, 5, -2, 7, -4]` | `15` | [2, 3, 5, −2, 7] |
| `nums = [-2, -3, -7, -2, -10, -4]` | `-2` | all negative: best single element |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁴ ≤ nums[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All subarrays | fix start, extend end, running sum | O(n²) | O(1) |
| Kadane | cur = max(x, cur + x); best = max(best, cur) | O(n) | O(1) |

> [!tip] Interview angle
> Expect follow-ups: return the subarray itself, the all-negative case, and the divide-and-conquer O(n log n) version.

---

## 3. All subarrays

**Intuition.** For each start `i`, extend `j` and keep the running sum (the O(n³) version recomputes it each time).

```python
def max_sub_brute(nums):
    best = nums[0]
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            best = max(best, s)
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Kadane

**Intuition.** Let `cur` be the best sum of a subarray **ending at** `i`. It's either `nums[i]` alone or `nums[i]` appended to the best one ending at `i − 1`. A negative `cur` can only hurt the next element, so it's dropped. This is the 1-D DP `dp[i] = max(nums[i], dp[i − 1] + nums[i])` with O(1) state.

**Dry run** — `[2 3 5 −2 7 −4]`: cur 2 5 10 8 15 11; best 15.

**Recover the subarray:** keep `start` reset to `i` whenever `cur` restarts, and record `(start, i)` whenever `best` improves. **Striver's form:** `sum += x; best = max(best, sum); if sum < 0: sum = 0`. It's the same thing, and seeding `best` with `nums[0]` (or −∞) keeps the all-negative case correct.

**C++**
```cpp
int maxSubArray(vector<int>& nums) {
    int cur = nums[0], best = nums[0];
    for (int i = 1; i < (int)nums.size(); i++) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    return best;
}
```

**Java**
```java
static int maxSubArray(int[] nums) {
    int cur = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(nums[i], cur + nums[i]);
        best = Math.max(best, cur);
    }
    return best;
}
```

**Python**
```python
def max_sub_array(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- All negative → the max element.
- Single element.
- Zeros.

---

## Common mistakes

1. Seeding `best = 0` → returns 0 for all-negative input.
2. Resetting `sum = 0` *before* updating `best` (Striver form) → loses all-negative answers.
3. Returning `cur` instead of `best`.

---

## Follow-ups

1. Return the subarray.
2. Maximum circular subarray (LC 918).
3. Maximum product subarray.
4. Max subarray sum with at most one deletion (LC 1186).

<details><summary>Answer sketches</summary>

**#1:** Track `start` on reset and `(ansStart, ansEnd)` on improvement.

**#2:** max(kadane, total − minKadane), unless all are negative.

**#3:** Track both max and min ending here: [Maximum Product Subarray](31-maximum-product-subarray.md).

**#4:** Two DP states: no deletion / one deletion used.
</details>

---

## Flashcards

**Kadane recurrence?** #flashcard
cur = max(x, cur + x); best = max(best, cur).

**Kadane: all negative?** #flashcard
Seed with nums[0], so the answer is the max element.

**Circular max subarray?** #flashcard
max(kadane, total − min subarray), unless all negative.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
