---
module: striver/28-dynamic-programming
lesson: 7
topic: Ninja's training
difficulty: Medium
source: https://takeuforward.org/learning/dsa/ninja's-training?category=2d-dp&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, 2d-dp]
---
# 7. Ninja's training

← [House robber](06-house-robber.md) · [Part 28 index](README.md) · Next → [Grid unique paths](08-grid-unique-paths.md)

> [!abstract] Problem at a glance
> **Task:** Each day pick one of 3 activities (with given points); you can't repeat the previous day's activity. Maximise total points.
> **Key insight:** Today's choice depends on yesterday's, so the state needs that too: `dp[day][last]` = best points for days `0..day` when activity `last` is forbidden on `day`. Equivalently, `dp[d][t]` = best total ending with activity `t` on day `d`, and `dp[d][t] = p[d][t] + max_{t'≠t} dp[d−1][t']`.
> **Difficulty:** Medium · **Pattern:** 2D DP: (index, last choice)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/ninja's-training?category=2d-dp&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized recursion on (day, last)](#3-memoized-recursion-on-day-last) · [4. Tabulation with one row](#4-tabulation-with-one-row) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`points[d][t]` is the merit for doing activity `t ∈ {0,1,2}` on day `d`. Every day you do exactly one activity, never the same one on two consecutive days. Return the maximum total.

| Input | Output | Why |
|---|---|---|
| `points = [[1,2,5],[3,1,1],[3,3,3]]` | `11` | 5 (t2) + 3 (t0) + 3 (t1) |
| `points = [[10,40,70],[20,50,80],[30,60,90]]` | `210` | 70 + 50 + 90 |

**Constraints:** `1 ≤ n ≤ 10⁵`, `0 ≤ points[d][t] ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized recursion on (day, last) | f(d, last) = max over t ≠ last | O(n·4·3) | O(n·4) |
| Tabulation with one row | prev[t] = best ending with t yesterday | O(n·9) | O(1) |

> [!tip] Interview angle
> The lesson here is that when a choice constrains the next one, you add the previous choice to the state. Say "state = (day, last activity)" out loud. The rest is the familiar 1D pattern.

---

## 3. Memoized recursion on (day, last)

**Intuition.** `f(d, last)` = best from days `0..d` if activity `last` is banned on day `d` (`last = 3` means nothing banned). Try every `t ≠ last`: `p[d][t] + f(d−1, t)`. Base: `d = 0` returns the max over allowed `t`.

```python
def ninja_memo(p):
    n = len(p)
    dp = [[-1] * 4 for _ in range(n)]
    def f(d, last):
        if dp[d][last] != -1:
            return dp[d][last]
        best = 0
        for t in range(3):
            if t != last:
                best = max(best, p[d][t] + (f(d - 1, t) if d > 0 else 0))
        dp[d][last] = best
        return best
    return f(n - 1, 3)
```

**Complexity:** time **O(n·4·3)**, space **O(n·4)**.

---

## 4. Tabulation with one row

**Intuition.** Let `prev[t]` be the best total for days so far ending with activity `t`. Today `cur[t] = p[d][t] + max(prev[t'] for t' ≠ t)`. The answer is `max(prev)` after the last day.

**Algorithm**

1. `prev = p[0]` (copy).
2. For each later day `d`: `cur[t] = p[d][t] + max(prev[u] for u ≠ t)`; `prev = cur`.
3. Return `max(prev)`.

**Dry run** — [[1,2,5],[3,1,1],[3,3,3]]: prev = [1,2,5] → [3+5, 1+5, 1+2] = [8,6,3] → [3+6, 3+8, 3+8] = [9,11,11] → 11.

**C++**
```cpp
int ninjaTraining(vector<vector<int>>& p) {
    vector<int> prev = p[0];
    for (int d = 1; d < (int)p.size(); d++) {
        vector<int> cur(3, 0);
        for (int t = 0; t < 3; t++)
            for (int u = 0; u < 3; u++)
                if (u != t) cur[t] = max(cur[t], p[d][t] + prev[u]);
        prev = cur;
    }
    return *max_element(prev.begin(), prev.end());
}
```

**Java**
```java
static int ninjaTraining(int[][] p) {
    int[] prev = p[0].clone();
    for (int d = 1; d < p.length; d++) {
        int[] cur = new int[3];
        for (int t = 0; t < 3; t++)
            for (int u = 0; u < 3; u++)
                if (u != t) cur[t] = Math.max(cur[t], p[d][t] + prev[u]);
        prev = cur;
    }
    return Math.max(prev[0], Math.max(prev[1], prev[2]));
}
```

**Python**
```python
def ninja_training(p):
    prev = list(p[0])
    for d in range(1, len(p)):
        prev = [p[d][t] + max(prev[u] for u in range(3) if u != t) for t in range(3)]
    return max(prev)
```

**Complexity:** time **O(n·9)**, space **O(1)** — n days × 3 × 3 transitions, with one row of state.

---

## Edge cases

- One day: the max of that row.
- All rows equal: any alternating schedule is optimal.

---

## Common mistakes

1. Greedy max each day, which can forbid a bigger value tomorrow.
2. Using `last = −1` as an index (use 3 as the sentinel).
3. Updating `prev` in place while still reading it.

---

## Follow-ups

1. `k` activities instead of 3?
2. Same activity allowed but at most twice in a row?

<details><summary>Answer sketches</summary>

**#1:** Keep the best and second-best of `prev`. Then `cur[t] = p[d][t] + (best if argbest ≠ t else second)`, O(n·k).

**#2:** Add a run-length to the state: `(day, last, run)`.
</details>

---

## Flashcards

**Ninja's training state?** #flashcard
(day, last activity), with 3 or 4 values for last.

**Generic lesson?** #flashcard
When the previous choice restricts the next, put it in the state.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
