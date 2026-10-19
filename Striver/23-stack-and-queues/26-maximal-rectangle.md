---
module: striver/23-stack-and-queues
lesson: 26
topic: Maximum Rectangles
difficulty: Hard
source: https://takeuforward.org/learning/dsa/maximum-rectangles?category=faqs&source=strivers-a2z-dsa-sheet
tags: [striver, stack-and-queues, stack, monotonic-stack, matrix, dp]
---
# 26. Maximum Rectangles

← [Largest rectangle in a histogram](25-largest-rectangle-in-a-histogram.md) · [Part 23 index](README.md) · Next → [Stock span problem](27-stock-span-problem.md)

> [!abstract] Problem at a glance
> **Task:** Largest all-1s rectangle in a binary matrix.
> **Key insight:** Treat each row as the **floor of a histogram**: `heights[j]` = number of consecutive 1s ending at this row in column `j` (reset to 0 on a 0). Then the answer is the max over rows of Largest Rectangle in Histogram.
> **Difficulty:** Hard · **Pattern:** Row-wise histogram + monotonic stack · **Also on:** [LC 85](https://leetcode.com/problems/maximal-rectangle/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/maximum-rectangles?category=faqs&source=strivers-a2z-dsa-sheet) · **Time:** 30 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Histogram per row, quadratic scan](#3-histogram-per-row-quadratic-scan) · [4. Histogram per row + monotonic stack](#4-histogram-per-row--monotonic-stack) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `R × C` binary matrix, return the area of the largest rectangle containing only 1s.

| Input | Output | Why |
|---|---|---|
| `[[1,0,1,0,0],[1,0,1,1,1],[1,1,1,1,1],[1,0,0,1,0]]` | `6` | rows 1–2, columns 2–4 |
| `[[0]]` | `0` |  |

**Constraints:** `1 ≤ R, C ≤ 200`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Histogram per row, quadratic scan | heights per row, O(C²) best rectangle | O(R·C²) | O(C) |
| Histogram per row + monotonic stack | update heights, run largest-rectangle per row | O(R·C) | O(C) |

> [!tip] Interview angle
> Recognising the reduction is the whole problem. Say it in one sentence: 'every rectangle has a bottom row; for that row, column heights form a histogram.' Reuse the histogram routine as a helper.

---

## 3. Histogram per row, quadratic scan

**Intuition.** Same reduction, but solve each histogram by expanding from each start column with a running minimum.

```python
def maxrect_slow(mat):
    if not mat:
        return 0
    C, best = len(mat[0]), 0
    h = [0] * C
    for row in mat:
        for j in range(C):
            h[j] = h[j] + 1 if row[j] else 0
        for l in range(C):
            m = h[l]
            for r in range(l, C):
                m = min(m, h[r])
                best = max(best, m * (r - l + 1))
    return best
```

**Complexity:** time **O(R·C²)**, space **O(C)**.

---

## 4. Histogram per row + monotonic stack

**Intuition.** The height update is O(C) per row and the one-pass histogram is O(C), so the whole thing is linear in the matrix size.

**Algorithm**

1. `h = [0]·C`.
2. For each row: `h[j] = h[j] + 1` if the cell is 1, else 0.
3. `best = max(best, largestRectangleArea(h))`.

**Dry run** — Sample: row 0 → h [1,0,1,0,0] → 1. Row 1 → [2,0,2,1,1] → 3. Row 2 → [3,1,3,2,2] → 6 (height 2 × width 3). Row 3 → [4,0,0,3,0] → 4. Best 6.

**C++**
```cpp
int histArea(const vector<int>& h) {
    int n = h.size(), best = 0;
    vector<int> st;
    for (int i = 0; i <= n; i++) {
        int cur = i == n ? 0 : h[i];
        while (!st.empty() && h[st.back()] >= cur) {
            int t = st.back(); st.pop_back();
            int left = st.empty() ? -1 : st.back();
            best = max(best, h[t] * (i - left - 1));
        }
        st.push_back(i);
    }
    return best;
}
int maximalRectangle(vector<vector<int>> mat) {
    if (mat.empty()) return 0;
    int C = mat[0].size(), best = 0;
    vector<int> h(C, 0);
    for (auto& row : mat) {
        for (int j = 0; j < C; j++) h[j] = row[j] ? h[j] + 1 : 0;
        best = max(best, histArea(h));
    }
    return best;
}
```

**Java**
```java
static int histArea(int[] h) {
    int n = h.length, best = 0;
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i <= n; i++) {
        int cur = i == n ? 0 : h[i];
        while (!st.isEmpty() && h[st.peek()] >= cur) {
            int t = st.pop();
            int left = st.isEmpty() ? -1 : st.peek();
            best = Math.max(best, h[t] * (i - left - 1));
        }
        st.push(i);
    }
    return best;
}
static int maximalRectangle(int[][] mat) {
    if (mat.length == 0) return 0;
    int C = mat[0].length, best = 0;
    int[] h = new int[C];
    for (int[] row : mat) {
        for (int j = 0; j < C; j++) h[j] = row[j] == 1 ? h[j] + 1 : 0;
        best = Math.max(best, histArea(h));
    }
    return best;
}
```

**Python**
```python
def maximal_rectangle(mat):
    if not mat:
        return 0
    def hist(h):
        n, best, st = len(h), 0, []
        for i in range(n + 1):
            cur = 0 if i == n else h[i]
            while st and h[st[-1]] >= cur:
                t = st.pop()
                left = st[-1] if st else -1
                best = max(best, h[t] * (i - left - 1))
            st.append(i)
        return best
    C, best = len(mat[0]), 0
    h = [0] * C
    for row in mat:
        for j in range(C):
            h[j] = h[j] + 1 if row[j] else 0
        best = max(best, hist(h))
    return best
```

**Complexity:** time **O(R·C)**, space **O(C)** — R rows × O(C) height update and O(C) histogram pass.

---

## Edge cases

- All zeros: 0.
- Single row / single column.
- LeetCode gives `char` cells (`'0'`/`'1'`): compare to `'1'`.

---

## Common mistakes

1. Not resetting height to 0 on a 0 cell (columns aren't contiguous).
2. Recomputing heights from scratch per row (O(R²C)).
3. Mixing up rows/columns when the matrix isn't square.

---

## Follow-ups

1. Largest square of 1s (LC 221)?
2. Count all-1 submatrices (LC 1504)?

<details><summary>Answer sketches</summary>

**#1:** DP: `dp[i][j] = 1 + min(top, left, diag)`; O(RC).

**#2:** Histogram per row + monotonic stack counting, O(RC).
</details>

---

## Flashcards

**Maximal rectangle reduction?** #flashcard
Each row is the floor of a histogram of consecutive-1 heights; run largest-rectangle-in-histogram per row.

**Height update rule for maximal rectangle?** #flashcard
h[j] = cell ? h[j] + 1 : 0.

**Interview track →** [Stack deep-dive](../../01-data-structures/05-stack.md) · [Queue deep-dive](../../01-data-structures/06-queue.md)
