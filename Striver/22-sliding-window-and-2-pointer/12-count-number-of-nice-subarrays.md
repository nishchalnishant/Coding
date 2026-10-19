---
module: striver/22-sliding-window-and-2-pointer
lesson: 12
topic: Count Number of Nice Subarrays
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-number-of-nice-subarrays?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, counting, at-most-k]
---
# 12. Count Number of Nice Subarrays

← [Binary Subarrays With Sum](11-binary-subarrays-with-sum.md) · [Part 22 index](README.md) · Next → [Subarrays with K Different Integers](13-subarrays-with-k-different-integers.md)

> [!abstract] Problem at a glance
> **Task:** Count subarrays that contain exactly `k` odd numbers.
> **Key insight:** Map each number to `x % 2` and it's Binary Subarrays With Sum with `goal = k`. Use atMost(k) − atMost(k − 1) on the odd count.
> **Difficulty:** Medium · **Pattern:** Reduce to binary sum, then atMost subtraction · **Also on:** [LC 1248](https://leetcode.com/problems/count-number-of-nice-subarrays/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-number-of-nice-subarrays?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Prefix counts of odds](#3-prefix-counts-of-odds) · [4. atMost(k) − atMost(k − 1)](#4-atmostk--atmostk--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` and an integer `k`, a subarray is nice if it contains exactly `k` odd numbers. Return the number of nice subarrays.

| Input | Output | Why |
|---|---|---|
| `nums = [1,1,2,1,1], k = 3` | `2` | [1,1,2,1] and [1,2,1,1] |
| `nums = [2,4,6], k = 1` | `0` |  |
| `nums = [2,2,2,1,2,2,1,2,2,2], k = 2` | `16` |  |

**Constraints:** `1 ≤ nums.length ≤ 5·10⁴`, `1 ≤ nums[i] ≤ 10⁵`, `1 ≤ k ≤ nums.length`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Prefix counts of odds | hashmap of prefix odd counts | O(n) | O(n) |
| atMost(k) − atMost(k − 1) | window on the odd count | O(n) | O(1) |

> [!tip] Interview angle
> Tests whether you spot the reduction. Say "odd → 1, even → 0, now it's binary subarrays with sum k" and reuse the code.

---

## 3. Prefix counts of odds

**Intuition.** Running odd count `c`; for each index add how many earlier prefixes had `c − k` odds.

```python
def nice_prefix(nums, k):
    seen = {0: 1}
    c = total = 0
    for x in nums:
        c += x & 1
        total += seen.get(c - k, 0)
        seen[c] = seen.get(c, 0) + 1
    return total
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. atMost(k) − atMost(k − 1)

**Intuition.** Same at-most window as Binary Subarrays With Sum, adding `x & 1` instead of `x`.

**Algorithm**

1. `atMost(k)`: window counting odds; shrink while odds > k; add `r − l + 1`.
2. Return `atMost(k) − atMost(k − 1)`.

**Dry run** — [1,1,2,1,1], k=3: atMost(3) = 1+2+3+4+4 = 14, atMost(2) = 1+2+3+3+3 = 12 → 2.

**C++**
```cpp
int atMostOdd(vector<int>& nums, int k) {
    if (k < 0) return 0;
    int l = 0, odd = 0, cnt = 0;
    for (int r = 0; r < (int)nums.size(); r++) {
        odd += nums[r] & 1;
        while (odd > k) odd -= nums[l++] & 1;
        cnt += r - l + 1;
    }
    return cnt;
}
int numberOfSubarrays(vector<int>& nums, int k) {
    return atMostOdd(nums, k) - atMostOdd(nums, k - 1);
}
```

**Java**
```java
static int atMostOdd(int[] nums, int k) {
    if (k < 0) return 0;
    int l = 0, odd = 0, cnt = 0;
    for (int r = 0; r < nums.length; r++) {
        odd += nums[r] & 1;
        while (odd > k) odd -= nums[l++] & 1;
        cnt += r - l + 1;
    }
    return cnt;
}
static int numberOfSubarrays(int[] nums, int k) {
    return atMostOdd(nums, k) - atMostOdd(nums, k - 1);
}
```

**Python**
```python
def number_of_subarrays(nums, k):
    def at_most(k):
        if k < 0:
            return 0
        l = odd = cnt = 0
        for r, x in enumerate(nums):
            odd += x & 1
            while odd > k:
                odd -= nums[l] & 1
                l += 1
            cnt += r - l + 1
        return cnt
    return at_most(k) - at_most(k - 1)
```

**Complexity:** time **O(n)**, space **O(1)** — two linear passes.

---

## Edge cases

- No odd numbers → 0.
- `k` larger than the number of odds → 0.

---

## Common mistakes

1. Missing the reduction and writing a custom window that undercounts even runs.
2. `x % 2` on negatives in C++/Java gives −1 (not an issue here, values ≥ 1, but `x & 1` is safer).

---

## Follow-ups

1. Exactly k elements divisible by 3.
2. Count via odd positions directly.

<details><summary>Answer sketches</summary>

**#1:** Map to `x % 3 == 0`; same code.

**#2:** For each block of k consecutive odds, multiply (evens before + 1) × (evens after + 1).
</details>

---

## Flashcards

**Nice Subarrays reduction?** #flashcard
odd → 1, even → 0; count subarrays with sum exactly k.

**Second method?** #flashcard
Product of gaps: (evens before the first odd + 1) × (evens after the k-th odd + 1) per block of k odds.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../coding/algorithms/04-sliding-window.md)
