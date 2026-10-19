---
module: striver/16-binary-search
lesson: 28
topic: Split Array — Largest Sum
difficulty: Hard
source: https://takeuforward.org/learning/dsa/split-array---largest-sum?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, binary-search, binary-search, bs-on-answer, greedy, dp]
---
# 28. Split Array — Largest Sum

← [Minimize Max Distance to Gas Station](27-minimise-max-distance-to-gas-station.md) · [Part 16 index](README.md) · Next → [Find Row with Maximum 1's](29-row-with-maximum-ones.md)

> [!abstract] Problem at a glance
> **Task:** Split `nums` into `k` non-empty contiguous subarrays minimising the largest subarray sum.
> **Key insight:** Third name for the same problem (Book Allocation, Painter's Partition). Binary search the largest sum `[max, Σ]` with the greedy part counter.
> **Difficulty:** Hard · **Pattern:** Binary search on answer + greedy partition · **Also on:** [LC 410](https://leetcode.com/problems/split-array-largest-sum/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/split-array---largest-sum?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DP over prefixes](#3-dp-over-prefixes) · [4. Binary search on largest sum](#4-binary-search-on-largest-sum) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty subarrays such that the largest sum of any subarray is minimised. Return that minimised largest sum.

| Input | Output | Why |
|---|---|---|
| `nums = [7, 2, 5, 10, 8], k = 2` | `18` | [7 2 5] [10 8] |
| `nums = [1, 2, 3, 4, 5], k = 2` | `9` | [1 2 3] [4 5] |

**Constraints:** `1 ≤ n ≤ 1000`, `0 ≤ nums[i] ≤ 10⁶`, `1 ≤ k ≤ min(50, n)`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DP over prefixes | dp[j][i] = min over p of max(dp[j−1][p], sum(p..i)) | O(k · n²) | O(k · n) |
| Binary search on largest sum | parts(cap) ≤ k → go left | O(n log Σ) | O(1) |

> [!tip] Interview angle
> Mention the DP alternative to show breadth: `dp[i][j]` = best for the first `i` elements in `j` parts, O(n² k). Binary search wins at O(n log Σ).

---

## 3. DP over prefixes

**Intuition.** Classic partition DP with prefix sums.

```python
def split_array_dp(nums, k):
    n = len(nums)
    pre = [0] * (n + 1)
    for i, x in enumerate(nums):
        pre[i + 1] = pre[i] + x
    inf = float("inf")
    dp = [[inf] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 0
    for j in range(1, k + 1):
        for i in range(1, n + 1):
            for p in range(j - 1, i):
                dp[j][i] = min(dp[j][i], max(dp[j - 1][p], pre[i] - pre[p]))
    return dp[k][n]
```

**Complexity:** time **O(k · n²)**, space **O(k · n)**.

---

## 4. Binary search on largest sum

**Intuition.** Greedy: extend the current part while it fits under `cap`. Feasible iff parts ≤ k (k ≤ n, so extra parts can always be carved off).

**Dry run** — `[7 2 5 10 8]`, k 2: lo 10 hi 32 mid 21 → [7 2 5] [10 8] 2 ✓ hi 20; mid 15 → [7 2 5] [10] [8] 3 ✗ lo 16; mid 18 → 2 ✓ hi 17; mid 16 ✗ lo 17; mid 17 ✗ lo 18 → 18.

**C++**
```cpp
int splitArray(vector<int>& nums, int k) {
    long long lo = 0, hi = 0;
    for (int x : nums) { lo = max(lo, (long long)x); hi += x; }
    long long ans = hi;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2, cur = 0;
        int parts = 1;
        for (int x : nums) {
            if (cur + x > mid) { parts++; cur = 0; }
            cur += x;
        }
        if (parts <= k) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return (int)ans;
}
```

**Java**
```java
static int splitArray(int[] nums, int k) {
    long lo = 0, hi = 0;
    for (int x : nums) { lo = Math.max(lo, x); hi += x; }
    long ans = hi;
    while (lo <= hi) {
        long mid = lo + (hi - lo) / 2, cur = 0;
        int parts = 1;
        for (int x : nums) {
            if (cur + x > mid) { parts++; cur = 0; }
            cur += x;
        }
        if (parts <= k) { ans = mid; hi = mid - 1; }
        else lo = mid + 1;
    }
    return (int) ans;
}
```

**Python**
```python
def split_array(nums, k):
    def parts(cap):
        p, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                p, cur = p + 1, 0
            cur += x
        return p
    lo, hi = max(nums), sum(nums)
    ans = hi
    while lo <= hi:
        mid = (lo + hi) // 2
        if parts(mid) <= k:
            ans, hi = mid, mid - 1
        else:
            lo = mid + 1
    return ans
```

**Complexity:** time **O(n log Σ)**, space **O(1)** — log(Σ) greedy checks.

---

## Edge cases

- k = n → max(nums).
- Zeros in the array.
- k = 1 → Σ.

---

## Common mistakes

1. Lower bound 0 / 1 instead of max(nums).
2. 32-bit Σ when values reach 10⁶ × 1000 = 10⁹ (borderline).

---

## Follow-ups

1. Minimise the *difference* between largest and smallest part.
2. Return the split.

<details><summary>Answer sketches</summary>

**#1:** No monotone predicate; DP.

**#2:** Greedy at the answer; if fewer than k parts, split remaining multi-element parts.
</details>

---

## Flashcards

**Split array largest sum — two solutions?** #flashcard
BS on answer O(n log Σ); DP O(k n²).

**Book allocation = painter's partition = ?** #flashcard
Split array largest sum.

**Interview track →** [Binary search deep-dive](../../02-algorithms/11-binary-search.md) · [Binary search walkthroughs](../../coding/algorithms/11-binary-search.md)
