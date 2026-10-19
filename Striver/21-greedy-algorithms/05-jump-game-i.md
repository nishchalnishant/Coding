---
module: striver/21-greedy-algorithms
lesson: 5
topic: Jump Game I
difficulty: Medium
source: https://takeuforward.org/learning/dsa/jump-game---i?category=easy&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, array]
---
# 5. Jump Game I

← [Fractional Knapsack](04-fractional-knapsack.md) · [Part 21 index](README.md) · Next → [Shortest Job First](06-shortest-job-first.md)

> [!abstract] Problem at a glance
> **Task:** Each `nums[i]` is the maximum jump length from index i; can you reach the last index from index 0?
> **Key insight:** Track the farthest index reachable so far. If you ever stand at an index beyond it, you're stuck; otherwise extend it with `i + nums[i]`.
> **Difficulty:** Medium · **Pattern:** Farthest-reach scan · **Also on:** [LC 55](https://leetcode.com/problems/jump-game/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/jump-game---i?category=easy&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. DP: reachable[i]](#3-dp-reachablei) · [4. Greedy farthest reach](#4-greedy-farthest-reach) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an array `nums`, you start at index 0 and from index `i` can jump to any index in `[i + 1, i + nums[i]]`. Return `true` if you can reach the last index.

| Input | Output | Why |
|---|---|---|
| `nums = [2,3,1,1,4]` | `true` | 0 → 1 → 4 |
| `nums = [3,2,1,0,4]` | `false` | everything funnels into index 3, which has 0 |

**Constraints:** `1 ≤ n ≤ 10⁴`, `0 ≤ nums[i] ≤ 10⁵`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| DP: reachable[i] | mark each reachable index forward | O(n·max(nums)) | O(n) |
| Greedy farthest reach | maxReach = max(maxReach, i + nums[i]) | O(n) | O(1) |

> [!tip] Interview angle
> Show the DP/recursion first only if asked; the expected answer is the O(n) reach scan with the argument "reachable indices always form a prefix".

---

## 3. DP: reachable[i]

**Intuition.** `ok[0] = true`; for each reachable i mark `i+1 … i+nums[i]`. Correct but quadratic in the worst case.

```python
def can_jump_dp(nums):
    n = len(nums)
    ok = [False] * n
    ok[0] = True
    for i in range(n):
        if ok[i]:
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                ok[j] = True
    return ok[-1]
```

**Complexity:** time **O(n·max(nums))**, space **O(n)**.

---

## 4. Greedy farthest reach

**Intuition.** The set of reachable indices is always a prefix `[0, maxReach]`: if you can reach j you can reach everything before it (you passed through on the way). Scan left to right; if `i > maxReach`, index i is unreachable, so the end is too.

**Dry run** — [3,2,1,0,4]: reach 3, 3, 3, 3 → at i = 4 > 3 → false.

**Backward variant:** keep `goal = n − 1`; scanning right to left, if `i + nums[i] ≥ goal` set `goal = i`. Answer `goal == 0`.

**C++**
```cpp
bool canJump(vector<int>& nums) {
    int reach = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        if (i > reach) return false;
        reach = max(reach, i + nums[i]);
    }
    return true;
}
```

**Java**
```java
static boolean canJump(int[] nums) {
    int reach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > reach) return false;
        reach = Math.max(reach, i + nums[i]);
    }
    return true;
}
```

**Python**
```python
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True
```

**Complexity:** time **O(n)**, space **O(1)** — one pass; reachable indices form a prefix.

---

## Edge cases

- Single element → true (already there).
- Zero at index 0 with n > 1 → false.
- Zeros that can be jumped over.

---

## Common mistakes

1. Returning false as soon as you see a 0 — it may be jumpable.
2. Checking `reach >= n − 1` but never checking `i > reach`.

---

## Follow-ups

1. Minimum number of jumps.
2. Can jump left or right exactly nums[i] (LC 1306).

<details><summary>Answer sketches</summary>

**#1:** Jump Game II — BFS by levels in O(n) (problem 14).

**#2:** BFS/DFS on indices.
</details>

---

## Flashcards

**Jump Game I in O(n)?** #flashcard
Track `reach`; fail if `i > reach`; update `reach = max(reach, i + nums[i])`.

**Why is a single reach value enough?** #flashcard
Reachable indices always form a prefix of the array.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../coding/algorithms/16-greedy.md)
