---
module: striver-a2z/27-graphs
lesson: 7
topic: Flood fill algorithm
difficulty: Easy
source: https://takeuforward.org/learning/dsa/flood-fill-algorithm?category=traversal-problems&source=strivers-a2z-dsa-sheet
tags: [striver, graph, grid, dfs]
---
# 7. Flood fill algorithm

← [Number of islands](06-number-of-islands.md) · [Part 27 index](README.md) · Next → [Number of enclaves](08-number-of-enclaves.md)

> [!abstract] Problem at a glance
> **Task:** Recolour the 4-connected region of the pixel `(sr, sc)` (all pixels with its original colour) to `color`.
> **Key insight:** DFS from `(sr, sc)` over neighbours that still have the **original** colour, repainting as you go. The repainted colour doubles as the visited mark, except when `color == original`, where repainting changes nothing and the DFS would loop forever. Return immediately in that case.
> **Difficulty:** Easy · **Pattern:** Grid DFS from one source · **Also on:** LC 733
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/flood-fill-algorithm?category=traversal-problems&source=strivers-a2z-dsa-sheet) · **Time:** 10 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. BFS with a queue](#3-bfs-with-a-queue) · [4. Recursive DFS](#4-recursive-dfs) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

`image` is an `m × n` grid of integers. Starting from pixel `(sr, sc)`, change the colour of that pixel and of every pixel 4-directionally connected to it through pixels of the same original colour to `color`. Return the image.

| Input | Output | Why |
|---|---|---|
| `image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2` | `[[2,2,2],[2,2,0],[2,0,1]]` | the bottom-right 1 is not connected to the centre |
| `image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0` | `[[0,0,0],[0,0,0]]` | same colour: nothing changes |

**Constraints:** `1 ≤ m, n ≤ 50`, `0 ≤ colours < 2¹⁶`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| BFS with a queue | queue from the source, repaint on push | O(m·n) | O(m·n) |
| Recursive DFS | repaint, recurse on same-colour neighbours | O(m·n) | O(m·n) recursion |

> [!tip] Interview angle
> Raise the `color == original` case before the interviewer does. It is the whole trick of this question.

---

## 3. BFS with a queue

**Intuition.** Push the source and repaint it; pop cells, and push and repaint any neighbour that still has the original colour. Uses the same early exit for `color == original`.

```python
from collections import deque

def flood_fill_bfs(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    R, C = len(image), len(image[0])
    image[sr][sc] = color
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= a < R and 0 <= b < C and image[a][b] == old:
                image[a][b] = color
                q.append((a, b))
    return image
```

**Complexity:** time **O(m·n)**, space **O(m·n)**.

---

## 4. Recursive DFS

**Intuition.** `fill(r, c)`: if out of bounds or the pixel is not the original colour, return; else repaint and recurse in 4 directions. The grid is at most 50×50, so recursion depth is fine.

**Algorithm**

1. `old = image[sr][sc]`; if `old == color`, return the image unchanged.
2. `fill(r, c)`: stop if out of bounds or `image[r][c] != old`.
3. Otherwise set `image[r][c] = color` and call `fill` on the 4 neighbours.
4. Call `fill(sr, sc)` and return the image.

**Dry run** — Example 1: old = 1 at (1,1). Repaint (1,1) → (0,1) → (0,0) → (1,0) → (2,0) → (0,2). (1,2) and (2,1) are 0; (2,2) is never reached.

**C++**
```cpp
void fill(vector<vector<int>>& img, int r, int c, int old, int color) {
    if (r < 0 || r >= (int)img.size() || c < 0 || c >= (int)img[0].size() || img[r][c] != old) return;
    img[r][c] = color;
    fill(img, r + 1, c, old, color); fill(img, r - 1, c, old, color);
    fill(img, r, c + 1, old, color); fill(img, r, c - 1, old, color);
}
vector<vector<int>> floodFill(vector<vector<int>>& image, int sr, int sc, int color) {
    int old = image[sr][sc];
    if (old != color) fill(image, sr, sc, old, color);
    return image;
}
```

**Java**
```java
static void fill(int[][] img, int r, int c, int old, int color) {
    if (r < 0 || r >= img.length || c < 0 || c >= img[0].length || img[r][c] != old) return;
    img[r][c] = color;
    fill(img, r + 1, c, old, color); fill(img, r - 1, c, old, color);
    fill(img, r, c + 1, old, color); fill(img, r, c - 1, old, color);
}
static int[][] floodFill(int[][] image, int sr, int sc, int color) {
    int old = image[sr][sc];
    if (old != color) fill(image, sr, sc, old, color);
    return image;
}
```

**Python**
```python
def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    R, C = len(image), len(image[0])
    def fill(r, c):
        if r < 0 or r >= R or c < 0 or c >= C or image[r][c] != old:
            return
        image[r][c] = color
        fill(r + 1, c); fill(r - 1, c); fill(r, c + 1); fill(r, c - 1)
    fill(sr, sc)
    return image
```

**Complexity:** time **O(m·n)**, space **O(m·n) recursion** — each pixel is repainted at most once; recursion depth is bounded by the region size.

---

## Edge cases

- `color` equals the original colour: return unchanged (otherwise infinite recursion).
- 1×1 image: just repaint.
- Same colour reachable only diagonally: not part of the region.

---

## Common mistakes

1. Missing the `old == color` guard, causing infinite recursion / stack overflow.
2. Comparing neighbours to `color` instead of `old`.
3. Reading `image[sr][sc]` after repainting it.

---

## Follow-ups

1. Return the number of repainted pixels?
2. Paint-bucket with 8-connectivity?

<details><summary>Answer sketches</summary>

**#1:** Count inside `fill`, or return 1 + the sum of the recursive calls.

**#2:** Recurse into 8 neighbours.
</details>

---

## Flashcards

**The flood-fill trap?** #flashcard
`color == original` → return immediately.

**Visited set in flood fill?** #flashcard
The new colour acts as the mark.

**Interview track →** [Graph deep-dive](../../01-data-structures/13-graphs.md) · [Graph algorithms](../../04-practice/algorithms/13-graph-algorithms.md)
