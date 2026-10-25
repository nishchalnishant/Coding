---
module: striver-a2z/15-hashing
lesson: 4
topic: Largest Subarray with Sum 0
difficulty: Medium
source: https://takeuforward.org/learning/dsa/largest-subarray-with-sum-0?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, hashing, hashing, prefix-sum]
---
# 4. Largest Subarray with Sum 0

← [Longest Subarray with Sum K](03-longest-subarray-with-sum-k.md) · [Part 15 index](README.md) · Next → [Count Subarrays with Given Sum](05-count-subarrays-with-given-sum.md)

> [!abstract] Problem at a glance
> **Task:** Return the length of the longest contiguous subarray whose sum is 0.
> **Key insight:** Sum of `(j, i]` is 0 iff `P[i] == P[j]`. So the answer is the largest distance between two equal prefix sums — store the first index of each prefix, seeded `{0: −1}`.
> **Difficulty:** Medium · **Pattern:** Prefix sum + first-index map (k = 0) · **Also on:** [GfG: Largest subarray with 0 sum](https://www.geeksforgeeks.org/problems/largest-subarray-with-0-sum/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/largest-subarray-with-sum-0?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All subarrays with a running sum](#3-all-subarrays-with-a-running-sum) · [4. Equal prefix sums](#4-equal-prefix-sums) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums`, return the length of the longest subarray with sum `0`, or 0 if none exists.

| Input | Output | Why |
|---|---|---|
| `nums = [15, -2, 2, -8, 1, 7, 10, 23]` | `5` | [−2, 2, −8, 1, 7] |
| `nums = [2, 10, 4]` | `0` |  |
| `nums = [1, 0, -5]` | `1` | [0] |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁹ ≤ nums[i] ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All subarrays with a running sum | fix l, extend r | O(n²) | O(1) |
| Equal prefix sums | first[p]; on repeat, len = i − first[p] | O(n) average | O(n) |

---

## 3. All subarrays with a running sum

**Intuition.** Same as the sum-k brute force with `k = 0`.

```python
def max_len_zero_brute(nums):
    best = 0
    for l in range(len(nums)):
        s = 0
        for r in range(l, len(nums)):
            s += nums[r]
            if s == 0:
                best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Equal prefix sums

**Intuition.** This is [Longest Subarray with Sum K](03-longest-subarray-with-sum-k.md) with `k = 0`, which simplifies the lookup to `p` itself: a repeated prefix value means everything between the two occurrences cancelled out.

**Dry run** — `[15 −2 2 −8 1 7 10 23]`: p = 15, 13, 15, 7, 8, 15, 25, 48. 15 first at 0; reappears at i=2 (len 2) and i=5 (len 5). Answer 5.

**C++**
```cpp
int maxLen(vector<int>& nums) {
    unordered_map<long long, int> first;
    first[0] = -1;
    long long p = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        p += nums[i];
        auto it = first.find(p);
        if (it != first.end()) best = max(best, i - it->second);
        else first[p] = i;
    }
    return best;
}
```

**Java**
```java
static int maxLen(int[] nums) {
    HashMap<Long, Integer> first = new HashMap<>();
    first.put(0L, -1);
    long p = 0;
    int best = 0;
    for (int i = 0; i < nums.length; i++) {
        p += nums[i];
        Integer j = first.get(p);
        if (j != null) best = Math.max(best, i - j);
        else first.put(p, i);
    }
    return best;
}
```

**Python**
```python
def max_len_zero(nums):
    first = {0: -1}
    p = best = 0
    for i, x in enumerate(nums):
        p += x
        if p in first:
            best = max(best, i - first[p])
        else:
            first[p] = i
    return best
```

**Complexity:** time **O(n) average**, space **O(n)**.

---

## Edge cases

- Whole array sums to 0 (needs the seed).
- Single zero → 1.
- All zeros → n.
- Large values: 64-bit prefix.

---

## Common mistakes

1. Missing `{0: −1}` → misses prefixes that are 0 themselves.
2. Updating the stored index on repeats.

---

## Follow-ups

1. Count subarrays with sum 0.
2. Contiguous array, equal 0s and 1s (LC 525).
3. Does any zero-sum subarray exist?

<details><summary>Answer sketches</summary>

**#1:** Count map seeded {0: 1}: [Count Subarrays with Given Sum](05-count-subarrays-with-given-sum.md) with k = 0.

**#2:** Replace 0 with −1; this problem.

**#3:** Set of prefixes; true on the first repeat.
</details>

---

## Flashcards

**Zero-sum subarray ⇔ ?** #flashcard
Two equal prefix sums.

**Seed for longest zero-sum subarray?** #flashcard
{0: −1}.

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Hashing walkthroughs](../../04-practice/data-structures/02-hashing.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
