---
module: striver/21-greedy-algorithms
lesson: 15
topic: Jump Game II
difficulty: Medium
source: https://takeuforward.org/learning/dsa/jump-game-ii?category=hard&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, bfs, array]
---
# 15. Jump Game II

← [Candy](14-candy.md) · [Part 21 index](README.md) · Next → [Minimum coins (greedy, canonical denominations)](16-minimum-coins-greedy-canonical-denominations.md)

> [!abstract] Problem at a glance
> **Task:** Return the minimum number of jumps to reach the last index (it's guaranteed reachable).
> **Key insight:** Implicit BFS: indices reachable in exactly k jumps form a contiguous window. Sweep each window, record the farthest index it can reach — that's the next window. Count windows.
> **Difficulty:** Medium · **Pattern:** BFS by levels over index ranges · **Also on:** [LC 45](https://leetcode.com/problems/jump-game-ii/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/jump-game-ii?category=hard&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DP: min jumps per index](#3-dp-min-jumps-per-index) · [4. Greedy level window](#4-greedy-level-window) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `nums` where `nums[i]` is the maximum jump length from index i, return the minimum number of jumps to reach index `n − 1` from index 0. The end is always reachable.

| Input | Output | Why |
|---|---|---|
| `nums = [2,3,1,1,4]` | `2` | 0 → 1 → 4 |
| `nums = [2,3,0,1,4]` | `2` |  |

**Constraints:** `1 ≤ n ≤ 10⁴`, `0 ≤ nums[i] ≤ 1000`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DP: min jumps per index | dp[j] = min(dp[i] + 1) over i that reach j | O(n · max(nums)) | O(n) |
| Greedy level window | [l, r] window per jump; next r = max(i + nums[i]) | O(n) | O(1) |

> [!tip] Interview angle
> Name it as BFS on a graph where index i has edges to i+1…i+nums[i], then show that BFS layers are contiguous ranges, so the queue collapses to two integers. That framing is what earns the hire signal.

---

## 3. DP: min jumps per index

**Intuition.** `dp[0] = 0`; relax every target from every index. Correct but quadratic.

```python
def jump_dp(nums):
    n = len(nums)
    INF = float('inf')
    dp = [INF] * n
    dp[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            dp[j] = min(dp[j], dp[i] + 1)
    return dp[-1]
```

**Complexity:** time **O(n · max(nums))**, space **O(n)**.

---

## 4. Greedy level window

**Intuition.** Window `[l, r]` = indices reachable with exactly `jumps` jumps (start: `[0, 0]`). From the window, the farthest reachable index is `max(i + nums[i])`; the next window is `[r + 1, farthest]`. Stop when `r ≥ n − 1`.

**Algorithm**

1. `jumps = 0, l = r = 0`.
2. While `r < n − 1`: `far = max(i + nums[i] for i in [l, r])`; `l = r + 1`; `r = far`; `jumps++`.
3. Return `jumps`.

**Dry run** — [2,3,1,1,4]: window [0,0] → far 2 → [1,2], jumps 1 → far max(4, 3) = 4 → [3,4], jumps 2 → r ≥ 4 stop.

**Common compact form:** one loop over `i < n − 1` keeping `end` and `far`; when `i == end`, `jumps++`, `end = far`. Identical logic.

**C++**
```cpp
int jump(vector<int>& nums) {
    int n = nums.size(), jumps = 0, l = 0, r = 0;
    while (r < n - 1) {
        int far = 0;
        for (int i = l; i <= r; i++) far = max(far, i + nums[i]);
        l = r + 1;
        r = far;
        jumps++;
    }
    return jumps;
}
```

**Java**
```java
static int jump(int[] nums) {
    int n = nums.length, jumps = 0, l = 0, r = 0;
    while (r < n - 1) {
        int far = 0;
        for (int i = l; i <= r; i++) far = Math.max(far, i + nums[i]);
        l = r + 1;
        r = far;
        jumps++;
    }
    return jumps;
}
```

**Python**
```python
def jump(nums):
    n, jumps, l, r = len(nums), 0, 0, 0
    while r < n - 1:
        far = max(i + nums[i] for i in range(l, r + 1))
        l, r = r + 1, far
        jumps += 1
    return jumps
```

**Complexity:** time **O(n)**, space **O(1)** — every index is in exactly one window, so the total work is O(n).

---

## Edge cases

- n = 1 → 0 jumps.
- First jump already reaches the end.
- If reachability weren't guaranteed, `far ≤ r` would mean stuck → return −1.

---

## Common mistakes

1. Jumping to the index with the biggest `nums[i]` instead of the biggest `i + nums[i]`.
2. Counting a jump when already at the last index (loop on `i < n − 1`).
3. Infinite loop when unreachable and no stuck check.

---

## Follow-ups

1. Can't guarantee reachability.
2. Jump Game VII / VI (LC 1871, 1696).

<details><summary>Answer sketches</summary>

**#1:** If a level yields `far ≤ r`, return −1.

**#2:** Sliding window over reachable positions; monotonic deque for max-score DP.
</details>

---

## Flashcards

**Jump Game II in O(n)?** #flashcard
BFS levels as index windows: next window ends at `max(i + nums[i])` over the current window.

**Why are BFS levels contiguous ranges?** #flashcard
If you can reach j in ≤ k jumps you can reach every index < j in ≤ k jumps.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../coding/algorithms/16-greedy.md)
