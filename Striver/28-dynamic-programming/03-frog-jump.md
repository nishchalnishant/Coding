---
module: striver/28-dynamic-programming
lesson: 3
topic: Frog Jump
difficulty: Easy
source: https://takeuforward.org/learning/dsa/frog-jump?category=1d-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, 1d-dp]
---
# 3. Frog Jump

← [Climbing stairs](02-climbing-stairs.md) · [Part 28 index](README.md) · Next → [Frog jump with K distances](04-frog-jump-with-k-distances.md)

> [!abstract] Problem at a glance
> **Task:** A frog jumps from stone `0` to stone `n−1`, each jump going 1 or 2 stones ahead and costing `|h[i] − h[j]|`. Minimise the total energy.
> **Key insight:** Stone `i` is reached from `i−1` or `i−2`, so `dp[i] = min(dp[i−1] + |h[i]−h[i−1]|, dp[i−2] + |h[i]−h[i−2]|)`. Greedy (always take the cheaper next jump) fails, because a cheap jump now can force an expensive one later.
> **Difficulty:** Easy · **Pattern:** 1D DP: min over last move
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/frog-jump?category=1d-dp&source=strivers-a2z-dsa-sheet) · **Time:** 15 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Recursion over the last jump](#3-recursion-over-the-last-jump) · [4. Memoization](#4-memoization) · [5. Tabulation, O(1) space](#5-tabulation-o1-space) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `heights[0..n−1]`, a frog starts on stone 0. From stone `i` it can jump to `i+1` or `i+2`, paying `|heights[i] − heights[j]|`. Return the minimum total energy needed to reach stone `n−1`.

| Input | Output | Why |
|---|---|---|
| `heights = [10,20,30,10]` | `20` | 0→1 (10) then 1→3 (10) |
| `heights = [10,50,10]` | `0` | jump 0→2 directly |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ heights[i] ≤ 10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Recursion over the last jump | f(i) = min of the two predecessors | O(2ⁿ) | O(n) |
| Memoization | cache f(i) | O(n) | O(n) |
| Tabulation, O(1) space | keep dp[i−1], dp[i−2] only | O(n) | O(1) |

> [!tip] Interview angle
> Show a counter-example to greedy before writing the DP: `[30, 10, 60, 10, 60, 50]`. Greedy picks the cheaper next jump each time and pays 60, while the optimum is 40.

---

## 3. Recursion over the last jump

**Intuition.** `f(i)` = min energy to reach stone `i`. The final jump into `i` came from `i−1` or (if `i > 1`) `i−2`. Base: `f(0) = 0`.

```python
def frog_rec(h):
    def f(i):
        if i == 0:
            return 0
        best = f(i - 1) + abs(h[i] - h[i - 1])
        if i > 1:
            best = min(best, f(i - 2) + abs(h[i] - h[i - 2]))
        return best
    return f(len(h) - 1)
```

**Complexity:** time **O(2ⁿ)**, space **O(n)**.

---

## 4. Memoization

**Intuition.** Same recurrence with `dp[i]` cached. Each of the `n` states does O(1) work.

```python
def frog_memo(h):
    dp = [-1] * len(h)
    def f(i):
        if i == 0:
            return 0
        if dp[i] != -1:
            return dp[i]
        best = f(i - 1) + abs(h[i] - h[i - 1])
        if i > 1:
            best = min(best, f(i - 2) + abs(h[i] - h[i - 2]))
        dp[i] = best
        return best
    return f(len(h) - 1)
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 5. Tabulation, O(1) space

**Intuition.** Compute `dp[i]` left to right. Only the last two values are read, so roll two variables.

**Algorithm**

1. `prev = 0` (dp[0]), `prev2 = 0` (unused until i = 2).
2. For `i = 1..n−1`: `one = prev + |h[i]−h[i−1]|`; `two = i > 1 ? prev2 + |h[i]−h[i−2]| : ∞`; `cur = min(one, two)`.
3. Shift: `prev2 = prev`, `prev = cur`. Return `prev`.

**Dry run** — [10,20,30,10]: dp = 0, 10, min(10+10, 0+20) = 20, min(20+20, 10+10) = 20 → 20.

**C++**
```cpp
int frogJump(vector<int>& h) {
    int n = h.size(), prev = 0, prev2 = 0;
    for (int i = 1; i < n; i++) {
        int one = prev + abs(h[i] - h[i - 1]);
        int two = i > 1 ? prev2 + abs(h[i] - h[i - 2]) : INT_MAX;
        int cur = min(one, two);
        prev2 = prev;
        prev = cur;
    }
    return prev;
}
```

**Java**
```java
static int frogJump(int[] h) {
    int n = h.length, prev = 0, prev2 = 0;
    for (int i = 1; i < n; i++) {
        int one = prev + Math.abs(h[i] - h[i - 1]);
        int two = i > 1 ? prev2 + Math.abs(h[i] - h[i - 2]) : Integer.MAX_VALUE;
        int cur = Math.min(one, two);
        prev2 = prev;
        prev = cur;
    }
    return prev;
}
```

**Python**
```python
def frog_jump(h):
    prev = prev2 = 0
    for i in range(1, len(h)):
        one = prev + abs(h[i] - h[i - 1])
        two = prev2 + abs(h[i] - h[i - 2]) if i > 1 else float("inf")
        prev2, prev = prev, min(one, two)
    return prev
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, two rolling values.

---

## Edge cases

- `n = 1`: already there, cost 0.
- `n = 2`: only the single jump.
- Equal heights: cost 0 everywhere.

---

## Common mistakes

1. Greedy next-cheaper-jump.
2. Accessing `h[i−2]` when `i = 1`.
3. Initialising `dp` with 0 and taking `min`, which wrongly yields 0.

---

## Follow-ups

1. Up to `k` stones per jump?
2. Print the path.

<details><summary>Answer sketches</summary>

**#1:** The next lesson: `dp[i] = min_{1≤j≤k} dp[i−j] + |h[i]−h[i−j]|`, O(n·k).

**#2:** Store which predecessor won at each `i`, then walk back from `n−1`.
</details>

---

## Flashcards

**Frog jump recurrence?** #flashcard
`dp[i] = min(dp[i−1] + |h_i − h_{i−1}|, dp[i−2] + |h_i − h_{i−2}|)`.

**Why not greedy?** #flashcard
A cheap jump now can force an expensive one later, e.g. [30,10,60,10,60,50].

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
