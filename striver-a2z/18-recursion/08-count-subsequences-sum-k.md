---
module: striver-a2z/18-recursion
lesson: 8
topic: Count All Subsequences with Sum K
difficulty: Medium
source: https://takeuforward.org/learning/dsa/count-all-subsequences-with-sum-k?category=subsequence-pattern-problems&source=strivers-a2z-dsa-sheet
tags: [striver, recursion, recursion, dp, subsequence]
---
# 8. Count All Subsequences with Sum K

← [Check if There Exists a Subsequence with Sum K](07-subsequence-sum-k-exists.md) · [Part 18 index](README.md) · Next → [Generate Binary Strings Without Consecutive 1s](09-binary-strings-no-consecutive-ones.md)

> [!abstract] Problem at a glance
> **Task:** Count the subsequences (by index set) of a positive array whose sum is exactly `k`.
> **Key insight:** Same pick/not-pick tree, but **return a count**: base cases return 1 or 0, and each node returns `take + skip`. Memoise (i, remaining) for O(n · k), or do the 1D counting DP `ways[s] += ways[s − x]` downward.
> **Difficulty:** Medium · **Pattern:** Pick / not-pick counting → counting DP · **Also on:** [GfG Perfect Sum](https://www.geeksforgeeks.org/problems/perfect-sum-problem5633/1)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/count-all-subsequences-with-sum-k?category=subsequence-pattern-problems&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Pick / not-pick counting recursion](#3-pick--not-pick-counting-recursion) · [4. 1D counting DP](#4-1d-counting-dp) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums` of positive integers and an integer `k`, return the number of subsequences whose elements sum to `k`. Subsequences are distinguished by indices, so equal values at different positions count separately. Return the answer modulo 10⁹ + 7.

| Input | Output | Why |
|---|---|---|
| `nums = [4, 9, 2, 5, 1], k = 10` | `2` | [4, 5, 1], [9, 1] |
| `nums = [4, 2, 10, 5, 1, 3], k = 5` | `3` | [4, 1], [2, 3], [5] |
| `nums = [1, 1, 1], k = 2` | `3` | three index pairs |

**Constraints:** `1 ≤ n ≤ 1000`, `1 ≤ nums[i] ≤ 1000`, `1 ≤ k ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Pick / not-pick counting recursion | f(i, rem) = f(i+1, rem − a[i]) + f(i+1, rem) | O(2ⁿ) | O(n) |
| 1D counting DP | ways[s] += ways[s − x], s from k down to x | O(n · k) | O(k) |

> [!tip] Interview angle
> This finishes the three-variant ladder (print all → return any → count). The structural point: printing needs side effects, finding needs short-circuit boolean returns, counting needs summed integer returns. With zeros allowed (GfG variant) the base case must not stop at `rem == 0` early — each zero doubles the count.

---

## 3. Pick / not-pick counting recursion

**Intuition.** At `i == n` return `1 if rem == 0 else 0`. With positive values, prune `rem < 0 → 0`. Every leaf is one subsequence; the sum over leaves is the count.

```python
def count_rec(nums, k):
    def f(i, rem):
        if rem < 0:
            return 0
        if i == len(nums):
            return 1 if rem == 0 else 0
        return f(i + 1, rem - nums[i]) + f(i + 1, rem)
    return f(0, k) % (10**9 + 7)
```

**Complexity:** time **O(2ⁿ)**, space **O(n)**.

---

## 4. 1D counting DP

**Intuition.** `ways[s]` = number of subsets of the processed items with sum s; `ways[0] = 1` (empty subset). Adding item `x` creates `ways[s − x]` new subsets of sum `s`. Downward iteration keeps it 0/1.

**Dry run** — [1, 1, 1], k = 2: start [1,0,0]; x=1 → [1,1,0]; x=1 → [1,2,1]; x=1 → [1,3,3] → 3.

**C++**
```cpp
int countSubsequenceWithTargetSum(vector<int>& nums, int k) {
    const int MOD = 1e9 + 7;
    vector<int> ways(k + 1, 0);
    ways[0] = 1;
    for (int x : nums)
        for (int s = k; s >= x; s--)
            ways[s] = (ways[s] + ways[s - x]) % MOD;
    return ways[k];
}
```

**Java**
```java
static int countSubsequenceWithTargetSum(int[] nums, int k) {
    final int MOD = 1_000_000_007;
    int[] ways = new int[k + 1];
    ways[0] = 1;
    for (int x : nums)
        for (int s = k; s >= x; s--)
            ways[s] = (ways[s] + ways[s - x]) % MOD;
    return ways[k];
}
```

**Python**
```python
def count_subsequence_with_target_sum(nums, k):
    MOD = 10**9 + 7
    ways = [1] + [0] * k
    for x in nums:
        for s in range(k, x - 1, -1):
            ways[s] = (ways[s] + ways[s - x]) % MOD
    return ways[k]
```

**Complexity:** time **O(n · k)**, space **O(k)** — n × k additions; one row.

---

## Edge cases

- Duplicates — count by index, not by value.
- No subsequence → 0.
- Zeros (GfG variant) double the count; don't stop at rem == 0.

---

## Common mistakes

1. Returning 1 as soon as `rem == 0` before `i == n` — wrong once zeros exist.
2. Upward iteration in 1D DP.
3. Missing the modulo when counts grow (n = 1000).

---

## Follow-ups

1. Elements can be 0.
2. Target Sum (LC 494): assign ± to every element.
3. Count with each element usable unlimited times (coin change II).

<details><summary>Answer sketches</summary>

**#1:** Use the `i == n` base case only; or count zeros z and multiply the zero-free answer by 2ᶻ.

**#2:** Reduce to counting subsets with sum (total + target)/2.

**#3:** Iterate s upward.
</details>

---

## Flashcards

**Counting version of the subsequence template?** #flashcard
Base returns 1/0; node returns take + skip.

**Three subsequence variants and their return types?** #flashcard
Print all: void + side effect. Any one: bool short-circuit. Count: int sum.

**Interview track →** [Recursion deep-dive](../../02-algorithms/09-recursion.md) · [Backtracking deep-dive](../../02-algorithms/12-backtracking.md) · [Recursion walkthroughs](../../04-practice/algorithms/09-recursion.md) · [Backtracking walkthroughs](../../04-practice/algorithms/12-backtracking.md)
