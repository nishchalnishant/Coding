---
module: striver/14-arrays
lesson: 26
topic: Next Permutation
difficulty: Medium
source: https://takeuforward.org/learning/dsa/next-permutation?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, array, permutation, in-place]
---
# 26. Next Permutation

← [Kadane's Algorithm: Maximum Subarray Sum](25-kadanes-algorithm.md) · [Part 14 index](README.md) · Next → [Majority Element II](27-majority-element-ii.md)

> [!abstract] Problem at a glance
> **Task:** Rearrange `nums` in place into the next lexicographically greater permutation (or the smallest one if it's the last).
> **Key insight:** From the right, find the first `i` with `nums[i] < nums[i + 1]` (the pivot). Swap it with the smallest value to its right that's greater than it (scan from the right). Then reverse the suffix after `i`, which was descending. No pivot means it's the last permutation, so reverse the whole array.
> **Difficulty:** Medium · **Pattern:** Permutation: pivot + suffix reverse · **Also on:** [LC 31](https://leetcode.com/problems/next-permutation/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/next-permutation?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Generate all, find the next](#3-generate-all-find-the-next) · [4. Pivot, swap, reverse](#4-pivot-swap-reverse) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums`, rearrange it into the lexicographically next greater permutation. If none exists, rearrange it into ascending order. Use O(1) extra memory.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 2, 3]` | `[1, 3, 2]` |  |
| `nums = [3, 2, 1]` | `[1, 2, 3]` | last → first |
| `nums = [2, 1, 5, 4, 3, 0, 0]` | `[2, 3, 0, 0, 1, 4, 5]` |  |

**Constraints:** `1 ≤ n ≤ 100`, `0 ≤ nums[i] ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Generate all, find the next | list every permutation in order | O(n! · n) | O(n!) |
| Pivot, swap, reverse | find the dip from the right; swap with the next larger; reverse the suffix | O(n) | O(1) |

---

## 3. Generate all, find the next

**Intuition.** Generate all permutations (deduplicated and sorted), find the current one, return the next. Only usable for tiny n, but it defines the problem precisely.

```python
def next_perm_brute(nums):
    from itertools import permutations
    ps = sorted(set(permutations(nums)))
    k = ps.index(tuple(nums))
    nums[:] = list(ps[(k + 1) % len(ps)])
```

**Complexity:** time **O(n! · n)**, space **O(n!)**.

---

## 4. Pivot, swap, reverse

**Intuition.** The longest non-increasing suffix is already at its largest arrangement, so the change must happen just before it, at the pivot `i`. To grow by as little as possible, put the smallest value larger than `nums[i]` from the suffix at `i`. The suffix stays non-increasing after the swap, so reversing it gives its smallest arrangement.

**Algorithm**

1. `i = n − 2`; while `i >= 0 and nums[i] >= nums[i + 1]`: `i−−`.
2. If `i >= 0`: `j = n − 1`; while `nums[j] <= nums[i]`: `j−−`; swap `nums[i]`, `nums[j]`.
3. Reverse `nums[i + 1 .. n − 1]` (the whole array if `i = −1`).

**Dry run** — `[2 1 5 4 3 0 0]`: suffix `5 4 3 0 0` is non-increasing, pivot i = 1 (value 1). The rightmost value > 1 is 3 (j = 4). Swap → `[2 3 5 4 1 0 0]`. Reverse the suffix → `[2 3 0 0 1 4 5]`.

**Previous permutation:** mirror everything: find `nums[i] > nums[i + 1]`, swap with the largest smaller value on the right, reverse. C++ has `std::next_permutation` built in. Mention it, but write the algorithm.

**C++**
```cpp
void nextPermutation(vector<int>& nums) {
    int n = nums.size(), i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) i--;
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] <= nums[i]) j--;
        swap(nums[i], nums[j]);
    }
    reverse(nums.begin() + i + 1, nums.end());
}
```

**Java**
```java
static void nextPermutation(int[] nums) {
    int n = nums.length, i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) i--;
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] <= nums[i]) j--;
        int t = nums[i]; nums[i] = nums[j]; nums[j] = t;
    }
    for (int l = i + 1, r = n - 1; l < r; l++, r--) {
        int t = nums[l]; nums[l] = nums[r]; nums[r] = t;
    }
}
```

**Python**
```python
def next_permutation(nums):
    n, i = len(nums), len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1:] = reversed(nums[i + 1:])
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## Edge cases

- Last permutation → wraps to the first.
- Duplicates (strict `>=` / `<=` comparisons matter).
- n = 1.

---

## Common mistakes

1. `>` instead of `>=` when finding the pivot → wrong with duplicates.
2. Sorting the suffix (O(n log n)) when a reverse suffices.
3. Swapping with the first larger element from the *left* of the suffix instead of the smallest larger (scan from the right).

---

## Follow-ups

1. k-th permutation of 1..n (LC 60).
2. All permutations.
3. Next greater number with the same digits (LC 556).

<details><summary>Answer sketches</summary>

**#1:** Factorial number system: pick digit ⌊k / (n − 1)!⌋, recurse. O(n²).

**#2:** Backtracking ([Part 18](../18-recursion/README.md)), or call next permutation n! times starting sorted.

**#3:** Next permutation on the digits; check the 32-bit overflow.
</details>

---

## Flashcards

**Next permutation step 1?** #flashcard
From the right, first i with nums[i] < nums[i + 1].

**Next permutation step 2?** #flashcard
Swap nums[i] with the rightmost nums[j] > nums[i].

**Next permutation step 3?** #flashcard
Reverse nums[i + 1 ..]; if there was no pivot, reverse everything.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../coding/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../coding/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
