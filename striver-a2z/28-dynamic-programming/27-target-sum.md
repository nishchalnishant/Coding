---
module: striver-a2z/28-dynamic-programming
lesson: 27
topic: Target sum
difficulty: Medium
source: https://takeuforward.org/learning/dsa/target-sum?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, subsequence, counting]
---
# 27. Target sum

← [Minimum coins](26-minimum-coins.md) · [Part 28 index](README.md) · Next → [Coin change II](28-coin-change-ii.md)

> [!abstract] Problem at a glance
> **Task:** Assign `+` or `−` to each number to reach `target`; count the assignments.
> **Key insight:** Let `P` be the `+` set and `N` the `−` set. Then `P − N = target` and `P + N = S`, so `P = (S + target)/2`. That is count partitions with a given difference: count subsets with sum `(S + target)/2`, with zeros doubling the count.
> **Difficulty:** Medium · **Pattern:** Sign assignment → count subsets · **Also on:** LC 494
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/target-sum?category=dp-on-subsequences&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion over signs](#3-recursion-over-signs) · [4. Count subsets with sum (S + target)/2](#4-count-subsets-with-sum-s--target2) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums` (non-negative) and `target`, return the number of ways to put `+` or `−` before each number so that the expression evaluates to `target`.

| Input | Output | Why |
|---|---|---|
| `nums = [1,1,1,1,1], target = 3` | `5` | choose which one is negative |
| `nums = [1], target = 1` | `1` |  |

**Constraints:** `1 ≤ n ≤ 20`, `0 ≤ nums[i] ≤ 1000`, `Σ nums ≤ 1000`, `−1000 ≤ target ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursion over signs | f(i, sum) tries ± | O(2ⁿ) | O(n) |
| Count subsets with sum (S + target)/2 | reduction + 1D counting | O(n·S) | O(S) |

> [!tip] Interview angle
> Brute force is `2ⁿ` (fine for n ≤ 20, so say so). Then show the reduction. Handle a negative `target` with `abs(target)`: by symmetry the count is the same.

---

## 3. Recursion over signs

**Intuition.** Try both signs for every number and count the leaves equal to `target`.

```python
def target_rec(nums, target):
    def f(i, cur):
        if i == len(nums):
            return 1 if cur == target else 0
        return f(i + 1, cur + nums[i]) + f(i + 1, cur - nums[i])
    return f(0, 0)
```

**Complexity:** time **O(2ⁿ)**, space **O(n)**.

---

## 4. Count subsets with sum (S + target)/2

**Intuition.** Check that `S + |target|` is even and `|target| ≤ S`, then run the counting DP.

**Algorithm**

1. `t = |target|`; if `t > S` or `(S + t)` odd → 0.
2. `k = (S + t)/2`; `dp[0] = 1`; for each `x`, `j = k..x`: `dp[j] += dp[j − x]`.
3. Return `dp[k]`.

**Dry run** — [1,1,1,1,1], 3: S = 5, k = 4 → C(5,4) = 5.

**C++**
```cpp
int findTargetSumWays(vector<int>& nums, int target) {
    int S = 0;
    for (int x : nums) S += x;
    int t = abs(target);
    if (t > S || (S + t) % 2) return 0;
    int k = (S + t) / 2;
    vector<int> dp(k + 1, 0);
    dp[0] = 1;
    for (int x : nums)
        for (int j = k; j >= x; j--)
            dp[j] += dp[j - x];
    return dp[k];
}
```

**Java**
```java
static int findTargetSumWays(int[] nums, int target) {
    int S = 0;
    for (int x : nums) S += x;
    int t = Math.abs(target);
    if (t > S || (S + t) % 2 == 1) return 0;
    int k = (S + t) / 2;
    int[] dp = new int[k + 1];
    dp[0] = 1;
    for (int x : nums)
        for (int j = k; j >= x; j--)
            dp[j] += dp[j - x];
    return dp[k];
}
```

**Python**
```python
def find_target_sum_ways(nums, target):
    S, t = sum(nums), abs(target)
    if t > S or (S + t) % 2:
        return 0
    k = (S + t) // 2
    dp = [1] + [0] * k
    for x in nums:
        for j in range(k, x - 1, -1):
            dp[j] += dp[j - x]
    return dp[k]
```

**Complexity:** time **O(n·S)**, space **O(S)** — n × S/2 additions instead of 2ⁿ.

---

## Edge cases

- Negative target: same count as `|target|`.
- Zeros: `±0` are two different assignments, so the count doubles.
- `|target| > S`: 0.

---

## Common mistakes

1. Missing the parity / range check, which reads a negative index.
2. Not using `abs(target)`.

---

## Follow-ups

1. Return one valid assignment.
2. Offset-array DP instead?

<details><summary>Answer sketches</summary>

**#1:** Backtrack through the 2D table.

**#2:** `dp[i][sum + S]`, which handles any signs at O(n·2S).
</details>

---

## Flashcards

**Target sum reduction?** #flashcard
Count subsets with sum (S + |target|)/2.

**Zeros in target sum?** #flashcard
Each doubles the count (+0 / −0).

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
