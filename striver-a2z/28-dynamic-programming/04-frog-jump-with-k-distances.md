---
module: striver-a2z/28-dynamic-programming
lesson: 4
topic: Frog jump with K distances
difficulty: Medium
source: https://takeuforward.org/learning/dsa/frog-jump-with-k-distances?category=1d-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, 1d-dp]
---
# 4. Frog jump with K distances

← [Frog Jump](03-frog-jump.md) · [Part 28 index](README.md) · Next → [Maximum sum of non adjacent elements](05-maximum-sum-of-non-adjacent-elements.md)

> [!abstract] Problem at a glance
> **Task:** Same as Frog Jump, but each jump can move 1 to `k` stones ahead.
> **Key insight:** Generalise the last-move recurrence: `dp[i] = min_{j=1..k, i−j≥0} dp[i−j] + |h[i] − h[i−j]|`. Now `k` predecessors are read, so the rolling-variable trick no longer gives O(1). Keep the full array (or a window of size `k`).
> **Difficulty:** Medium · **Pattern:** 1D DP: min over a window of predecessors
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/frog-jump-with-k-distances?category=1d-dp&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoization over k predecessors](#3-memoization-over-k-predecessors) · [4. Tabulation](#4-tabulation) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `heights` and `k`, the frog starts on stone 0. From `i` it may jump to any `i + j` with `1 ≤ j ≤ k`, paying `|heights[i] − heights[i+j]|`. Return the minimum energy to reach the last stone.

| Input | Output | Why |
|---|---|---|
| `heights = [10,30,40,50,20], k = 3` | `30` | 0→1 (20), 1→4 (10) |
| `heights = [10,20,10], k = 1` | `20` | forced 1-step jumps |

**Constraints:** `1 ≤ n ≤ 10⁵`, `1 ≤ k ≤ 100`, `0 ≤ heights[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoization over k predecessors | f(i) = min over j in 1..k | O(n·k) | O(n) |
| Tabulation | fill dp left to right | O(n·k) | O(n) |

> [!tip] Interview angle
> State the complexity honestly as O(n·k). If asked to speed it up, note that `|h[i] − h[j]|` depends on `i`, so a monotonic deque does not apply directly. Splitting into `h[j] ≥ h[i]` and `h[j] < h[i]` needs ordered structures, which is overkill for this constraint.

---

## 3. Memoization over k predecessors

**Intuition.** `f(i)` tries every predecessor `i − j` in range and caches the result.

```python
def frogk_memo(h, k):
    dp = [-1] * len(h)
    def f(i):
        if i == 0:
            return 0
        if dp[i] != -1:
            return dp[i]
        dp[i] = min(f(i - j) + abs(h[i] - h[i - j]) for j in range(1, min(k, i) + 1))
        return dp[i]
    return f(len(h) - 1)
```

**Complexity:** time **O(n·k)**, space **O(n)**.

---

## 4. Tabulation

**Intuition.** `dp[0] = 0`. For each `i`, scan the up-to-`k` previous stones and take the min. Space could drop to O(k) with a circular buffer, but O(n) is the usual answer.

**Algorithm**

1. `dp[0] = 0`.
2. For `i = 1..n−1`: `dp[i] = min over j = 1..min(k, i)` of `dp[i−j] + |h[i] − h[i−j]|`.
3. Return `dp[n−1]`.

**Dry run** — [10,30,40,50,20], k = 3: dp = 0, 20, 30, 40, min(40+30, 30+20, 20+10) = 30.

**C++**
```cpp
int frogJumpK(vector<int>& h, int k) {
    int n = h.size();
    vector<int> dp(n, INT_MAX);
    dp[0] = 0;
    for (int i = 1; i < n; i++)
        for (int j = 1; j <= k && i - j >= 0; j++)
            dp[i] = min(dp[i], dp[i - j] + abs(h[i] - h[i - j]));
    return dp[n - 1];
}
```

**Java**
```java
static int frogJumpK(int[] h, int k) {
    int n = h.length;
    int[] dp = new int[n];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;
    for (int i = 1; i < n; i++)
        for (int j = 1; j <= k && i - j >= 0; j++)
            dp[i] = Math.min(dp[i], dp[i - j] + Math.abs(h[i] - h[i - j]));
    return dp[n - 1];
}
```

**Python**
```python
def frog_jump_k(h, k):
    n = len(h)
    dp = [0] + [float("inf")] * (n - 1)
    for i in range(1, n):
        for j in range(1, min(k, i) + 1):
            dp[i] = min(dp[i], dp[i - j] + abs(h[i] - h[i - j]))
    return dp[n - 1]
```

**Complexity:** time **O(n·k)**, space **O(n)** — n states × k transitions.

---

## Edge cases

- `k ≥ n`: the frog can jump straight to the end, but it may not be optimal.
- `k = 1`: the answer is the sum of adjacent differences.
- `n = 1`: 0.

---

## Common mistakes

1. Looping `j` past `i` (a negative index wraps around silently in Python).
2. Initialising `dp[i]` to 0 before taking the min.

---

## Follow-ups

1. Reconstruct the jumps.
2. Frog may jump only to stones with height ≤ current?

<details><summary>Answer sketches</summary>

**#1:** Record the argmin `j` for each `i`.

**#2:** Add the condition to the inner loop; unreachable stones keep ∞.
</details>

---

## Flashcards

**Frog-K recurrence and cost?** #flashcard
`dp[i] = min_{j≤k} dp[i−j] + |h_i − h_{i−j}|`, O(n·k).

**Why no O(1)-space version here?** #flashcard
Each state reads k predecessors, so you need at least a window of k.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../04-practice/algorithms/15-dynamic-programming.md)
