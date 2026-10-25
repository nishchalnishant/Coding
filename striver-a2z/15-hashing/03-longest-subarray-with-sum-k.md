---
module: striver-a2z/15-hashing
lesson: 3
topic: Longest Subarray with Sum K
difficulty: Medium
source: https://takeuforward.org/learning/dsa/longest-subarray-with-sum-k?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, hashing, hashing, prefix-sum, array]
---
# 3. Longest Subarray with Sum K

← [Longest Consecutive Sequence in an Array](02-longest-consecutive-sequence.md) · [Part 15 index](README.md) · Next → [Largest Subarray with Sum 0](04-largest-subarray-with-sum-0.md)

> [!abstract] Problem at a glance
> **Task:** Return the length of the longest contiguous subarray whose sum equals `k`. Values may be negative.
> **Key insight:** `sum(l..i) = P[i] − P[l − 1]`. At index `i`, the longest subarray ending here starts right after the **earliest** index whose prefix was `P[i] − k`. Store each prefix's first index only, seeded with `{0: −1}`.
> **Difficulty:** Medium · **Pattern:** Prefix sum + first-index map · **Also on:** [LC 325 (premium)](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/longest-subarray-with-sum-k?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All subarrays with a running sum](#3-all-subarrays-with-a-running-sum) · [4. Sliding window (non-negative values only)](#4-sliding-window-non-negative-values-only) · [5. Prefix sum + first-index map](#5-prefix-sum--first-index-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` (may contain negatives and zeros) and an integer `k`, return the length of the longest subarray with sum exactly `k`. Return 0 if none exists.

| Input | Output | Why |
|---|---|---|
| `nums = [10, 5, 2, 7, 1, 9], k = 15` | `4` | [5, 2, 7, 1] |
| `nums = [-3, 2, 1], k = 6` | `0` |  |
| `nums = [1, -1, 5, -2, 3], k = 3` | `4` | [1, −1, 5, −2] |

**Constraints:** `1 ≤ n ≤ 10⁵`, `−10⁵ ≤ nums[i] ≤ 10⁵`, `−10⁹ ≤ k ≤ 10⁹`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All subarrays with a running sum | fix l, extend r, accumulate | O(n²) | O(1) |
| Sliding window (non-negative values only) | grow r; shrink l while sum > k | O(n) | O(1) |
| Prefix sum + first-index map | first[p] = earliest index; seed {0: −1}; len = i − first[p − k] | O(n) average | O(n) |

> [!tip] Interview angle
> Ask immediately: "can values be negative?" All non-negative → sliding window, O(1) space (shown below as a variant). Negatives → prefix + map is required.

---

## 3. All subarrays with a running sum

**Intuition.** Fix the start, extend the end while keeping a running sum — no third loop needed.

```python
def longest_subarray_k_brute(nums, k):
    best = 0
    for l in range(len(nums)):
        s = 0
        for r in range(l, len(nums)):
            s += nums[r]
            if s == k:
                best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Sliding window (non-negative values only)

**Intuition.** With every value ≥ 0, the window sum is monotone: extending never decreases it, shrinking never increases it. So when the sum exceeds `k`, the only fix is moving `l`. One negative breaks this (`[3, −1, 1]`, k = 3: shrinking past 3 loses the answer `[3, −1, 1]`). Shown for contrast; it is not run against the negative tests.

```python
def longest_subarray_k_window(nums, k):
    # valid only when all nums[i] >= 0
    l = s = best = 0
    for r, x in enumerate(nums):
        s += x
        while s > k and l <= r:
            s -= nums[l]
            l += 1
        if s == k:
            best = max(best, r - l + 1)
    return best
```

**Complexity:** time **O(n)**, space **O(1)**.

---

## 5. Prefix sum + first-index map

**Intuition.** A subarray `(j, i]` has sum `k` iff `P[i] − P[j] = k`, i.e. `P[j] = P[i] − k`. To maximise `i − j`, we want the smallest such `j`, so the map keeps the **first** index where each prefix value occurred and never overwrites it. The seed `{0: −1}` represents the empty prefix before index 0, so subarrays starting at index 0 are found.

**Algorithm**

1. `first = {0: −1}`, `p = 0`, `best = 0`.
2. For each `i`: `p += nums[i]`.
3. If `p − k` in `first`: `best = max(best, i − first[p − k])`.
4. If `p` not in `first`: `first[p] = i` (keep the earliest).

**Dry run** — `[1 −1 5 −2 3]`, k = 3: p = 1, 0, 5, 3, 6. i=0: need −2 ✗, first{0:−1, 1:0}. i=1: p=0, need −3 ✗, 0 already present. i=2: p=5, need 2 ✗, add 5:2. i=3: p=3, need 0 → i − (−1) = 4 ✓. i=4: p=6, need 3 → 4 − 3 = 1. Answer 4.

**C++**
```cpp
int longestSubarray(vector<int>& nums, int k) {
    unordered_map<long long, int> first;
    first[0] = -1;
    long long p = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        p += nums[i];
        auto it = first.find(p - k);
        if (it != first.end()) best = max(best, i - it->second);
        if (!first.count(p)) first[p] = i;
    }
    return best;
}
```

**Java**
```java
static int longestSubarray(int[] nums, int k) {
    HashMap<Long, Integer> first = new HashMap<>();
    first.put(0L, -1);
    long p = 0;
    int best = 0;
    for (int i = 0; i < nums.length; i++) {
        p += nums[i];
        Integer j = first.get(p - k);
        if (j != null) best = Math.max(best, i - j);
        first.putIfAbsent(p, i);
    }
    return best;
}
```

**Python**
```python
def longest_subarray(nums, k):
    first = {0: -1}
    p = best = 0
    for i, x in enumerate(nums):
        p += x
        if p - k in first:
            best = max(best, i - first[p - k])
        if p not in first:
            first[p] = i
    return best
```

**Complexity:** time **O(n) average**, space **O(n)**.

---

## Edge cases

- Answer starts at index 0 (needs the seed).
- Zeros: `[2, 0, 0, 3]`, k = 3 → length 3 (`[0, 0, 3]`).
- k = 0 with zeros and cancelling pairs.
- No valid subarray → 0.
- Prefix overflow: use `long long` / `long` for the prefix and the map key.

---

## Common mistakes

1. Overwriting `first[p]` with later indices → shorter answers.
2. Missing the `{0: −1}` seed.
3. Using a sliding window when negatives are allowed.
4. Inserting `p` before the lookup — harmless here when k ≠ 0, but wrong for k = 0 (gives length 0 matches).

---

## Follow-ups

1. Shortest subarray with sum k.
2. Sum ≥ k with negatives (LC 862).
3. Longest subarray with sum divisible by k.
4. Binary array, equal 0s and 1s (LC 525).

<details><summary>Answer sketches</summary>

**#1:** Keep the **latest** index per prefix instead (overwrite).

**#2:** Monotonic deque over prefix sums: [Stack / Queues](../23-stack-and-queues/README.md).

**#3:** Map `p mod k` (normalised to non-negative) to its first index.

**#4:** Map 0 → −1, then longest subarray with sum 0: [Largest Subarray with Sum 0](04-largest-subarray-with-sum-0.md).
</details>

---

## Flashcards

**Longest subarray sum k with negatives?** #flashcard
Prefix sum + map of first index; seed {0: −1}; len = i − first[p − k].

**Why never overwrite first[p]?** #flashcard
The earliest index gives the longest subarray.

**When does a sliding window suffice?** #flashcard
All values non-negative (sum is monotone in the window).

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Hashing walkthroughs](../../04-practice/data-structures/02-hashing.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
