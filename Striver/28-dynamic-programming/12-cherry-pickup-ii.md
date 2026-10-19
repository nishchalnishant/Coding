---
module: striver/28-dynamic-programming
lesson: 12
topic: Cherry pickup II
difficulty: Hard
source: https://takeuforward.org/learning/dsa/cherry-pickup-ii?category=dp-on-grids&source=strivers-a2z-dsa-sheet
tags: [striver, dynamic-programming, dp, grid, 3d-dp]
---
# 12. Cherry pickup II

← [Triangle](11-triangle.md) · [Part 28 index](README.md) · Next → [Count Square Submatrices with All Ones](13-count-square-submatrices-with-all-ones.md)

> [!abstract] Problem at a glance
> **Task:** Two robots start at the top-left and top-right corners and move down one row at a time (column −1/0/+1). Maximise the cherries collected; a shared cell counts once.
> **Key insight:** Both robots are always on the **same row**, so the state is `(row, c1, c2)`, which is 3D rather than 4D. Each step tries 3×3 = 9 move pairs. Add `g[r][c1] + g[r][c2]`, counting once if `c1 == c2`.
> **Difficulty:** Hard · **Pattern:** 3D DP: two agents moving in lockstep · **Also on:** LC 1463
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/cherry-pickup-ii?category=dp-on-grids&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Memoized recursion on (r, c1, c2)](#3-memoized-recursion-on-r-c1-c2) · [4. Bottom-up with a 2D layer](#4-bottom-up-with-a-2d-layer) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`grid` is `rows × cols`. Robot A starts at `(0, 0)` and robot B at `(0, cols−1)`. Each step, both move to the next row, each to column `c−1`, `c` or `c+1` (staying in the grid). A robot collects the cherries of every cell it visits, and a cell visited by both is counted once. Return the maximum total after both reach the last row.

| Input | Output | Why |
|---|---|---|
| `[[3,1,1],[2,5,1],[1,5,5],[2,1,1]]` | `24` | A: 3+2+5+2 = 12, B: 1+5+5+1 = 12 |
| `[[1,0,0,0,0,0,1],[2,0,0,0,0,3,0],[2,0,9,0,0,0,0],[0,3,0,5,4,0,0],[1,0,2,3,0,0,6]]` | `28` |  |

**Constraints:** `2 ≤ rows, cols ≤ 70`, `0 ≤ grid[i][j] ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Memoized recursion on (r, c1, c2) | 9 transitions per state | O(R·C²·9) | O(R·C²) |
| Bottom-up with a 2D layer | front[c1][c2] from the row below | O(R·C²·9) | O(C²) |

> [!tip] Interview angle
> Explain why the state is 3D: "Both robots advance one row per step, so a single row index describes both." This is the same trick as Cherry Pickup I, where `r1 + c1 = r2 + c2` collapses one coordinate.

---

## 3. Memoized recursion on (r, c1, c2)

**Intuition.** `f(r, c1, c2)` = max cherries from row `r` down, with robots at `c1` and `c2`. Out-of-grid columns give −∞. In the last row, return what is collected there.

```python
def cherry_memo(g):
    R, C = len(g), len(g[0])
    from functools import lru_cache
    @lru_cache(None)
    def f(r, c1, c2):
        if c1 < 0 or c2 < 0 or c1 >= C or c2 >= C:
            return float("-inf")
        here = g[r][c1] + (g[r][c2] if c1 != c2 else 0)
        if r == R - 1:
            return here
        return here + max(f(r + 1, c1 + d1, c2 + d2) for d1 in (-1, 0, 1) for d2 in (-1, 0, 1))
    return f(0, 0, C - 1)
```

**Complexity:** time **O(R·C²·9)**, space **O(R·C²)**.

---

## 4. Bottom-up with a 2D layer

**Intuition.** Process rows from the bottom. `front[c1][c2]` is the best from row `r+1` downward. Each new layer `cur` reads 9 cells of `front`, so only two `C × C` layers are kept.

**Algorithm**

1. `front[c1][c2] = g[R−1][c1] + (c1≠c2 ? g[R−1][c2] : 0)`.
2. For `r = R−2..0`: `cur[c1][c2] = here + max over valid (d1, d2) of front[c1+d1][c2+d2]`.
3. `front = cur`; return `front[0][C−1]`.

**Dry run** — [[3,1,1],[2,5,1],[1,5,5],[2,1,1]]: the best final layer value at (0, 2) is 24.

**C++**
```cpp
int cherryPickup(vector<vector<int>>& g) {
    int R = g.size(), C = g[0].size();
    vector<vector<int>> front(C, vector<int>(C));
    for (int a = 0; a < C; a++)
        for (int b = 0; b < C; b++)
            front[a][b] = g[R - 1][a] + (a != b ? g[R - 1][b] : 0);
    for (int r = R - 2; r >= 0; r--) {
        vector<vector<int>> cur(C, vector<int>(C));
        for (int a = 0; a < C; a++)
            for (int b = 0; b < C; b++) {
                int best = INT_MIN;
                for (int da = -1; da <= 1; da++)
                    for (int db = -1; db <= 1; db++) {
                        int na = a + da, nb = b + db;
                        if (na >= 0 && na < C && nb >= 0 && nb < C) best = max(best, front[na][nb]);
                    }
                cur[a][b] = g[r][a] + (a != b ? g[r][b] : 0) + best;
            }
        front = cur;
    }
    return front[0][C - 1];
}
```

**Java**
```java
static int cherryPickup(int[][] g) {
    int R = g.length, C = g[0].length;
    int[][] front = new int[C][C];
    for (int a = 0; a < C; a++)
        for (int b = 0; b < C; b++)
            front[a][b] = g[R - 1][a] + (a != b ? g[R - 1][b] : 0);
    for (int r = R - 2; r >= 0; r--) {
        int[][] cur = new int[C][C];
        for (int a = 0; a < C; a++)
            for (int b = 0; b < C; b++) {
                int best = Integer.MIN_VALUE;
                for (int da = -1; da <= 1; da++)
                    for (int db = -1; db <= 1; db++) {
                        int na = a + da, nb = b + db;
                        if (na >= 0 && na < C && nb >= 0 && nb < C) best = Math.max(best, front[na][nb]);
                    }
                cur[a][b] = g[r][a] + (a != b ? g[r][b] : 0) + best;
            }
        front = cur;
    }
    return front[0][C - 1];
}
```

**Python**
```python
def cherry_pickup(g):
    R, C = len(g), len(g[0])
    front = [[g[R - 1][a] + (g[R - 1][b] if a != b else 0) for b in range(C)] for a in range(C)]
    for r in range(R - 2, -1, -1):
        cur = [[0] * C for _ in range(C)]
        for a in range(C):
            for b in range(C):
                best = max(front[na][nb]
                           for na in (a - 1, a, a + 1) if 0 <= na < C
                           for nb in (b - 1, b, b + 1) if 0 <= nb < C)
                cur[a][b] = g[r][a] + (g[r][b] if a != b else 0) + best
        front = cur
    return front[0][C - 1]
```

**Complexity:** time **O(R·C²·9)**, space **O(C²)** — R·C² states, 9 transitions each; two C × C layers.

---

## Edge cases

- `cols = 2`: the robots can meet; count a shared cell once.
- Cells may be 0 everywhere: answer 0.

---

## Common mistakes

1. Counting a shared cell twice.
2. Using a 4D state `(r1, c1, r2, c2)` when `r1 = r2` always.
3. Using 0 for invalid columns in a max DP (any negative-free grid hides the bug; use −∞ or skip them).

---

## Follow-ups

1. Cherry Pickup I (one robot there and back, with obstacles)?
2. k robots?

<details><summary>Answer sketches</summary>

**#1:** Model it as two robots going forward in lockstep: state `(steps, r1, r2)` with `c = steps − r`.

**#2:** State `(row, c1..ck)` grows as C^k, so it is only feasible for tiny k.
</details>

---

## Flashcards

**Cherry pickup II state?** #flashcard
(row, c1, c2), since both robots share the row.

**Transitions per state?** #flashcard
3 × 3 = 9 column-move pairs.

**Shared cell rule?** #flashcard
Add it once when c1 == c2.

**Interview track →** [DP deep-dive](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · [Recursion & DP masterclass](../../03-patterns/RECURSION_AND_DP_MASTERCLASS.md) · [DP walkthroughs](../../coding/algorithms/15-dynamic-programming.md)
