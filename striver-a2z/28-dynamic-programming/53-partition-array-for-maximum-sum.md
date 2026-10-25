---
module: striver-a2z/28-dynamic-programming
lesson: 53
topic: Partition array for maximum sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/partition-array-for-maximum-sum?category=mcm-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, partition-dp]
---
# 53. Partition array for maximum sum

← [Palindrome partitioning II](52-palindrome-partitioning-ii.md) · [Part 28 index](README.md) · Next → [Minimum path sum in a grid](54-minimum-path-sum-in-a-grid.md)

> [!abstract] Problem at a glance
> **Task:** Split into contiguous blocks of length ≤ k; each block becomes its max. Maximise the total.
> **Key insight:** Front partition: `dp[i]` = best for the suffix `arr[i..]`. Try the first block `arr[i..j]` for `j < i + k`, keeping a running max: `dp[i] = max over j of maxSoFar·(j − i + 1) + dp[j+1]`. It is O(n·k), and the running max avoids rescanning each block.
> **Difficulty:** Medium · **Pattern:** Front partition DP · **Also on:** LC 1043
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/partition-array-for-maximum-sum?category=mcm-dp&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized f(i)](#3-memoized-fi) · [4. Bottom-up suffix dp](#4-bottom-up-suffix-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `arr` and `k`, partition the array into contiguous subarrays of length at most `k`. Each element of a subarray becomes that subarray's maximum. Return the largest possible sum.

| Input | Output | Why |
|---|---|---|
| `[1,15,7,9,2,5,10], k = 3` | `84` | [15,15,15,9,10,10,10] |
| `[1,4,1,5,7,3,6,1,9,9,3], k = 4` | `83` |  |
| `[1], k = 1` | `1` |  |

**Constraints:** `1 ≤ n ≤ 500`, `0 ≤ arr[i] ≤ 10⁹`, `1 ≤ k ≤ n`. The answer fits in 32-bit on LC.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized f(i) | first block length 1..k | O(n·k) | O(n) |
| Bottom-up suffix dp | i from n−1 down | O(n·k) | O(n) |

> [!tip] Interview angle
> It is the same shape as palindrome partitioning II: choose where the first block ends. State the running-max optimisation. A backward or forward fill is fine; forward `dp[i]` = best for the prefix of length `i` works too.

---

## 3. Memoized f(i)

**Intuition.** `f(n) = 0`. Extend the block one element at a time, tracking its max.

```python
def pams_memo(arr, k):
    from functools import lru_cache
    n = len(arr)
    @lru_cache(None)
    def f(i):
        if i == n:
            return 0
        best = mx = 0
        for j in range(i, min(n, i + k)):
            mx = max(mx, arr[j])
            best = max(best, mx * (j - i + 1) + f(j + 1))
        return best
    return f(0)
```

**Complexity:** time **O(n·k)**, space **O(n)**.

---

## 4. Bottom-up suffix dp

**Intuition.** The same recurrence, filled from the right.

**Algorithm**

1. `dp[n] = 0`.
2. For `i = n−1..0`: `mx = 0`; for `j = i..min(n, i+k)−1`: `mx = max(mx, arr[j])`, `dp[i] = max(dp[i], mx·(j−i+1) + dp[j+1])`.
3. Return `dp[0]`.

**Dry run** — [1,15,7,9,2,5,10], k = 3: dp[4] = 30, dp[3] = 39, dp[1] = 45 + dp[4] = 75, dp[0] = 84.

**C++**
```cpp
int maxSumAfterPartitioning(vector<int>& arr, int k) {
    int n = arr.size();
    vector<int> dp(n + 1, 0);
    for (int i = n - 1; i >= 0; i--) {
        int mx = 0;
        for (int j = i; j < min(n, i + k); j++) {
            mx = max(mx, arr[j]);
            dp[i] = max(dp[i], mx * (j - i + 1) + dp[j + 1]);
        }
    }
    return dp[0];
}
```

**Java**
```java
static int maxSumAfterPartitioning(int[] arr, int k) {
    int n = arr.length;
    int[] dp = new int[n + 1];
    for (int i = n - 1; i >= 0; i--) {
        int mx = 0;
        for (int j = i; j < Math.min(n, i + k); j++) {
            mx = Math.max(mx, arr[j]);
            dp[i] = Math.max(dp[i], mx * (j - i + 1) + dp[j + 1]);
        }
    }
    return dp[0];
}
```

**Python**
```python
def max_sum_after_partitioning(arr, k):
    n = len(arr)
    dp = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        mx = 0
        for j in range(i, min(n, i + k)):
            mx = max(mx, arr[j])
            dp[i] = max(dp[i], mx * (j - i + 1) + dp[j + 1])
    return dp[0]
```

**Complexity:** time **O(n·k)**, space **O(n)** — n start positions × k block lengths.

---

## Edge cases

- `k = 1`: the array sum.
- `k = n`: `n · max`.

---

## Common mistakes

1. Recomputing the block max with an inner scan (O(n·k²)).
2. Allowing blocks longer than `k`.

---

## Follow-ups

1. Minimise instead (block becomes its min)?
2. Return the partition.

<details><summary>Answer sketches</summary>

**#1:** Same DP with min and a running min.

**#2:** Store the best `j` per `i` and follow it.
</details>

---

## Flashcards

**Partition for max sum recurrence?** #flashcard
dp[i] = max over block i..j (len ≤ k) of max·len + dp[j+1].

**Front partition DP shape?** #flashcard
dp[i] over suffixes; loop over where the first block ends.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
