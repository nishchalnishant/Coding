---
module: striver-a2z/21-greedy-algorithms
lesson: 14
topic: Candy
difficulty: Hard
source: https://takeuforward.org/learning/dsa/candy?category=hard&source=strivers-a2z-dsa-sheet
tags: [striver, greedy-algorithms, greedy, array, two-pass]
---
# 14. Candy

← [Valid Parenthesis String](13-valid-parenthesis-string.md) · [Part 21 index](README.md) · Next → [Jump Game II](15-jump-game-ii.md)

> [!abstract] Problem at a glance
> **Task:** Children in a line have ratings; each gets ≥ 1 candy and a child with a higher rating than a neighbour gets more candy than that neighbour. Minimise total candy.
> **Key insight:** Split the two-sided constraint into two one-sided ones. Left pass enforces the left neighbour, right pass the right neighbour; taking the max of both satisfies both minimally.
> **Difficulty:** Hard · **Pattern:** Two passes (left & right constraints) · **Also on:** [LC 135](https://leetcode.com/problems/candy/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/candy?category=hard&source=strivers-a2z-dsa-sheet) · **Time:** 25 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Two passes](#3-two-passes) · [4. Slope counting, O(1) space](#4-slope-counting-o1-space) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given `ratings[0…n−1]`, give each child at least one candy such that any child with a strictly higher rating than an adjacent child gets more candy than that child. Return the minimum total.

| Input | Output | Why |
|---|---|---|
| `ratings = [1,0,2]` | `5` | 2,1,2 |
| `ratings = [1,2,2]` | `4` | 1,2,1 — equal neighbours have no constraint |
| `ratings = [1,3,4,5,2]` | `11` | 1,2,3,4,1 |

**Constraints:** `1 ≤ n ≤ 2·10⁴`, `0 ≤ ratings[i] ≤ 2·10⁴`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Two passes | L[i] from left, R[i] from right, sum max | O(n) | O(n) |
| Slope counting, O(1) space | sum peaks and valleys as triangles | O(n) | O(1) |

> [!tip] Interview angle
> Expected answer: two passes O(n)/O(n). Bonus: the O(1)-space slope-counting solution — walk up-slopes and down-slopes and add triangle numbers, fixing the peak with a max.

---

## 3. Two passes

**Intuition.** `L[i]` = minimum candies honouring only the left neighbour: `L[i] = L[i−1] + 1` if `r[i] > r[i−1]`, else 1. `R[i]` likewise from the right. Each child needs at least `max(L[i], R[i])`, and that assignment satisfies both sides.

**Dry run** — [1,0,2]: L = 1,1,2; R = 2,1,1; max = 2,1,2 → 5.

```python
def candy_two_pass(ratings):
    n = len(ratings)
    L = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            L[i] = L[i - 1] + 1
    total, R = max(L[-1], 1), 1
    for i in range(n - 2, -1, -1):
        R = R + 1 if ratings[i] > ratings[i + 1] else 1
        total += max(L[i], R)
    return total
```

**Complexity:** time **O(n)**, space **O(n)**.

---

## 4. Slope counting, O(1) space

**Intuition.** Walk the ratings as a mountain range. On an up-slope of length `up`, the children get 2, 3, …, up + 1. On the following down-slope of length `down` they get down, …, 1. The peak belongs to both slopes and must get `max(up, down) + 1` — so when `down` exceeds `up`, each extra down step also raises the peak by one.

**Algorithm**

1. `total = 1`, `up = down = peak = 0`.
2. Equal neighbours: reset `up = down = peak = 0`, `total += 1`.
3. Up step: `up++`, `peak = up`, `down = 0`, `total += up + 1`.
4. Down step: `down++`, `up = 0`, `total += down`, plus 1 more if `down > peak` (the peak must grow).
5. Return `total`.

**Dry run** — [1,3,4,5,2]: 1 → up 1 (+2), up 2 (+3), up 3 (+4) → peak 3; down 1: +1 (1 ≤ peak). Total 1+2+3+4+1 = 11.

**C++**
```cpp
int candy(vector<int>& r) {
    int n = r.size(), total = 1, up = 0, down = 0, peak = 0;
    for (int i = 1; i < n; i++) {
        if (r[i] > r[i - 1]) { up++; peak = up; down = 0; total += up + 1; }
        else if (r[i] == r[i - 1]) { up = down = peak = 0; total += 1; }
        else { up = 0; down++; total += down + (down > peak ? 1 : 0); }
    }
    return total;
}
```

**Java**
```java
static int candy(int[] r) {
    int n = r.length, total = 1, up = 0, down = 0, peak = 0;
    for (int i = 1; i < n; i++) {
        if (r[i] > r[i - 1]) { up++; peak = up; down = 0; total += up + 1; }
        else if (r[i] == r[i - 1]) { up = down = peak = 0; total += 1; }
        else { up = 0; down++; total += down + (down > peak ? 1 : 0); }
    }
    return total;
}
```

**Python**
```python
def candy(ratings):
    total, up, down, peak = 1, 0, 0, 0
    for i in range(1, len(ratings)):
        if ratings[i] > ratings[i - 1]:
            up += 1; peak = up; down = 0
            total += up + 1
        elif ratings[i] == ratings[i - 1]:
            up = down = peak = 0
            total += 1
        else:
            up = 0; down += 1
            total += down + (1 if down > peak else 0)
    return total
```

**Complexity:** time **O(n)**, space **O(1)** — one pass, four counters.

---

## Edge cases

- Single child → 1.
- Equal neighbours impose nothing (each can be 1).
- Strictly decreasing — peak at the start grows to n.

---

## Common mistakes

1. Taking `L[i] + R[i] − 1` or a sum instead of the max.
2. Treating equal ratings as needing equal candy.
3. One pass only (left constraints) — violates right neighbours.

---

## Follow-ups

1. Circular arrangement.
2. Constraint on both sides in a 2D grid.

<details><summary>Answer sketches</summary>

**#1:** Start the passes at a global minimum (which can safely get 1) and unroll the circle.

**#2:** Process cells in increasing rating order: `c = 1 + max(c of lower-rated neighbours)` — a DAG longest path.
</details>

---

## Flashcards

**Candy two-pass rule?** #flashcard
L from left (+1 on rise), R from right (+1 on rise leftwards); answer Σ max(L, R).

**Why is max(L, R) optimal?** #flashcard
Each is a lower bound for that child, and the max satisfies both neighbours simultaneously.

**Interview track →** [Greedy deep-dive](../../02-algorithms/16-greedy.md) · [Greedy walkthroughs](../../04-practice/algorithms/16-greedy.md)
