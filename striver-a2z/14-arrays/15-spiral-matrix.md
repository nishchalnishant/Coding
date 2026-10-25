---
module: striver-a2z/14-arrays
lesson: 15
topic: Print the Matrix in Spiral Manner
difficulty: Medium
source: https://takeuforward.org/learning/dsa/print-the-matrix-in-spiral-manner?category=faqs-medium&source=strivers-a2z-dsa-sheet
tags: [striver, arrays, matrix, simulation]
---
# 15. Print the Matrix in Spiral Manner

← [Rearrange Array Elements by Sign](14-rearrange-by-sign.md) · [Part 14 index](README.md) · Next → [Pascal's Triangle I](16-pascals-triangle-i.md)

> [!abstract] Problem at a glance
> **Task:** Return the elements of an m × n matrix in clockwise spiral order.
> **Key insight:** Keep four boundaries: `top`, `bottom`, `left`, `right`. Walk right along `top`, down along `right`, left along `bottom`, up along `left`, shrinking each boundary after its side. Guard the last two walks with `top <= bottom` / `left <= right` for single rows and columns.
> **Difficulty:** Medium · **Pattern:** Matrix boundary simulation · **Also on:** [LC 54](https://leetcode.com/problems/spiral-matrix/)
> **Source:** [takeuforward problem](https://takeuforward.org/learning/dsa/print-the-matrix-in-spiral-manner?category=faqs-medium&source=strivers-a2z-dsa-sheet) · **Time:** 20 min

**Sections:** [1. Problem](#1-problem) · [2. Approaches at a glance](#2-approaches-at-a-glance) · [3. Four boundaries](#3-four-boundaries) · [Edge cases](#edge-cases) · [Common mistakes](#common-mistakes) · [Follow-ups](#follow-ups) · [Flashcards](#flashcards)

---

## 1. Problem

Given an `m × n` matrix, return all of its elements in spiral order, starting from the top-left and moving clockwise.

| Input | Output | Why |
|---|---|---|
| `[[1,2,3],[4,5,6],[7,8,9]]` | `[1,2,3,6,9,8,7,4,5]` |  |
| `[[1,2,3,4],[5,6,7,8],[9,10,11,12]]` | `[1,2,3,4,8,12,11,10,9,5,6,7]` |  |

**Constraints:** `1 ≤ m, n ≤ 100`.

---

## 2. Approaches at a glance

| Approach | Idea | Time | Space |
|---|---|---|---|
| Four boundaries | right, down, left, up; shrink after each side | O(m · n) | O(1) beyond the output |

> [!tip] Interview angle
> The bugs are all in non-square inputs. Before coding, say you'll test a single row, a single column and a 3 × 4 matrix, then actually trace one of them.

---

## 3. Four boundaries

**Intuition.** Each loop of the spiral peels one ring. After the top row, `top++`; after the right column, `right−−`. The bottom row and left column are only walked if a row or column still remains, otherwise the middle row or column of an odd-sized shape is printed twice.

**Algorithm**

1. `top = 0`, `bottom = m − 1`, `left = 0`, `right = n − 1`.
2. While `top <= bottom && left <= right`:
3.   `left..right` on row `top`; `top++`.
4.   `top..bottom` on column `right`; `right−−`.
5.   If `top <= bottom`: `right..left` on row `bottom`; `bottom−−`.
6.   If `left <= right`: `bottom..top` on column `left`; `left++`.

**Dry run** — 3 × 4: row 0 → 1 2 3 4 (top=1); col 3 → 8 12 (right=2); row 2 ← 11 10 9 (bottom=1); col 0 ↑ 5 (left=1); row 1 → 6 7 (top=2); col 2: top > bottom, empty; guards stop the rest.

**Direction-vector alternative:** `dr = [0,1,0,−1]`, `dc = [1,0,−1,0]` with a `visited` grid; turn right when the next cell is out of bounds or visited. Easier to get right, O(mn) extra space.

**C++**
```cpp
vector<int> spiralOrder(vector<vector<int>>& mat) {
    vector<int> res;
    int top = 0, bottom = mat.size() - 1, left = 0, right = mat[0].size() - 1;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; c++) res.push_back(mat[top][c]);
        top++;
        for (int r = top; r <= bottom; r++) res.push_back(mat[r][right]);
        right--;
        if (top <= bottom) {
            for (int c = right; c >= left; c--) res.push_back(mat[bottom][c]);
            bottom--;
        }
        if (left <= right) {
            for (int r = bottom; r >= top; r--) res.push_back(mat[r][left]);
            left++;
        }
    }
    return res;
}
```

**Java**
```java
static List<Integer> spiralOrder(int[][] mat) {
    List<Integer> res = new ArrayList<>();
    int top = 0, bottom = mat.length - 1, left = 0, right = mat[0].length - 1;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; c++) res.add(mat[top][c]);
        top++;
        for (int r = top; r <= bottom; r++) res.add(mat[r][right]);
        right--;
        if (top <= bottom) {
            for (int c = right; c >= left; c--) res.add(mat[bottom][c]);
            bottom--;
        }
        if (left <= right) {
            for (int r = bottom; r >= top; r--) res.add(mat[r][left]);
            left++;
        }
    }
    return res;
}
```

**Python**
```python
def spiral_order(mat):
    res = []
    top, bottom, left, right = 0, len(mat) - 1, 0, len(mat[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res.append(mat[top][c])
        top += 1
        for r in range(top, bottom + 1):
            res.append(mat[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(mat[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(mat[r][left])
            left += 1
    return res
```

**Complexity:** time **O(m · n)**, space **O(1) beyond the output**.

---

## Edge cases

- 1 × n and m × 1.
- 1 × 1.
- m ≠ n, both odd and even.

---

## Common mistakes

1. Missing the `top <= bottom` / `left <= right` guards → the middle row/column is duplicated.
2. Shrinking a boundary before walking its side.
3. Off-by-one in the reverse loops (`range(right, left − 1, −1)`).

---

## Follow-ups

1. Spiral Matrix II (LC 59): fill 1..n² in spiral order.
2. Anticlockwise or starting from the centre?
3. Spiral order of a matrix too big for one pass?

<details><summary>Answer sketches</summary>

**#1:** Same boundary loop, writing a counter instead of reading.

**#2:** Change the side order, or generate clockwise and reverse.

**#3:** Each ring is independent; process ring by ring.
</details>

---

## Flashcards

**Spiral matrix: four variables?** #flashcard
top, bottom, left, right.

**Spiral matrix: why the extra guards?** #flashcard
After top++ / right−−, a single remaining row or column would be walked twice.

**Spiral order alternative?** #flashcard
Direction vectors + visited grid; turn on wall/visited.

**Interview track →** [Array deep-dive](../../01-data-structures/01-array.md) · [Array walkthroughs](../../04-practice/data-structures/01-array.md) · [Matrix deep-dive](../../01-data-structures/04-matrix.md) · [Matrix walkthroughs](../../04-practice/data-structures/04-matrix.md) · [Two pointers](../../02-algorithms/03-two-pointers.md)
