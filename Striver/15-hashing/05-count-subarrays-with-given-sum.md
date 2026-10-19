---
module: striver/15-hashing
lesson: 5
topic: Count Subarrays with Given Sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-subarrays-with-given-sum?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, hashing, hashing, prefix-sum]
---
# 5. Count Subarrays with Given Sum

← [Largest Subarray with Sum 0](04-largest-subarray-with-sum-0.md) · [Part 15 index](README.md) · Next → [Count Subarrays with Given XOR K](06-count-subarrays-with-xor-k.md)

> [!abstract] Problem at a glance
> **Task:** Return how many contiguous subarrays sum to exactly `k`. Values may be negative.
> **Key insight:** Every earlier prefix equal to `P[i] − k` starts one valid subarray ending at `i`. Keep a **count** of each prefix value seen, seeded `{0: 1}`, and add `cnt[p − k]` before recording `p`.
> **Difficulty:** Medium · **Pattern:** Prefix sum + count map · **Also on:** [LC 560](https://leetcode.com/problems/subarray-sum-equals-k/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-subarrays-with-given-sum?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. All subarrays with a running sum](#3-all-subarrays-with-a-running-sum) · [4. Prefix sum + count map](#4-prefix-sum--count-map) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an integer array `nums` and an integer `k`, return the total number of subarrays whose sum equals `k`.

| Input | Output | Why |
|---|---|---|
| `nums = [1, 1, 1], k = 2` | `2` | [1, 1] twice |
| `nums = [1, 2, 3], k = 3` | `2` | [1, 2], [3] |
| `nums = [3, 1, 2, 4], k = 6` | `2` | [3, 1, 2], [2, 4] |

**Constraints:** `1 ≤ n ≤ 2·10⁴`, `−1000 ≤ nums[i] ≤ 1000`, `−10⁷ ≤ k ≤ 10⁷`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| All subarrays with a running sum | fix l, extend r, count hits | O(n²) | O(1) |
| Prefix sum + count map | ans += cnt[p − k]; then cnt[p] += 1; seed {0: 1} | O(n) average | O(n) |

> [!tip] Interview angle
> The answer can reach n(n + 1)/2 ≈ 2·10⁸ here, still an `int`; for larger n use 64-bit. A sliding window doesn't work even for counting when negatives are present.

---

## 3. All subarrays with a running sum

**Intuition.** Count rather than maximise. Note there's no early break: later elements can bring the sum back to `k`.

```python
def subarray_sum_brute(nums, k):
    count = 0
    for l in range(len(nums)):
        s = 0
        for r in range(l, len(nums)):
            s += nums[r]
            if s == k:
                count += 1
    return count
```

**Complexity:** time **O(n²)**, space **O(1)**.

---

## 4. Prefix sum + count map

**Intuition.** Valid starts for a subarray ending at `i` are exactly the earlier positions whose prefix is `p − k`; there may be several (zeros and negatives repeat prefixes), so we need their count, not one index. The seed `{0: 1}` counts the empty prefix, i.e. subarrays starting at 0. Look up before incrementing `cnt[p]` so that, for `k = 0`, the current prefix doesn't match itself (the empty subarray).

**Dry run** — `[3 1 2 4]`, k = 6: cnt{0:1}. p=3: need −3 → 0; cnt{0,3}. p=4: need −2 → 0. p=6: need 0 → +1. p=10: need 4 → +1. Answer 2.

**C++**
```cpp
int subarraySum(vector<int>& nums, int k) {
    unordered_map<long long, int> cnt;
    cnt[0] = 1;
    long long p = 0;
    int ans = 0;
    for (int x : nums) {
        p += x;
        auto it = cnt.find(p - k);
        if (it != cnt.end()) ans += it->second;
        cnt[p]++;
    }
    return ans;
}
```

**Java**
```java
static int subarraySum(int[] nums, int k) {
    HashMap<Long, Integer> cnt = new HashMap<>();
    cnt.put(0L, 1);
    long p = 0;
    int ans = 0;
    for (int x : nums) {
        p += x;
        ans += cnt.getOrDefault(p - k, 0);
        cnt.merge(p, 1, Integer::sum);
    }
    return ans;
}
```

**Python**
```python
def subarray_sum(nums, k):
    cnt = {0: 1}
    p = ans = 0
    for x in nums:
        p += x
        ans += cnt.get(p - k, 0)
        cnt[p] = cnt.get(p, 0) + 1
    return ans
```

**Complexity:** time **O(n) average**, space **O(n)**.

---

## Edge cases

- k = 0 with zeros: `[0, 0, 0]` → 6.
- Negatives creating repeated prefixes.
- Whole array is the only answer.

---

## Common mistakes

1. Seeding `{0: 0}` or nothing → misses subarrays from index 0.
2. Incrementing `cnt[p]` before the lookup → over-counts when k = 0.
3. Storing one index per prefix (the 'longest' map) instead of a count.

---

## Follow-ups

1. Subarray sums divisible by k (LC 974).
2. Binary array, count subarrays with sum = goal (LC 930).
3. Number of submatrices summing to target (LC 1074).
4. XOR instead of sum.

<details><summary>Answer sketches</summary>

**#1:** Count map over `p mod k`, normalised: `((p % k) + k) % k`.

**#2:** Same map, or atMost(goal) − atMost(goal − 1) with a window: [Sliding Window](../22-sliding-window-and-2-pointer/README.md).

**#3:** Fix a pair of rows, collapse columns, run this on the 1-D column sums: O(r²·c).

**#4:** [Count Subarrays with XOR K](06-count-subarrays-with-xor-k.md).
</details>

---

## Flashcards

**Count subarrays sum k: seed?** #flashcard
{0: 1} — the empty prefix.

**Count subarrays sum k: order of operations?** #flashcard
ans += cnt[p − k] first, then cnt[p]++.

**Why can't a sliding window count sum-k subarrays with negatives?** #flashcard
The window sum isn't monotone, so you can't decide which pointer to move.

**Interview track →** [Hashing deep-dive](../../01-data-structures/02-hashing.md) · [Hashing walkthroughs](../../coding/data-structures/02-hashing.md) · [Sliding window](../../02-algorithms/04-sliding-window.md)
