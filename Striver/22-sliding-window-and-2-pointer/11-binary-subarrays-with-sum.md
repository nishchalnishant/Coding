---
module: striver/22-sliding-window-and-2-pointer
lesson: 11
topic: Binary Subarrays With Sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/binary-subarrays-with-sum?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet
tags: [striver, sliding-window-and-2-pointer, sliding-window, prefix-sum, counting, at-most-k]
---
# 11. Binary Subarrays With Sum

← [Number of Substrings Containing All Three Characters](10-number-of-substrings-containing-all-three-characters.md) · [Part 22 index](README.md) · Next → [Count Number of Nice Subarrays](12-count-number-of-nice-subarrays.md)

> [!abstract] Problem at a glance
> **Task:** Count subarrays of a binary array whose sum equals `goal`.
> **Key insight:** "Exactly goal" isn't monotone for a window, but "at most goal" is. So answer = atMost(goal) − atMost(goal − 1), where atMost counts windows by adding `r − l + 1` per right end. The prefix-sum + hashmap method also works and handles negatives.
> **Difficulty:** Medium · **Pattern:** Exactly(K) = atMost(K) − atMost(K − 1) · **Also on:** [LC 930](https://leetcode.com/problems/binary-subarrays-with-sum/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/binary-subarrays-with-sum?category=counting-subarrays-and-substrings-problems&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Brute force: every start](#3-brute-force-every-start) · [4. Prefix sums + hashmap](#4-prefix-sums--hashmap) · [5. atMost(goal) − atMost(goal − 1)](#5-atmostgoal--atmostgoal--1) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given a binary array `nums` and an integer `goal`, return the number of non-empty subarrays with sum equal to `goal`.

| Input | Output | Why |
|---|---|---|
| `nums = [1,0,1,0,1], goal = 2` | `4` | [1,0,1], [1,0,1,0], [0,1,0,1], [1,0,1] |
| `nums = [0,0,0,0,0], goal = 0` | `15` | every subarray |

**Constraints:** `1 ≤ nums.length ≤ 3·10⁴`, `nums[i] ∈ {0, 1}`, `0 ≤ goal ≤ nums.length`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Brute force: every start | running sum from each start | O(n²) | O(1) |
| Prefix sums + hashmap | count prefix == running − goal | O(n) | O(n) |
| atMost(goal) − atMost(goal − 1) | two at-most windows | O(n) | O(1) |

> [!tip] Interview angle
> The canonical place to introduce the atMost subtraction. Mention that a plain "shrink while sum > goal" window undercounts because of zeros, and that prefix sums are the fallback for non-binary arrays.

---

## 3. Brute force: every start

**Intuition.** For each start, extend with a running sum; count matches; break once the sum exceeds `goal` (values are non-negative).

```python
def binary_sum_brute(nums, goal):
    total = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s == goal:
                total += 1
            elif s > goal:
                break
    return total
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Prefix sums + hashmap

**Intuition.** A subarray `(i, j]` has sum `P[j] − P[i]`. For each `j`, add how many earlier prefixes equal `P[j] − goal`. Same as Subarray Sum Equals K; works for any integers.

```python
def binary_sum_prefix(nums, goal):
    seen = {0: 1}
    s = total = 0
    for x in nums:
        s += x
        total += seen.get(s - goal, 0)
        seen[s] = seen.get(s, 0) + 1
    return total
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. atMost(goal) − atMost(goal − 1)

**Intuition.** `atMost(k)`: expand `r`, shrink while sum > k, then every subarray ending at `r` with start in `[l, r]` has sum ≤ k, so add `r − l + 1`. Subtracting the counts for `k` and `k − 1` leaves exactly-`k`. `atMost(−1)` is 0.

**Algorithm**

1. Define `atMost(k)`: return 0 if `k < 0`; window with running sum; shrink while sum > k; add `r − l + 1`.
2. Return `atMost(goal) − atMost(goal − 1)`.

**Dry run** — [1,0,1,0,1], goal 2: atMost(2) = 1+2+3+4+4 = 14, atMost(1) = 1+2+2+3+2 = 10 → 4.

**C++**
```cpp
int atMostSum(vector<int>& nums, int k) {
    if (k < 0) return 0;
    int l = 0, sum = 0, cnt = 0;
    for (int r = 0; r < (int)nums.size(); r++) {
        sum += nums[r];
        while (sum > k) sum -= nums[l++];
        cnt += r - l + 1;
    }
    return cnt;
}
int numSubarraysWithSum(vector<int>& nums, int goal) {
    return atMostSum(nums, goal) - atMostSum(nums, goal - 1);
}
```

**Java**
```java
static int atMostSum(int[] nums, int k) {
    if (k < 0) return 0;
    int l = 0, sum = 0, cnt = 0;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];
        while (sum > k) sum -= nums[l++];
        cnt += r - l + 1;
    }
    return cnt;
}
static int numSubarraysWithSum(int[] nums, int goal) {
    return atMostSum(nums, goal) - atMostSum(nums, goal - 1);
}
```

**Python**
```python
def num_subarrays_with_sum(nums, goal):
    def at_most(k):
        if k < 0:
            return 0
        l = s = cnt = 0
        for r, x in enumerate(nums):
            s += x
            while s > k:
                s -= nums[l]
                l += 1
            cnt += r - l + 1
        return cnt
    return at_most(goal) - at_most(goal - 1)
```

**Complexity:** time **O(n)**, space **O(1)** — two linear passes, constant space.

---

## Edge cases

- `goal = 0` → count runs of zeros (atMost(−1) = 0 handles it).
- `goal` > total ones → 0.

---

## Common mistakes

1. A single exact-sum window with `while sum > goal` — misses windows that differ by leading zeros.
2. Not guarding `atMost(−1)`; the loop would shrink past `r`.
3. Seeding the prefix map without `{0: 1}`.

---

## Follow-ups

1. Array has negatives.
2. Count subarrays with sum in [lo, hi].

<details><summary>Answer sketches</summary>

**#1:** The window breaks (sums aren't monotone); only prefix sums + hashmap work.

**#2:** atMost(hi) − atMost(lo − 1).
</details>

---

## Flashcards

**Exactly-K counting trick for windows?** #flashcard
exactly(K) = atMost(K) − atMost(K − 1).

**How does atMost count?** #flashcard
After shrinking to validity, add r − l + 1: every start in [l, r] gives a valid subarray ending at r.

**Interview track →** [Sliding-window deep-dive](../../02-algorithms/04-sliding-window.md) · [Two-pointers deep-dive](../../02-algorithms/03-two-pointers.md) · [Sliding-window walkthroughs](../../coding/algorithms/04-sliding-window.md)
