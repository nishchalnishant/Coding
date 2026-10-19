---
module: striver/22-sliding-window-and-2-pointer
lesson: 13
topic: Subarrays with K Different Integers
difficulty: Hard
source: https://takeuforward.org/learning/dsa/subarrays-with-k-different-integers?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, hashing, counting, at-most-k, hard]
---
# 13. Subarrays with K Different Integers

← [Count Number of Nice Subarrays](12-count-number-of-nice-subarrays.md) · [Part 22 index](README.md) · Next → [Part 23: Stack / Queues](../23-stack-and-queues/README.md)

> [!abstract] Problem at a glance
> **Task:** Count subarrays with exactly `k` distinct integers.
> **Key insight:** Exactly-k distinct isn't monotone, but at-most-k is: if `[l, r]` has ≤ k distinct, so does every `[l', r]` with `l' ≥ l`. So answer = atMost(k) − atMost(k − 1), each an O(n) window with a count map.
> **Difficulty:** Hard · **Pattern:** Exactly(K) = atMost(K) − atMost(K − 1) with a count map · **Also on:** [LC 992](https://leetcode.com/problems/subarrays-with-k-different-integers/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/subarrays-with-k-different-integers?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. atMost(k) − atMost(k − 1)](#4-atmostk--atmostk--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` and an integer `k`, return the number of good subarrays: contiguous subarrays with exactly `k` different integers.

| Input | Output | Why |
|---|---|---|
| `nums = [1,2,1,2,3], k = 2` | `7` | [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2] |
| `nums = [1,2,1,3,4], k = 3` | `3` | [1,2,1,3], [2,1,3], [1,3,4] |

**Constraints:** `1 ≤ nums.length ≤ 2·10⁴`, `1 ≤ nums[i], k ≤ nums.length`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | set per start, count when size == k | O(n²) | O(n) |
| atMost(k) − atMost(k − 1) | two at-most-distinct windows | O(n) | O(n) |

> [!tip] Interview angle
> The hard capstone of the atMost trick. Explain why a direct exactly-k window fails (for a fixed `r`, the valid starts form a range in the middle, not a prefix) and why subtraction fixes it.

---

## 3. Brute force: every start

**Intuition.** For each start, extend with a set; count each `j` where the size is exactly `k`; break when it exceeds `k`.

```python
def k_diff_brute(nums, k):
    total = 0
    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            if len(seen) == k:
                total += 1
            elif len(seen) > k:
                break
    return total
```

**Complexity:** time **O(n²)**, space **O(n)**.

---

## 4. atMost(k) − atMost(k − 1)

**Intuition.** `atMost(k)`: window with a count array and a `distinct` counter; shrink while `distinct > k`; add `r − l + 1`. The difference counts subarrays with exactly `k` distinct.

**Algorithm**

1. `atMost(k)`: `cnt` array, `l = distinct = total = 0`.
2. For each `r`: if `cnt[nums[r]] == 0`, `distinct += 1`; `cnt[nums[r]] += 1`.
3. While `distinct > k`: decrement `cnt[nums[l]]`, if 0 `distinct -= 1`; `l += 1`.
4. `total += r − l + 1`.
5. Return `atMost(k) − atMost(k − 1)`.

**Dry run** — [1,2,1,2,3], k=2: atMost(2) = 1+2+3+4+2 = 12; atMost(1) = 1+1+1+1+1 = 5 → 7.

**C++**
```cpp
int atMostDistinct(vector<int>& nums, int k) {
    vector<int> cnt(nums.size() + 1, 0);
    int l = 0, distinct = 0, total = 0;
    for (int r = 0; r < (int)nums.size(); r++) {
        if (cnt[nums[r]]++ == 0) distinct++;
        while (distinct > k)
            if (--cnt[nums[l++]] == 0) distinct--;
        total += r - l + 1;
    }
    return total;
}
int subarraysWithKDistinct(vector<int>& nums, int k) {
    return atMostDistinct(nums, k) - atMostDistinct(nums, k - 1);
}
```

**Java**
```java
static int atMostDistinct(int[] nums, int k) {
    int[] cnt = new int[nums.length + 1];
    int l = 0, distinct = 0, total = 0;
    for (int r = 0; r < nums.length; r++) {
        if (cnt[nums[r]]++ == 0) distinct++;
        while (distinct > k)
            if (--cnt[nums[l++]] == 0) distinct--;
        total += r - l + 1;
    }
    return total;
}
static int subarraysWithKDistinct(int[] nums, int k) {
    return atMostDistinct(nums, k) - atMostDistinct(nums, k - 1);
}
```

**Python**
```python
def subarrays_with_k_distinct(nums, k):
    def at_most(k):
        cnt = [0] * (len(nums) + 1)
        l = distinct = total = 0
        for r, x in enumerate(nums):
            if cnt[x] == 0:
                distinct += 1
            cnt[x] += 1
            while distinct > k:
                cnt[nums[l]] -= 1
                if cnt[nums[l]] == 0:
                    distinct -= 1
                l += 1
            total += r - l + 1
        return total
    return at_most(k) - at_most(k - 1)
```

**Complexity:** time **O(n)**, space **O(n)** — each window pass is linear; values ≤ n so an array replaces the hashmap.

---

## Edge cases

- `k` greater than the number of distinct values → 0.
- All equal, `k = 1` → n(n+1)/2.

---

## Common mistakes

1. One window that counts when `distinct == k` — misses all starts between the leftmost and rightmost valid ones.
2. Sizing the count array by `max(nums)` but indexing past it.
3. Forgetting `atMost(0) = 0` (the loop handles it: the window is always empty).

---

## Follow-ups

1. One-pass version.
2. Longest subarray with exactly k distinct.

<details><summary>Answer sketches</summary>

**#1:** Keep two left pointers `l1` (≤ k distinct) and `l2` (≤ k − 1 distinct); add `l2 − l1` per `r`.

**#2:** Plain window: record length only when `distinct == k`.
</details>

---

## Flashcards

**Subarrays with exactly K distinct?** #flashcard
atMost(K) − atMost(K − 1), each a shrink-while-distinct>K window adding r − l + 1.

**Why does a direct exactly-K window fail?** #flashcard
For fixed r, valid starts are a middle range, not a prefix of [l, r]; one pointer can't track both ends.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../coding/algorithms/04-sliding-window.md)
